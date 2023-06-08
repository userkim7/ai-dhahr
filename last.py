import os
import pickle
import random
import copy

size=9

class Play:
    def __init__(self):
        self.map_data=[[0 for i in range(size+8)] for j in range(4)]+[[0,0,0,0]+[9 for i in range(size)]+[0,0,0,0] for j in range(size)]+[[0 for i in range(size+8)] for j in range(4)]
        self.map_shape=[['┏ ']+['┳ ' for i in range(size-2)]+['┓']]+[['┣ ']+['╋ ' for i in range(size-2)]+['┫'] for j in range(size-2)]+[['┗ ']+['┻ ' for i in range(size-2)]+['┛']]
        self.player_color=1
        self.computer_color=-1
        self.play_data=[]
        self.pos_data=[]
        self.score_data=[]

    def judge(self,pos,color): 
        for List in ([1,-1],[1,0],[1,1],[0,1]):
            data=[]
            win=0
            for num in range(-4,5):
                data.append(self.map_data[pos[1]+4+List[1]*num][pos[0]+4+List[0]*num])
            for num in data:
                if num==color:
                    win+=1
                else:
                    win=0
                if win==5:
                    return True
                
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
                     ai.weight[pos[1]+List[1]*num][pos[0]+List[0]*num]=weight[num+5]
                except:
                    pass
                
    def analysis(self,color):
        if len(self.pos_data)>1:
            self.play_data.append([self.pos_data[-1][0]-self.pos_data[-2][0],self.pos_data[-1][1]-self.pos_data[-2][1]])
        else:
            self.play_data.append([0,0])
        self.score_data.append(ai.scoring()*color)
                
    def choose_color(self):
        self.player_color=random.choice([-1,1])
        self.computer_color=self.player_color*-1

    def choose_pos(self):
        pos=ai.position(self.player_color)
        '''
        pos=[-4,-4]
        while self.map_data[pos[1]+4][pos[0]+4]!=9:
            pos=list(map(int,input().split(' ')))
            '''
        self.map_data[pos[1]+4][pos[0]+4]=self.player_color
        self.map_shape[pos[1]][pos[0]]=' ■□'[self.player_color]
        ai.weight[pos[1]][pos[0]]=-99
        self.pos_data.append(pos)
        self.analysis(self.player_color)
        return pos

    def computer_pos(self):
        pos=ai.position(self.computer_color)
        self.map_data[pos[1]+4][pos[0]+4]=self.computer_color
        self.map_shape[pos[1]][pos[0]]=' ■□'[self.computer_color]
        ai.weight[pos[1]][pos[0]]=-99
        self.pos_data.append(pos)
        self.analysis(self.computer_color)
        return pos

    def play(self):
        ai.weight=[[0 for i in range(size)] for j in range(size)]
        run=True
        self.choose_color()
        if self.player_color==1:
            if should_print:
                list_print(self.map_shape)#
            self.judge(self.choose_pos(),1)
        while run:
            if len(self.play_data)==size**2:
                return 0
            else:
                if should_print:
                    list_print(self.map_shape)#
                if self.judge(self.computer_pos(),self.computer_color):
                    return self.computer_color
                if should_print:
                    list_print(self.map_shape)#
                if self.judge(self.choose_pos(),self.player_color):
                    return self.player_color

class Ai:
    def __init__(self):
        self.weight=[[0 for i in range(size)] for j in range(size)]
        '''try:
            with open('list.pickle','rb') as f:
                self.name_list=pickle.load(f)
        except:'''
        self.name_list=[]

    def scoring(self):
        num=0
        data=[]
        for row in self.weight:
            if max(row)>num:
                num=max(row)
        return num

    def position(self,color):
        if not play.play_data or random_rate>random.random():
            return self.random_pos()
        return self.alphabeta(color)

    def random_pos(self):
        if not play.pos_data:
            return [random.randint(0,size-1),random.randint(0,size-1)]
        pos=[random.randint(0,size-1),random.randint(0,size-1)]
        while play.map_data[pos[1]+4][pos[0]+4]!=9:
            pos=[random.randint(0,size-1),random.randint(0,size-1)]
        return pos
    
    def alphabeta(self,color):
        d=5
        depth=len(play.play_data)
        data=[]
        tree=[[[[0 for i in range(size**2)] for j in range(size**2)] for k in range(size**2)] for l in range(size**2)]
        for num in range(len(self.name_list)):
            if self.name_list[num][:depth]==play.play_data:
                data.append([num,self.name_list[num][depth:depth+d]])
        if not data:
            return self.random_pos()
        for List in data:
            address=[]
            for num in range(len(List[1])-1):
                address.append(self.index(List[1][num]))
            for pos in address:
                target=tree[pos]
            with open('data/List[0].pickle','rb') as f:
                target=pickle.load(f)[depth]
                
        for num in range(size**2):
            for num2 in range(size**2):
                for num3 in range(size**2):
                    if tree[num][num2][num3]==[0 for i in range(size**2)]:
                        tree[num][num2][num3]=0
                        continue
                    memory=99
                    for num4 in tree[num][num2][num3]:
                        if num4<memory and num4!=0:
                            memory=num4
                    tree[num][num2][num3]=memory
                if tree[num][num2]==[0 for i in range(size**2)]:
                    tree[num][num2]=0
                    continue
                memory=-99
                for num4 in tree[num][num2]:
                    if num4>memory and num4!=0:
                        memory=num4
                tree[num][num2]=memory
            if tree[num]==[0 for i in range(size**2)]:
                tree[num]=0
                continue
            memory=99
            for num4 in tree[num]:
                if num4<memory and num4!=0:
                    memory=num4
            tree[num]=memory
        memory=0
        for num in range(len(tree)):
            if num>memory:
                memory=num
        memory2=[]
        for num,value in enumerate(tree):
            if value==memory:
                memory2.append(num)
        return self.index2(random.choice(memory2))
            
    def index(self,pos):
        return (pos[1]+round(size/2))*size+(pos[0]+round(size/2))

    def index2(self,num):
        return [num%size-round(size/2),num//size-round(size/2)]
            
    def treeing(self,score):
        List=copy.deepcopy(play.play_data)
        run=True
        for flip in range(2):
            for turn in [[1,-1],[-1,1],[1,-1],[1,1]]:
                for num in range(len(self.name_list)):
                    if self.name_list[num][0]==List:
                    run=False
                    self.name_list[num][1]+=score
                    break
                if run:
                    self.name_list.append([List,score])
                with open('list.pickle','wb') as f:
                    pickel.dump(self.name_list,f)
                for num in range(1,len(List)):
                    List2[num]=[List[num][0]*turn[0],List[num][1]*turn[1]]
                List=copy.deepcopy(List2)
            if not flip:
                for pos in List:
                    pos.reverse()
                
def list_print(List):
    #os.system('cls')
    data=''
    for row in List:
        data+=''.join(row)+'\n'
    print(data)


play=Play()
ai=Ai()

random_rate=1
learn_rate=1

for num in range(1,10001):
    play=Play()
    should_print=False

    ai.treeing(play.play())

    if should_print or num%100==1:
        os.system('cls')
        list_print(play.map_shape)
    random_rate*=0.9999
    learn_rate*=0.9999
    print(f'{num}')
    
