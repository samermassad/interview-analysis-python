import video_analyser
import argparse
import glob
from excel_export import ExcelExporter
from tqdm import tqdm


def main(root_dir):
    exporter = ExcelExporter('D:/Desktop/results.xlsx')
    files = glob.iglob(root_dir + '**/*.mp4', recursive=True)
    # number_of_files = len(list(files))
    # progress_bar = tqdm(total=2, position=1, leave=True)
    for filename in files:
        analysed_data = video_analyser.analyse_file(filename)
        exporter.append_results(analysed_data, filename)
        # progress_bar.update(1)
    print("Exporting the XLSX file...")
    exporter.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="root directory of video files")
    args = parser.parse_args()
    main(args.dir)
