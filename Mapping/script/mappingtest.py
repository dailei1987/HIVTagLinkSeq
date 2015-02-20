#!/usr/bin/python 
#WROTE ON 4/9/2012 UTILIZING A BASH SCRIPT QSEQ2FQ.SH
#JUST HAD SOME CHICKEN DRUMSTICKS AND RICE AND VEGES
#HOPE I CAN FINISH IT IN 2 HOURS
#When counting base, count from 1. Do not count from 0, otherwise it will confuse everyone
import os
import glob
import sys

def IdentifyReadName(samfile,ID):
  infile = open(samfile, 'r')
  for line in infile.xreadlines():
    if line[0] == '@': continue
    line = line.rstrip()
    info = line.rsplit("\t")
    position = int(info[3])
    if info[5] == '100M' or info[5] == '87M':
      ID.append(info[0])
  return ID
  infile.close()

def extractfastq(zipfile,ID):
  os.system('gunzip '+zipfile)
  fqfile  = zipfile.replace('.gz','')
  outfilename = fqfile.replace('lane2','InVivo').replace('lane3','InVivo').replace('lane4','ExVivo').replace('lane5','ExVivo').replace('fastq/','Mut/')
  infile  = open(fqfile,'r')
  outfile = open(outfilename,'w')
  switch  = 0
  for line in infile.xreadlines():
    line = line.rstrip()
    if '@HWI-ST1148' == line[0:11]:
      if line[1::].rsplit(' ')[0] in ID:
        outfile.write(line+"\n")
        switch = 1
      else:
        switch = 0
    elif switch == 1:
      outfile.write(line+"\n")
  infile.close()
  outfile.close()
  os.system('gzip '+outfilename)
  os.system('gzip '+fqfile)
  
#################MAIN###################
fqfiles = glob.glob('fastq/*R1*.gz')
refseqs = ['Fasta/Ref1.fa','Fasta/Ref2.fa']
fqfiles = sorted(fqfiles)

for zipfile in fqfiles:
  zipfile1 = zipfile
  zipfile3 = zipfile.replace('R1', 'R2')
  fqfile = zipfile.rsplit('fastq/')[1].rsplit('_')[0]+zipfile.rsplit('_')[4].rsplit('.')[0]
  fqfile1 = zipfile1.rsplit('.fastq')[0].replace('fastq/', '')
  fqfile3 = zipfile3.rsplit('.fastq')[0].replace('fastq/', '')
  Jsonfile = ''.join(["Json/", fqfile, ".json"])
  Mutfile = ''.join(["Mut/", fqfile, ".mut"])
  refid = 0
  ID_1    = []
  ID_3    = []
  for refseq in refseqs:
    refid = refid+1
    os.system("bwa aln -l 7 -k 2 -n 8 -B 13 -t 6 -o 0 "+refseq+" "+zipfile1+" > tmp/"+fqfile1+".sai")
    os.system("bwa aln -l 7 -k 2 -n 8 -B 0 -t 6 -o 0 "+refseq+" "+zipfile3+" > tmp/"+fqfile3+".sai")
    os.system("bwa samse "+refseq+" tmp/"+fqfile1+".sai "+zipfile1+" > tmp/"+fqfile1+'_'+str(refid)+".sam")
    os.system("bwa samse "+refseq+" tmp/"+fqfile3+".sai "+zipfile3+" > tmp/"+fqfile3+'_'+str(refid)+".sam")
    ID_1 = IdentifyReadName("tmp/"+fqfile1+'_'+str(refid)+".sam",ID_1)
    ID_3 = IdentifyReadName("tmp/"+fqfile3+'_'+str(refid)+".sam",ID_3)
    os.system("rm tmp/*.sai")
  ID = ID_1+ID_3
  ID = set(ID)
  extractfastq(zipfile1,ID)
  extractfastq(zipfile3,ID)
  os.system("rm tmp/*")
