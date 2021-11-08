import sys
import sqlparse 
import csv


def insert_type(k):
    if k in tables.keys():
        from_query_tables.append(k)
    elif k in cols:
        sel_query_cols.append(k)


def check_keyword(i):
    for k in keyword_count.keys():
        if k in i.lower():
            keyword_count[k]+=1
""""print(f"Name of the script      : {sys.argv[0]=}")
print(f"Arguments of the script : {sys.argv[1]=}")"""


def check_aggregate(idd):
  if "(" in idd:
    t=idd[0:-1]
    ll=t.split("(")
    lll=ll[0].lower().strip()
    if lll not in ["max","min","count","sum","average"]:
      print("invalid aggregate function "+lll )
      sys.exit()
    """agg_clause[lll]=ll[1].strip()"""
    agg_clause[ll[1].strip()]=lll
    select_cols.append(ll[1].strip())
  else:
    if idd not in cols:
      print("Column not found "+idd)
      sys.exit()
    select_cols.append(idd)
    

def get_columns(k):
  if ',' in k:
      t=k.split(",")
      for i in t:
          check_aggregate(i.strip())
  else:
      check_aggregate(k.strip())


def get_table(k):
  if "," in k:
      t=k.split(",")
      for i in t:
          if i.strip().lower() in tables.keys():
              from_tabl.append(i.strip().lower())
          else:
              return 0

  else:
      if k.strip().lower() in tables.keys():
          from_tabl.append(k.strip().lower())
      else:
         return 0
  return 1

def load_tables():
  """print (from_tabl)
  print(data)"""
  for i in from_tabl:
    data[i]=[]
    col_count=len(tables[i])
    for k in tables[i]:
      temp={}
      temp[k]=[]
      data[i].append(temp)
    c=0
    l1 = []
    with open("/content/drive/MyDrive/IIITH- Folder/Data Systems/filesds/files/"+i+".csv",'r') as f:
      fileData = []
      reader = csv.reader(f,delimiter=",")
      for row in reader:
          c=0;
          """while c<col_count:"""
          for k in tables[i]:  
            data[i][c][k].append(int(row[c]))
            c+=1
            """fileData.append(row[c])"""
  """print(data)"""

def quotes_removal(s): ## to remove "" or '' from values in table.
    ### return quotes(single or double) free value (integer or variable/column name)
    s = s.strip()
    while len(s) > 1 and (s[0]=='\"' or s[0]=='\'') and s[0]==s[-1]:
        s = s[1:-1] ## copying original str say,"abcxyz" or 'abcxyz' to abcxyz
    return s


def get_r(i):
  if "<=" in i:
    return "<="
  elif ">=" in i:
    return ">="
  elif "=" in i:
    return "="
  elif ">" in i:
    return ">"
  elif "<" in i:
    return "<"

def compare(v1,v2,r):
  if r=='>=' and v1>=v2:
    return True
  elif  r=='<=' and v1<=v2:
    return True
  elif  r=='<' and v1<v2:
    return True
  elif  r=='=' and v1==v2:
    return True
  elif  r=='>' and v1>v2:
    return True  
  else:
    return False  


def get_relationalc(p):
  for i in p:
    p=get_r(i.strip())
    rel_list.append(p)
    s=i.strip().split(p)
    condlist[p]=s


def where_condition(cond):
  t=cond.strip().split(" ",1)
  if "and" in t[1].lower():
    condition["and"]+=1;
    t= t[1].strip().lower().split("and")
    get_relationalc(t)    

  elif "or" in cond.lower():
    condition["or"]+=1;
    t= t[1].strip().lower().split("or")
    get_relationalc(t)
  else: 
    p=[]
    p.append(t[1]) 
    """print(p)  """
    get_relationalc(p)

def check_aggregate_group(idd):
    idd=idd.strip()
    """"if "(" in idd:
    t=idd[0:-1]
    ll=t.split("(")
    print(ll)
    lll=ll[0].lower().strip()
    if lll not in ["max","min","count","sum","average"]:
      print("invalid aggregate function "+lll )
      sys.exit()
    grp_agg_clause[lll]=ll[1].strip()
    clause_grp.append(lll)"""

    """select_cols.append(ll[1].strip())"""
    """else:"""
    if idd not in cols:
      print("Column not found "+idd)
      sys.exit()
    grp_agg_clause["no"]=idd.strip()
    clause_grp.append("no")
    """print(grp_agg_clause)
    print(clause_grp)"""
    """select_cols.append(idd)"""

def load_tables_rows():
  """print (from_tabl)"""
  """print(data1)"""
  for i in from_tabl:
    data1[i]=[]
    data1[i].append(tables[i])
    col_count=len(tables[i])
    """for k in tables[i]:
      temp={}
      temp[k]=[]
      data[i].append(temp)"""
    c=0
    l1 = []
    with open(i+".csv",'r') as f:
      fileData = []
      reader = csv.reader(f,delimiter=",")
      for row in reader:
        c=0
        tempp=[]
        while c<col_count:
          t=quotes_removal(row[c])  
          tempp.append(int(t))
          c=c+1
        data1[i].append(tempp)
  """print(f"from fun {data1}")"""



def join2table(t1,t2):
  first=t1[0]+t2[0]
  tem=[]
  fin=[]
  fin.append(first)
  for i in range(1,len(t1)):
    for j in range(1,len(t2)):
      tem=t1[i]+t2[j]
      fin.append(tem)
  return fin

def group(temp,tt,i1,column):
  out=[]
  out.append(temp[0][i1])
  for k in tt:
    pos=column.index(k)
    agg=agg_clause[k]
    count=0
    sum=0
    average=0
    min=temp[0][pos]
    max=temp[0][pos]
    for p in temp:
      if agg=="min":
        if min>=p[pos]:
          min=p[pos]
          final=min
      elif   agg=="max":
         if max<=p[pos]:  
           max=p[pos]
           final=max
      elif   agg=="count":
        count=count+1
        final=count
      elif   agg=="sum":
        sum=sum+p[pos]
        final=sum 
      else:
        count=count+1
        sum=sum+p[pos]
    if  agg=="average":
      final=sum/count  
    out.append(final)
  return out

def sel_agg(temp,column):
  out=[]
  """print (temp)
  print(column)"""
  for k in column:
    pos=column.index(k)
    """print(pos)"""
    agg=agg_clause[k]
    """print(agg)"""
    count=0
    sum=0
    average=0
    min=temp[0][pos]
    max=temp[0][pos]
    for p in temp:
      if agg=="min":
        if min>=p[pos]:
          min=p[pos]
          final=min
      elif   agg=="max":
         if max<=p[pos]:  
           max=p[pos]
           final=max
      elif   agg=="count":
        count=count+1
        final=count
      elif   agg=="sum":
        sum=sum+p[pos]
        final=sum 
      else:
        count=count+1
        sum=sum+p[pos]
    if  agg=="average":
      final=sum/count
    """print(final)  """
    out.append(final)
  """print (out)"""
  return out

def print_final():
    """print (outp)"""
    """if len(from_tabl)==1:"""

    tables
    agg_clause
    print("Output:")
    for i in range(0,len(outp)):
      if i==0:
        """print(outp[0])"""
        ll=0
        for k in outp[0]:
          aggp=""
          for ke,valu in tables.items():
            if k in valu:
              p=ke
            if len(agg_clause)>0:
              if k in agg_clause:
                aggp=agg_clause[k]
          ll=ll+1
          if ll==len(outp[0]):
            if aggp !="":
              print(f"{p}.{aggp}({k})",end='')
            else:  
              print(f"{p}.{k}",end='')
          else: 
            if aggp !="":
              print(f"{p}.{aggp}({k}),",end='')
            else:  
              print(f"{p}.{k},",end='')
      else:
        ll=0
        for k in outp[i]:
          ll=ll+1
          if ll==len(outp[i]):
              print(f"{k}",end='')
          else:   
            print(f"{k},",end='')
      print()





"""Parse metadata file"""
tables =dict()
"""Data of all the tables"""
"""Tables"""
table=""
cols=[]
"""All the columns of all tables"""
col=[]
"""All the columns of 1 table"""
c=0
with open("metadata.txt",'r') as f:
    tt=f.readlines()
    for line1 in tt:
        line=line1.strip()
        if line=="<begin_table>":
            c=1
            continue
        elif line=="<end_table>":
            tables[table]=col
            col=[]
            continue
        elif c==1:
            table=line.lower()
            c=0
        else:
            col.append(line.lower())
            cols.append(line.lower())
       
        """tables[line]=col"""
        
"""print(tables)
print(cols)"""

""" Parsing sql statement"""
qr=sys.argv[1]
"""qr=input()"""
qr=qr.strip()
"""print(qr[-1])"""
if ";" != qr[-1]:
  print("Semicolon not present")
  sys.exit()

qr=qr[:-1]

"""print(sqlparse.split(qr))"""
parsev= sqlparse.parse(qr)
"""print (parsev)"""
tt=parsev[0]
mytok=[]
"""spliting th query into list"""
l=len(parsev[0].tokens)


sel_query_cols=[]
"""columns in select query"""
from_query_tables=[]
"""tables in from """
keyword_count ={"select":0,"distinct":0,"from":0,"where":0,"order by":0,"group by":0,"*":0}

"""keywords"""
for i in parsev[0].tokens:
    if ' '!=str(i):
        mytok.append(str(i).lower())

    if  isinstance(i, sqlparse.sql.IdentifierList):
        ttt=str(i).lower()
        li_id=ttt.split(",")
        for k in li_id:
          insert_type(k)
    elif isinstance(i, sqlparse.sql.Identifier):
        insert_type(str(i).lower())
    else:
        check_keyword(str(i).lower())

"""
print(mytok)
print(keyword_count)
print(sel_query_cols)
print(from_query_tables)
"""



"""Try to execute a simple query and error handling- select * from table1"""
select_cols=[]
"""main column"""
from_tabl=[]
"""tables"""
agg_clause={}
"""aggregate clauses in select"""
grp_agg_clause={}
"""aggregate clauses in group by"""
clause_grp=[]
"""which clause in group"""
data={}
"""cartisian product columns"""
data1={}
"""whole tables rows """
le=len(mytok)
"""print(le)"""

condition={"and":0,"or":0}
"""conditions in where"""
condlist={}
"""condition as a listed dictionary"""
rel_list=[]
"""relational condition"""
try:
  if le<4:
      print("Incomplete  statement ")
      sys.exit()

  if mytok[0].lower()=="select":
      """print("select")"""
      i=0;

      if mytok[i+1].lower()=="distinct":
          i+=1
          if mytok[i+1].lower()=="*":
              pass
              """print("distinct *")"""
              """check_keyword(mytok[i+1].lower())"""
              
          else:
              """print("distinct id")"""
              get_columns(mytok[i+1])
      elif mytok[i+1].lower()=="*":
          pass
          """print("*")"""
          """print(from_tabl)"""
          """check_keyword(mytok[i+1].lower())"""
      else:
          """print("Id")"""
          get_columns(mytok[i+1])
    
      if mytok[i+2].lower()=="from":
          i=i+2
          """print("from")"""
          if i>=l:
            
            print("Incomplete  statement ")
            sys.exit()
          """val=get_tables(mytok[i+1].lower())"""
          if i+1>=le:
                print("Incomplete  statement ")
                sys.exit()
          val=get_table(mytok[i+1])
    
          if val:
              i=i+2
              """print("table"+"i="+str(i))"""
              """load_tables()"""
              load_tables_rows()
              """print(data1)
              print(keyword_count["*"])"""
              if keyword_count["*"]==1:
                for t in from_tabl:
                  for z in data1[t][0]:
                    select_cols.append(z)
                """print("list of columns if *")
                print(select_cols)"""

          else:
              print("Table missing/not present")
              sys.exit()
      else:
          print("From statement missing")
          sys.exit()

      if i<le and "where" in mytok[i].lower():
          """split_where(mytok[i].lower())"""
          """print("where")"""
          where_condition(mytok[i])
          i=i+1

      if i+1<le and mytok[i].lower()=="group by":
          i=i+1
          """print("group")"""
          """split_group_by(mytok[i].lower())"""
          check_aggregate_group(mytok[i])
          i=i+1
          

      if i+1<le and mytok[i].lower()=="order by":
          i=i+1
          """print("order by")"""
          ordcol=mytok[i].split();
          order_ad=ordcol[1].strip()
          if "max" in ordcol[0] or "min" in ordcol[0] or "sum" in ordcol[0] or "count" in ordcol[0] or "average" in ordcol[0]:
            y=ordcol[0][:-1]
            x=y.split('(')
            ordcol[0]=x[1].strip()

          if ordcol[0] not in select_cols:
            print("Column not in select clause/missing column")
            sys.exit()
          order_by=ordcol[0].strip()
          
  else:
      print("Select statement missing")
      sys.exit()


  """print(select_cols)
  print("select agg")
  print(agg_clause)

  print(from_tabl)

  print("where conditions")
  print(condlist)
  print("and or")
  print(condition)
  print("where conditions relation")
  print(rel_list)
  print("agregate clause")
  print(grp_agg_clause)
  print("agregate clause")
  print(clause_grp)"""
  final_col_list=select_cols
  outp=[]
  """ Doing the join of tables and applying the where filter """
  """if len(from_tabl)==1:
    outp=data1[from_tabl[0]]
    if keyword_count["where"]==1:
      print("where present")
    else:
      outp=data1[from_tabl[0]]
      data1={}
      print(f"where {outp}")"""

  l=len(from_tabl)
  temp=data1[from_tabl[0]]
  """print(f"table1:{len(temp)}")"""
  for i in range(1,l):
    """print(f"table1:{len(data1[from_tabl[i]])}")"""
    temp=join2table(temp,data1[from_tabl[i]])
  outp=temp  
  if keyword_count["where"]==1:
      l=len(outp)
      a1=condlist[rel_list[0]][0].strip()
      i1=outp[0].index(a1)
      v1=condlist[rel_list[0]][1].strip()
      t=-1
      if v1 not in outp[0]:
        v1=int(v1)
      else:
        t=outp[0].index(v1)

      if len(rel_list)>1:
        a2=condlist[rel_list[1]][0].strip()
        i2=outp[0].index(a2)
        v2=condlist[rel_list[1]][1].strip()
        tt=-1
        if v2 not in outp[0]:
          v2=int(v2)
        else:
          tt=outp[0].index(v2)
      """for i in range(1,l):"""
      i=1;
      while i<l:
        v11=outp[i][i1]
        if t== -1:
          b1=compare (v11,v1,rel_list[0])
        else:
          v12=outp[i][t]
          b1=compare (v11,v12,rel_list[0])

        if len(rel_list)>1:
          v21=outp[i][i2]
          if tt== -1:
            b2=compare (v21,v2,rel_list[1])
          else:
            v22=outp[i][tt]
            b2=compare (v21,v22,rel_list[1])
          if condition["and"]==1:
            fi= b1 and b2
          elif condition["or"]==1:
            fi= b1 or b2
        else:
          fi=b1
        if not fi :
          del outp[i]
          l=l-1
          i=i-1
        i+=1



          

  """print(len(outp))
  print(outp)

  print_final()
  print(len(outp))
  """

  """ Applying group by and aggregate function"""
  """if len(from_tabl)==1:"""

  if keyword_count["group by"]:
      i1=outp[0].index(grp_agg_clause[clause_grp[0]])
      tt=select_cols[1:]
      li=[]
      if select_cols[0].strip() != grp_agg_clause[clause_grp[0]].strip():
        print("First column should be same as group by column")
        sys.exit()

      for k in tt:
        li.append(agg_clause[k])
      l=len(outp)
      i=1;
      fin=[]
      fin.append(select_cols)
      temp=[]
      poss=[]
      while i<l:
        count=0
        for li in poss:
          del outp[li-count]
          l=l-1
          count=count+1
          if l==1:
            break
        if i>=l:
          break    
        temp=[]
        poss=[]
        v=outp[i][i1]
        temp.append(outp[i])
        del outp[i]
        l=l-1
        j=i
        while j<l:
          if v==outp[j][i1]:
            temp.append(outp[j])
            """del outp[j]"""
            """l=l-1"""
            poss.append(j)
          j=j+1 
        fin.append(group(temp,tt,i1,outp[0]))
      outp=fin

  """outp=outp[from_tabl[0]]"""

  """select columns mentioned"""

  if keyword_count["*"] ==0:
      pos=[]
      for i in final_col_list:
        t=outp[0]
        pos.append(t.index(i))

      temp=[]
      temp.append(final_col_list)
      for i in range(1,len(outp)):
          tt=[]
          for j in pos:
            tt.append(outp[i][j])
          temp.append(tt)
      outp=temp

      ttt=[]
      ttt.append(final_col_list)
      td=outp[1:]  
      pp=[]
      if keyword_count["group by"] !=1 and len(final_col_list)==len(agg_clause):
        pp=sel_agg(td,final_col_list)
        ttt.append(pp)
        outp=ttt

      elif keyword_count["group by"] !=1 and len(agg_clause)>0  :
        sys.exit()

      """"else:
        temp=[]
        temp.append(final_col_list)
        for i in range(1,len(outp)):
          tt=[]
          for j in pos:
            tt.append(outp[i][j])
          temp.append(tt)
        outp=temp"""      


  flag=0
  if keyword_count["*"] ==1:
    if len(agg_clause)==1 and "*" in agg_clause.keys() and agg_clause["*"]=="count" :
      print(f"count(*)")
      print(len(outp[1:]))
      flag=1 

  if flag == 0:
      """Order by and distinct at end"""
      if keyword_count["distinct"] ==1:
        ll=len(outp)
        i=1
        while i<ll and i>0:
          j=i+1
          while j<ll and j>1:
            if i<ll and j<ll and outp[i]==outp[j]:
              del outp[j]
              ll=ll-1
            else:
              j=j+1    
          i=i+1  
        """print(outp)"""

      if  keyword_count["order by"] ==1:
          tempo=[]
          posi=final_col_list.index(order_by)
          for v in range(1,len(outp)):
            for w in range(v+1,len(outp)):
              if  outp[v][posi] > outp[w][posi]:
                tempo=outp[v]
                outp[v]=outp[w]
                outp[w]=tempo 
          if order_ad=="desc":
            tempp=outp[1:]
            rev=tempp[::-1]
            outp=rev;
            outp.insert(0,final_col_list)      


      print_final()


except SystemExit:
    print("Error")

except:
    print("Invalid Query")







