from odoo import fields, models


class Provider(models.Model):

    _name = "it_infra.provider"
    _description = "Provider"

    name = fields.Char()

    membership_number = fields.Char()

    contact = fields.Char()

    ip_address = fields.Char(string="IP Address")

    netmask = fields.Char()

    gateway = fields.Char()

    dns_server_1 = fields.Char()

    dns_server_2 = fields.Char()

    notes = fields.Html()
