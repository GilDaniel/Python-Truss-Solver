import numpy as np

# Element is an object of TrussElement, points is a list of TrussNode
def rigidity_constant(element,nodes):

    lengthVector = np.matrix([[nodes[element.node2ID-1].x-nodes[element.node1ID-1].x],[nodes[element.node2ID-1].y-nodes[element.node1ID-1].y]]);
    length = np.sqrt(lengthVector[0].item()**2 + lengthVector[1].item()**2).item();
    theta = np.arctan2(lengthVector[1].item(),lengthVector[0].item()).item();
    k= np.array([ [np.cos(theta)**2,                np.cos(theta)*np.sin(theta),    -np.cos(theta)**2,              -np.cos(theta)*np.sin(theta)],
                  [np.cos(theta)*np.sin(theta),     np.sin(theta)**2,               -np.cos(theta)*np.sin(theta),   -np.sin(theta)**2],
                  [-np.cos(theta)**2,               -np.cos(theta)*np.sin(theta),   np.cos(theta)**2,               np.cos(theta)*np.sin(theta)],
                  [-np.cos(theta)*np.sin(theta),    -np.sin(theta)**2,              np.cos(theta)*np.sin(theta),    np.sin(theta)**2]])
    
    return (element.elastic_modulus*element.section_area/length)*np.round(k,decimals=10)
    

def global_rigidity_matrix_spreading(local_rigidity_matrices,nodes,elements):
    mat_dim = 2*len(nodes)
    global_matrix = np.zeros((mat_dim,mat_dim))
    n=0
    for element in elements:
        i = element.node1ID
        j = element.node2ID
        global_matrix[2*i-2,2*i-2] += local_rigidity_matrices[n][0,0]  
        global_matrix[2*i-2,2*i-1] += local_rigidity_matrices[n][0,1]
        global_matrix[2*i-2,2*j-2] += local_rigidity_matrices[n][0,2]
        global_matrix[2*i-2,2*j-1] += local_rigidity_matrices[n][0,3]
        global_matrix[2*i-1,2*i-2] += local_rigidity_matrices[n][1,0]
        global_matrix[2*i-1,2*i-1] += local_rigidity_matrices[n][1,1]
        global_matrix[2*i-1,2*j-2] += local_rigidity_matrices[n][1,2]
        global_matrix[2*i-1,2*j-1] += local_rigidity_matrices[n][1,3]
        global_matrix[2*j-2,2*i-2] += local_rigidity_matrices[n][2,0]
        global_matrix[2*j-2,2*i-1] += local_rigidity_matrices[n][2,1]
        global_matrix[2*j-2,2*j-2] += local_rigidity_matrices[n][2,2]
        global_matrix[2*j-2,2*j-1] += local_rigidity_matrices[n][2,3]
        global_matrix[2*j-1,2*i-2] += local_rigidity_matrices[n][3,0]
        global_matrix[2*j-1,2*i-1] += local_rigidity_matrices[n][3,1]
        global_matrix[2*j-1,2*j-2] += local_rigidity_matrices[n][3,2]
        global_matrix[2*j-1,2*j-1] += local_rigidity_matrices[n][3,3]

        n+=1
   
    return global_matrix

def apply_countour_conditions(global_matrix,nodes):
    i=0
    for n in range(len(nodes)):
        if nodes[n].restX == 1:
            global_matrix[i,:] = 0
            global_matrix[:,i] = 0
            global_matrix[i,i] = 1
            nodes[n].extForceX = 0
        i+=1
        if nodes[n].restY == 1:
            global_matrix[i,:] = 0
            global_matrix[:,i] = 0
            global_matrix[i,i] = 1
            nodes[n].extForceY = 0
        i+=1
    return global_matrix

def find_normal_forces(local_rigidity_matrices,elements,displacements):
    normal_forces = []
    n=0
    for element in elements:
        i= element.node1ID
        j= element.node2ID
        disp_vector = np.array([displacements[2*i-2],displacements[2*i-1],displacements[2*j-2],displacements[2*j-1]])
        normal_forces.append(local_rigidity_matrices[n] @ disp_vector)
        element.set_element_normal_force(normal_forces[-1])
        n+=1
    return np.array(normal_forces)