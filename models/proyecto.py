from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo import _
import re


class Proyecto(models.Model):
    _inherit = "project.task"

    responsable = fields.Many2many(
        "res.users", string="Responsables"
    )
    marcas = fields.Many2many("marcas.grilla_marketing", string="Marcas")
    plataformas = fields.Many2many("plataformas.grilla_marketing", string="Plataformas")
    formatos = fields.Many2many("formatos.grilla_marketing", string="Formatos")
    guion = fields.Html(string="Guion")
    evento_id = fields.Many2one("calendar.event", string="Evento en calendario")
    not_blog = fields.Boolean(
        string="No es un blog", default=False, help="Indica si la tarea es un blog", tracking=True)
    # blog_id = fields.Many2one(
    #     "blog.post", string="Blog", help="Blog asociado a la tarea" )
    contenido_blog = fields.Html(
        string="Contenido del blog",
        help="Contenido del blog asociado a la tarea")
    seo_palabras = fields.Html()
    proposito = fields.Many2many("propositos.grilla_marketing", string="Propósitos")


    def write (self, vals):
        res = super(Proyecto, self).write(vals)
        if "stage_id" in vals:
            self.alert_state_value()
        return res  


    def alert_state_value (self):
        for record in self:
            contenido = (record.contenido_blog or '').strip()
            contenido_texto = re.sub('<[^<]+?>', '', contenido).strip()
            print("Contenido del blog:", contenido_texto)
            if not record.not_blog :
                if record.stage_id.is_etapa_blog:
                    if not contenido_texto:
                        raise UserError(_("Debe agregar contenido del blog para pasar a la siguiente etapa."))



    def create_evento_tarea(self):
        try:
            for record in self:
                plataformas_id = []
                for plataforma in record.plataformas:
                    plataformas_id.append(plataforma.id)

                if record.date_deadline:
                    evento = self.env["calendar.event"].create(
                        {
                            "name": record.name + " - " + record.project_id.name,
                            "start": record.date_deadline,
                            "stop": record.date_deadline,
                            "grilla_id": record.id,
                            "partner_ids": [self.env.user.partner_id.id],
                            "plataformas": [(6, 0, plataformas_id)],
                        }
                    )
                    self.write(
                        {
                            "evento_id": evento.id,
                        }
                    )
                else:
                    raise UserError(_("Debe especificar una fecha de programacion"))
        except Exception as e:
            raise UserError(_("No se pudo ejecutar la tarea"))

    def set_notification(self):
        for record in self.env["project.task"].search([("date_deadline", "!=", False), ("stage_id.name", "not in", ["Material Listo", "Publicado / Usado"])]):
            fecha_original = record.date_deadline
            fecha_modificada = fecha_original - relativedelta(days=1)

            # Comparar solo las fechas sin las horas
            if fecha_modificada.date() == fields.Datetime.now().date():
                print("------------------------SE ENVIO LA NOTIFICACION-------------------------")
                message = "¡La tarea ha alcanzado la fecha de vencimiento!"
                partner_ids = [user.partner_id.id for user in record.user_ids]

                # Crear la notificación
                record.message_post(
                    body="¡La tarea ha alcanzado la fecha de vencimiento!",
                    message_type="notification",
                    subtype_xmlid="mail.mt_comment",
                )
                record.message_notify(
                    body=message,
                    partner_ids=partner_ids,
                    subject=f"La Tarea {record.name} esta en la fecha limite!!",
                )

            # Debug de las fechas
            print("------------------------FECHA DE VENCIMIENTO-------------------------")
            print(fecha_modificada.date())  # Solo la parte de la fecha
            print(fecha_original)
            print(fields.Datetime.now().date())  # Solo la parte de la fecha

