from Graph import digraph,random

DefaultNames="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def make_random_game(totalplaces=16,Names=DefaultNames,minpaths=1,maxpaths=8,startnode=0,playerturn=0):
    vertices={}
    edges=[]
    for vertex in range(totalplaces):
        vertices[Names[vertex]]=(1+2*round(random()*2)*int(random()*3+1))
    for i in range(totalplaces):
        edgecount=round(minpaths+random()*(maxpaths-minpaths))
        for edge in range(edgecount):
            dest=int(random()*totalplaces)
            if not (Names[i],Names[dest]) in edges:
                edges.append((Names[i],Names[dest]))
    return Game(digraph(vertices,edges))

class Game:
    def __init__(self,digraph,startnode='0',playerturn=0):
        self.digraph=digraph
        self.currentnode=startnode
        self.playerturn=0
        self.players=2
    def AvailableMoves(self,node=None):
        if node==None: #use current node if undefined
            node=self.currentnode
        moves=[]
        for i in self.digraph.edges:
            
            if i[0]==node:
                moves.append(i[1])
        return moves
    def Move(self,newnode):
        #Move from current node to new node
        self.currentnode=newnode
        #Award Points from new node to the active player.
        #Switch Turns
        self.playerturn=(self.playerturn+1)%self.players
    def Play(self):
        Scores=[0 for i in range(self.players)]
        N=0
        while 1:
            print("Turn %03d"%N)
            turn=self.playerturn
            print("It is player %02d's turn. \nThe game is currently in state %s "%(self.playerturn,self.currentnode))
            print("You can move to node(s):")
            moves=self.AvailableMoves()
            for i in moves:
                print(" "+i)
            path=input("Please choose a path: (%s)"%("\\".join(moves)))
            while not path in moves:
                path=input("Invalid path! Please choose a path %s"%("\\".join(moves)))
            self.Move(path)
            points=self.digraph.vertices[self.currentnode]
            print("This move was worth %02d points"%points)
            Scores[turn]+=points
            N+=1
            print("Current Score: %s"%("-".join(["%03d"%s for s in Scores])))
            
            

TestGame=make_random_game(startnode=0,playerturn=0)
TestGame.Play()
im=TestGame.digraph.draw()
im.save('test.png')
