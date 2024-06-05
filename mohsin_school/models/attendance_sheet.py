from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AttendanceSheet(models.Model):
    _name = "mohsin.attendance.sheet"
    _description = "Mohsin Attendance Sheet"

    name = fields.Char(string='Name', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Attendance Start'),
        ('done', 'Attendance Taken'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, default='draft')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    student_attendance_mode = fields.Selection(related='company_id.student_attendance_mode')
    date = fields.Date(string='Date', required=True)
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now)
    check_out = fields.Datetime(string="Check Out")
    attendance_register_id = fields.Many2one('mohsin.attendance.register', string='Attendance Register', required=True)
    course_id = fields.Many2one('mohsin.school.course', related='attendance_register_id.course_id')
    batch_id = fields.Many2one('mohsin.school.course.batch', string='Batch', required=True)
    subject_id = fields.Many2one('mohsin.school.subject', string='Subject')
    description = fields.Html(string='Description')
    sheet_to_close = fields.Boolean(string='Sheet to Close', compute='_compute_sheet_to_close')
    attendance_sheet_line = fields.One2many('mohsin.attendance.sheet.line', 'attendance_sheet_id',
                                            readonly=True, string='Sheet Lines')

    _sql_constraints = [
        ('unique_date_attendance_register', 'unique(date, attendance_register_id)',
         'Attendance has already been marked for the given date.'
         ),
    ]



    def button_draft(self):
        self.write({'state': 'draft'})

    def button_open(self):
        self.write({'state': 'progress'})

    def button_mark_attendance(self):
        action = {
            'name': _('Mark Attendance'),
            'res_model': 'mohsin.attendance.mark.wizard',
            'view_mode': 'form',
            'context': {
                'active_model': 'mohsin.attendance.sheet',
                'active_ids': self.ids,
                'active_id': self.id,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
        return action


    def button_cancel(self):
        self.write({'state': 'draft'})


    def button_close(self):
        for line in self.attendance_sheet_line:
            vals = {
                'student_id': line.student_id.id,
                'attendance_status': line.attendance_status,
                'is_late_arrival': line.is_late_arrival,
                'attendance_sheet_id': line.attendance_sheet_id.id,
                'date_attendance': self.date,
                'company_id': self.company_id.id,
            }
            self.env['mohsin.student.attendance'].create(vals)
        self.write({'state': 'done'})


    @api.depends('state', 'attendance_sheet_line')
    def _compute_sheet_to_close(self):
        for record in self:
            if record.state == 'progress':
                if len(record.attendance_sheet_line) > 0:
                    record.sheet_to_close = False
                else:
                    record.sheet_to_close = False
            else:
                record.sheet_to_close = False



class AttendanceSheet(models.Model):
    _name = "mohsin.attendance.sheet.line"
    _description = "Attendance Sheet Line"
    _order = "student_id asc"

    attendance_sheet_id = fields.Many2one('mohsin.attendance.sheet', string='Attendance Sheet')
    student_id = fields.Many2one('res.partner', string="Student",
                                 domain="[('is_student','=',True)]",
                                 required=True, ondelete='cascade')
    attendance_status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
    ], string='Attendance Type', default='present')
    is_late_arrival = fields.Boolean(string='Late Arrival')

