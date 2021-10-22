# #!/usr/bin/python

# class Stack(object):

#     def __init__(self,size):
#         self.size=size
#         self.list=[]
#         self.top=-1
#     def push_s(self,ele):
#         if self.isfull():
#             raise Exception("out of range")
#         else:
#             self.list.append(ele)
#             self.top=self.top+1
#     def pop_s(self):
#         if self.isempty():
#             raise Exception("stack is empty")
#         else:
#             self.top=self.top-1
#             return self.list.pop()
#     def isfull(self):
#         return self.top+1==self.size
#     def isempty(self):
#         return self.top==-1



# stack=Stack(20)

# # for i in range(3):
# #     stack.push_s(i)
# #     # stack.pop_s()

# stack.push_s((1,3))
# stack.push_s((3,4))
# stack.list[1]=(5,6)
# print(stack.list)
# # print(stack.isempty())


def test():
    state = [0,1,0,0]
    return state

def tprint(list):
    print(list[1])


tprint(test())
