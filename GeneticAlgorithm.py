import math
import random
import operator
from turtle import color, width
from unittest import result
import matplotlib

import matplotlib.pyplot as plt
import csv
from d2l import torch as d2l

#适应函数：利用率最高
#

class GA():
    def __init__(self, length, count, csv,w,l,bigw,bigl,s,id):
        self.length = length #染色体长度
        self.count = count #种群中染色体数量
        self.csv=csv#数据
        self.w=w#宽
        self.l=l#长
        self.bigw=bigw
        self.bigl=bigl
        self.alls=0.0#使用板材面积
        self.id=id
        self.s=s
        self.block_s=bigw*bigl
        self.population = self.gen_population(length, count, csv) #目前排序生成

    def evolve(self,retain_rate = 0.2, random_select_rate = 0.5, mutation_rate = 0.01):
        """
        进化，对当前一代种群一次进行选择，交叉并产生新一代种群，然后对新一代种群进行变异
        """
        parents = self.selection(retain_rate, random_select_rate)
       # print("numpar:%d"%len(parents))
        self.crossover(parents)
        self.mutation(mutation_rate)

    def gen_chromosome(self, length, csv):
        """
        用一个实数表示一个基因
        """
        random.shuffle(csv)
        
        chromosome = []
        ch_w = []
        ch_l = []
        ch_id = []
        now_num=1
        stacks=[]
        
        for i in range(length):
            ch_w.append(csv[i][3])
            ch_l.append(csv[i][4])
            ch_id.append(csv[i][0])
            now_num=random.randint(0,length)
            if i==0:
                chromosome.append(now_num)
            else:
                if csv[i][3]==csv[i-1][3]:
                    chromosome.append(now_num)
                else:
                    if csv[i][4]==csv[i-1][4]:
                        chromosome.append(now_num)
                    else:
                        now_num+=1
                        chromosome.append(now_num)
        """
        for i in range(length):
            chromosome |= (1 << i) * random.randint(0,1)
        """
        #整数编码
        return (chromosome,ch_w,ch_l,ch_id,stacks)

    def gen_population(self,length,count,csv):
        """
        获取初始种群（一个含有count个长度为length的染色体列表）
        """
        return [self.gen_chromosome(length,csv) for i in range(count)]

    def fitness(self, chromosome, w, l,id, control,stacks):
        """
        染色体解码为布局方案
        并得到对应利用率
        
        """
        
        x,tmp,stacks = self.decode(chromosome,w,l,id,control)
        return x,stacks

    def selection(self, retain_rate, random_select_rate):
        """
        选择
        先对适应度从大到小排序，选出存活的染色体
        在进行随机选择，选出适应度虽然小，但是幸存下来的个体
        """
        #对适应度从大到小排序
        graded=[]
      #  print(len(self.population[0]))
        for chromosome,w,l,id, stak in self.population:
          #  print("che%d"%len(chromosome))
            fit,sta=self.fitness(chromosome,w,l,id,0,stak)
            graded.append((fit,(chromosome,w,l,id,sta)))
        
        #graded = [(self.fitness(chromosome,w,l,id,0,stacks), (chromosome,w,l,id,stacks)) for chromosome,w,l,id,stacks in self.population]
       # print(graded)
        graded = [x[1] for x in sorted(graded, reverse = True)]
        #print(graded[0])
        #选出适应性强的染色体
        retain_length = int(len(graded) * retain_rate)
        parents = graded[:retain_length]
        #选出是是影响不强，但是幸存的染色体
        for chromosome,w,l,id,stacks in graded[retain_length:]:
            if random.random() < random_select_rate:
                parents.append((chromosome,w,l,id,stacks))
        #print('a')
        #print(parents[0][4])
        return  parents

    def crossover(self,parents):
        """
        染色体的交叉，反之，生成新一代的种群
        """
        #新出生的孩子，最终会被加入存活下来的父母之中，形成新一代的种群
        children = []
        #需要繁殖的孩子的量
        target_count = len(self.population) - len(parents)
        #开始根据需要的量进行繁殖
        flag={}
        while len(children) < target_count:
            male = random.randint(0, len(parents)-1)
            female = random.randint(0, len(parents)-1)
            child_chr=[]
            child_w=[]
            child_l=[]
            child_id=[]
            flag.clear()
            if male != female:
                male_stack=parents[male][4]
                female_stack=parents[female][4]
             #   print(type(male_stack))
                male_stack.sort(key=lambda x:x[2],reverse=True)
                female_stack.sort(key=lambda x:x[2],reverse=True)
               # print(type(male_stack))
                #print(type(female_stack))
                male_len=len(male_stack)
                female_len=len(female_stack)
                """
                print('a')
                print(male_len)
                print(female_len)
                print('a')
                """
                index_male=0
                index_female=0
                for i in range(int(0.5*male_len)):
                    who=random.randint(1,10)
                    if(who<=5):
                        #从male中拿stack
                        accu_now=male_stack[index_male][0]
                        tail_now=male_stack[index_male][1]
                        st_now=tail_now-accu_now
                        for j in range(st_now,tail_now):
                            item_id=parents[male][3][j]
                            item_value=parents[male][0][j]
                            item_w=parents[male][1][j]
                            item_l=parents[male][2][j]
                            if(item_id not in flag.keys()):
                                child_chr.append(item_value)
                                child_id.append(item_id)
                                child_w.append(item_w)
                                child_l.append(item_l)
                                flag[item_id]=1
                        index_male+=1
                    else:
                        #从female中拿stack
                        accu_now=female_stack[index_female][0]
                        tail_now=female_stack[index_female][1]
                        st_now=tail_now-accu_now
                        for j in range(st_now,tail_now):
                            item_id=parents[female][3][j]
                            item_value=parents[female][0][j]
                            item_w=parents[female][1][j]
                            item_l=parents[female][2][j]
                            if(item_id not in flag.keys()):
                                child_chr.append(item_value)
                                child_id.append(item_id)
                                child_w.append(item_w)
                                child_l.append(item_l)
                                flag[item_id]=1
                        index_female+=1

                for i in range(0,len(parents[male][0])):
                    item_id=parents[male][3][i]
                    item_value=parents[male][0][i]
                    item_w=parents[male][1][i]
                    item_l=parents[male][2][i]
                    if(item_id not in flag.keys()):
                        child_chr.append(item_value)
                        child_id.append(item_id)
                        child_w.append(item_w)
                        child_l.append(item_l)
                        flag[item_id]=1
            
                for i in range(0,len(parents[female][0])):
                    item_id=parents[female][3][i]
                    item_value=parents[female][0][i]
                    item_w=parents[female][1][i]
                    item_l=parents[female][2][i]
                    if(item_id not in flag.keys()):
                        child_chr.append(item_value)
                        child_id.append(item_id)
                        child_w.append(item_w)
                        child_l.append(item_l)
                        flag[item_id]=1

               
            
               # print("???%d"%len(child_chr))
                children.append((child_chr,child_w,child_l,child_id,[]))    
                
                
                
        self.population = parents + children

    def mutation(self, rate):
        """
        变异，对种群的所有个体，随机改变某个个体中的某个基因
        """
        for i in range(len(self.population)):
            if random.random() < rate:
                j = random.randint(0, self.length-1)
                self.population[i][1][j],self.population[i][2][j]=self.population[i][2][j],self.population[i][1][j]
       

    def decode(self,chromosome,w,l,id,control):
        """
        解码得到此时的利用率
        """
        block_num=1
        #使用板材个数
        
        w_limit=self.bigw
        l_limit=self.bigl
        
        ch_id=id
        ans=[]
        #id_block,id_item,left_down(x,y),right_up(x,y)
        
        
        s_w=w
        s_l=l
        
        now_w=0.0#当前stack距离左边的w
        now_l=0.0#当前stack高度，相对于benchmarkl
        
        st_w=0.0#stack的w
        st_l=0.0#stack的l
        benchmarkl=now_l#下一个strip由此创建
        #表示上一个strip的高度，本strip中的stack都基于benchmarkl创建
        
        
        benchmarkl_tmp=0.0
        #记录本strip的benchmarkl

        stacks=[]
        #记录产生的栈:1.accu：栈中累计的item数量 2.i：栈尾的item的index 3.st_l：栈长 4.st_w：栈宽
        
        
        leng=len(chromosome)
        accu=0
      #  print("leng:%d"%leng)
        for i in range(leng):
            
            item_w=0
            item_l=0
            ch_now=chromosome[i]
            if(ch_now>0):
                item_w=s_w[i]
                item_l=s_l[i]
            else:
                item_w=s_l[i]
                item_l=s_w[i]
            
            if(i==0):
                benchmarkl=0
                benchmarkl_tmp=item_l
                now_l=item_l
                now_w=item_w
                st_w=item_w
                accu+=1
                ans.append((block_num,ch_id[i],0,0,item_w,item_l))
            
            else:
               # csv_now=chromosome[i]
                if(st_w==item_w):
                    #可以放进本stack
                    if(now_l+item_l<=l_limit):
                        #本stack内
                        ans.append((block_num,ch_id[i],now_w-item_w,now_l,now_w,now_l+item_l))
                        benchmarkl_tmp=max(benchmarkl_tmp,now_l+item_l)
                        now_l+=item_l
                        accu+=1
                    else:
                     #新创建一个stack，不能则加一个block
                        stacks.append((accu,i,st_l,st_w))
                        accu=1
                        if(now_w+item_w>w_limit):
                            #不能横向再加stack
                            #考虑在benchmarkl的基础上加新的stack或者增加新的block
                            if(benchmarkl_tmp+item_l<=l_limit):
                                #新的strip
                                ans.append((block_num,ch_id[i],0,benchmarkl_tmp,item_w,item_l+benchmarkl_tmp))
                                now_w=item_w
                                #此时w直接从0开始，为item_w
                                now_l=item_l+benchmarkl_tmp
                                #stack的高度为当前item高度加上当前strip的benchmarkl
                                benchmarkl=benchmarkl_tmp
                                benchmarkl_tmp=benchmarkl+item_l
                                st_w=now_w
                                st_l=item_l
                            else:
                                #此时要开一个新的block
                                block_num+=1
                                ans.append((block_num,ch_id[i],0,0,item_w,item_l))
                                benchmarkl=0.0
                                benchmarkl_tmp=item_l
                                now_l=item_l
                                now_w=item_w
                                st_w=item_w
                                st_l=item_l
                        else:
                            
                            #横向创建新的stack
                            #高度基于benchmarkl
                          #  stacks.append((accu,i,st_l,st_w))
                            ans.append((block_num,ch_id[i],now_w,benchmarkl,now_w+item_w,benchmarkl+item_l))
                            now_w=item_w+now_w
                            now_l=item_l+benchmarkl
                            benchmarkl_tmp=max(benchmarkl_tmp,now_l)
                            st_w=item_w
                            st_l=item_l
                else:
                    #暂时只能考虑w和w对齐
                    #创建新的stack
                    stacks.append((accu,i,st_l,st_w))
                    accu=1
                    if(now_w+item_w>w_limit):
                            if(benchmarkl_tmp+item_l<=l_limit):
                                #新的strip
                                ans.append((block_num,ch_id[i],0,benchmarkl_tmp,item_w,item_l+benchmarkl_tmp))
                                now_w=item_w
                                #此时w直接从0开始，为item_w
                                now_l=item_l+benchmarkl_tmp
                                #stack的高度为当前item高度加上当前strip的benchmarkl
                                benchmarkl=benchmarkl_tmp
                                benchmarkl_tmp=benchmarkl+item_l
                                st_w=now_w
                                st_l=item_l
                            else:
                                #此时要开一个新的block
                                block_num+=1
                                ans.append((block_num,ch_id[i],0,0,item_w,item_l))
                                benchmarkl=0.0
                                benchmarkl_tmp=item_l
                                now_l=item_l
                                now_w=item_w
                                st_w=item_w
                                st_l=item_l
                    else:  
                        #横向创建新的stack
                        #高度基于benchmarkl
                        ans.append((block_num,ch_id[i],now_w,benchmarkl,now_w+item_w,benchmarkl+item_l))
                        now_w=item_w+now_w
                        now_l=item_l+benchmarkl
                        benchmarkl_tmp=max(benchmarkl_tmp,now_l)
                        st_w=item_w
                        st_l=item_l
        return self.s/(block_num*self.block_s),ans,stacks
                
                    

    def result(self,control):
        """
         获得当前代的最优值，这里取的是函数取最大值时候的x的值
        """
        graded = [(self.fitness(chromosome,w,l,id,control,stacks), (chromosome,w,l,id,control,stacks)) for chromosome,w,l,id,stacks in self.population]
       # print(graded)
        graded = [x[1] for x in sorted(graded, reverse = True)]
        return self.decode(graded[0][0],graded[0][1],graded[0][2],graded[0][3],control)
    
    
    