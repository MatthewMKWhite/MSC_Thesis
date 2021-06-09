import csv

with open('Vignettes.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        for i in range(1, 5):
            if int(row["Subject"]) == i and int(row["RoundNum"]) == 1:
                print(row)

