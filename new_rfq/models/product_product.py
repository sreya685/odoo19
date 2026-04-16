from odoo import api,fields,models



class ProductProduct(models.Model):
    _inherit = 'product.product'




    def button_po(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Button wizard',
            'res_model': 'wizard.po',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,

            }
        }