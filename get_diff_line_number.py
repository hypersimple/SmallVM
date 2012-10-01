DataSource = "./diff_5_3.txt"

# all output is for file 1

for line in open(DataSource):
    if (not line.startswith('>')) and (not line.startswith('<')) and (not line.startswith('-')):
        if 'a' in line:
            out = line.split('a')[0].split(',')[0]
            print out
        elif 'd' in line:
            out = int(line.split('d')[0].split(',')[0])-1
            print out
        elif 'c' in line:
            out = int(line.split('c')[0].split(',')[0])-1
            print out
