#10 hotels with cheapest price per night
from operator import itemgetter
import pandas as pd
input_file=open("tripadvisor_data.csv")
output_file=open("tripadvisor_data_sorted.csv","w")

table=[]
header=input_file.readline()
for line in input_file:
    col=line.split(",")
    col[7]=float(col[7][1:])
    table.append(col)
table_sorted=sorted(table,key=itemgetter(7),reverse=False)
output_file.write(header)
input_file.close()
output_file.close()
for row in table_sorted:
    row=[str(x) for x in row]
    row=[','.join(row)]
f2=pd.DataFrame(table_sorted,columns=header.split(","))
# print(f2.iloc[:,[0,3,4,7]])
print('\033[1;31m Ten Cheapest Hotels\033[0m')
from prettytable import PrettyTable
x = PrettyTable()
x.field_names = ["hotel_name", "reviews", "tripadvisor_rating", "price_per_night"]
for i in range(10):
    list=[]
    list.append(table_sorted[i][0])
    list.append(table_sorted[i][3])
    list.append(table_sorted[i][4])
    list.append(table_sorted[i][7])
    x.add_row(list)

print(x)

#Ten Most Popular Hotels (most people reviewed)
from operator import itemgetter
import pandas as pd
input_file=open("tripadvisor_data.csv")
output_file=open("tripadvisor_data_sorted.csv","w")

table=[]
header=input_file.readline()
for line in input_file:
    col=line.split(",")
    col[3]=float(col[3])
    table.append(col)
table_sorted=sorted(table,key=itemgetter(3),reverse=True)
output_file.write(header)
input_file.close()
output_file.close()
for row in table_sorted:
    row=[str(x) for x in row]
    row=[','.join(row)]
f2=pd.DataFrame(table_sorted,columns=header.split(","))
# print(f2.iloc[:,[0,3,4,7]])
print('\033[1;31m Ten Most Popular Hotels (most people reviewed)\033[0m')
from prettytable import PrettyTable
x = PrettyTable()
x.field_names = ["hotel_name", "reviews", "tripadvisor_rating", "price_per_night"]
for i in range(10):
    list=[]
    list.append(table_sorted[i][0])
    list.append(table_sorted[i][3])
    list.append(table_sorted[i][4])
    list.append(table_sorted[i][7])
    x.add_row(list)

print(x)

#Ten Hotels with Most highest Rating
from operator import itemgetter
import pandas as pd
input_file=open("tripadvisor_data.csv")
output_file=open("tripadvisor_data_sorted.csv","w")

table=[]
header=input_file.readline()
for line in input_file:
    col=line.split(",")
    col[4]=float(col[4])
    table.append(col)
table_sorted=sorted(table,key=itemgetter(4),reverse=True)
output_file.write(header)
input_file.close()
output_file.close()
for row in table_sorted:
    row=[str(x) for x in row]
    row=[','.join(row)]
f2=pd.DataFrame(table_sorted,columns=header.split(","))
# print(f2.iloc[:,[0,3,4,7]])
print('\033[1;31m Ten Hotels with Most highest Rating\033[0m')
from prettytable import PrettyTable
x = PrettyTable()
x.field_names = ["hotel_name", "reviews", "tripadvisor_rating", "price_per_night"]
for i in range(10):
    list=[]
    list.append(table_sorted[i][0])
    list.append(table_sorted[i][3])
    list.append(table_sorted[i][4])
    list.append(table_sorted[i][7])
    x.add_row(list)

print(x)

#plot gragh to show price changes through time
import csv
from datetime import datetime
from matplotlib import pyplot as plt
filename = 'tripadvisor_data.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    dates, prices = [], []
    for row in reader:
        try:
            current_date =datetime.strptime(row[5], '%m/%d/%Y')  
            price = float(row[7][1:-1]) 
        except ValueError:
            try:
                current_date =datetime.strptime(row[5], '%Y/%m/%d').strftime('%m/%d/%Y')  
                price = float(row[7][1:]) 
            except ValueError:
                print( 'fail to read data')  
            else:     #store data
                dates.append(current_date)
                prices.append(price)
fig = plt.figure(dpi=128,figsize=(10,6))
plt.plot(dates,prices,c='red',alpha=0.5)
title = "Price Changes Through Time"
plt.title(title, fontsize=20)
plt.xlabel('', fontsize=15)
fig.autofmt_xdate()
plt.ylabel("Price_per_night ($)", fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=10)
 
plt.show()