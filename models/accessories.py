from odoo import fields, models


class Accessory(models.Model):
    _name = "it_infra.accessory"
    _description = "Accessory"
    _inherit = "it_infra.computer"

    name = fields.Char(string="Accessory Name", required=True)
    accessory_type = fields.Selection([
        ('hdmi', 'HDMI'),
        ('usb', 'USB'),
        ('ethernet', 'Ethernet'),
        ('power', 'Power'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ], string="Accessory Type", required=True)

    product_key = fields.Char(string="Product Key")

    office_suite_id = fields.Many2one(
        comodel_name="it_infra.software",
        string="Office Suite",
        domain=[("category_id.parent_id", "ilike", "Office Suite")],
    )

    accessory_maintenance_ids = fields.One2many(
        comodel_name="it_infra.accessory_maintenance",
        inverse_name="accessory_id",
        string="Maintenance History",
    )