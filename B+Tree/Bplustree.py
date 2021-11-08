import bisect
import sys

class btreenode(object):

    def __init__(self):
        self.leaf = True
        self.value = []  # 2
        self.pointer = []  # 3 pointers
        self.counter = 0
        self.leaf_pointer = None
        self.occurence = {}


class BTree(object):

    def __init__(self):
        self.head = btreenode()


    def insert_helper(self, head, value):


        if head.leaf == True:

            if head.counter != 2:

                head.counter += 1
                bisect.insort_left(head.value, value)
                bisect.insort_left(head.pointer, value)
                return head, False

            else:
                # return_node = self.chop(head, value)
                return self.chop(head, value), True


        else:
            i = 0
            ff=0
            while i < len(head.value):
                # for i in range(length):
                if value < head.value[i]:
                    ptr, indicate = self.insert_helper(head.pointer[i], value)
                    ff=1
                    break
                elif i + 1 < len(head.value) and value<head.value[i+1]:
                    ptr, indicate = self.insert_helper(head.pointer[i + 1], value)
                    ff=1
                    break
                i += 1
            if ff == 0:
                ptr, indicate = self.insert_helper(head.pointer[i], value)

            if not indicate:
                return head, False

            else:
                if head.counter < 2:
                    # right
                    value1 = ptr.value[0]

                    head.counter += 1
                    value2 = head.value[0]
                    if value1 > value2:
                        # head.counter += 1
                        head.value.append(value1)
                        head.pointer[1] = ptr.pointer[0]
                        head.pointer.append(ptr.pointer[1])

                        return head , False

                    # left
                    if value1 < value2:
                        head.value.insert(0, value1)
                        ptr.pointer.append(head.pointer[1])
                        head.pointer = ptr.pointer
                        # head.counter += 1
                        return head, False

                else:
                    # head.pointer[1] = ptr.pointer[0]
                    t = ptr.value[0]
                    search_from = head.value

                    if t < search_from[0]:
                        head.pointer[0] = ptr.pointer[1]
                    elif t > search_from[0] and t < search_from[1]:
                        head.pointer[1] = ptr.pointer[1]
                    elif t > search_from[1]:
                        head.pointer[2] = ptr.pointer[0]

                    self.check(head)

                    return_node = self.level_merge(head, ptr)

                    return return_node, True

        return (head, False)

    def check(self, root):
        for i in range(4):
            continue
        return

    def search_repeated_helper(self, head, value):
        ind = head.value.index(value)
        # return True
        if head.leaf == False:
            head = head.pointer[ind + 1]
        while (head.leaf == False):
            head = head.pointer[0]

        if head.leaf == True:
            if value in head.value:
                if value not in head.occurence:
                    head.occurence[value] = 2
                else:
                    head.occurence[value] = head.occurence[value] + 1
        # return True

    def search_repeated(self, head, value):

        if value in head.value:
            self.search_repeated_helper(head, value)

            return True


        elif head.leaf:
            return False

        i = 0
        ff = 0
        while i < len(head.value):

            if value < head.value[i]:
                ff = 1
                return self.search_repeated(head.pointer[i], value)
            elif i + 1 < len(head.value) and value < head.value[i + 1]:
                ff = 1
                return self.search_repeated(head.pointer[i + 1], value)
            i += 1
        if ff == 0:
            return self.search_repeated(head.pointer[i], value)



    def insert(self, value):

        if self.head.counter != 0:
            if self.search_repeated(self.head, value):
                return

        if not self.head.leaf:
            return_node, indicate = self.insert_helper(self.head, value)
            self.head = return_node
        else:
            if self.head.counter > 1:
                return_node = self.chop(self.head, value)
                self.head = return_node
            else:
                bisect.insort_left(self.head.value, value)
                bisect.insort_left(self.head.pointer, value)
                self.head.counter += 1

    def create_node(self, head, leaf, pos, lc, rc):
        tmp = btreenode()

        if not leaf:
            tmp.leaf = False
            tmp.counter = 1
            tmp.value.append(head.value[pos])
            tmp.pointer.append(lc)
            tmp.pointer.append(rc)

        else:
            tmp.value = head.value[pos:]
            tmp.pointer = head.pointer[pos:]
            tmp.counter = 2
            tmp.leaf = True
            for k in range(len(tmp.value)):
                if tmp.value[k] in head.occurence:
                    tmp.occurence[tmp.value[k]] = head.occurence[tmp.value[k]]


        return tmp

    def integrate(self, head, ptr, side):

        if side == "left":
            head.value.insert(0, ptr.value[0])
            head.pointer.insert(0, ptr.pointer[0])
            head.pointer[1] = ptr.pointer[1]
            return head

        if side == "mid":
            head.value.insert(1, ptr.value[0])
            head.pointer[1] = ptr.pointer[0]
            head.pointer.insert(2, ptr.pointer[1])
            return head

        if side == "right":
            bisect.insort_left(head.value, ptr.value[0])
            head.pointer.append(ptr.pointer[1])
            return head

    def create_level_node(self, head, lptr, rptr):

        ptr = btreenode()
        ptr.value.append(head.value[lptr])
        ptr.pointer = head.pointer[lptr:rptr]
        ptr.leaf = False
        ptr.counter = 1
        return ptr

    def level_merge(self, head_a, head_b):

        # left
        if head_b.value[0] < head_a.value[0]:
            merged_root = self.integrate(head_a, head_b, "left")
            return self.chop(merged_root, -1)

        # mid
        elif head_b.value[0] > head_a.value[0] and head_b.value[0] < head_a.value[1]:
            merged_root = self.integrate(head_a, head_b, "mid")
            return self.chop(merged_root, -1)

        # right
        else:
            merged_root = self.integrate(head_a, head_b, "right")
            return self.chop(merged_root, -1)


    def chop(self, head, value):
        if head.leaf:
            bisect.insort_left(head.value, value)
            bisect.insort_left(head.pointer, value)

            sr = self.create_node(head, True, 1, -1, -1)
            sr.leaf_pointer = head.leaf_pointer
            head.leaf_pointer = sr
            return_node = self.create_node(head, False, 1, head, sr)
            templ =[]
            templ.append(head.value[0])
            head.value = templ

            for k in range(len(sr.value)):
                if sr.value[k] in head.occurence:
                    head.occurence.pop(sr.value[k])


            head.counter = 1
            t = []
            t.append(head.pointer[0])
            head.pointer = t
            return return_node
        else:
            rightChild = self.create_level_node(head, 2, 4)
            leftChild = self.create_level_node(head, 0, 2)
            head.pointer = [leftChild, rightChild]
            head.counter = 1
            tempp=[]
            tempp.append(head.value[1])
            head.value = tempp
            return head

    def frequency(self, head, value):

        if value in head.value:
            ind = head.value.index(value)
            if head.leaf == False:
                head = head.pointer[ind + 1]
            while head.leaf == False:
                head = head.pointer[0]
            if head.leaf == True and value in head.value:
                if value in head.occurence:
                    return head.occurence[value]
                else:
                    return 1
        elif head.leaf == True:
            return 0

        i = 0
        ff=0
        while i < len(head.value):
            if value < head.value[i]:

                ff=1
                return self.frequency(head.pointer[i], value)

            elif i + 1 < len(head.value) and value<head.value[i+1]:

                ff=1
                return self.frequency(head.pointer[i+1], value)

            i += 1
        if ff == 0:
            return self.frequency(head.pointer[i], value)




    def range(self, head, x, y):
        count_nodes = 0
        indicate = 0
        while not head.leaf:
            head = head.pointer[0]

        if head.leaf:

            while head != None:

                if indicate == 1:
                    break

                for item in head.value:
                    if item >= x and item <= y:
                        if item in head.occurence:
                            count_nodes += head.occurence[item]
                        else:
                            count_nodes += 1

                    if item >= y:
                        indicate = 1
                        break

                head = head.leaf_pointer

        return count_nodes



    def find(self, head, value):

        if value in head.value:
            return "YES"

        elif head.leaf == True:
            return "NO"

        i = 0
        ff=0
        while i < len(head.value):
            # for i in range(length):
            if value < head.value[i]:
                ff=1
                return self.find(head.pointer[i], value)
            elif i + 1 < len(head.value) and value<head.value[i+1]:
                ff=1
                return self.find(head.pointer[i+1], value)
            i += 1
        if ff == 0:
            return self.find(head.pointer[i], value)

    def caller(self, op, X, Y=0):
        if op == "insert":
            self.insert(X)

        elif op == "find":
            return self.find(self.head, X)

        elif op == "count":
            return self.frequency(self.head, X)
        elif op == "range":
            return self.range(self.head, X, Y)
        elif op == "display":
            self.display1(self.head)
            self.leafs(self.head)
        else:
            print("Invalid Query")

inputFile = sys.argv[1]
outputFile = "output.txt"


obj1 = BTree()
final = ""
fr = open(inputFile,"r")
f = fr.readline()
while f:
    tmp = f.strip().split(" ")
    l=len(tmp)
    if l==2:
        v=obj1.caller(tmp[0].lower(),int(tmp[1]))
    else:
        v= obj1.caller(tmp[0].lower(),int(tmp[1]),int(tmp[2]))
    if v != None:    
        final+=str(v)+"\n"
    f = fr.readline()


fw = open(outputFile, "w")
fw.write(final)
fw.close()

