## ASSIGNMENT 3

### Running Code-
Enter the input file as 1st argument in the terminal while running the Bplustree.py file.
>python Bplustree.py  input.txt
>Output will be produced in output.txt file.

### Implementation Details-
- Created a btreenode -
leaf = True   - If the node is leaf or not
value = []  # 2  - key list to store node keys
pointer = []  # 3 pointers  - pointer list  to store node pointers
counter = 0  - Keep track of number of keys in node
leaf_pointer = None  - pointer to sibling in case of leaf
occurence = {} - dictionary to store occurence of node at leaf.

- Initially took a head node as leaf and inserted data in it.
- Once it is full, split the node into parent,left child and right child  , changing the type of node to leaf and non leaf accordingly.
- Similarly when a new node comes , we keep on checking from  head of the Bplus tree to find a position to innsert the node till it reaches the leaf.
- For duplicate nodes, we increase the count of the node in leaf.
- For finding the node in bplus tree, we start from head and loop on 1 node comparing with the value to be inserted. And move to the corresponding pointer in the bplus tree. If found return 'YES' and if it reaches leaf and values is not found return 'NO'
- For count, first fnd the node and go to leaf following the right pointer and recursively leftmost pointer till it reaches leaf. From leaf we return the count from dictionary.
- For range between x and y , find x then reach leaf, from there we count the number of nodes in leaf node following the next pointer till on reaches y or just greater than y.
