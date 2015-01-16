# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2010 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
############################################################################
#    Coded by: Luis Torres (luis_t@vauxoo.com)
#    Launchpad Project Manager for Publication: Nhomar Hernandez - nhomar@vauxoo.com
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
    "name" : "Personalizacion de Reporte de Factura Electronica",
    "version" : "1.0",
    "author" : "Salvador Martinez",
    "category" : "Localization/Mexico",
    "description" : """Modulo basado en el modulo oficial de localizacion mexicana l10n_mx_facturae_report
    Agrega informacion del pedido de venta que genero la Factura. Incoterm y Nombre de Contacto como Sucursal.
    Este modulo depende del invoice_so que se encuentra en el repositorio de lp:addons-vauxoo/7.0
    """,
    "website" : "http://www.tequila1921.com/",
    "license" : "AGPL-3",
    "depends" : ["account", "report_webkit", "l10n_mx_regimen_fiscal", "invoice_so",
        "l10n_mx_notes_invoice"],
    "demo" : [],
    "data" : [
        "data.xml",
        "l10n_mx_facturae_report_webkit.xml",
    ],
    "installable" : True,
    "active" : False,
}
