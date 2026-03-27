
from odoo import api,fields,models,_
from odoo.exceptions import ValidationError


class MrpProductionExt(models.Model):
    _name = 'mrp.production.ext'
    _description = 'Mrp Production Ext'
    _rec_name = 'mrp_name'

    mrp_name = fields.Char(string='Production Name',default=lambda self: _('New'))
    product_id = fields.Many2one('product.product')
    bom_id = fields.Many2one('mrp.bom')
    quantity = fields.Integer(string='Quantity')
    planned_date = fields.Date(string='Planned Date')
    state=fields.Selection(
        selection=[('draft','Draft'),('confirmed','Confirmed'),('in progress','In Progress'),('done','Done'),('cancelled','Cancelled')],
        string='Status',default='draft'
    )
    material_line_ids = fields.One2many('mrp.production.material.line','production_id')
    is_material_available = fields.Boolean(default=False)
    material_count = fields.Integer(compute='_compute_materials_count')

    def create(self, vals):
        if vals.get('mrp_name', _('New')) == _('New'):
            vals['mrp_name'] = self.env['ir.sequence'].next_by_code('mrp.production.ext') or _('New')
        return super().create(vals)

    def button_confirmed(self):

        if self.bom_id  and self.quantity > 0:
            self.state = 'confirmed'


    # @api.onchange('bom_id')
    # def onchange_bom_error(self):
    #     if not self.bom_id:
    #         raise ValidationError('BOM does not exists')
    def _compute_materials_count(self):
        f = self.env['mrp.production.material.line'].search_count([
            ('production_id','=',self.id)
        ])
        self.material_count = f
    def material_view(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'materials',
            'res_model': 'mrp.production.material.line',
            'view_mode': 'list,form',
            'domain': [('production_id', '=', self.id)]

        }

    def start_production(self):
        if self.material_line_ids:
            self.state = 'in progress'


    def button_consumed_qty(self):
        self.material_line_ids.consumed_qty = 1
