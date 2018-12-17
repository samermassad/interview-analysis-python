import video_analyser
import argparse
import glob
from excel_export import ExcelExporter
import time


def main(root_dir, output_file):
    exporter = ExcelExporter(output_file)
    print("Exporting results to: {}".format(output_file))

    files = glob.iglob(root_dir + '**/*.mp4', recursive=True)
    number_of_files = len(list(glob.iglob(root_dir + '**/*.mp4', recursive=True)))
    current_file_number = 1

    for filename in files:
        now = time.strftime('%Y/%m/%d-%H:%M:%S')
        percentage = current_file_number / number_of_files * 100
        print("[{}] Analysing {}/{} ({}%): {}".format(now, current_file_number, number_of_files,
                                                      float("%0.2f" % percentage), filename))

        analysed_data = video_analyser.analyse_file(filename)

        exporter.append_results(analysed_data, filename)

        current_file_number += 1
    print("Results exported to: {}".format(output_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="root directory of video files")
    parser.add_argument("-o", help="output file name/path")
    args = parser.parse_args()
    if args.o:
        file = args.o
    else:
        file = "./results/{}_{}".format(time.strftime('%Y-%m-%d-%H-%M-%S'), 'results.xlsx')
    main(args.dir, file)
