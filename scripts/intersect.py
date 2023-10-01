import pandas as pd
import pyranges as pr
import sys
import csv
import os

## tells us the bedfile is the first input in the bash command
filteredFile = sys.argv[1]
AsiSIFile = sys.argv[2]
file_name = sys.argv[1].replace('_filtered.bed', '_intersect.bed')

## execute the timer function
timedecorator_file_path = os.path.join(os.path.dirname(__file__), "time.py")
exec(open(timedecorator_file_path).read())

## Create a function to find the intersect between the filtered bed file and AsiSI break sites
@timer_func
def intersect(filtered, AsiSI):
    filtered = pd.read_csv(filtered, delimiter='\t')
    Asibed = pd.read_csv(AsiSI, delimiter='\t', header=None)
    asicols = "Chromosome Start End".split()
    Asibed.columns = asicols
    # using pyranges let's make two genomic range objects 
    gr1, gr2 = pr.PyRanges(filtered), pr.PyRanges(Asibed)
    # intersect the two genomic ranges
    gr = gr1.intersect(gr2)
    # Create a dataframe from the intersected ranges
    AsiSI_intersect = gr.df
    return AsiSI_intersect.to_csv(file_name, sep='\t', index=False)

intersect(filteredFile, AsiSIFile)