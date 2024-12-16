from odoo import models, fields

class PrinterMaintenance(models.Model):
    _name = 'it_infra.printer.maintenance'
    _description = 'Printer Maintenance'

    name = fields.Char(string='Maintenance Name', required=True)
    maintenance_date = fields.Date(string='Maintenance Date', required=True)
    description = fields.Text(string='Description')

    printer_id = fields.Many2one(
        'it_infra.printer',  # The related model for the printer
        string='Printer',  # Field label for the UI
        required=True,  # Making the printer selection mandatory
        ondelete='cascade'  # Delete the maintenance record if the associated printer is deleted
    )

    maintenance_type = fields.Selection([
        ('repair', 'Repair'),
        ('service', 'Service'),
        ('refurbishment', 'Refurbishment'),
    ], string='Maintenance Type', required=True)  # The type of maintenance done