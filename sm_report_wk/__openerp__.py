# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Nicolas Bessi, Vincent Renaville, Guewen Baconnier
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

{'name': 'Multiples Reportes usando Webkit Library',
 'version': '1.0.0',
 'category': 'Reports/Webkit',
 'description': """
Multiples Reportes con webkit
#################

* Agrega reportes de Pedidos de Venta

Depends on base_header_webkit community addon available here:
`https://launchpad.net/webkit-utils <https://launchpad.net/webkit-utils>`_
    """,
 'author': 'Camptocamp - Modified Tequila 1921',
 'website': 'http://www.tequila1921.com',
 'depends': ['base', 'sale_order_webkit', 'sm_base_headers_webkit'],
 'update_xml': ['reports.xml',
 ],
 'demo_xml': [],
 'test': [],
 'installable': True,
 'active': False,
 }
