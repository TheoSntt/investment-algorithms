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


def knapsack_problem(objects, max_weight):
    n = len(objects)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, max_weight + 1):
            if int(objects[i - 1]['price']) > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - int(objects[i - 1]['price'])] + int(objects[i - 1]['profit'])*int(objects[i - 1]['price'])/100)

    max_value = dp[n][max_weight]
    selected_objects = []
    j = max_weight
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selected_objects.append(objects[i - 1])
            j -= int(objects[i - 1]['price'])
    selected_objects.reverse()

    return max_value, selected_objects


"""Extracting the data from the CSV file into a Python list."""
file_path = "../data/v1/dataset.csv"
shares = make_list_from_csv(file_path)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit, max_profit_combination = knapsack_problem(shares, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"La meilleure combinaison permet un bénéfice de {max_profit}")

"""Writing the results to a csv file"""
max_profit_combination = sorted(max_profit_combination, key=lambda x: x['name'], reverse=False)
outfile_path = "../results/v1/dp.csv"
create_csv_from_results(outfile_path, max_profit_combination, max_profit)

