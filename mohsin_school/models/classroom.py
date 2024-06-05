from odoo import api, fields, models, _


class ClassroomBuilding(models.Model):
    _name = 'mohsin.school.building'
    _description = 'Mohsin School Building'

    active = fields.Boolean(default=True)
    name = fields.Char(string="Building", required=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    address_id = fields.Many2one('res.partner', required=True, string="Building Address",
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")


class ClassroomBuildingRoom(models.Model):
    _name = 'mohsin.school.building.room'
    _description = 'Classrooms'

    name = fields.Char(string='Room Name', required=True, index=True, translate=True)
    building_id = fields.Many2one('mohsin.school.building', string='Building', required=True )
    capacity = fields.Integer(string='Capacity', required=True, default=30)
