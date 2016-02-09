# # Final executable
import sys

from gbfs import get_next_move_gbfs
from mini_max import get_next_move_mm
from alpha_beta import get_next_move_ab
from ip_graph import *


ip_file = sys.argv[2]
OP_FILE_NEXT = "next_state.txt"
BATTLE_TRACE_FILE = "trace_state.txt"

algo = 0
board_value = []
player = ''
depth = 0
board_state = []

algo2 = 0
player2 = ''
depth2 = 0

def set_algo(num):
    global algo
    algo = int(num)

def set_player(num):
    global player
    player = num

def set_depth(d):
    global depth
    depth = int(d)
    
def set_algo2(num):
    global algo2
    algo2 = int(num)

def set_player2(num):
    global player2
    player2 = num

def set_depth2(d):
    global depth2
    depth2 = int(d)

def add_board_value(num_arr):
    board_value.append(num_arr)

def add_board_state(state_arr):
    board_state.append(state_arr)
        
options = {1 : set_algo,
           2 : set_player,
           3 : set_depth,
           4 : add_board_value,
           5 : add_board_value,
           6 : add_board_value,
           7 : add_board_value,
           8 : add_board_value,
           9 : add_board_state,
           10 : add_board_state,
           11 : add_board_state,
           12 : add_board_state,
           13 : add_board_state
}

options_battle = {1 : set_algo,
           2 : set_player,
           3:  set_algo,
           4 : set_depth,
           5 : set_player2,
           6:  set_algo2,
           7 : set_depth2,
           8 : add_board_value,
           9 : add_board_value,
           10 : add_board_value,
           11 : add_board_value,
           12 : add_board_value,
           13 : add_board_state,
           14 : add_board_state,
           15 : add_board_state,
           16 : add_board_state,
           17 : add_board_state
}

def run_gbfs(board, st_a, st_b, depth):
    return get_next_move_gbfs(board, st_a, st_b, depth)

def run_minimax(board, st_a, st_b, depth):
    return get_next_move_mm(board, st_a, st_b, depth)

def run_alphabeta(board, st_a, st_b, depth):
    return get_next_move_ab(board, st_a, st_b, depth)

algo_opt = {1: run_gbfs,
        2: run_minimax,
        3: run_alphabeta}

def choose_x(player_x, player_o):
    return player_x, player_o 
    
def choose_y(player_x, player_o):
    return player_o, player_x 
    
player_opt = {X: choose_x,
        O: choose_y}


with open(ip_file, 'r') as f:
    line = f.readline()
    line = line.strip()
    count = 1
    if (line == "4"):
        while line:
            print line.strip()
            options_battle[count](line.strip())
            line = f.readline()
            count += 1
    else:
        while line:
            print line.strip()
            options[count](line.strip())
            line = f.readline()
            count += 1
    f.close()

 
board = init_board(board_value)
# print board


# print player
player_x, player_o = init_state(board_state)

# print get_score(st_a, board)

if(algo2 == 0):
    # use player to decide st_a and st_b
    # st_a plays first
    st_a, st_b = player_opt[player](player_x, player_o)
    
    # print algo,depth
    # use algo to decide among available algos
    # use depth in mini-max and alpha beta
    next_move = algo_opt[algo](board, st_a, st_b, depth)
    st_a = st_a.union(next_move)
    st_b = st_b.difference(next_move)
    
    # switched player again for output
    player_x, player_o = player_opt[player](st_a, st_b)
    print '\n' + output_state(player_x, player_o)
    
    with open(OP_FILE_NEXT, 'w') as f:
        f.write(output_state(player_x, player_o))
        f.close()
else:
    # battle mode
    trace_state = ''
    while not is_terminated(player_x, player_o) :
        # use player to decide st_a and st_b
        # st_a plays first
        st_a, st_b = player_opt[player](player_x, player_o)
        
        next_move_a = algo_opt[algo](board, st_a, st_b, depth)
        st_a = st_a.union(next_move_a)
        st_b = st_b.difference(next_move_a)
        
        # switched player again for output
        player_x, player_o = player_opt[player](st_a, st_b)
        # print '\n' + output_state(player_x, player_o)
        trace_state += output_state(player_x, player_o) + '\r\n' 
        
        if is_terminated(player_x, player_o):
            continue
#         # use player to decide st_a and st_b
#         # st_a plays first
#         st_a, st_b = player_opt[player](player_x, player_o)
#         
        next_move_b = algo_opt[algo2](board, st_b, st_a, depth2)
        st_b = st_b.union(next_move_b)
        st_a = st_a.difference(next_move_b)
        
        # switched player again for output
        player_x, player_o = player_opt[player](st_a, st_b)
        # print '\n' + output_state(player_x, player_o)
        trace_state += output_state(player_x, player_o) + '\r\n' 
        
    with open(BATTLE_TRACE_FILE, 'w') as f:
        f.write(trace_state[:-2])
        f.close()
    
 

