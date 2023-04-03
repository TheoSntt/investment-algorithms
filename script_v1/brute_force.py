"""This scripts finds the correct solution to the best investment using brute force.
It needs 2 arguments to be run :
- in_file : The input file containing the shares to evaluate. If you downloaded the whole repository on GitHub,
A correct value could be --in_file="../data/demo_dataset.csv"
- out_file : The output file in which the selected shares will be written.
An example value could be --out_file="../results/brute_force_result.csv"
"""

import csv
import time
import itertools
import argparse


def make_list_from_csv(csv_file_path):
    """This function takes the input CSV file containing the shares and converts it to an array containing
    Python objects with names, prices and profits. The array is the input of the algorithm."""
    data = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                data.append({"name": row[0], "price": float(row[1]), "profit": float(row[2])})
                line_count += 1

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
            row = [share['name'],
                   share['price'],
                   share['profit'],
                   str(share['profit']*share['price']/100).replace(".", ",")]
            writer.writerow(row)
        writer.writerow(["Prix total :",
                         sum(share['price'] for share in best_combination),
                         "Profit total :",
                         str(best_profit).replace(".", ",")])


def brute_force_find_best_investments(shares, money_cap):
    """ Brute force algorithm to solve our investment problem : it iterates through all the possible combination of n
    shares (2^n combinations) using intertools.combinations. It then tests whether it fits the money_cap, and
    if it does, it calculates the total profit and store it if it is better than the previous best profit stored"""
    best_combination = []
    best_profit = 0
    it = 1
    # Iterate through all possible combinations of shares
    for i in range(1, len(shares) + 1):
        for combination in itertools.combinations(shares, i):
            it += 1
            total_price = sum(int(share['price']) for share in combination)

            # Test whether the combination exceeds the money cap
            if total_price <= money_cap:
                total_profit = sum(share['price']*share['profit']/100 for share in combination)

                # Update the best combination if this one is better
                if total_profit > best_profit:
                    best_combination = combination
                    best_profit = total_profit

    return best_combination, best_profit, it


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
# Parse the arguments
args = parser.parse_args()

"""Extracting the data from the CSV file into a Python list."""
share_list = make_list_from_csv(args.in_file)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit_combination, max_profit, nb_it = brute_force_find_best_investments(share_list, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"Nombre de combinaisons testées : {nb_it}")
print(f"La meilleure combinaison permet un bénéfice de {max_profit} pour un coût total "
      f"de {sum(share['price'] for share in max_profit_combination)} euros")

"""Writing the results to a csv file"""
create_csv_from_results(args.out_file, max_profit_combination, max_profit)

