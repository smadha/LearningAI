from fact_parser import *

'''
generator FOL-BC-OR(KB,goal,sub) yields a substitution
for each rule (lhs => rhs) in FETCH-RULES-FOR-GOAL(KB, goal) do
(lhs, rhs) <- STANDARDIZE-VARIABLES((lhs, rhs))
for each sub' in FOL-BC-AND(KB,lhs,UNIFY(rhs, goal, sub')) do
yield sub'
'''
'''
return a generator of substitutions
query - [{'Traitor': ['Anakin']}] 
'''
def FOL_BC_ASK(KB,query):
    for q in query:
        return FOL_BC_OR(KB, q, { })

'''
yields a substitution
goal = {'Traitor': ['Anakin']}
sub = {'a':'Anakin'}
'''
def FOL_BC_OR(KB,goal, sub):
    if not goal:
        return True
    # get match
    match = get_match_fact(KB, goal)
    # get LHS, RHS
    lhs = match [0]
    
    if lhs[0] == goal:
        print "goal matched ", goal
        return True
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
    
    print "FOL_BC_OR", goal
    print match
    print new_sub
    #Pass LHS to AND TREE one by one
    
    FOL_BC_AND(KB,lhs,new_sub)  

    #print  "FOL_BC_OR", KB,goal

'''
goals = [{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}]
sub= {'a': 'Anakin'}
yields a substitution
'''
def FOL_BC_AND(KB,goals,sub):
    '''    
    generator FOL-BC-AND(KB,goals,sub) yields a substitution if sub = failure then return
    else if LENGTH(goals) = 0 then yield sub
    else do
    first,rest <- FIRST(goals), REST(goals)
    for each sub' in FOL-BC-OR(KB, SUBST(sub, first), sub) do
    for each sub'' in FOL-BC-AND(KB,rest,sub') do yield sub''
    '''
    if not goals:
        return True
    
    goals = substitute(goals, sub) 
    print  "FOL_BC_AND", goals
    
    first = goals.pop(0)
    
    FOL_BC_OR(KB, first, sub)
    
    FOL_BC_AND(KB, goals, sub)
    
