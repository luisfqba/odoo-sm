# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
############################################################################
#    Coded by: moylop260 (moylop260@vauxoo.com)
#    Coded by: isaac (isaac@vauxoo.com)
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

from osv import osv
from osv import fields
import tools
import time
import xml.dom.minidom
import os
import base64
import hashlib
import tempfile
import os
import netsvc
from tools.translate import _
import codecs
import release
from datetime import datetime

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    def _get_method_type_selection(self, cr, uid, context=None):
        types = super(res_partner, self)._get_method_type_selection(cr, uid, context=context)
        types.extend([
            ('complemento_detallista','Complemento Detallista'),
        ])
        
        return types

    _columns = {
        'addenda_type': fields.selection(_get_method_type_selection, "Tipo de Addenda", type='char', size=64),
        'num_proveedor': fields.char('Numero de Proveedor', size = 24, help = 'Es el número de proveedor que el partner asigno a la compañia'),
    }
    
res_partner()

