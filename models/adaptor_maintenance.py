from datetime import date
from odoo import fields, models


class AdaptorMaintenance(models.Model):
    _name = "it_infra.adaptor_maintenance"
    _description = "Adaptor Maintenance"
    _order = "date desc"

    name = fields.Char(string="Description", required=True)
    date = fields.Date(default=date.today(), required=True)
    adaptor_id = fields.Many2one(
        comodel_name="it_infra.adaptor",
        string="Adaptor",
        required=True,
    )
