'''
A 2d array representing 5*5 board
00,01,02,03,04
10,11,12,13,14
20,21,22,23,24
30,31,32,33,34
40,41,42,43,44
'''
COL_LEGEND = 'ABCDE'
ROW_LEGEND = '12345'
DIRTY_VALUE = 9999

ALL_CELL = set([00, 01, 02, 03, 04, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34, 40, 41, 42, 43, 44])
X = 'X'
O = 'O'
NEG_INF = -float("inf")
POS_INF = float("inf")

'''
Transform cell from 00 -> A1
01 -> B1
'''
def transform_cell(cell):
    row, col = _get_row_cell(cell)
    return COL_LEGEND[col]+ROW_LEGEND[row]
'''
Returns row+col using row and col
*DIRTY_VALUE* if out of bounds
'''
def _str_add_valid_int(row , col):
    if(0 <= row <= 4 and 0 <= col <= 4):
        return int(str(row) + str(col))
    return DIRTY_VALUE
'''
Returns row and cell using row+cell
'''
def _get_row_cell(cell):
    return cell / 10, cell % 10
'''
return up, down, left,right
*DIRTY_VALUE* if out of bounds
'''
def _get_adj_cells(row, col):
    up = _str_add_valid_int(row + 1, col)
    down = _str_add_valid_int(row - 1, col)
    left = _str_add_valid_int(row, col - 1)
    right = _str_add_valid_int(row, col + 1)
    return up, down, left,right

def _clear_dirty(set_cells):
    if DIRTY_VALUE in set_cells:
        set_cells.remove(DIRTY_VALUE)
    return set_cells
'''
- Expect a list of size 5
- Each element is a space separated list of size 5 containing only numbers
- No validations are done 
- Returns a dictionary with d[row_num][column_index]=number
'''
def init_board(list_value):
    board = {}
    row_c = 0
    for row in list_value:
        col_i = 0
        board[row_c] = {}
        for ele in row.split():
            board[row_c][col_i] = int(ele)
            col_i += 1
        row_c += 1
        
    return board
'''
Initialize set of states from input list of *,X,O.
Return player_x, player_y
**XX*
**XOX
***O*
**OO*
*****
'''
def init_state(list_value):
    player_x=set([])
    player_o=set([])
    row_c = 0
    for row in list_value:
        col_i = 0
        for ele in row:
            if(ele == X):
                player_x.add(_str_add_valid_int(row_c,col_i))
            elif(ele == O):
                player_o.add(_str_add_valid_int(row_c,col_i))
            col_i += 1
        row_c += 1
        
    return player_x,player_o
'''
Print output as 
**XX*
**XOX
***O*
**OO*
*****
'''
def output_state(player_x,player_o):
    op=''
    for row_c in range(0,5):
        for col_i in range(0,5):
            cell = _str_add_valid_int(row_c,col_i)
            if(cell in player_x):
                op+=X
            elif(cell in player_o):
                op+=O
            else:
                op+='*'
        op+='\r\n'
    return op[:-2]
'''
- Takes list of occupied cells as [row][col] 11, 12 etc.. from player A and B
- Return 
    list of possible RAID destination cells in same format for player A
    list of possible SNEAK destination cells in same format for player A
'''
def get_possible_moves(set_a, set_b):
    possible_raid = set([])
    possible_sneak = ALL_CELL  # initialize with full set
    total_occupied = set_a.union(set_b)
    
    # #Add all possible raid moves from list_a
    for cell in set_a:
        row, col = _get_row_cell(cell)
        up, down, left,right = _get_adj_cells(row, col)
        
        possible_raid.add(up)
        possible_raid.add(down)
        possible_raid.add(left)
        possible_raid.add(right)
     
    # #strip occupied cells from set_a and set_b 
    possible_raid = possible_raid.difference(set_a)
    possible_raid = possible_raid.difference(set_b)
    # #strip dirty value 9999
    _clear_dirty(possible_raid)
    
    # #get possible_sneak = possible_sneak - total_occupied - possible_raid
    possible_sneak = possible_sneak.difference(total_occupied).difference(possible_raid)
    
    return possible_raid, possible_sneak

'''
Returns set(new cells) occupied by player a if player choose to raid on raid_cell. Including raid_cell
*No validation*
'''
def move_raid(set_a, set_b, raid_cell):
    row, col = _get_row_cell(raid_cell)
    # get cells adj to raid cells
    adj_raid_cell = set(_get_adj_cells(row, col))
    # del out of bound values
    _clear_dirty(adj_raid_cell)
    # delete already occupied cells
    adj_raid_cell = adj_raid_cell.difference(set_a)
    
    # select cells that are part of player b 
    return adj_raid_cell.intersection(set_b).union(set([raid_cell]))

    
'''
return score for one player
'''
def get_score(set_a, board):
    score_a = 0
    for cell in set_a:
        row, col = _get_row_cell(cell)
        score_a += board[row][col]
    return score_a  
'''
return points of set_a - points of set_b
''' 
def evaluate_state(set_a, set_b, board):
    return get_score(set_a, board) - get_score(set_b, board)

''' 
defining tie breaker
'''
def is_tie_breaker(cell_a,cell_b):
    return cell_a < cell_b
#     row_a,col_a = _get_row_cell(cell_a) 
#     row_b,col_b = _get_row_cell(cell_b)
#     if row_a < row_b:
#         return True
#     elif row_a == row_b:
#         if col_a < col_b:
#             return True
#         else:
#             return False
#     else:
#         return False

''' 
defining termination
'''
def is_terminated(set_a, set_b):
    return set_a.union(set_b) == ALL_CELL

'''
write log file
'''
def write_traverse_log(traverse_log):
    with open("traverse_log.txt",'w') as f:
        f.write(traverse_log);
        f.close()

# TEST CALLS
# list_value = "20 16 1 32 30*20 12 2 11 8 *28 48 9 1 1*20 12 10 6 2 *25 30 23 21 10" 
# board = init_board(list_value.split("*"))

# print get_possible_moves(set([0]), set([1]))
# print get_possible_moves(set([10]), set([1]))
# print get_possible_moves(set([22]), set([1]))

# print board
# print get_score(set([32,33,23,13]), board) #-> 28    
# print get_score(set([02,03,12,14]), board) #-> 43
# print evaluate_state(set([32, 33, 23, 13]), set([02, 03, 12, 14]), board)


# print move_raid(set([10]), set([1]),11)
# print move_raid(set([10]), set([1]),0)
# print move_raid(set([10]), set([1]),20) # no add
# print move_raid(set([21]), set([23]),22)
# print move_raid(set([21]), set([30]),31)
# print move_raid(set([21]), set([30]),22) # no add

# print output_state(set([21]), set([30]))

# print is_tie_breaker(04,22)
# print is_tie_breaker(03,04)
# print is_tie_breaker(22,04)

# print transform_cell(0)
# print transform_cell(1)

# print is_terminated(set([0]), set([1]))
# print is_terminated(set([0,1,2,3,4,10,11,12,13,14,20,21,22,23,24]), set([30,31,32,33,34,40,41,42,43,44]))



