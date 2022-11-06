import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from copy import deepcopy


def signature(perm): # Importé directement depuis le module group.py
    s = 1
    qlist = list(perm)
    for i in range(1, len(perm)+1):
        while int(qlist[i-1]) != i:
            a = int(qlist[i-1])
            b = int(qlist[a-1])
            qlist[a-1] = str(a)
            qlist[i-1] = str(b)
            s *= -1
    return s


class Taquin:
    def __init__(self, configuration, custom_final=()):
        """Initialiser le jeu

        Args:
            configuration (_type_): Configuration initiale.
            custom_final (tuple, optional): Si précisé, modifie l'état final.
        """
        self.configuration = configuration
        config = self.to_tuple()
        empty_pos = list(config).index(0)
        try :
            self.n = int(np.math.sqrt(len(config)))
        except :
            print("configuration non carrée")
            return
        self.empty_i = empty_pos // self.n
        self.empty_j = empty_pos % self.n
        if len(custom_final) == 0:
            self.final = tuple([i for i in range(1,self.n**2)]+[0])
        else:
            self.final = custom_final
        
    def __str__(self):
        return str(self.configuration) + f"({self.empty_i}, {self.empty_j})"
    
    def to_tuple(self):
        if type(self.configuration) == tuple:
            return self.configuration
        temp = []
        for line in self.configuration:
            temp += list(line)
        return tuple(temp)
    
    def read(self, state):
        config = []
        empty_index = list(state).index(0)
        for line in range(self.n):
            config.append(list(state)[line*self.n:(line+1)*self.n])
        self.configuration = np.array(config)
        self.empty_i = empty_index // self.n
        self.empty_j = empty_index % self.n
        
    # ----------------------------
    def old_horizon(self): # correspond à h dans le rapport rendu avec ce code.
        temp_sum = 0
        n = self.n
        for a in range(1,n**2):
            pos = list(self.to_tuple()).index(a)
            i = pos // n
            j = pos % n
            temp_sum += np.abs(i - np.math.floor((a-1)/n)) + np.abs(j - ((a-1) % n))
        return temp_sum
    # ----------------------------

    def horizon(self):
        """Métrique h' définie dans le rapport rendue avec ce code.
        Ici, on mesure la distance h'(actuel, final).

        Returns:
            int: distance h'(actuel, final) de l'état actuel à l'état final.
        """
        temp_sum = 0
        n = self.n
        for a in range(1,n**2):
            pos = list(self.to_tuple()).index(a)
            other_pos = list(self.final).index(a)
            i = pos // n
            j = pos % n
            other_i = other_pos // n
            other_j = other_pos % n
            temp_sum += np.abs(i - other_i) + np.abs(j - other_j)
        return temp_sum


    def move(self, i,j):
        if (i != self.empty_i and j != self.empty_j) \
            or (i != self.empty_i and (i+1 != self.empty_i and i-1 != self.empty_i)) \
                or (j != self.empty_j and (j+1 != self.empty_j and j-1 != self.empty_j)):
                    print("Ne peut pas déplacer, case non adjacente.")
                    return False
        temp = self.configuration[i][j]
        self.configuration[i][j] = self.configuration[self.empty_i][self.empty_j]
        self.configuration[self.empty_i][self.empty_j] = temp
        self.empty_i = i
        self.empty_j = j
        return True
    
    def up(self):
        self.move(self.empty_i + 1, self.empty_j)
    
    def down(self):
        self.move(self.empty_i - 1, self.empty_j)
    
    def left(self):
        self.move(self.empty_i, self.empty_j + 1)
    
    def right(self):
        self.move(self.empty_i, self.empty_j - 1)
    
    
    def try_up(self):
        return self.empty_i != self.n-1
                  
    def try_down(self):
        return self.empty_i != 0
            
    def try_left(self):
        return self.empty_j != self.n-1
            
    def try_right(self):
        return self.empty_j != 0
    
    def is_solvable(self): # Réutilise le même concept que dans l'approche naïve
        config = list(self.to_tuple())
        empty_index = config.index(0)
        final = list(self.final)
        final_empty_index = final.index(0)
        config.pop(empty_index)
        final.pop(final_empty_index)
        is_same_parity_as_final = ((int(signature(config)==-1) + (self.n - empty_index // self.n)) % 2) == ((int(signature(final)==-1) + (self.n - final_empty_index // self.n)) % 2)
        return is_same_parity_as_final
        
    def display(self, textshow=True, save=False, name="fig"):
        """Afficher la configuarion actuelle à l'aide du module matplotlib.pyplot

        Args:
            textshow (bool, optional): Si les nombres doivent s'afficher dans les carreaux ou pas. True par défaut.
            save (bool, optional): Enregistre l'image dans images/ si True. False par défaut.
            name (str, optional): Le nom du fichier enregistré. "fig" par défaut.
        """
        cmap = ListedColormap([[1,1,1]] + [[1,(i-1)/(self.n**2),1-(i-1)/(self.n**2)] for i in range(1,self.n**2+1)])
        fig, ax = plt.subplots()
        ax.imshow(self.configuration, cmap=cmap)
        if textshow:
            for (i, j), z in np.ndenumerate(self.configuration):
                if str(z)=="0":
                    pass
                ax.text(j, i, z, ha='center', va='center')
        ax.set_axis_off()
        if save:
            fig.savefig(f"images/{name}.png", dpi=300, format="png")
        plt.close(fig)

    def ida_star(self):
        bound = deepcopy(self.horizon())
        configuration = deepcopy(self.to_tuple())
        path = [configuration]
        stack = [[path, 0, bound]]
        mini = 0
        while mini < np.inf:
            mini = np.inf
            while len(stack) > 0:
                last_path, g, last_bound = stack[-1]
                #print(last_path, g, last_bound)
                #print(last_path)
                stack.pop(-1)
                self.read(last_path[-1])
                #print(self)
                f = g + self.horizon()
                if self.horizon() == 0:
                    return (last_path, last_bound)
                elif f > last_bound:
                    if f < mini:
                        mini = f
                else:
                    if self.try_up():
                        #print("up")
                        self.up()
                        current = deepcopy(self.to_tuple())
                        if current not in last_path:
                            stack.append([last_path + [current], g+1, last_bound])
                        self.down()
                    if self.try_down():
                        #print("down")
                        self.down()
                        current = deepcopy(self.to_tuple())
                        if current not in last_path:
                            stack.append([last_path + [current], g+1, last_bound])
                        self.up()
                    if self.try_right():
                        #print("right")
                        self.right()
                        current = deepcopy(self.to_tuple())
                        if current not in last_path:
                            stack.append([last_path + [current], g+1, last_bound])
                        self.left()
                    if self.try_left():
                        #print("left")
                        self.left()
                        current = deepcopy(self.to_tuple())
                        if current not in last_path:
                            stack.append([last_path + [current], g+1, last_bound])
                        self.right()
            if mini < np.inf:
                stack.append([path, 0, mini])
        return None
                    
                
            
    
    
    