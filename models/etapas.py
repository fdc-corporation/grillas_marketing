from odoo import models, fields, api

class EtapasGrillaMarketing(models.Model):
    _inherit = "project.task.type"
    _description = "Etapas Grilla Marketing"

    is_etapa_blog = fields.Boolean(
        string="¿Es etapa de blog?" )