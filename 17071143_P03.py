#-----------------------------------------------------------------------------
class Node: 
    def __init__(self, state=None, parent=None, cost=0):
        
        self.state = state 
        self.parent = parent
        self.cost = cost 
        self.children = []
        
    def addChildren(self, children): 
        
        self.children.extend(children)

#----------------------------------------------------------------------------- 
def expansion(state_space, node): 
    children = []
    
    for [m,n,c] in state_space: 
        
        if m == node.state: 
            children.append(Node(n, node.state, node.cost + c))
        
        elif n == node.state: 
            children.append(Node(m, node.state, node.cost + c))
    
    return children

#-----------------------------------------------------------------------------
# MUST UNDERSTAND MORE! 
def insertionSort(frontier):
    
    i = 1 
    while i < len(frontier): 
        
        x = i 
        while x > 0 and frontier[x - 1].cost > frontier[x].cost:
            
            frontier[x], frontier[x - 1] = frontier[x - 1], frontier[x]
            
            x = x - 1
            
        i = i + 1
        
    return frontier

#----------------------------------------------------------------------------- 
def checkredundant(frontier, child):
    
    duplicate_test = -1
    for each_frontier in range(len(frontier)): 
                    
        if frontier[each_frontier].state == child.state and frontier[each_frontier].parent == child.parent: 
                        
            # NEED ANOTHER IF STATEMENT HERE FOR COST CHECKING
            if frontier[each_frontier].cost > child.cost:
                duplicate_test = each_frontier
                break     
                        
    return duplicate_test

#-----------------------------------------------------------------------------
def ucs(state_space, initial_state, goal_state): 
    frontier = []
    explored = []
    goalie = Node()
    foundgoal = False 
    solution = []
    
    frontier.append(Node(initial_state, None))
    
    while not foundgoal: 
        
        if frontier[0].state == goal_state: 
            foundgoal = True
            goalie = frontier[0]
            break
        
        children = expansion(state_space, frontier[0])
        
        frontier[0].addChildren(children)
        
        explored.append(frontier[0])
        
        del frontier[0]
        
        
        for child in children: 
            if not (child.state in [e.state for e in explored]):
                
                duplicate_test = checkredundant(frontier, child)
                
                if duplicate_test != -1: 
                    
                    del frontier[duplicate_test]
                    frontier.append(child)
                    
                else: 
                    
                    frontier.append(child)
                
                frontier = insertionSort(frontier)
        
        print("_ _ _" * 18)
        print("Frontier: ", [[f.state, f.cost] for f in frontier])
        print("Explored", [e.state for e in explored])
              
    solution = [goalie.state]
    path_cost = 0
        
    while goalie.parent is not None:
        
        solution.insert(0, goalie.parent)
        
        for e in explored: 
            
            if e.state == goalie.parent: 
                path_cost += getCost(state_space, e.state, goalie.state)
                goalie = e
                break
    
    return solution, path_cost
            
#-----------------------------------------------------------------------------    
def getCost(state_space, state0, state1):
    for [m, n, c] in state_space:
        if [state0, state1] == [m, n] or [state1, state0] == [m, n]:
            return c
        
#-----------------------------------------------------------------------------  
if __name__ == "__main__":

    state_space = [
                    ["Arad", "Zerind", 75],
                    ["Arad", "Timisoara", 118],
                    ["Arad", "Sibiu", 140],
                    ["Zerind", "Oradea", 71],
                    ["Oradea", "Sibiu", 151],
                    ["Sibiu", "Fagaras", 99],
                    ["Sibiu", "Rimnicu Vilcea", 80],
                    ["Fagaras", "Bucharest", 211],
                    ["Rimnicu Vilcea", "Craiova", 146],
                    ["Rimnicu Vilcea", "Pitesti", 97],
                    ["Pitesti", "Bucharest", 101],
                    ["Pitesti", "Craiova", 138],
                    ["Craiova", "Drobeta", 120],
                    ["Drobeta", "Mehadia", 75],
                    ["Mehadia", "Lugoj", 70],
                    ["Lugoj", "Timisoara", 111],
                    ["Bucharest", "Giurgiu", 90],
                    ["Bucharest", "Urziceni", 85],
                    ["Urziceni", "Vaslui", 142],
                    ["Urziceni", "Hirsova", 98],
                    ["Hirsova", "Eforie", 86],
                    ["Vaslui", "Iasi", 92],
                    ["Iasi", "Neamt", 87],
                    ]

    initial_state = "Arad"
    goal_state = "Bucharest"

    [solution, cost] = ucs(state_space, initial_state, goal_state)
    
    print("Solution: ", solution)
    print("Path Cost: ", cost)
