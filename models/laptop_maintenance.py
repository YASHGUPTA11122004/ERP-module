from datetime import date
from odoo import fields, models

class LaptopMaintenance(models.Model):
    _name = "it_infra.laptop_maintenance"
    _description = "Laptop Maintenance"
    _order = "date desc"

    name = fields.Char(string="Description", required=True)
    date = fields.Date(default=date.today(), required=True)
    laptop_id = fields.Many2one(comodel_name="it_infra.laptop")
