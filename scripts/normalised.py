import pandas as pd
import pyranges as pr
import sys
import csv

## tells us the bedfile is the first input in the bash command
filteredFile = sys.argv[1]
intersectFile = sys.argv[2]
overlapFile = sys.argv[3]
file_name = sys.argv[1].replace('.breakends_filtered.bed', '')

def countlines(inputbed):
    with open(inputbed, 'r') as bed:
        for count, line in enumerate(bed):
            pass
    return count

total=countlines(filteredFile)
AsiSIbreaks=countlines(intersectFile)
total_normalised=total/1000
normalise=AsiSIbreaks/total_normalised

overlaps=countlines(overlapFile)

output = pd.DataFrame([[total,AsiSIbreaks,normalise,overlaps,file_name]])
output.to_csv('normalised.txt', sep='\t',header=None, index=False)