# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from osv import fields,osv
import netsvc
import openerp.addons.decimal_precision as dp

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def _get_state_selection(self, cursor, user_id, context=None):
        return (
            ('created','Creado'),
            ('approved', 'Aprobado'),
            ('shipping', 'Enviado'),
            ('cancelled', 'Cancelado'),
            ('inreview', 'En Revision'),
            ('invoiced', 'Facturado'),
            ('paid', 'Pagado'),
            ('delivered', 'Entregado'),
            ('stopped', 'Detenido'))
            
    def _so_extra_cost(self, cr, uid, ids, field_names=None, arg=False, context=None):
        """ 
        @return: Dictionary of values
        """
        lines = self.pool.get('sm.delivery.costs.sale.line').search(cr, uid,[('order_id','in',ids)])
       
        res = {}
        
        for id in ids:
            res[id] = {}.fromkeys(field_names, 0)
        
        for f in field_names:
            c = context.copy()
           
            stock = self.get_product_available(cr, uid, ids, context=c)
            for id in ids:
                res[id][f] = stock.get(id, 0.0)
            
        cost = 0.0
        for line in lines:
            cost += line.amount
            res[line.order_id]['sm_cost'] = cost
        
        return res
        
    def _get_stock(self, cr, uid, ids, field_name, arg, context=None):
        """ Gets stock of products for locations
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        if 'location_id' not in context:
            locations = self.pool.get('stock.location').search(cr, uid, [('usage', '=', 'internal')], context=context)
        else:
            locations = context['location_id'] and [context['location_id']] or []

        if isinstance(ids, (int, long)):
            ids = [ids]

        res = {}.fromkeys(ids, 0.0)
        if locations:
            cr.execute('''select
                    prodlot_id,
                    sum(qty)
                from
                    stock_report_prodlots
                where
                    location_id IN %s and prodlot_id IN %s group by prodlot_id''',(tuple(locations),tuple(ids),))
            res.update(dict(cr.fetchall()))

        return res


    _columns = {
        'sm_carrier_id': fields.many2one('sm.delivery.simple.carrier', 'Transportista'),
        'carrier_ref': fields.char('Num. de Guia', size=32),
        're_carrier_name': fields.char('Reembarque', size=128),
        're_carrier_ref': fields.char('Guia Reembarque', size=32),
        'carrier_notes': fields.char('Observaciones Transportista', size=128),
        'carrier_delivery_date': fields.date('Fecha de Envio'),
        'carrier_shipped_date': fields.date('Fecha de Entrega Mercancia'),
        'check_guide': fields.boolean('Guia Revisada'),
        're_check_guide': fields.boolean('Guia reembarque Revisada'),
        'carrier_exclude_check': fields.boolean('Excluir', help='si marca esta casilla se puede usar en reportes y analisis para exlcuir estos pedidos del analisis.'),
        'costs_lines': fields.one2many('sm.delivery.costs.sale.line', 'order_id', 'Costos'),
        'sm_state': fields.selection(_get_state_selection, 'Estado', required=True, help='Indica el estado del Pedido.'),
        'sm_cost': fields.function(_so_extra_cost, multi='sm_cost',
            type='float',  digits_compute=dp.get_precision('Account'),
            string='Costos Extra',
            help="Suma total de costos extra."),
    }
    _defaults = {
        'sm_carrier_id': False,
        'sm_state': 'created', 
    }
sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
