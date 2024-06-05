from odoo import api, fields, models, _
from random import randint

class SchoolCourseSubjectGroup(models.Model):
    _name = 'mohsin.school.subject.group'
    _description = 'Subject Group'

    name = fields.Char(string='Subject Group', required=True)


class SchoolCourseSubject(models.Model):
    _name = 'mohsin.school.subject'
    _description = 'Subject'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Subject', required=True)
    code = fields.Char(string='Code', required=True, size=10)
    active = fields.Boolean('Active', default=True)
    subject_group_id = fields.Many2one('mohsin.school.subject.group', string='Subject Group')
    color = fields.Integer(default=_default_color)
    company_id = fields.Many2one('res.company', 'Company')



