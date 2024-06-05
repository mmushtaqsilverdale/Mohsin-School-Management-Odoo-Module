from odoo import models, fields, api

class resource_calendar(models.Model):
    _inherit = 'resource.calendar'

    is_school_calendar = fields.Boolean("School Calendar")
