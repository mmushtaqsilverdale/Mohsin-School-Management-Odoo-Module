from odoo import api, fields, models, _


class SchoolSection(models.Model):
    _name = 'mohsin.school.course.section'
    _description = 'Course Section'
    _rec_name = 'display_name'

    name = fields.Char(string='Course', required=True, index=True, translate=True)
    course_id = fields.Many2one('mohsin.school.course', string='Course', required=True)
    display_name = fields.Char(string="Display Name", compute='_compute_display_name')

    @api.depends('name', 'course_id.code')
    def _compute_display_name(self):
        for record in self:
            record.display_name = str(record.course_id.code) + '/' + str(record.name)

