import numpy as np
# Class with all the data and methods of a node
class TrussNode:

    def __init__(self, name,x, y,restX,restY,extForceX,extForceY):
        self.name = name
        self.x = x
        self.y = y
        self.restX = restX
        self.restY = restY
        self.extForceX = extForceX
        self.extForceY = extForceY
        # Initialize displacements and support reactions with 0, they will be calculated later
        self.dispX = 0
        self.dispY = 0
        self.supportReactionX = 0
        self.supportReactionY = 0

    
    def file_to_truss_node(fileMatrix):
        trussNodeList = []
        for line in fileMatrix:
            trussNodeList.append(TrussNode(line[0],float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5]),float(line[6])))
        return trussNodeList
    
    def get_ext_force_vector(nodes):
        extForceVector = []
        for node in nodes:
            extForceVector.append(node.extForceX)
            extForceVector.append(node.extForceY)
        return extForceVector
    
    def set_nodes_displacements(nodes,displacements):
        i=0
        for node in nodes:
            node.dispX = displacements[i]
            i+=1
            node.dispY = displacements[i]
            i+=1
    def set_nodes_support_reactions(nodes,support_reactions):
        i=0
        for node in nodes:
            node.supportReactionX = support_reactions[i]
            i+=1
            node.supportReactionY = support_reactions[i]
            i+=1


    def get_node_data_string(self):
        return f"Node {self.name} has support reactions: ({np.round(self.supportReactionX, decimals=8)}, {np.round(self.supportReactionY, decimals=8)}) and displacements: ({np.round(self.dispX, decimals=8)}, {np.round(self.dispY, decimals=8)}))"