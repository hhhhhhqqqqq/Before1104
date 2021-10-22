class List(object):
    def __init__(self,listin):

        self.listin=[]

list_1 = List([])
list_2 = List([])
list_1.listin=[1,1,2,3,4,5,8,9]
list_2.listin=[3,4]
list_1.listin.append(7)
list_1.listin.append(78)
print("list_1.listin[0]=",list_1.listin[6])
print("list_2.listin[0]=",list_2.listin[0])


L_min_stnd_1 = 4
L_max_stnd_1 = 31
A_min_stnd_1 = -20
A_max_stnd_1 = 49
B_min_stnd_1 = -36
B_max_stnd_1 = 58

Threshold_1= (L_min_stnd_1,L_max_stnd_1,A_min_stnd_1,A_max_stnd_1,B_min_stnd_1,B_max_stnd_1)
print("original threshold_1", Threshold_1)
assume_array = [2,3,8,9,0,4]

Threshold_1 = tuple(assume_array)
print(type(Threshold_1))
print("afterwards threshold_1",Threshold_1)