
#DEPRECIATED - not used by final programm

def type_detect(object1,object2):
    """raise TypeError exception if object1 and object2 do not share the same type"""
    if type(object1)!=type(object2):
        raise TypeError(": [typeError] this object does not share the same type as : ")

def out_of_range_detect(list,index):
    n==len(list)
    if index>n or index<0:
        raise IndexError(str(index)+"is not in range. it must be in [[0,"+str(n)+"[[")
