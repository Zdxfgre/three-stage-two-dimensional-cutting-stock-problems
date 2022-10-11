import GeneticAlgorithm2

import csv
import random
import matplotlib

import matplotlib.pyplot as plt


def get_random_color():
    """获取一个随机的颜色"""
    r = lambda: random.uniform(0,1)
    return [r(),r(),r(),1]

def run(input_path,output_path,population_num,iterate_time,pici,pic_save_path):
    now_percent=0.0
    now_s=0.0
    now_block_num=0.0
    init_data=[]
    with open(input_path,'r',encoding='utf-8') as csv.file:
        reader=csv.reader(csv.file)
        for row in reader:
           # print(row)
            row[3]=float(row[3])
            row[4]=float(row[4])
            init_data.append(list(row))
    
    #print((init_data))
    init_data.sort(key=lambda x:x[1],reverse=True)
    
    csv_need=[]
    tmp_csv_list=[]
    last_material=init_data[0][1]
    for i in range(0,len(init_data)):
        material=init_data[i][1]
        print(init_data[i])
        if(i==0):
            tmp_csv_list.append(list(init_data[i]))
        else:
            if(material!=last_material):
                csv_need.append(list(tmp_csv_list))
                tmp_csv_list.clear()
                tmp_csv_list=[]
                tmp_csv_list.append(list(init_data[i]))
            else:
                tmp_csv_list.append(list(init_data[i]))
        last_material=material
    
    #if(len(tmp_csv_list)>0):
    csv_need.append(list(tmp_csv_list))
    
    for i in range(len(csv_need)):
        
        csv_list=list(csv_need[i])
        #print(csv_list)
        w=[]
        l=[]
        id=[]
        run_num=0.0
          #  print("i:",i)
          #  print(init_data[i])
          #  print(do_final)
        l_limit=2440.0
        w_limit=1220.0
        csv_list.sort(key=lambda x:x[3],reverse=True)
        stacks=[]
            #栈中item数量，栈中item的id,栈中material,栈的长度，栈的宽度
         #   print(len(csv_list))
        last_w=csv_list[0][3]
        now_stack=[]#记录当前stack中的item_list
        now_num=1.0#记录当前stack中item数量
        now_w=[]#记录当前stack中的item_w，和now_stack中的id对应
        now_l=[]#记录当前stack中的item_l，和now_stack中的id对应
        now_id=[]#记录当前stack中的item_id
        now_mat=[]#记录当前stack中的材料
        stack_l=0.0#记录当前stack累计的长度
        stack_w=csv_list[0][3]
        stack_id=0
        item_s=0.0
        for j in range(len(csv_list)):
            now_item_w=csv_list[j][3]  
            now_material=csv_list[j][1]
            item_s+=(csv_list[j][3]*csv_list[j][4])
          #  now_s+=(csv_list[j][3]*csv_list[j][4])
            if(last_w==now_item_w):
                now_num+=1
                if(stack_l+csv_list[j][4]<=l_limit):
                        #栈中还能放得下
                    stack_l+=csv_list[j][4]
                    now_stack.append(list(csv_list[j]))
                    now_w.append(csv_list[j][3])
                    now_l.append(csv_list[j][4])
                    now_id.append(csv_list[j][0])
                    now_mat.append(now_material)
                else:
                        #栈已经放不下了，开一个新的栈
                    stacks.append((stack_id,stack_l,stack_w,now_num,list(now_stack),list(now_id),list(now_w),list(now_l),list(now_mat)))
                    stack_l=csv_list[j][4]
                    stack_w=csv_list[j][3]
                    stack_id+=1
                    now_num=1.0
                    now_w.clear()
                    now_l.clear()
                    now_stack.clear()
                    now_id.clear()
                    now_mat.clear()
                    now_stack.append(list(csv_list[j]))
                    now_w.append(csv_list[j][3])
                    now_l.append(csv_list[j][4])
                    now_id.append(csv_list[j][0])  
                    now_mat.append(now_material)   
                
            else:
                stacks.append((stack_id,stack_l,stack_w,now_num,list(now_stack),list(now_id),list(now_w),list(now_l),list(now_mat)))
                stack_l=csv_list[j][4]
                stack_w=csv_list[j][3]
                stack_id+=1
                now_num=1.0
                now_w.clear()
                now_l.clear()
                now_stack.clear()
                now_id.clear()
                now_mat.clear()
                now_stack.append(list(csv_list[j]))
                now_w.append(csv_list[j][3])
                now_l.append(csv_list[j][4])
                now_id.append(csv_list[j][0])     
                now_mat.append(now_material)
            last_w=now_item_w
        stacks.append((stack_id,stack_l,stack_w,now_num,list(now_stack),list(now_id),list(now_w),list(now_l),list(now_mat)))
        strips=[]
            #strip中的id,条带中的stack数量，                     
            #考虑按照栈的长度进行排序
            #从大到小组合为strip
            #strip的最大l
            #strip的w
    
        stacks.sort(key=lambda x:x[1],reverse=True)
        stack_index=[]
        index_to={}
        for j in range(len(stacks)):
            index_to[stacks[j][0]]=j
  
        # for stack in stacks:
        #     print(stack)
        stack_id=[]#记录strip中的stack的id
        strip_w=0.0
        strip_l=0.0
        strip_id=0
        strip_w_list=[]
        strip_l_list=[]
        strip_id_list=[]
        strip_id=0
        for stack in stacks:
            now_id=stack[0]
            now_stack_w=stack[2]
            now_stack_l=stack[1]
            if(strip_w+now_stack_w>w_limit):
                    #超过宽度限制，即表示当前stack无法再加入当前的strip
                strips.append((strip_id,strip_w,strip_l,list(stack_id)))
                stack_id.clear()
                strip_w_list.append(strip_w)
                strip_l_list.append(strip_l)
                strip_id_list.append(strip_id)
                strip_id+=1
                stack_id.append(now_id)
                strip_w=now_stack_w
                strip_l=now_stack_l
            else:
                strip_w+=now_stack_w
                strip_l=max(strip_l,now_stack_l)
                stack_id.append(now_id)
    
        strips.append((strip_id,strip_w,strip_l,list(stack_id)))
        strip_id_list.append(strip_id)
        strip_id+=1
        strip_w_list.append(strip_w)
        strip_l_list.append(strip_l)
            
        strip_1=[]
        strip_2=[]
        strip_3=[]
    
        for j in range(len(strips)):
            num=random.randint(1,3)
            if(num==1):
                strip_1.append(list(strips[j]))
            elif (num==2):
                strip_2.append(list(strips[j]))
            else:
                strip_3.append(list(strips[j]))
        strip_1.sort(key=lambda x:x[2],reverse=True)
        strip_2.sort(key=lambda x:x[1],reverse=True)
        random.shuffle(strip_3)
    
        strips_fin=[]
        for j in range(len(strip_1)):
            strips_fin.append(list(strip_1[j]))
        for j in range(len(strip_2)):
            strips_fin.append(list(strip_2[j]))
        for j in range(len(strip_3)):
            strips_fin.append(list(strip_3[j]))
            

        run_num+=1
         #   print((csv_list_fin))

        s=0.0
        for strip_small in strips_fin:
            print(strip_small)
        print("b")
        ga=GeneticAlgorithm2.GA(len(strips_fin),population_num,list(strips_fin),list(strip_w_list),list(strip_l_list),1220.0,2440.0,s,list(strip_id_list))
        for x in range(iterate_time):
            ga.evolve()
        block_num,result_draw=ga.result(1)
            
        now_block_num+=block_num
            
        print("blocknum:",block_num)
        print("item_s",item_s)
        percent=(item_s/(float(block_num)*2440.0*1220.0))
            #now_percent+=percent
            
            
        print("material and percent:",now_material,percent)
        w.clear()
        l.clear()
        id.clear()
        print(now_block_num)
            #now_percent=now_s/(float(now_block_num)*(2440.0*1220.0))
    
    

        fig=plt.figure(figsize=(80,60),dpi=20)
        plt.plot(1220,2440)
    
        now_w=0.0
        now_l=0.0
        last_block_id=1
        s_accu=0.0
    
        out_file=[]
    
        for j in range(len(result_draw)):
            lis=result_draw[j]
            for k in range(len(lis)):
                strip=strips[lis[k][1]]
          #         print(strip)
                block_id=lis[k][0]
         #;
         # print(block_id)
                if(block_id!=last_block_id):
                    plt.savefig(pic_save_path+str(last_block_id)+'.jpg')
               # print(s_accu/(2440.0*1220.0))
                    s_accu=0.0
                #保存路径
                    plt.clf()
                    plt.plot(1220,2440)
                w_st=lis[k][2]
                l_st=lis[k][3]
                stack_list=strip[3]
          #  print(stack_list)
                for j in range(len(stack_list)):
                    stack_now=stacks[index_to[stack_list[j]]]
                    now_item=stack_now[4]
                    accu_l=l_st
                    item_list=now_item
             #   print(stack_list[j])
             #   print(item_list)
                    for item in item_list:
                        item_w=item[3]
                        item_l=item[4]
                        item_st_w=w_st
                        now_s+=item_w*item_l
                        item_st_l=accu_l
                        accu_l+=item_l
                        material=item[1]
                        color=get_random_color()
                        s_accu+=(float(item_w)*float(item_l))
                        plt.gca().add_patch(plt.Rectangle((item_st_w,item_st_l),item_w,item_l,color=color))
                        out_file.append((item[1],block_id,item[0],item_st_w,item_st_l,item_w,item_l))
            
                    w_st+=stack_now[2]
                last_block_id=block_id
                plt.savefig(pic_save_path+str(block_id)+'.jpg')
        
        print(len(out_file))
        with open(output_path,'a',encoding='utf-8',newline='') as csv.file:
            writer=csv.writer(csv.file)
            for j in range(len(out_file)):
                writer.writerow([pici,out_file[j][0],out_file[j][1],out_file[j][2],out_file[j][3],out_file[j][4],out_file[j][5],out_file[j][6]])
        csv_list.clear()
        w.clear()
        l.clear()


    now_percent=now_s/(now_block_num*(2440.0*1220.0))        
    print("now_percent:",now_percent)
    return now_percent,now_block_num,now_s