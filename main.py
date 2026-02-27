data_list = []
with open('2702_data_log.txt', 'r') as file:
    for line in file:
        data_list.append(line.strip())

o1 = {}
o2 = {}
o3 = {}
o4 = {}

for line in data_list:
    time_line = line.split("ACTIVE")[0]
    time_line = time_line.split()[-1][0:-1]
    if "Output 1" in line:
        if "HIGHACTIVE" in line:
            o1[time_line] = "HIGHACTIVE"
        elif "LOWACTIVE" in line:
            o1[time_line] = "LOWACTIVE"
    if "Output 2" in line:
        if "HIGHACTIVE" in line:
            o2[time_line] = "HIGHACTIVE"
        elif "LOWACTIVE" in line:
            o2[time_line] = "LOWACTIVE"
    if "Output 3" in line:
        if "HIGHACTIVE" in line:
            o3[time_line] = "HIGHACTIVE"
        elif "LOWACTIVE" in line:
            o3[time_line] = "LOWACTIVE"
    if "Output 4" in line:
        if "HIGHACTIVE" in line:
            o4[time_line] = "HIGHACTIVE"
        elif "LOWACTIVE" in line:
            o4[time_line] = "LOWACTIVE"

#Make csv file from 4 dictionaries
import csv
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['Time', 'Output 1', 'Output 2', 'Output 3', 'Output 4']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for time in sorted(set(list(o1.keys()) + list(o2.keys()) + list(o3.keys()) + list(o4.keys()))):
        writer.writerow({'Time': time, 'Output 1': o1.get(time, ''), 'Output 2': o2.get(time, ''), 'Output 3': o3.get(time, ''), 'Output 4': o4.get(time, '')})
    
    