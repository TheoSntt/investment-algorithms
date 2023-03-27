import csv


def make_dict_form_csv(csv_file_path):
    data = {}
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                data[row[0]] = {
                    "price": row[1],
                    "profit": row[2]
                }
                line_count += 1

    return data


file_path = "data/v1/dataset.csv"
data = make_dict_form_csv("data/v1/dataset.csv")
print(data)
