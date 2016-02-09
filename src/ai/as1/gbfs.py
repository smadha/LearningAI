'''
Greedy Best-First-Search
'''
from ip_graph import *

'''
Given board values and player a and b state it gives you next move for player a using GBFS
*depth is not used here. It's included for similar interface with other algos*
'''
def get_next_move_gbfs(board, state_a, state_b, depth):
    # TODO - handle tie breaker 
    raid_a, sneak_a = get_possible_moves(state_a, state_b)
    max_score = NEG_INF
    new_occ_cells = set([])  # this contain all the new cells include move and conquered
    max_move = 0  # this have the moved cell
    
    for move_a in sneak_a:
        move = set([move_a])
        new_score = evaluate_state(state_a.union(move), state_b, board)
        # print "{0} - {1}".format(move, new_score) 
        if(new_score > max_score):
            max_score = new_score
            new_occ_cells = move
            max_move = move_a
        if(new_score == max_score and is_tie_breaker(move_a, max_move)):
            max_score = new_score
            new_occ_cells = move
            max_move = move_a
    
    for move_a in raid_a:
        move = move_raid(state_a, state_b, move_a)
        new_score = evaluate_state(state_a.union(move), state_b.difference(move), board)
        # print "{0} - {1}".format(move, new_score) 
        if(new_score > max_score):
            max_score = new_score
            new_occ_cells = move
            max_move = move_a
        if(new_score == max_score and is_tie_breaker(move_a, max_move)):
            max_score = new_score
            new_occ_cells = move
            max_move = move_a
    
    # print max_score
    return new_occ_cells


# TEST CASES
# 1-sneak
#      Basic 
#      sneak with only 1 cell left
#      sneak when 0 cells available
# 2- Basic raid
#      Basic 
#      raid with only 1 cell left
#      raid when 0 cells available
#      raid conquering opp cells
#      raid when singe adj > sneak
# 3- Tie Breaker 


