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
from l10n_mx_facturae.invoice import conv_ascii

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _get_facturae_invoice_xml_data(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ids = isinstance(ids, (int, long)) and [ids] or ids
        ir_seq_app_obj = self.pool.get('ir.sequence.approval')
        invoice = self.browse(cr, uid, ids[0], context=context)
        sequence_app_id = ir_seq_app_obj.search(cr, uid, [(
            'sequence_id', '=', invoice.invoice_sequence_id.id)], context=context)
        type_inv = 'cfd22'
        if sequence_app_id:
            type_inv = ir_seq_app_obj.browse(
                cr, uid, sequence_app_id[0], context=context).type
        if 'cfdi' in type_inv:
            comprobante = 'cfdi:Comprobante'
            emisor = 'cfdi:Emisor'
            receptor = 'cfdi:Receptor'
            concepto = 'cfdi:Conceptos'
            facturae_version = '3.2'
        else:
            comprobante = 'Comprobante'
            emisor = 'Emisor'
            regimenFiscal = 'RegimenFiscal'
            receptor = 'Receptor'
            concepto = 'Conceptos'
            facturae_version = '2.2'
        data_dict = self._get_facturae_invoice_dict_data(
            cr, uid, ids, context=context)[0]
        doc_xml = self.dict2xml({comprobante: data_dict.get(comprobante)})

        #######################################
        # Crear el Complemento aqui
        #######################################
        doc_xml = self.add_complemento_xml(cr, ids, doc_xml, comprobante, invoice, context=context)

        invoice_number = "sn"
        (fileno_xml, fname_xml) = tempfile.mkstemp(
            '.xml', 'openerp_' + (invoice_number or '') + '__facturae__')
        fname_txt = fname_xml + '.txt'
        f = open(fname_xml, 'w')
        doc_xml.writexml(f, indent='    ', addindent='    ', newl='\r\n', encoding='UTF-8')
        f.close()
        os.close(fileno_xml)
        (fileno_sign, fname_sign) = tempfile.mkstemp('.txt', 'openerp_' + (
            invoice_number or '') + '__facturae_txt_md5__')
        os.close(fileno_sign)
        context.update({
            'fname_xml': fname_xml,
            'fname_txt': fname_txt,
            'fname_sign': fname_sign,
        })
        context.update(self._get_file_globals(cr, uid, ids, context=context))
        fname_txt, txt_str = self._xml2cad_orig(
            cr=False, uid=False, ids=False, context=context)
        data_dict['cadena_original'] = txt_str
        msg2=''

        if not txt_str:
            raise osv.except_osv(_('Error in Original String!'), _(
                "Can't get the string original of the voucher.\nCkeck your configuration.\n%s" % (msg2)))

        if not data_dict[comprobante].get('folio', ''):
            raise osv.except_osv(_('Error in Folio!'), _(
                "Can't get the folio of the voucher.\nBefore generating the XML, click on the button, generate invoice.\nCkeck your configuration.\n%s" % (msg2)))

        context.update({'fecha': data_dict[comprobante]['fecha']})
        sign_str = self._get_sello(
            cr=False, uid=False, ids=False, context=context)
        if not sign_str:
            raise osv.except_osv(_('Error in Stamp !'), _(
                "Can't generate the stamp of the voucher.\nCkeck your configuration.\ns%s") % (msg2))

        nodeComprobante = doc_xml.getElementsByTagName(comprobante)[0]
        nodeComprobante.setAttribute("sello", sign_str)
        data_dict[comprobante]['sello'] = sign_str

        noCertificado = self._get_noCertificado(cr, uid, ids, context['fname_cer'])
        if not noCertificado:
            raise osv.except_osv(_('Error in No. Certificate !'), _(
                "Can't get the Certificate Number of the voucher.\nCkeck your configuration.\n%s") % (msg2))
        nodeComprobante.setAttribute("noCertificado", noCertificado)
        data_dict[comprobante]['noCertificado'] = noCertificado

        cert_str = self._get_certificate_str(context['fname_cer'])
        if not cert_str:
            raise osv.except_osv(_('Error in Certificate!'), _(
                "Can't get the Certificate Number of the voucher.\nCkeck your configuration.\n%s") % (msg2))
        cert_str = cert_str.replace(' ', '').replace('\n', '')
        nodeComprobante.setAttribute("certificado", cert_str)
        data_dict[comprobante]['certificado'] = cert_str
        if 'cfdi' in type_inv:
            nodeComprobante.removeAttribute('anoAprobacion')
            nodeComprobante.removeAttribute('noAprobacion')
        x = doc_xml.documentElement
        nodeReceptor = doc_xml.getElementsByTagName(receptor)[0]
        nodeConcepto = doc_xml.getElementsByTagName(concepto)[0]
        x.insertBefore(nodeReceptor, nodeConcepto)

        self.write_cfd_data(cr, uid, ids, data_dict, context=context)

        if context.get('type_data') == 'dict':
            return data_dict
        if context.get('type_data') == 'xml_obj':
            return doc_xml
        data_xml = doc_xml.toxml('UTF-8')
        data_xml = codecs.BOM_UTF8 + data_xml
        fname_xml = (data_dict[comprobante][emisor]['rfc'] or '') + '_' + (
            data_dict[comprobante].get('serie', '') or '') + '_' + (
            data_dict[comprobante].get('folio', '') or '') + '.xml'
        data_xml = data_xml.replace(
            '<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0" encoding="UTF-8"?>\n')
        date_invoice = data_dict.get('Comprobante',{}) and datetime.strptime( data_dict.get('Comprobante',{}).get('fecha',{}), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d') or False
        if date_invoice  and date_invoice < '2012-07-01':
            facturae_version = '2.0'
        self.validate_scheme_facturae_xml(cr, uid, ids, [data_xml], facturae_version)
        data_dict.get('Comprobante',{})
        
        return fname_xml, data_xml
        
    def add_complemento_xml(self, cr, ids, doc_xml=None, comprobante=None, invoice=None, context=None):
        """
         @params xml_doc : File XML
         @params comprobante : Name to the Node that contain the information the XML
        """
        
        if context is None:
            context = {}
	
        if doc_xml:	    
            tipo = invoice.partner_id.addenda_type
            
            tipos = []
            
            if tipo:
                tipos = tipo.split('_')
            
            complemento = 'complemento'
        
            if complemento in tipos:
                node_Complemento = doc_xml.getElementsByTagName('cfdi:Complemento')

                if len(node_Complemento) == 0:
                    configure_ns_func = tipo + '_configure'
                    
                    xml_ns, ns, xsd = getattr(self, str(configure_ns_func))()
                    
                    nodeComprobante = doc_xml.getElementsByTagName(comprobante)[0]

                    xsi_schemans    = "http://www.w3.org/2001/XMLSchema-instance"
                    ns_xmlns        = "http://www.w3.org/2000/xmlns/"
                    ns_xsd_sat      = nodeComprobante.getAttribute('xsi:schemaLocation')
                    
                    #Llamada dinamica de generacion del tipo de complemento
#                    cpl_attrs, cpl_attrs_types, cpl_attrs_order = getattr(self, tipo)(doc_xml, node_Complemento, invoice, comprobante)
                    cpl_Structure = getattr(self, tipo)(invoice, comprobante)
                    
                    node_Complemento = self.det_add_node(
                        'cfdi:Complemento', cpl_Structure['attribs'], nodeComprobante, doc_xml, attrs_types=cpl_Structure['attribs_types'])                    
        
                    nodeComprobante.setAttributeNS(xsi_schemans, 'xsi:schemaLocation', ns_xsd_sat + ns + ' ' + xsd)
                    nodeComprobante.setAttributeNS(ns_xmlns, xml_ns, ns)
        
        return doc_xml
        
    def det_add_node(self, node_name=None, attrs=None, parent_node=None,
                 minidom_xml_obj=None, attrs_types=None, order=False):
        """
        @params node_name : Name node to added
        @params attrs : Attributes to add in node
        @params parent_node : Node parent where was add new node children
        @params minidom_xml_obj : File XML where add nodes
        @params attrs_types : Type of attributes added in the node
        @params order : If need add the params in order in the XML, add a
                list with order to params
        """
        
        if not order:
            order = attrs
                
        if node_name is None:
            new_node = parent_node
            
        else:
            new_node = minidom_xml_obj.createElement(node_name)
            
        for key in order:
            if attrs_types[key] == 'attribute':
                new_node.setAttribute(key, conv_ascii(attrs[key]))

            elif attrs_types[key] == 'textNode':
                key_node = minidom_xml_obj.createElement(key)
                text_node = minidom_xml_obj.createTextNode(conv_ascii(attrs[key]))

                key_node.appendChild(text_node)
                new_node.appendChild(key_node)

            elif attrs_types[key] == 'textNodeAttrib':
                ## Crear el nodo key_node con sus attribs correspondientes
                key_node_attrs = attrs[key]['attribs']
                key_node_attrs_types = attrs[key]['attribs_types']
                key_node_order = False

                if attrs[key].has_key('attribs_order'):
                    key_node_order = attrs[key]['attribs_order']

                key_node = self.det_add_node(
                    key, key_node_attrs, new_node, minidom_xml_obj, key_node_attrs_types, key_node_order)

                ## Se crea el nodo de texto
                if attrs[key].has_key('text') and attrs[key]['text']:
                    text_node = minidom_xml_obj.createTextNode(conv_ascii(attrs[key]['text']))
                    key_node.appendChild(text_node)
                    
                new_node.appendChild(key_node)
                
            elif attrs_types[key] == 'textNodeMulti':
                for item in attrs[key]['items']:
                    item_node_name = item['nodeName']
                    item_node_attrs = item['attribs']
                    item_node_attrs_types = item['attribs_types']
                    item_node_order = {}
                    
                    if item.has_key('attribs_order'):
                        item_node_order = item['attribs_order']
                    
                    item_node = self.det_add_node(
                        item_node_name, item_node_attrs, new_node, minidom_xml_obj, item_node_attrs_types, item_node_order)
                new_node.appendChild(item_node)
                            
            if node_name is not None:
                parent_node.appendChild(new_node)
        
        return new_node
        
account_invoice()

