def enumerate_ask(target_variables, observations, bayes_net, variables):
    '''
    target_variables = Single variable name -> NightDefense
    observations = given events -> {NightDefense : +, Infiltration : - }
    bayes_net - Dictionary of EventNode 
    '''
     
    calc_prob = {} # required probability numbers for target_variables
    
    hidden_variables = [v for v in variables if v not in observations.keys()]
    
    # TODO check if observations could be provided for nodes with parents
        
    # TODO make xi restricted to asked values
    for xi in ["+","-"]:
        print target_variables, xi, observations
        calc_prob[xi] = enumerate_all(hidden_variables, extend(observations, target_variables, xi), bayes_net)
    
    print calc_prob
    return calc_prob

def enumerate_all(variables, observations, bayes_net):
    '''
    variable = Single variable name -> NightDefense
    observations -> {'LeakIdea': '-', 'Demoralize': '+', 'Infiltration': '+'} value +/-
    '''
#     print variables, observations, "\n"
    if not variables or len(variables) == 0: 
        return 1
    
    first = variables[0]; rest = variables[1:]
    
#     if not set(bayes_net[first].getParents()).issubset(observations):
#         # observation for parents are not available yet
#         # add this to rest and we can process it later
#         rest.append(first)   
#         print "Appended for re-evaluation" - first
#         return enumerate_all(rest, observations, bayes_net)
    
    # observation for parents are available
    obs_parents = ''.join([observations[p] for p in bayes_net[first].getParents()])
        
    if first in observations:     
        prob_first = bayes_net[first].getProbability(observations[first], obs_parents)
        total_prob = prob_first * enumerate_all(rest, observations, bayes_net)
#         print first, observations[first], obs_parents, prob_first, total_prob
        return total_prob 
    else :
        prob_first = []
        for value in ["+","-"]:
            prob_first_value = bayes_net[first].getProbability(value, obs_parents)
#             print first, value, obs_parents, prob_first_value
            prob_first.append( prob_first_value * enumerate_all(rest, extend(observations, first, value), bayes_net) )
        
#         print first, obs_parents, sum(prob_first) 
        return sum(prob_first)

def extend(event, var, val):
    '''
    {'LeakIdea': '-', 'Infiltration': '+'} Demoralize ++
    {'LeakIdea': '-', 'Demoralize': '++', 'Infiltration': '+'}
    '''
    eve2 = event.copy()
    eve2[var] = val
    return eve2
