import csv
import time
import heapq


def make_list_from_csv(csv_file_path, include_neg=False):
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
                    if include_neg:
                        if price != 0 and profit != 0:
                            data.append({"name": row[0], "price": abs(price), "profit": abs(price) * abs(profit) / 100})
                    else:
                        if price > 0 and profit > 0:
                            data.append({"name": row[0], "price": price, "profit": price*profit/100})

                except ValueError:
                    pass
    print(line_count-1)
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


def greedy_knapsack_heapq(items, money_cap):
    heap = [(-item['profit']/item['price'], item) for item in items]
    heapq.heapify(heap)
    total_profit = 0
    total_price = 0
    taken = []
    while heap and total_price < money_cap:
        ratio, item = heapq.heappop(heap)
        if total_price + item['price'] <= money_cap:
            taken.append(item)
            total_profit += item['profit']
            total_price += item['price']
        else:
            # Add a fraction of the item to the knapsack
            fraction = (money_cap - total_price) / item['price']
            taken.append({
                'name': item['name'],
                'price': fraction * item['price'],
                'profit': fraction * item['profit']
            })
            total_profit += fraction * item['profit']
            total_price += fraction * item['price']
    return total_profit, taken


def greedy_knapsack(items, money_cap):
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


"""Extracting the data from the CSV file into a Python list."""
file_path = "../../data/v2/dataset2.csv"
shares = make_list_from_csv(file_path, include_neg=True)
print(len(shares))
# shares = sorted(shares, key=lambda x: x['profit'], reverse=True)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit, max_profit_combination = greedy_knapsack(shares, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"La meilleure combinaison permet un bénéfice de {max_profit} pour un coût total de {sum(share['price'] for share in max_profit_combination)}")



"""Writing the results to a csv file"""
max_profit_combination = sorted(max_profit_combination, key=lambda x: x['name'], reverse=False)
outfile_path = "../../results/v2/greedy_data2.csv"
create_csv_from_results(outfile_path, max_profit_combination, max_profit)

