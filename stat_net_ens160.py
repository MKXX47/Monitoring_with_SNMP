import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Définir les listes pour stocker les données
timestamps = []
net_flow = []

# Ouvrir le fichier CSV et lire les données
with open('csv/ens160.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        timestamp_str, flow_str = row
        timestamp = datetime.strptime(timestamp_str, '%d-%m-%y %H:%M')
        flow = float(flow_str) / 1024
        timestamps.append(timestamp)
        net_flow.append(flow)

# Agréger les données toutes les 4 heures en prenant la valeur maximale
aggregated_timestamps = []
aggregated_net_flow = []
current_timestamp = timestamps[0]
max_flow = 0
for i in range(len(timestamps)):
    if timestamps[i] - current_timestamp >= timedelta(hours=3):
        aggregated_timestamps.append(current_timestamp)
        aggregated_net_flow.append(max_flow)
        current_timestamp = timestamps[i]
        max_flow = 0
    if net_flow[i] > max_flow:
        max_flow = net_flow[i]
aggregated_timestamps.append(current_timestamp)
aggregated_net_flow.append(max_flow)

# Tracer le graphique à partir des données agrégées
fig = plt.figure(figsize=(10, 6))
plt.plot(aggregated_timestamps, aggregated_net_flow)
#plt.xlabel('Heure et jour')
plt.xlabel('Heure et jour')
plt.ylabel('Flux sur ens160 (KB)')
plt.title('Flux sur ens160 (MAX 3 heures)')
ticklabels = [ts.strftime('%d/%H:%M')  for ts in aggregated_timestamps]
plt.xticks(aggregated_timestamps, ticklabels, rotation=90,fontsize=7)


# Afficher le graphique
plt.grid()
plt.show()
