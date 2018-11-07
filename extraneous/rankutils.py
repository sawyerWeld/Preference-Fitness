# Various Utilities

def listtostring(rank, delim=''):
    li = list(rank)
    string = delim.join(map(str,li))
    return string
    