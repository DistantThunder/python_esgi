from sys import argv

while len(argv) != 3:
    if len(argv) < 3:
        print("Not enough arguments.")
        exit()
    elif len(argv) > 3:
        print("Too many arguments.")
        exit()

script, arg1, arg2 = argv

def filter(file1,file2):
    src_file = open(file1,'r')
    filtered_file = open(file2,'w')
    for line in src_file.readlines():
        if line[0] == '#':
            continue
        else:
            filtered_file.write(line)
    
    src_file.close()
    filtered_file.close()

filter(arg1,arg2)
