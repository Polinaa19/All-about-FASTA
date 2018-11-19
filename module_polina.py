import Bio
import progressbar
import time
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from Bio.SeqIO.FastaIO import SimpleFastaParser
from progressbar import *
from time import sleep

def complement_reverse_sequence(input_file, output_file):
    
    with open(input_file, 'r'):
        if file_type == "fasta" or "fastq":
            for seq_record in SeqIO.parse(input_file, file_type):
                sequence = str(repr(input_file))
    
                complement_sequence = Seq(sequence, IUPAC.unambiguous_dna).complement()
                reverse_complement_sequence = Seq(sequence, IUPAC.unambiguous_dna).reverse_complement()
        
                print('Complement sequence is: \n', complement_sequence, file = open(output_file, 'a'))
                print('Reverse complement sequence is: \n', reverse_complement_sequence, file = open(output_file, 'a'))
    
    return


def delete_reads_shorter_tuple(input_file, parameters, output_file, file_type):

    print('\nReading your file... \n')
    sequence_hadle = SeqIO.parse(input_file, "{}".format(file_type))

    print('Searching reads shorter than {} \n'.format(int(parameters)))
    long_reads = tuple(seq_record for seq_record in sequence_hadle if len(seq_record.seq) > int(parameters))


    SeqIO.write(long_reads, output_file, "{}".format(file_type))
    print('Reads longer than {} are written to {} \n'.format(int(parameters), output_file))

    return


def delete_reads_shorter_fastiterator(input_file, parameters, output_file, file_type):
    print('\nReading your file... \n')

    print('Searching reads shorter than {} \n'.format(int(parameters)))

    if file_type == "fastq":
        handle = open(output_file, "w")
        for title, seq, qual in FastqGeneralIterator(open(input_file)):
            if len(seq) > int(parameters):
                handle.write("@%s\n%s\n+\n%s\n" % (title, seq, qual))
        handle.close()

    else:
        handle = open(output_file, "w")
        for title, seq in SimpleFastaParser(open(input_file)):
            if len(seq) > int(parameters):
                handle.write("@%s\n%s\n" % (title, seq))
        handle.close()
       # long_reads = (seq for seq in SimpleFastaParser(open(input_file)) if len(seq) > int(parameters))
        #SeqIO.write(long_reads, output_file, "{}".format(file_type))

    print('Reads longer than {} are written to {} \n'.format(int(parameters), output_file))

    return





