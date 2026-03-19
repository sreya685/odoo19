from odoo import api, fields, models,_
from odoo import Command
from odoo.addons.test_convert.tests.test_env import record


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    p_id = fields.Many2one('project.task')
    def button_confirm(self):

        res = super().button_confirm()
        for record in self:

              project=False
              if record.order_line.product_id.project:
                      project = record.order_line.product_id.mapped('project')[0]

              q = sum(record.order_line.mapped('product_qty'))
              v = sum(record.order_line.mapped('price_unit'))
              n = record.order_line.mapped('name')

              if project != False:
                   child_id = []
                   for orderline in record.order_line:
                       for product in orderline:
                           child_id.append(Command.create({'name': product.product_id.name, 'project_id': project.id}))
                   status= self.env['project.task.type'].search([('name','=','In Progress')])
                   h=self.env['project.task'].create({
                        'name': f'PO Confirmation  {self.id}',
                        'stage_id': status.id,
                        'child_ids': child_id,
                        'description': f"product quantity: {str(q)}, product price: {str(v)}",
                        'project_id': project.id,
                        'po_id': self.id,

                      })
                   record.p_id = h.id
              record.message_post(
                  body=_(f"The purchase order has been confirmed .{n}"),
                  message_type="comment",
                  subtype_xmlid="mail.mt_comment"
              )

        return res

    def stat_po_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name':'project task',
            'res_model':'project.task',
            'view_mode':'list,form',
            'domain': [('po_id','=',self.id)]

        }











