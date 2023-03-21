import os,msvcrt
import pickle
import atexit
import random
import copy

#MCTS or future_look

#□■▣◆◇◈


#####

class Play:
    def __init__(self):
        self.map_data=[[0 for i in range(27)] for j in range(4)]+[[0,0,0,0]+[9 for i in range(19)]+[0,0,0,0] for j in range(19)]+[[0 for i in range(27)] for j in range(4)]
        self.map_shape=[['┏ ']+['┳ ' for i in range(17)]+['┓']]+[['┣ ']+['╋ ' for i in range(17)]+['┫'] for j in range(17)]+[['┗ ']+['┻ ' for i in range(17)]+['┛']]
        self.player_color=1
        self.play_data=[]

    def judge(self,pos,color):
        win=True
        for x in range(-1,2):
            for y in range(-1,2):
                if x!=0 or y!=0:
                    for num in range(1,5):
                        if self.map_data[pos[1]+4+num*y][pos[0]+4+num*x]!=color:
                            win=False
                    if win:
                        return True
                    else:
                        win=True

        for List in ([1,-1],[1,0],[1,1],[0,1]):
            data=[]
            for num in range(-4,5):
                data.append(play.map_data[pos[1]+4+List[1]*num][pos[0]+4+List[0]*num])
            weight=[0]+[data[num]**2-1 for num in range(9)]+[0]

            for num in range(9):
                if weight[num+1]>0:
                    add=0
                    sub=0
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
                                    sub-=1
                                run=False
                    weight[num+1]+=add+sub-80

            for num in range(-4,5):
                ai.weight[pos[1]+List[1]*num][pos[0]+List[0]*num]=weight[num+5]
                    

    def choose_color(self):
        pass

    def choose_pos(self):
        pos=[-4,-4]
        while self.map_data[pos[1]+4][pos[0]+4]!=9:
            pos=list(map(int,input().split(' ')))
        self.map_data[pos[1]+4][pos[0]+4]=self.player_color
        self.map_shape[pos[1]][pos[0]]=' ■□'[self.player_color]
        ai.weight[pos[1]][pos[0]]=-99
        self.play_data.append(pos)
        return pos

    def computer_pos(self):
        pos=ai.algorithm()
        self.map_data[pos[1]+4][pos[0]+4]=self.player_color*-1
        self.map_shape[pos[1]][pos[0]]=' ■□'[self.player_color*-1]
        ai.weight[pos[1]][pos[0]]=-99
        self.play_data.append(pos)
        return pos

    def play(self):
        run=True
        self.choose_color()
        if self.player_color==1:
            list_print(self.map_shape)#
            self.judge(self.choose_pos(),1)
        while run:
            if len(self.play_data)==361:
                return 0
            else:
                list_print(self.map_shape)#
                if self.judge(self.computer_pos(),self.player_color*-1):
                    return -1*self.player_color
                list_print(self.map_shape)#
                if self.judge(self.choose_pos(),self.player_color):
                    return 1*self.player_color

class Ai:
    def __init__(self):
        with open('data.pickle','rb') as file:
            self.winning_data=pickle.load(file)
        self.weight=[[0 for i in range(19)] for j in range(19)]

    
    def algorithm(self):
        num=0
        data=[]
        for row in self.weight:
            if max(row)>num:
                num=max(row)
        for y in range(19):
            for x,value in enumerate(self.weight[y]):
                if value==num:
                    data.append([x,y])
        return random.choice(data)
                

    def treeing(self,List,score):
        data=self.winning_data
        List=copy.deepcopy(List)
        for num in range(1,len(List)):
            List[num]=[List[num][0]-List[0][0],List[num][1]-List[0][0]]
        List[0]=[0,0]
        for flip in range(2):
            for turn in [[1,-1],[-1,1],[1,-1],[1,1]]:
                for num in range(1,len(List)):
                    run=True
                    for leaf in data['next']:
                        if List[num]==leaf['pos']:
                            run=False
                            data=leaf
                            leaf['win'][0]+=1
                            leaf['win'][score*(-1)**num]+=1
                    if run:
                        data['next'].append({'win':[1,0,0],'pos':List[num],'next':[]})
                        data=data['next'][-1]
                        data['win'][score*(-1)**num]+=1
                for num in range(1,len(List)):
                    List[num]=[List[num][0]*turn[0],List[num][1]*turn[1]]
            if not flip:
                for pos in List:
                    pos.reverse()

    def save(self):
        with open('data.pickle','wb') as f:
            pickle.dump(self.winning_data,f)

    def clear(self):
        self.winning_data={'pos':[0,0],'next':[]}
        with open('data.pickle','wb') as f:
            pickle.dump(self.winning_data,f)

def list_print(List):
    os.system('cls')
    data=''
    for row in List:
        data+=''.join(row)+'\n'
    print(data)

#####
    
play=Play()
ai=Ai()

#atexit.register(ai.save)

ai.treeing(play.play_data,play.play())
list_print(play.map_shape)
input()
print(ai.winning_data)
input()
ai.save()
