# lis=[[0]*4 for i in range (4)]
# print(lis)


# class Node(object):
#     precoordinate=[0,0]

# obj=Node()[]

# obj[0].precoordinate=[1,1]
# print(obj[0].precoordinate)

import collections

m=4
n=4

class Node(object):              #定义所有格子
    def __init__(self,x,y):
        self.passable=0
        self.coordinate=[x,y]
        self.precoordinate=[]
        self.visit=0
        self.colour=0




node=[[0]*n for i in range (m)]  #m*n two dimension-array -1

# print(node)

i=0
j=0

while i<m:
    j=0
    while j<n:
        node[i][j]=Node(i+1,j+1)
        # print(i)
        j=j+1
    i=i+1

# node[2][1].precoordinate=[4,1]

# # node=[[1,2],[2,4]]
# # node[1][1]=Node()
# print(node[3][3].coordinate)
# print(node[3][3].precoordinate)
# print(node[2][3].passable)



s=collections.deque()


s.append(node[2][1])
s.append(node[1][1])
s.append(node[0][0])
# print(s[1].coordinate)

currentnode=s.popleft()

print(currentnode.coordinate)

path_length=len(s)

print(path_length)