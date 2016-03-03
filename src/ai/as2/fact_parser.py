
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
    parsed_fact[fact[:i]] = fact[i+1:-1].split(", ")
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

def parse_full_facts(fact):
    parse_full_facts = []
    for f in fact.split(" => "):
        parse_full_facts.append(_parse_implication_facts(f))
    return parse_full_facts
        
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


