#!/usr/bin/env nextflow
nextflow.enable.dsl=2

// Set input files as parameters 
params.bedFile = file('data/breaks/*.bed')
params.AsiSIFile=file('data/chr21_AsiSI_sites.t2t.bed')

//Filter the bed files with a MAPQ>=30 

process filterBed {
    input:
    file bedFile

    output:
    file "*_filtered.bed"

    script: 
    """
    python3 $PWD/scripts/filter.py "${bedFile}"
    """
}

//Filter the bed files with a MAPQ>=30
process intersectBed {
    input:
    file filteredFile
    file AsiSIFile

    output:
    file "*_intersect.bed"

    script: 
    """
    python3 $PWD/scripts/intersect.py "${filteredFile}" "${AsiSIFile}"
    """
}

//Filter the bed files with a MAPQ>=30
process overlapBed {
    input:
    file filteredFile
    file AsiSIFile

    output:
    file "*_overlap.bed"

    script: 
    """
    python3 $PWD/scripts/overlap.py "${filteredFile}" "${AsiSIFile}"
    """
}

//Filter the bed files with a MAPQ>=30
process normalisedOutput {
    input:
    file filteredFile
    file intersectFile
    file overlapFile

    output:
    file "normalised.txt"

    script: 
    """
    python3 $PWD/scripts/normalised.py "${filteredFile}" "${intersectFile}" "${overlapFile}"
    """
}

//put all the processes together in a workflow 
workflow {
    
    // Create a channel with all the input files 
    all_bed_files = Channel.fromPath(params.bedFile)

    // Run the filter process
    filterBed(all_bed_files) 
    
    // Run the intersect process using the output of the filter process and the AsiSIFile
    intersectBed(filterBed.out, params.AsiSIFile)

    // Run the overlap process (To answer question 4 to find the maximum number of AsiSI sites observed in a sample)
    overlapBed(filterBed.out, params.AsiSIFile)
    
    // Collect the normalised output files 
    output=normalisedOutput(filterBed.out, intersectBed.out, overlapBed.out) \
    | collectFile \
    | view



    
}
