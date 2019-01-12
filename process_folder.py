import video_analyser
import argparse
import glob
from excel_export import ExcelExporter
import time
import logging
import grader


def main(root_dir, output_file):
    level = logging.INFO
    log_file = '{}.log'.format(output_file)
    handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
    logging.basicConfig(level=level,
                        format='%(asctime)s     %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=handlers)

    logging.info('Process Started')
    logging.info('Logging to: {}'.format(log_file))

    exporter = ExcelExporter(output_file)
    # print("Exporting results to: {}".format(output_file))
    logging.info('Exporting results to: {}'.format(output_file))

    files = glob.iglob(root_dir + '**/*.mp4', recursive=True)
    number_of_files = len(list(glob.iglob(root_dir + '**/*.mp4', recursive=True)))
    current_file_number = 1

    logging.info('{} files found'.format(number_of_files))

    for filename in files:

        # Logging
        percentage = current_file_number / number_of_files * 100
        logging.info("Analysing {}/{} ({}%): {}".format(current_file_number, number_of_files,
                                                      float("%0.2f" % percentage), filename))

        # Analyse video
        analysed_data = video_analyser.analyse_file(filename)

        # Calculate score
        score = grader.calculate_grade(analysed_data)

        # Append results to Excel
        exporter.append_results(analysed_data, filename)

        current_file_number += 1
    logging.info("Results exported to: {}".format(output_file))


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
