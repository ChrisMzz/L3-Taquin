import numpy as np
from graph import *
#À l'aide de mon module group (que j'ai modifié dans ce projet) disponible sur 
#https://github.com/ChrisMzz/Algebra-modules
from group import *

n = 2


def build_graph(n, p=0):
    adjency = {}
    parity = {}
    S = SymmetricGroup(n**2-1) 
    for i in range(n):
        for j in range(n):
            for sigma in S:
                node = tuple(sigma[:n*i+j] + [0] + sigma[n*i+j:])
                verteces = []
                state = sigma[:n*i+j] + [0] + sigma[n*i+j:]
                if n*i+j+1 < n**2 and ((j+1) // n) == (j // n): #Case droite
                    verteces.append(tuple(sigma[:n*i+j+1] + [0] + sigma[n*i+j+1:])) # conserves sigma's signature
                if n*i+j-1 > 0 and ((j-1) // n) == (j // n) : #Case gauche
                    verteces.append(tuple(sigma[:n*i+j-1] + [0] + sigma[n*i+j-1:])) # conserves sigma's signature
                if n*(i-1)+j >= 0: #Case supérieure
                    swapped = state[n*(i-1)+j]
                    state[n*(i-1)+j], state[n*i+j] = 0, swapped  
                    verteces.append(tuple(state))
                if n*(i+1)+j < n**2: #Case inférieure
                    swapped = state[n*(i+1)+j]
                    state[n*(i+1)+j], state[n*i+j] = 0, swapped                
                    verteces.append(tuple(state))
                parity[node] = (int(S.signature(sigma)==1) + i) % 2
                # using Keith Conrad's study in his paper on the 15-puzzle, we know it's isomorphic to A15, so we can abuse 
                # shortcut formulas such as this one to find sigma's parity
                adjency[node] = verteces
    puzzle = MyGraph()
    for node in adjency.keys():
        for connected_node in adjency[node]:
            puzzle.add_arc((node, connected_node))
    return (puzzle, parity)[p]

def solve(source):
    global n
    puzzle = build_graph(n)
    paths_from_source = dijkstra(puzzle,source)
    parent = tuple([i for i in range(1,n**2)] + [0])
    dist_from_source = paths_from_source[0][parent]
    path = []
    if parent == source:
        print("État initial est déjà final.")
    elif parent not in paths_from_source[1]:
        print(f"Pas de solution si l'état initial est {source}. Distance mininmale : {dist_from_source}")
        return False
    else :
        while paths_from_source[1][parent] in paths_from_source[1]:
            path.append(paths_from_source[1][parent])
            parent = paths_from_source[1][parent]
        path.append(source)
        path.reverse()
        path.append(tuple([i for i in range(1,n**2)] + [0]))
    print(f"Distance minimale de {source} à l'état final : {dist_from_source}")
    print(f"Chemin : {path}")
    return dist_from_source, path


source = [i for i in range(n**2)]
np.random.shuffle(source)
source = tuple(source)


source_parity = ("pair", "impair")[build_graph(n,1)[source]]
print(f"{source} est un état {source_parity}.")
solve(source)
