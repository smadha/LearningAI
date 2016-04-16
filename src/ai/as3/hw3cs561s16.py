import sys
from enumeration import enumerate_ask
from decimal import Decimal

ip_file = sys.argv[2]
print ip_file

SEP_QUERY = "******"
SEP_NODE = "***"

query_observations = []
query_str = []
'''
Key - Node name
Value - EventNode
'''
bayes_net = {}

'''
Utilty
Decison
Bayes
Maximum
'''


class EventNode:
    '''
    Demoralize ['NightDefense', 'Infiltration'] { '++': 0.3, '+-': 0.6 }
    prob = 0.4 / { '++': 0.3, '+ -': 0.6 } / decision
    '''
    variables = []
    def __init__(self, name, parents, prob):
        parents = parents.split()
        EventNode.variables.append(name.strip())
        self.name = name
        self.parents = parents 
        self.prob = prob

    def displayParents(self):
        print "parents " , self.parents
    
    def hasParents(self):
        return len(self.parents) > 0
    
    def getParents(self):
        return self.parents
    
    def isDecision(self):
        return str(self.prob) == "decision"
    
    def isUtility(self):
        return str(self.name) == "utility"
    
    def possibleValues(self):
        if not self.isUtility() and not self.isDecision() and isinstance(self.prob, dict):
            return self.prob.keys()
        
    def getProbability(self, event, observation):
        '''
        event = +/-
        observation = parent's observation
        '''
        prob_calc = 1
        if self.hasParents():
            prob_calc = self.prob[observation]
        else :
            prob_calc = self.prob
        
#         print self.name, event, observation, self.prob, prob_calc
        if event.strip() == "+":
            return prob_calc 
        else:
            return 1 - prob_calc
        
    
    def __str__(self):
        '''
        Demoralize ['NightDefense', 'Infiltration'] { '++': 0.3, '+ -': 0.6 }
        '''
        return " ".join([self.name, str(self.parents), str(self.prob)])
    
    def __repr__(self):
        return self.__str__()


with open(ip_file, 'r') as f:
    line = f.readline()
    addQuery = True 
    while(line):
        line = line.strip()
        if (line == SEP_QUERY):
            addQuery = False
        else:
            if (line == SEP_NODE):
                line = f.readline()
                continue
            if  addQuery:
                query_str.append(line)
            else :  # add node
                node_parent = line.split("|")
                name = node_parent[0].strip()
                parent = ""
                prob = {}
                if len(node_parent) > 1:
                    parent = node_parent[1].strip()
                    prob = {}
                    for par in range(pow(2, len(parent.split(" ")))):
                        line = f.readline().strip()
                        prob[''.join(line.split()[1:])] = float(line.split()[0])
                else:
                    prob = f.readline().strip()
                    if prob != 'decision':
                        prob = float(prob)
                bayes_net[name] = EventNode(name , parent, prob)
                
        line = f.readline()
    
    print bayes_net


# enumerate_ask("Demoralize", {'LeakIdea' : '+', 'Infiltration' :'+'}, bayes_net,EventNode.variables)
# enumerate_ask("Infiltration", {}, bayes_net,EventNode.variables)

# sample 4 
# query 2 A+ B-
# enumerate_ask("A", {'B' : '-'}, bayes_net,EventNode.variables)
# enumerate_ask("B", {'A' : '+'}, bayes_net,EventNode.variables)
# P(B = + | C = -)
# enumerate_ask("B", {'C' : '-'}, bayes_net,EventNode.variables)
# enumerate_ask("B", {}, bayes_net,EventNode.variables)
# enumerate_ask("C", {'B' : '+'}, bayes_net,EventNode.variables)
# enumerate_ask("C", {}, bayes_net,EventNode.variables)

output = []
for query in query_str:
    observations = {}
    target_variables = {}
    possible_case = ["P", "EU", "MEU"]
    
    case,query = query.split("(")
    query = query[:-1]
    
    query = query.split("|")

    for t_var in query[0].split(","):
        target_variables [t_var.split("=")[0].strip()] = t_var.split("=")[1].strip()
    if len(query) > 1:
        for obs in query[1].split(","):
            observations [obs.split("=")[0].strip()] = obs.split("=")[1].strip()
    
#     print case
#     print target_variables
#     print observations
#     print query
    result = 1.0
    
    for target_variable in target_variables:
        joint_obs = target_variables.copy()
        del(joint_obs[target_variable])
        joint_obs.update(observations)
#         
        res_target_variable = enumerate_ask(target_variable, joint_obs, bayes_net,EventNode.variables)
#         print res_target_variable[target_variables[target_variable]]
        result = result * res_target_variable[target_variables[target_variable]]
        
        
    output.append(result)


with open("output.txt", "w") as o:
    for prob in output:
        prob = Decimal(str(prob)).quantize(Decimal('.01'))
        o.write(str(prob) )
        o.write("\n")
    
# node = EventNode('Demoralize' ,'NightDefense Infiltration',{'++': .3 , '+-':0.6 })
# print node.hasParents()
# print node.possibleValues()
# node = EventNode('Demoralize' ,'',0.6 )
# print node.hasParents()
# print node.isDecision()
# print node.possibleValues()
# node = EventNode('Demoralize' ,'',"decision")
# print node.isDecision()
# print node.possibleValues()
# node = EventNode('utility' ,'',{'++': .3 , '+ -':0.6 })
# print node.isUtility()
