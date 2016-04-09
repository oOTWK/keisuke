from random import choice, random
from cspbase import *


def create_keisuke_puzzle_hard(n, m):
    possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    game_board = []
    for i in range(1,n+1):
        game_board.append([])
        for j in range(1,n+1):
            if i % (m+1) == 0 or j % (m+1) == 0:
                game_board[i-1].append(-1)
            else:
                game_board[i-1].append(choice(possible_values))
    horizontal = []
    vertical = []

    for row in game_board:
        temp = ()
        for item in row:
            if item == -1:
                if temp != () and len(temp) > 1:
                    horizontal.append(temp)
                temp = ()
            else:
                temp += (item,)
        if temp != () and len(temp) > 1:
            horizontal.append(temp)

    for i in range(n):
        temp = ()
        for row in game_board:
            if row[i] == -1:
                if temp != () and len(temp) > 1:
                    vertical.append(temp)
                temp = ()
            else:
                temp += (row[i],)
        if temp != () and len(temp) > 1:
            vertical.append(temp)

    final_board = [[item if item == -1 else 0 for item in row] for row in game_board]

    return final_board, horizontal, vertical


def create_keisuke_puzzle(n):
    '''
    Creates a randomly valid keisuke puzzle that is of dimension n x n.
    Will return a list representation of the puzzle along with a horizontal and vertical list of numeric values.
    '''

    possible_values = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    game_board = [[choice(possible_values) for x in range (n)] for y in range(n)]

    horizontal = []
    vertical = []

    for row in game_board:
        temp = ()
        for item in row:
            if item == -1:
                if temp != () and len(temp) > 1:
                    horizontal.append(temp)
                temp = ()
            else:
                temp += (item,)
        if temp != () and len(temp) > 1:
            horizontal.append(temp)

    for i in range(n):
        temp = ()
        for row in game_board:
            if row[i] == -1:
                if temp != () and len(temp) > 1:
                    vertical.append(temp)
                temp = ()
            else:
                temp += (row[i],)
        if temp != () and len(temp) > 1:
            vertical.append(temp)

    final_board = [[item if item == -1 else 0 for item in row] for row in game_board]

    return final_board, horizontal, vertical

def create_keisuke_puzzle_2(n):
    '''
    Creates a randomly valid keisuke puzzle that is of dimension n x n.
    Will return a list representation of the puzzle along with the list of numeric values.

    Possible version where we adjust the occurrence of black squares.
    '''

    quarter = n / 4
    percent = quarter / n
    possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    game_board = [[choice(possible_values) if random() >= percent else -1 for x in range (n)] for y in range(n)]

    horizontal = []
    vertical = []

    for row in game_board:
        temp = ()
        for item in row:
            if item == -1:
                if temp != () and len(temp) > 1:
                    horizontal.append(temp)
                temp = ()
            else:
                temp += (item,)
        if temp != () and len(temp) > 1:
            horizontal.append(temp)

    for i in range(n):
        temp = ()
        for row in game_board:
            if row[i] == -1:
                if temp != () and len(temp) > 1:
                    vertical.append(temp)
                temp = ()
            else:
                temp += (row[i],)
        if temp != () and len(temp) > 1:
            vertical.append(temp)

    final_board = [[item if item == -1 else 0 for item in row] for row in game_board]

    return final_board, horizontal, vertical



def keisuke_csp_model_1(initial_keisuke_board, horizontal, vertical):
    csp = CSP("Keiuske_M1")
    n = len(initial_keisuke_board)
    variables = []
    
    # separate constraints in length
    horizontal_by_length = [[] for i in range(n+1)];
    for i in range(len(horizontal)):
        horizontal_by_length[len(horizontal[i])].append(horizontal[i])
    
    vertical_by_length = [[] for i in range(n+1)];
    for i in range(len(vertical)):
        vertical_by_length[len(vertical[i])].append(vertical[i])
    
    
    # create domain
    domain = set()
    for i in range(len(horizontal)):
        domain = domain.union(set(horizontal[i]))
    for i in range(len(vertical)):
        domain = domain.union(set(vertical[i]))

    # create variables
    for i in range(n):
        variables.append([])
        for j in range(n):
            var = Variable("V{},{}".format(i,j))
            if initial_keisuke_board[i][j] == 0:
                var.add_domain_values(domain)
            else:
                var.add_domain_values([-1])
            variables[i].append(var)
            csp.add_var(var)
                
                
    # create constraints
    
    horizontal_cons = []
    vertical_cons = []
    
    # create row constraints
    for i in range(n):
        first_white_slot = 0
        for j in range(n):
            if (j == 0 and initial_keisuke_board[i][j] == -1):
                first_white_slot = 1
            if ((j == n-1 and initial_keisuke_board[i][j] != -1)
            or (j != n-1 and initial_keisuke_board[i][j+1] == -1)):
                length = j - first_white_slot + 1
                if length > 1:
                    con = Constraint("H", [variables[i][k] for k in range(first_white_slot, j+1)])

                    con.add_satisfying_tuples(horizontal_by_length[length])
                    csp.add_constraint(con)
                    horizontal_cons.append(con)
                        
                first_white_slot = j+2


    # create column constraints
    for i in range(n):
        first_white_slot = 0
        for j in range(n):

            if (j == 0 and initial_keisuke_board[j][i] == -1):
                first_white_slot = 1
            if ((j == n-1 and initial_keisuke_board[j][i] != -1)
            or (j != n-1 and initial_keisuke_board[j+1][i] == -1)):
                length = j - first_white_slot + 1
                if length > 1:
                    con = Constraint("C", [variables[k][i] for k in range(first_white_slot, j+1)])

                    con.add_satisfying_tuples(vertical_by_length[length])
                    csp.add_constraint(con)
                    vertical_cons.append(con)
                        
                first_white_slot = j+2

    # create diff constraints
    # separate by length
    horizontal_cons_length = [[] for i in range(n+1)]
    for i in range(len(horizontal_cons)):
        horizontal_cons_length[len(horizontal_cons[i].get_scope())].append(horizontal_cons[i])
        
    vertical_cons_length = [[] for i in range(n+1)]
    for i in range(len(vertical_cons)):
        vertical_cons_length[len(vertical_cons[i].get_scope())].append(vertical_cons[i])   
        
    
    # create binary difference between two same length horizontal
    for i in range(2, len(horizontal_cons_length)):
        same_length_cons = horizontal_cons_length[i]
        
        for j in range(len(same_length_cons)):
            for k in range(j+1, len(same_length_cons)):
                con = Constraint("H-diff",
                                 same_length_cons[j].get_scope() + same_length_cons[k].get_scope())
                
                # create a list of satisfiable tuples
                sat_tuple = []
                for l in range(len(horizontal_by_length[i])):
                    for m in range(len(horizontal_by_length[i])):
                        if (l != m):
                            sat_tuple.append(horizontal_by_length[i][l] + horizontal_by_length[i][m])

                con.add_satisfying_tuples(sat_tuple)
                csp.add_constraint(con)
        
    # create binary difference between two same length vertical
    for i in range(2, len(vertical_cons_length)):
        same_length_cons = vertical_cons_length[i]
        
        for j in range(len(same_length_cons)):
            for k in range(j+1, len(same_length_cons)):
                con = Constraint("V-diff",
                                 same_length_cons[j].get_scope() + same_length_cons[k].get_scope())
                
                # create a list of satisfiable tuples
                sat_tuple = []
                for l in range(len(vertical_by_length[i])):
                    for m in range(len(vertical_by_length[i])):
                        if (l != m):
                            sat_tuple.append(vertical_by_length[i][l] + vertical_by_length[i][m])

                con.add_satisfying_tuples(sat_tuple)
                csp.add_constraint(con)
                
    return (csp, variables)
                  

def print_sudo_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])


def print_sudo(var_array):
    for row in var_array:
        print([var for var in row])
