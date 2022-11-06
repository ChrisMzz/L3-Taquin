# L3-Taquin

## Introduction

Le but de ce projet est de s'intéresser à la solution au jeu du Taquin, connu aussi sous le nom de *15-puzzle en anglais*.

Celui-ci peut être représenté par un carré de $n \times n$ cases toutes numérotées de $0$ à $n^2 − 1$, et on commence le jeu sur une configuration aléatoire. On considère que la case numérotée $0$ est vide et qu'on peut l'échanger avec ses cases adjacentes à tout moment du jeu. Un échange avec une case sera considéré comme un mouvement et transformera l'état actuel en un de ses états *adjacents*. 
Naturellement, tout état a au plus $4$ états adjacents.

Le but est d'obtenir la configuration où tous les nombres de $1$ à $n^2 − 1$ sont numérotés dans l'ordre (on lit de gauche à droite puis de bas en haut) et où la dernière case est vide.

## Approche naïve

On commence d'abord par essayer de résoudre un jeu à partir d'une configuration aléatoire à l'aide de l'algorithme de Dijkstra.
[Fichier contenant le code qui correspond à cette partie.](https://github.com/ChrisMzz/L3-Taquin/blob/main/source/naif.py)
J'ai implémenté une légère modification du fichier `group.py` qui peut être retrouvé [ici](https://github.com/ChrisMzz/Algebra-modules/blob/main/lib/source/group.py), que j'avais codé dans le but d'étudier certaines propriétés du groupe symmétrique.

### Les limites de l'algorithme

On remarque cependant que l'algorithme de Dijkstra est très peu optimal dans les cas $n >= 3$, car il explore tous les sommets (et il y a $n^2!$ sommets pour un jeu de taille $n$, le nombre d'éléments de $S_{n^2}$). 
On va donc explorer un algorithme plus adapté à cette situation (nombre de sommets très élevé) dans la partie suivante.

## Algorithme IDA*

L'algorithme IDA* explore tous les chemins de chaque longueur de chemin possible, dans l'ordre croissant. Ceci trouve des solutions très rapidement pour des configurations initiales "proches" de la configuration finale (c'est-à-dire qu'il existe un chemin court connectant les deux), mais est assez long pour les configurations dont le chemin le plus court à la solution est de taille maximale.

- [Fichier contenant la classe Taquin utilisée pour représenter un jeu (contient l'algorithme `ida_star()`).](https://github.com/ChrisMzz/L3-Taquin/blob/main/source/taquin.py)
- [Fichier utilisé pour tester des configurations, des cas limites, etc.](https://github.com/ChrisMzz/L3-Taquin/blob/main/source/main.py)
- [`gif`s générés à partir de certaines solutions.](https://github.com/ChrisMzz/L3-Taquin/tree/main/source/images)

C'est majoritairement sur ce modèle que le projet s'appuie.


## Fonctionnalités ajoutées

---

### L'affichage d'une solution (animée ou non) peut être personalisée :

```py
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
...
class Taquin:
    ...
    def display(self, textshow=True, save=False, name="fig"):
        cmap = ListedColormap([[1,1,1]] + [[condition_1, condition_2, condition_3] for i in range(1,self.n**2+1)])
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
```
`cmap` est défini comme une `ListedColormap` d'une liste de valeurs RGB (chacune sous forme de liste `[r,g,b]` nombres compris entre 0 et 1) :
- `[[1,1,1]]` (case vide blanche) et $n^2-1$ valeurs RGB correspondant dans l'ordre aux valeurs $1$ à $n^2$
- j'ai choisi un formattage `[[1,(i-1)/(self.n**2),1-(i-1)/(self.n**2)] for i in range(1,self.n**2+1)]` qui donne un dégradé $\textcolor{magenta}{\text{magenta}}$ - $\textcolor{yellow}{\text{jaune}}$.

`textshow` permet d'afficher les nombres dans les cases si vous avez du mal à repérer les valeurs en ne regardant que les couleurs.

![](https://github.com/ChrisMzz/L3-Taquin/blob/main/source/images/3/(0%2C%203%2C%205%2C%208%2C%206%2C%201%2C%202%2C%207%2C%204)%20-%20pair.gif)


### La solution finale peut être modifiée :

La vérification de solvabilité d'un état a été modifiée pour varier en fonction de la solution finale :

```py
...
class Taquin:
    ...
    def is_solvable(self): # Réutilise le même concept que dans l'approche naïve
        config = list(self.to_tuple())
        empty_index = config.index(0)
        final = list(self.final)
        final_empty_index = final.index(0)
        config.pop(empty_index)
        final.pop(final_empty_index)
        is_same_parity_as_final = ((int(signature(config)==-1) + (self.n - empty_index // self.n)) % 2) == ((int(signature(final)==-1) + (self.n - final_empty_index // self.n)) % 2)
        return is_same_parity_as_final
```

On a donc un nouveau paramètre optionnel dans le constructeur de la classe `Taquin` :

```py
class Taquin:
    def __init__(self, configuration, custom_final=()):
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
```

Avec un nouvel attribut `self.final`, on peut trouver un chemin vers une nouvelle solution avec la même méthode `ida_star()`, grâce à une légère modification de la définition d'`horizon()` : 
```py
class Taquin:
    ...
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
```
Voir le [rapport](https://github.com/ChrisMzz/L3-Taquin/blob/main/Rapport.pdf) pour une démonstration de la validité de ce changement.

*Remarque : on peut désormais trouver une solution à partir d'une configuration impaire si on choisit une configuration finale impaire.*

---

Merci d'avoir tout lu !!
