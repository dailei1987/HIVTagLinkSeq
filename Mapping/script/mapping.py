#!/usr/bin/python 
#WROTE ON 4/9/2012 UTILIZING A BASH SCRIPT QSEQ2FQ.SH
#JUST HAD SOME CHICKEN DRUMSTICKS AND RICE AND VEGES
#HOPE I CAN FINISH IT IN 2 HOURS
#When counting base, count from 1. Do not count from 0, otherwise it will confuse everyone
import os
import glob
import sys

def FormatMut(JsonMut, Seq, startsite, Qual):
  inpos = 1000
  MutPos = JsonMut.replace('A','_')
  MutPos = MutPos.replace('C','_')
  MutPos = MutPos.replace('T','_')
  MutPos = MutPos.replace('G','_')
  wtbase = JsonMut.replace('1','')
  wtbase = wtbase.replace('2','')
  wtbase = wtbase.replace('3','')
  wtbase = wtbase.replace('4','')
  wtbase = wtbase.replace('5','')
  wtbase = wtbase.replace('6','')
  wtbase = wtbase.replace('7','')
  wtbase = wtbase.replace('8','')
  wtbase = wtbase.replace('9','')
  wtbase = wtbase.replace('0','')
  MutPos = MutPos.rsplit('_')
  MutPosarray = []
  MutIDarray = []
  RefPosarray = []
  FilterMut = []
  RefPos = int(startsite)-1
  Pos = 0
  for i in range(0,len(MutPos)-1):
    RefPos = RefPos + int(MutPos[i]) + 1
    Pos = Pos + int(MutPos[i]) + 1
    RefPosarray.append(RefPos)
    MutPosarray.append(Pos)
  for i in range(0,len(MutPosarray)):
    if int(Qual[MutPosarray[i]-1]) < 30:
      continue
    mutbase = Seq[MutPosarray[i]-1]
    RefPosOut = RefPosarray[i]
    if MutPosarray[i] >= inpos:
      RefPosOut = RefPosOut + 1
    Mut = ''.join([wtbase[i], str(RefPosOut), mutbase])
    MutIDarray.append(Mut)
  for i in MutIDarray:
    if not 'N' in i:
      FilterMut.append(i)
  if len(FilterMut) == 0:
    return 'WT'
  else:
    return '_'.join(FilterMut)


def IdentifyMut(Jsonfile, output):
  infile = open(Jsonfile, 'r')
  outfile = open(output, 'w')
  for line in infile.xreadlines():
    line = line.rstrip()
    info = line.rsplit('"')
    position = info[14][1:-1]
    if '["100M"]' in line or '["87M"]' in line:
      ID = info[3]
      REF = info[11]
      BARCODE = info[int(info.index('BC'))+2]
      MREF = info[int(info.index('mate'))+4]
      MUT = info[int(info.index('MD'))+2]
      SEQ = info[int(info.index('queryBases'))+2]
      QUAL = info[int(info.index('qualities'))+1].replace(':[','').replace('],', '').rsplit(',')
      if REF == MREF:
        MUT = FormatMut(MUT, SEQ, position, QUAL)
        outfile.write(ID+"\t"+REF+"\t"+BARCODE+"\t"+MUT+"\n")
  infile.close()
  outfile.close()

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
  for refseq in refseqs:
    refid = refid+1
    os.system("bwa aln -l 7 -k 2 -n 8 -B 13 -t 6 -o 0 "+refseq+" "+zipfile1+" > tmp/"+fqfile1+".sai")
    os.system("bwa aln -l 7 -k 2 -n 8 -B 0 -t 6 -o 0 "+refseq+" "+zipfile3+" > tmp/"+fqfile3+".sai")
    os.system("bwa sampe "+refseq+" tmp/"+fqfile1+".sai tmp/"+fqfile3+".sai "+zipfile1+" "+zipfile3+" > tmp/"+fqfile+".sam")
    os.system("samtools view -bS tmp/"+fqfile+".sam > tmp/"+fqfile+".bam")
    os.system("bamtools convert -format json -in tmp/"+fqfile+".bam -out Json/"+fqfile+".json")
    Mutfiletmp = Mutfile+str(refid)
    IdentifyMut(Jsonfile, Mutfiletmp)
    os.system("rm tmp/*")
    os.system("rm "+Jsonfile)
  os.system("cat "+Mutfile+"1 > "+Mutfile)
  os.system("cat "+Mutfile+"2 >> "+Mutfile)
  os.system("rm "+Mutfile+"1")
  os.system("rm "+Mutfile+"2")


