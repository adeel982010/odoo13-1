# -*- coding: utf-8 -*-


from odoo import api, fields, models, tools,_
from datetime import datetime, timedelta


class GateEntryIn(models.Model):
    _name = "gate.in"
    _description = 'Gate In Entry'
    
    user_id = fields.Many2one("res.users","Security Name",default=lambda self: self.env.user)
    name = fields.Char("Sequence Number", required=True, copy=False, index=True,default =lambda self: _('New'))
    date = fields.Datetime("Entry Date")
    supplier_id = fields.Many2one("res.partner", "Supplier Name")
    supplier_phone = fields.Char("Supplier Contact Number", related='supplier_id.phone')
    supplier_email = fields.Char("Supplier Email", related='supplier_id.email')
    stock_picking_id = fields.Many2one("stock.picking","Challan No")
    stock_picking_date = fields.Datetime("Challan Date")
    #stock_move_id = fields.
    stock_picking_line_ids = fields.One2many(
        "stock.move.inherit", "gate_in_id", "Item Description")
    origin = fields.Char("Source Doc")
    vehicle_no = fields.Char(string='Vehicle Number')
    vehicle_driver_name = fields.Char(string='Driver Name')
    driver_contact_number = fields.Char(string='Driver Contact No')
    #corresponding_company = fields.Char(string='Company')
    
    location_type_id = fields.Many2one('stock.picking.type',"Operational type-Warehouse")
    dest_location_id = fields.Many2one(
        'stock.location', "Destination Location")
    notes = fields.Text('Notes')
    
    ## Auto sequence
    
    @api.model
    def create (self,vals):
        if vals:
            vals['name'] = self.env['ir.sequence'].next_by_code('gate.in') or _('New')
        return super(GateEntryIn,self).create(vals)
        
    ##Onchange for stock.picking date in gate in form based on stock picking scheduled date
    
    @api.onchange('stock_picking_id')
    def on_change_select(self):
        values = {
            'stock_picking_date': self.stock_picking_id.scheduled_date or False, 
            'supplier_id': self.stock_picking_id.partner_id and self.stock_picking_id.partner_id.id or False, 
            'origin': self.stock_picking_id.origin or False,
            'location_type_id':self.stock_picking_id.picking_type_id and self.stock_picking_id.picking_type_id.id or False,
            'dest_location_id': self.stock_picking_id.location_dest_id and self.stock_picking_id.location_dest_id.id or False,
        }
        self.update(values)
        
    ##Get lines items from stock.picking to gate in form
    @api.onchange('stock_picking_id')
    def on_change_picking(self):
        res = self.env['stock.picking']
        val = res.move_ids_without_package.search([('picking_id', '=' , self.stock_picking_id.name)])
        print(val.picking_id.name)
        r = [(5, 0, 0)]
        value = {}
        
        if self.stock_picking_id:
            for line in val:
                data = { 'product_id':line.product_id.id,
                         'product_qty':line.product_uom_qty,
                         'product_done_qty':line.quantity_done,
                         'product_uom':line.product_uom.name,
                       }
                print(data)
                r.append((0,0,data))
            value.update(stock_picking_line_ids = r)
            return {'value': value} 
    
    
class StockPickingInherit(models.Model):
    _name = 'stock.move.inherit'
    
    gate_in_id = fields.Many2one("gate.in", "Gate In Entries")
    product_id = fields.Many2one(
        'product.product', 'Product', index=True, required=True) 
    product_qty = fields.Float(
        'Quantity',default=0.0, required=True)
    product_done_qty = fields.Float(
        'Done Quantity',default=0.0, required=True)
    product_uom = fields.Char(
        'UoM')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
