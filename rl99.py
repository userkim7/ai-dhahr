import os,msvcrt
import pickle
import atexit
import random
import copy

#□■▣◆◇◈

'''
        for num in range(len(List)-1,0,-1):
            List[num]=[List[num][0]-List[num-1][0],List[num][1]-List[num-1][1]]
        List[0]=[0,0]'''
#####
class Play:
    def __init__(self):
        self.map_data=[[0 for i in range(17)] for j in range(4)]+[[0,0,0,0]+[9 for i in range(9)]+[0,0,0,0] for j in range(9)]+[[0 for i in range(17)] for j in range(4)]
        self.map_shape=[['┏ ']+['┳ ' for i in range(7)]+['┓']]+[['┣ ']+['╋ ' for i in range(7)]+['┫'] for j in range(7)]+[['┗ ']+['┻ ' for i in range(7)]+['┛']]
        self.player_color=1
        self.play_data=[]
        self.pos_data=[]

    def judge(self,pos,color):
        for List in ([1,-1],[1,0],[1,1],[0,1]):
            data=[]
            win=0
            for num in range(-4,5):
                data.append(play.map_data[pos[1]+4+List[1]*num][pos[0]+4+List[0]*num])
            for num in data:
                if num==color:
                    win+=1
                else:
                    win=0
                if win==5:
                    return True

    def analysis(self):
        if len(self.pos_data)>1:
            self.play_data.append([self.pos_data[-1][0]-self.pos_data[-2][0],self.pos_data[-1][1]-self.pos_data[-2][1]])
        else:
            self.play_data.append([0,0])

    def choose_color(self):
        self.player_color=random.choice([-1,1])

    def choose_pos(self):
        pos=ai.position(self.player_color)
        '''
        pos=[-4,-4]
        while self.map_data[pos[1]+4][pos[0]+4]!=9:
            pos=list(map(int,input().split(' ')))
            '''
        self.map_data[pos[1]+4][pos[0]+4]=self.player_color
        self.map_shape[pos[1]][pos[0]]=' ■□'[self.player_color]
        self.pos_data.append(pos)
        #ai.weight[pos[1]][pos[0]]=-99
        self.analysis()
        return pos

    def computer_pos(self):
        pos=ai.position(self.player_color*-1)
        self.map_data[pos[1]+4][pos[0]+4]=self.player_color*-1
        self.map_shape[pos[1]][pos[0]]=' ■□'[self.player_color*-1]
        self.pos_data.append(pos)
        #ai.weight[pos[1]][pos[0]]=-99
        self.analysis()
        return pos

    def play(self):
        run=True
        ai.run=True
        ai.weight=[[0 for i in range(9)]for j in range(9)]
        self.choose_color()
        if self.player_color==1:
            if should_print:
                list_print(self.map_shape)#
            self.judge(self.choose_pos(),1)
        while run:
            if len(self.play_data)==81:
                return 0
            else:
                if should_print:
                    list_print(self.map_shape)#
                if self.judge(self.computer_pos(),self.player_color*-1):
                    return -1*self.player_color
                if should_print:
                    list_print(self.map_shape)#
                if self.judge(self.choose_pos(),self.player_color):
                    return 1*self.player_color

class Ai:
    def __init__(self):
        
        with open('data.pickle','rb') as f:
            self.winning_data=pickle.load(f)
            
        #self.winning_data=[[{'pos':[0,0],'next':[]}]]+[[] for i in range(99)]
        self.run=True
        self.training_data={}
        self.weight=[[0 for i in range(9)]for j in range(9)]

    def heavy(self,pos,color):
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
                try:
                     self.weight[pos[1]+List[1]*num][pos[0]+List[0]*num]=weight[num+5]
                except:
                    pass

    def algorithm(self):
        num=0
        data=[]
        for row in self.weight:
            if max(row)>num:
                num=max(row)
        for y in range(9):
            for x,value in enumerate(self.weight[y]):
                if value==num:
                    data.append([x,y])
        return random.choice(data)

    def position(self,color):
        if not play.play_data or not self.run or E>random.random():
            return ai.random_pos()
            #return self.algorithm()
        for leaf in self.winning_data[len(play.pos_data)]:
            self.run=False
            if play.play_data[-1]==leaf['pos']:
                self.run=True
                self.training_data=leaf['next']
                break
        num=0
        pos=[]
        for leaf in self.training_data:
            if leaf['reward']>num:
                num=leaf['reward']
                pos.append(leaf['pos'])
        for num in range(len(pos)-1,-1,-1):
            pos[num]=[play.pos_data[-1][0]+pos[num][0],play.pos_data[-1][1]+pos[num][1]]
            try:
                if play.map_data[pos[num][1]+4][pos[num][0]+4]==9:
                    return pos[num]
            except:
                pass
        return self.random_pos()
        #return self.algorithm()

    def random_pos(self):
        pos=[random.randint(0,8),random.randint(0,8)]
        while play.map_data[pos[1]+4][pos[0]+4]!=9:
            pos=[random.randint(0,8),random.randint(0,8)]
        return pos

    def treeing(self,List,score):
        data=self.winning_data
        List=copy.deepcopy(List)
        for flip in range(2):
            for turn in [[1,-1],[-1,1],[1,-1],[1,1]]:
                data=self.winning_data
                reward_list=[]
                for num in range(len(List)):
                    run=True
                    run2=True
                    for leaf in data[num]:
                        if List[num]==leaf['pos']:
                            run=False
                            if num<len(List)-1:
                                for leaf2 in leaf['next']:
                                    if leaf2['pos']==List[num+1]:
                                        run2=False
                                        reward_list.append(leaf2['reward'])
                                        break
                                if run2:
                                    leaf['next'].append({'pos':List[num+1],'reward':0})
                                    reward_list.append(0)
                            break
                    if run:
                        data[num].append({'pos':List[num],'next':[]})
                        try:
                            data[num][-1]['next'].append({'pos':List[num+1],'reward':0})
                        except:
                            pass
                        reward_list.append(0)
                reward_list[-1]=round((1-A)*reward_list[-1]+A*score,K)
                for num in range(len(reward_list)-2,-1,-1):
                    reward_list[num]=round((1-A)*reward_list[num]+A*(score*(-1)**num)*(reward_list[num+1]),K)
                for num in range(len(reward_list)-1):
                    for leaf in data[num]:
                        if List[num]==leaf['pos']:
                            for leaf2 in leaf['next']:
                                if leaf2['pos']==List[num+1]:
                                    leaf2['reward']=reward_list[num+1]
                                    break
                            break
                for num in range(1,len(List)):
                    List[num]=[List[num][0]*turn[0],List[num][1]*turn[1]]
            if not flip:
                for pos in List:
                    pos.reverse()

    def save(self):
        with open('data.pickle','wb') as f:
            pickle.dump(self.winning_data,f)

    def clear(self):
        self.winning_data=[[{'pos':[0,0],'next':[]}]]+[[] for i in range(360)]
        with open('data.pickle','wb') as f:
            pickle.dump(self.winning_data,f)

def list_print(List):
    #os.system('cls')
    data=''
    for row in List:
        data+=''.join(row)+'\n'
    print(data)

#####
    
ai=Ai()

#atexit.register(ai.save)

A=1
K=500
E=1

'''
print(ai.winning_data)
input()
'''

###
for num in range(1,10001):
    play=Play()
    should_print=False
    '''
    if num%10000==1:
        should_print=True
        '''
    ai.treeing(play.play_data,play.play())
    
    if should_print or num%250==1:
        os.system('cls')#
        list_print(play.map_shape)
        #input()
        ai.save()
        #os.system('cls')
        
    E*=0.9999
    A*=0.9999
    '''
    if num%250==0:
        ai.save()
        #print(f'\r{num}',end='')
        '''
    print(f'{num}')
        
    
input()
#ai.save()
