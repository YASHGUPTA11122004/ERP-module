from datetime import timedelta, datetime
from odoo import _, exceptions, fields, models, api

class Server(models.Model):
    _name = "it_infra.server"
    _description = "IT Infrastructure Server"
    _inherit = "it_infra.computer"

    SERVER_TYPE_SELECTION = [
        ("bare_metal", "Bare Metal"),
        ("bare_metal_sa", "Bare Metal (Standalone)"),
        ("cloud", "Cloud"),
        ("hypervisor", "Hypervisor"),
        ("vm", "Virtual Machine"),
        ("docker", "Docker Stack"),
    ]

    name = fields.Char(string='Server Name')

    # Convert processor field to a dropdown with 'AMD' and 'Intel'
    processor = fields.Selection([
        ('amd', 'AMD'),
        ('intel', 'Intel')
    ], string="Processor", required=True)

    disk = fields.Selection(
        selection=[('HDD', 'HDD'), ('SSD', 'SSD'), ('Hybrid','Hybrid')],
        string="Disk"
    )
    ram = fields.Char(string="RAM Capacity")
    other_configuration_details = fields.Text(string="Other Configuration Details")
    os_id = fields.Many2one(comodel_name="it_infra.software", string="Operating System")
    ram_type = fields.Selection([('sram','SRAM'),('dram','DRAM'),('sdram','SDRAM'),('sdr sdram','SDR SDRAM'),('ddr sdram','DDR SDRAM')], string="Ram Type")
    server_type = fields.Selection(selection=SERVER_TYPE_SELECTION, string="Server Type")
    category_ids = fields.Many2many(
        comodel_name="it_infra.server_category",
        relation="server_category_rel",
        string="Categories",
    )
    location_id = fields.Many2one(
        comodel_name="it_infra.location", required=True, string="Present Address/Installed Location"
    )
    internal_location = fields.Boolean(related="location_id.internal")
    mac_address = fields.Char(string="MAC Address")
    ip_address = fields.Char(string="IP Address")

    date_of_purchase = fields.Date(string='Date of Purchase')
    invoice_copy = fields.Binary(string='Invoice Copy', attachment=True)
    seller_email = fields.Char(string="Supplier's Email")
    seller_name = fields.Char(string="Supplier's Name")
    seller_contact = fields.Char(string="Supplier's Contact")
    seller_website = fields.Char(string="Supplier's Website/OEM Website")
    warranty_period_months = fields.Integer(
        string='Warranty (Months)', required=True, default=6
    )
    warranty_expired = fields.Date(string='Warranty Expiration Date', compute='_compute_warranty_expiry', store=True)
    warranty_related_doc_certificate = fields.Binary(string="Warranty Related Document/Certificate", attachment=True)
    warranty_certificate = fields.Binary(string="Warranty Certificate", attachment=True)
    warranty_remaining = fields.Char(string="Warranty Remaining", compute="_compute_warranty_remaining")
    employee = fields.Many2one("hr.employee")

    user_info_ids = fields.One2many(
        comodel_name="it_infra.user_info",
        inverse_name="server_id",
        string="User Information",
    )
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
            vals['reference_number'] = f"SRV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        return super(Server, self).create(vals)

    def write(self, vals):
        # Prevent any changes to the reference number
        if 'reference_number' in vals:
            raise exceptions.UserError(_("You cannot modify the Reference Number."))
        return super(Server, self).write(vals)

    server_maintenance_ids = fields.One2many(
        comodel_name="it_infra.server_maintenance",
        inverse_name="server_id",
        string="Maintenance History",
    )

    server_updation_ids = fields.One2many(
        comodel_name="it_infra.server_updation",
        inverse_name="server_id",
        string="Technical Update History",
    )
    @api.depends('date_of_purchase', 'warranty_period_months')
    def _compute_warranty_expiry(self):
        for server in self:
            if server.date_of_purchase and server.warranty_period_months >= 6:
                purchase_date = fields.Date.from_string(server.date_of_purchase)
                server.warranty_expired = purchase_date + timedelta(days=30 * server.warranty_period_months)
            else:
                server.warranty_expired = False

    @api.depends('warranty_expired')
    def _compute_warranty_remaining(self):
        for server in self:
            if server.warranty_expired:
                today = fields.Date.today()
                expiration_date = fields.Date.from_string(server.warranty_expired)
                remaining_days = (expiration_date - today).days

                if remaining_days > 0:
                    years = remaining_days // 365
                    remaining_days %= 365
                    months = remaining_days // 30
                    remaining_days %= 30
                    days = remaining_days

                    # Constructing the remaining warranty string in Years, Months, Days format
                    warranty_remaining = f"{years} Year(s), {months} Month(s), {days} Day(s)"
                    server.warranty_remaining = warranty_remaining
                else:
                    server.warranty_remaining = "Warranty Expired"
            else:
                server.warranty_remaining = "No Warranty Expiry Date"

    server_maintenance_ids = fields.One2many(
        comodel_name="it_infra.server_maintenance",
        inverse_name="server_id",
        string="Maintenance History",
    )

    server_updation_ids = fields.One2many(
        comodel_name="it_infra.server_updation",
        inverse_name="server_id",
        string="Technical Update History",
    )


class UserInfo(models.Model):
    _name = "it_infra.user_info"

    username = fields.Char(string='Username')
    userID = fields.Char(string='User ID')
    department = fields.Char(string='Department')
    server_id = fields.Many2one(
        comodel_name="it_infra.server",
        string="Server",
        required=False,
    )

class ServerMaintenance(models.Model):
    _name = "it_infra.server_maintenance"
    _description = "Server Maintenance"
    _order = "date desc"

    name = fields.Char(string="Description", required=True)
    date = fields.Date(default=fields.Date.context_today, required=True)
    server_id = fields.Many2one(
        comodel_name="it_infra.server",
        string="Server",
        required=False,
    )

class ServerUpdation(models.Model):
    _name = "it_infra.server_updation"
    _inherit = "it_infra.server_maintenance"

    def update_server_maintenance(self, maintenance_id, new_values):
        maintenance_record = self.browse(maintenance_id)
        if maintenance_record:
            maintenance_record.write(new_values)
        else:
            raise exceptions.UserError(_("Maintenance record not found."))
