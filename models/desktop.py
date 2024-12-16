from datetime import timedelta, datetime
from odoo import _, exceptions, fields, models, api


class Desktop(models.Model):
    _name = "it_infra.desktop"
    _description = "Desktop"
    _inherit = "it_infra.computer"

    name = fields.Char()
    product_id = fields.Char(string="Product ID")
    model = fields.Char(string="Model")
    user_id = fields.Many2one('res.users', string="User ID")
    employee = fields.Many2one("hr.employee")
    office_suite_id = fields.Many2one(
        comodel_name="it_infra.software",
        string="Office Suite",
        domain=[("category_id.parent_id", "ilike", "Office Suite")],
    )

    desktop_maintenance_ids = fields.One2many(
        comodel_name="it_infra.desktop_maintenance",
        inverse_name="desktop_id",
        string="Maintenance History",
    )

    # Additional fields
    os_id = fields.Many2one(comodel_name="it_infra.software", string="Operating System")
    hostname = fields.Char(string="Hostname")
    ip_address = fields.Char(string="IP Address")
    username = fields.Char(string="Username")
    stock_number = fields.Char(string="Stock Number")
    purchase_date = fields.Date(string="Purchase Date")
    invoice_copy = fields.Binary(string='Invoice Copy', attachment=True)
    seller_email = fields.Char(string="Supplier's Email")
    seller_name = fields.Char(string="Supplier's Name")
    seller_contact = fields.Char(string="Supplier's Contact")
    seller_website = fields.Char(string="Supplier's Website/OEM Website")

    # Warranty and Expiration Fields
    warranty = fields.Selection(
        selection=[('1', '1 Year'), ('2', '2 Years'), ('3', '3 Years'), ('4', '4 Years'), ('5', '5 Years')],
        string="Warranty",
        required=True
    )
    warranty_expiration = fields.Date(string="Warranty Expiration", compute="_compute_warranty_expiration", store=True)
    warranty_remaining = fields.Char(string="Warranty Remaining", compute="_compute_warranty_remaining")
    warranty_certificate = fields.Binary(string="Warranty Certificate", attachment=True)

    source_doc_number = fields.Char(string="Source Document Number")
    processor = fields.Selection(
        selection=[('amd', 'AMD'), ('intel', 'Intel')],
        string="Processor",
        required=True
    )
    disk = fields.Selection(
        selection=[('HDD', 'HDD'), ('SSD', 'SSD'), ('Hybrid','Hybrid')],
        string="Disk"
    )
    ram = fields.Char(string="RAM Capacity")
    ram_type = fields.Selection([('sram', 'SRAM'), ('dram', 'DRAM'), ('sdram', 'SDRAM'), ('sdr sdram', 'SDR SDRAM'),
                                 ('ddr sdram', 'DDR SDRAM')], string="Ram Type")
    graphic_card = fields.Char(string="Graphic Card")
    department = fields.Char(string="Department/Section")
    location = fields.Char(string="Location")

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
            vals['reference_number'] = f"DPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        return super(Desktop, self).create(vals)

    def write(self, vals):
        # Prevent any changes to the reference number
        if 'reference_number' in vals:
            raise exceptions.UserError(_("You cannot modify the Reference Number."))
        return super(Desktop, self).write(vals)

    @api.depends("purchase_date", "warranty")
    def _compute_warranty_expiration(self):
        for record in self:
            if record.purchase_date and record.warranty:
                # Calculate warranty expiration based on purchase_date and warranty duration
                years = int(record.warranty)
                record.warranty_expiration = record.purchase_date + timedelta(days=365 * years)
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

                    # Format the remaining warranty as Years, Months, Days
                    warranty_remaining = f"{years} Year(s), {months} Month(s), {days} Day(s)"
                    record.warranty_remaining = warranty_remaining
                else:
                    record.warranty_remaining = "Warranty Expired"
            else:
                record.warranty_remaining = "No Warranty Expiry Date"
