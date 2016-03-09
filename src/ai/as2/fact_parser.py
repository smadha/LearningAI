
'''
Takes input one single fact. 
No conjunction of multiple facts
return function followed by parameters in same order
I/P STR  -> 'Knows(Sidious,Pine)'
O/P DICT -> {'Knows' : ['Sidious','Pine'] }
'''
from copy import deepcopy

def _parse_one_fact(fact):
    parsed_fact = {}
    i = fact.index("(")
    parsed_fact[fact[:i]] = fact[i + 1:-1].split(", ")
    return parsed_fact
    
'''
Takes input as LHS of => or RHS of =>
return list of DICT of facts
IP STR-> Resource(x) && Knows(Sidious, x)
O/P List<dict> ->
    [
    {'Resource' : ['x'] }
    {'Knows' : ['Sidious','x'] }
    ]
'''
def _parse_implication_facts(fact):
    _parse_implication_facts = []
    for f in fact.split(" && "):
        _parse_implication_facts.append(_parse_one_fact(f))
    return _parse_implication_facts
'''
Splits implies in LHS and RHS
I/P: Resource(x) => Secret(x)
O/P: [[{'Resource': ['x']}], [{'Secret': ['x']}]]
'''
def parse_full_facts(fact):
    parse_full_facts = []
    for f in fact.split(" => "):
        parse_full_facts.append(_parse_implication_facts(f))
    return parse_full_facts

'''
All predicate names and constant names consist of only uppercase ('A', 'Z') or lowercase ('a','z') letters
There is no number or symbol (no '_', '', etc.) in the names.
'''
def is_constant(name):
    return len(name) <= 20 and name[0].isupper()
'''
Variables are denoted by a single lowercaseletter.
'''
def is_var(name):
#     return len(name) == 1 and name.islower()
    return name[0].islower()

def _get_term_one_fact(fact):
    '''
    I/P dict
    I/P - {'Traitor': ['x']}
    O/P - Traitor
    '''
    return fact.keys()[0]

def _get_var_one_fact(fact):
    '''
    I/P dict
    I/P - {'Traitor': ['x']}
    O/P - ['x']
    '''
    return fact.values()[0]

'''
#Rules matching conditions
# Function name should match - first rule irrespective of anything
#If the goal has only constants 
# ===> the exact goal should be found in the rule
# ===> if the rule is an implication then carry on
# ====> If the rule is not an implication then, either only the goal is present in the rule or it is present in conjunction with some other atomic sentence
#If the goal has a combination of variables and constants
#===> the non variable argument-> if both have non constants ->then they should match
#===? if both var, or one var nd other constant - simply add that to the rule set
'''
def get_match_fact(knowledge, query):
    '''
    knowledge = KB
    query = {'Enemy': ['Sidious', 'USC']}
    '''
    list_fact = []
    q_term = _get_term_one_fact(query)
    q_var = _get_var_one_fact(query)
    for k in knowledge:  # sample k = "[[{'Resource': ['x']}], [{'Secret': ['x']}]]"
        if len(k) == 2:  # if implication take RHS
            for fact in k[1]:  # sample k[1] = "[{'Secret': ['x']}]"
                if q_term == _get_term_one_fact(fact):
                    add = True
                    for idx,v in enumerate(_get_var_one_fact(fact)):
                        if is_constant(v) and is_constant(q_var[idx]) and v != q_var[idx]:
                            add = False
#                             print "*",fact, k
                    if add:
                        list_fact.append(k)
        else:  # sample k = "[[{'Enemy': ['Sidious', 'USC']}]]"
            for fact in k[0]:  # sample k[0] = "[{'Enemy': ['Sidious', 'USC']}]"
                if q_term == _get_term_one_fact(fact):
                    add = True
                    for idx,v in enumerate(_get_var_one_fact(fact)):
                        if is_constant(v) and is_constant(q_var[idx]) and v != q_var[idx]:
                            add = False
#                             print "*",fact, k
                    if add:
#                     print fact, k
                        list_fact.append(k)

    return deepcopy(list_fact)

def unify(fact1, goal):
    '''
    I/P {'Traitor': ['Anakin']}"), "{'Traitor': ['a']}
    O/P {'a':'Anakin'}
    '''
    res = {}
    if fact1.keys() != goal.keys():
        return res
    
    f1_params = enumerate(fact1.values()[0])
    f2_params = goal.values()[0]
    for idx, p1 in f1_params:
        p2 = f2_params[idx]
        if (is_var(p1) and is_var(p2)):
                res[p2]=p1
        elif (is_var(p1)):
            if (is_constant(p2)):
                res[p1]=p2
        elif (is_var(p2)):
            if (is_constant(p1)):
                res[p2]=p1
    
    return res

'''
Assign z as variable name in query
query will have only one variable
"[[{'Traitor': ['Anakin']}]]"
"[[{'Traitor': ['x']}]]"
NOT USED
'''
def standardize_var(query):
    for fact in query[0]:
        new_var = []
        for val in fact.values()[0]:
            if is_var(val):
                new_var.append('z')
            else:
                new_var.append(val)
        fact[fact.keys()[0]] = new_var 
    return query
'''
Assign unique variable names in whole knowledge base
NOT USED
'''
def standardize(knowledge):
    idx = 97
    for k in knowledge:
        cur_var = {}
        for side in k:
            for fact in side:
                new_var = []
                for val in fact.values()[0]:
                    if is_var(val):
                        if val not in cur_var.keys():
                            cur_var[val] = chr(idx)
                            idx += 1
                        new_var.append(cur_var[val])
                    else:
                        new_var.append(val)
                fact[fact.keys()[0]] = new_var
    return knowledge

idx_std = 0
'''
FOR ONE RULE
Assign unique variable names to this rule in whole knowledge base 
'''
def standardize_rule(rule):
    global idx_std
    cur_var = {}
    for side in rule:
        for fact in side:
            new_var = []
            for val in fact.values()[0]:
                if is_var(val):
                    if val not in cur_var.keys():
                        cur_var[val] = val + str(idx_std)
                    new_var.append(cur_var[val])
                else:
                    new_var.append(val)
            fact[fact.keys()[0]] = new_var
    
    idx_std += 1
    return rule

    
'''
Apply subsititutions
I/P
clause - [[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]
sub_map - {'a': 'Anakin'}
O/P
[[{'ViterbiSquirrel': ['Anakin']}, {'Secret': ['b']}, {'Tells': ['Anakin', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['Anakin']}]]

'''
def substitute(clause, sub_map):
    clause_str = str(clause)
    for key in sub_map.keys():
        is_no_cons = is_var(sub_map[key])
        key_temp = key
        val_temp = None
        while is_no_cons:
            is_no_cons = key_temp in sub_map and is_var(sub_map[key_temp])
            if is_no_cons: key_temp = sub_map[key_temp]
            
        if key_temp in sub_map:
            val_temp = sub_map[key_temp]
        else:
            val_temp = key_temp
            
        clause_str = clause_str.replace('\'{0}\''.format(key),'\'{0}\''.format(val_temp))
        
    return eval(clause_str)

def ressurect_fact(parsed_fact):
    fact = "{0}(".format(_get_term_one_fact(parsed_fact) )
    for var in _get_var_one_fact(parsed_fact):
        if is_var(var):
            var = "_"
        fact+="{0}, ".format(var)
    return "{0})".format(fact[:-2])

ressurect_fact(eval("{'Tells': ['Anakin', 'Pine', 'z2']}"))

# print _parse_one_fact("Knows(Sidious, Pine)")
# print _parse_one_fact("Traitor(Anakin)")

# print _parse_implication_facts("Resource(x) && Knows(Sidious, x)")
# print _parse_implication_facts("Enemy(Sidious, USC)")

# print parse_full_facts("Resource(x) && Knows(Sidious, x)")
# print parse_full_facts("Enemy(Sidious, USC)")
# print len(parse_full_facts("Enemy(Sidious, USC)"))
# print parse_full_facts("Resource(x) && Knows(Sidious, x) => Tells(Anakin, x, Sidious)")
# print parse_full_facts("Resource(x) => Secret(x)")
# print len(parse_full_facts("Resource(x) => Secret(x)"))


# print is_var('n')
# print is_var('n1')
# print is_var('n2')
# print is_var('Sidious')

# print is_constant('Sidious')
# print is_constant('USC')
# print is_constant('x')
# print is_constant('sidious')

# print unify(eval("{'Traitor': ['Anakin', 'x']}"), eval("{'Traitor': ['a', 'Bob']}") )
# print unify(eval("{'Traitor': ['a']}"), eval("{'Traitor': ['Anakin']}") )
# print unify(eval("{'Traitor': ['a']}"), eval("{'Traitor': ['b']}") )
# print unify(eval("{'Traitor': ['Anakin']}"), eval("{'Traitor': ['Anakin']}") )
# print unify(eval("{'Traitor': ['Anakin']}"), eval("{'ViterbiSquirrel': ['x']}") )

# print "[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"
# print substitute(eval("[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"), eval("{'a': 'Anakin'}") )
# print substitute(eval("[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"), eval("{'a': 'Anakin','b': 'Bnakin'}") )
# print substitute(eval("[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"), eval("{'x': 'Anakin'}") )

# print standardize_var(eval("[[{'Traitor': ['Anakin']}]]"))
# print standardize_var(eval("[[{'Traitor': ['x']}]]"))

# print substitute(eval("[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}]"), 
#                  eval("{'a': 'Anakin', 'c': 'Sidious', 'b': 'e', 'd': 'Pine', 'f': 'Sidious'}"))
# 
# print substitute(eval("[{'ViterbiSquirrel': ['a']}, {'Secret': ['e']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}]"), 
#                  eval("{'a': 'Anakin', 'c': 'Sidious', 'e': 'b', 'b': 'Pine', 'd': 'Pine', 'f': 'Sidious'}"))
# 
# print substitute(eval("[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}]"), 
#                  eval("{'a': 'Anakin', 'c': 'Sidious', 'b': 'e', 'e': 'Pine', 'd': 'Pine', 'f': 'Sidious'}"))

# print standardize_rule(eval("[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"))
# print standardize_rule(eval("[[{'Faster': ['Bob', 'Steve']}, {'Pig': ['Steve']}]]"))
# print standardize_rule(eval("[[{'Buffalo': ['x']}, {'Pig': ['y']}], [{'Faster': ['x', 'y']}]]"))
# print standardize_rule(eval("[[{'Pig': ['x']}, {'Slug': ['y']}], [{'Faster': ['x', 'y']}]]"))
# print standardize_rule(eval("[[{'Faster': ['Bob', 'Steve']}, {'Pig': ['Steve']}]]"))
# print standardize_rule(eval("[[{'Buffalo': ['x']}, {'Pig': ['y']}], [{'Faster': ['x', 'y']}]]"))
# print standardize_rule(eval("[[{'Pig': ['x']}, {'Slug': ['y']}], [{'Faster': ['x', 'y']}]]"))


