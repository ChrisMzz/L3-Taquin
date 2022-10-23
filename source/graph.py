import math
import time


class MyGraph:
  def __init__(self):
    self.adjacency = {} #on représente le graphe avec un dictionnaire dont les clefs sont les noeuds du graphes, et les valeurs des ensembles de noeuds ver lesquels pointe le noeud.
    self.weights = {} #les poids des arcs sont stockés dans un dictionnaire
    
  def __str__(self):
    return "adjacency : " + str(self.adjacency) + ", weights : " + str(self.weights)

  def add_node(self, s):
    if s in self.adjacency:
      return
    self.adjacency[s] = set() #on initialise la liste d'adjacence des avec un ensemble vide

  def add_arc(self, arc, weight = 1):
    s1, s2 = arc
    self.add_node(s1)
    self.add_node(s2)
    self.weights[arc] = weight
    if s2 not in self.adjacency[s1]:
      self.adjacency[s1].add(s2)
    
  def remove_arc(self, arc):
    if arc not in set.weights:
      return
    del self.weights[arc]
    s1, s2 = arc
    self.adjacency[s1].remove(s2)
    
  def remove_node(self, node): #il faut d'abord retirer tous les arcs pointant sur le noeud, tous les arc partant du noeuds, puis supprimer le noeud
    if node not in self.adjacency:
      return
    for other in self.adjancency:
      self.remove_arc( (node, other) )
      self.remove_arc( (other, node) )
    del self.adjancency[node]
      
  def nodes(self):
    return set(self.adjacency)#on convertit les clefs du dictionnaire en un ensemble 
    
  def successors(self, node):
    return set(self.adjacency[node])
    
  def predecessors(self, node):
    return set(s for s in self.adjacency if s in self.adjacency[node])
    
  def arc_weight(self, arc):
    return self.weights[arc]



def extract_min(F, distances): 
    min_dst = math.inf # la plus petite distance trouvée jusqu'à présent
    min_s = None  # le sommet associé à cette plus petite distance
    for s in F: # on parcourt tous les sommets de la file F
        if distances[s] <= min_dst: # si s a une plus petite distance que tout ceux vu jusqu'à présent, c'est lui qui devient le nouveau min_s
            min_s = s 
            min_dst = distances[s]
    F.remove(min_s) # on retire le plus petite sommet qu'on a trouvé de la file F
    return min_s 

def dijkstra(graph, 
             source):
  distances = {} #on initialise distances et parents avec des dictionnaires vides
  parents = {}
  F = graph.nodes() #F est l'ensemble des noeuds du graphe
 
  for u in graph.nodes():
    distances[u] = math.inf #on initialise les distances à l'infini
    
  distances[source] = 0 #on initialise la distance du point d'origine à 0
  t = time.time()
  while len(F) > 0 : 
    
    if len(F) % 100 == 0 :
        print(len(F),time.time() - t)
        t = time.time()
    u = extract_min(F, distances)
    for v in graph.successors(u):
      if distances[v] > distances[u] + graph.arc_weight( (u, v) ):
        #print("d[" + str(v) + "] <- d[" + str(u) + "] + w(" + str(u) + ", " + str(v) + ")")
        #print(distances[v], distances[u], graph.arc_weight( (u, v) ))
        distances[v] = distances[u] + graph.arc_weight( (u, v) )
        parents[v] = u
        
  return distances, parents