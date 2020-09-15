file_name = input("Insert file name: ")
file = open(file_name, 'r')
count = 0
for line in file:
    line = line.rstrip()
    if line == "creation_date:0;last_used:0;difficulty:0;topics: ;":
        count = count + 1
print(count)
file.close()