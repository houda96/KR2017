import math
import glob
import pycosat
import itertools
from itertools import combinations
from itertools import product
import re
from ast import literal_eval

dimension1 = 9
dimension2 = 9
numbers = 9
n = 9

rules = []

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
for r in range(dimension1):
    for v in range(numbers):
        clause = []
        for c in range(dimension2):
            clause.append(int(r*dimension2*numbers+c*dimension2+(v+1)))
        rules.append(clause)

# Rows uniqueness
for r in range(dimension1):
    for v in range(numbers):
        for ci in range(dimension2-1):
            for cj in range(ci+1, dimension2):
                rules.append([-int(r*dimension2*numbers+ci*dimension2+(v+1)),
                               -int(r*dimension2*numbers+cj*dimension2+(v+1))])

# Columns definedness
for c in range(dimension2):
    for v in range(numbers):
        clause = []
        for r in range(dimension1):
            clause.append(int(r*dimension2*numbers+c*dimension2+(v+1)))
        rules.append(clause)

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
for rOffset in range(sqrt1):
    for cOffset in range(sqrt2):
        for v in range(1, numbers+1):
            clause = []
            for r in range(sqrt1):
                for c in range(sqrt2):
                    num = int((rOffset*sqrt1 + r)*dimension2*numbers +
                                (cOffset*sqrt2 + c)*dimension2 + v)
                    clause.append(num)
            rules.append(clause)

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

def convert_killer_sudoku(file):
    n = 9
    cages = []
    f = open(file, "r")
    killer_sudoku = f.read().split('\n')[:-1]
    for cage in killer_sudoku:
        all_cells = re.findall(r"(\(.{4}\))", cage)
        sum_value = cage.split('=')[0]
        #new_cage = sum_value + "="+ ", ".join(all_cells)
        new_cage = (sum_value, all_cells)
        cages.append(new_cage)
    return cages

def find_combinations(cage):
    all_combis = []
    sum_value = int(cage[0])
    amount_cells = len(cage[1])
    print(cage, sum_value, amount_cells)
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for x in range(len(numbers)):
        for combi in combinations(numbers, x):
            if sum(combi) == sum_value and len(combi) == amount_cells:
                all_combis.extend([other_combi for other_combi in itertools.permutations(combi, amount_cells)])
    return all_combis

file_path = 'Data/KillerE/'
sudoku_number = '0.killer'
fileN = file_path + sudoku_number
cages = convert_killer_sudoku(fileN)
total_combis = []
newVars = 730
for cage in cages:
    combis = find_combinations(cage)
    cells = cage[1]
    lijst = []
    for combi in combis:
        if len(cells) == 1:
            cell = literal_eval(cells[0])
            v = combi[0]
            r = cell[0]
            c = cell[1]
            total_combis.append([int(r*dimension2*numbers+c*dimension2+(v))])
        else:
            combi_clauses = []
            for i in range(len(cells)):
                cell = literal_eval(cells[i])
                v = combi[i]
                r = cell[0]
                c = cell[1]
                combi_clauses.append(int(r*dimension2*numbers+c*dimension2+(v)))
            rest = combi_clauses[1:]
            for j in rest:
                total_combis.append([-int(newVars), j])
            lijst.append([combi_clauses[0], newVars])
            newVars += 1
    lijst = product(*lijst)
    for i in lijst:
        total_combis.append(list(i))
clauses= rules + total_combis

a = pycosat.solve(clauses)
print a
for i in range(9):
    for j in range(9):
        num = i*9*9 + j*9
        sublist = a[num:num+9]
        for elem in sublist:
            if elem > 0:
                print (elem-num),
        print(" ")
