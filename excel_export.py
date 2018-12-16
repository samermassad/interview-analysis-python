import xlsxwriter
from video_results import VideoResults
from enums import Emotions


class ExcelExporter:
    def __init__(self, file_name):
        self.workbook = xlsxwriter.Workbook(file_name)
        self.worksheet = self.workbook.add_worksheet()

        # Write headers
        bold = self.workbook.add_format({'bold': 1})

        self.worksheet.write('A1', 'File', bold)
        self.worksheet.write('B1', 'Number of Faces', bold)
        self.worksheet.write('C1', 'Camera Instability', bold)
        self.worksheet.write('D1', 'Detection Confidence', bold)
        self.worksheet.write('E1', 'Head Pose - Roll', bold)
        self.worksheet.write('F1', 'Head Pose - Pan', bold)
        self.worksheet.write('G1', 'Head Pose - Tilt', bold)
        self.worksheet.write('H1', 'Emotions - Joy', bold)
        self.worksheet.write('I1', 'Emotions - Sorrow', bold)
        self.worksheet.write('J1', 'Emotions - Anger', bold)
        self.worksheet.write('K1', 'Emotions - Surprised', bold)

        self.append_row = 1

    def append_results(self, results, file):
        self.worksheet.write_string(self.append_row, 0, file)
        self.worksheet.write_number(self.append_row, 1, results.face_count)
        self.worksheet.write_number(self.append_row, 2, results.camera_instability)
        self.worksheet.write_number(self.append_row, 3, results.detection_confidence)
        self.worksheet.write_number(self.append_row, 4, results.head_pose['roll_angle'])
        self.worksheet.write_number(self.append_row, 5, results.head_pose['pan_angle'])
        self.worksheet.write_number(self.append_row, 6, results.head_pose['tilt_angle'])
        self.worksheet.write_number(self.append_row, 7, results.emotions[Emotions.happy])
        self.worksheet.write_number(self.append_row, 8, results.emotions[Emotions.sorrow])
        self.worksheet.write_number(self.append_row, 9, results.emotions[Emotions.angry])
        self.worksheet.write_number(self.append_row, 10, results.emotions[Emotions.surprised])
        self.append_row += 1

    def save(self):
        self.workbook.close()
