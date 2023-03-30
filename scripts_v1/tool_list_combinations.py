import csv


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


def find_combinations(items, max_weight):
    results = []

    def backtrack(curr_items, curr_weight, start):
        if curr_weight > max_weight:
            return
        results.append(curr_items)
        for i in range(start, len(items)):
            backtrack(curr_items + [items[i]], curr_weight + int(items[i]['price']), i+1)
    backtrack([], 0, 0)
    return results


"""Extracting the data from the CSV file into a Python list."""
file_path = "data/v1/dataset.csv"
shares = make_list_from_csv("data/v1/dataset.csv")
shares = sorted(shares, key=lambda x: x['price'], reverse=True)

possible_combinations = find_combinations(shares, 500)
print(len(possible_combinations))


