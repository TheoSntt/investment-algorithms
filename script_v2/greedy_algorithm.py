"""This scripts finds an approximate solution to the best investment problem in less than
a second. It needs 3 arguments to be run :
- in_file : The input file containing the shares to evaluate. If you downloaded the whole repository on GitHub,
correct values include --in_file="../data/dataset1.csv" or --in_file="../data/dataset2.csv"
- out_file : The output file in which the selected shares will be written.
An example value could be --out_file="../results/greedy_algorithm_result.csv"
- include_neg : In the datasets, some data have negative values. We can either suppose that the correct value is their
positive counterpart, and include them, or suppose that the correct value can't be deduced, and exclude them. By adding
the --include_neg flag in the command prompt, you include the values. Without the flag, they are excluded.
"""

import csv
import time
import argparse


def make_list_from_csv(csv_file_path, include_negative_numbers):
    """This function takes the input CSV file containing the shares and converts it to an array containing
    Python objects with names, prices and profits. The array is the input of the algorithm.
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
                try:
                    price = float(row[1])
                    profit = float(row[2])
                    if include_negative_numbers:
                        if price != 0 and profit != 0:
                            data.append({"name": row[0], "price": abs(price), "profit": abs(price) * abs(profit) / 100})
                    else:
                        if price > 0 and profit > 0:
                            data.append({"name": row[0], "price": price, "profit": price*profit/100})

                except ValueError:
                    pass
    print(f"Données en entrée : {len(data)} actions ont été conservées "
          f"sur les {line_count - 1} présentes dans le fichier")
    return data


def create_csv_from_results(csv_file_path, best_combination, best_profit):
    """This function is called on the results of the algorithm. It creates a CSV file containing the results :
    the shares selected by the algorithm and the total price and profit obtained."""
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        # Creating the csv writer object and writing the header
        writer = csv.writer(csv_file, delimiter=',')
        en_tete = ['name',
                   'price',
                   'profit (%)',
                   'profit (euros)']
        writer.writerow(en_tete)
        for share in best_combination:
            price = share['price']
            profit_flat = share['profit']
            profit_perc = profit_flat*100/price
            row = [share['name'],
                   str(price).replace(".", ","),
                   str(profit_perc)[:5].replace(".", ","),
                   str(profit_flat).replace(".", ",")]
            writer.writerow(row)
        writer.writerow(["Prix total :",
                         str(sum(share['price'] for share in best_combination)).replace(".", ","),
                         "Profit total :",
                         str(best_profit).replace(".", ",")])


def ga_find_best_investments(items, money_cap):
    """ Greedy algorithm to approximate the solution to our investment problem. It sorts the shares based on their
    profit to price ratio and then buy them in that order (the most profitable first) until the money cap is reached.
    This algorithm is not guaranteed to find THE ONE optimal answer, but the margin of error is very small on our data.
    And it solves the problem is a logarithmic time : it runs on O(n log n).
    """
    items = sorted(items, key=lambda x: x['profit'] / x['price'], reverse=True)
    total_profit = 0
    total_price = 0
    taken = []
    for item in items:
        if total_price + item['price'] <= money_cap:
            taken.append(item)
            total_profit += item['profit']
            total_price += item['price']
    return total_profit, taken


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
shares = make_list_from_csv(args.in_file, args.include_neg)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit, max_profit_combination = ga_find_best_investments(shares, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"La meilleure combinaison permet un bénéfice de {max_profit} pour un coût total "
      f"de {sum(share['price'] for share in max_profit_combination)}")

"""Writing the results to a csv file"""
max_profit_combination = sorted(max_profit_combination, key=lambda x: x['name'], reverse=False)
create_csv_from_results(args.out_file, max_profit_combination, max_profit)

