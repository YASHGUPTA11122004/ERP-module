from datetime import timedelta, datetime, date
from odoo import _, exceptions, fields, models, api


class Printer(models.Model):
    _name = "it_infra.printer"
    _description = "Printer"
    _inherit = "it_infra.computer"

    name = fields.Char(required=True)
    model = fields.Char(string="Model")
    ip_address = fields.Char(string="IP Address")
    mac_address = fields.Char(string="MAC Address")
    location = fields.Char(string="Location")
    purchase_date = fields.Date(string="Purchase Date")
    invoice_copy = fields.Binary(string='Invoice Copy', attachment=True)
    employee = fields.Many2one('hr.employee', string="Employee", required=False, default=None)
    warranty = fields.Selection([
        ('1', '1 Year'),
        ('2', '2 Years'),
        ('3', '3 Years'),
        ('4', '4 Years'),
        ('5', '5 Years')
    ], string="Warranty")

    warranty_expired = fields.Date(string="Warranty Expiry Date", compute="_compute_warranty_expired", store=True)
    warranty_remaining = fields.Char(string="Remaining Warranty", compute="_compute_warranty_remaining", store=True)
    warranty_certificate = fields.Binary(string="Warranty Certificate", attachment=True)

    source_doc_numbers = fields.Char(string="Source Document Number")
    printer_type = fields.Char(string="Printer Type")
    seller_website = fields.Char(string="Supplier's Website/OEM Website")

    # Convert toner detail into a dropdown
    toner_detail = fields.Selection([
        ('toner_1', 'Toner Type 1'),
        ('toner_2', 'Toner Type 2'),
        ('toner_3', 'Toner Type 3'),
        ('toner_4', 'Toner Type 4'),
        ('toner_5', 'Toner Type 5'),
        # Add more toner types as needed
    ], string="Toner Type")

    # Convert cartridge into a dropdown
    cartridge = fields.Selection([
        ('cartridge_1', 'Cartridge Type 1'),
        ('cartridge_2', 'Cartridge Type 2'),
        ('cartridge_3', 'Cartridge Type 3'),
        ('cartridge_4', 'Cartridge Type 4'),
        ('cartridge_5', 'Cartridge Type 5'),
        # Add more cartridge types as needed
    ], string="Cartridge Type")

    technology = fields.Selection([
        ('laser', 'Laser'),
        ('inkjet', 'Inkjet'),
        ('dot_matrix', 'Dot Matrix'),
        ('monochrome', 'Monochrome'),
        ('color', 'Color'),
        ('general_purpose', 'General Purpose'),
        ('mfp_machine_cannon', 'MFP Machine (canon 2945)'),
        ('mono_MFP', 'Mono MFP'),
        ('color_MFP', 'Color MFP'),
    ], string="Technology")

    seller_email = fields.Char(string="Supplier's Email")
    seller_name = fields.Char(string="Supplier's Name")
    seller_contact = fields.Char(string="Supplier's Contact")

    credential_ids = fields.One2many('it_infra.printer.credentials', 'printer_id', string="Credentials")
    updation_ids = fields.One2many('it_infra.printer.updation', 'printer_id', string="Updation History")
    maintenance_ids = fields.One2many(
        'it_infra.printer.maintenance',
        'printer_id',
        string='Maintenance Records',
    )

    network_feature = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="Network Feature", required=True, default='no')

    network_features = fields.Boolean(
        string="Network Feature", required=True, )

    printing_capability_a3 = fields.Boolean(string="A3")
    printing_capability_a4 = fields.Boolean(string="A4")
    printing_capability_a5 = fields.Boolean(string="A5")

    @api.depends('warranty', 'purchase_date')
    def _compute_warranty_expired(self):
        for record in self:
            if record.purchase_date and record.warranty:
                warranty_period = int(record.warranty)
                record.warranty_expired = record.purchase_date + timedelta(days=365 * warranty_period)
            else:
                record.warranty_expired = False

    @api.depends('warranty_expired')
    def _compute_warranty_remaining(self):
        for record in self:
            if record.warranty_expired:
                remaining_time = record.warranty_expired - date.today()
                if remaining_time.days > 0:
                    years, days = divmod(remaining_time.days, 365)
                    months, days = divmod(days, 30)
                    record.warranty_remaining = f"{years} Years, {months} Months, {days} Days"
                else:
                    record.warranty_remaining = "Expired"
            else:
                record.warranty_remaining = "No Warranty Info"

    @api.model
    def create(self, vals):
        """Override create method to add custom logic on record creation."""
        record = super(Printer, self).create(vals)
        if not record.source_doc_numbers:
            record.source_doc_numbers = f"PR-{record.id:04d}"
        return record

    reference_number = fields.Char(
        string="Reference Number",
        readonly=True,
        copy=False,
        required=True,
        default=lambda self: _("New")
    )

    @api.model
    def create(self, vals):
        # Generate a unique reference number only once
        if vals.get('reference_number', 'New') == 'New':
            vals['reference_number'] = f"PRT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        return super(Printer, self).create(vals)

    def write(self, vals):
        # Prevent any changes to the reference number
        if 'reference_number' in vals:
            raise exceptions.UserError(_("You cannot modify the Reference Number."))
        return super(Printer, self).write(vals)

class PrinterCredentials(models.Model):
    _name = 'it_infra.printer.credentials'
    _description = 'Printer Credentials'

    user_id = fields.Many2one('res.users', string="User")
    username = fields.Char(string="UserID")
    password = fields.Char(string="Password")
    printer_id = fields.Many2one('it_infra.printer', string="Printer", required=True)


class PrinterUpdation(models.Model):
    _name = 'it_infra.printer.updation'
    _description = 'Printer Updation'

    update_name = fields.Char(string="Update Name", required=True)
    update_date = fields.Date(string="Update Date", default=fields.Date.today)
    printer_id = fields.Many2one('it_infra.printer', string="Printer", required=True)
