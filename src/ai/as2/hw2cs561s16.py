# # Final executable
import sys
from fact_parser import *
from FOL_BC import *

ip_file = sys.argv[2]
print ip_file

query = ''
knowledge = []

with open(ip_file, 'r') as f:
    line = f.readline().strip()
    query = line
#    print line
    #ignore number count 
    f.readline()
    line = f.readline().strip()
    while line:
#        print line
        knowledge.append(line)
        line = f.readline().strip()
    f.close()
    print query
    print len(knowledge)
    print "\n".join(knowledge)
    print "---"

query = parse_full_facts(query)
knowledge = [parse_full_facts(k) for k in knowledge]
# print query
# print len(knowledge)
# print "\n".join([str(k) for k in knowledge])
# print "---"


# print get_match_fact(knowledge,eval("{'Traitor': ['Anakin']}"))
# print get_match_fact(knowledge,eval("{'Enemy': ['Sidious','x']}") )
# print "---",get_match_fact(knowledge,eval("{'ViterbiSquirrel': ['Anakin']}") )

query = standardize_var(query)
print query
knowledge = standardize(knowledge)
print "\n".join([str(k) for k in knowledge])
print "---"

FOL_BC_ASK(knowledge, query[0])
