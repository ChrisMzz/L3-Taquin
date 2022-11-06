#%%
import shutil
from taquin import *
import numpy as np
import os
from PIL import Image
import time
import matplotlib

matplotlib.use('Agg')
t = time.time()
n = 3



def randomize(config, iter): # cette fonction a été créée pour vérifier que la parité était bien calculée.
    """Déplacer le 0 aléatoirement dans une configuration pour en obtenir une autre, conservant la parité de la configuration donnée.
        random_config (list): la configuration donnée
        iter (int): nombre de fois qu'on déplace le 0 (non trivialement, c'est-à-dire qu'on ne déplace pas vers la gauche et la droite consécutivement par exemple)

    Returns:
        tuple: `(puzzle, list(puzzle.to_tuple()))` où puzzle est le jeu du Taquin initialisée sur la nouvelle configuration.
    """
    i, previous = 0, 5
    puzzle = Taquin(make_initial(config))
    while i <= iter:
        dir = np.random.randint(0,4)
        if dir == 0 and previous != 0 and puzzle.try_up():
            puzzle.up()
            i += 1
        elif dir == 1 and previous != 1 and puzzle.try_down():
            puzzle.down()
            i += 1
        if dir == 2 and previous != 2 and puzzle.try_left():
            puzzle.left()
            i += 1
        elif dir == 3 and previous != 3 and puzzle.try_right():
            puzzle.right()
            i += 1
        previous = dir
    return puzzle, list(puzzle.to_tuple())
        
        

def make_initial(initial_config, random=False):
    """Créer l'array nécessaire pour initialiser Taquin à partir d'une liste initial_config.

    Args:
        initial_config (list): Configuration donnée.
        random (bool, optional): Si on veut rendre la configuration aléatoire. Utile pour comparer la validité du test de parité. Déconseillé pour n>3

    Returns:
        ndarray: tableau représentant la configuration initiale obtenue.
    """
    if random:
        np.random.shuffle(initial_config)
    initial_state = []
    for line in range(n):
        initial_state.append(initial_config[line*n:(line+1)*n])
    initial_state = np.array(initial_state)
    return initial_state










random_config = [0, 3, 5, 8, 6, 1, 2, 7, 4]
initial_state = make_initial(random_config)
puzzle = Taquin(initial_state)

# Pour tester un état final pair différent
#puzzle = Taquin(initial_state, (1,2,3,4,5,6,7,0,8))

# État initial et final tous deux impairs, pour tester compatibilité des parités
#random_config = [0, 5, 3, 8, 6, 1, 2, 7, 4]
#puzzle = Taquin(make_initial(random_config), (1,2,3,4,5,6,8,7,0))



# Pour pouvoir tester les jeux n >= 4 sans attendre 40 ans pour une solution
#random_config = [i for i in range(1,n**2)] + [0]
#puzzle, random_config = randomize(random_config, 300)


if not puzzle.is_solvable():
    while not puzzle.is_solvable():
        puzzle = Taquin(make_initial(random_config))
        #puzzle = Taquin(make_initial(random_config), (1,2,3,4,5,6,8,7,0))


print(puzzle)
print(puzzle.final)
print(puzzle.is_solvable())


# Pour sauvegarder un gif de la résolution :
save = True
# Penser à bien créer les dossiers "images/{n}" dans le répertoire actif avant d'utiliser.



if puzzle.is_solvable():
    dirname = puzzle.horizon()
    sol = puzzle.ida_star()
    print(f"Fini en {time.time() - t}s")
    if n <= 5:
        dirname = tuple(random_config)
    print(f"Il faut minimum {sol[1]} coups pour résoudre le puzzle à partir de l'état {dirname}.\n \
        Un des chemins les plus courts est {sol[0]}.")
    if not os.path.isdir(f"images/{n}/{dirname}") and save:
        os.mkdir(f"images/{n}/{dirname}")
        gif = []
        for move in range(len(sol[0])):
            puzzle.read(sol[0][move])
            puzzle.display(True, True, f"{n}/{dirname}/{move}")
            gif.append(Image.open(f"images/{n}/{dirname}/{move}.png"))
        gif[0].save(f'images/{n}/{dirname}.gif', save_all=True, optimize=False, append_images=gif[1:])
        shutil.rmtree(f"images/{n}/{dirname}")
else:
    print(f"En partant de {puzzle.to_tuple()}, le puzzle est impossible à résoudre.")





# %%
