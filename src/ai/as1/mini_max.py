'''
Mini-Max 
'''
from ip_graph import *

global_depth=0
##TODO Add Termination conditions
traverse_log = "Node,Depth,Value"

def _log_state(node,depth,value):
    global traverse_log
    global global_depth

    depth = global_depth - depth
    
    if isinstance(node, int):
        node = transform_cell(node)
    
    if value == NEG_INF:
        value="-Infinity"
    
    if value == POS_INF:
        value="Infinity"
        
    traverse_log+="\r\n{0},{1},{2}".format(node, depth, value)

    
def _set_possible_move(possible_new_cells, move_a, move):
    #sort possible_new_cells in Expand Order given in assignment
    possible_new_cells[possible_new_cells.index(move_a)] = move


def _get_sorted_list(raid_a, sneak_a):
    possible_new_cells = list(raid_a.union(sneak_a)) # init new cells with sorted possible moves
    possible_new_cells.sort()
    return possible_new_cells


'''
Given board values and player a and b state it gives you next move for player a using Mini-Max
'''
def get_next_move_mm(board, state_a, state_b, depth):
    #print evaluate_state(state_a, state_b, board)
    # Maximum of minimum
    global global_depth
    global_depth=depth
    raid_a, sneak_a = get_possible_moves(state_a, state_b)
    possible_new_cells = _get_sorted_list(raid_a, sneak_a)    #sort possible_new_cells in Expand Order given in assignment
    
    max_score = NEG_INF
    new_occ_cells = set([])  # this contain all the new cells include move and conquered
    
    for move_a in sneak_a:
        move = set([move_a])# single cell
        _set_possible_move(possible_new_cells, move_a, move)
    
    for move_a in raid_a:
        move = move_raid(state_a, state_b, move_a)# could be multiple cells
        _set_possible_move(possible_new_cells, move_a, move)

    for move in possible_new_cells:
        _log_state("root", depth, max_score)
        # Use this move to see what min_value does
        new_score = min_value(move.difference(state_b).pop(), board, state_a.union(move), state_b.difference(move), depth - 1)
        
        ## possible log here 
        _log_state(move.difference(state_b).pop(), depth-1, new_score)
        
        # get arg max new_score
        if(new_score > max_score):
            max_score = new_score
            new_occ_cells = move

    _log_state("root", depth, max_score)
    
    # Done to handle edge case if board is full 
    if(max_score == NEG_INF):
        _log_state("root", depth, evaluate_state(state_a, state_b, board))
        
    write_traverse_log(traverse_log)
    return new_occ_cells

'''
Plays as max player for player A
'''
def max_value(act_move,board, state_a, state_b, depth):
#     print "\nMAX - {0} \n".format(depth)+output_state(state_a, state_b)
#     print evaluate_state(state_a, state_b, board)
    
    if depth == 0 or is_terminated(state_a, state_b):
        new_score = evaluate_state(state_a, state_b, board)
        #_log_state(act_move, 0, new_score)
        return new_score
    
    raid_a, sneak_a = get_possible_moves(state_a, state_b)
    possible_new_cells = _get_sorted_list(raid_a, sneak_a)    #sort possible_new_cells in Expand Order given in assignment

    max_score = NEG_INF
    
    for move_a in sneak_a:
        move = set([move_a])# single cell
        _set_possible_move(possible_new_cells, move_a, move)
        # print "{0} - {1}".format(move, new_score) 
    
    for move_a in raid_a:
        move = move_raid(state_a, state_b, move_a)# could be multiple cells
        _set_possible_move(possible_new_cells, move_a, move)
        # print "{0} - {1}".format(move, new_score) 
    
    
    for move in possible_new_cells:
        _log_state(act_move, depth, max_score)
        # Use this move to see what min_value does
        new_score = min_value(move.difference(state_b).pop(), board, 
                              state_a.union(move), state_b.difference(move), depth-1)
        
        _log_state(move.difference(state_b).pop(), depth-1, new_score)

        # get arg max new_score
        if(new_score > max_score):
            max_score = new_score
    
    return max_score

'''
Plays as player B - min player
'''
def min_value(act_move,board, state_a, state_b, depth):
#     print "\n MIN - {0} \n".format(depth)+output_state(state_a, state_b)
#     print evaluate_state(state_a,state_b, board)

    if depth == 0 or is_terminated(state_a, state_b):
        new_score = evaluate_state(state_a, state_b, board)
        #_log_state(act_move, 0, new_score)
        return new_score
    
    raid_b, sneak_b = get_possible_moves(state_b, state_a)
    possible_new_cells = _get_sorted_list(raid_b, sneak_b)    #sort possible_new_cells in Expand Order given in assignment
    
    min_score = POS_INF
    
    for move_a in sneak_b:
        move = set([move_a])# single cell
        _set_possible_move(possible_new_cells, move_a, move)
    
    for move_a in raid_b:
        move = move_raid(state_b, state_a, move_a)# could be multiple cells
        _set_possible_move(possible_new_cells, move_a, move)
    

    for move in possible_new_cells:
        _log_state(act_move, depth, min_score)
        # Use this move to see what min_value does
        new_score = max_value(move.difference(state_a).pop(), board, state_a.difference(move),
                              state_b.union(move), depth-1)        
        
        _log_state(move.difference(state_a).pop(), depth-1, new_score)

        # get arg min new_score
        if(new_score < min_score):
            min_score = new_score
    
    return min_score

# TEST case
# check for d=3



