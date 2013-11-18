"""
Initialization costs O(#a+1 * #b+1)
The matrix load costs O(#a * #b)
The while statement costs O(#a * #y)
O(#a+1 * #b+1) = O(#a*#b + #a + #b + 1)
#a < #a*#b
#b < #a*#b
1 < #a*#b
->
O(#a*#b + #a + #b + 1) < O(3*#a*#b)
Total time compexity using big O properties 
O(#a * #b)
"""
def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)] #O(#a+1 * #b+1)
    # row 0 and column 0 are initialized to 0 already
    # This for statement in total has O(#a * #b)
    for i, x in enumerate(a):  #O(#a)
        for j, y in enumerate(b):  #O(#b)
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1 #O(1)
            else:
                lengths[i+1][j+1] = \
                    max(lengths[i+1][j], lengths[i][j+1]) #O(1)
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b) #O(1)
    """Worst case scenario in each cycle either x or y is modified (not both)
    Time Compexity: O(x*y)"""
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]: #O(1)
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]: #O(1)
            y -= 1
        else:
            assert a[x-1] == b[y-1] #O(1)
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result
