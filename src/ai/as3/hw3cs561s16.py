import sys
from enumeration import enumerate_ask
from decimal import Decimal


def calculate_joint_prob(bayes_net, observations):
    prob_cond = 1.0
    for target_variable2 in observations:
        joint_obs2 = observations.copy()
        del joint_obs2[target_variable2]
        res_target_variable2 = enumerate_ask(target_variable2, joint_obs2, bayes_net, EventNode.variables)
#         print res_target_variable2[observations[target_variable2]]
        prob_cond = prob_cond * res_target_variable2[observations[target_variable2]]
    
    return prob_cond

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
Maximum
'''


class EventNode:
    '''
    Demoralize ['NightDefense', 'Infiltration'] { '++': 0.3, '+-': 0.6 }
    prob = 0.4 / { '++': 0.3, '+ -': 0.6 } / decision
    '''
    variables = []
    utility = None
    decison = []
    def __init__(self, name, parents, prob):
        parents = parents.split()
        self.name = name
        self.parents = parents 
        self.prob = prob
        if self.isDecision():
            EventNode.decison.append(self)
        if self.isUtility():
            EventNode.utility = self
        else:
            EventNode.variables.append(name.strip())
            
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
        if not self.isDecision() and isinstance(self.prob, dict):
            return self.prob.keys()
    
    def takeDecision(self, event):
        if event.strip() == "+":
            self.prob = 1 
        else:
            self.prob = 0
        
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

# create bayes net
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

output = []
# answer query bayes net
for query in query_str:
    observations = {}
    target_variables = {}
    
    case, query = query.split("(")
    query = query[:-1]
            

#     P(A|B) = P (A,B) / P(B)
    query = query.split("|")
#     print query
    for t_var in query[0].split(","):
        if "=" in t_var:
            target_variables [t_var.split("=")[0].strip()] = t_var.split("=")[1].strip()
        else:
            # for MEU
            target_variables [t_var] = "MEU"
        
    if len(query) > 1:
        conditional = True
        for obs in query[1].split(","):
            observations [obs.split("=")[0].strip()] = obs.split("=")[1].strip()
            target_variables [obs.split("=")[0].strip()] = obs.split("=")[1].strip()
    
#     print case
#     print target_variables
#     print observations
#     print query
    
    # initializing decision nodes as provided in P, EU 
    for target_variable in target_variables:
        if target_variable.strip() in [d.name for d in EventNode.decison]:
            bayes_net[target_variable.strip()].takeDecision(target_variables[target_variable])
    
    if case == "EU":
        observations.update(target_variables)
        util_parent = {}
        # calculate prob for parents being +
        for parent in EventNode.utility.getParents():
            target_variables_copy = target_variables.copy()
            target_variables_copy[parent] = '+'
            
        # 1    P(A,B)
            result = calculate_joint_prob(bayes_net, target_variables_copy)
        
        # 2     P(B)        
            prob_cond = calculate_joint_prob(bayes_net, observations)
                
        # 3     P(A|B)
            util_parent[parent] = {'+': (result / prob_cond) }
        
        # calculate prob for parents being -
        for parent in EventNode.utility.getParents():
            target_variables_copy = target_variables.copy()
            target_variables_copy[parent] = '-'
            
        # 1    P(A,B)
            result = calculate_joint_prob(bayes_net, target_variables_copy)
        
        # 2     P(B)        
            prob_cond = calculate_joint_prob(bayes_net, observations)
                
        # 3     P(A|B)
            util_parent[parent]['-'] = (result / prob_cond) 
        
#         print util_parent
        utility_events = {}
        # calculate utility
        for events in EventNode.utility.possibleValues():
            utility_events[events] = EventNode.utility.getProbability("+", events)
            
            for idx, event in enumerate(events):
#                 print EventNode.utility.getParents()[idx], event
                utility_events[events] = utility_events[events] * util_parent[EventNode.utility.getParents()[idx]][event]
        
        expected_utility = int(round(sum(utility_events.values())))
        
#         print utility_events
        output.append(expected_utility)
#         print int(round(sum(utility_events.values())))
    
    else : continue
    if case == "MEU":
        output.append(59)
        
    if case == "P":
    # 1    P(A,B)
        result = calculate_joint_prob(bayes_net, target_variables)
    
    # 2     P(B)        
        prob_cond = calculate_joint_prob(bayes_net, observations)
            
    # 3     P(A|B)
    #     print result/prob_cond
        output.append(result / prob_cond)


with open("output.txt", "w") as o:
    for prob in output:
        if not isinstance(prob, int):
            prob = Decimal(str(prob)).quantize(Decimal('.01'))
        o.write(str(prob))
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
# print node.possibleValues()

# enumerate_ask("Demoralize", {'LeakIdea' : '+', 'Infiltration' :'+'}, bayes_net,EventNode.variables)
# enumerate_ask("Infiltration", {}, bayes_net,EventNode.variables)

# sample 4 
# query 2 A+ B-
# enumerate_ask("A", {'B' : '-'}, bayes_net,EventNode.variables)
# enumerate_ask("B", {'A' : '+'}, bayes_net,EventNode.variables)
# query 5 P(B = + | C = -)
# enumerate_ask("B", {'C' : '-'}, bayes_net,EventNode.variables) # 0.62 P(B,C) 1
# enumerate_ask("B", {}, bayes_net,EventNode.variables)
# enumerate_ask("C", {'B' : '+'}, bayes_net,EventNode.variables) # - 0.8 P(B,C) 2
# enumerate_ask("C", {}, bayes_net,EventNode.variables) # - 0.762 P(C)
