#!/usr/bin/python
import os
import sys
import glob
from string import atof

def createhash(IDhash):
  for i in range(0,13):
    IDhash[str(i)] = []
  return IDhash

def run(obj):
  #hash in all data
  filenames = glob.glob('PreAssemb/'+obj+'/*.dat')
  masterhash={}
  for infile in filenames:
    infile = open(infile, 'r')
    for line in infile.xreadlines():
      line = line.rstrip().rsplit("\t")
      ID = line[0]
      Ref = line[1]
      Mut = line[2]
      if not masterhash.has_key(ID):
        masterhash[ID]=createhash({})
      masterhash[ID][Ref].append(Mut)
    infile.close()

  #format data
  outfile = open('result/'+obj,'w')
  header = "\t".join(['ID','1','2','3','4','5','6','7','8','9','10','11','12','Frag','Complete'])
  outfile.write(header+"\n")
  countcomplete = 0
  for ID in masterhash.keys():
    countfrag = 0
    complete = 0
    datalist = [ID]
    for ref in range(0,12):
      if len(masterhash[ID][str(ref)]) == 0:
        Mutlist = 'na'
      else:
        countfrag=countfrag+1
        Mutlist = sorted(list(set(masterhash[ID][str(ref)])))
        if len(Mutlist) >= 2 and Mutlist.count('WT'):
          Mutlist.remove('WT')
        Mutlist = '_'.join(Mutlist)
        if ref == 11 and countfrag == 12:
          complete = 1
          countcomplete = countcomplete + 1
      assert(Mutlist!='')
      datalist.append(Mutlist)
    if countfrag == 13:
      countfrag = 12
    datalist.append(str(countfrag))
    datalist.append(str(complete))
    out = "\t".join(datalist)
    outfile.write(out+"\n")
  print 'total completed genes: ',countcomplete
  outfile.close()

#main#
run('Week10R2')
