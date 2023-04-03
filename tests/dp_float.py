import csv
import time


def make_list_from_csv(csv_file_path):
    data = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                data.append({"name": row[0], "price": float(row[1].replace(",", ".")), "profit": float(row[2].replace(",", "."))})
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


def knapsack_dp(items, capacity):
    # Initialize dictionary
    max_value = {(i, j): 0 for i in range(len(items)+1) for j in range(capacity+1)}

    # Iterate over items and weights
    for i in range(1, len(items)+1):
        for j in range(1, capacity+1):
            # Compute maximum value
            if items[i-1]['price'] <= j:
                max_value[(i, j)] = max(max_value[(i-1, j)], max_value[(i-1, round(j-items[i-1]['price'], 2))] + items[i-1]['profit'])
            else:
                max_value[(i, j)] = max_value[(i-1, j)]

    # Compute optimal value
    optimal_value = max_value[(len(items), capacity)]

    return optimal_value

"""Extracting the data from the CSV file into a Python list."""
file_path = "./dataset_float.csv"
shares = make_list_from_csv(file_path)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit, max_profit_combination = knapsack_dp(shares, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"La meilleure combinaison permet un bénéfice de {max_profit}")

"""Writing the results to a csv file"""
max_profit_combination = sorted(max_profit_combination, key=lambda x: x['name'], reverse=False)
outfile_path = "./dp.csv"
create_csv_from_results(outfile_path, max_profit_combination, max_profit)

