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

{
    "name" : "Complemento Detallista para Factura Electronica para Mexico (CFDi)",
    "version" : "1.0",
    "author" : "chava-mm@hotmail.com",
    "category" : "Localization/Mexico",
    "description" : """This module add Complemento Detallista AMC8.1 to files from invoices with standard CFD-2010 of Mexican SAT.
    """,
    "website" : "http://chavamm.wordpress.com/",
    "license" : "AGPL-3",
    "depends" : ["l10n_mx_facturae_addenda", "l10n_mx_invoice_discount", "l10n_mx_facturae_complemento",
        ],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
        'security/l10n_mx_facturae_detallista.xml',
        'invoice_view.xml',
    ],
    "installable" : True,
    "active" : False,
}
