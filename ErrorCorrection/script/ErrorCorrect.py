#!/usr/bin/python
import glob
import sys
import os
import csv
from scipy import stats
from string import atof
from operator import itemgetter

def processpefile(infilename, outfilename):
  infile = open(infilename, 'r')
  outfile = open(outfilename, 'w')
  for line in infile.xreadlines():
    line = line.rsplit(':')[1]
    outfile.write(line)
  infile.close()
  outfile.close()
  

def sortfile(infile, sortfile):
  intable = csv.reader(open(infile), delimiter = "\t")
  intable = sorted(intable, key = itemgetter(0))
  write_file = csv.writer(open(sortfile, 'wb'), delimiter = "\t")
  for row in intable:
    write_file.writerow(row)

def errorcorrect(infile, outfile):
  sortfile = open(infile, 'r')
  ecfile = open(outfile, 'w')
  barcode = ''
  mutlist = []
  countoccur = 0
  countline = 0
  for line in sortfile.xreadlines():
    line = line.rstrip()
    line = line.split("\t")
    if countline == 0:
      barcode = line[0]
      mutlist = line[1].rsplit('_')
      countoccur = countoccur + 1
      countline = countline + 1
    elif line[0] == barcode:
      countoccur = countoccur + 1
      mutlist.extend(line[1].rsplit('_'))
    else:
      mutID = list(set(mutlist))
      for mut in mutID:
        mutcount = mutlist.count(mut)
        pvalue = stats.binom.sf(int(mutcount)-1,int(countoccur),0.001)
        ecfile.write(barcode+"\t"+str(countoccur)+"\t"+mut+"\t"+str(mutcount)+"\t"+str(pvalue)+"\n")
      countoccur = 1
      barcode = line[0]
      mutlist = line[1].rsplit('_')
  mutID = list(set(mutlist))
  for mut in mutID:
    mutcount = mutlist.count(mut)
    pvalue = stats.binom.sf(int(mutcount)-1,int(countoccur),0.001)
    ecfile.write(barcode+"\t"+str(countoccur)+"\t"+mut+"\t"+str(mutcount)+"\t"+str(pvalue)+"\n")
  ecfile.close()
  sortfile.close()



#############MAIN###############
filenames = glob.glob('data/*')
if 'data/InVivo' in filenames: filenames.remove('data/InVivo')
if 'data/Replicate2' in filenames: filenames.remove('data/Replicate2')
for infile in filenames:
  pefile = infile.replace('data/', 'tmp/')
  sortedfile = ''.join([pefile, '.sort'])
  ecfile = ''.join([pefile, '.ec'])
  processpefile(infile, pefile)
  sortfile(pefile, sortedfile)
  errorcorrect(sortedfile, ecfile)
  os.system("mv "+ecfile+" errorcorrect/")
  os.system("rm tmp/*")
