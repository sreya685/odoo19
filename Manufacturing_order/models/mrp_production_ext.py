from email.policy import default

from odoo import api,fields,models,_,Command
from odoo.exceptions import ValidationError
from odoo.http import request


class MrpProductionExt(models.Model):
    _name = 'mrp.production.ext'
    _description = 'Mrp Production Ext'
    _rec_name = 'mrp_name'

    mrp_name = fields.Char(string='Production Name',default=lambda self: _('New'))
    product_id = fields.Many2one('product.product', domain=[('is_manufacturable','=',True)])
    bom_id = fields.Many2one('mrp.bom')
    quantity = fields.Integer(string='Quantity')
    planned_date = fields.Date(string='Planned Date')
    state=fields.Selection(
        selection=[('draft','Draft'),('confirmed','Confirmed'),('in progress','In Progress'),('done','Done'),('cancelled','Cancelled')],
        string='Status',default='draft'
    )
    material_line_ids = fields.One2many('mrp.production.material.line','production_id')
    is_material_available = fields.Boolean(compute='compute_m_a',default=False,store=True)
    material_count = fields.Integer(compute='_compute_materials_count')
    total_consumed = fields.Integer(compute='_compute_total_consumed')
    remaining_material = fields.Integer(compute='_compute_remaining_material',default=0)
    produced_qty = fields.Integer(compute='_compute_prd_qty',default=0,store=True)
    remaining_qty = fields.Integer(compute='_compute_rem_qty',default=0,store=True)
    backorder_id = fields.Many2one('mrp.production.ext')
    # backorder_rem_qty = fields.Integer(compute='_compute_backorder_rem_',store=True,default=0)
    # backorder_avail_qty = fields.Integer(compute='_compute_backorder_avail_qty',store=True,default=0)


    def create(self, vals):
        if vals.get('mrp_name', _('New')) == _('New'):
            vals['mrp_name'] = self.env['ir.sequence'].next_by_code('mrp.production.ext') or _('New')
            # n=vals.get('product_id')
            # # for record in self:
            #     # if record.state == 'done':
            # x =   self.env['product.product'].write({
            #                 'name': n,
            #                 'type': 'consu',
            #                 'qty_available': 2,

#                         })
#             vals['product_id'] = x.id


        return    super().create(vals)

    def button_confirmed(self):

        if self.bom_id and self.quantity > 0:
            # if self.is_material_available == True:
                self.state = 'confirmed'
        for record in self:
            if record.material_line_ids:
                for line in record.material_line_ids:
                   if line.product_id.qty_available == 0 :

                         raise ValidationError('please update stock qty')


    @api.onchange('product_id','bom_id','quantity')
    def onchange_bom(self):
        for record in self:
            if record.material_line_ids:
                record.material_line_ids = [Command.clear()]

            lines =[]

            for line in record.bom_id.bom_line_ids:
                lines.append(Command.create({
                    'product_id': line.product_id.id,
                    'bom_line_qty': line.product_qty
                }))
        self.material_line_ids = lines


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
        for record in self:
            consume=[]
            if record.material_line_ids:

                    for line in record.material_line_ids:
                        if line.required_qty < line.available_qty:
                            if line.consumed_qty < line.required_qty:
                                line.consumed_qty = line.required_qty



                        else:
                            consume.append(int(line.available_qty / line.bom_line_qty))
                            mini = min(consume)
                            print(mini)
                            line.consumed_qty = line.bom_line_qty * mini


    @api.constrains('bom_id')
    def check_bom(self):
        if not self.bom_id:
            raise ValidationError('bom is required')

    @api.onchange('material_line_ids.consumed_qty','material_line_ids.required_qty')
    def prevention_consumed_qty(self):
        for record in self:
            if record.material_line_ids:
                for line in record.material_line_ids:
                    if line.consumed_qty > line.required_qty:
                        raise ValidationError('consumed qty cannot be greater than required qty')

    def button_done(self):
        for record in self:
            if record.material_line_ids:
                for line in record.material_line_ids:
                    if line.required_qty >= line.consumed_qty:
                          record.state = 'done'


            if record.state == 'done':

                  k =   self.env['product.product'].search([
                      ('name','=', record.product_id.name)

                    ])
                  k.qty_available += record.quantity


    @api.depends('material_line_ids.consumed_qty')
    def _compute_total_consumed(self):
        for record in self:
            t=0
            if record.material_line_ids:
               for line in record.material_line_ids:
                   t += line.consumed_qty
            record.total_consumed = t

    @api.depends('total_consumed','material_line_ids.required_qty')
    def _compute_remaining_material(self):
        for record in self:
            t_remaining = 0
            if record.material_line_ids:
                for line in record.material_line_ids:
                    t_remaining += line.required_qty
            record.remaining_material = t_remaining - record.total_consumed


    @api.onchange('product_id')
    def onchange_product(self):
        for record in self:
            if record.product_id:
               if not record.product_id.is_manufacturable:
                  raise ValidationError('product must be manufacturable')

    @api.depends('material_line_ids','material_line_ids.available_qty','material_line_ids.required_qty')
    def compute_m_a(self):
        for record in self:
            p=[]
            if record.material_line_ids and record.quantity:
               for line in record.material_line_ids:
                     if line.available_qty >= line.required_qty:
                       p.append(1)
                     else:
                       p.append(0)
            s=0
            for i in range(len(p)):

                s +=p[i]
                if s == len(p):
                    record.is_material_available = True


    @api.depends('state','product_id')
    def _compute_prd_qty(self):
        for record in self:
          if record.state == 'done':
            record.produced_qty = record.product_id.qty_available

    def partial_production(self):
        for record in self:
            e=[]
            t=0
            for line in record.material_line_ids:
                if line.required_qty > line.available_qty:
                     t = int(line.available_qty / line.bom_line_qty)
                     e.append(t)
            print('IOIOIIUGUGUY',e)


            if e:

                minimum = min(e)
                record.quantity = minimum
                record.state = 'in progress'
                lines=[]
                for line in record.material_line_ids:
                    lines.append(Command.create({
                    'product_id': line.product_id.id,
                    'available_qty':line.available_qty,
                    'required_qty' :line.required_qty

                }))
                n = self.env['mrp.production.ext'].create({
                    'product_id': record.product_id.id,
                    'bom_id': record.bom_id.id,
                    'quantity': record.remaining_qty,
                     'material_line_ids': lines

                })
                record.backorder_id = n.id


                # for l in range(len(e)):
                #     for line in record.material_line_ids:
                #      if e[l] == line.bom_line_qty :
                #          line.consumed_qty = line.available_qty
                #          record.state ='in progress'

    @api.depends('material_line_ids.required_qty','material_line_ids.available_qty')
    def _compute_rem_qty(self):
        for record in self:
            if record.material_line_ids:
                for line in record.material_line_ids:
                    if line.required_qty > line.available_qty:
                         record.remaining_qty = line.required_qty - line.available_qty
    def backorder(self):
                    return {
                        'type': 'ir.actions.act_window',
                        'name': 'backorder',
                        'res_model': 'mrp.production.ext',
                        'res_id': self.backorder_id.id,
                        'view_mode': 'form',
                        'domain': [('production_id', '=', self.id)]

                    }
    # @api.depends('quantity')
    # def _compute_backorder_rem_(self):
    #          if
                     #   req  >     avai  >=   bom
                     #   12     8     8        4        1
                     #    3     2     2         1        1
