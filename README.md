# Python Truss Solver

## Overview
A Python tool for solving both isostatic (statically determinate) and hyperstatic (statically indeterminate) truss structures.

It uses a simplified Finite Element Method (FEM) approach based on the principle of superposition and Hooke’s Law to compute nodal displacements. From these results and the applied boundary conditions, the solver calculates internal axial forces in each member and the support reactions.

The model assumes linear-elastic material behavior and small deformations.

---

## Features
- Reads truss data (nodes and elements) from `.csv` files  
- Computes:
  - Nodal displacements  
  - Axial forces in each element  
  - Support reactions  
- Works for both isostatic and hyperstatic structures  

---

## Technologies
- **Python**
- **NumPy** (for matrix operations and solving linear systems)

---


## Installation

1. Install Python:  
   https://www.python.org/downloads/

2. Install dependencies:
   ```bash
   pip install numpy argparse
   
3. Clone the repository:
   ```bash
    git clone https://github.com/GilDaniel/Python-Truss-Solver.git
4. Run:
  If using the default files 'SimpleTrussNodeData.csv' and 'SimpleTrussElementData.csv' just run: 
    ```bash
    python main.py 
  If you wish to specify your own node data and element data:
    
    python main.py --nodes MyNodeDataName.csv --elements MyElementsData.csv
    
## Notes
  Assumes linear-elastic behavior
  Valid for small deformations
  Mainly intended for learning and basic structural analysis
## License
  MIT License


Special thanks to Prof. Dr. Edson Denner Leonel for providing theorical info and studying material for this implementation
