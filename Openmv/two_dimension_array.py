#定义类中的二维数组
class Dimension(object):
    row_number=4
    column_number=4


class CoordinInfor(object):

    def __init__(self,lis,m,n):
        # self.row=m
        # self.column=n
        self.lis=[[0]*n for i in range (m)]

coordininfor=CoordinInfor([],Dimension.row_number,Dimension.column_number)
coordininfor.lis[1][1]=9

print(coordininfor.lis)

# class CoordinInfor(object):

#     def _init_(self,lis,m,n):
#         self.row=m
#         self.column=n
#         self.lis=[[0]*2 for i in range (3)]

# coordininfor=CoordinInfor([[]],Dimension.row_number,Dimension.column_number)





# testlist=[[0]*2 for i in range (3)]
# print(testlist)



# class List(object):
#     def __init__(self,listin):
#         self.listin=[4, 31, -20, 49, -36, 58]

# list_black = List([])

# print(list_black.listin)