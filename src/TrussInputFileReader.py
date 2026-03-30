# Reads Truss data from csv file and returns a matrix with the data
def read_data(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    fileMatrix = []
    i = 0
    for line in lines:
        #skip column names
        if i == 0:
           i+=1
           continue
       
        line = line.replace("\n","").split(",")
        fileMatrix.append(line)
        i+=1
    return fileMatrix
