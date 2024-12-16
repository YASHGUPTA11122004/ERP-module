from datetime import date
from odoo import fields, models


class CableMaintenance(models.Model):
    _name = "it_infra.cable_maintenance"
    _description = "Cable Maintenance"
    _order = "date desc"

    name = fields.Char(string="Description", required=True)
    date = fields.Date(default=date.today(), required=True)
    cable_id = fields.Many2one(
        comodel_name="it_infra.cable",
        string="Cable",
        required=True,
    )