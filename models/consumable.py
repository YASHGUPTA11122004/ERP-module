from datetime import timedelta, datetime
from odoo import models, fields, api
from odoo import _, exceptions, fields, models, api

class ConsumableItem(models.Model):
    _name = 'it_infra.consumable.item'
    _description = 'Consumable Item'

    name = fields.Char(string='Item Name', required=True)
    description = fields.Text(string='Description')


class ConsumableRecord(models.Model):
    _name = 'it_infra.consumable.record'
    _description = 'Consumable Record'

    location = fields.Char(string="Location")
    name = fields.Char(string='Make', required=True)
    user = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    purchase = fields.Boolean(string='Purchased', default=False)
    item = fields.Many2one('it_infra.consumable.item', string='Item', required=True)

    unique_id = fields.Char(string='Unique ID', readonly=True, copy=False, default='New')
    model_number = fields.Char(string='Model Number')
    serial_number = fields.Char(string='Serial Number')
    part_number = fields.Char(string='Part Number')
    description = fields.Text(string='Additional Description')

    updation_ids = fields.One2many(
        'it_infra.updation.maintenance', 'record_id', string='Updation & Maintenance Records'
    )
    maintenance_ids = fields.One2many(
        'it_infra.maintenance.details', 'record_id', string='Maintenance Records'
    )

    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Stocked In'),
        ('stored', 'Issued To'),
        ('return', 'Return'),
        ('decommissioned', 'Decommissioned'),
    ], string='State', default='draft')

    # Warranty and Expiration Fields
    warranty = fields.Selection(
        selection=[('1', '1 Year'), ('2', '2 Years'), ('3', '3 Years'), ('4', '4 Years'), ('5', '5 Years')],
        string="Warranty",
        required=True
    )
    warranty_expiration = fields.Date(string="Warranty Expiration", compute="_compute_warranty_expiration", store=True)
    warranty_remaining = fields.Char(string="Warranty Remaining", compute="_compute_warranty_remaining")
    warranty_certificate = fields.Binary(string="Warranty Certificate", attachment=True)
    invoice_copy = fields.Binary(string="Invoice Copy", attachment=True)
    supplier_email = fields.Char(string="Supplier's Email")
    supplier_name = fields.Char(string="Supplier's Name")
    supplier_contact = fields.Char(string="Supplier's Contact")
    supplier_website = fields.Char(string="Supplier's Website/OEM Website")

    # Define actions to change state
    def action_draft(self):
        self.status = 'draft'

    def action_active(self):
        self.status = 'active'

    def action_stored(self):
        self.status = 'stored'

    def action_return(self):
        self.status = 'active'

    def action_decommissioned(self):
        self.status = 'decommissioned'

    # Override the create method to auto-generate a unique ID
    @api.model
    def create(self, vals):
        if vals.get('unique_id', 'New') == 'New':
            vals['unique_id'] = self.env['ir.sequence'].next_by_code('it_infra.consumable.record') or 'New'
        return super(ConsumableRecord, self).create(vals)

    @api.depends("date", "warranty")
    def _compute_warranty_expiration(self):
        for record in self:
            if record.date and record.warranty:
                years = int(record.warranty)
                record.warranty_expiration = record.date + timedelta(days=365 * years)
            else:
                record.warranty_expiration = False

    @api.depends("warranty_expiration")
    def _compute_warranty_remaining(self):
        for record in self:
            if record.warranty_expiration:
                today = fields.Date.today()
                expiration_date = fields.Date.from_string(record.warranty_expiration)
                remaining_days = (expiration_date - today).days

                if remaining_days > 0:
                    years = remaining_days // 365
                    remaining_days %= 365
                    months = remaining_days // 30
                    remaining_days %= 30
                    days = remaining_days

                    record.warranty_remaining = f"{years} Year(s), {months} Month(s), {days} Day(s)"
                else:
                    record.warranty_remaining = "Warranty Expired"
            else:
                record.warranty_remaining = "No Warranty Expiry Date"

class UpdationMaintenance(models.Model):
    _name = 'it_infra.updation.maintenance'
    _description = 'Updation and Maintenance Record'

    record_id = fields.Many2one(
        'it_infra.consumable.record', string='Consumable Record', required=True, ondelete='cascade'
    )
    update_date = fields.Date(string='Update Date', default=fields.Date.today, required=True)
    update_description = fields.Text(string='Update Description', required=True)
    performed_by = fields.Many2one('res.users', string='Performed By', required=True)
    state = fields.Selection(
        [('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')],
        string='Status',
        default='pending',
        required=True
    )


