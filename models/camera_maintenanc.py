# it_infra/models/camera_maintenance.py

from odoo import fields, models
from datetime import date


class CameraMaintenance(models.Model):
    _name = "it_infra.camera_maintenance"
    _description = "Camera Maintenance"
    _order = "date desc"

    name = fields.Char(string="Description", required=True)
    date = fields.Date(default=date.today(), required=True)
    camera_id = fields.Many2one(
        comodel_name="it_infra.camera",
        string="Camera",
        required=True,
    )
