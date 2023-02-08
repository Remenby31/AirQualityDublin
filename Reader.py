import csv
import matplotlib.pyplot as plt

file_path = "DCU/DCU_mobiles_01-04-2022_31-07-2022.csv"
data = []

with open(file_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        data.append(row[0].split(';'))
    labels = data.pop(0)

# timestamp;sensor ID;pm2.5(ug/m3);pm10(ug/m3);latitude;longitude

# plot pm2.5 value on a map using latitude and longitude
# pm2.5 is the 3rd column in the data
# latitude is the 5th column in the data
# longitude is the 6th column in the data

# convert pm2.5 to float
for row in data:
    row[2] = float(row[2])
    row[5] = float(row[5])
    row[4] = float(row[4])


# plot pm2.5 value scatter plot
plt.scatter([row[5] for row in data], [row[4] for row in data], c=[row[2] for row in data], cmap='jet')
plt.colorbar()
plt.show()


