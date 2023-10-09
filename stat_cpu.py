import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Définir les listes pour stocker les données
timestamps = []
cpu_usage = []

# Ouvrir le fichier CSV et lire les données
with open('csv/cpu_over5.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        timestamp_str, usage_str = row
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        usage = float(usage_str) * 100
        timestamps.append(timestamp)
        cpu_usage.append(usage)

# Agréger les données toutes les 4 heures en prenant la valeur maximale
aggregated_timestamps = []
aggregated_cpu_usage = []
current_timestamp = timestamps[0]
max_usage = 0
for i in range(len(timestamps)):
    if timestamps[i] - current_timestamp >= timedelta(hours=3):
        aggregated_timestamps.append(current_timestamp)
        aggregated_cpu_usage.append(max_usage)
        current_timestamp = timestamps[i]
        max_usage = 0
    if cpu_usage[i] > max_usage:
        max_usage = cpu_usage[i]
aggregated_timestamps.append(current_timestamp)
aggregated_cpu_usage.append(max_usage)

# Tracer le graphique à partir des données agrégées
fig = plt.figure(figsize=(10, 6))
plt.plot(aggregated_timestamps, aggregated_cpu_usage)
plt.xlabel('Heure et jour')
plt.ylabel('Utilisation CPU (%)')
plt.title('Utilisation CPU (Max 3 heures)')
ticklabels = [ts.strftime('%d/%H:%M')  for ts in aggregated_timestamps]
plt.xticks(aggregated_timestamps, ticklabels, rotation=90,fontsize=7)

# Afficher le graphique
plt.grid()
plt.show()
