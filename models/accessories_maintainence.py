from datetime import date
from odoo import fields, models


class AccessoryMaintenance(models.Model):
    _name = "it_infra.accessory_maintenance"
    _description = "Accessory Maintenance"
    _order = "date desc"

    name = fields.Char(string="Description", required=True)
    date = fields.Date(default=date.today(), required=True)
    accessory_id = fields.Many2one(
        comodel_name="it_infra.accessory",
        string="Accessory",
        required=True,
    )