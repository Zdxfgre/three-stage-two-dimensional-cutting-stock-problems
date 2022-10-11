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
    def __init__(self, length, count, strip,strip_w,strip_l,bigw,bigl,s,strip_id):
        self.length = length #染色体长度
        self.count = count #种群中染色体数量
        self.strip=strip#数据
        self.strip_w=strip_w#宽
        self.stripl=strip_l#长
        self.bigw=bigw
        self.bigl=bigl
        self.alls=0.0#使用板材面积
        self.strip_id=strip_id
        self.s=s
        self.block_s=bigw*bigl
        self.population = self.gen_population(length, count, strip) #目前排序生成

    def evolve(self,retain_rate = 0.2, random_select_rate = 0.5, mutation_rate = 0.01):
        """
        进化，对当前一代种群一次进行选择，交叉并产生新一代种群，然后对新一代种群进行变异
        """
        parents = self.selection(retain_rate, random_select_rate)
       # print("numpar:%d"%len(parents))
        self.crossover(parents)
        self.mutation(mutation_rate)

    def gen_chromosome(self, length, strip):
        """
        用一个实数表示一个基因
        """
        
        #(strip_id,strip_w,strip_l,stack_id)

        #random.shuffle(strip)
        rstrip=strip
        chromosome = []
        ch_w = []
        ch_l = []
        ch_id = []
        strip_stack=[]

        for i in range(length):
            ch_w.append(rstrip[i][1])
            ch_l.append(rstrip[i][2])
            ch_id.append(rstrip[i][0])
            #strip_stack.append(list(rstrip[3]))
            chromosome.append(rstrip[i][0])
        """
        for i in range(length):
            chromosome |= (1 << i) * random.randint(0,1)
        """
        #整数编码
        return (chromosome,ch_w,ch_l,ch_id,rstrip)

    def gen_population(self,length,count,strip):
        """
        获取初始种群（一个含有count个长度为length的染色体列表）
        """
        return [self.gen_chromosome(length,strip) for i in range(count)]

    def fitness(self, chromosome, w, l,id, control,rstrip):
        """
        染色体解码为布局方案
        并得到对应利用率
        
        """
        #返回利用的板子数量
        x = self.decode(chromosome,w,l,id,control,rstrip)
        return x

    def selection(self, retain_rate, random_select_rate):
        """
        选择
        先对适应度从大到小排序，选出存活的染色体
        在进行随机选择，选出适应度虽然小，但是幸存下来的个体
        """
        #对适应度从大到小排序
        graded=[]
      #  print(len(self.population[0]))
        for chromosome,w,l,id,rstrip  in self.population:
          #  print("che%d"%len(chromosome))
            fit,sta=self.fitness(chromosome,w,l,id,0,rstrip)
            graded.append((fit,(chromosome,w,l,id,rstrip)))
        
        #graded = [(self.fitness(chromosome,w,l,id,0,stacks), (chromosome,w,l,id,stacks)) for chromosome,w,l,id,stacks in self.population]
       # print(graded)
        graded = [x[1] for x in sorted(graded, reverse = True)]
        #print(graded[0])
        #选出适应性强的染色体
        retain_length = int(len(graded) * retain_rate)
        parents = graded[:retain_length]
        #选出是是影响不强，但是幸存的染色体
        for chromosome,w,l,id,rstrip in graded[retain_length:]:
            if random.random() < random_select_rate:
                parents.append((chromosome,w,l,id,rstrip))
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
            child_strip=[]
            flag.clear()

            now_num=0
            if male != female:
                male_strip=parents[male][4]
                female_strip=parents[female][4]
                #chromosome,ch_w,ch_l,ch_id,stacks
             #   print(type(male_stack))
                male_strip.sort(key=lambda x:x[2],reverse=True)
                female_strip.sort(key=lambda x:x[2],reverse=True)
                
                if(len(male_strip)>1 and len(female_strip)>1):
                    index_male=random.randint(0,len(male_strip)-1)
                    index_female=random.randint(0,len(female_strip)-1)
                else:
                    index_male=0
                    index_female=0
                
                male_strip_tmp_1=[]
                male_strip_tmp_2=[]
                female_strip_tmp_1=[]
                female_strip_tmp_2=[]
                """
                for i in range(0,len(male_strip)):
                    chose=random.randint(1,10)
                    if(chose<=5):
                        male_strip_tmp_1.append(male_strip[i])
                    else:
                        male_strip_tmp_2.append(male_strip[i])
                male_strip_tmp_1.sort(key=lambda x:x[1],reverse=True)
                male_strip_tmp_2.sort(key=lambda x:x[2],reverse=True)
                male_strip.clear()
                for i in range(len(male_strip_tmp_1)):
                    male_strip.append(male_strip_tmp_1[i])
                for i in range(len(male_strip_tmp_2)):
                    male_strip.append(male_strip_tmp_2[i]) 
                """
                """
                for i in range(0,len(female_strip)):
                    chose=random.randint(1,10)
                    if(chose<=5):
                        female_strip_tmp_1.append(female_strip[i])
                    else:
                        female_strip_tmp_2.append(female_strip[i])
                female_strip_tmp_1.sort(key=lambda x:x[1],reverse=True)
                female_strip_tmp_2.sort(key=lambda x:x[2],reverse=True)
                female_strip.clear()
                for i in range(len(female_strip_tmp_1)):
                    female_strip.append(female_strip_tmp_1[i])
                for i in range(len(female_strip_tmp_2)):
                    female_strip.append(female_strip_tmp_2[i])   
                """
                
               # print(type(male_stack))
                #print(type(female_stack))
                male_len=len(male_strip)
                need_num=int(0.01*male_len)
                for i in range(male_len):
                    if(now_num>=need_num):
                        break
                    who=random.randint(1,10)
                    if(who<=1):
                        for j in range(len(male_strip)):
                            now_id=male_strip[j][0]
                            strip_info=male_strip[j]
                            strip_id=male_strip[j][0]
                            strip_w=male_strip[j][1]
                            strip_l=male_strip[j][2]
                            if(now_id not in flag.keys()):
                                now_num+=1
                                flag[now_id]=1
                                child_strip.append(strip_info)
                                child_chr.append(strip_id)
                                child_w.append(strip_w)
                                child_l.append(strip_l)
                                break
                                
                    else:
                        #从female中拿stack
                        for j in range(len(female_strip)-1,0,-1):
                            now_id=female_strip[j][0]
                            strip_info=female_strip[j]
                            strip_id=female_strip[j][0]
                            strip_w=female_strip[j][1]
                            strip_l=female_strip[j][2]
                            if(now_id not in flag.keys()):
                                now_num+=1
                                flag[now_id]=1
                                child_strip.append(strip_info)
                                child_chr.append(strip_id)
                                child_w.append(strip_w)
                                child_l.append(strip_l)
                                break

                for j in range(len(male_strip)):
                    now_id=male_strip[j][0]
                    strip_info=male_strip[j]
                    strip_id=male_strip[j][0]
                    strip_w=male_strip[j][1]
                    strip_l=male_strip[j][2]
                    if(now_id not in flag.keys()):
                        flag[now_id]=1
                        child_strip.append(strip_info)
                        child_chr.append(strip_id)
                        child_w.append(strip_w)
                        child_l.append(strip_l)
            
                for j in range(len(female_strip)):
                    now_id=female_strip[j][0]
                    strip_info=female_strip[j]
                    strip_id=female_strip[j][0]
                    strip_w=female_strip[j][1]
                    strip_l=female_strip[j][2]
                    if(now_id not in flag.keys()):
                        flag[now_id]=1
                        child_strip.append(strip_info)
                        child_chr.append(strip_id)
                        child_w.append(strip_w)
                        child_l.append(strip_l)

               

               # print("???%d"%len(child_chr))
                children.append((child_chr,child_w,child_l,child_id,child_strip)) 
                
        self.population = parents + children

    def mutation(self, rate):
        """
        变异，对种群的所有个体，随机改变某个个体中的某个基因
        """
        for i in range(len(self.population)):
            if random.random() < rate:
                leng=len(self.population[i][4])
                j = random.randint(0, leng-1)
                k = random.randint(0, leng-1)
                self.population[i][4][j],self.population[i][4][k]=self.population[i][4][j],self.population[i][4][k]

               # self.population[i][3][j],self.population[i][3][k]=self.population[i][3][j],self.population[i][3][k]
                
                
                
                
       

    def decode(self,chromosome,w,l,id,control,rstrip):
        """
        解码得到此时的利用率
        """
        block_num=1

        w_limit=self.bigw
        l_limit=self.bigl
        #板子的长宽
        
       # print(l_limit)
        now_l=0.0
        #当前累计的高度
        now_w=0.0
        #当前累计宽度
        #(strip_id,strip_w,strip_l,stack_id)
        strip=self.strip
        
        benchmark_l=0.0
        
        ans=[]
        #记录每个strip的位置
        strip_accu=[]
        for i in range(len(rstrip)):
            strip_w=rstrip[i][1]
            strip_l=rstrip[i][2]
            #当前的strip的长宽
            
            strip_id=rstrip[i][0]
            
            if(now_w+strip_w<=w_limit):
                strip_accu.append((block_num,strip_id,now_w,benchmark_l))
                now_w+=strip_w
                now_l=max(now_l,strip_l)
            elif(now_l+strip_l<=l_limit):
                #表示当前板子里面还能放strip
                strip_accu.append((block_num,strip_id,0,now_l))
                benchmark_l=now_l
                now_l+=strip_l
            else:
                block_num+=1
                ans.append(list(strip_accu))
                strip_accu.clear()
                strip_accu.append((block_num,strip_id,0,0))
                now_l=strip_l
                benchmark_l=0.0
            
        
        ans.append(strip_accu)
        return block_num,ans
                
                    

    def result(self,control):
        """
         获得当前代的最优值，这里取的是函数取最大值时候的x的值
        """
        graded = [(self.fitness(chromosome,w,l,id,control,rstrip), (chromosome,w,l,id,control,rstrip)) for chromosome,w,l,id,rstrip in self.population]
       # print(graded)
        graded = [x[1] for x in sorted(graded, reverse = True)]
        return self.decode(graded[0][0],graded[0][1],graded[0][2],graded[0][3],control,graded[0][5])