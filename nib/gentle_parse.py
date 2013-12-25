#class GentleParse(list):
class GentleParse():

    __comments = []
    __comments_line_idx = []
    __terminates = []
    __data = []
    __data_line_idx = []

    def __init__(self, strings):
        self.__strings = strings

    def parse(self, expr):
        for i, string in enumerate(self.__strings):
            string_ = string.split()
            line = []
            try:
                for j, expr_type in enumerate(expr):
                    if expr_type == "float":
                        line.append(float(string_[j]))
                    elif expr_type == "int":
                        line.append(int(string_[j]))
                    elif expr_type == "str":
                        line.append(str(string_[j]))
            except ValueError:
                self.__comments.append(string)
                self.__comments_line_idx.append(i)
                continue

            self.__data.append(line)
            self.__data_line_idx.append(i)
            if len(line)<len(string_):
                self.__terminates.append(string_[len(line):])
            else:
                self.__terminates.append([])

    def unparse(self):
        strings = []
        idxs = self.__comments_line_idx + self.__data_line_idx
        idxs.sort()
        for i in idxs:
            if i in self.__comments_line_idx:
                comment_idx = self.__comments_line_idx.index(i)
                strings.append(self.__comments[comment_idx])
            else:
                data_idx = self.__data_line_idx.index(i)
                string = self.__data[data_idx]+self.__terminates[data_idx]
                strings.append(" ".join([ str(item) for item in string ]))
        return strings

    def aslist(self):
        return self.__data

    def __len__(self):
        """Called to implement the built-in function len(). Should 
        return the length of the object, an integer >= 0. Also, an 
        object that doesn't define a __nonzero__() method and whose 
        __len__() method returns zero is considered to be false in a 
        Boolean context.""" 
        return len(self.__data)

    def __getitem__(self,key):
        """Called to implement evaluation of self[key]. For sequence 
        types, the accepted keys should be integers and slice objects. 
        Note that the special interpretation of negative indexes (if 
        the class wishes to emulate a sequence type) is up to the 
        __getitem__() method. If key is of an inappropriate type, 
        TypeError may be raised; if of a value outside the set of 
        indexes for the sequence (after any special interpretation of 
        negative values), IndexError should be raised. For mapping 
        types, if key is missing (not in the container), KeyError 
        should be raised. Note: for loops expect that an IndexError 
        will be raised for illegal indexes to allow proper detection of 
        the end of the sequence.""" 
        #if not key:
        #    raise KeyError
        if not (key < len(self.__data)):
            raise IndexError
        return self.__data[key]

    def __setitem__(self,key,value):
        """Called to implement assignment to self[key]. Same note as 
        for __getitem__(). This should only be implemented for mappings 
        if the objects support changes to the values for keys, or if 
        new keys can be added, or for sequences if elements can be 
        replaced. The same exceptions should be raised for improper key 
        values as for the __getitem__() method.""" 
        if not key:
            raise KeyError
        if not (key < len(self.__data)):
            raise IndexError
        self.__data[key] == value
 
    def __delitem__(self,key):
        """Called to implement deletion of self[key]. Same note as for 
        __getitem__(). This should only be implemented for mappings if 
        the objects support removal of keys, or for sequences if 
        elements can be removed from the sequence. The same exceptions 
        should be raised for improper key values as for the __getitem__
        () method."""
        pass 
 
    # __iter__ is not strictly required, it's only needed to implement
    # efficient iteration.
    def __iter__(self):
        """This method is called when an iterator is required for a 
        container. This method should return a new iterator object that 
        can iterate over all the objects in the container. For 
        mappings, it should iterate over the keys of the container, and 
        should also be made available as the method iterkeys()."""
        for item in self.__data:
            yield item
 
    # __contains__ isn't strictly required either, it's only needed to
    # implement the `in` operator efficiently.
    def __contains__(self,item):
        """Called to implement membership test operators. Should return 
        true if item is in self, false otherwise. For mapping objects, 
        this should consider the keys of the mapping rather than the 
        values or the key-item pairs."""
        pass
 
    # Mutable sequences only, provide the Python list methods.
    def append(self,item):
        self.__data.append(item)

    def count(self):
        pass
    def index(self,item):
        pass
    def extend(self,other):
        pass
    def insert(self,item):
        pass
    def pop(self):
        pass
    def remove(self,item):
        pass
    def reverse(self):
        pass
    def sort(self):
        pass
 
    # If you want to support addition and multiplication provide the
    # methods __add__(), __radd__(), __iadd__(), __mul__(), __rmul__() 
    # and __imul__().
