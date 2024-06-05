from odoo import api, fields, models, _

class StudentEnrollment(models.Model):
    _name = 'mohsin.school.student.enrollment'
    _description = 'Student Enrollment'

    model = fields.Char('Related Document Model')
    res_id = fields.Many2oneReference('Related Document ID', model_field='model')

    school_name = fields.Char('School Name', required=True)
    course_name = fields.Char('Program/Course', required=True)
    date_start = fields.Date('Start Date', required=True)
    date_end = fields.Date('End Date', required=True)
    status = fields.Selection([
        ('enroll', 'Enrolled'),
        ('complete', 'Completed'),
        ('transfer', 'Transferred'),
        ('withdrawn', 'Withdrawn'),
        ('suspended', 'Suspended'),
        ('other', 'Other'),
    ], string='Status')
    transcript_detail = fields.Text('Transcript')
    reason = fields.Text(string='Reason for Leaving')
    address_school = fields.Text('School Address')
