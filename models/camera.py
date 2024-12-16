# it_infra/models/camera.py

from odoo import fields, models
from datetime import date


class Camera(models.Model):
    _name = "it_infra.camera"
    _description = "Camera"

    name = fields.Char(string="Camera Name", required=True)
    camera_type = fields.Selection([
        ('dslr', 'DSLR'),
        ('mirrorless', 'Mirrorless'),
        ('action', 'Action'),
        ('security', 'Security'),
        ('webcam', 'Webcam'),
        ('other', 'Other'),
    ], string="Camera Type", required=True)

    product_key = fields.Char(string="Product Key")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('stored', 'Stored'),
        ('decommissioned', 'Decommissioned'),
    ], string="Status", default='draft')

    office_suite_id = fields.Many2one(
        comodel_name="it_infra.software",
        string="Office Suite",
        domain=[("category_id.parent_id", "ilike", "Office Suite")],
    )

    camera_maintenance_ids = fields.One2many(
        comodel_name="it_infra.camera_maintenance",
        inverse_name="camera_id",
        string="Maintenance History",
    )

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_active(self):
        self.write({'state': 'active'})

    def action_stored(self):
        self.write({'state': 'stored'})

    def action_decommissioned(self):
        self.write({'state': 'decommissioned'})
