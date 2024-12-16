from datetime import timedelta, datetime
from odoo import _, exceptions, fields, models, api


class Workstation(models.Model):
    _name = "it_infra.workstation"
    _description = "Workstation"
    _inherit = "it_infra.computer"

    name = fields.Char(string="Name", required=True)

    # Basic Details
    workstation_name = fields.Char(string="Workstation Name", required=True)
    ip_address = fields.Char(string="IP Address")
    mac_address = fields.Char(string="MAC Address")
    os_id = fields.Many2one(comodel_name="it_infra.software", string="Operating System")
    processor = fields.Selection(
        selection=[('amd', 'AMD'), ('intel', 'Intel')],
        string="Processor",
        required=True
    )
    disk = fields.Selection(
        selection=[('HDD', 'HDD'), ('SSD', 'SSD'), ('Hybrid','Hybrid')],
        string="Disk"
    )
    ram_type = fields.Selection([('sram', 'SRAM'), ('dram', 'DRAM'), ('sdram', 'SDRAM'), ('sdr sdram', 'SDR SDRAM'),
                                 ('ddr sdram', 'DDR SDRAM')], string="Ram Type")
    ram = fields.Char(string="RAM Capacity")
    other_configuration_details = fields.Text(string="Other Configuration Details")
    installed_location = fields.Char(string="Installed Location")

    # Purchase and Warranty Details
    purchase_date = fields.Date(string="Date of Purchase")
    warranty_months = fields.Integer(string="Warranty in Months", default=6)
    warranty_expiration = fields.Date(string="Warranty Expiration", compute="_compute_warranty_expiration", store=True)
    warranty_remaining = fields.Char(string="Warranty Remaining", compute="_compute_warranty_remaining")
    invoice_copy = fields.Binary(string="Invoice Copy", attachment=True)

    # Seller Details
    seller_name = fields.Char(string="Supplier's Name")
    seller_email = fields.Char(string="Supplier's Email")
    seller_contact = fields.Char(string="Supplier's Contact")
    seller_website = fields.Char(string="Supplier's Website/OEM Website")

    # Warranty Document
    warranty_certificate = fields.Binary(string="Warranty Certificate", attachment=True)

    # User Details Table

    # Maintenance History
    maintenance_history_ids = fields.One2many(
        comodel_name="it_infra.workstation_maintenance",
        inverse_name="workstation_id",
        string="Maintenance History"
    )

    reference_number = fields.Char(
        string="Reference Number",
        readonly=True,
        copy=False,
        required=True,
        default=lambda self: self._generate_reference_number()
    )
    employee=fields.Many2one("hr.employee")
    @api.model
    def create(self, vals):
        # Check if the reference number is not set, and generate a unique reference number
        if 'reference_number' not in vals or vals['reference_number'] == 'New':
            vals['reference_number'] = self._generate_reference_number()
        return super(Workstation, self).create(vals)

    def write(self, vals):
        # Prevent any changes to the reference number
        if 'reference_number' in vals:
            raise exceptions.UserError(_("You cannot modify the Reference Number."))
        return super(Workstation, self).write(vals)

    def _generate_reference_number(self):
        # Generate a unique reference number using the current datetime
        return f"WKS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Updation History
    updation_history_ids = fields.One2many(
        comodel_name="it_infra.workstation_updation",
        inverse_name="workstation_id",
        string="Updation History"
    )

    # Computed Field for Operating System
    operating_system = fields.Char(
        string="Operating System",
        compute="_compute_operating_system",
        store=True
    )

    @api.depends('os_id')
    def _compute_operating_system(self):
        for record in self:
            if record.os_id:
                record.operating_system = record.os_id.name
            else:
                record.operating_system = False

    @api.depends("purchase_date", "warranty_months")
    def _compute_warranty_expiration(self):
        for record in self:
            if record.purchase_date:
                record.warranty_expiration = record.purchase_date + timedelta(days=30 * record.warranty_months)
            else:
                record.warranty_expiration = False

    @api.depends('warranty_expiration')
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

                    # Constructing the remaining warranty string in Years, Months, Days format
                    warranty_remaining = f"{years} Year(s), {months} Month(s), {days} Day(s)"
                    record.warranty_remaining = warranty_remaining
                else:
                    record.warranty_remaining = "Warranty Expired"
            else:
                record.warranty_remaining = "No Warranty Expiry Date"

    @api.model
    def create(self, vals):
        if 'workstation_name' in vals:
            vals['name'] = vals['workstation_name']
        return super(Workstation, self).create(vals)


class WorkstationMaintenance(models.Model):
    _name = "it_infra.workstation_maintenance"
    _description = "Workstation Maintenance History"

    workstation_id = fields.Many2one(comodel_name="it_infra.workstation", string="Workstation", required=True)
    maintenance_date = fields.Date(string="Maintenance Date", required=True)
    description = fields.Text(string="Maintenance Description")
    performed_by = fields.Many2one(comodel_name="res.users", string="Performed By")


class WorkstationUpdation(models.Model):
    _name = "it_infra.workstation_updation"
    _description = "Workstation Updation History"

    workstation_id = fields.Many2one(comodel_name="it_infra.workstation", string="Workstation", required=True)
    update_date = fields.Date(string="Update Date", required=True)
    update_description = fields.Text(string="Update Description")
    updated_by = fields.Many2one(comodel_name="res.users", string="Updated By")
