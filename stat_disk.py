import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Définir les listes pour stocker les données
timestamps = []
disk_usage = []

# Ouvrir le fichier CSV et lire les données
with open('csv/disk_root.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        timestamp_str, usage_str = row
        timestamp = datetime.strptime(timestamp_str, '%d-%m-%y %H:%M')
        usage = float(usage_str)/(1024 * 1024) # convertir en GB
        timestamps.append(timestamp)
        disk_usage.append(usage)
# Agréger les données toutes les 4 heures en prenant la valeur maximale et minimale
aggregated_timestamps = []
aggregated_disk_usage_max = []
aggregated_disk_usage_min = []
current_timestamp = timestamps[0]
max_usage = 0
min_usage = 1000000 # valeur initiale élevée pour trouver le minimum
for i in range(len(timestamps)):
    if timestamps[i] - current_timestamp >= timedelta(hours=3):
        aggregated_timestamps.append(current_timestamp)
        aggregated_disk_usage_max.append(max_usage)
        aggregated_disk_usage_min.append(min_usage)
        current_timestamp = timestamps[i]
        max_usage = 0
        min_usage = 1000000 # valeur initiale élevée pour trouver le minimum
    if disk_usage[i] > max_usage:
        max_usage = disk_usage[i]
    if disk_usage[i] < min_usage:
        min_usage = disk_usage[i]
aggregated_timestamps.append(current_timestamp)
aggregated_disk_usage_max.append(max_usage)
aggregated_disk_usage_min.append(min_usage)
 # Tracer le graphique à partir des données agrégées
fig = plt.figure(figsize=(10, 6))
plt.plot(aggregated_timestamps, aggregated_disk_usage_max, label='Max')
plt.plot(aggregated_timestamps, aggregated_disk_usage_min, label='Min')
plt.xlabel('Heure et jour')
plt.ylabel('Stockage disque racine (GB)')
plt.title('Stockage du disque racine (MAX et MIN 3 heures)')
ticklabels = [ts.strftime('%d/%H:%M')  for ts in aggregated_timestamps]
plt.xticks(aggregated_timestamps, ticklabels, rotation=90,fontsize=7)

# Afficher le graphique
plt.grid()
plt.legend()
plt.show()
