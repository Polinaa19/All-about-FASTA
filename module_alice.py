'''
This module contains "basic_statistics" function, providing some basic statistics for our FASTA/FASTQ file and "quality_score" function, performing assesment of average per base quality
'''
import Bio
import statistics
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import progressbar as pb
from Bio import SeqIO
import time


basic_statistics(input_file, output_mode = "quiet", output_file = "basic_statistics.csv"):def fast_report(input_file, output_file, output_mode="quiet"):

    with open(input_file, "r"):
        read_length = [len(seq_record.seq) for seq_record in SeqIO.parse(input_file, file_type)]
        count_reads = len(read_length)
        total_length = sum(read_length)
        read_mean = statistics.mean(read_length)
        read_mode = statistics.mode(read_length)
        mode_percent = (read_length.count(read_mode) / count_reads) * 100

        if count_reads == 1:
            print("Length:", read_length, file = open(output_file, "a"))
            if output_mode == "verbose":
                print("There is one sequence in your file. The sequence length is {}".format(read_length[0]))
        else:
            print("Reads:", count_reads, "\n"
                  "Min length:", min(read_length), "\n"
                  "Max length:", max(read_length), "\n"
                  "Average length:", round(read_mean, 2), "\n"
                  "Prevailing length:", read_mode, "({}%)".format(round(mode_percent, 1)), "\n"
                  "Total length:", total_length,
                   file = open(output_file, "a"))
            if output_mode == "verbose":
                print("The file contains {} reads. The read lengths range from {} to {}. The most frequent length is {} ({}% of all reads). The total length is {}.".format(count_reads,
                min(read_length), max(read_length), statistics.mode(read_length), round(mode_percent, 1), total_length))

    return


def quality_score(input_file, output_file):
    start_time = time.clock()
    widgets = ['Assesment of quality score: ', pb.Percentage(), ' ',
               pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
    counter = 0

    with open(input_file, "r"):
        if file_type == "fastq":
            print("Data exploring...")

            if phred == "0" or "33":  #0 goes as an argument if phred hasn't been specified
                encoding = "phred33"
                num = 33
            elif phred == "64":
                encoding = "phred64"
                num = 64
            else:
                print("Unsupportable encoding")

            print("Encoding: {}".format(encoding))

            qualities = []
            for _, _, qual in FastqGeneralIterator(open(input_file)):
                    qualities.append([ord(sym) - num for sym in qual])
            qualities = tuple(qualities)
            max_read_length = max([len(q) for q in qualities])
            base_numbers = [i for i in range(1, (max_read_length + 1))]

            per_base_qualities = np.zeros((max_read_length,), dtype=int)
            per_base_quantities = np.zeros((max_read_length,), dtype=int)
            add_one = np.ones((max_read_length,), dtype=int)

            timer_1 = pb.ProgressBar(widgets=widgets, maxval=(len(qualities))).start()

            for i in qualities:
                counter += 1
                timer_1.update(counter)
                i = np.asarray(i)
                per_base_qualities[:len(i)] += i
                per_base_quantities[:len(i)] += add_one[:len(i)]

            timer_1.finish()
            print("Counting the average quality...")
            average_per_base_quality = per_base_qualities / per_base_quantities
            print(time.clock() - start_time, "seconds_calculations")

            print("All calculations are finished. Drawing the plot...")
            plt.bar(base_numbers, average_per_base_quality, color=['green'])
            plt.xlabel("base number")
            plt.ylabel("average quality")
            plt.autoscale(enable=True, axis='both', tight=None)
            plt.savefig('average_quality.png')
            print("The plot has been saved as 'average_quality.png'")

            df_quality = pd.DataFrame(average_per_base_quality, base_numbers, columns=["average quality"])
            df_quality.to_csv(output_file, sep='\t')

        else:
            print("Quality score function is available only for fastq files")


    print("Time:", time.clock() - start_time, "seconds")
    return
