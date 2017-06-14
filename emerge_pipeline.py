#!/usr/bin/python

import argparse
import os
import sys
import re
import subprocess



def main():

    parser = get_arguments()
    args = parser.parse_args()

    try:
        check_if_vcf_files_exist(args.file)
    except IOError, e:
        usage("Error: VCF file(s) not found: '%s'\n" % str(e), parser)


    print """Starting annotation pipeline with the following options:\n
    VCF File(s): %s
    Merge VCF files: %s
    Annotate using Seattle Seq: %s
    Filter by PASS: %s
    Filter by QUAL score: %s
    """ %(args.file, args.merge, args.seaseq, args.passfilter, args.qualfilter)

    ## Apply Qual filters

    #subprocess.call(["bcftools", "merge", "tests/sample.vcf.gz", "tests/sample2.vcf.gz", ">", "temp.vcf"])
    subprocess.call(["bcftools merge tests/sample.vcf.gz tests/sample2.vcf.gz > temp2.vcf"], stderr=subprocess.STDOUT, shell=True)
    #subprocess.call(["bcftools merge tests/sample*.vcf.gz > temp2.vcf"], shell=True)

    ## merge the files


def usage(error, parser):
    print error
    parser.print_help()
    sys.exit(0)


#
# -c       only perform custom final annotations such as custom gene lists and
#          (useful if the VCF file has already been annotated by Annovar and SNPEff)
#
# -d int   filter individual genotypes by minimum depth
def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', nargs="+", metavar="PATHS", required="True",
                        help='Specify VCF file(s) to be annotated.')

    parser.add_argument('-o', '--outdirectory', nargs=1, metavar="PATH",
                        help='Specify where to put the output files.')

    parser.add_argument('-m', '--merge', action='store_true',
                        help='Merge all VCF files before annotating.')

    parser.add_argument('-p', '--passfilter', action='store_true',
                        help='Apply PASS filter to variants in VCF file.')

    parser.add_argument('-q', '--qualfilter',  metavar="QUAL",
                        help='Apply specified Quality filter to variants in VCF file.')

    parser.add_argument('-s', '--seaseq', action='store_true',
                        help='Annotate VCF file using Seattle Seq. ')

    parser.add_argument('-c', '--config', nargs=1, metavar="PATH",
                        help='Location of config file.  Default is config file in pipeline directory.')

    return parser


def hello(one, two):
    return "%s, %s!" %(one, two)


def check_if_vcf_files_exist(paths):
    list_of_vcf_files = []
    if paths:
        for p in paths:
            if (os.path.isfile(p)) and re.search(".vcf(.gz)?$", p):
                list_of_vcf_files += [p]
            else:
                raise IOError(p)

        return list_of_vcf_files


if __name__ == "__main__":
    main()


