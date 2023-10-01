import pandas as pd
import pyranges as pr
import sys
import csv
import os

## tells us the bedfile is the first input in the bash command
filteredFile = sys.argv[1]
AsiSIFile = sys.argv[2]
file_name = sys.argv[1].replace('_filtered.bed', '_overlap.bed')

## execute the timer function
timedecorator_file_path = os.path.join(os.path.dirname(__file__), "time.py")
exec(open(timedecorator_file_path).read())
@timer_func
## Let's create a function to help us answer question 4 to find the number of unique sites that overlap with AsiSI break sites
def overlap(filtered, AsiSI):
    filtered = pd.read_csv(filtered, delimiter='\t')
    Asibed = pd.read_csv(AsiSI, delimiter='\t', header=None)
    asicols = "Chromosome Start End".split()
    Asibed.columns = asicols
    # using pyranges let's make two grange objects 
    gr1, gr2 = pr.PyRanges(filtered), pr.PyRanges(Asibed)
    # intersect the two granges
    gr = gr2.overlap(gr1)
    # Create a dataframe from the overlap genomic ranges
    AsiSI_intersect = gr.df
    return AsiSI_intersect.to_csv(file_name, sep='\t', index=False)

overlap(filteredFile, AsiSIFile)