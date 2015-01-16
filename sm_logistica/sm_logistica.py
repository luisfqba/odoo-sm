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

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'teq_comercial_name': fields.char('Nombre Comercial', size=128),
        'teq_shipping_info': fields.text('Información de Entrega'),
    }

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

    def _get_invoice_num(self, cr, uid, ids, field, args, context=None):
        result = {}
        res = ''    
        number = ''   
        #raise osv.except_osv('Error :', 'datos [%s]' % (ids))

        for last in self.browse(cr, uid, ids, context=context):
            #raise osv.except_osv('Error :', 'datos [%s]' % (last.invoice_ids))
            res = ''
            sep = ','
            for i in last.invoice_ids:
                if str(res) != '' :
                    res = res + sep + str(i.number)
                else:
                    res = str(i.number)

            result[last.id] = res
        return result


    _columns = {
        'teq_comercial_name': fields.related('partner_id', 'teq_comercial_name', type='char', store=True, string='Nombre Comercial'),
        'teq_shipping_info': fields.related('partner_id', 'teq_shipping_info', type='text', string='Información de Entrega'),
        'teq_state': fields.selection(_get_state_selection, 'Estado', required=True, help='Indica el estado del proceso del Pedido.'),
        'shipping_state_id': fields.related('partner_shipping_id', 'state_id', type='many2one', relation="res.country.state", string="Entidad Federativa"),
        'shipping_city': fields.related('partner_shipping_id', 'city', type='char', string="Ciudad"),
        #'teq_invoice_ref': fields.char('Factura', size=32),
        'teq_invoice_num': fields.function(_get_invoice_num, method=True, type='char', size=64, string='Factura', store=False, help='Muestra el numero de factura del pedido'),
    }

    _defaults = {
            'teq_state': 'created',
    }

class stock_picking(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    _columns = {
        'teq_shipping_info': fields.related('sale_id', 'teq_shipping_info', type='text', string='Información de Entrega'),
        'teq_state': fields.related('sale_id', 'teq_state', type='selection', required=True),
        'teq_invoice_num': fields.related('sale_id', 'teq_invoice_num', type='char', string='Factura', readonly=True),
    }

class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'
    _columns = {
        'picking_note': fields.related('picking_id', 'note', type='text', string='Notas'),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
