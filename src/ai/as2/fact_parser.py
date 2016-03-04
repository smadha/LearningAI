
'''
Takes input one single fact. 
No conjunction of multiple facts
return function followed by parameters in same order
I/P STR  -> 'Knows(Sidious,Pine)'
O/P DICT -> {'Knows' : ['Sidious','Pine'] }
'''
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
    return len(name) == 1 and name.islower()
'''
I/P dict
I/P - {'Traitor': ['x']}
O/P - return Traitor
'''
def _get_term_one_fact(fact):
    return fact.keys()[0]

def get_match_fact(knowledge, query):
    '''
    knowledge = KB
    query = {'Enemy': ['Sidious', 'USC']}
    '''
    q_term = _get_term_one_fact(query)
    for k in knowledge:  # sample k = "[[{'Resource': ['x']}], [{'Secret': ['x']}]]"
        if len(k) == 2:  # if implication take RHS
            for fact in k[1]:  # sample k[1] = "[{'Secret': ['x']}]"
                if q_term == _get_term_one_fact(fact):
#                     print fact, k
                    return k[:]
        else:  # sample k = "[[{'Enemy': ['Sidious', 'USC']}]]"
            for fact in k[0]:  # sample k[0] = "[{'Enemy': ['Sidious', 'USC']}]"
                if q_term == _get_term_one_fact(fact):
#                     print fact, k
                    return k[:]
def unify(fact1, fact2):
    '''
    I/P {'Traitor': ['Anakin']}"), "{'Traitor': ['a']}
    O/P {'a':'Anakin'}
    '''
    res = {}
    f1_params = enumerate(fact1.values()[0])
    f2_params = fact2.values()[0]
    for idx, p1 in f1_params:
        p2 = f2_params[idx]
        if (is_var(p1)):
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
        clause_str = clause_str.replace('\'{0}\''.format(key),'\'{0}\''.format(sub_map[key]))
        
    return eval(clause_str)
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
# print is_var('Sidious')
# 
# print is_constant('Sidious')
# print is_constant('USC')
# print is_constant('x')
# print is_constant('sidious')

# print unify(eval("{'Traitor': ['Anakin', 'x']}"), eval("{'Traitor': ['a', 'Bob']}") )
# print unify(eval("{'Traitor': ['a']}"), eval("{'Traitor': ['Anakin']}") )
# print unify(eval("{'Traitor': ['a']}"), eval("{'Traitor': ['b']}") )
# print unify(eval("{'Traitor': ['Anakin']}"), eval("{'Traitor': ['Anakin']}") )

# print "[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"
# print substitute(eval("[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"), eval("{'a': 'Anakin'}") )
# print substitute(eval("[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"), eval("{'a': 'Anakin','b': 'Bnakin'}") )
# print substitute(eval("[[{'ViterbiSquirrel': ['a']}, {'Secret': ['b']}, {'Tells': ['a', 'b', 'c']}, {'Hostile': ['c']}], [{'Traitor': ['a']}]]"), eval("{'x': 'Anakin'}") )

# print standardize_var(eval("[[{'Traitor': ['Anakin']}]]"))
# print standardize_var(eval("[[{'Traitor': ['x']}]]"))
