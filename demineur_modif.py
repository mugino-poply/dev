"""
Auteur: Hippolyte Amory
"""

import random
import sys
import re

def validate_arguments(func):
    """
    S'assure que des données incorrectes ne sont pas transmises par accident lors d'appels internes
    """
    def wrapper(*args, **kwargs):
        if len(args) >= 2:
            if not all(map(lambda x: isinstance(x, int), args[:2])):
                raise TypeError("Les dimensions du plateau doivent être des entiers.")
        return func(*args, **kwargs)
    return wrapper


def safe_execution(func):
    """
    Ajoute une gestion globale des exceptions dans une fonction
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Erreur dans {func.__name__}: {e}")
    return wrapper


@validate_arguments
@safe_execution
def create_board(n:int, m:int, carac=". "):
    """
    Construit un tableau de taille n x m
    Paramètres : 
        n (int): nombre de colonnes
        m (int): nombre de lignes
    Returns :
        (List[list[str]]): plateau de jeu 
    """
    
    BOARD = [[carac]*n for i in range(m)]  # Par défaut game_board
    return BOARD

@safe_execution
def print_board(board : list[list[str]]):
    """
    Affiche le tableau
    Paramètres :
        board (List[list[str]]): plateau de jeu
    """

    TAILLE = get_size(board)
    if TAILLE[0] <= 10 >= TAILLE[1]: # Si taille inférieure à 10*10
        print("  ", end=" ")
        for i in range(TAILLE[0]):
            print(str(i)+" ", end = " ")
        print()
        print(" ", end=" ")
        for j in range((TAILLE[0]-(TAILLE[0]//2))*2):
            print("--", end ="-")
        print()
        for k in range(TAILLE[1]):
            elem = str(k) + " |"
            for l in range(TAILLE[0]):
                elem += str(board[k][l]) + " "
            print(elem + "|")
        print(" ", end=" ")
        for j in range((TAILLE[0]-(TAILLE[0]//2))*2):
            print("--", end ="-")
    else:   # Si taille supérieure à 10*10
        n = str(TAILLE[0])
        unite = int(n[1])  # Chiffre des unites
        dizaine = int(n[0])  # Chiffre des dizaines
        print("   "*10, end="    ")
        for d in range(1, dizaine+1):
            if d == dizaine:  # Dernière dizaine
                print((str(d)+"  ")*unite, end='')
            else:
                print((str(d)+"  ")*10, end = "")
        print()
        print("   ", end=" ")
        i = 0
        v = i
        while v < TAILLE[0]:
            print(str(i)+" ", end = " ")
            v += 1
            i += 1
            if i == 10:
                i -= 10
        print()
        print("   ", end=" ")
        for j in range((TAILLE[0]-(TAILLE[0]//2))*2):
            print("--", end ="-")
        print()
        for k in range(TAILLE[1]):
            if k < 10:
                elem = " " +str(k) + " |"
            else:
                elem = str(k) + " |"
            for l in range(TAILLE[0]):
                elem += str(board[k][l]) + " "
            print(elem + "|")
        print("   ", end=" ")
        for j in range((TAILLE[0]-(TAILLE[0]//2))*2):
            print("--", end ="-")
        
@safe_execution
def get_size(board: list[list[str]]):
    """
    Renvoie un tuple correspondant à la taille du tableau.
    Paramètres:
        board (list[list[str]]): plateau de jeu
    Returns:
        Tuple(int, int): (nombre de colonnes, nombre de lignes)
    """
    return (len(board[0]), len(board))

def get_neighbors(board : list[list[str]], pos_x:int, pos_y:int):
    """
    Renvoie une liste de cases (tuples) voisines à la case actuelle
    Paramètres:
        board (List[list[str]]): plateau de jeu
        pos_x (int): position actuelle en x
        pos_y (int): position actuelle en y
    Returns:
        List[tuples]: coordonnées des cases voisines
    """
    m = len(board)-1
    n = len(board[0])-1
    if pos_x == 0:  # Première ligne
        if pos_y == 0:  # Coin supérieur gauche
            tuples = [(0,1), (1,0), (1,1)]
        elif pos_y == n:  # Coin supérieur droit
            tuples = [(0, n-1), (1, n), (1, n-1)]
        else:
            tuples = [(0, pos_y-1), (1, pos_y-1), (1, pos_y), (1, pos_y+1), (0, pos_y+1)]
    elif pos_y == 0:  # Première colonne
        if pos_x == m:  # Coin inférieur gauche
            tuples = [(m-1, 0), (m-1, 1), (m, 1)]
        else:
            tuples = [(pos_x-1, 0), (pos_x-1, 1), (pos_x, 1), (pos_x+1, 1), (pos_x+1, 0)]
    elif pos_x == m:  # Dernière ligne
        if pos_y == n:  # Coin inférieur droit
            tuples = [(m-1, n), (m-1, n-1), (m, n-1)]
        else:
            tuples = [(m, pos_y-1), (m-1, pos_y-1), (m-1, pos_y), (m-1, pos_y+1), (m, pos_y+1)]
    elif pos_y == n:  # Dernière colonne
        tuples = [(pos_x-1, n), (pos_x-1, n-1), (pos_x, n-1), (pos_x+1, n-1), (pos_x+1, n)]
    else: 
        tuples = [(pos_x-1, pos_y-1), (pos_x-1, pos_y), (pos_x-1, pos_y+1), (pos_x, pos_y-1), (pos_x, pos_y+1), (pos_x+1, pos_y-1), (pos_x+1, pos_y), (pos_x+1, pos_y+1)]
    return tuples


def place_mines(reference_board : list[list[str]], nbr_mines:int, first_pos_x:int, first_pos_y:int):
    """
    Place des mines aléatoirement sur le plateau après le 1er tour
    Paramètres:
        reference_board (List[list[str]]): plateau de reference
        nbr_mines (int): nombre de mines
        first_pos_x (int): position en x du premier coup
        first_pos_y (int): position en y du premier coup
    Returns:
        List[tuples] : liste des mines
    """
    
    SANS_MINES = get_neighbors(reference_board, first_pos_x, first_pos_y)  # Voisins de la première case
    SANS_MINES.append((first_pos_x, first_pos_y))
    TAILLE = get_size(reference_board)
    NBR_LIGNES = TAILLE[1]
    NBR_COLONNES = TAILLE[0]

    def mine_positions():
        """
        Générateur de mines
        """
        while True:
            x = random.randint(0, NBR_LIGNES - 1)
            y = random.randint(0, NBR_COLONNES - 1)
            if (x, y) not in SANS_MINES and reference_board[x][y] != 'X ':
                yield (x, y)

    mines = []
    for x, y in mine_positions():
        if len(mines) == nbr_mines:
            break
        mines.append((x, y))
        reference_board[x][y] = 'X '  # Placement de la mine dans le plateau de reference

    return mines

def fill_in_board(reference_board : list[list[str]]):
    """
    Calcul du nombre de mines présentes dans le voisinage de chaque case
    Paramètres:
        reference_board (List[list[str]]): plateau de reference
    """
    for i in range(len(reference_board)):  # i == n° de ligne
        for j in range(len(reference_board[0])):  # j == n° de colonne
            if reference_board[i][j] == 'X ':
                vois = get_neighbors(reference_board, i, j)
                for case in vois:  # case est une case voisine à la case actuelle à chaque itération
                    if reference_board[case[0]][case[1]] != 'X ':
                        reference_board[case[0]][case[1]] += 1
    

def propagate_click(game_board : list[list[str]], reference_board : list[list[str]], pos_x:int, pos_y:int):
    """
    Dévoile toutes les cases adjacentes à celle sur laquelle on a cliqué par itération.
    Paramètres:
        game_board (List[list[str]]): plateau de jeu
        reference_board (List[list[str]]): plateau de reference
        pos_x (int): position en x de la case actuelle
        pos_y (int): position en y de la case actuelle
    """

    def neighbors_to_explore(x, y):
        """
        Générateur utilisé pour gérer les cases à explorer
        """
        for nx, ny in get_neighbors(reference_board, x, y):
            if game_board[nx][ny] == '. ':
                yield nx, ny

    stack = [(pos_x, pos_y)]

    while stack:
        cx, cy = stack.pop()
        if game_board[cx][cy] != '. ':
            continue

        if reference_board[cx][cy] == 'X ':
            continue

        if reference_board[cx][cy] == 0:
            game_board[cx][cy] = "0 "
            stack.extend(neighbors_to_explore(cx, cy))
        elif reference_board[cx][cy] > 0:
            game_board[cx][cy] = f"{reference_board[cx][cy]} "

    return


def parse_input(n:int, m:int):
    """
    Permet au joueur de dévoiler une case ou mettre un drapeau
    Paramètres:
        n (int): nombre de colonnes
        m (int): nombre de lignes
    Returns:
        ret (lst[str, int, int]): action à effectuer + coordonnées de la case
    """
    while True:
        tour = input("Action et case souhaitées (format : [action] [ligne] [colonne]): ")
        match = re.match(r"^(f|\.|d|c)\s+(\d+)\s+(\d+)$", tour)
        if not match:
            print("Entrée invalide. Format attendu : [action] [ligne] [colonne]")
            continue
        action, ligne, colonne = match.groups()
        ligne, colonne = int(ligne), int(colonne)
        if 0 <= ligne < m and 0 <= colonne < n:
            return [action, ligne, colonne]
        else:
            print("Coordonnées hors limites. Réessayez.")
    ret = [action, ligne, colonne]
    return ret


def check_win(game_board : list[list[str]], reference_board : list[list[str]], mines_list : list[tuple[int, int]], total_flags:int):
    """
    Renvoie True si le joueur a gagné, False sinon
    Paramètres:
        game_board (List[list[str]]): plateau de jeu
        reference_board (List[list[str]]): plateau de reference
        mines_list (List[tuple[int, int]]): liste des coordonnées des mines
        total_flags (int): nombre de flags biens positionnés
    Returns:
        bool: True si gagné, False si toujours pas
    """
    r = '\033[91m'  # rouge
    b = '\033[0m'  # normal (blanc)
    if total_flags == len(mines_list):
        return True
    nbr_mines_sans_flag = len(mines_list) - total_flags  # mines pas recouvertes d'un flag
    hide_case = 0  # nombre de cases pas encore dévoilées
    for i in range(len(game_board)):  # i == n° de ligne
        for j in range(len(game_board[0])):  # j == n° de colonne
            if game_board[i][j] == r+'X'+b+" ":
                return False
            if game_board[i][j] == '. ':
                hide_case+=1
    if hide_case == nbr_mines_sans_flag:
        return True
    return False
    


def init_game(n:int, m:int, nbr_mines:int):
    """
    Initialise le jeu
    Paramètres:
        n (int): nombre de colonnes
        m (int): nombre de lignes
        nbr_mines (int): nombre de mines
    Returns:
        Tuple[List[list[str]]: game_board (plateau de jeu), List[list[str]]: reference_board (plateau de reference), List[tuple(int, int)]: LST_MINES (liste des mines)]
    """
    game_board = create_board(n, m)
    reference_board = create_board(n, m, 0)
    print_board(game_board)
    print()
    while True:
        prem_tour = input("Première case (format : [action] [ligne] [colonne]): ")
        match = re.match(r"^c\s+(\d+)\s+(\d+)$", prem_tour, re.IGNORECASE)
        if match:
            prem_ligne, prem_colonne = map(int, match.groups())
            if 0 <= prem_ligne < m and 0 <= prem_colonne < n:
                break
            else:
                print("Coordonnées hors limites. Réessayez.")
        else:
            print("Format invalide. Réessayez.")
    
    LST_MINES = place_mines(reference_board, nbr_mines, prem_ligne, prem_colonne)
    fill_in_board(reference_board)
    propagate_click(game_board, reference_board, prem_ligne, prem_colonne)
    print_board(game_board)
    print()
    return game_board, reference_board, LST_MINES


def main():
    """
    Fonction principale du programme, grâce à laquelle on peut jouer
    """
    n = int(sys.argv[1])  # Nombre de colonnes
    m = int(sys.argv[2])  # Nombre de lignes
    nbr_mines = int(sys.argv[3])  # Nombre de mines
    TOUR1 = init_game(n, m, nbr_mines)
    game_board = TOUR1[0]
    reference_board = TOUR1[1]
    LST_MINES = TOUR1[2]
    right_flags = 0  # Nombre de flags bien positionnés
    r = '\033[91m'  # rouge
    b = '\033[0m'  # normal (blanc)
    g = '\033[92m'  # vert
    while not check_win(game_board, reference_board, LST_MINES, right_flags):  # Tant qu'une des conditions de victoire n'est pas remplie
        tour = parse_input(n, m)  # Coup du joueur
        if tour[0] == 'f':  # Action souhaitée: placer un flag
            game_board[tour[1]][tour[2]] = g+'F'+b+" "
            if reference_board[tour[1]][tour[2]] == 'X ':  # Si flag sur une mine
                right_flags += 1
        elif tour[0] == '.':  # Action souhaitée: enlever un flag
            if game_board[tour[1]][tour[2]] == g+'F'+b+" ":  # Si flag sur la case
                game_board[tour[1]][tour[2]] = '. '
        else:  # Action souhaitée: dévoiler une case
            if (tour[1], tour[2]) in LST_MINES:  # Si la case est une mine
                game_board[tour[1]][tour[2]] = r+'X'+b+" "  # Place la bombe (X) sur le plateau de jeu
                break  # Condition de défaite remplie: sortie de la boucle while
            propagate_click(game_board, reference_board, tour[1], tour[2])  # Si la case n'est pas une mine, on dévoile les cases adjacentes
        print_board(game_board)
        print()
    if check_win(game_board, reference_board, LST_MINES, right_flags):  # Si gagné
        print(g+'Bravo ! Vous avez trouvé toutes les mines'+b)
        return 1
    else:  # Si perdu
        print_board(game_board)
        print()
        print(r+'BOUM ! Perdu'+b)
        return 0


if __name__ == '__main__':
    main()