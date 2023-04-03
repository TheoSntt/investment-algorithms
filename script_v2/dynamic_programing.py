"""This scripts finds the correct solution to the best investment problem in less than a minute.
It needs 3 arguments to be run :
- in_file : The input file containing the shares to evaluate. If you downloaded the whole repository on GitHub,
correct values include --in_file="../data/dataset1.csv" or --in_file="../data/dataset2.csv"
- out_file : The output file in which the selected shares will be written.
An example value could be --out_file="../results/dynamic_programing_result.csv"
- include_neg : In the datasets, some data have negative values. We can either suppose that the correct value is their
positive counterpart, and include them, or suppose that the correct value can't be deduced, and exclude them. By adding
the --include_neg flag in the command prompt, you include the values. Without the flag, they are excluded.
"""

import csv
import time
import argparse


def make_list_from_csv_multiply(csv_file_path, include_negative_numbers):
    """This function takes the input CSV file containing the shares and converts it to an array containing
    Python objects with names, prices and profits. The array is the input of the algorithm.
    In this script, the price and profit and multiplied by 100 so the decimal numbers become integers.
    It is needed to be able to use the dynamic programing approach to this problem.
    Also, the input data includes incorrect values (0 and negative numbers). This function deals with them."""
    data = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
                if include_negative_numbers:
                    try:
                        price = abs(float(row[1]))
                        profit = abs(float(row[2]))
                        if price != 0 and profit != 0:
                            data.append({"name": row[0],
                                         "price": int(price*100),
                                         "profit": int(profit*100*price*100)})
                    except ValueError:
                        pass
                else:
                    try:
                        price = float(row[1])
                        profit = float(row[2])
                        if price > 0 and profit > 0:
                            data.append({"name": row[0],
                                         "price": int(price*100),
                                         "profit": int(profit*100*price*100)})
                    except ValueError:
                        pass
    print(f"Données en entrée : {len(data)} actions ont été conservées "
          f"sur les {line_count - 1} présentes dans le fichier")
    return data


def create_csv_from_results(csv_file_path, best_combination, best_profit):
    """This function is called on the results of the algorithm. It creates a CSV file containing the results :
    the shares selected by the algorithm and the total price and profit obtained.
    In this script the data is divided back to its original values, to compensate the multiplication done in
    the previous function."""
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        # Creating the csv writer object and writing the header
        writer = csv.writer(csv_file, delimiter=',')
        en_tete = ['name',
                   'price',
                   'profit (%)',
                   'profit (euros)']
        writer.writerow(en_tete)
        for share in best_combination:
            price = share['price']/100
            profit_euros = share['profit']/1000000
            profit_percent = profit_euros*100/price
            row = [share['name'],
                   str(price).replace(".", ","),
                   str(profit_percent)[:5].replace(".", ","),
                   str(profit_euros).replace(".", ",")]
            writer.writerow(row)
        writer.writerow(["Prix total :",
                         str(sum(share['price']/100 for share in best_combination)).replace(".", ","),
                         "Profit total :",
                         str(best_profit/1000000).replace(".", ",")])


def dp_find_best_investments(objects, money_cap):
    """ Dynamic programing algorithm to solve our investment problem. It creates a 2D array and use it to store
    local optimal solutions, used to itarativly calculate wider local solution, until the final solution is reached.
    The dynamic programing approach to the knapsack problem (our problem is a variation of this problem) solves the
    problem in O(n*W) time (where n is the number of shares and W is the money cap). Since we need to multiply the 
    value by 100 with our data, it runs in 0(100*n*W time).
    """
    n = len(objects)
    dp = [[0] * (money_cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, money_cap + 1):
            if int(objects[i - 1]['price']) > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j],
                               dp[i - 1][j - objects[i - 1]['price']] + objects[i - 1]['profit'])

    max_value = dp[n][money_cap]
    selected_objects = []
    j = money_cap
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selected_objects.append(objects[i - 1])
            j -= int(objects[i - 1]['price'])
    selected_objects.reverse()

    return max_value, selected_objects


"""Creation of the user arguments"""
# Create an ArgumentParser object
parser = argparse.ArgumentParser()
# Add arguments to the parser
parser.add_argument("--in_file",
                    help="Data file containing the shares",
                    default="../data/demo_dataset.csv")
parser.add_argument("--out_file",
                    help="Output file in which the results will be written",
                    default="../results/bruteforce_results.csv")
parser.add_argument("--include_neg",
                    action="store_true",
                    help="Define whether to keep invalid negative data (as their positive counterpart) or exclude them")
# Parse the arguments
args = parser.parse_args()

"""Extracting the data from the CSV file into a Python list."""
shares = make_list_from_csv_multiply(args.in_file, args.include_neg)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit, max_profit_combination = dp_find_best_investments(shares, 50000)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"La meilleure combinaison permet un bénéfice de {max_profit/1000000} pour un "
      f"coût total de {sum(share['price']/100 for share in max_profit_combination)} euros.")

"""Writing the results to a csv file"""
max_profit_combination = sorted(max_profit_combination, key=lambda x: x['name'], reverse=False)
create_csv_from_results(args.out_file, max_profit_combination, max_profit)

