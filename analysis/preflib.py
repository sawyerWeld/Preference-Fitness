# Reading in data from the preflib format
with open('EDIreland.soi', 'r') as file:
    data = file.readlines()
    for line in data:
        print(line)
            
print('Finished writing to file')