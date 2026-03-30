import numpy as np
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
    
    def set_element_normal_force(self,normal_force):
        self.normal_force = normal_force

    def get_data_string(self,nodes):
        truss_direction_vector = np.array([nodes[self.node2ID-1].x - nodes[self.node1ID-1].x, nodes[self.node2ID-1].y - nodes[self.node1ID-1].y])
        normal_force_modulus = np.sqrt(self.normal_force[0]**2 + self.normal_force[1]**2)
        force = self.normal_force[0:2]

        if normal_force_modulus <= 0e-10:
            return f"Truss element {nodes[self.node1ID-1].name}-{nodes[self.node2ID-1].name} has a null normal force."
        elif force.dot(truss_direction_vector) < 0:
            force_type = "Tension"
        else:
            force_type = "Compression"

        return f"Truss element {nodes[self.node1ID-1].name}-{nodes[self.node2ID-1].name} has a {force_type} normal force: {normal_force_modulus}"