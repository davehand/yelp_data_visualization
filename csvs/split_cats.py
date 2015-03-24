#!/usr/bin/env python
import csv
import ast

count=0
with open("categories.csv", "rb") as source:
    rdr = csv.reader(source)
    with open ("real_categories.csv", "wb") as result:
        wtr = csv.writer( result )
        for r in rdr:
            business = r[1].strip()
            cats = r[0]
            categories = []
            if count > 0:
                categories = ast.literal_eval(cats)
            else:
                categories.append(cats)
                count += 1

            for cat in categories:
                cat = cat.strip()
                cat = cat.replace('"', "")
                cat = cat.replace('\"', "")
                cat = cat.replace("'", "")
                cat = cat.replace("\'", "")
                if cat:
                    wtr.writerow( (business, cat) )
