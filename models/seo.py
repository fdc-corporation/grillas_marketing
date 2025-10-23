from odoo import models, fields, api, _
 

class SeoSettings(models.Model):
    _name = "seo.project"

    name = fields.Char(string="Nombre")
    