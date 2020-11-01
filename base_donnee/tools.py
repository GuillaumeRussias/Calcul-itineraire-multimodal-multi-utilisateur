def search_last_int_index_iterable(iterable):
    last=None
    for index in range(len(iterable)):
        if type(iterable[index])==type(1):
            last=index
    return last

def inclusion_test(list1,list2):
    for l in list1:
        if l not in list2:
            return False
    return True

def garder_plus_grands_elements_sens_inclusion(list_bidim):
    n=len(list_bidim)
    s=0
    i=0
    while i<n:
        for j in range(n-s):
            if i-s!=j and inclusion_test(list_bidim[i-s],list_bidim[j]):
                del list_bidim[i-s]
                s+=1
                break
        i+=1

#TEST:
"""
list_bidim=[[0,2,3,1],[1,0],[0,2,3,1],[0,1,2],[4,5],[0,4,5,6,7]]
garder_plus_grands_elements_sens_inclusion(list_bidim)
print(list_bidim)
"""
