from odoo import fields, models
class aman(models.Model):
    _name = 'abc.abc'
    _description = "sdfg"

    name=fields.Char()

class PeripheralDevice(models.Model):
    _name = "it_infra.peripheral_device"
    _description = "Peripheral Device"
    _inherit = "it_infra.computer"

    name = fields.Char(string="Device Name", required=True)
    device_type = fields.Selection([
        ('printer', 'Printer'),
        ('scanner', 'Scanner'),
        ('monitor', 'Monitor'),
        ('keyboard', 'Keyboard'),
        ('mouse', 'Mouse'),
        ('other', 'Other'),
    ], string="Device Type", required=True)

    product_key = fields.Char(string="Product Key")  # Added field

    office_suite_id = fields.Many2one(
        comodel_name="it_infra.software",
        string="Office Suite",
        domain=[("category_id.parent_id", "ilike", "Office Suite")],
    )

    # # Adding the mandatory Operating System field
    # os_id = fields.Many2one(
    #     comodel_name="it_infra.operating_system",  # Update this with the correct model name
    #     string="Operating System",
    #     required=True,  # Marking this field as mandatory
    # )

    peripheral_device_maintenance_ids = fields.One2many(
        comodel_name="it_infra.peripheral_device_maintenance",
        inverse_name="peripheral_device_id",
        string="Maintenance History",
    )
