from enums import Emotions
import openpyxl
from openpyxl.styles import Font


class ExcelExporter:
    def __init__(self, file_name):
        self.filename = file_name
        workbook = openpyxl.Workbook()
        worksheet = workbook.get_active_sheet()

        # Write headers
        worksheet['A1'] = 'File'
        worksheet['B1'] = 'Number of Faces'
        worksheet['C1'] = 'Camera Instability'
        worksheet['D1'] = 'Detection Confidence'
        worksheet['E1'] = 'Head Pose - Roll'
        worksheet['F1'] = 'Head Pose - Pan'
        worksheet['G1'] = 'Head Pose - Tilt'
        worksheet['H1'] = 'Emotions - Joy'
        worksheet['I1'] = 'Emotions - Sorrow'
        worksheet['J1'] = 'Emotions - Anger'
        worksheet['K1'] = 'Emotions - Surprised'

        bold_font = Font(bold=True)
        for cell in worksheet["1:1"]:
            cell.font = bold_font

        workbook.save(self.filename)

        self.append_row = 2

    def append_results(self, results, file):
        results_file = openpyxl.load_workbook(self.filename)

        results_sheet = results_file.get_active_sheet()

        results_sheet.cell(row=self.append_row, column=1).value = file
        results_sheet.cell(row=self.append_row, column=2).value = results.face_count
        results_sheet.cell(row=self.append_row, column=3).value = results.camera_instability
        results_sheet.cell(row=self.append_row, column=4).value = results.detection_confidence
        results_sheet.cell(row=self.append_row, column=5).value = results.head_pose['roll_angle']
        results_sheet.cell(row=self.append_row, column=6).value = results.head_pose['pan_angle']
        results_sheet.cell(row=self.append_row, column=7).value = results.head_pose['tilt_angle']
        results_sheet.cell(row=self.append_row, column=8).value = results.emotions[Emotions.happy]
        results_sheet.cell(row=self.append_row, column=9).value = results.emotions[Emotions.sorrow]
        results_sheet.cell(row=self.append_row, column=10).value = results.emotions[Emotions.angry]
        results_sheet.cell(row=self.append_row, column=11).value = results.emotions[Emotions.surprised]

        self.append_row += 1

        results_file.save(self.filename)
