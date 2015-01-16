# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2014 chavamm - http://chavamm.wordpress.com/
#    All Rights Reserved.
#    info chavamm (chava-mm@hotmail.com)
############################################################################
#    Coded by: chavamm (chava-mm@hotmail.com)
#    
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
import time

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def complemento_detallista_liverpool_configure(self):
        return self.complemento_detallista_configure()
        
    def complemento_detallista_liverpool(self, invoice=None, comprobante=None):
        
        nodes_to_build = [
            'contentVersion',
            'documentStatus',
            'documentStructureVersion',
            'type',
            'detallista:requestForPaymentIdentification',      ## 1.1
            'detallista:specialInstruction',                   ## 1.2
            'detallista:orderIdentification',                  ## 1.3
            'detallista:AdditionalInformation',                ## 1.4
            'detallista:DeliveryNote',                         ## 1.5
            'detallista:buyer',                                ## 1.6
            'detallista:seller',                               ## 1.7
            'detallista:allowanceCharge',                      ## 1.14
            'detallista:lineItem',                             ## 1.15
            'detallista:totalAmount',                          ## 1.16
            'detallista:TotalAllowanceCharge',                 ## 1.17
        ]
        
        det_data = self.det_format_data_dict(invoice)
        
        return self.build_document_structure(det_data, nodes=nodes_to_build)
        
account_invoice()
