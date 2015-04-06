from random import SystemRandom
import sys

one = '\033[0;36m1\033[0m'
zero = '\033[0;31m0\033[0m'
blank = '\033[0;37m_\033[0m'
while True:
    width = int(raw_input('Enter width of rectangle: ').split()[0])
    if not width:
        continue
    height = int(raw_input('Enter height of rectangle: ').split()[0])
    if not height:
        continue

    def hexArrayPrint(A):
        for i,row in enumerate(A):
            if i%2 == 0:
                print '',
            for val in row:
                print one if val else zero,
                #print '{:1}'.format(val),
            print

    def pathPrint(path,symbol):
        #print path
        for i in range(height):
            if i%2 == 0:
                print '',
            for j in range(width):
                print symbol if (i,j) in path else blank,
            print
        #hexArrayPrint([[(i,j) in path for i in range(dim)] for j in range(dim)])

    def isOpen(percolation,vertex):
        a,b = vertex
        return percolation[a][b] == 1

    def neighbors_of(vertex):
        out = []
        a,b = vertex
        
        shift = (0,1) if a % 2 == 0 else (0,-1)

        for i in (-1,1):
            for j in shift:
                if 0 <= a+i <= height - 1 and 0 <= b+j <= width -1:
                    out.append((a+i,b+j))

        for j in (-1,1):
            if 0 <= b+j <= width -1:
                out.append((a,b+j))
        return out

    r = SystemRandom()

    percolation = [[r.randint(0,1) for i in range(width)] for j in range(height)] 

    hexArrayPrint(percolation)

    def findLeftRightOpen(percolation):
        queue = [[(i,0)] for i in range(height) if isOpen(percolation,(i,0))]
        visited = set()

        while queue:
            path = queue.pop(0)
            vertex = path[-1]

            # Did the path reach the right side?
            if vertex[1] == width - 1 and isOpen(percolation,vertex):
                return path

            elif vertex not in visited and isOpen(percolation,vertex):
                for current_neighbour in neighbors_of(vertex):
                    new_path = list(path)
                    new_path.append(current_neighbour)
                    queue.append(new_path)

                visited.add(vertex)
        return None

    def findTopBottomClosed(percolation):
        queue = [[(0,i)] for i in range(width) if not isOpen(percolation,(0,i))]
        visited = set()

        while queue:
            path = queue.pop(0)
            vertex = path[-1]

            # Did the path reach the bottom?
            if vertex[0] == height - 1 and not isOpen(percolation,vertex):
                return path

            elif vertex not in visited and not isOpen(percolation,vertex):
                for current_neighbour in neighbors_of(vertex):
                    new_path = list(path)
                    new_path.append(current_neighbour)
                    queue.append(new_path)

                visited.add(vertex)
        return None

    path = findLeftRightOpen(percolation)
    if path:
        print "Found an open left-right crossing:"
        pathPrint(path, one)
    else:
        path = findTopBottomClosed(percolation)
        if path:
            print "Found a closed top-bottom crossing:"
            pathPrint(path, zero)
        else:
            print "Uh-oh. Found neither TB nor LR; something went wrong."