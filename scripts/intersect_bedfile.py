import pandas as pd
import pyranges as pr
import sys
import csv

## tells us the bedfile is the first input in the bash command
filteredFile = sys.argv[1]
AsiSIFile = sys.argv[2]
file_name = sys.argv[1].replace('_filtered.bed', '_intersect.bed')

def intersect(filtered, AsiSI):
    filtered = pd.read_csv(filtered, delimiter='\t')
    Asibed = pd.read_csv(AsiSI, delimiter='\t', header=None)
    asicols = "Chromosome Start End".split()
    Asibed.columns = asicols
    # using pyranges let's make to grange objects 
    gr1, gr2 = pr.PyRanges(filtered), pr.PyRanges(Asibed)
    # intersect the two granges
    gr = gr1.intersect(gr2)
    # Create a dataframe from the intersected ranges
    AsiSI_intersect = gr.df
    return AsiSI_intersect.to_csv(file_name, sep='\t', index=False)

intersect(filteredFile, AsiSIFile)