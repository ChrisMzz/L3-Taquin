import numpy as np
from graph import *
#À l'aide de mon module group (que j'ai modifié dans ce projet) disponible sur 
#https://github.com/ChrisMzz/Algebra-modules
from group import *

n = 3

def build_graph(n, p=0):
    adjacency = {}
    parity = {}
    S = SymmetricGroup(n**2-1) 
    for i in range(n):
        for j in range(n):
            for sigma in S:
                node = tuple(sigma[:n*i+j] + [0] + sigma[n*i+j:])
                verteces = []
                state = sigma[:n*i+j] + [0] + sigma[n*i+j:]
                if n*i+j+1 < n**2 and ((j+1) // n) == (j // n): #Case droite
                    verteces.append(tuple(sigma[:n*i+j+1] + [0] + sigma[n*i+j+1:])) # conserve la signature de sigma
                if n*i+j-1 >= 0 and ((j-1) // n) == (j // n) : #Case gauche
                    verteces.append(tuple(sigma[:n*i+j-1] + [0] + sigma[n*i+j-1:])) # conserve la signature de sigma
                if n*(i-1)+j >= 0: #Case supérieure
                    swapped = state[n*(i-1)+j]
                    state[n*(i-1)+j], state[n*i+j] = 0, swapped
                    verteces.append(tuple(state))
                    state[n*(i-1)+j], state[n*i+j] = swapped, 0
                if n*(i+1)+j < n**2: #Case inférieure
                    swapped = state[n*(i+1)+j]
                    state[n*(i+1)+j], state[n*i+j] = 0, swapped                
                    verteces.append(tuple(state))
                parity[node] = (int(S.signature(sigma)==1) + (n-i)) % 2
                # Les deux opérations ci-dessus (cases supérieure et inférieure) changent la parité de sigma, ce qui nous permet donc d'associer :
                    # Une permutation sigma de signature 1 et dont la position du 0 est sur la dernière ligne (ou un indice = dernière ligne mod 2)
                    # engendre un état pair. Si la position du 0 est sur une des autres lignes, l'état est impair.
                    # Inversement, une permutation sigma de signature -1 et dont la position du 0 est sur la dernière ligne (ou un indice = dernière ligne mod 2)
                    # engendre un état impair. Si la position du 0 est sur une des autres lignes, l'état est pair.
                # J'utilise des notions abordées par Keith Conrad dans son étude du "15-puzzle"
                # qui engendre des raccourcis mathématiques sur la parité d'un élément.
                adjacency[node] = verteces
    puzzle = MyGraph()
    for node in adjacency.keys():
        for connected_node in adjacency[node]:
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
t = time.time()
print(f"{source} est un état {source_parity}.")
solve(source)
print(f"Fini en {time.time() - t} secondes.")