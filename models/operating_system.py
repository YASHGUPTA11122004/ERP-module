from odoo import fields, models


class OperatingSystem(models.Model):

    _name = "it_infra.operating_system"
    _description = "Operating System"

    _architecture_ = [("(x86)", "32 bits"), ("(x64)", "64 bits")]

    name = fields.Char(required=True)

    version = fields.Char()

    architecture = fields.Selection(selection=_architecture_)

    category_id = fields.Many2one(
        comodel_name="it_infra.software_category",
        string="Category",
        required=True,
    )

    def name_get(self):
        result = []
        for os in self:
            if os.category_id.parent_id.name == "Operating System":
                result.append(
                    (
                        os.id,
                        "%s %s %s"
                        % (
                            os.name,
                            os.version or "",
                            os.architecture or "",
                        ),
                    )
                )
            else:
                result.append(
                    (os.id, "%s %s" % (os.name, os.version or ""))
                )
        return result
