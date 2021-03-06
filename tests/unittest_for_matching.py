import unittest
import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import module_matching
from Bio import SeqIO
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from Bio.SeqIO.FastaIO import SimpleFastaParser

fasta_test1 = os.path.join(os.path.dirname(__file__), 'fasta_test1.fasta')
fasta_test2 = os.path.join(os.path.dirname(__file__), 'fasta_test2.fasta')
fastq_test1 = os.path.join(os.path.dirname(__file__), 'fastq_test1.fastq')
fastq_test2 = os.path.join(os.path.dirname(__file__), 'fastq_test2.fastq')
fasta_result =  os.path.join(os.path.dirname(__file__), 'fasta_result.fasta')
fastq_result =  os.path.join(os.path.dirname(__file__), 'fastq_result.fastq')

class TestMatchingFasta(unittest.TestCase):
    
    def test_join_fasta(self):
        module_matching.join_sequences(fasta_test1, fasta_test2, fasta_result, 'fasta')
        counter = sum(1 for title, seq in SimpleFastaParser(open(fasta_result)))
        self.assertEqual(counter, 13)
        
    def test_overlap_fasta(self):
        module_matching.overlap_sequences(fasta_test1, fasta_test2, fasta_result, 'fasta')
        counter = sum(1 for title, seq in SimpleFastaParser(open(fasta_result)))
        self.assertEqual(counter, 3)
        
    def test_subtract_fasta(self):
        module_matching.subtract_sequences(fasta_test1, fasta_test2, fasta_result, 'fasta')
        counter = sum(1 for title, seq in SimpleFastaParser(open(fasta_result)))
        self.assertEqual(counter, 10)
    
    def tearDown(self):
        os.remove(fasta_result)


class TestMatchingFastq(unittest.TestCase):
    
    def test_join_fastq(self):
        module_matching.join_sequences(fastq_test1, fastq_test2, fastq_result, 'fastq')
        counter = sum(1 for title, seq, qual in FastqGeneralIterator(open(fastq_result)))
        self.assertEqual(counter, 28)
    def test_overlap_fastq(self):
        module_matching.overlap_sequences(fastq_test1, fastq_test2, fastq_result, 'fastq')
        counter = sum(1 for title, seq, qual in FastqGeneralIterator(open(fastq_result)))
        self.assertEqual(counter, 0)
    def test_subtract_fastq(self):
        module_matching.subtract_sequences(fastq_test1, fastq_test2, fastq_result, 'fastq')
        counter = sum(1 for title, seq, qual in FastqGeneralIterator(open(fastq_result)))
        self.assertEqual(counter, 28)
    
    def tearDown(self):
        os.remove(fastq_result)
    
    
if __name__ == '__main__':
    unittest.main()
