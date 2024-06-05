from odoo import api, fields, models, _

class AttendanceMarkWizard(models.TransientModel):
    _name = 'mohsin.attendance.mark.wizard'
    _description = 'Mark Student Attendance'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id, readonly=False)

    attendance_sheet_id = fields.Many2one('mohsin.attendance.sheet', string="Attendance Sheet", readonly=True)

    attendance_status = fields.Selection([
        ('absent', 'Mark Absent'),
        ('present', 'Mark Present'),
    ], string='Attendance Type', default='absent', required=True)

    is_late_arrival = fields.Boolean(string='Late Arrival')
    course_id = fields.Many2one(related='attendance_sheet_id.course_id')


    student_ids = fields.Many2many('res.partner',
                                   domain="[('is_student','=',True)]",
                                   string='Students'
                                   )








    @api.model
    def default_get(self, fields):
        res = super(AttendanceMarkWizard, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id', [])
        record = self.env[active_model].search([('id', '=', active_id)])
        res['attendance_sheet_id'] = record.id
        return res





    def action_process_attendance(self):
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        active_id = self.env.context.get('active_id', [])
        attendance_sheet_idx = self.env.context.get('')
        record_id = self.env[active_model].search([('id', '=', active_id)])


        student_ids = self.env['res.partner'].search(
            [('course_id', '=', record_id.course_id.id), ('batch_id', '=', record_id.batch_id.id),
             ('is_student', '=', True)])

        for student in self.student_ids:
            # Check if the attendance record for the student already exists
            existing_record = self.env['mohsin.attendance.sheet.line'].search([
                ('attendance_sheet_id', '=', self.attendance_sheet_id.id),
                ('student_id', '=', student.id)
            ])
            if not existing_record:
                self.env['mohsin.attendance.sheet.line'].create({
                    'attendance_sheet_id': self.attendance_sheet_id.id,
                    'student_id': student.id,
                    'attendance_status': self.attendance_status,
                    'is_late_arrival': self.is_late_arrival,
                })
            # Optionally, change the state of the attendance sheet to 'progress' if needed
        self.attendance_sheet_id.write({'state': 'progress'})
        return {'type': 'ir.actions.act_window_close'}






