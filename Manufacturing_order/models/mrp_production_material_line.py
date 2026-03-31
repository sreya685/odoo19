from email.policy import default

from odoo import fields,models,api
from odoo.orm.decorators import ondelete


class MrpProductionMaterialLine(models.Model):
    _name = 'mrp.production.material.line'
    _description = 'Manufacturing Material Line'

    production_id = fields.Many2one('mrp.production.ext',ondelete='cascade')
    product_id = fields.Many2one('product.product')
    required_qty = fields.Integer(compute='_compute_req_qty',default=0,store=True)
    available_qty = fields.Integer(compute='_compute_available_qty',default=0,store=True)
    consumed_qty = fields.Integer()
    bom_line_qty = fields.Integer()



    @api.depends('production_id.quantity','bom_line_qty')
    def _compute_req_qty(self):
        for record in self:
            qty = record.production_id.quantity
            record.required_qty = record.bom_line_qty * qty

    @api.depends('product_id','consumed_qty','required_qty')
    def _compute_available_qty(self):


                 for line in self.production_id.material_line_ids:
                     if line.product_id.is_storable:
                         line.available_qty = line.product_id.qty_available
                         if line.consumed_qty == line.required_qty:
                                 # record.product_id.qty_available =  record.product_id.qty_available - line.consumed_qty
                                 # line.available_qty = line.product_id.qty_available
                                 line.available_qty = line.available_qty - line.consumed_qty
                                 line.product_id.qty_available =  line.available_qty
                                 if line.product_id.qty_available < 0:
                                     # record.product_id.qty_available = 0
                                     # line.available_qty = line.product_id.qty_available
                                     line.available_qty = 0
                                     line.product_id.qty_available = line.available_qty







