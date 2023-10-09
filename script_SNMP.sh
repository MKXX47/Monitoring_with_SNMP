#!/bin/bash
host='IP_Adress'
community='community'

ram_oid='.1.3.6.1.4.1.2021.4.6.0'
cpu_oid='.1.3.6.1.4.1.2021.11.9.0'
cpu_oid2='.1.3.6.1.4.1.2021.11.11.0'
cpu_oid5='1.3.6.1.4.1.2021.10.1.3.2'

while true; do
         ram_data=$(snmpget -v 2c -c "$community" "$host" "$ram_oid" | awk '{print $4}')
         cpu_now=$(snmpget -v 2c -c "$community" "$host" "$cpu_oid" | awk '{print $4}')
         cpu_idle=$(snmpget -v 2c -c "$community" "$host" "$cpu_oid2" | awk '{print $4}')
         cpu_over5=$(snmpget -v 2c -c "$community" "$host" "$cpu_oid5" | awk '{print $4}')

         #Ens160
         in_ens=$(snmpget -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.31.1.1.1.2.2 )
         out_ens=$(snmpget -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.31.1.1.1.4.2)
         echo "$(date +"%Y-%m-%d %H:%M:%S");ens160;${in_ens};${out_ens}" >> "ens160.csv"

         #Disk Root
         stockage_r=$(snmpwalk -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.25.2.3.1.6.31)
         echo "Disk Usage : $(date +"%Y-%m-%d %H:%M:%S");Disk Racine;${stockage_r}"
         echo "$(date +"%Y-%m-%d %H:%M:%S");Disk Racine;${stockage_r}" >> "disk_root.csv"

         timestamp=$(date +"%Y-%m-%d %H:%M:%S")

         echo "$timestamp;$cpu_now;$cpu_idle" >> "cpu_usage.csv"
         echo "$timestamp;$ram_data" >> "ram_usage.csv"
         echo "$timestamp;$cpu_over5" >> "cpu_over5.csv"
         #Disk All
         for i in $(snmpwalk -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.25.2.3.1.1)
                do
                        nom=$(snmpwalk -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.25.2.3.1.3.$i)
                        stockage=$(snmpwalk -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.25.2.3.1.6.$i)
                        echo "Disk Usage : $(date +"%Y-%m-%d %H:%M:%S");${nom};${stockage}"
                        echo "$(date +"%Y-%m-%d %H:%M:%S");${nom};${stockage}" >> "disk.csv"
                done
         #Net interface All
         for i in $(snmpwalk -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.2.2.1.1)
                do
                        name=$(snmpget -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.31.1.1.1.1.$i)

                        in=$(snmpget -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.31.1.1.1.2.$i )
                        out=$(snmpget -Oqv -v2c -c community IP_Adress 1.3.6.1.2.1.31.1.1.1.4.$i)

                        echo "$(date +"%Y-%m-%d %H:%M:%S");${name};${in};${out}" >> "net.csv"
                        echo "Net Interface :$(date +"%Y-%m-%d %H:%M:%S");${name};${in};${out}"
                done
         sleep 300

done
