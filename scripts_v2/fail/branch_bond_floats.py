import csv
import time
import heapq


def make_list_from_csv(csv_file_path):
    data = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                try:
                    profit = float(row[1])
                    profit = float(row[2])
                    if profit > 0 and profit > 0:
                        if line_count <= 350:
                            data.append({"name": row[0], "price": profit, "profit": profit * profit / 100})
                            line_count += 1
                except ValueError:
                    pass
    return data


def create_csv_from_results(csv_file_path, best_combination, best_profit):
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        # Creating the csv writer object and writing the header
        writer = csv.writer(csv_file, delimiter=',')
        en_tete = ['name',
                   'profit',
                   'profit (euros)']
        writer.writerow(en_tete)
        for share in best_combination:
            row = [share['name'], share['profit'], share['profit']]
            writer.writerow(row)
        writer.writerow(["Prix total :",
                         str(sum(int(share['profit']) for share in best_combination)).replace(".", ","),
                         "Profit total :",
                         str(best_profit).replace(".", ",")])


class Node:
    def __init__(self, level, profit, price, taken):
        self.level = level
        self.profit = profit
        self.price = price
        self.taken = taken

    def __lt__(self, other):
        return self.profit > other.profit

def bound(node, items, capacity):
    if node.price >= capacity:
        return 0
    else:
        profit_bound = node.profit
        price = node.price
        for i in range(node.level, len(items)):
            if price + items[i]['price'] <= capacity:
                profit_bound += items[i]['profit']
                price += items[i]['price']
            else:
                profit_bound += (capacity - price) * items[i]['profit'] / items[i]['price']
                break
        return profit_bound

def knapsack(items, capacity):
    items = sorted(items, key=lambda x: x['profit'] / x['price'], reverse=True)
    best_profit = 0
    best_taken = []
    pq = []
    root = Node(0, 0, 0, [])
    heapq.heappush(pq, root)
    while pq:
        node = heapq.heappop(pq)
        if node.profit > best_profit:
            best_profit = node.profit
            best_taken = node.taken
        if node.level < len(items):
            left = Node(node.level + 1, node.profit + items[node.level]['profit'], node.price + items[node.level]['price'], node.taken + [items[node.level]])
            if left.price <= capacity and left.profit > best_profit:
                best_profit = left.profit
                best_taken = left.taken
            if bound(left, items, capacity) > best_profit:
                heapq.heappush(pq, left)
            right = Node(node.level + 1, node.profit, node.price, node.taken)
            if bound(right, items, capacity) > best_profit:
                heapq.heappush(pq, right)
    return best_profit, best_taken


"""Extracting the data from the CSV file into a Python list."""
file_path = "../data/v2/dataset1.csv"
shares = make_list_from_csv(file_path)
# shares = sorted(shares, key=lambda x: x['profit'], reverse=True)

"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit, max_profit_combination = knapsack(shares, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"La meilleure combinaison permet un bénéfice de {max_profit}")


"""Writing the results to a csv file"""
max_profit_combination = sorted(max_profit_combination, key=lambda x: x['name'], reverse=False)
outfile_path = "../results/v2/branch_bond.csv"
create_csv_from_results(outfile_path, max_profit_combination, max_profit)

