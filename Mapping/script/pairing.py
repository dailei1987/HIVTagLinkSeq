#!/usr/bin/python
import os
import sys
import glob

#MAIN#
#filenames = glob.glob('Mut/*.mut')
filenames = glob.glob('Mut/*.mut')
#filenames = glob.glob('Mut/s_8_1_1101.mut')

countfile = 0
for infilename in filenames:
  countfile = countfile + 1
  outfilename = infilename.replace('Mut/', 'paired/').replace('.mut', '.pair')
  infile = open(infilename, 'r')
  outfile = open(outfilename, 'w')
  IDfor = ''
  pairing = 0
  mut = []
  BC = ''
  for line in infile.xreadlines():
    line = line.rstrip()
    line = line.rsplit("\t")
    if pairing == 1 and line[0] == IDfor:
      mut.append(line[3])
      mut = '_'.join(mut).rsplit('_')
      if len(list(set(mut))) == 1 and mut[0] == 'WT':
        out = "\t".join([BC, 'WT'])
        outfile.write(out+"\n")
      else:
        mutlist = []
        for M in list(set(mut)):
          if M != 'WT':
            mutlist.append(M)
        mut = '_'.join(mutlist)
        out = "\t".join([BC,mut])
        outfile.write(out+"\n")
      mut = []
      pairing = 0
    elif pairing == 1 and line[0] != IDfor:
      IDfor = line[0]
      BC = '_'.join([line[1],line[2][1:14]])
      pairing = 1
      mut = []
      mut.append(line[3])
    elif pairing == 0:
      IDfor = line[0]
      BC = '_'.join([line[1],line[2][1:14]])
      pairing = 1
      mut = []
      mut.append(line[3])
  infile.close()
  outfile.close()
  print 'complete.......', countfile, ' files'
  #sys.exit()
