#00 필요 모듈
import random 
import copy # deepcopy를 위함
import operator

## 공정 상황
lot_A,lot_B,lot_C = 3,2,1
A = [i for i in range(int(lot_A))]
B = [A[-1]+i+1 for i in range(int(lot_B))]
C = [B[-1]+i+1 for i in range(int(lot_C))]
runtime_A = [18,6,3,1,192,2] 
runtime_B = [2,2,1,1,60,1]
runtime_C = [1,2,2,1,60,1]
process = [1,2,3,4,5,6]  
INF = 99999



#01 초기 염색체의 집합(염색체500개)을 생성한다.
# gene : 유전인자 -> 공정 시작 시간
# chromosome : 염색체 : 주어진 문제에 대한 가능한 해들을 정해진 형태의 자료구조로 표현한것-> 파라미터
# population : 염색체의 집합 
def chromosome():  
    
    schedule_A_fator = []
    schedule_A_ST = []
    
    for i in range(lot_A):
        each_list = []
        each_list += ["A"+"lot"+str(i+1)+"_"+str(process[j]) for j in range(6)]
        schedule_A_fator += [each_list] 
    
    
    for i in schedule_A_fator:
        each_ST=[0]
        each_ST[0] = random.randint(1,36) #478
        for j in range(5): # 6개의 공정
            #limit = [496,502,505,506,698]
            limit = [60,80,100,300,698] # 공정1-4 100이하에서
            ST = random.randint(each_ST[j]+runtime_A[j],limit[j])
            each_ST += [ST]
        schedule_A_ST += [each_ST]
    #schedule_A_ST += ["//"]
        
        
    schedule_B_fator = []
    schedule_B_ST = []
    for i in range(lot_B):
        each_list = []
        each_list += ["B"+"lot"+str(i+1)+"_"+str(process[j]) for j in range(6)]
        schedule_B_fator += [each_list] 
    
    
    for i in schedule_B_fator:
        each_ST=[0]
        each_ST[0] = random.randint(1,36) #633
        for j in range(5): # 6개의 공정
            #limit = [635,637,638,639,699]
            limit = [40,60,100,300,699] # 공정1-4 100이하에서
            ST = random.randint(each_ST[j]+runtime_B[j],limit[j])
            each_ST += [ST]
        schedule_B_ST += [each_ST]
    #schedule_B_ST += ["//"]
        

    schedule_C_fator = []
    schedule_C_ST = []
    for i in range(lot_C):
        each_list = []
        each_list += ["C"+"lot"+str(i+1)+"_"+str(process[j]) for j in range(6)]
        schedule_C_fator += [each_list] 
    
    
    for i in schedule_C_fator:
        each_ST=[0]
        each_ST[0] = random.randint(1,36) #633
        for j in range(5): # 6개의 공정
            #limit = [634,636,638,639,699]
            limit = [40,60,100,300,699] # 공정1-4 100이하에서
            ST = random.randint(each_ST[j]+runtime_C[j],limit[j])
            each_ST += [ST]
        schedule_C_ST += [each_ST]
    #schedule_C_ST += ["//"]

    schedule_fator = schedule_A_fator +schedule_B_fator +schedule_C_fator
    schedule_ST = schedule_A_ST + schedule_B_ST + schedule_C_ST 
    return schedule_fator ,schedule_ST  



#최종완료시간계산
def total_CT(schedule_ST):
    total_lot = len(schedule_ST)
    last_process_ST = []
    
   
    
    for i in range(total_lot):
        last_process_ST += [schedule_ST[i][5]]  
        
    CT = [0]*len(last_process_ST)
    for i in A:
        CT[i] = last_process_ST[i] + int(1)
    for i in B:
        CT[i] = last_process_ST[i] + int(0)
    for i in C:
        CT[i] = last_process_ST[i] + int(0)
        
    last_CT = max(CT)
    
    return last_CT

#n개의 공정스케줄링 chromosome 생성 및 저장
def chromosome_set1(n):
    chromosome_set = {}
    for i in range(n):
        schedule_fator, schedule_ST = chromosome()
        last_CT = total_CT(schedule_ST)
        chromosome_set[i+1] = [last_CT,schedule_ST]
        
    return chromosome_set,schedule_fator, schedule_ST
# 염색체 집합 생성 및 염색체 별 
chromosome_set,schedule_fator, schedule_ST = chromosome_set1(500)   
def new_sort(x):
    for i in range(len(x)):
        lista = list(x[i+1])
        return lista[0]
        
#      

def fitness_function(chromosome_set):
    nums_of_chro = len(chromosome_set)
    fitness_set = {}
    for i in range(nums_of_chro):
        
        
        
        fitness_set[i+1]=chromosome_set[i+1][0]
   
    return fitness_set

fitness_set = fitness_function(chromosome_set)



def constraint(chromosome_set,fitness_set):
    t_set=[]
    for i in chromosome_set: # i+1번째 염색체(1번째 염색체,i=0)
        
        t = [[] for _ in range(701)] # 시간 인덱스 700까지
        t_assemble = [[] for _ in range(701)] # 시간 인덱스 700까지
        t_dcac = [[] for _ in range(701)]
        t_load = [[] for _ in range(701)]
        t_os = [[] for _ in range(701)]
        t_dm = [[] for _ in range(701)]
        
        t_1 =[[] for _ in range(701)]
        t_2 =[[] for _ in range(701)]
        t_3 =[[] for _ in range(701)]
        t_4 =[[] for _ in range(701)]
        t_6 =[[] for _ in range(701)]
        solution1 = chromosome_set[i]  
        fitness_value = solution1[0] 
        chromosomes = solution1[1]
        for j in A: # A제품 생산시간 할당
            #globals()['{}염색체_A_{}'.format(i,j+1)] = chromosomes[j]
            name = 'A'+'lot'+str(A[j]+1)+'_'
            for process_ in range(6): #총 인력
                for time in range(runtime_A[process_]):
                    t[chromosomes[j][process_]+time]+=[name+str(process_+1)]      
            #조립공정
            for process_ in [0]: #1번 공정
                for time in range(runtime_A[process_]):
                    t_1[chromosomes[j][process_]+time]+=[name+str(process_+1)]      
            for process_ in [2]: #3번 공정
                for time in range(runtime_A[process_]):
                    t_3[chromosomes[j][process_]+time]+=[name+str(process_+1)] 
            for process_ in [0,2]: #전동기 6대
                for time in range(runtime_A[process_]):
                    t_assemble[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            
                    
            #검사공정         
            for process_ in [1]: #2번 공정
                for time in range(runtime_A[process_]):
                    t_2[chromosomes[j][process_]+time]+=[name+str(process_+1)]             
            for process_ in [3]: #4번 공정
                for time in range(runtime_A[process_]):
                    t_4[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
            for process_ in [5]: #6번 공정
                for time in range(runtime_A[process_]):
                    t_6[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
            
    
            for process_ in [1,3,5]: 
                for time in range(runtime_A[process_]):
                    t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,3,5]: 
                for time in range(runtime_A[process_]):
                    t_load[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,5]: 
                for time in range(runtime_A[process_]):
                    t_os[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                    t_os[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,5]: 
                for time in range(runtime_A[process_]):
                    t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                    
    
        
            
        for j in B: # B제품 생산시간 할당
            #globals()['{}염색체_B_{}'.format(i,j-len(A)+1)] = chromosomes[j]
            name = 'B'+'lot'+str(j-len(A)+1)+'_'
            for process_ in range(6):
                for time in range(runtime_B[process_]):
                    t[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            #조립공정
            for process_ in [0]: #1번 공정
                for time in range(runtime_B[process_]):
                    t_1[chromosomes[j][process_]+time]+=[name+str(process_+1)]      
            for process_ in [2]: #3번 공정
                for time in range(runtime_B[process_]):
                    t_3[chromosomes[j][process_]+time]+=[name+str(process_+1)] 
            for process_ in [0,2]: #전동기 6대
                for time in range(runtime_B[process_]):
                    t_assemble[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            
                    
            #검사공정         
            for process_ in [1]: #2번 공정
                for time in range(runtime_B[process_]):
                    t_2[chromosomes[j][process_]+time]+=[name+str(process_+1)]             
            for process_ in [3]: #4번 공정
                for time in range(runtime_B[process_]):
                    t_4[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
            for process_ in [5]: #6번 공정
                for time in range(runtime_B[process_]):
                    t_6[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
            
    
            for process_ in [1,3,5]: 
                for time in range(runtime_B[process_]):
                    t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,3,5]: 
                for time in range(runtime_B[process_]):
                    t_load[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,5]: 
                for time in range(runtime_B[process_]):
                    t_os[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,5]: 
                for time in range(runtime_B[process_]):
                    t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                    t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                    
        for j in C: # A제품 생산시간 할당
            #globals()['{}염색체_C_{}'.format(i,j-len(A+B)+1)] = chromosomes[j]
            name = 'C'+'lot'+str(j-len(A+B)+1)+'_'
            for process_ in range(6):
                for time in range(runtime_C[process_]):
                    t[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            #조립공정
            for process_ in [0]: #1번 공정
                for time in range(runtime_C[process_]):
                    t_1[chromosomes[j][process_]+time]+=[name+str(process_+1)]      
            for process_ in [2]: #3번 공정
                for time in range(runtime_C[process_]):
                    t_3[chromosomes[j][process_]+time]+=[name+str(process_+1)] 
            for process_ in [0,2]: #전동기 6대
                for time in range(runtime_C[process_]):
                    t_assemble[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            
                    
            #검사공정         
            for process_ in [1]: #2번 공정
                for time in range(runtime_C[process_]):
                    t_2[chromosomes[j][process_]+time]+=[name+str(process_+1)]             
            for process_ in [3]: #4번 공정
                for time in range(runtime_C[process_]):
                    t_4[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
            for process_ in [5]: #6번 공정
                for time in range(runtime_C[process_]):
                    t_6[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
            
    
            for process_ in [3]: 
                for time in range(runtime_C[process_]):
                    t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,5]: 
                for time in range(runtime_C[process_]):
                    t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                    t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                    
            for process_ in [1,3,5]: 
                for time in range(runtime_C[process_]):
                    t_load[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,5]: 
                for time in range(runtime_C[process_]):
                    t_os[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            for process_ in [1,5]: 
                for time in range(runtime_C[process_]):
                    t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                    t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                    t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
            
    
        total_t = [t,t_1,t_3,t_assemble,t_2,t_4,t_6,t_dcac,t_load,t_os,t_dm]
        
        t_set.append(total_t)
    
           



    for i in range(len(chromosome_set)): # i+1번째 염색체 (i=0 : 1번 염색체)
    #[t,t_1,t_3,t_assemble,t_2,t_4,t_6,t_dcac,t_load,t_os,t_dm]
        t = t_set[i][0]
        t_1 = t_set[i][1]
        t_3 = t_set[i][2]
        t_assemble = t_set[i][3]
        t_2 = t_set[i][4]
        t_4 = t_set[i][5]
        t_6 = t_set[i][6]
        t_dcac = t_set[i][7]
        t_load = t_set[i][8]
        t_os = t_set[i][9]
        t_dm = t_set[i][10]
        
        
        #모든 공정에 투입된 인력은 총 가용 인력(10)인을 넘을 수 없다.
        for j in range(len(t)):  
            if len(t[j]) > 10:
                fitness_set[i+1]=INF
                break
        #모든 조립 공정에 투입된 인력은 최대 가용 인력(4인)을 넘을 수 없다
            if len(t_1[j]) > 4 or len(t_3[j]) > 4:
                fitness_set[i+1]=INF
                break
           
        #모든 검사 공정에 투입된 인력은 최대 가용 인력(2인)을 넘을 수 없다
        for j in range(len(t)):  
            if len(t_2[j]) > 2 or len(t_4[j]) > 2 or len(t_6[j]) > 2:
                fitness_set[i+1]=INF
                break
            
        # 전동기는 6대 
        for j in range(len(t)):  
            if len(t_assemble[j]) > 6:
                fitness_set[i+1]=INF
                break
        # dcac는 8대 
        for j in range(len(t)):  
            if len(t_dcac[j]) > 8:
                fitness_set[i+1]=INF
                break
        # load는 10대 
        for j in range(len(t)):  
            if len(t_load[j]) > 10:
                fitness_set[i+1]=INF
                break
        # os는 7대 
        for j in range(len(t)):  
            if len(t_os[j]) > 7:
                fitness_set[i+1]=INF
                break
        # dm는 9대 
        for j in range(len(t)):  
            if len(t_dm[j]) > 9:
                fitness_set[i+1]=INF
                break
        
        # value값 기준 정렬
        fitness_set = sorted(fitness_set.items(),key = lambda x : x[1],reverse=True)
        value_sort = copy.deepcopy(fitness_set)
        fitness_set = dict(fitness_set)


    return fitness_set , value_sort
                
constraint , value_sort=constraint(chromosome_set,fitness_set)




def trim_chromoseome(constraint):
    trim_chromosome_set = copy.deepcopy(chromosome_set)
    key = dict.keys(constraint)
    key = set(key)
    for i in key:
        if constraint[i] == 99999:
            del trim_chromosome_set[i]
    return trim_chromosome_set

trim_chromosome_set=trim_chromoseome(constraint)


    
def mutation(trim_chromosome_set):
    new_chromosome_set = {}
    for i in range(50):
        
        # 1-4 공정
        new_chromosome=[[] for _ in range(lot_A+lot_B+lot_C)]
        chromosome_number = []
        STs = [[] for _ in range(5)]
        for j in range(5):
            pop = value_sort.pop() #(염색체,적합도값)        
            chromosome_number += [pop[0]]
            
        
            STs[j] += trim_chromosome_set[chromosome_number[j]][1] 
        print(chromosome_number)
        
        for lot in range(lot_A+lot_B+lot_C):
            process_1 =[]
            
            for _ in range(5):
                process_1.append(STs[_][lot][0])
            selection = min(process_1)
            selection_index = process_1.index(selection)
            selection_chromosome_number = chromosome_number[selection_index]
            selection_chromosome = trim_chromosome_set[selection_chromosome_number][1]
            
            
            new_chromosome[lot] += selection_chromosome[lot][0:4]
            
        # 5-6 공정
        
        
        for lot in range(lot_A+lot_B+lot_C):
            process_5 =[]
            
            for _ in range(5):
                process_5.append(STs[_][lot][4])
            selection = min(process_5)
            selection_index = process_5.index(selection)
            selection_chromosome_number = chromosome_number[selection_index]
            selection_chromosome = trim_chromosome_set[selection_chromosome_number][1]
            
            
            new_chromosome[lot] += selection_chromosome[lot][4:6]
        
        process6 = []
        
        for lot in range(lot_A+lot_B+lot_C):
            process6.append(new_chromosome[lot][5])
                
        fitness = max(process6)
        
        
        new_chromosome_set[i+1]=[fitness,new_chromosome]
        
            
    return new_chromosome_set 
new_chromosome_set = mutation(trim_chromosome_set)
    
# 새로운 염색체 집합이 제약식을 통과하는지 확인필요
new_fitness_set = fitness_function(new_chromosome_set)    
# value값 기준 정렬


new_value = sorted(new_fitness_set.items(),key =  lambda x : x[1],reverse=True)
#constraint , value_sort=constraint(new_chromosome_set,new_fitness_set)

#new_chromosome_set_sort = sorted(new_chromosome_set.items(),key = lambda x : x[1])




# new_t_set=[]
# for i in new_chromosome_set: # i+1번째 염색체(1번째 염색체,i=0)
    
#     new_t = [[] for _ in range(701)] # 시간 인덱스 700까지
#     new_t_assemble = [[] for _ in range(701)] # 시간 인덱스 700까지
#     new_t_dcac = [[] for _ in range(701)]
#     new_t_load = [[] for _ in range(701)]
#     new_t_os = [[] for _ in range(701)]
#     new_t_dm = [[] for _ in range(701)]
    
#     new_t_1 =[[] for _ in range(701)]
#     new_t_2 =[[] for _ in range(701)]
#     new_t_3 =[[] for _ in range(701)]
#     new_t_4 =[[] for _ in range(701)]
#     new_t_6 =[[] for _ in range(701)]
#     solution1 = new_chromosome_set[i]  
#     fitness_value = solution1[0] 
#     chromosomes = solution1[1]
#     for j in A: # A제품 생산시간 할당
#         #globals()['{}염색체_A_{}'.format(i,j+1)] = chromosomes[j]
#         name = 'A'+'lot'+str(A[j]+1)+'_'
#         for process_ in range(6): #총 인력
#             for time in range(runtime_A[process_]):
#                 t[chromosomes[j][process_]+time]+=[name+str(process_+1)]      
#         #조립공정
#         for process_ in [0]: #1번 공정
#             for time in range(runtime_A[process_]):
#                 new_t_1[chromosomes[j][process_]+time]+=[name+str(process_+1)]      
#         for process_ in [2]: #3번 공정
#             for time in range(runtime_A[process_]):
#                 new_t_3[chromosomes[j][process_]+time]+=[name+str(process_+1)] 
#         for process_ in [0,2]: #전동기 6대
#             for time in range(runtime_A[process_]):
#                 new_t_assemble[chromosomes[j][process_]+time]+=[name+str(process_+1)]
        
                
#         #검사공정         
#         for process_ in [1]: #2번 공정
#             for time in range(runtime_A[process_]):
#                 new_t_2[chromosomes[j][process_]+time]+=[name+str(process_+1)]             
#         for process_ in [3]: #4번 공정
#             for time in range(runtime_A[process_]):
#                 new_t_4[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
#         for process_ in [5]: #6번 공정
#             for time in range(runtime_A[process_]):
#                 new_t_6[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
        

#         for process_ in [1,3,5]: 
#             for time in range(runtime_A[process_]):
#                 new_t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,3,5]: 
#             for time in range(runtime_A[process_]):
#                 new_t_load[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,5]: 
#             for time in range(runtime_A[process_]):
#                 new_t_os[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#                 new_t_os[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,5]: 
#             for time in range(runtime_A[process_]):
#                 new_t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                

    
        
#     for j in B: # B제품 생산시간 할당
#         #globals()['{}염색체_B_{}'.format(i,j-len(A)+1)] = chromosomes[j]
#         name = 'B'+'lot'+str(j-len(A)+1)+'_'
#         for process_ in range(6):
#             for time in range(runtime_B[process_]):
#                 new_t[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         #조립공정
#         for process_ in [0]: #1번 공정
#             for time in range(runtime_B[process_]):
#                 new_t_1[chromosomes[j][process_]+time]+=[name+str(process_+1)]      
#         for process_ in [2]: #3번 공정
#             for time in range(runtime_B[process_]):
#                 new_t_3[chromosomes[j][process_]+time]+=[name+str(process_+1)] 
#         for process_ in [0,2]: #전동기 6대
#             for time in range(runtime_B[process_]):
#                 new_t_assemble[chromosomes[j][process_]+time]+=[name+str(process_+1)]
        
                
#         #검사공정         
#         for process_ in [1]: #2번 공정
#             for time in range(runtime_B[process_]):
#                 new_t_2[chromosomes[j][process_]+time]+=[name+str(process_+1)]             
#         for process_ in [3]: #4번 공정
#             for time in range(runtime_B[process_]):
#                 new_t_4[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
#         for process_ in [5]: #6번 공정
#             for time in range(runtime_B[process_]):
#                 new_t_6[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
        

#         for process_ in [1,3,5]: 
#             for time in range(runtime_B[process_]):
#                 new_t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,3,5]: 
#             for time in range(runtime_B[process_]):
#                 new_t_load[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,5]: 
#             for time in range(runtime_B[process_]):
#                 new_t_os[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,5]: 
#             for time in range(runtime_B[process_]):
#                 new_t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#                 new_t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                
#     for j in C: # A제품 생산시간 할당
#         #globals()['{}염색체_C_{}'.format(i,j-len(A+B)+1)] = chromosomes[j]
#         name = 'C'+'lot'+str(j-len(A+B)+1)+'_'
#         for process_ in range(6):
#             for time in range(runtime_C[process_]):
#                 new_t[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         #조립공정
#         for process_ in [0]: #1번 공정
#             for time in range(runtime_C[process_]):
#                 new_t_1[chromosomes[j][process_]+time]+=[name+str(process_+1)]      
#         for process_ in [2]: #3번 공정
#             for time in range(runtime_C[process_]):
#                 new_t_3[chromosomes[j][process_]+time]+=[name+str(process_+1)] 
#         for process_ in [0,2]: #전동기 6대
#             for time in range(runtime_C[process_]):
#                 new_t_assemble[chromosomes[j][process_]+time]+=[name+str(process_+1)]
        
                
#         #검사공정         
#         for process_ in [1]: #2번 공정
#             for time in range(runtime_C[process_]):
#                 new_t_2[chromosomes[j][process_]+time]+=[name+str(process_+1)]             
#         for process_ in [3]: #4번 공정
#             for time in range(runtime_C[process_]):
#                 new_t_4[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
#         for process_ in [5]: #6번 공정
#             for time in range(runtime_C[process_]):
#                 new_t_6[chromosomes[j][process_]+time]+=[name+str(process_+1)]    
        

#         for process_ in [3]: 
#             for time in range(runtime_C[process_]):
#                 new_t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,5]: 
#             for time in range(runtime_C[process_]):
#                 new_t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#                 new_t_dcac[chromosomes[j][process_]+time]+=[name+str(process_+1)]
                
#         for process_ in [1,3,5]: 
#             for time in range(runtime_C[process_]):
#                 new_t_load[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,5]: 
#             for time in range(runtime_C[process_]):
#                 new_t_os[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#         for process_ in [1,5]: 
#             for time in range(runtime_C[process_]):
#                 new_t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#                 new_t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
#                 new_t_dm[chromosomes[j][process_]+time]+=[name+str(process_+1)]
        

#     new_total_t = [new_t,new_t_1,new_t_3,new_t_assemble,new_t_2,new_t_4,new_t_6,new_t_dcac,new_t_load,new_t_os,new_t_dm]
    
#     new_t_set.append(new_total_t)
         
# new_fitness_set = fitness_function(new_chromosome_set)

############################

# value_sort = list(value_sort)
# for i in value_sort:
#     if i[1] == 99999:
#         value_sort.remove(i)



# # 99999가 아닌 염색체의 갯수
# def available_chrome(constraint):
#     count = 0
#     key = dict.keys(constraint)
#     key = set(key)
#     available = []
#     for i in key:
#         if constraint[i] == 99999:
#             pass
#         else:
#             count += 1
#             available.append(i)
#     return count , available

# available_chrome_count, available_chrome = available_chrome(constraint)