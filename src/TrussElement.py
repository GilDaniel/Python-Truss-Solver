import numpy as np
# Class with all the data and methods of a truss element
class TrussElement:

    def __init__(self, node1ID, node2ID, elastic_modulus,section_area):
        self.node1ID = node1ID
        self.node2ID = node2ID
        self.elastic_modulus = elastic_modulus
        self.section_area = section_area

    def file_to_truss_element(fileMatrix):
        trussElementList = []
        for line in fileMatrix:
            trussElementList.append(TrussElement(int(line[0]),int(line[1]),float(line[2]),float(line[3])))
        return trussElementList
    
    def calc_local_rigidity_constant(self,nodes):

        element_length_vector = np.matrix([[nodes[self.node2ID-1].x-nodes[self.node1ID-1].x],[nodes[self.node2ID-1].y-nodes[self.node1ID-1].y]]);
        element_length = np.sqrt(element_length_vector[0].item()**2 + element_length_vector[1].item()**2).item();

        theta = np.arctan2(element_length_vector[1].item(),element_length_vector[0].item()).item();
        
        #Precalculate sin and cos of theta
        sint = np.sin(theta)
        cost = np.cos(theta)

        #Calculate local rigidity constant matrix 
        k= np.array([ [cost**2,       cost*sint,    -cost**2,     -cost*sint],
                      [cost*sint,     sint**2,      -cost*sint,   -sint**2],
                      [-cost**2,      -cost*sint,   cost**2,      cost*sint],
                      [-cost*sint,    -sint**2,     cost*sint,    sint**2]])
        
        return (self.elastic_modulus*self.section_area/element_length)*k
    
    
    def set_normal_force(self,normal_force):
        self.normal_force = normal_force

    def get_data_string(self,nodes):

        truss_direction_vector = np.array([nodes[self.node2ID-1].x - nodes[self.node1ID-1].x, nodes[self.node2ID-1].y - nodes[self.node1ID-1].y])
        
        normal_force_modulus = np.sqrt(self.normal_force[0]**2 + self.normal_force[1]**2)
        
        force = self.normal_force[0:2]

        #If the normal force is aligned with the truss direction vector, then it's tension, otherwise it's compression.
        if normal_force_modulus <= 0e-10:
            return f"Truss element {nodes[self.node1ID-1].name}-{nodes[self.node2ID-1].name} has a null normal force."
        elif force.dot(truss_direction_vector) < 0:
            force_type = "Tension"
        else:
            force_type = "Compression"

        return f"Truss element {nodes[self.node1ID-1].name}-{nodes[self.node2ID-1].name} has a {force_type} normal force: {np.round(normal_force_modulus,decimals=8)}"