import os
import math
#import resource
from functools import cmp_to_key
import time
import sys

class filet:
    
  def __init__(self,tup_val,fi_no):
    self.tup_val=tup_val
    self.fi_no=fi_no



def limit_memory(maxsize): 
    soft, hard = resource.getrlimit(resource.RLIMIT_AS) 
    print(soft)
    print(hard)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))

def compare(t11,t22):
  temp1=[]
  t1=t11.strip().split("  ")
  t2=t22.strip().split("  ")
  for c in cols:
    v1=t1[mdata[c][0]]
    v2=t2[mdata[c][0]]
    if v1==v2:
      continue
    elif v1<v2 and order=="asc" or (v1>v2 and order=="desc"):
      return -1
    elif  v1>v2 and order=="asc" or (v1<v2 and order=="desc"):
      return 1

  return 0 




def buildminheap(a, n):
  for  j in  range(int(n/2), -1, -1):
    minheapify(a,j,n)


def minheapify(a, i,n):
  smallest=i
  left = (2*i+1)
  right = ((2*i)+2)
  if (left >=n):
    return
  else:
    if (left < n and compare(a[left].tup_val,a[i].tup_val)==-1):
      smallest = left
    else:
      smallest = i
    if (right < n  and compare(a[right].tup_val,a[smallest].tup_val)==-1):
      smallest = right;
    if (smallest != i):
      temp = a[i]
      a[i] = a[smallest]
      a[smallest] = temp
      minheapify(a, smallest,n)
        


start_time = time.time()
        
#x= input()  

"""Parsing metadata file"""

mdata={}
no_of_tup=0
f = open("metadata.txt", "r")
t=f.readlines()
#print(t)

f.close()
tuples=0
i=0
for k in t:
  tt=k.split(",")
  tem=[]
  tem.append(i)
  tem.append(tt[1].strip())
  mdata[tt[0]]=tem
  tuples+=int(tt[1])+2
  i+=1




#list of columns on which sorting to be done
cols=[]
#Input and output files
inputn=""
output=""
#Main memory size in MB
main=0
#order

#x= "input.txt output.txt 0.25 asc Name Address"

# ./sort input.txt output.txt 0.25 asc C1 C2 (for part1)
#temp=x.split(' ')
inputn=sys.argv[1]
output=sys.argv[2]
main=float(sys.argv[3])*1024*1024
order=sys.argv[4]
cols=sys.argv[5:]
print(cols)
#print(temp)
#print(f"{inputn}:{output}:{main}:{order}")
#print(cols)

if(tuples>=main):
    print("2 way merge sort not feasible with this memory")
    sys.exit()

print("###Start execution")

"""Counting number of tupeles in our input file"""
f = open(inputn, "r")

count_t=0
while True:
  ttt=f.readline()
  if not ttt:
    break
  count_t+=1  

f.close()

print("###Running Phase 1")

#print(count_t)
no_of_tup=count_t
#print(no_of_tup)

#tuples=tuples+2*(count_of_cols)
size=no_of_tup*tuples
print("Size of File "+str(size)+" Bytes")
print("Size of Main Memory "+str(main)+"Bytes")

#limit_memory(0.0014781951*1024*1024)
#process = psutil.Process(os.getpid())
#print(process.memory_info().rss) 


tup_in_file=math.floor(main/tuples)
#print("Number of Tuples in 1 file "+ str(tup_in_file))

no_of_files= math.ceil(no_of_tup/tup_in_file)
#tup_in_file=int(no_of_tup/no_of_files)
print("Number of sub-files splits " +str(no_of_files))

count_file=0
#filenames=[]


file1=open(inputn, "r")
while(True):
  tupc=[]
  k=tup_in_file
  while(k):
    #tup=[]
    line1=file1.readline()
    if not line1:
      break
    #tup=line1.split("  ")
    tupc.append(line1)
    k-=1
  
  if(k==tup_in_file):
    break
  count_file+=1
  #sort(tupc,order,cols)
  #print(type(tupc[0]))
  print("Sorting #"+str(count_file)+"sublist")
  tupc=sorted(tupc, key=cmp_to_key(compare))
  if no_of_files==1:
    f_name="output.txt"
  else:  
    f_name=str(count_file-1)+".txt"
  #filenames.append(f_name)
  fw= open(f_name,"w+")
  print("Writing to disk #"+str(count_file))
  for k in tupc:
    fw.write(k)
  fw.close()
file1.close()

if no_of_files==1:
    print("###Completed Execution")
    elapsed_time = time.time() - start_time
    print("\nTime elapsed(in seconds): ",elapsed_time)
    sys.exit()
#input.txt output.txt 0.25 asc C1 C2
#input1.txt output.txt 0.0014781951 asc C1 C2
#input.txt output.txt 100 desc C1 C2

print("###Running phase 2")


#todo -Second phase
output_l=[]
fout= open(output,"w+")
fd_li=[]
#vector<filet>
pri_que=[]
"""self.tup_val=tup_val
    self.fi_no=fi_no"""

#Calculating no of tuples of each file to be loaded in half  the memory

main_in= main/2
no_tup_in=math.floor(main_in/tuples)
print(no_tup_in)
tup_of_file= math.ceil(no_tup_in/no_of_files)
print(tup_of_file)

#list of list to store tup_of_file no of tuples of each file
temp_file_tup=[]
cc=0
flag=0

while cc<no_of_files:
  flag=0
  temp_tup=[]
  tempfd= open(str(cc)+".txt","r")
  fd_li.append(tempfd)

  line1=tempfd.readline()
  #for 1st tuple of each file
  fit= filet(line1,cc)
  pri_que.append(fit)
  
  """for i in range(1,tup_of_file):
    #print(i)
    line1=tempfd.readline()
    if line1:
      temp_tup.append(line1)
    else:
      break
  temp_file_tup.append(temp_tup) """   
  cc+=1
    
  #get n tuples in a list of list
  #get 1st tuple and create its object and save it in pri_que

#print(pri_que)
#print(pri_que[0].tup_val)
#print(temp_file_tup)
buildminheap(pri_que, no_of_files)

#input1.txt output.txt 0.25 asc C1 C2
"""for k in pri_que:
  print(k.tup_val)"""
  
  #print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

print("Sorting.....")
count=no_of_files
while (count!=0):
  #print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
  #print("in")
  fileno=pri_que[0].fi_no
  output_l.append(pri_que[0].tup_val)
  if (no_tup_in==len(output_l)):
    print("Writing on disk")
    for x in output_l:
      fout.write(x)
    output_l=[]

  line1=fd_li[fileno].readline()
  if line1:
        pri_que[0].tup_val=line1
        minheapify(pri_que,0,count)

  else:
    #load more rows from file
    if (os.path.isfile(str(fileno)+".txt")):
        print("remove file")
        fd_li[fileno].close()
        os.remove(str(fileno)+".txt")
        count-=1
        if count==0:
          break
    pri_que[0] = pri_que[count]
    minheapify(pri_que,0,count)
  #if count==0:
  #break  
for x in output_l:
      fout.write(x)
        
fout.close()
#print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
print("### Completed execution")
elapsed_time = time.time() - start_time
print("\nTime elapsed(in seconds): ",elapsed_time)