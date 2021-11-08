import math
import sys
from functools import cmp_to_key
import time
import os

#####################################################
class filet:
    def __init__(self, tup_val, fi_no, yval):
        self.tup_val = tup_val
        self.fi_no = fi_no
        self.yval = yval


def get_initial(r_file, M):
    num_linesr = sum(1 for line in open(r_file))
    blocks_in_file = num_linesr / 100
    no_of_sublist = math.ceil(blocks_in_file / M)
    print(no_of_sublist)
    return num_linesr, no_of_sublist


def compare(t11, t22):
    t1 = t11.strip().split(' ')
    t2 = t22.strip().split(' ')
    if t1[1] <= t2[1]:
        return -1
    else:
        return 1


def compare1(t11, t22):
    t1 = t11.strip().split(' ')
    t2 = t22.strip().split(' ')
    if t1[0] <= t2[0]:
        return -1
    else:
        return 1


def create_sublist(file_name, no_of_sublist, memory_blocks, typ):
    filenames = []
    no_tup_in_sublist = memory_blocks * 100
    file1 = open(file_name, "r")
    for i in range(no_of_sublist):
        tupc = []
        k = no_tup_in_sublist
        while (k):
            # tup=[]
            line1 = file1.readline()
            if not line1:
                break
            # tup=line1.split("  ")
            tupc.append(line1)
            k -= 1

        # if(k==tup_in_file):
        #   break
        # count_file+=1
        # #sort(tupc,order,cols)
        # #print(type(tupc[0]))
        print("Sorting #" + str(i) + "sublist")
        if typ == 0:
            tupc = sorted(tupc, key=cmp_to_key(compare))
        else:
            tupc = sorted(tupc, key=cmp_to_key(compare1))
        f_name = file_name + str(i) + ".txt"
        filenames.append(f_name)
        # filenames.append(f_name)
        fw = open(f_name, "w+")
        print("Writing to sublist #" + f_name)
        for k in tupc:
            fw.write(k)
        fw.close()
    file1.close()
    return filenames


def compare_heap(t11, t22):
    if t11 <= t22:
        return -1
    else:
        return 1


def buildminheap(a, n):
    for j in range(int(n / 2), -1, -1):
        minheapify(a, j, n)


def minheapify(a, i, n):
    smallest = i
    left = (2 * i + 1)
    right = ((2 * i) + 2)
    if (left >= n):
        return
    else:
        if (left < n and compare_heap(a[left].yval, a[i].yval) == -1):
            smallest = left
        else:
            smallest = i
        if (right < n and compare_heap(a[right].yval, a[smallest].yval) == -1):
            smallest = right
        if (smallest != i):
            temp = a[i]
            a[i] = a[smallest]
            a[smallest] = temp
            minheapify(a, smallest, n)


def create_queue(r, count_in_block, typ, countr):
    fd_r = []
    tuplelist = []
    for i in range(len(r)):
        file1 = open(r[i], "r")
        fd_r.append(file1)
        for j in range(count_in_block):
            line1 = file1.readline()
            if not line1:
                break
            countr[i] += 1
            # tup=line1.split("  ")
            t1 = line1.strip().split(' ')
            if typ == 0:
                yval = t1[1]
            else:
                yval = t1[0]
            fit = filet(line1, i, yval)
            tuplelist.append(fit)
    return tuplelist, fd_r


def insert_pque(list1_s, fd_s, pos, counts, typ):
    fd = fd_s[pos]
    for j in range(100):
        line1 = fd.readline()
        if not line1:
            break
        counts[pos] += 1
        t1 = line1.strip().split(' ')
        if typ == 0:
            yval = t1[1]
        else:
            yval = t1[0]
        fit = filet(line1, pos, yval)
        list1_s.append(fit)
        # temp1=list1_s[0]
        # list1_s[0]=list1_s[len(list1_s)-1]
        # list1_s[len(list1_s) - 1]=temp1

        # list1_s.insert(0,fit)
        # minheapify(list1_s, 0,len(list1_s))
    buildminheap(list1_s, len(list1_s))


def get_s_file(list1_s, yvalue, counts, fd_s, typ):
    t_name = "temp" + ".txt"
    f = open(t_name, "w+")
    tups = list1_s[0].tup_val
    f.write(tups)
    prev = list1_s[0].yval
    pos = list1_s[0].fi_no
    counts[pos] -= 1
    # ------------ added
    list1_s[0] = list1_s[len(list1_s) - 1]
    # list1_s = list1_s[:-1]
    del list1_s[-1]
    # -------------------
    # list1_s.pop(0)
    minheapify(list1_s, 0, len(list1_s))
    if counts[pos] == 0:
        insert_pque(list1_s, fd_s, pos, counts, typ)

    while (len(list1_s) > 0 and prev == list1_s[0].yval):
        tups = list1_s[0].tup_val
        f.write(tups)

        prev = list1_s[0].yval
        pos = list1_s[0].fi_no
        counts[pos] -= 1
        # list1_s.pop(0)
        # ------------ added
        list1_s[0] = list1_s[len(list1_s) - 1]
        # list1_s = list1_s[:-1]
        del list1_s[-1]
        # -------------------
        minheapify(list1_s, 0, len(list1_s))
        if counts[pos] == 0:
            # counts[pos]=10
            # insert a new block to the priority queue
            insert_pque(list1_s, fd_s, pos, counts, typ)

    f.close()
    return t_name


def change_r_queue(list1_r, yvalue, countr, fd_r, file_temp, fw):
    tupr = list1_r[0].tup_val
    prev = list1_r[0].yval
    pos = list1_r[0].fi_no
    countr[pos] -= 1
    # list1_r.pop(0)
    # ------------ added
    list1_r[0] = list1_r[len(list1_r) - 1]
    # list1_r = list1_r[:-1]
    del list1_r[-1]
    # -------------------
    minheapify(list1_r, 0, len(list1_r))
    file1 = open(file_temp, "r")
    # changed
    col = tupr.split(" ")[0]
    while (True):
        line1 = file1.readline()
        # fin=tupr+line1 #changed

        if not line1:
            break
        fin = col + " " + line1
        fw.write(fin)
    file1.close()
    if countr[pos] == 0:
        # counts[pos]=10
        # insert a new block to the priority queue
        insert_pque(list1_r, fd_r, pos, countr, 0)

    while (len(list1_r) > 0 and prev == list1_r[0].yval):

        tupr = list1_r[0].tup_val
        yr=tupr.split(" ")[0]
        prev = list1_r[0].yval
        pos = list1_r[0].fi_no
        countr[pos] -= 1
        # list1_r.pop(0)
        # ------------ added
        list1_r[0] = list1_r[len(list1_r) - 1]
        # list1_r = list1_r[:-1]
        del list1_r[-1]
        # -------------------
        minheapify(list1_r, 0, len(list1_r))
        file1 = open(file_temp, "r")
        while (True):
            line1 = file1.readline()
            if not line1:
                break
            fin = yr + " " + line1
            fw.write(fin)
        file1.close()

        if countr[pos] == 0:
            # counts[pos]=10
            # insert a new block to the priority queue
            insert_pque(list1_r, fd_r, pos, countr, 0)


def delete_notmatch(list1_r, yvalue, countr, fd_r, typ):
    # R = 5  S = (1, 2, 3, 4) 5 ya 6
    tupr = list1_r[0].tup_val
    prev = list1_r[0].yval
    pos = list1_r[0].fi_no
    countr[pos] -= 1
    # list1_r.pop(0)
    # ------------ added
    list1_r[0] = list1_r[len(list1_r) - 1]
    # list1_r = list1_r[:-1]
    del list1_r[-1]
    # -------------------
    minheapify(list1_r, 0, len(list1_r))
    if countr[pos] == 0:
        insert_pque(list1_r, fd_r, pos, countr, typ)

    while (len(list1_r) > 0 and prev == list1_r[0].yval):

        tupr = list1_r[0].tup_val
        prev = list1_r[0].yval
        pos = list1_r[0].fi_no
        countr[pos] -= 1
        # list1_r.pop(0)
        # ------------ added
        list1_r[0] = list1_r[len(list1_r) - 1]
        # list1_r = list1_r[:-1]
        del list1_r[-1]
        # -------------------
        minheapify(list1_r, 0, len(list1_r))


        if countr[pos] == 0:
            # counts[pos]=10
            # insert a new block to the priority queue
            insert_pque(list1_r, fd_r, pos, countr, typ)


def sort_merge_phase2(r, s, M, count_in_block):
    countr = []
    counts = []
    for i in range(len(r)):
        countr.append(0)

    for i in range(len(s)):
        counts.append(0)

    list1_r, fd_r = create_queue(r, count_in_block, 0, countr)
    list1_s, fd_s = create_queue(s, count_in_block, 1, counts)

    buildminheap(list1_r, len(list1_r))
    buildminheap(list1_s, len(list1_s))

    print(len(list1_r))
    print(len(list1_s))

    flag = 0

    fout_name = initials_out
    # filenames.append(f_name)
    fw = open(fout_name, "w+")

    while (len(list1_r) > 0 and len(list1_s) > 0):
        # sublist_no=list1_r[0].fi_no
        # tupr=list1_r[0].tup_val
        # flag=0
        if list1_r[0].yval == list1_s[0].yval:
            # flag=1
            file_temp = get_s_file(list1_s, list1_s[0].yval, counts, fd_s, 1)
            change_r_queue(list1_r, list1_r[0].yval, countr, fd_r, file_temp, fw)

        elif list1_r[0].yval < list1_s[0].yval:
            delete_notmatch(list1_r, list1_r[0].yval, countr, fd_r, 0)

        else:
            delete_notmatch(list1_s, list1_s[0].yval, counts, fd_s, 1)

    for x in fd_r:
        x.close()

    for x in fd_s:
        x.close()

    fw.close()

###############################################################
def create_hash_buckets(r_file,memory_blocks,typ):
    fileread = open(r_file, "r")
    count_rr=[]
    fd_rr=[]

    for i in range(capacity):
        if typ==0:
            file1=open(r_file+str(i)+"r.txt", "w+")
        else:
            file1 = open(r_file+str(i) + "s.txt", "w+")

        fd_rr.append(file1)
        count_rr.append(0)

    while( True):
        line1=fileread.readline()
        if line1:
            if typ==0:
                keyval = line1.split(" ")[1]
                keyval=keyval[:-1]
            else:
                keyval = line1.split(" ")[0]

            tt=gethash_val(keyval)
            fd_rr[tt].write(line1)
            count_rr[tt]+=1
        else:
            break
    for i in range(capacity):
        fd_rr[i].close()
        if typ==0:
            filee = open(r_file+str(i) + "r.txt", "r+")
        else:
            filee = open(r_file+str(i) + "s.txt", "r+")

        fd_rr[i]=filee

    return fd_rr,count_rr




def gethash_val(keyval):
        a = 1
        h_val = 0

        for i in range(len(keyval)):
            h_val = h_val + (a * ord(keyval[i]))
            a = a * div
            h_val = h_val % capacity

        return h_val

###############################################################
get_input=sys.argv[1]

input_list=get_input.split(" ")
number_of_args=len(input_list)

if number_of_args !=4:
    print("Invalid arguments")
    sys.exit()
# r_file="/content/drive/MyDrive/IIITH- Folder/Data Systems/inputR"
# s_file="/content/drive/MyDrive/IIITH- Folder/Data Systems/inputS"
# r_file = "inputR"
# s_file = "inputS"
# # hash/sort
# type_join = "sort"
# memory_blocks = 10

r_file = input_list[0]
s_file = input_list[1]
# # hash/sort
type_join = input_list[2]
memory_blocks = int(input_list[3])
count_in_block = 100

if "/" in r_file and s_file:
    r1=r_file.split("/")[-1]
    s1=s_file.split("/")[-1]


initials_out=r1+"_"+s1+"_"+"join.txt"

if type_join == "sort":
    print("Sort Merge Join")
    start_time = time.time()
    num_tuples_r, sublist_r = get_initial(r_file, memory_blocks)
    num_tuples_s, sublist_s = get_initial(s_file, memory_blocks)

    file_name_r = create_sublist(r_file, sublist_r, memory_blocks, 0)
    file_name_s = create_sublist(s_file, sublist_s, memory_blocks, 1)

    count_r = len(file_name_r)
    count_s = len(file_name_s)

    br_bs = count_r * memory_blocks + count_s * memory_blocks

    print(file_name_r)
    print(file_name_s)

    if br_bs > memory_blocks * memory_blocks:
        print("memory exceeded")

    else:
        sort_merge_phase2(file_name_r, file_name_s, memory_blocks, count_in_block)
    print(f"Sort Merge join completed")
    print("###Completed Execution")
    elapsed_time = time.time() - start_time
    print("\nTime elapsed(in seconds): ", elapsed_time)
    os.remove("temp.txt")

elif type_join == "hash":
    start_time = time.time()
    print("Hash Join")
    div = 31
    capacity = 10
    fd_r, count_r = create_hash_buckets(r_file, count_in_block, 0)
    fd_s, count_s = create_hash_buckets(s_file, count_in_block, 1)

    print(f"Files of hash for R {count_r}")
    print(f"Files of hash for S {count_s}")
    flag = 0
    for i in range(len(fd_r)):
        countv = min(count_r[i], count_s[i])
        if (countv / 100 > memory_blocks):
            print("Memory limit exceeded")
            flag = 1
            break

    fout_name = initials_out
    # filenames.append(f_name)
    fw = open(fout_name, "w+")

    if (flag == 0):
        for i in range(capacity):
            new = dict()
            if (count_r[i] <= count_s[i] and count_r[i] != 0):
                # print("check")
                while (True):
                    line1 = fd_r[i].readline()
                    if not line1:
                        break
                    y = line1[:-1].split(" ")[1]

                    if y not in new:
                        new[y] = []
                        new[y].append(line1[:-1])

                    else:
                        new[y].append(line1[:-1])
                    # new[y]=new[y].append(line1)
                #print(new)
                while (True):
                    line2 = fd_s[i].readline()
                    if not line2:
                        break
                    y1 = line2.split(" ")[0]
                    if y1 in new:
                        for x in new[y1]:
                            fin = x + " " + line2[:-1].split(" ")[1] + "\n"
                            # print(fin)
                            fw.write(fin)
            elif (count_r[i] > count_s[i] and count_s[i] != 0):
                # print("check")
                while (True):
                    line1 = fd_s[i].readline()
                    # print(line1)
                    if not line1:
                        break
                    y = line1.split(" ")[0]
                    if y not in new:
                        new[y] = []
                        new[y].append(line1[:-1])
                    else:
                        new[y].append(line1[:-1])
                #print(new)
                while (True):
                    line2 = fd_r[i].readline()
                    # print(line2)
                    if not line2:
                        break
                    y1 = line2[:-1].split(" ")[1].strip()
                    if y1 in new:
                        # print (y1)
                        for x in new[y1]:
                            # fin = x + " " + line2.split(" ")[1]
                            fin = line2.split(" ")[0] + " " + x + "\n"
                            # print(fin)
                            fw.write(fin)
            fd_r[i].close()
            fd_s[i].close()

        fw.close()
        print(f"Hash join completed")
        print("###Completed Execution")
        elapsed_time = time.time() - start_time
        print("\nTime elapsed(in seconds): ", elapsed_time)

