import csv

file_path = "DCU/test.csv"
data = []

with open(file_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        data.append(row[0].split(';'))
    labels = data.pop(0)

print(labels)