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



    @api.depends('production_id','production_id.material_line_ids.bom_line_qty')
    def _compute_req_qty(self):
        for record in self:
            qty = record.production_id.quantity
            for line in record.production_id.material_line_ids:
                line.required_qty = line.bom_line_qty * qty

    @api.depends('product_id','production_id.material_line_ids.consumed_qty','production_id.material_line_ids.required_qty')
    def _compute_available_qty(self):
        for record in self:
            if record.product_id.is_storable:
                 for line in record.production_id.material_line_ids:
                     line.available_qty = line.product_id.qty_available
                     if line.consumed_qty == line.required_qty:
                             line.product_id.qty_available = line.available_qty - line.consumed_qty
                             if line.product_id.qty_available <0:
                                 line.product_id.qty_available =0






