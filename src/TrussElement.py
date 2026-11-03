import numpy as np
# Class with all the data and methods of a truss element
class TrussElement:

    def __init__(self, node1, node2, elastic_modulus,section_area, Ix,Iz,Ixz):
        self.node1 = node1
        self.node2 = node2
        self.elastic_modulus = elastic_modulus
        self.section_area = section_area
        self.Ix = Ix
        self.Iz = Iz
        self.Ixz = Ixz

        self.max_I = 0.5*(Ix + Iz) + np.sqrt(((Ix-Iz)*0.5)**2 + Ixz**2)
        self.min_I = 0.5*(Ix + Iz) - np.sqrt(((Ix-Iz)*0.5)**2 + Ixz**2)
        self.max_inertia_angle = 0.5*np.arctan2(2*Ixz,Ix-Iz)
        self.min_inertia_angle = self.max_inertia_angle + np.pi/2

        self.truss_direction_vector = np.array([self.node2.x- self.node1.x, self.node2.y - self.node1.y])
        self.truss_length = np.sqrt(self.truss_direction_vector[0]**2 + self.truss_direction_vector[1]**2)     
        self.theta = np.arctan2(self.truss_direction_vector[1],self.truss_direction_vector[0]).item();
                
    @staticmethod
    def file_to_truss_element(fileMatrix,nodes):
        trussElementList = []
        for line in fileMatrix:
            node1 = nodes[int(line[0])-1]
            node2 = nodes[int(line[1])-1]
            trussElementList.append(TrussElement(node1, node2,float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6])))
        return trussElementList
  
    def calc_local_rigidity_constant(self,nodes):

        #Precalculate sin and cos of theta
        sint = np.sin(self.theta)
        cost = np.cos(self.theta)

        #Calculate local rigidity constant matrix 
        k= np.array([ [cost**2,       cost*sint,    -cost**2,     -cost*sint],
                      [cost*sint,     sint**2,      -cost*sint,   -sint**2],
                      [-cost**2,      -cost*sint,   cost**2,      cost*sint],
                      [-cost*sint,    -sint**2,     cost*sint,    sint**2]])
        
        return (self.elastic_modulus*self.section_area/self.truss_length)*k
    
   
    def set_normal_force(self,normal_force):
        self.normal_force = normal_force
        self.normal_force_modulus = np.sqrt(normal_force[0]**2 + normal_force[1]**2)
        self.calculate_load()

    def calculate_load(self):
        #If the normal force is aligned with the truss direction vector, then it's tension, otherwise it's compression.
        if self.normal_force_modulus <= 0e-10:
            return f"Truss element {self.node1.name}-{self.node2.name} has a null normal force."
        elif self.normal_force.dot(self.truss_direction_vector) < 0:
            self.force_type = "Tension"
        else:
            self.force_type = "Compression"
            self.critical_buckling_load = self.calculate_critical_buckling_load()
            self.critical_buckling_tension = self.critical_buckling_load/self.section_area
            self.radius_of_gyration = np.sqrt(self.min_I/self.section_area)
            self.slenderness_ratio = self.truss_length/self.radius_of_gyration
            
        self.tension = self.calculate_tension()

    def calculate_tension(self):
        return self.normal_force_modulus/self.section_area
   
    def calculate_critical_buckling_load(self):
        # Calculate the critical buckling load using Euler's formula
        # P_cr = (pi^2 * E * I) / (K * L)^2
        # where K is the effective length factor, L is the length of the element, E is the elastic modulus, and I is the moment of inertia.
       
        
        # Assuming pinned-pinned boundary conditions since its a truss element, K = 1.0
        # Using the minimum moment of inertia for buckling calculations
        
        P_cr = (np.pi**2 * self.elastic_modulus * self.min_I) / (1 * self.truss_length)**2
        return P_cr

    def get_data_string(self,nodes):

        
        if self.normal_force_modulus <= 0e-10:
            return f"Truss element {self.node1.name}-{self.node2.name} has a null normal force."
        elif self.force_type == "Tension":
            return f"Truss element {self.node1.name}-{self.node2.name} has a {self.force_type} normal force: {np.round(self.normal_force_modulus,decimals=8)} and a tension of: {np.round(self.tension,decimals=8)}"
        else:
            return f"Truss element {self.node1.name}-{self.node2.name} has a {self.force_type} normal force: {np.round(self.normal_force_modulus,decimals=8)}, a tension of: {np.round(self.tension,decimals=8)}, a critical buckling load of: {np.round(self.critical_buckling_load,decimals=8)}, a critical buckling tension of: {np.round(self.critical_buckling_tension,decimals=8)}, a radius of gyration of: {np.round(self.radius_of_gyration,decimals=8)}, and a slenderness ratio of: {np.round(self.slenderness_ratio,decimals=8)}"
    