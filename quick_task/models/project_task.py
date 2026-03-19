from odoo import api,fields,models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    po_id = fields.Many2one('purchase.order')
    def stat_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name':'purchase order',
            'res_model':'purchase.order',
            'view_mode':'list,form',
            'domain': [('p_id','=',self.id)]

        }