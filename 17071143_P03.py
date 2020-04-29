class Node: 
    def __init__(self, state=None, parent=None, cost=0):
        self.state = state 
        self.parent = parent
        self.cost = cost 
        self.children = []
        
    def addchildren(self, children): 
        self.children.extend(children)
        

def expansion(state_space, node): 
    children = []
    for [m,n,c] in state_space: 
        if m == node.state: 
            children.append(Node(n, node.state, node.cost+c))
        elif n == node.state: 
            children.append(Node(m, node.state, node.cost+c))
    return children

def ucs(state_space, initial_state, goal_state): 
    frontier = []
    explored = []
    goalie = Node()
    goalfound = False 
    solution = []
    
    frontier.append(Node(initial_state, None))
    
    while not goalfound: 
        if frontier[0] == goal_state: 
            goalie = frontier[0]
            foundgoal = True
            break
        
        else: 
            children = expansion(state_space, frontier[0])
            explored.append(frontier[0])
            frontier[0].addchildren(children)
            del frontier[0]
        
        for child in children: 
            
            if not (child.state in [e.state for e in explored]):
                duplicate_test = check_redundancy(frontier, children)
                
                if duplicate_test != -1: 
                    del frontier[duplicate_test]
                    frontier.append(child)
                else: 
                    frontier.append(child)
              
def check_redundancy(frontier, children): 
    duplicate_test = -1
    for x in frontier: 
        if x in children: 
            # NEED ANOTHER IF STATEMENT HERE FOR COST CHECKING
            duplicate_test = frontier.indexOf(x)
            break
        
    return duplicate_test
        
if __name__ == '__main__':
    state_space = [['Arad', 'Zerind', 75], ['Arad', 'Timisoara', 118], ['Arad', 'Sibiu', 140],
                   ['Timisoara', 'Lugoj', 111], ['Lugoj', 'Mehadia', 70], ['Mehadia', 'Drobeta', 75],
                   ['Drobeta', 'Craiova', 120], ['Craiova', 'Rimnicu Vilcea', 146], ['Craiova', 'Pitesti', 138],
                   ['Pitesti', 'Bucharest', 101], ['Rimnicu Vilcea', 'Pitesti', 97], ['Rimnicu Vilea', 'Sibiu', 80],
                   ['Zerind', 'Arad', 75], ['Zerind', 'Oradea', 71], ['Oradea', 'Sibiu', 151], ['Sibiu', 'Arad', 140],
                   ['Sibiu', 'Fagaras', 99], ['Sibiu', 'Rimnicu Vilcea', 80], ['Fagaras', 'Bucharest', 211]]

    initial_state = 'Arad'
    goal_state = 'Bucharest'
