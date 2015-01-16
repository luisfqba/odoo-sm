# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Alejandro Negrin anegrin@vauxoo.com,
#    Planified by: Alejandro Negrin, Humberto Arocha, Moises Lopez
#    Finance by: Vauxoo.
#    Audited by: Humberto Arocha (hbto@vauxoo.com) y Moises Lopez (moylop260@vauxoo.com)
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

{
    "name" : "Invoice Cancel Button Move - Accounting",
    "version" : "2.0",
    "author" : "Tequila 1921",
    "category" : "Custom",
    "description": """
Invoice Cancel Button Move
============================================
This module move Invoice Cancel Button to buttom of State Field

    """,
    "depends" : ["account", ],
    "demo_xml" : [],
    "update_xml" : ["account_invoice.xml",],
    "active": False,
    "installable": True,
    "certificate": False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

