from odoo import models, fields, api, exceptions, _

class StudentAttendance(models.Model):
    _name = "mohsin.student.attendance"
    _description = "Student Attendance"

    student_id = fields.Many2one('res.partner', string="Student",
                                 domain="[('is_student','=',True)]",
                                 required=True, ondelete='cascade', index=True)

    date_attendance = fields.Date('Attendance Date', required=True)
    check_in = fields.Datetime(string="Check In", readonly=False, store=True)
    check_out = fields.Datetime(string="Check Out")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    student_attendance_mode = fields.Selection(related='company_id.student_attendance_mode')

    attendance_hours = fields.Float(string='Attendance Hours', store=True,
                                    readonly=True)

    attendance_status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
    ], string='Attendance Type', default='present')
    is_late_arrival = fields.Boolean(string='Late Arrival')

    attendance_sheet_id = fields.Many2one('mohsin.attendance.sheet', string='Attendance Sheet')

    # Academic Fields
    course_id = fields.Many2one('mohsin.school.course', store=True,
                                compute='_compute_from_student_id'
                                )
    roll_no = fields.Char(string='Roll No.', store=True, compute='_compute_from_student_id')
    batch_id = fields.Many2one('mohsin.school.course.batch', related='student_id.batch_id')

    # period wise attendance fields
    subject_id = fields.Many2one('mohsin.school.subject', string='Subject',
                                 domain="[('id','in',subject_ids)]"
                                 )
    subject_ids = fields.Many2many('mohsin.school.subject', string='Subjects', compute='_compute_subject_ids', store=True)

    @api.constrains('student_id', 'date_attendance')
    def _check_student_attendance_overlap(self):
        for record in self:
            if record.student_attendance_mode == 'period':
                # Check if there are any overlapping records with the same student and date_attendance
                domain = [
                    ('student_id', '=', record.student_id.id),
                    ('date_attendance', '=', record.date_attendance),
                    ('id', '!=', record.id),
                    '|',
                    ('check_in', '<=', record.check_in),
                    ('check_out', '>=', record.check_in),
                ]
            else:
                # Check if there are any overlapping records with the same student and date_attendance
                domain = [
                    ('student_id', '=', record.student_id.id),
                    ('date_attendance', '=', record.date_attendance),
                    ('id', '!=', record.id),
                ]

            if self.search_count(domain) > 0:
                raise exceptions.ValidationError(_('Student attendance cannot overlap.'))

    @api.depends('student_id')
    def _compute_from_student_id(self):
        for record in self:
            record.course_id = record.student_id.course_id.id
            record.roll_no = record.student_id.roll_no


    @api.depends('course_id')
    def _compute_subject_ids(self):
        for attendance in self:
            if attendance.course_id:
                subject_lines = attendance.env['mohsin.school.course.subject.line'].search([
                    ('course_id', '=', attendance.course_id.id)
                ])
                attendance.subject_ids = subject_lines.mapped('subject_id')
            else:
                attendance.subject_ids = False


