import numpy as np
# Functions to manipulate the rigidity constants of the truss elements, and to find the normal forces in each element
def global_rigidity_matrix_spreading(local_rigidity_matrices,nodes,elements):
    mat_dim = 2*len(nodes)
    global_matrix = np.zeros((mat_dim,mat_dim))
    n=0
    for element in elements:
        i = element.node1.id
        j = element.node2.id
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
        i= element.node1.id
        j= element.node2.id
        disp_vector = np.array([displacements[2*i-2],displacements[2*i-1],displacements[2*j-2],displacements[2*j-1]])
        force_in_tips = local_rigidity_matrices[n] @ disp_vector
        normal_force = np.array([force_in_tips[0],force_in_tips[1]])
        normal_forces.append(normal_force)
        element.set_normal_force(normal_force)
        n+=1
    return np.array(normal_forces)