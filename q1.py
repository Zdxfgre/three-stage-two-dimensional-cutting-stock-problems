import math
from mimetypes import init
import random
import operator
from turtle import color, width
from unittest import result
import matplotlib

import matplotlib.pyplot as plt
import csv
import get_data_2

input_path='...'
output_path='...'

tmp_path='...'

init_data=[]
with open(input_path,'r',encoding='utf-8') as csv.file:
    reader=csv.reader(csv.file)
    init_data=[]
    for row in reader:
        row[3]=float(row[3])
        row[4]=float(row[4])
        row[6]=int(row[6])
        init_data.append(row)


init_data.sort(key=lambda x:x[6])
tmp_=[]
fin=[]
for i in range(len(init_data)):
    if(i==0):
        tmp_.append(list(init_data[i]))
    else:
        if(init_data[i][6]==init_data[i-1][6]):
            tmp_.append(list(init_data[i]))
        else:
            fin.append(list(tmp_))
            tmp_.clear()
            tmp_.append(list(init_data[i]))

fin.append(tmp_)
# for i in range(len(fin)):
#     print(i)
#     print(fin[i])        
    
accu_s=0.0
accu_num=0.0
for i in range(len(fin)):
    pici=fin[i]
    print(pici)
    with open(tmp_path,'w',encoding='utf-8',newline='') as csv.file:
        writer=csv.writer(csv.file)
        for j in range(len(pici)):
            writer.writerow(pici[j])
    result,num,s=get_data_2.run(tmp_path,output_path,80,200,pici[j][6])
    accu_num+=num
    accu_s+=s
final_percent=accu_s/(accu_num*2440.0*1220.0)
print(accu_num)
print("final percent:",final_percent)
        
#

#print(reader)

#result=get_data_1.run(input_path,output_path,80,90)

#print(result)



