def load_sites(file_name):
    lines = [ line.rstrip() for line in open(file_name) ]
    lines = [ [ float(x) for x in string.split() ] for string in lines ]
    return lines

def load_data(file_name):
    lines = [ line.rstrip() for line in open(file_name) ]
    lines = prepare_data(lines)
    return lines
    
def prepare_data(lines):
    # find all occurance of > in a list
    indices = [ i for i, x in enumerate(lines) if x == ">" ]

    # split a list into small lists
    lines = [ lines[indices[i]:indices[i+1]] for i in xrange(len(indices)-1) ]

    # remove all ">" and float the result
    [ lst.remove('>') for lst in lines] #
    lines = [ [ [ float(x) for x in string.split() ] 
                           for string in line ] 
                           for line in lines if len(line)>1 ]
    return lines
