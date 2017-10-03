import math
import glob
import subprocess
import pycosat

rules = []

# For 9x9
# dimension1 = 9
# dimension2 = 9
# numbers = 9
# n = 3

# # For 16x16
dimension1 = 16
dimension2 = 16
numbers = 16
n = 4


# TO TRY DIFFERENT ENCODINGS
# minimal: cell d, row u, column u, block u, assigned
# efficient: cell d, cell u, row u, column u, block u, assigned
# extended: cell d, cell u, row d, row u, column d, column u, block d, block u
    # assigned



# Cells definedness
for r in range(dimension1):
    for c in range(dimension2):
        clause = []
        for v in range(numbers):
            clause.append(int(r*dimension2*numbers+c*dimension2+(v+1)))
        rules.append(clause)

# Cells uniqueness
for r in range(dimension1):
    for c in range(dimension2):
        for vi in range(numbers-1):
            for vj in range(vi+1, numbers):
                rules.append([-int(r*dimension2*numbers+c*dimension2+(vi+1)),
                              -int(r*dimension2*numbers+c*dimension2+(vj+1))])

# Rows definedness
# for r in range(dimension1):
#     for v in range(numbers):
#         clause = []
#         for c in range(dimension2):
#             clause.append(int(r*dimension2*numbers+c*dimension2+(v+1)))
#         rules.append(clause)

# Rows uniqueness
for r in range(dimension1):
    for v in range(numbers):
        for ci in range(dimension2-1):
            for cj in range(ci+1, dimension2):
                rules.append([-int(r*dimension2*numbers+ci*dimension2+(v+1)),
                               -int(r*dimension2*numbers+cj*dimension2+(v+1))])

# Columns definedness
# for c in range(dimension2):
#     for v in range(numbers):
#         clause = []
#         for r in range(dimension1):
#             clause.append(int(r*dimension2*numbers+c*dimension2+(v+1)))
#         rules.append(clause)

# Columns uniqueness
for c in range(dimension2):
    for v in range(numbers):
        for ri in range(dimension1-1):
            for rj in range(ri+1, dimension1):
                rules.append([-int(ri*dimension2*numbers+c*dimension2+(v+1)),
                               -int(rj*dimension2*numbers+c*dimension2+(v+1))])

# Block definedness
sqrt1 = int(math.sqrt(dimension1))
sqrt2 = int(math.sqrt(dimension2))
# for rOffset in range(sqrt1):
#     for cOffset in range(sqrt2):
#         for v in range(1, numbers+1):
#             clause = []
#             for r in range(sqrt1):
#                 for c in range(sqrt2):
#                     num = int((rOffset*sqrt1 + r)*dimension2*numbers +
#                                 (cOffset*sqrt2 + c)*dimension2 + v)
#                     clause.append(num)
#             rules.append(clause)

# Block uniqueness
for v in range(1, numbers):
    for i in range(sqrt1):
        for j in range(sqrt2):
            for x in range(1, sqrt1+1):
                for y in range(1, sqrt2+1):
                    for k in range(y+1, sqrt2+1):
                        num = [-int((n*i+x-1) * dimension2 * numbers +
                                (n*j+y-1) * dimension2 + v),
                                -int((n*i+x-1) * dimension2 * numbers +
                                (n*j+k-1) * dimension2 + v)]
                        rules.append(num)

for v in range(1, numbers):
    for i in range(sqrt1):
        for j in range(sqrt2):
            for x in range(1, sqrt1+1):
                for y in range(1, sqrt2+1):
                    for k in range(x+1, sqrt2+1):
                        for l in range(1, sqrt2+1):
                            num = [-int((n*i+x-1) * dimension2 * numbers +
                                    (n*j+y-1) * dimension2 + v),
                                    -int((n*i+k-1) * dimension2 * numbers +
                                    (n*j+l-1) * dimension2 + v)]
                            rules.append(num)


def convert_sudoku(file, dimension1, dimension2):
    f = open(file, "r")
    sudoku = f.read().split(' \n')
    sudoku = [sud.split(' ') for sud in sudoku[:-1]]
    list_sudoku = []
    for r in range(dimension1):
        for c in range(dimension2):
            if int(sudoku[r][c]) != 0:
                list_sudoku.append([int(r*dimension2*numbers+
                                        c*dimension2+int(sudoku[r][c]))])
    return list_sudoku

file_path = 'Data/'
folder = "LargeE/"
for filee in glob.glob(file_path + folder + "*"):
     fixedRules = convert_sudoku(filee, dimension1, dimension2)
     clauses = rules + fixedRules
     pycosat.solve(clauses, verbose=1)
    # proc = subprocess.Popen(["python","-c","cnf = " + str(clauses) + ";import pycosat;a=pycosat.solve(cnf,verbose = 1);print(a)"], stdout = subprocess.PIPE).communicate()[0].decode('utf-8')
    # print(proc)


    #outputFile = open("DataDIMACS/" + folder + filee.split("/")[-1], "a")
    #outputFile.write("p cnf " + str(dimension1*dimension2*numbers) + " " +
#                        str(len(clauses)) + "\n")
    #for clause in clauses:
    #    for literal in clause:
    #        outputFile.write(str(literal) + " ")
    #    outputFile.write("0 \n")
    #outputFile.close()
#sudoku_number = '3463883_sudoku.txt'
#fileN = file_path + sudoku_number



# outputFile = open("DataCNF/NormalE/" + sudoku_number, "a")
# outputFile.write("p cnf " + str(dimension1*dimension2*numbers) + " " +
#                     str(len(clauses)) + "\n")
# for clause in clauses:
#     for literal in clause:
#         outputFile.write(str(literal) + " ")
#     outputFile.write("0 \n")
# outputFile.close()


# print(len(clauses))
# def writeOutput(final_list):
#     filename='CNF_sent.txt'
#     outputFile = open(filename,'a')
#     final = ["and"]
#     outputFile.write("5")
#     outputFile.write("\n")
#     for sentence in final_list:
#         ors = ["or"]
#         for elem in sentence:
#             if elem < 0:
#                 t = ["not", str(-1*elem)]
#             else:
#                 t = str(elem)
#             ors.append(t)
#         final.append(ors)
#     sentence=str(final)
#     #sentence=sentence.replace("\'","\"")
#     outputFile.write(sentence)
#     outputFile.close()
#
# writeOutput(clauses)


#print(pycosat.solve(clauses))
#print(len(list(pycosat.itersolve(clauses))))
