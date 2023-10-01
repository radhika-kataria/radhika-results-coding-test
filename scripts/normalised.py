import pandas as pd
import pyranges as pr
import sys
import csv
import os

## Define the input files
filteredFile = sys.argv[1]
intersectFile = sys.argv[2]
overlapFile = sys.argv[3]

## Get the sample names to print in the output at the end
file_name = sys.argv[1].replace('.breakends_filtered.bed', '')

## execute the timer function
timedecorator_file_path = os.path.join(os.path.dirname(__file__), "time.py")
exec(open(timedecorator_file_path).read())
@timer_func

## Function to count the number of lines in the bed file to give us the total number of breaks in a sample
def countlines(inputbed):
    with open(inputbed, 'r') as bed:
        for count, line in enumerate(bed):
            pass
    return count

## Execute the function to get the total number of filtered breaks found in each sample
total=countlines(filteredFile)

## Count number of filtered breaks found in each sample that overlap with AsiSI breaks
AsiSIbreaks=countlines(intersectFile)

## Divide the filtered breaks by 1000
total_normalised=total/1000

## Divide the number of breaks in each sample overlapping an AsiSI break site by the total number of break sites
normalise=AsiSIbreaks/total_normalised

## Count the number of unique AsiSI break sites found in each sample
overlaps=countlines(overlapFile)

## Collate all the above sum of break sites in a dataframe with the sample name
output = pd.DataFrame([[total,AsiSIbreaks,normalise,overlaps,file_name]])

## Print outputs
output.to_csv('normalised.txt', sep='\t',header=None, index=False)