# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_school = fields.Boolean(related='company_id.is_school', readonly=False)
    school_type = fields.Selection(related='company_id.school_type', readonly=False)
    resource_calendar_id = fields.Many2one(related='company_id.resource_calendar_id', readonly=False)
    use_batch = fields.Boolean(related='company_id.use_batch', readonly=False)
    use_section = fields.Boolean(related='company_id.use_section', readonly=False)





    #Attendance Module of school
    group_student_attendance_use_pin = fields.Boolean(
        string='Student PIN')

    group_student_attendance_use_day = fields.Boolean(
        string='Day Attendance')

    group_student_attendance_use_period = fields.Boolean(
        string='Period Attendance')

    group_student_attendance_use_time = fields.Boolean(
        string='Attendance Time')

    student_attendance_mode = fields.Selection(related='company_id.student_attendance_mode', readonly=False)
    student_attendance_with_time = fields.Boolean(related='company_id.student_attendance_with_time', readonly=False)

    attendance_kiosk_mode = fields.Selection(related='company_id.student_attendance_kiosk_mode', readonly=False)
    attendance_barcode_source = fields.Selection(related='company_id.student_attendance_barcode_source', readonly=False)
    attendance_kiosk_delay = fields.Integer(related='company_id.student_attendance_kiosk_delay', readonly=False)

    # @api.depends('student_attendance_mode')
    def _compute_attendance_type(self):
        if self.student_attendance_mode == 'day':
            self.group_student_attendance_use_day = True
            self.group_student_attendance_use_period = False
        else:
            self.group_student_attendance_use_day = False
            self.group_student_attendance_use_period = True

    @api.onchange('student_attendance_mode')
    def _onchange_student_attendance_mode(self):
        self.group_student_attendance_use_day = False
        self.group_student_attendance_use_period = False

        if self.student_attendance_mode == 'day':
            self.group_student_attendance_use_day = True
        else:
            self.group_student_attendance_use_period = True
