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

##############################################################################
#	Transportistas
#
##############################################################################

class sm_delivery_simple_carrier(osv.osv):
    _name = 'sm.delivery.simple.carrier'
    _columns = {
        'name': fields.char('Nombre', size=128),
        'partner_id': fields.many2one('res.partner', 'Empresa'),
        'active': fields.boolean('Active'),
    }
    _defaults = {
        'active': True
    }
sm_delivery_simple_carrier()

##############################################################################
#	Conceptos de Costos Extra
#
##############################################################################

class sm_delivery_costs_concept(osv.osv):
    _name = 'sm.delivery.costs.concept'
    _columns = {
        'name': fields.char('Nombre', size=128, required=True),
        'description': fields.text('Descripción'),
        'active': fields.boolean('Active'),
    }
    _defaults = {
        'active': True
    }

sm_delivery_costs_concept()

##############################################################################
#	Lineas de costo de pedido
#
##############################################################################

class sm_delivery_costs_sale_line(osv.osv):
    _name = 'sm.delivery.costs.sale.line'
    _rec_name = 'concept_id'
    _columns = {
        'concept_id': fields.many2one('sm.delivery.costs.concept', 'Concepto', required=True),
        #'name': fields.char('Ref', size=128),
        'amount': fields.float('Monto', digist=(12,6), required=True),
        'note': fields.text('Observaciones'),
        'order_id': fields.many2one('sale.order', 'Sale order'),
    }
sm_delivery_costs_sale_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
