import os
import pickle
import random
import copy
import re
import sys
from math import inf

sys.setrecursionlimit(10**6)

size=9

class Board:
    def __init__(self):
        self.data=[[0 for i in range(size+8)] for j in range(4)]+[[0,0,0,0]+[9 for i in range(size)]+[0,0,0,0] for j in range(size)]+[[0 for i in range(size+8)] for j in range(4)]
        self.look=[['┏ ']+['┳ ' for i in range(size-2)]+['┓']]+[['┣ ']+['╋ ' for i in range(size-2)]+['┫'] for j in range(size-2)]+[['┗ ']+['┻ ' for i in range(size-2)]+['┛']]

    def print(self):
        if not should_print:
            return 0
        os.system('cls')
        data=''
        for List in self.look:
            data+=''.join(List)+'\n'
        print(data)

    def heavy(self,pos,color):
        for List in ([1,-1],[1,0],[1,1],[0,1]):
            data=[]
            for num in range(-4,5):
                data.append(board.data[pos[1]+4+List[1]*num][pos[0]+4+List[0]*num])
            weight=[0]+[data[num]**2-1 for num in range(9)]+[0]

            for num in range(9):
                if weight[num+1]>0:
                    add=0
                    for num2 in [-1,1]:
                        run=True
                        num1=num2
                        while run:
                            num3=num-num1
                            if num3<0 or num3>8:
                                break
                            if data[num3]==color:
                                add+=1
                                num1+=num2
                            else:
                                if data[num3]==color*-1:
                                    add-=1
                                run=False
                    weight[num+1]+=add-80

            for num in range(-4,5):
                try:
                     self.weight[pos[1]+List[1]*num][pos[0]+List[0]*num]=weight[num+5]
                except:
                    pass

    def max_score(self):
        return max(max(self.weight))

class Player:
    def __init__(self):
        self.color=1

    def choose_pos(self):
        pos=list(map(int,input().split(' ')))
        main.impact(pos,self.color)
        return pos

class Pc:
    def __init__(self):
        self.color=-1

    def choose_pos(self):
        pos=ai.position()
        main.impact(pos,self.color)
        return pos

p=re.compile('[+-]\d+')

class Ai:
    def __init__(self):
        try:
            with open('save.pickle','rb') as f:
                self.played_data=pickle.load(f)
        except:
            self.played_data=[]

    def random_pos(self):
        if not main.play_data:
            return [random.randint(0,size-1),random.randint(0,size-1)]
        pos=[random.randint(0,size-1),random.randint(0,size-1)]
        while board.data[pos[1]+4][pos[0]+4]!=9:
            pos=[random.randint(0,size-1),random.randint(0,size-1)]
        return pos

    def position(self):
        if not main.play_data:
            return [int(size/2),int(size/2)]
        return self.AB([])
        return self.random_pos()

    def str(self,score):
        if score>=0:
            return f'+{score}'
        else:
            return str(score)

    def save(self,score):
        if not score:
            return 0
        main.play_pos()
        List=copy.deepcopy(main.pos_data)
        for flip in range(2):
            for turn in ([1,1],[-1,1],[1,-1],[-1,-1]):
                data=''
                for pos in List:
                    data+=pos_hex([(pos[0]-List[0][0])*turn[0],(pos[1]-List[0][1])*turn[1]])
                self.played_data.append(data+self.str(score))
            if not flip:
                for num,pos in enumerate(List):
                    List[num]=[pos[1],pos[0]]

    def export(self):
        with open('save.pickle','wb') as f:
            pickle.dump(self.played_data,f)

    def AB(self,ban):
        List=[]
        for data in self.played_data:
            num=len(main.pos_hex)
            if data[:num]==main.pos_hex and data[num:2] not in ban:
                List.append(data[num:])
        if not List:
            return self.random_pos()
        List.sort()
        List=self.area(List,0)
        pos=pos_dehex(self.minmax(List,0,-inf,+inf,True)[1])
        run=True
        try:
            if board.data[pos[1]+4][pos[0]+4]==9:
                run=False
        except:
            pass
                
        while run:
            pos=self.AB(ban+[pos_hex(pos)])
            try:
                run=board.data[pos[1]+4][pos[0]+4]!=9
            except:
                pass
        return pos

    def area(self,List,depth):
        if depth>4:
            memory=0
            for data in List:
                memory+=int(p.search(data).group())
            return [memory,List[0][:2]]
        memory=0
        memory2=[]
        num=depth*2
        for num2,data in enumerate(List):
            if data[num:num+2]==List[memory][num:num+2]:
                continue
            else:
                memory2.append(self.area(List[memory:num2],depth+1))
                memory=num2
        memory2.append(self.area(List[memory:len(List)],depth+1))
        return memory2

    def minmax(self,List,depth,A,B,Max):
        if depth>4:
            return List
        if Max:
            maxE=[-inf,'']
            for data in List:
                E=self.minmax(data,depth+1,A,B,False)
                maxE=[max(maxE[0],E[0]),E[1]]
                A=max(A,E[0])
                if B<=A:
                    break
            return maxE
        else:
            minE=[inf,'']
            for data in List:
                E=self.minmax(data,depth+1,A,B,True)
                minE=[min(minE[0],E[0]),E[1]]
                B=min(B,E[0])
                if B<=A:
                    break
            return minE
                
class Main:
    def __init__(self):
        self.play_data=[]
        self.pos_data=[]
        self.pos_hex=''

    def choose_color(self):
        player.color=random.choice([-1,1])
        pc.color=player.color*-1

    def judge(self,pos,color):
        for List in ([1,-1],[1,0],[1,1],[0,1]):
            data=[]
            win=0
            for num in range(-4,5):
                data.append(board.data[pos[1]+4+List[1]*num][pos[0]+4+List[0]*num])
            for num in data:
                if num==color:
                    win+=1
                else:
                    win=0
                if win==5:
                    self.score=board.max_score()
                    return True
                
            board.heavy(pos,color)

    def impact(self,pos,color):
        board.data[pos[1]+4][pos[0]+4]=color
        board.look[pos[1]][pos[0]]=' ■□'[color]
        board.weight[pos[1]][pos[0]]=-99
        self.play_data.append(pos)
        self.pos_hex+=pos_hex2(pos)

    def play(self):
        board.weight=[[0 for i in range(size)] for j in range(size)]

        self.choose_color()

        if player.color==1:
            board.print()
            self.judge(player.choose_pos(),1)
            main.pos_hex='ee'
        while True:
            if len(self.play_data)>=size**2-1:
                return 0
            else:
                board.print()
                if self.judge(pc.choose_pos(),pc.color):
                    return pc.color*self.score
                board.print()
                if self.judge(player.choose_pos(),player.color):
                    return player.color*self.score

    def play_pos(self):
        zero=self.play_data[0]
        for pos in self.play_data:
            self.pos_data.append([pos[0]-zero[0],pos[1]-zero[1]])

vulnerable=size*2-1

def hex(num):
    List=[f'{i}' for i in range(10)]+['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s']
    return List[num//vulnerable]+List[num%vulnerable]

def dehex(Str):
    List=[f'{i}' for i in range(10)]+['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s']
    return List.index(Str[0])*vulnerable+List.index(Str[1])

def pos_hex(pos):
    return hex((pos[1]+size-1)*vulnerable+pos[0]+size-1)

def pos_hex2(pos):
    return pos_hex([pos[1]-main.play_data[0][0],pos[0]-main.play_data[0][1]])

def pos_dehex(Str):
    num=dehex(Str)
    return [num%vulnerable-size+1+main.play_data[0][0],num//vulnerable-size+1+main.play_data[0][1]]

main=Main()
board=Board()
player=Player()
pc=Pc()
ai=Ai()


should_print=True

for i in range(300000):
    main=Main()
    board=Board()
    
    ai.save(main.play())
    











    
