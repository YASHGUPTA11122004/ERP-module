from datetime import date
from odoo import fields, models


class PeripheralDeviceMaintenance(models.Model):
    _name = "it_infra.peripheral_device_maintenance"
    _description = "Peripheral Device Maintenance"
    _order = "date desc"

    name = fields.Char(string="Description", required=True)
    date = fields.Date(default=date.today(), required=True)
    peripheral_device_id = fields.Many2one(
        comodel_name="it_infra.peripheral_device",
        string="Peripheral Device",
        required=False,
    )
