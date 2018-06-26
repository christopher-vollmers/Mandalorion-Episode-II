import sys

infile=sys.argv[1]
out=open(sys.argv[2],'w')

def revComp(sequence):
    '''Returns the reverse complement of a sequence'''
    bases = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'N':'N', '-':'-'}
    return ''.join([bases[x] for x in list(sequence)])[::-1]


def read_fastq_file(seq_file):
    '''
    Takes a FASTQ file and returns a list of tuples
    In each tuple:
        name : str, read ID
        left,right: str, "p" if read is complete on that end
        seq : str, sequence
        qual : str, quality line

        seq_length : int, length of the sequence
    '''
    read_list = []
    length = 0
    for line in open(seq_file):
        length += 1
    lineNum = 0
    seq_file_open = open(seq_file, 'r')
    while lineNum < length:
        name_root = seq_file_open.readline().strip()[1:].split('_')
        name, left, right = name_root[0],name_root[1], name_root[2]
        seq = seq_file_open.readline().strip()
        plus = seq_file_open.readline().strip()
        qual = seq_file_open.readline().strip()

        seq_length = len(seq)
        read_list.append((name, left, right, seq, qual, seq_length))
        lineNum += 4

    return read_list


def find_direction(sequence):
    left_sequence=sequence[:200]
    right_sequence=sequence[-200:]
    T_stretches=[]
    A_stretches=[]
    T_stretch=0
    A_stretch=0

    for base in left_sequence:
        if base == 'T':
            T_stretch+=1
        else:
            T_stretches.append(T_stretch)
            T_stretch=0
    for base in right_sequence:
        if base == 'A':
            A_stretch+=1
        else:
            A_stretches.append(A_stretch)
            A_stretch=0
    

    if max(T_stretches)>max(A_stretches):
        direction='-'
    else:
        direction='+'

    return direction,str(max(T_stretches)),str(max(A_stretches))

def filterReads(reads):

    for name, left, right, seq, qual, seq_length in reads:
        if left=='p' and right=='p':
            
            direction,T,A=find_direction(seq)

            if direction=='-':
                seq=revComp(seq)
            out.write('>%s\n%s\n' % (name,seq))

def main():
    reads=read_fastq_file(infile)
    filterReads(reads)

main()

    






    
