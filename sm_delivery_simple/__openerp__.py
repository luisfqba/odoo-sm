# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    "name" : "Delivery Simple",
    "version" : "1.1",
    "author" : "Tequila 1921",
    "category" : "Generic Modules/",
    "description" : """Este modulo agrega la opcion de poder seleccionar un Transportista el cual realizara la entrega de la mercancia.
                        Agrega la opcion de poder asignar costos extra por diferentes motivos al pedido. Pueden ser costos por transporte, maniobras, etc.
        """,
    "depends" : ["sale", "l10n_mx_cities"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["delivery_view.xml"],
    "data" : ["security/sm_delivery_simple_security_groups.xml",
              "report/report_delivery_view.xml",
    ],
    "installable": True,
    "active": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
