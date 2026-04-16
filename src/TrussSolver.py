import RigidityConstant as rc
import TrussInputFileReader as tr
import TrussNode as tn
import TrussElement as te
import numpy as np
import ArgumentParseSetup as args

data_args = args.setup_arguments()
# Read truss data from sheets 
node_data = tr.read_data(f"../data/{data_args.nodes}")
element_data = tr.read_data(f"../data/{data_args.elements}")

# Convert data to nodes and elements
nodes = tn.TrussNode.file_to_truss_node(node_data)
elements = te.TrussElement.file_to_truss_element(element_data)

# Calculate rigidity matrices for each element
local_rigidity_matrices = []
for element in elements:
    local_rigidity_matrices.append(element.calc_local_rigidity_constant(nodes))

# Spread local rigidity matrices to global matrix
rig_matrix = rc.global_rigidity_matrix_spreading(local_rigidity_matrices,nodes,elements)

# Get external force vector
ext_force_vector = tn.TrussNode.get_ext_force_vector(nodes)

# Apply contour conditions to global matrix
rig_matrix_with_contour = np.copy(rig_matrix)
rig_matrix_with_contour = rc.apply_countour_conditions(rig_matrix_with_contour,nodes)

# Solve linear system for displacements
displacements = np.linalg.solve(rig_matrix_with_contour,ext_force_vector)
tn.TrussNode.set_nodes_displacements(nodes,displacements)

# Calculate support reactions
support_reactions = rig_matrix @ displacements - ext_force_vector
tn.TrussNode.set_nodes_support_reactions(nodes,support_reactions)

# Calculate normal forces in each element
normal_forces = rc.find_normal_forces(local_rigidity_matrices,elements,displacements)




print("--------------DETAILED DATA--------------\n");
print("Rigidity Matrix: \n", rig_matrix_with_contour)
print("External Force Vector: \n", ext_force_vector)
print("Displacements: \n", displacements)
print("Support Reactions: \n", support_reactions)
print("Normal Forces: \n", normal_forces)

print("\n--------------SUMMARY--------------\n");
for element in elements:
    print(element.get_data_string(nodes),"\n")
for node in nodes:
    print(node.get_node_data_string())