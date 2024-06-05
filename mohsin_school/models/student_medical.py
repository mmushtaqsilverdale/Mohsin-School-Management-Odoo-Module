from odoo import api, fields, models, _


class StudentMedicalcat(models.Model):
    _name = 'mohsin.school.medical.cat'
    _description = 'Medical Category'

    name = fields.Char(string='Name', required=True)



class StudentMedicaltype(models.Model):
    _name = 'mohsin.school.medical.type'
    _description = 'Medical Types'

    name = fields.Char(string='Name', required=True)
    med_cat_id = fields.Many2one('mohsin.school.medical.cat', string='Category', required=True)




class StudentMedical(models.Model):
    _name = 'mohsin.school.student.medical'
    _description = 'Student Medical History'


    student_id = fields.Many2one('res.partner', string='Student', required=True, ondelete='cascade', index=True, copy=False)
    med_cat_id = fields.Many2one('mohsin.school.medical.cat', string='Category', required=True)
    med_type_id = fields.Many2one('mohsin.school.medical.type', string='Type', required=True,
                                 domain="[('med_cat_id','=',med_cat_id)]"
                                 )
    med_condition = fields.Text(string='Condition')
    med_remarks = fields.Text(string='Remarks')
