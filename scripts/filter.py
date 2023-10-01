import pandas as pd
from time import time
import sys
import csv
import os

## tells us the bedfile is the first input in the bash command
bedfile = sys.argv[1]
file_name = sys.argv[1].replace('.bed', '_filtered.bed')

## execute the timer function
timedecorator_file_path = os.path.join(os.path.dirname(__file__), "time.py")
exec(open(timedecorator_file_path).read())

## Let's create a function to filter the bed file (this function could poteintally be stored in a separate script and called)
@timer_func
def filterBed(bedfile):
    bed = pd.read_csv(bedfile, delimiter='\t', header=None)
    ## Name columns in the bedfile
    cols = "Chromosome Start End Readname MAPQ Strand".split()
    bed.columns = cols
    ## Filter the MAPQ >=30 using lambda
    bed_filtered=bed[bed.apply(lambda x: x['MAPQ'] >= 30, axis=1)]
	## Save output as dataframe
    bed_filtered_df = pd.DataFrame(data=bed_filtered)
    ##Return the output as a filtered bed file 
    return bed_filtered_df.to_csv(file_name, sep='\t', index=False)

## Run the function 
filterBed(bedfile)

