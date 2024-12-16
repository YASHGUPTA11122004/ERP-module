from datetime import date

from odoo import fields, models


class DesktopMaintenance(models.Model):

    _name = "it_infra.desktop_maintenance"
    _description = "Desktop Maintenance"
    _order = "date desc"

    name = fields.Char(string="Description", required=True)

    date = fields.Date(default=date.today(), required=True)

    desktop_id = fields.Many2one(comodel_name="it_infra.desktop")
