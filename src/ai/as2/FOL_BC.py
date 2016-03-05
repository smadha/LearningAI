from fact_parser import *

def make_output(suffix, goal):
    if(goal):
        print suffix + str(goal)

'''
return a generator of substitutions
query - [{'Traitor': ['Anakin']}] 
'''
def FOL_BC_ASK(KB,query):
    for q in query:
        return FOL_BC_OR(KB, q, [])

'''
goal = {'Traitor': ['Anakin']}
sub = {'a':'Anakin'}
1. Find match in KB
2. If match == goal return
3. generate substitution
4. Call AND for further investigation 
'''
def FOL_BC_OR(KB,goal, sub):
    if not goal:
        return []
    make_output("Ask: ",goal)
    # get match
    match = get_match_fact(KB, goal)
    # get LHS, RHS
    lhs = match [0]
    rhs = []
    if lhs[0] == goal:
        make_output("True: ",goal)
        return []
    #new_clause = []
    
    if len(match) ==2: #check if rhs is there
        rhs =  match [1][0] # single conclusion by design
        new_sub = unify(rhs, goal)
        #new_clause = substitute(match, new_sub) 
    else: #process LHS
        for fact in lhs:
            new_sub = unify(fact, goal)
            if (new_sub):
                #new_clause = substitute(match, new_sub)
                break

    
    sub.append(new_sub)
    #Pass LHS to AND TREE 

    and_sub = FOL_BC_AND(KB,lhs,sub)
    deduced_state = rhs
    sub+=and_sub
    for sub_i in sub:
        deduced_state = substitute(deduced_state, sub_i)
#         print '*',goal, rhs,[new_sub, unify(goal, deduced_state)]
    
    if (deduced_state):
        sub.append(unify(goal, deduced_state))
        make_output("True-: ", deduced_state)
    
    return sub


'''
goals = [{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}]
sub= {'a': 'Anakin'}
yields a substitution
'''
def FOL_BC_AND(KB,goals,subs):
    '''    
    generator FOL-BC-AND(KB,goals,subs) yields a substitution if subs = failure then return
    else if LENGTH(goals) = 0 then yield subs
    else do
    first,rest <- FIRST(goals), REST(goals)
    for each subs' in FOL-BC-OR(KB, SUBST(subs, first), subs) do
    for each subs'' in FOL-BC-AND(KB,rest,subs') do yield subs''
    '''
    if not goals:
        return []
    for sub in subs:
        goals = substitute(goals, sub) 
#     print  "FOL_BC_AND", goals, subs
    
    first = goals.pop(0)
    
    new_sub = FOL_BC_OR(KB, first, subs)
#     if(new_sub):
#         print goals
#         print new_sub

    for sub in new_sub:
        goals = substitute(goals, sub)
         
    FOL_BC_AND(KB, goals, new_sub)
    
    return new_sub
    
