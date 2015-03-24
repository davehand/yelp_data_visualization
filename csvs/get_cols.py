import csv

with open("originals/yelp_academic_dataset_review.csv", "rb") as source:
    rdr = csv.reader(source)
    with open ("review.csv", "wb") as result:
        wtr = csv.writer( result )
        for r in rdr:
            #wtr.writerow( (r[9], r[16]) ) #categories
            wtr.writerow( (r[1], r[4], r[6], r[2]) ) #reviews
            #wtr.writerow( (r[16], r[22], r[39], r[46], r[61], r[10], r[74]) ) #business
