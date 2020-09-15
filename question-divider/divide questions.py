file = open("hr_wip2019.hr", "r")
outfile1 = open("part1.hr", "w")
outfile2 = open("part2.hr", "w")
outfile3 = open("part3.hr", "w")
totalcount = 0
for line in file:
    line = line.rstrip()
    if line == "creation_date:0;last_used:0;difficulty:0;topics: ;":
        totalcount = totalcount + 1
count = 0
file.close()
file = open("hr_wip.hr", "r")
fisierstring1 = ""
fisierstring2 = ""
fisierstring3 = ""
for line in file:
    line = line.rstrip()
    if line == "creation_date:0;last_used:0;difficulty:0;topics: ;":
        count = count + 1
    if count <= int(totalcount/3):
        fisierstring1 = fisierstring1 + line
        fisierstring1 = fisierstring1 + '\n'
    elif count <= int(2 * totalcount / 3):
        fisierstring2 = fisierstring2 + line
        fisierstring2 = fisierstring2 + '\n'
    else:
        fisierstring3 = fisierstring3 + line
        fisierstring3 = fisierstring3 + '\n'
outfile1.write(fisierstring1)
outfile2.write(fisierstring2)
outfile3.write(fisierstring3)
file.close()
outfile1.close()
outfile2.close()
outfile3.close()