#!/usr/bin/env python3

"""
Extract summary parameters (95th percentile and mean) for QUAL, DP, and MQ
from a VCF file. Accepts both plain-text and gzipped VCFs. Outputs a
parameter file named <input>.params.

Credit: Script written by Dr Graham Etherington and minor edits made by Jessica Peers.

Usage:
    python extract_vcf_params.py input.vcf[.gz]
""

import os
import sys
import gzip
import numpy as np
import vcf

# Input VCF path from command line
vcf_file = sys.argv[1]

# Derive output filename: <basename>.params
file_name = os.path.basename(vcf_file)
file_root = os.path.splitext(file_name)[0]
outfile_name = file_root + ".params"

# Lists to store QUAL, DP, MQ values
quals = []
depths = []
mapquals = []

# Handle gzipped or uncompressed VCF files
if vcf_file.endswith(".gz"):
    # Read and decode gzipped VCF into a string buffer
    with gzip.open(vcf_file, "rb") as f:
        content = f.read().decode("utf-8")
    import io
    vcf_reader = vcf.VCFReader(io.StringIO(content))
else:
    # Plain-text VCF
    with open(vcf_file, "r") as f:
        vcf_reader = vcf.VCFReader(f)

# Iterate over each VCF record and extract fields if present
for record in vcf_reader:
    if record.QUAL is not None:
        quals.append(record.QUAL)
    if "DP" in record.INFO:
        depths.append(record.INFO["DP"])
    if "MQ" in record.INFO:
        mapquals.append(record.INFO["MQ"])

# Convert lists to NumPy arrays
np_quals = np.array(quals)
np_depths = np.array(depths)
np_mapquals = np.array(mapquals)

# Compute 95th percentiles
highQUAL = np.percentile(np_quals, 95)
highDP = np.percentile(np_depths, 95)
highMQ = np.percentile(np_mapquals, 95)

# Compute means
meanQUAL = np.mean(np_quals)
meanDP = np.mean(np_depths)
meanMQ = np.mean(np_mapquals)

# Write output parameter file
with open(outfile_name, "w") as outfile:
    outfile.write("highQUAL:" + str(highQUAL) + "\n")
    outfile.write("highDP:" + str(highDP) + "\n")
    outfile.write("highMQ:" + str(highMQ) + "\n")
    outfile.write("meanQUAL:" + str(meanQUAL) + "\n")
    outfile.write("meanDP:" + str(meanDP) + "\n")
    outfile.write("meanMQ:" + str(meanMQ) + "\n")
