#!/usr/bin/env nextflow
nextflow.enable.dsl=2

// Set input files as parameters 
params.bedFile = file('../coding-test-advanced/data/breaks/*.bed')
params.AsiSIFile=file('../coding-test-advanced/data/chr21_AsiSI_sites.t2t.bed')

//Filter the bed files with a MAPQ>=30 
process filterBed {
    input:
    file bedFile

    output:
    file "*_filtered.bed"

    script: 
    """
    python3 ~/brokenstrings/scripts/filter_bedfile.py "${bedFile}"
    """
}


process intersect {
    input:
    file filteredFile
    file AsiSIFile

    output:
    file "*_intersect.bed"

    script: 
    """
    python3 ~/brokenstrings/scripts/intersect_bedfile.py "${filteredFile}" "${AsiSIFile}"
    """
}

process overlap {
    input:
    file filteredFile
    file AsiSIFile

    output:
    file "*_overlap.bed"

    script: 
    """
    python3 ~/brokenstrings/scripts/overlap.py "${filteredFile}" "${AsiSIFile}"
    """
}

process normalised {
    input:
    file filteredFile
    file intersectFile
    file overlapFile

    output:
    file "normalised.txt"

    script: 
    """
    python3 ~/brokenstrings/scripts/normalised.py "${filteredFile}" "${intersectFile}" "${overlapFile}"
    """
}

workflow {
    // create a channel with all the input files 
    all_bed_files = Channel.fromPath(params.bedFile)

    filterBed(all_bed_files) 
    intersect(filterBed.out, params.AsiSIFile)
    overlap(filterBed.out, params.AsiSIFile)
    
    output=normalised(filterBed.out, intersect.out, overlap.out) \
    | collectFile \
    | view



    
}
