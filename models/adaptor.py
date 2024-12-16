from odoo import fields, models


class Adaptor(models.Model):
    _name = "it_infra.adaptor"
    _description = "Adaptor"
    _inherit = "it_infra.computer"

    name = fields.Char(string="Adaptor Name", required=True)
    adaptor_type = fields.Selection([
        ('hdmi', 'HDMI'),
        ('usb', 'USB'),
        ('ethernet', 'Ethernet'),
        ('power', 'Power'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ], string="Adaptor Type", required=True)

    product_key = fields.Char(string="Product Key")

    office_suite_id = fields.Many2one(
        comodel_name="it_infra.software",
        string="Office Suite",
        domain=[("category_id.parent_id", "ilike", "Office Suite")],
    )

    adaptor_maintenance_ids = fields.One2many(
        comodel_name="it_infra.adaptor_maintenance",
        inverse_name="adaptor_id",
        string="Maintenance History",
    )
