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


def find_best_investments(shares, max_price):
    # results = []
    best_combination = []
    best_profit = 0
    count = 0

    def backtrack(curr_shares, curr_price, start):
        nonlocal best_combination
        nonlocal best_profit
        nonlocal count
        count += 1
        if curr_price > max_price:
            return
        # results.append(curr_shares)
        total_profit = sum(int(share['price']) * int(share['profit']) / 100 for share in curr_shares)
        if total_profit > best_profit:
            best_combination = curr_shares
            best_profit = total_profit
        for i in range(start, len(shares)):
            backtrack(curr_shares + [shares[i]], curr_price + int(shares[i]['price']), i+1)
    backtrack([], 0, 0)
    return best_combination, best_profit, count


"""Extracting the data from the CSV file into a Python list."""
file_path = "../data/v1/dataset.csv"
shares = make_list_from_csv(file_path)
shares = sorted(shares, key=lambda x: x['price'], reverse=True)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit_combination, max_profit, iterator = find_best_investments(shares, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"Nombre de combinaisons testées : {iterator}")
print(f"La meilleure combinaison permet un bénéfice de {max_profit}")

"""Writing the results to a csv file"""
max_profit_combination = sorted(max_profit_combination, key=lambda x: x['name'], reverse=False)
outfile_path = "../results/v1/recursive.csv"
create_csv_from_results(outfile_path, max_profit_combination, max_profit)


