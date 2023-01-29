# Randomly places mines in a 2d vector
import random

def placement(debug,matrix,mines):
    if debug:
        mines = [(0,0),(1,1),(2,2)]
        for x,y in mines:
            matrix[x][y] = -1
        return mines
    for i in range(12):
        x = random.randint(0,9)
        y = random.randint(0,9)
        mines.append((x,y))
        matrix[x][y] = -1
    return mines


def numbering(matrix, mines):
    for x,y in mines:
        for ax,ay in ((x+1,y),(x-1,y),(x,y+1),(x,y-1),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1)):
            if ax>=0 and ax <=9 and ay>=0 and ay <=9 and matrix[ax][ay] not in mines:
                matrix[ax][ay] +=1
    return matrix

if __name__ == "__main__":
    mines = []
    matrix = [[0 for x in range(10)] for y in range(10)]
    mines = placement(1,matrix,mines)
    matrix = numbering(matrix, mines)
    for x in range(10):
        for y in range(10):
            print(matrix[x][y], end=" ")
        print("\n")