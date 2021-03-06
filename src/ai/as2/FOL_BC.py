from fact_parser import *

FAILURE_SUB = "FAILURE"
traverse_log = ""

def make_output(suffix, goal=None):
    global traverse_log
    
    if(goal):
#         print suffix + ressurect_fact(goal)
        traverse_log +="\r\n{0}".format(suffix + ressurect_fact(goal))
    else:
#         print suffix
        traverse_log +="\r\n{0}".format(suffix)
    

'''
return a generator of substitutions
query - [{'Traitor': ['Anakin']}] 
'''
def FOL_BC_ASK(KB,query):
#     print query
#     print query[0]
    global traverse_log
    for sub in FOL_BC_OR(KB, query[0], {}):
        # print "TRUE _-_-_#",sub
        if len(query) == 2:
            for sub2 in FOL_BC_OR(KB, query[1], {}):
                # print "_-_-_##",sub2
                make_output("True")
                return traverse_log
            # print "FAIL _-_-_##",query
            make_output("False")
        else:
            make_output("True")
        return  traverse_log
    
    # print "FAIL _-_-_#",query
    make_output("False")
    return  traverse_log
    

'''
goal = {'Traitor': ['Anakin']}
sub = {'a':'Anakin'}
1. Find match in KB
2. If match == goal return
3. generate substitution
4. Call AND for further investigation 
'''    
def FOL_BC_OR(KB,goal, sub):
    #print "FOL_BC_OR -I", goal, sub
    
    make_output("Ask: ",goal)
    # get match
    # TODO handle it as a list
    matchs = get_match_fact(KB, goal)
    log_false_in_end = True
    if not matchs:
        #print "FAILS FOL_BC_OR NO MATCH",goal,sub
        log_false_in_end = False
        make_output("False: ",goal)
            
    repeat = False
    
    for match_orig in matchs:
        if repeat:
            make_output("Ask: ",goal)
        repeat = True
        match = standardize_rule(match_orig)
        # get LHS, RHS
        lhs = match [0]
        rhs = []
        
        if len(match) ==2: #check if rhs is there
            rhs =  match [1][0] # single conclusion by design
            new_sub = unify(rhs, goal)
            #new_clause = substitute(match, new_sub) 
        else: #process LHS    
            new_sub = unify(lhs[0], goal) # if no implication than only one atomic sentence
            if (new_sub): #TODO TEST
                new_goal = substitute(goal, new_sub)
                if lhs[0] == new_goal:
                    lhs[0] = {}
            else:
                # if no sub available and lhs[0] != new_goal failure
                if lhs[0] != goal:
                    new_sub = FAILURE_SUB
                    log_false_in_end = False
                else:
                    lhs[0]={}
    
        # TODO chain substitution 
        new_sub.update(sub)
        
        #Pass LHS to AND TREE 
        ##print "FOL_BC_OR -F", lhs,new_sub

        for sub1 in FOL_BC_AND(KB,lhs,new_sub):
            log_false_in_end = False
            if sub1:
                make_output("True: ", substitute(goal,sub1) )
            yield sub1
        
    if log_false_in_end:
            print "log_false_in_end", goal,sub
            make_output("False: ", substitute(goal,sub) )


'''
goals = [{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}]
sub= {'a': 'Anakin'}
yields a substitution
'''
def FOL_BC_AND(KB,goal,sub):
    '''    
    generator FOL-BC-AND(KB,goal,sub) yields a substitution if sub = failure then return
    else if LENGTH(goal) = 0 then yield sub
    else do
    first,rest <- FIRST(goal), REST(goal)
    for each sub' in FOL-BC-OR(KB, SUBST(sub, first), sub) do
    for each sub'' in FOL-BC-AND(KB,rest,sub') do yield sub''
    '''
    #print  "FOL_BC_AND -I" ,goal,sub
    
    if sub == FAILURE_SUB :
        #print  "FOL_BC_AND FALURE" ,goal,sub
        make_output("False: ",goal)
        return
    
    if not goal or not goal[0]:
        #print "FOL_BC_AND TRUE  ",goal,sub
        yield sub
    else:             
        first = goal[0]
        rest = goal[1:]
        
        for sub1 in FOL_BC_OR(KB, substitute(first, sub), sub) :
            #print "FOL_BC_AND -R2 ",goal,sub1
            for sub2 in FOL_BC_AND(KB,rest,sub1) : 
    #            #print "FOL_BC_AND -R3 ",goal,sub2
                yield sub2

    
    
