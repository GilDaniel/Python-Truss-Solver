# Python Truss Solver

A Python tool for analyzing isostatic (statically determinate) and hyperstatic
(statically indeterminate) truss structures with a simplified Finite Element
Method (FEM).

The solver calculates nodal displacements, support reactions, and axial forces
in each member. It assumes linear-elastic material behavior and small
displacements.

## Features

- Reads node and element data from CSV files.
- Calculates nodal displacements, support reactions, and member axial forces.
- Reports axial stress and, for compression members, the Euler critical
  buckling load and stress.
- Plots the truss geometry and analysis results:
  - Blue members are in tension; red members are in compression.
  - Axial stresses are shown in MPa; compression members also show the Euler
    critical buckling stress.
  - Applied X and Y forces are drawn as separate colored arrows.
  - Nodes and restrained supports are marked on the plot.

## Requirements

- Python
- NumPy
- Matplotlib

Install the required packages:

```bash
pip install numpy matplotlib
```

## Usage

Run the solver with the default input files:

```bash
python TrussSolver.py
```

Specify alternative CSV files with:

```bash
python TrussSolver.py --nodes MyNodeData.csv --elements MyElementData.csv
```

The files are resolved relative to the `data` directory. Each node row must
provide its name, X and Y coordinates, X and Y restraint flags, and external X
and Y forces. Each element row must provide the indices of its two nodes
(starting at 1), elastic modulus, cross-sectional area, and section inertia
values `Ix`, `Iz`, and `Ixz`.

Use a consistent unit system for all input values. For example, with
coordinates in meters, use pascals for elastic modulus, square meters for area,
and fourth-power meters for moments of inertia.

## Assumptions and limitations

- Linear-elastic material behavior and small displacements.
- The Euler buckling calculation assumes pinned-pinned members (`K = 1`) and
  uses the smaller principal section inertia.
- Euler buckling results describe ideal elastic buckling; they do not account
  for inelastic buckling, imperfections, or design-code resistance factors.
- Intended primarily for educational use and basic structural analysis.

## License

MIT License

Special thanks to Prof. Dr. Edson Denner Leonel for providing theoretical
background and study materials for this implementation.
