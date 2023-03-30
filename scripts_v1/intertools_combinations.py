import csv
import time
import itertools


def make_list_from_csv(csv_file_path):
    data = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                data.append({"name": row[0], "price": row[1], "profit": row[2]})
                line_count += 1

    return data


def create_csv_from_results(csv_file_path, best_combination, best_profit):
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        # Creating the csv writer object and writing the header
        writer = csv.writer(csv_file, delimiter=',')
        en_tete = ['name',
                   'price',
                   'profit (%)',
                   'profit (euros)']
        writer.writerow(en_tete)
        for share in best_combination:
            row = [share['name'], share['price'], share['profit'], str(int(share['profit'])*int(share['price'])/100).replace(".", ",")]
            writer.writerow(row)
        writer.writerow(["Prix total :", sum(int(share['price']) for share in best_combination), "Profit total :", str(best_profit).replace(".", ",")])


def find_best_investments(shares, money_cap):
    best_combination = []
    best_profit = 0
    it = 1
    # Iterate through all possible combinations of shares
    for i in range(1, len(shares) + 1):
        for combination in itertools.combinations(shares, i):
            it += 1
            total_price = sum(int(share['price']) for share in combination)

            # Only consider combinations that do not exceed the money cap
            if total_price <= money_cap:
                total_profit = sum(int(share['price'])*int(share['profit'])/100 for share in combination)

                # Update the best combination if this one is better
                if total_profit > best_profit:
                    best_combination = combination
                    best_profit = total_profit

    return best_combination, best_profit, it


"""Extracting the data from the CSV file into a Python list."""
file_path = "../data/v1/dataset.csv"
shares = make_list_from_csv(file_path)
"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit_combination, max_profit, nb_it = find_best_investments(shares, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"Nombre de combinaisons testées : {nb_it}")
print(f"La meilleure combinaison permet un bénéfice de {max_profit}")

"""Writing the results to a csv file"""
outfile_path = "../results/v1/intertools.csv"
create_csv_from_results(outfile_path, max_profit_combination, max_profit)

