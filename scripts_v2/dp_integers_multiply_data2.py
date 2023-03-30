import csv
import time


def make_list_from_csv_multiply(csv_file_path):
    data = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                try:
                    price = float(row[1])
                    profit = float(row[2])
                    if price > 0 and profit > 0:
                        data.append({"name": row[0],
                                     "price": int(price*100),
                                     "profit": int(profit*price)})
                        line_count += 1
                except ValueError:
                    pass
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
            price = share['price']/100
            profit_euros = share['profit']/100
            profit_percent = profit_euros*100/price
            row = [share['name'],
                   str(price).replace(".", ","),
                   str(profit_percent)[:5].replace(".", ","),
                   str(profit_euros).replace(".", ",")]
            writer.writerow(row)
        writer.writerow(["Prix total :",
                         str(sum(share['price']/100 for share in best_combination)).replace(".", ","),
                         "Profit total :",
                         str(best_profit/100).replace(".", ",")])


def knapsack_problem_integers(objects, max_weight):
    n = len(objects)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, max_weight + 1):
            if objects[i - 1]['price'] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - objects[i - 1]['price']] + objects[i - 1]['profit'])

    max_value = dp[n][max_weight]
    selected_objects = []
    j = max_weight
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selected_objects.append(objects[i - 1])
            j -= objects[i - 1]['price']
    selected_objects.reverse()

    return max_value, selected_objects


"""Extracting the data from the CSV file into a Python list."""
file_path = "../data/v2/dataset2.csv"
shares = make_list_from_csv_multiply(file_path)
# shares = sorted(shares, key=lambda x: x['price'], reverse=True)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit, max_profit_combination = knapsack_problem_integers(shares, 50000)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"La meilleure combinaison permet un bénéfice de {max_profit/100}")

"""Writing the results to a csv file"""
max_profit_combination = sorted(max_profit_combination, key=lambda x: x['name'], reverse=False)
outfile_path = "../results/v2/dp_data2.csv"
create_csv_from_results(outfile_path, max_profit_combination, max_profit)

