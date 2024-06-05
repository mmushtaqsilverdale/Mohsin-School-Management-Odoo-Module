# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import xlsxwriter
from io import BytesIO
import base64


class MohsinSchool(http.Controller):
    @http.route('/mohsin_school/mohsin_school', auth='public')
    def index(self, **kw):
        sales_orders = http.request.env['res.partner'].search([('is_student', '=', True)])
        output = "<h1>List of Students</h1><br><ul>"
        for sale in sales_orders:
            output = output + "<li>" + sale['name'] + "</li>"
            print(sale['name'])
        output = output + "</ul>"
        return output

#     @http.route('/mohsin_school/mohsin_school/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mohsin_school.listing', {
#             'root': '/mohsin_school/mohsin_school',
#             'objects': http.request.env['mohsin_school.mohsin_school'].search([]),
#         })

#     @http.route('/mohsin_school/mohsin_school/objects/<model("mohsin_school.mohsin_school"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mohsin_school.object', {
#             'object': obj
#         })
class AttendanceReportController(http.Controller):

    @http.route('/attendance/report', type='http', auth='user')
    def get_attendance_report(self, **kwargs):
        # Fetch attendance records
        attendance_records = request.env['mohsin.student.attendance'].search([])

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Attendance Report')

        # Add a bold format for headers
        bold = workbook.add_format({'bold': True})

        # Write the headers
        headers = ['Roll Number', 'Student Name', 'Attendance Date', 'Course', 'Batch', 'Attendance Sheet', 'Attendance Type']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, bold)

        # Write the data
        row = 1
        for record in attendance_records:
            worksheet.write(row, 0, record.student_id.roll_no)
            worksheet.write(row, 1, record.student_id.name)
            worksheet.write(row, 2, str(record.date_attendance))
            worksheet.write(row, 3, str(record.course_id.name))
            worksheet.write(row, 4, str(record.batch_id.name))
            worksheet.write(row, 5, str(record.attendance_sheet_id.name))
            worksheet.write(row, 6, record.attendance_status)
            row += 1

        workbook.close()

        output.seek(0)
        file_data = output.read()
        output.close()

        # Return the file as a response
        response = request.make_response(
            file_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=Attendance_Report.xlsx;')
            ]
        )
        return response
