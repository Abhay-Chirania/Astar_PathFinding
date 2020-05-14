import numpy as np
import math
import random
import cv2
class Node(object):
    def __init__(self,i,j,isWall):
        self.i=i
        self.j=j
        self.g=0
        self.h=0
        self.f=0
        self.previous=None
        self.isWall=isWall
    def neighbour(self,grid,width,heigt):
        neighbour=[]
        i=self.i
        j=self.j
        if i>0:
            neighbour.append(grid[i-1][j])
        if i<height-1:
            neighbour.append(grid[i+1][j])
        if j>0:
            neighbour.append(grid[i][j-1])
        if j<width-1:
            neighbour.append(grid[i][j+1])
        if i>0 and j>0:
            neighbour.append(grid[i-1][j-1])
        if i<height-1 and j<width-1:
            neighbour.append(grid[i+1][j+1])
        if i>0 and j<width-1:
            neighbour.append(grid[i-1][j+1])
        if i<height-1 and j>0:
             neighbour.append(grid[i+1][j-1])
        return neighbour

def dist(c,d):
    return math.sqrt(((c.i-d.i)**2)+((c.j-d.j)**2))
def heuristic(c,d):
    xD=abs(c.i-d.i)
    yD=abs(c.j-d.j)
    rem=abs(xD-yD)
    return (1.414*min(xD,yD))+rem
def redraw(current):
    path=[]
    temp=current
    path.append(current)
    while(temp.previous!=None):
        path.append(temp.previous)
        temp=temp.previous
    return path



def printAndmakeImg(obstacles,height,width,solved=False,start=(0,0),end=(0,0),path=[]):
    img=np.zeros((height,width,3),np.uint8)
    for i in range(height):
        for j in range(width):
            if not solved:
                if (i,j)==start or (i,j)==end:
                #    print('*',end='  ')
                    img[i,j]=[0,255,0]
                elif (i,j) in obstacles:
                     pass
                #    print('|',end='  ')
                else:
                #    print('o',end='  ')
                    img[i,j]=[255,255,255]
            else:
                if (i,j) in path:
                #   print("*",end='  ')
                    img[i,j]=[0,255,0]
                elif (i,j) in obstacles:
                    pass
                #    print('|',end='  ')
                else:
                #   print('o',end='  ')
                    img[i,j]=[255,255,255]

        #print()
        reSizedimg=cv2.resize(img,(400,400),interpolation=cv2.INTER_NEAREST)
    cv2.imshow('{}.png'.format('Solved' if solved else 'Unsolved' ),reSizedimg)



                                        ###Main Code###





width=50                                                            #width of grid
height=50                                                           #height of grid
obstacleChance=0.3                                                  #chance of obstacle to generate
startPos=(random.randint(0,height-1),random.randint(0,width-1))     #start position
endPos=(random.randint(0,height-1),random.randint(0,width-1))       #end position
#startPos=(0,0)
#endPos=(height-1,width-1)


grid=[['' for j in range(width)] for i in range(height)]
##for image
imgArr=[['' for j in range(width)] for i in range(height)]
obstacles=[]
for i in range(height):
    for j in range(width):
        isWall=True if random.random()<obstacleChance else False
        if isWall and (i,j)!=startPos and (i,j)!=endPos:
            obstacles.append((i,j))
        grid[i][j]=Node(i,j,isWall)
printAndmakeImg(obstacles,height,width,start=startPos,end=endPos)
start=grid[startPos[0]][startPos[1]]
end=grid[endPos[0]][endPos[1]]
print(start,end)
start.isWall=False
end.isWall=False
openSet=[]
closedSet=[]

openSet.append(start)
start.previous=None
pathpoints=[]
while len(openSet)>0:
    bestI=0
    for i in range(len(openSet)):
        if openSet[i].f<openSet[bestI].f:
            bestI=i
    current=openSet[bestI]
    if current==end:
        pathpoints=redraw(current)
        break
    openSet.remove(current)
    closedSet.append(current)
    neighbour=current.neighbour(grid,width,height)
    for i in neighbour:
        if i in closedSet or i.isWall:
            continue
        tCost=current.g+dist(current,i)
        if i not in openSet:
            openSet.append(i)
        elif tCost>=i.g:
            continue
        i.previous=current
        i.g=tCost
        i.f=i.g+heuristic(i,end)


if len(pathpoints) ==0:
    print("Cannot find path")
else:
    print("\n\nFOUND THE PATH")
    path=[]
    for i in reversed(range(len(pathpoints))):
        path.append((pathpoints[i].i,pathpoints[i].j))
    print()
    printAndmakeImg(obstacles,height,width,solved=True,path=path)
