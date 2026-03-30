import argparse
def setup_arguments():
    parser = argparse.ArgumentParser(description="Truss Analysis Program")
    parser.add_argument("--nodes", type=str, default="SimpleTrussNodeData.csv", help="Input CSV file with truss data")
    parser.add_argument("--elements", type=str, default="SimpleTrussElementData.csv", help="Input CSV file with truss element data")
    return parser.parse_args()