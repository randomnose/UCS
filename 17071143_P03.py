#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:30:43 2020

@author: esontan
"""
from queue import PriorityQueue

pathcost = PriorityQueue()

class Node: 
    def __init__(self, state=None, parent=None, cost = 0): 
        self.state = state
        self.parent = parent
        self.cost = cost
        self.children = []
        
    def addChildren(self, children):
        self.children.extend(children)
        

# To expand and find children of a node
def expansion(state_space, node): 
    children = []
    for [m, n, c] in state_space: 
        if m == node.state: 
            children.append(Node(n, node.state, node.cost+c))
        elif n == node.state: 
            children.append(Node(m, node.state, node.cost+c))
    return children


# Uniform Cost Search
def ucs(state_space, initial_state, goal_state): 
    
    frontier = [] 
    explored = []
    foundgoal = False
    goalie = Node()
    
    frontier.append(Node(initial_state, None))    
    
    while not foundgoal: 
    
        children = expansion(state_space, frontier[0])
        next_cost = pathcost.get()
        matchy = matching(state_space, next_cost)
        frontier[0].addChildren(matchy)   
        explored.append(frontier[0])
        del frontier[0]
        
        pathcost.pop()
        
        for child in children:
                if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
                    # if child node is the goal_state, then turn found_goal boolean to true and append child node
                    # to frontier[]
                    # the goal node will be stored in goalie
                    if child.state == goal_state:
                        foundgoal = True
                        goalie = child
                    frontier.append(child)
         
        print("Explored:", [e.state for e in explored])
        print("Frontier:", [f.state for f in frontier])
        print("Children:", [c.state for c in children])
        print("")
        
    solution = [goalie.state]
    path_cost = 0
    # while loop will continue to loop until the initial_state has been traced back, which is also why condition
    # is set as goalie.parent is not None. because the initial_state object has no parent as it is the first node
    # .parent is a property to let us trace back to find an object's parent (predecessor)
    while goalie.parent is not None:
        # insert the goalie's parent object into solution[]
        solution.insert(0, goalie.parent)
        # for each element in explored[]
        for e in explored:
            # if object at e is goalie's parent, then replace goalie with the parent node and repeat the process
            # this process allow us to path cost of parent node, and its parent node, and so on, until the initial node
            if e.state == goalie.parent:
                path_cost += getCost(state_space, e.state, goalie.state)
                goalie = e
                break
            
    return solution, path_cost
    
def getCost(state_space, state0, state1):
    for [m, n, c] in state_space:
        if [state0, state1] == [m, n] or [state1, state0] == [m, n]:
            return c
        
def matching(state_space, cost): 
    for [m,n,c] in state_space: 
        if cost == c:
            return [n]
            
    
if __name__ == '__main__':
    state_space = [['Arad', 'Zerind', 75], ['Arad', 'Timisoara', 118], ['Arad', 'Sibiu', 140],
                   ['Timisoara', 'Lugoj', 111], ['Lugoj', 'Mehadia', 70], ['Mehadia', 'Drobeta', 75],
                   ['Drobeta', 'Craiova', 120], ['Craiova', 'Rimnicu Vilcea', 146], ['Craiova', 'Pitesti', 138],
                   ['Pitesti', 'Bucharest', 101], ['Rimnicu Vilcea', 'Pitesti', 97], ['Rimnicu Vilea', 'Sibiu', 80],
                   ['Zerind', 'Arad', 75], ['Zerind', 'Oradea', 71], ['Oradea', 'Sibiu', 151], ['Sibiu', 'Arad', 140],
                   ['Sibiu', 'Fagaras', 99], ['Sibiu', 'Rimnicu Vilcea', 80], ['Fagaras', 'Bucharest', 211]]

    initial_state = 'Arad'
    goal_state = 'Bucharest'

    [solution, cost] = ucs(state_space, initial_state, goal_state)
    print("Solution:", solution)
    print("Path cost:", cost)

    
