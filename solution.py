#!/usr/bin/env python3
from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3
from itertools import combinations 
import time
#### All your code can go here.

#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.

KB = Glucose3()
pos_to_index = [
                 [-1,-1,-1,-1], 
                 [-1,-1,-1,-1], 
                 [-1,-1,-1,-1],  
                 [-1,-1,-1, 0],  
                ]
visited = [
             [1,0,0,0], 
             [0,0,0,0], 
             [0,0,0,0],  
             [0,0,0,0],  
            ]

def no_mine(pos, direction):
    global KB
    global pos_to_index
    global visited
    validDirections = ['Up','Down','Left','Right']
    assert direction in validDirections, 'Invalid Direction.'
    index = validDirections.index(direction)
    validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
    move = validMoves[index]
    newPos = []
    for v, inc in zip(pos,move):
        z = v + inc 
        z = 4 if z>4 else 1 if z<1 else z 
        newPos.append(z)
    if newPos == pos:
        return
    KB.add_clause([(-1)*(pos_to_index[newPos[0]-1][newPos[1]-1]+1)])

def find_best_safe_unvisited():
    global KB
    global pos_to_index
    X = []
    for i in range(4):
        for j in range(4):
        	if i==3 and j==3:
        		if KB.solve([pos_to_index[2][3] + 1]) == False or KB.solve([pos_to_index[3][2] + 1]) == False:
        			X.clear()
        			X.append([4,4])
        			return(X)
        	else:
	            if len(X) == 0 or abs(i+1) + abs(j+1) >= abs(X[0][0]) + abs(X[0][1]):
	                if KB.solve([pos_to_index[i][j] + 1]) == False and visited[i][j] == 0:
	                    if len(X) == 0:
	                        X.append([i+1,j+1])
	                    else:
	                        if abs(i+1) + abs(j+1) == abs(X[0][0]) + abs(X[0][1]):
	                            X.append([i+1, j+1])
	                        if abs(i+1) + abs(j+1) > abs(X[0][0]) + abs(X[0][1]):
	                            X.clear()
	                            X.append([i+1, j+1])

    return(X)

def feasible(pos):
    if pos[0]>=1 and pos[0]<=4 and pos[1]>=1 and pos[1]<=4:
        return True
    else:
        return False

def goto(X, pos):
    global KB
    global pos_to_index
    a = [pos]
    b = [-1]
    i = 0
    visited = [
                [0,0,0,0], 
                [0,0,0,0], 
                [0,0,0,0],  
                [0,0,0,0],  
              ]
    visited[pos[0]-1][pos[1]-1] = 1 
    for p in a:
        if feasible([p[0],p[1]+1]) and visited[p[0]-1][p[1]] == 0 and KB.solve([pos_to_index[p[0]-1][p[1]] + 1]) == False:
            a.append([p[0],p[1]+1])
            b.append(i)
            visited[p[0]-1][p[1]] = 1
        if feasible([p[0]+1,p[1]]) and visited[p[0]][p[1]-1] == 0 and KB.solve([pos_to_index[p[0]][p[1]-1] + 1]) == False:
            a.append([p[0]+1,p[1]])
            b.append(i)
            visited[p[0]][p[1]-1] = 1
        if feasible([p[0],p[1]-1]) and visited[p[0]-1][p[1]-2] == 0 and KB.solve([pos_to_index[p[0]-1][p[1]-2] + 1]) == False:
            a.append([p[0],p[1]-1])
            b.append(i)
            visited[p[0]-1][p[1]-2] = 1
        if feasible([p[0]-1,p[1]]) and visited[p[0]-2][p[1]-1] == 0 and KB.solve([pos_to_index[p[0]-2][p[1]-1] + 1]) == False:
            a.append([p[0]-1,p[1]])
            b.append(i)
            visited[p[0]-2][p[1]-1] = 1

        i += 1
    #print('a = ', a)
    #print('b = ', b)
    validDirections = ['Up','Down','Left','Right']
    validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
    indices = []
    for i in range(len(a)):
        if a[i] in X:
            while(i != -1):
                indices.append(i)
                i = b[i]
            break
    #print('indices = ', indices)
    Y = []
    for i in range(len(indices)):
        j = len(indices) - 1 - i
        if j < len(indices) - 1:
            index = validMoves.index([a[indices[j]][0] - a[indices[j+1]][0], a[indices[j]][1] - a[indices[j+1]][1]])
            #print('index = ', index)
            Y.append(validDirections[index])
    return(Y)
        
def add_info(p, pos):
    global KB
    global pos_to_index
    if p == '=0':
            no_mine(pos, 'Up')
            no_mine(pos, 'Down')
            no_mine(pos, 'Left')
            no_mine(pos, 'Right')
    if p == '=1':
            a = []
            if pos[0]>1:
                a.append(pos_to_index[pos[0]-2][pos[1]-1] + 1)
            if pos[1]<4:
                a.append(pos_to_index[pos[0]-1][pos[1]] + 1)
            if pos[0]<4:
                a.append(pos_to_index[pos[0]][pos[1]-1] + 1)
            if pos[1]>1:
                a.append(pos_to_index[pos[0]-1][pos[1]-2] + 1)
            KB.add_clause(a)
            for i in range(len(a)):
                a[i] = (-1)*a[i]
            #print(a)
            comb = combinations(a, 2)
            for i in comb:
                KB.add_clause(i)
            a.clear()
    if p == '>1': 
            a = []
            if pos[0]>1:
                a.append(pos_to_index[pos[0]-2][pos[1]-1] + 1)
            if pos[1]<4:
                a.append(pos_to_index[pos[0]-1][pos[1]] + 1)
            if pos[0]<4:
                a.append(pos_to_index[pos[0]][pos[1]-1] + 1)
            if pos[1]>1:
                a.append(pos_to_index[pos[0]-1][pos[1]-2] + 1)
            comb = combinations(a, len(a)-1)
            for i in comb:
                KB.add_clause(i)
            #print(a)
            a.clear()

def main():

    ag = Agent()
    
    #ag.TakeAction('Right')
    #print('Percept ',ag.PerceiveCurrentLocation())
    #ag.TakeAction('Right')
    #print('Percept ',ag.PerceiveCurrentLocation())

    global KB
    global pos_to_index
    global visited

    pos_in_order = [[4,4]]
    for a in pos_in_order:
        if a[0]-1 > 0:
                if(pos_to_index[a[0]-2][a[1]-1] == -1):
                        pos_in_order.append([a[0]-1, a[1]])
                        pos_to_index[a[0]-2][a[1]-1] = len(pos_in_order)-1      
        if a[1]-1 > 0:
                if(pos_to_index[a[0]-1][a[1]-2] == -1):
                        pos_in_order.append([a[0], a[1]-1])
                        pos_to_index[a[0]-1][a[1]-2] = len(pos_in_order)-1                      

    print(pos_to_index)
    #print(pos_in_order)

#add contion of [1,1] and [4,4] being mine free
    KB.add_clause([-1])
    KB.add_clause([-16])

#add condition of 2-5 Mines only
    a = []
    for i in range(16):
        a.append(i+1)

    comb = combinations(a, 15)
    for i in comb:
        KB.add_clause(i)
    
    a.clear()
    for i in range(16):
        a.append((-1)*(i+1)) 
    
    comb = combinations(a, 6)
    for i in comb:
        KB.add_clause(i)
    a.clear()

    Moves=[]

#starts moving now
    print('curLoc',ag.FindCurrentLocation())
    while(ag.FindCurrentLocation() != [4,4]):
        #time.sleep(1)
        p = ag.PerceiveCurrentLocation()    
        print('Percept ',p)
        pos = ag.FindCurrentLocation()
        add_info(p, pos)
        X = find_best_safe_unvisited()
        #print(X)
        if len(X) == 0:
            print("Wrong Board, Requires Risk which I wont take")
            return
        Y = goto(X, pos)
        #print(Y)
        for i in range(len(Y)):
            #time.sleep(1)
            Moves.append(Y[i])
            ag.TakeAction(Y[i])
            p = ag.FindCurrentLocation()
            if visited[p[0]-1][p[1]-1] == 0 and i < len(Y) - 1:
                visited[p[0]-1][p[1]-1] = 1
                pt = ag.PerceiveCurrentLocation()
                add_info(pt, p)
            visited[p[0]-1][p[1]-1] = 1


    print('curLoc',ag.FindCurrentLocation())
    print('successfully exited with the steps: ', Moves)
    
if __name__=='__main__':
    main()
