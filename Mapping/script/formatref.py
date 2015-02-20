#!/usr/bin/python
import os
import glob
import sys

fastafile = open('Fasta/obj70.fa')
refseq = ''
for line in fastafile.xreadlines():
  if '>' in line:
    continue
  line = line.rstrip()
  refseq = refseq+line
fastafile.close()

primerfile = open('doc/PrimerInfo','r')
ref1file = open('Fasta/Ref1.fa','w')
ref2file = open('Fasta/Ref2.fa','w')
constant = 'GCGGCCCGACGTAACGATTCGAG' #the constant site before the forward primer, after the 13N barcode
rconstant = constant[::-1].replace('C','g').replace('T','a').replace('A','t').replace('G','c')
rconstant = rconstant.replace('c','C').replace('t','T').replace('a','A').replace('g','G')
for line in primerfile.xreadlines():
  if 'ID' in line:
    continue
  line = line.rstrip().rsplit("\t")
  ID = int(line[0])
  start = int(line[1])
  end = int(line[3])
  length = end-start+1
  seg = refseq[start-1:end]
  if ID%2 == 0:
    ref1file.write('>'+str(ID)+"\n")
    ref1file.write(seg+rconstant+"\n")
  else:
    ref2file.write('>'+str(ID)+"\n")
    ref2file.write(seg+rconstant+"\n")
primerfile.close()
ref1file.close()
ref2file.close()
