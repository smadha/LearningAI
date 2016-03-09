from fact_parser import *

FAILURE_SUB = "FAILURE"

def make_output(suffix, goal):
    if(goal):
        print suffix + str(goal)

'''
return a generator of substitutions
query - [{'Traitor': ['Anakin']}] 
'''
def FOL_BC_ASK(KB,query):
    print query
    for q in query:
        print q
        for sub in FOL_BC_OR(KB, q, []):
            print q, sub
    return 

'''
goal = {'Traitor': ['Anakin']}
sub = {'a':'Anakin'}
1. Find match in KB
2. If match == goal return
3. generate substitution
4. Call AND for further investigation 
'''    
def FOL_BC_OR(KB,goal, sub):
    print "FOL_BC_OR -I", goal, sub
    
    #make_output("Ask: ",goal)
    # get match
    # TODO handle it as a list
    matchs = get_match_fact(KB, goal)
    if not matchs:
        print "FAILS FOL_BC_OR NO MATCH",goal,sub
            
        
    for match_orig in matchs:
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
                else:
                    lhs[0]={}
    
        # TODO chain substitution 
        new_sub.update(sub)
        
        #Pass LHS to AND TREE 
        print "FOL_BC_OR -F", lhs,new_sub
        
        for sub1 in FOL_BC_AND(KB,lhs,new_sub):
            yield sub1
    


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
    #print  "FOL_BC_AND -I" ,goals,sub
    
    if sub == FAILURE_SUB :
        print  "FALURE FOL_BC_AND FALURE" ,goals,sub
        return
    
    if not goals or not goals[0]:
        print "TRUE FOL_BC_AND -R1 ",goals,sub
        yield sub
    else:             
        first = goals[0]
        rest = goals[1:]
        
        for sub1 in FOL_BC_OR(KB, substitute(first, sub), sub) :
            print "FOL_BC_AND -R2 ",goals,sub1
            for sub2 in FOL_BC_AND(KB,rest,sub1) : 
    #            print "FOL_BC_AND -R3 ",goals,sub2
                yield sub2

    
    
