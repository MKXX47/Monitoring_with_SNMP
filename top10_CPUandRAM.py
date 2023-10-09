def top_process(filename):
    service_dict = dict()
    top_10 = []
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            line_elements = line.split()
            elements_split = line_elements[0].split(';')
            if len(elements_split) == 2:
                service = elements_split[0]
                consumption = int(elements_split[1])
                if service not in service_dict:
                    service_dict[service] = consumption
                else:
                    service_dict[service] += consumption
            else:
                continue
        sorted_dict = sorted(service_dict.items(), key=lambda x: x[1], reverse=True)
        for key, value in sorted_dict:
            if i < 10:
                top_10.append(key)
                i += 1
            else:
                break

    return top_10


cpu_top_10 = top_process("top10_cpu.csv")
ram_top_10 = top_process("top10_ram.csv")

print("le Top 10 des applications qui consomment le plus de temps cumulé CPU:")
for app in cpu_top_10:
    print(app)

print("\nle Top 10 des applications qui consomment le plus de mémoire vive (RAM):")
for app in ram_top_10:
    print(app)
