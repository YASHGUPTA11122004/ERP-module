from odoo import fields, models


class Cable(models.Model):
    _name = "it_infra.cable"
    _description = "Cable"
    _inherit = "it_infra.computer"

    name = fields.Char(string="Cable Name", required=True)
    cable_type = fields.Selection([
        ('hdmi', 'HDMI'),
        ('usb', 'USB'),
        ('ethernet', 'Ethernet'),
        ('power', 'Power'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ], string="Cable Type", required=True)

    product_key = fields.Char(string="Product Key")

    office_suite_id = fields.Many2one(
        comodel_name="it_infra.software",
        string="Office Suite",
        domain=[("category_id.parent_id", "ilike", "Office Suite")],
    )

    cable_maintenance_ids = fields.One2many(
        comodel_name="it_infra.cable_maintenance",
        inverse_name="cable_id",
        string="Maintenance History",
    )