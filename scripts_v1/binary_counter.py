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


def find_best_investments(shares, money_cap):
    """This function uses a binary counter to generate each possible combination.
    A one at the index i of the binary means including shares[i].
    A zero at the index i of the binary means not including shares[i]."""
    # Create the variable that will store the final results
    max_profit = 0
    max_profit_combination = []
    # Loop for 2^n where n is the number of shares. 2^n is the number of combinations of n objects.
    for i in range(2 ** len(shares)):
        # Create the binary
        binary = bin(i)[2:].zfill(len(shares))
        # For this given combination, initialize the variables
        combination = []
        total_price = 0
        total_profit = 0
        # Loop through the shares to include it or not in the combination based on the binary value
        for j in range(len(shares)):
            if binary[j] == '1':
                # If the share is to be in the combination, add it to it and calculate its price and profit
                share = shares[j]
                combination.append(share)
                total_price += float(share['price'])
                total_profit += float(share['price'])*float(share['profit'])/100
        # We have now the total price and profit of the combination.
        # If the price exceeds the limit, the combination is not to be considered.
        if total_price > money_cap:
            pass
        else:
            # If the price is within the price cap, we see if this combination is better than the previously best one
            if total_profit > max_profit:
                max_profit = total_profit
                max_profit_combination = combination
    return max_profit, max_profit_combination, i+1


"""Extracting the data from the CSV file into a Python list."""
file_path = "../data/v1/dataset.csv"
shares = make_list_from_csv(file_path)
"""Calling the algorithm on the shares list."""
start_time = time.time()
max_profit, max_profit_combination, it_nb = find_best_investments(shares, 500)
print("Analyse terminée. Temps d'exécution : {:.2f}s".format(time.time() - start_time))
print(f"Nombre de combinaisons testées : {it_nb}")
print(f"La meilleure combinaison permet un bénéfice de {max_profit}")
"""Writing the results to a csv file"""
outfile_path = "../results/v1/binary_counter.csv"
create_csv_from_results(outfile_path, max_profit_combination, max_profit)




