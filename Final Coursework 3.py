"""
Created on Wed Dec 13 10:15:15 2023

@author: HP
"""

"""
MATH20621 - Coursework 3
Student name: Tianchen Yang
Student id:   10777419
Student mail: tianchen.yang@student.manchester.ac.uk

Do not change any part of this string except to replace
the <tags> with your name, id and university email address.
"""

def request_location(question_str):
    """
    Prompt the user for a board location, and return that location.
    
    Takes a string parameter, which is displayed to the user as a prompt.
    
    Raises ValueError if input is not a valid integer, 
    or RuntimeError if the location typed is not in the valid range.
    
    *************************************************************
    DO NOT change this function in any way
    You MUST use this function for ALL user input in your program
    *************************************************************
    """
    loc = int(input(question_str))
    if loc<0 or loc>=24:
        raise RuntimeError("Not a valid location")
    return loc


def draw_board(g):
    """
    Display the board corresponding to the board state g to console.
    Also displays the numbering for each point on the board, and the
    number of counters left in each players hand, if any.
    A reference to remind players of the number of each point is also displayed.
    
    You may use this function in your program to display the board
    to the user, but you may also use your own similar function, or
    improve this one, to customise the display of the game as you choose
    """
    def colored(r, g, b, text):
        """
        Spyder supports coloured text! This function creates coloured
        version of the text 'text' that can be printed to the console.
        The colour is specified with red (r), green (g), blue (b) components,
        each of which has a range 0-255.
        """
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def piece_char(i):
        """
        Return the (coloured) character corresponding to player i's counter,
        or a + to indicate an unoccupied point
        """
        if i==0:
            return colored(100,100,100,'+')
        elif i==1:
            return colored(255,60,60,'X')
        elif i==2:
            return colored(60,120,255,'O')

        
    board = '''
x--------x--------x  0--------1--------2 
|        |        |  |        |        |
|  x-----x-----x  |  |  3-----4-----5  |
|  |     |     |  |  |  |     |     |  |
|  |  x--x--x  |  |  |  |  6--7--8  |  |
|  |  |     |  |  |  |  |  |     |  |  |
x--x--x     x--x--x  9-10-11    12-13-14
|  |  |     |  |  |  |  |  |     |  |  |
|  |  x--x--x  |  |  |  | 15-16-17  |  |
|  |     |     |  |  |  |     |     |  |
|  x-----x-----x  |  |  18---19----20  |
|        |        |  |        |        |
x--------x--------x  21------22-------23
'''    
    boardstr = ''
    i = 0
    for c in board:
        if c=='x':
            boardstr += piece_char(g[0][i])
            i += 1
        else:
            boardstr += colored(100,100,100,c)
    if g[1]>0 or g[2]>0:
        boardstr += '\nPlayer 1: ' + (piece_char(1)*g[1])
        boardstr += '\nPlayer 2: ' + (piece_char(2)*g[2])
    print(boardstr)
    
    
    
#############################    
# The functions for each task
    
def is_adjacent(i, j):
    '''
    This function is used to check whether the input integers i and j are 
    adjacent to each other, if they are adjacent to each other, return True, 
    if they are not adjacent to each other, return False.
    
    i and j are integers
    '''
    # Use set to make judgments faster
    adjacent_positions = { 
        0: {1, 9}, 1: {0, 2, 4}, 2: {1, 14},
        3: {4, 10}, 4: {1, 3, 5, 7}, 5: {4, 13},
        6: {7, 11}, 7: {4, 6, 8}, 8: {7, 12},
        9: {0, 10, 21}, 10: {3, 9, 11, 18}, 11: {6, 10, 15},
        12: {8, 13, 17}, 13: {5, 12, 14, 20}, 14: {2, 13, 23},
        15: {11, 16}, 16: {15, 17, 19}, 17: {12, 16},
        18: {10, 19}, 19: {16, 18, 20, 22}, 20: {13, 19},
        21: {9, 22}, 22: {19, 21, 23}, 23: {14, 22}
    }
    # check if the j in the adjacent
    return j in adjacent_positions[i]


def new_game():
    '''
    This function is to create a new game 
    '''
    board = [0] * 24  # Set an empty board
    p1_counters = 9   # Each player will have 9 counters
    p2_counters = 9
    active_player = 1 # Player 1 will starts the game first

    return [board, p1_counters, p2_counters, active_player]

def remaining_counters(g):
    '''
    This function will return the number of counter the player in hand at state g.
    '''
    #cal the remain counter the current_player have
    current_player = g[3]
    unplaced_counters = g[current_player] 
    on_board_counters = g[0].count(current_player)
    #add different stage counters together
    total_counters = unplaced_counters + on_board_counters
    return total_counters

def is_in_mill(g, i):
    '''
    Check if the counter at point i is part of a mill in the game state g.
    '''
    if i < 0 or i >= 24 or g[0][i] == 0:
        return -1
    player = g[0][i]
    
    # Store all triple-connected cases
    mills = {
        0: [[1, 2], [9, 21]],
        1: [[0, 2], [4, 7]],
        2: [[0, 1], [14, 23]],
        3: [[4, 5], [10, 18]],
        4: [[1, 7], [3, 5]],
        5: [[3, 4], [13, 20]],
        6: [[7, 8], [11, 15]],
        7: [[1, 4], [6, 8]],
        8: [[6, 7], [12, 17]],
        9: [[0, 21], [10, 11]],
        10: [[3, 18], [9, 11]],
        11: [[6, 15], [9, 10]],
        12: [[8, 17], [13, 14]],
        13: [[5, 20], [12, 14]],
        14: [[2, 23], [12, 13]],
        15: [[6, 11], [16, 17]],
        16: [[15, 17], [19, 22]],
        17: [[8, 12], [15, 16]],
        18: [[3, 10], [19, 20]],
        19: [[16, 22], [18, 20]],
        20: [[5, 13], [18, 19]],
        21: [[0, 9], [22, 23]],
        22: [[16, 19], [21, 23]],
        23: [[2, 14], [21, 22]]
    }
    
    # Check if the player forms a mill at the specified point
    return player if any(all(g[0][x] == player for x in mill) for mill in mills[i]) else 0



def player_can_move(g):
    '''
    Check whether the player can move. 
    Return True when the current player can move.
    Return False when there are not enough counters or no adjacent unoccupied space.
    '''
    current_player = g[3]
    # Check if the current player has counters left in hand
    if g[current_player] > 0:
        return True
    
    # Check if any of the player's counters on the board are next to an unoccupied space
    if current_player in g[0]:
        return any(g[0][i] == current_player and g[0][j] == 0 and is_adjacent(i, j) for i in range(24) for j in range(24))
    return False


def place_counter(g, i):
    '''
    Place a counter for the currently active player at point i on the board at stage g.
    '''
    current_player = g[3]
    # Check if the location is already occupied
    if g[0][i] != 0:
        raise RuntimeError("Location already occupied by a counter")
    
    g[0][i] = current_player # Place the counter for the current current_player
    g[current_player]-=1 # Decrease the number of counters in hand for the current_player
    

def move_counter(g, i, j):
    '''
    Move a counter of the currently current_player from point i to the adjacent point j at stage g.
    
    g is the state.
    i and g are the integer point on the board.
    '''
    current_player = g[3]
    
    # Check for valid conditions to move the counter
    if not is_adjacent(i, j):
        raise RuntimeError("Points are not adjacent")
    
    if g[0][i] != current_player:
        raise RuntimeError(f"Point {i} does not contain a counter of the current player")
    
    if g[0][j] != 0:
        raise RuntimeError(f"Point {j} is already occupied")
    
    # Move the counter
    g[0][i], g[0][j] = 0, current_player

def remove_opponent_counter(g, i):
    '''
    Remove an opponent's counter from point i on the board in the game state g.
    '''
    current_player = g[3]
    opponent = 3 - current_player  # Use a formula to switch players (assuming there are only two players)
    
    #Return RuntimeError when the point isn't opponent
    if g[0][i] != opponent:
        raise RuntimeError("Point does not contain an opponent's counter")

    g[0][i] = 0

def remove_if_in_mill(g, location):
    '''
    Check if a mill is formed at the given location on the game board.
    If a mill is formed, prompt the current player to input the opponent's counter location to remove it from the board.
    
    g is the he current game state.
    
    '''
    # check the mill and remove the counters
    current_player = g[3]
    formed_mill = is_in_mill(g, location)
    if formed_mill:
        while True:
            try:
                remove_location = request_location(f"Player {current_player}, enter the location of an opponent's counter to remove: ")
                remove_opponent_counter(g, remove_location) # remove the counters
                break
            except RuntimeError as e:
                print(f"RuntimeError: {e}")
        
        
def turn(g):
    '''
    Simulate taking a turn of the game. Handles both Stage 1 and Stage 2.
    '''
    current_player = g[3]
    opponent = 3 - current_player  # Use a formula to switch players (assuming there are only two players)
    current_player_count = remaining_counters(g)
    
    if current_player_count<=2:
        print(f"Player {current_player} loses! They have only two counters left on the board.") # player have only two counters left on the board
        return False
    if not player_can_move(g):
        print(f"Player {current_player} loses! They can't move anymore.")  # player can't move anymore
        return False
    
    # Stage 1: Placing counters on the board
    if g[1] + g[2] > 0:
        while True:
            try:
                location = request_location(f"Player {current_player}, enter a location to place your counter: ")
                # Check if the location is unoccupied
                place_counter(g,location)
                remove_if_in_mill(g, location) # Detect the mill and delete the counters
                break
            except RuntimeError as e:
                print(f"RuntimeError: {e}")
                
    # Stage 2: Moving counters on the board        
    else:
        while True:
            try:
                move_from = request_location(f"Player {current_player}, enter the location to move your counter from: ")
                move_to = request_location(f"Player {current_player}, enter the location to move your counter to: ")
                move_counter(g, move_from, move_to) # move_counter
                remove_if_in_mill(g, move_to) # check after the moving
                break
            except RuntimeError as e:
                print(f"RuntimeError: {e}")
    
    #change the player 
    g[3] = opponent    
    
    return True 


def save_state(g, filename):
    '''
    This function will save the game state g to a text file.
    The function will return RuntimeError is the file cannot be saved.
    '''
    try:
        with open(filename, 'w') as file:
            # Write the board state
            file.write(', '.join(map(str, g[0])) + '\n')
            # Write the counters and the active player
            file.write('\n'.join(map(str, g[1:])))
    except Exception as e:
        raise RuntimeError("Error saving the file: " + str(e))


def load_state(filename):
    '''
    This function will load the game state g from a text file.
    The function will return RuntimeError is the file cannot be loaded.
    '''
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            board_state = list(map(int, lines[0].split(', ')))  # Read the board state
            p1_counters = int(lines[1].strip())  # Read the number of counters left in Player 1's hand
            p2_counters = int(lines[2].strip())  # Read the number of counters left in Player 2's hand
            active_player = int(lines[3].strip())  # Read the current active player
            return [board_state, p1_counters, p2_counters, active_player]
        
    except Exception as e:
        raise RuntimeError("Error loading the file: " + str(e))


def play_game():
    '''
    This function will creates a new game state g and playing game. Until the winner display,
    '''
    
    # you will create a new game, and repeatedly call the turn function
    g = new_game() 

    draw_board(g)
    while turn(g):
        draw_board(g)
    winner = "Player 2" if g[3] == 1 else "Player 1"
    print(f"Congratulations, {winner} wins the game!")
    
def main():
    # You could add some tests to main()
    # to check your functions are working as expected

    # The main function will not be assessed. All code to
    # play the game should be in the play_game() function,
    # and so your main function should simply call this.
    play_game()
    
main()    