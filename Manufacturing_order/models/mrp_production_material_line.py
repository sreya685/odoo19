from email.policy import default

from odoo import fields,models,api



class MrpProductionMaterialLine(models.Model):
    _name = 'mrp.production.material.line'
    _description = 'Manufacturing Material Line'

    production_id = fields.Many2one('mrp.production.ext')
    product_id = fields.Many2one('product.product')
    required_qty = fields.Integer(compute='_compute_req_qty',default=0,store=True)
    available_qty = fields.Integer(compute='_compute_available_qty',default=0,store=True)
    consumed_qty = fields.Integer()

    @api.depends('production_id')
    def _compute_req_qty(self):
        for record in self:
            record.required_qty = record.production_id.bom_id.product_qty * record.production_id.quantity

    @api.depends('product_id')
    def _compute_available_qty(self):
        for record in self:
            if record.product_id.is_storable:
                 record.available_qty = record.product_id.qty_available






