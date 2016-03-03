# # Final executable
import sys
from fact_parser import parse_full_facts

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
print query

print len(knowledge)

knowledge = [parse_full_facts(k) for k in knowledge]
print "\n".join([str(k) for k in knowledge])
print "---"






