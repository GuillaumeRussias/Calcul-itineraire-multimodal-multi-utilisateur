
#DEPRECIATED - not used by final programm







import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from base_donnee import exceptions
#import exceptions

class Tree:
    """a structure of tree"""

    def __init__(self,node_value):
        """Constructor: creates a node of a tree with node_value as value and without son """
        self.node=node_value
        self.sons=[]

    def __repr__(self):
            return "Tree_object. self.node="+repr(self.node)+", type="+str(type(self.node))
    def __str__(self):
            return "Tree("+str(self.node)+")"

    def push_son(self,tree_son):
        """ Appends a son to the instance. tree_son must be a tree. Raises typeError if tree_son isn't a tree
        """
        try :
             exceptions.type_detect(tree_son,self)
        except TypeError as Tp:
            print(tree_son,Tp,self)
        else:
            self.sons.append(tree_son)

    def get_son(self,son_index):
        """returns the son at son_index position. if ison_index is out of range, returns None"""
        try:
             out_of_range_detect(self.sons,son_index)
        except IndexError as Ir:
            print(Ir,"returning None")
            return None
        else:
            return self.sons[son_index]

    def deep_research(self,node_value):
        """Search a node in self and all its descendents. If the node is find, put in self.search_results, the list of all ancestors of the node, begining by self and ending by node.
         Warning , potentially hight cost"""
        tuple_results=self.recursive_deep_research(node_value,())
        if tuple_results==():
            raise ValueError("Error in deep_research(self,node) : the node you are looking for is not in this tree")
        return tuple_results

    def recursive_deep_research(self,node_value,work_tuple):
        """only used by deep_research"""
        work_tuple+=(self.node,)
        if self.node==node_value:
            return work_tuple
        elif len(self.sons)==0:
            return ()
        else:
            for son in self.sons:
                result_tuple=son.recursive_deep_research(node_value,work_tuple)
                if (result_tuple!=()):
                    return result_tuple
        return ()

    def display(self,prefix='*',indent=' '):
        """display in console the instance and all of his sons, grand_sons.... """
        total_indent=""
        self.recursive_display(prefix,indent,total_indent)

    def recursive_display(self,prefix,indent,total_indent):
        """recursive function called in diplay"""
        print(prefix+total_indent+str(self.node))
        total_indent=total_indent+indent
        for son in self.sons:
            son.recursive_display(prefix,indent,total_indent)

    def build_from_iterable(self,iterable):
        """build a tree from an iterable object with multiple dimensions: list, dictionnary.
        particulary it can takes as argument the mix list/dictionnary {'a':[{'a1':'xd'},{'a2':'omg'}],'b':'b','c':{'c1':{'c11':'c11','c12':'c12'},'c2':'c2'}} """
        if type(iterable)==type({'dictionary':'type'}):
            for key,value in iterable.items():
                self.push_son(Tree(key))
                self.sons[-1].build_from_iterable(iterable[key])

        elif type(iterable)==type(['list','type']):
            for i,value in enumerate(iterable):
                self.push_son(Tree(i))
                self.sons[-1].build_from_iterable(iterable[i])

"""
 #TEST
iterable={'a':[{'a1':'xd'},{'a2':'oo'}],'b':'b','c':{'c1':{'c11':'c11','c12':'c12'},'c2':'c2'}}
arbre=Tree('bonjour')
arbre.build_from_iterable(iterable)
arbre.display()
arbre.deep_research('c12')
"""
