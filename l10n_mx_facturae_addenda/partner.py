# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
############################################################################
#    Coded by: moylop260 (moylop260@vauxoo.com)
#    Coded by: Isaac Lopez (isaac@vauxoo.com)
############################################################################
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

import time
from tools.translate import _
from osv import fields, osv 
import pooler


class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    def _get_method_type_selection(self, cr, uid, context=None):
        #From module of l10n_mx_facturae_addsor inherit this function and add new methods
        types = []
        return types
    
    _columns = {
        'addenda_type': fields.selection(_get_method_type_selection, "Tipo de Addenda", type='char', size=64),
        'num_proveedor': fields.char('Numero de Proveedor', size = 24, help = 'Es el número de proveedor que el partner asigno a la compañia'),
    }
    
res_partner()
