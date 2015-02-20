#!/usr/bin/python
import os
import sys
import glob
from string import atof

#adjust position and filterprimer
def filterprimer(mutid,ref,phash):
  wtaa=mutid[0]
  mutaa=mutid[-1]
  mutpos=int(mutid[1:-1])
  shift=phash[ref][0]-1
  mutpos=shift+mutpos
  if mutpos<=phash[ref][1]:
    return 'WT'
  elif mutpos>=phash[ref][3]:
    return 'WT'
  else:
    mut = wtaa+str(mutpos)+mutaa
    return mut

#harshin primer
primerfile=open('../Mapping/doc/PrimerInfo','r')
phash={}
for line in primerfile.xreadlines():
  if 'ID' in line:
    continue
  line=line.rstrip().rsplit("\t")
  ref=line[0]
  Fstart=int(line[1])
  Fend=int(line[2])
  Rstart=int(line[3])
  Rend=int(line[4])
  data=[Fstart,Fend,Rstart,Rend]
  phash[ref]=data
primerfile.close()

#main#
filenames=glob.glob('errorcorrect/Week10R2/*.ec')
for infile in filenames:
  outfile=infile.replace('.ec','.dat').replace('errorcorrect/','PreAssemb/')
  infile=open(infile,'r')
  outfile=open(outfile,'w')
  for line in infile.xreadlines():
    line=line.rstrip().rsplit("\t")
    ref=line[0].rsplit('_')[0]
    bc=line[0].rsplit('_')[1]
    allcount=atof(line[1])
    mutid=line[2]
    mutcount=atof(line[3])
    if 't' in bc or 'a' in bc or 'c' in bc or 'g' in bc or 'n' in bc or 'N' in bc:
      continue
    if mutcount/allcount > 0.45 and allcount >= 3:
      if mutid!='WT':
        mutid=filterprimer(mutid,ref,phash)
      out="\t".join([bc,ref,mutid])
      outfile.write(out+"\n")
  infile.close()
  outfile.close()
