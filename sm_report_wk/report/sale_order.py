# -*- encoding: utf-8 -*-
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
import time

from openerp.report import report_sxw
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

def conv_ascii(text):
    """
    @param text : text that need convert vowels accented & characters to ASCII
    Converts accented vowels, ñ and ç to their ASCII equivalent characters
    """
    old_chars = [
        'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù', 'ä', 'ë', 'ï', 'ö',
        'ü', 'â', 'ê', 'î', 'ô', 'û', 'Á', 'É', 'Í', 'Ó', 'Ú', 'À', 'È', 'Ì',
        'Ò', 'Ù', 'Ä', 'Ë', 'Ï', 'Ö', 'Ü', 'Â', 'Ê', 'Î', 'Ô', 'Û', 'ñ', 'Ñ',
        'ç', 'Ç', 'ª', 'º', '°', ' ', 'Ã', 'Ø'
    ]
    new_chars = [
        'a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o',
        'u', 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', 'A', 'E', 'I',
        'O', 'U', 'A', 'E', 'I', 'O', 'U', 'A', 'E', 'I', 'O', 'U', 'n', 'N',
        'c', 'C', 'a', 'o', 'o', ' ', 'A', '0'
    ]
    for old, new in zip(old_chars, new_chars):
        try:
            text = text.replace(unicode(old, 'UTF-8'), new)
        except:
            try:
                text = text.replace(old, new)
            except:
                raise osv.except_osv(_('Warning !'), _(
                    "Can't recode the string [%s] in the letter [%s]") % (text, old))
    return text
    

class SaleOrderReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(SaleOrderReport, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time,
                                  'company_vat': self._get_company_vat,
								  'get_data_partner': self._get_data_partner
								  })

    def _get_company_vat(self):
        res_users_obj = pooler.get_pool(self.cr.dbname).get('res.users')
        company_vat = res_users_obj.browse(self.cr, self.uid, self.uid).company_id.partner_id.vat
        return company_vat

	
    def _get_data_partner(self, partner_id):
        #address_invoice = ''
        partner_obj = self.pool.get('res.partner')
        res = {}
        partner = partner_obj.browse(self.cr, self.uid, partner_id)
        #id_parent = partner_id.commercial_partner_id.id
        #address_parent = partner_obj.browse(self.cr, self.uid, id_parent)
        
        res.update({
            'name' : partner.name or False,
            'parent_name' : partner.parent_id.name or False,
            'vat' : partner._columns.has_key('vat_split') \
                and partner.vat_split or partner.vat or False,
            'street' : partner.street or False,
            'l10n_mx_street3' : partner.l10n_mx_street3 or False,
            'l10n_mx_street4' : partner.l10n_mx_street4 or False,
            'street2' : partner.street2 or False,
            'city' : partner.city_id and \
                partner.city_id.name or False,
            'state' : partner.state_id and \
                partner.state_id.name or False,
            'country' : partner.country_id and\
                partner.country_id.name or False,
            'l10n_mx_city2' : partner.l10n_mx_city2 and partner.l10n_mx_city2 or False,
            'zip' : partner.zip or False,
            'phone' : partner.phone or False,
            'fax' : partner.fax or False,
            'mobile' : partner.mobile or False,
        })
        
        return res
		
report_sxw.report_sxw('report.smreport.sale.order.wk',
                      'sale.order',
                      'addons/sm_report/report/sale_order.mako',
                      parser=SaleOrderReport)
