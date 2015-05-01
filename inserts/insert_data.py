import os
import csv
import sys

#initialize variables for loop
first_line=True
header_string = ""
f = open('test.txt','w')

#for each line of the file, begin creating the insert sql statement
#write each insert statement to file specified on command line
with open("review.csv", "rb") as source:
    rdr = csv.reader(source)
    for r in rdr:
        if first_line:
            first_line = False
            row_one = []
            for c in r:
                row_one.append(c)
            header_string += row_one[0].rstrip()
            #for x in range(1,len(row_one)):
            for x in range(1,5):
                header_string += ", " + row_one[x].rstrip()
        else:
            cols = []
            for c in r:
                cols.append(c)
            if (cols[0].rstrip() == ''):
                values_string = "null"
            else:
                values_string = "'" +  cols[0].rstrip() + "'"
            i = 0
            #for x in range(1,len(cols)):
            for x in range(1,5):
                if (cols[x].rstrip() == ''):
                    values_string += ", null"
                else:
                    val = cols[x].rstrip()
                    if "'" in val:
                        val = val.replace("'", "''")
                    #values_string += ", '" + val + "'"
                    #review only
                    if i == 1 or  i == 2:
                        values_string += ", " + val
                    else:
                        values_string += ", '" + val + "'"
                i += 1
            f.write("insert into " + "review" + "(" + header_string + ") values(" + values_string + ");")
            f.write("\n")



f.close()

print header_string
