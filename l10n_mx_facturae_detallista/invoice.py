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
    
    def complemento_detallista_configure(self):
        
        ns   = "http://www.sat.gob.mx/detallista"
        xsd  = "http://www.sat.gob.mx/sitio_internet/cfd/detallista/detallista.xsd"
        xml_ns = 'xmlns:detallista'
        
        return xml_ns, ns, xsd
        
    def complemento_detallista(self, invoice=None, comprobante=None):
        
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
            #'detallista:shipTo',                              ## 1.8  (0, 1)
            #'detallista:InvoiceCreator',                      ## 1.9  (0, 1)
            #'detallista:Customs',                             ## 1.10 (0, 999999)
            #'detallista:currency',                            ## 1.11 (0, 3)
            #'detallista:paymentTerms',                        ## 1.12 (0, 1)
            #'detallista:shipmentDetail',                      ## 1.13 (0, 1)
            'detallista:allowanceCharge',                      ## 1.14
            'detallista:lineItem',                             ## 1.15
            'detallista:totalAmount',                          ## 1.16
            'detallista:TotalAllowanceCharge',                 ## 1.17
        ]
        
        det_data = self.det_format_data_dict(invoice)
        
        return self.build_document_structure(det_data, nodes=nodes_to_build)
        
    def build_document_structure(self, det_data, nodes=[]):
        ############################
        # Inicializacion Detallista
        ############################

        """
        Document Structure for AMC 8.1 - Detail
        1.1 -> requestForPaymentIdentification (1, 1)
        1.2 -> specialInstruction (0, 4)
        1.3 -> orderIdentification (1, 1)
        1.4 -> AdditionalInformation (1, 1)
        1.5 -> DeliveryNote (0, 1)
        1.6 -> buyer (1, 1)
        1.7 -> seller (0, 1)
        1.8 -> shipTo (0, 1)
        1.9 -> InvoiceCreator (0, 1)
        1.10 -> Customs (0, 999999)
        1.11 -> currency (0, 3)
        1.12 -> paymentTerms (0, 1)
        1.13 -> shipmentDetail (0, 1)
        1.14 -> allowanceCharge (0, 99)
        1.15 -> lineItem (0, 9999999)
        1.16 -> totalAmount (0, 1)
        1.17 -> TotalAllowanceCharge (0, 999999)
        """	
	
        node_Detallista_attrs = {
            'contentVersion': '1.3.1',
            'documentStatus': 'ORIGINAL',
            'documentStructureVersion': 'AMC8.1',
            'type': 'SimpleInvoiceType',
    	    #### 1.1	
            'detallista:requestForPaymentIdentification': {
                'attribs': {
                    'detallista:entityType': det_data['requestForPaymentIdentification.node.entityType.value'],
                },
                'attribs_types': {
                    'detallista:entityType':'textNode',
                },
            },
            #### 1.2
            'detallista:specialInstruction': {
                'attribs': {
        	        'code':det_data['specialInstruction.attrib.code'],
                    'detallista:text':det_data['specialInstruction.node.text.value']
                },
                'attribs_types': {
                    'code':'attribute',
                    'detallista:text':'textNode'
                },
            },
            #### 1.3
            'detallista:orderIdentification':{
                'attribs': {
                    'detallista:referenceIdentification':{
                        'text': det_data['orderIdentification.node.referenceIdentification.value'],
                        'attribs':{
                            'type': det_data['orderIdentification.node.referenceIdentification.attrib.type'],
                        },
                        'attribs_types':{
                            'type':'attribute',
                        }
                    },
                    'detallista:ReferenceDate': det_data['orderIdentification.node.ReferenceDate.value']
                },
                'attribs_types': {
                    'detallista:referenceIdentification':'textNodeAttrib',
                    'detallista:ReferenceDate':'textNode'
                }
            },
            #### 1.4
            'detallista:AdditionalInformation': {
	            'attribs': {
	                'detallista:referenceIdentification': {
		                'text':det_data['AdditionalInformation.node.referenceIdentification.value'],
		                'attribs': {
		                    'type': det_data['AdditionalInformation.node.referenceIdentification.attrib.type'],
		                },
		                'attribs_types': {
		                    'type':'attribute'
		                }
	                }
	            },
	            'attribs_types': {
	                'detallista:referenceIdentification':'textNodeAttrib'
	            }
	        },
            #### 1.5
            'detallista:DeliveryNote': {
	            'attribs': {
	                'detallista:referenceIdentification': det_data['DeliveryNote.node.referenceIdentification.value'],
	                'detallista:ReferenceDate':det_data['DeliveryNote.node.ReferenceDate.value'],
        	    },
                'attribs_types': {
	                'detallista:referenceIdentification':'textNode',
	                'detallista:ReferenceDate':'textNode'
	            }
	        },
    	    #### 1.6
            'detallista:buyer': {
	            'attribs': {
	                'detallista:gln':det_data['buyer.node.gln.value'],
	                'detallista:contactInformation':{
		            'text':'',
		            'attribs':{
		                'detallista:personOrDepartmentName':{
			                'text':'',
			                'attribs':{
				                'detallista:text': det_data['buyer.node.contactInformation.node.personOrDepartmentName.node.text.value'],
				            },
			                'attribs_types':{
				                'detallista:text':'textNode',
				            },
			            },
		            },
		            'attribs_types':{
		                'detallista:personOrDepartmentName':'textNodeAttrib',
		            },
	                }
	            },
	            'attribs_types': {
	                'detallista:gln':'textNode',
	                'detallista:contactInformation':'textNodeAttrib',
	            }
	        },
            ### 1.7
            'detallista:seller': {
	            'attribs': {
	                'detallista:gln':det_data['seller.node.gln.value'],
	                'detallista:alternatePartyIdentification':{
		                'text':det_data['seller.node.alternatePartyIdentification.value'],
		                'attribs':{
			                'type':det_data['seller.node.alternatePartyIdentification.attrib.type'],
	                    },
		                'attribs_types':{
			                'type':'attribute'
	                    }
                    }
	            },
	            'attribs_types': {
	                'detallista:gln':'textNode',
	                'detallista:alternatePartyIdentification':'textNodeAttrib'
	            }
            },
            ###
            ### 1.8 -> shipTo (0, 1)
            ### 1.9 -> InvoiceCreator (0, 1)
            ### 1.10 -> Customs (0, 999999)
            ### 1.11 -> currency (0, 3)
            ### 1.12 -> paymentTerms (0, 1)
            ### 1.13 -> shipmentDetail (0, 1)
            ###
	        ### 1.14 -> allowanceCharge (0, 99)
	        'detallista:allowanceCharge': {
	            'attribs': {
	                'settlementType':det_data['allowanceCharge.attrib.settlementType'],
	                'allowanceChargeType':det_data['allowanceCharge.attrib.allowanceChargeType'],
	                'detallista:specialServicesType':det_data['allowanceCharge.node.specialServicesType.value'],
	                'detallista:monetaryAmountOrPercentage':{
		                'text':'',
		                'attribs':{
			                'detallista:rate':{
			                    'text':'',
			                    'attribs':{
				                    'base': det_data['allowanceCharge.node.monetaryAmountOrPercentage.node.rate.attrib.base'],
				                    'detallista:percentage':det_data['allowanceCharge.node.monetaryAmountOrPercentage.node.rate.node.percentage.value'],
				                },
			                    'attribs_types':{
				                    'base':'attribute',
				                    'detallista:percentage':'textNode'
				                }
			                }
	                    },
		                'attribs_types':{
			                'detallista:rate':'textNodeAttrib',    
	                    }
                    }
	            },
	            'attribs_types': {
	                'settlementType':'attribute',
	                'allowanceChargeType':'attribute',
	                'detallista:specialServicesType':'textNode',
	                'detallista:monetaryAmountOrPercentage':'textNodeAttrib'
	            }

            },
            
            ### 1.15 -> lineItem (0, 9999999)
            'detallista:lineItem':{
                'items': self._get_lines(det_data['lineItem']),
            },
            
	        ### 1.16 -> totalAmount (0, 1)
	        'detallista:totalAmount': {
	            'attribs': {
	                'detallista:Amount': det_data['totalAmount.node.Amount.value'],
	            },
	            'attribs_types': {
	                'detallista:Amount':'textNode',
                },        
            },
            ### 1.17 -> TotalAllowanceCharge (0, 999999)
            'detallista:TotalAllowanceCharge':{
	            'attribs': {
	                'allowanceOrChargeType': det_data['TotalAllowanceCharge.attrib.allowanceOrChargeType'],
	                'detallista:specialServicesType': det_data['TotalAllowanceCharge.node.specialServicesType.value'],
	                'detallista:Amount':det_data['TotalAllowanceCharge.node.Amount.value'],
	            },
                'attribs_types': {
	                'allowanceOrChargeType': 'attribute',
	                'detallista:specialServicesType':'textNode',
	                'detallista:Amount': 'textNode',
	            },
	            'attribs_order': [
	                'allowanceOrChargeType',
	                'detallista:specialServicesType',
	                'detallista:Amount',
	            ]
	        }
        }

        node_Detallista_attrs_types = {
            'contentVersion': 'attribute',
            'documentStatus': 'attribute',
            'documentStructureVersion': 'attribute',
            'type': 'attribute',
            'detallista:requestForPaymentIdentification':'textNodeAttrib',      ## 1.1
            'detallista:specialInstruction':'textNodeAttrib',                   ## 1.2
            'detallista:orderIdentification':'textNodeAttrib',                  ## 1.3
            'detallista:AdditionalInformation':'textNodeAttrib',                ## 1.4
            'detallista:DeliveryNote': 'textNodeAttrib',                        ## 1.5
            'detallista:buyer': 'textNodeAttrib',                               ## 1.6
            'detallista:seller': 'textNodeAttrib',                              ## 1.7
            'detallista:allowanceCharge':'textNodeAttrib',                      ## 1.8
            'detallista:lineItem': 'textNodeMulti',                             ## 1.15
            'detallista:totalAmount':'textNodeAttrib',                          ## 1.16
            'detallista:TotalAllowanceCharge':'textNodeAttrib',                 ## 1.17
        }   
        
        node_Detallista_order = [
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
            'detallista:allowanceCharge',                      ## 1.8
            'detallista:lineItem',                             ## 1.15
            'detallista:totalAmount',                          ## 1.16
            'detallista:TotalAllowanceCharge',                 ## 1.17
        ]
        
        ### Filter for Node Elements to Include
        if len(nodes):
            node_Detallista_order = nodes
               
        detallista_structure = {
            'attribs':{
                'detallista:detallista': {
                    'attribs':node_Detallista_attrs,
                    'attribs_types': node_Detallista_attrs_types,
                    'attribs_order': node_Detallista_order,
                },
            },
            'attribs_types':{
                'detallista:detallista':'textNodeAttrib',
            }
        }
        
        return detallista_structure
	
    def _get_lines(self, lines_data):
        item_consecutive_num = 1
	
        lineItems = []

        for line in lines_data:
            item_attribs = {
                'type':'SimpleInvoiceLineItemType',
                'number': str(item_consecutive_num),
                'detallista:tradeItemIdentification':{
                    'text':'',
                    'attribs':{
                        'detallista:gtin':line['Item']['tradeItemIdentification.node.gtin.value']
                    },
                    'attribs_types':{
                        'detallista:gtin':'textNode'
                    }
                },
                'detallista:alternateTradeItemIdentification': {
                    'text':line['Item']['alternateTradeItemIdentification.value'],
                    'attribs':{
                        'type':line['Item']['alternateTradeItemIdentification.attrib.type'],
                    },
                    'attribs_types':{
                        'type':'attribute',
                    },
                },
	            'detallista:tradeItemDescriptionInformation':{
	                'text':'',
	                'attribs':{
                        'language':line['Item']['tradeItemDescriptionInformation.attrib.language'],
                        'detallista:longText':line['Item']['tradeItemDescriptionInformation.node.longText.value'],
		            },
	                'attribs_types':{
                        'language':'attribute',
                        'detallista:longText':'textNode',
                    },
                },
	            'detallista:invoicedQuantity':{
                    'text':line['Item']['invoicedQuantity.value'],
                    'attribs':{
                        'unitOfMeasure':line['Item']['invoicedQuantity.attrib.unitOfMeasure'],
		            },
                    'attribs_types':{
                        'unitOfMeasure':'attribute',
		            },
                },
                'detallista:grossPrice':{
                    'text':'',
                    'attribs':{
                        'detallista:Amount':line['Item']['grossPrice.node.Amount.value'],
                    },
	                'attribs_types':{
                        'detallista:Amount':'textNode',
                    },
                },
	            'detallista:netPrice':{
                    'text':'',
                    'attribs':{
                        'detallista:Amount':line['Item']['netPrice.node.Amount.value'],
                    },
                    'attribs_types':{
                        'detallista:Amount':'textNode',
                    },
                },
                'detallista:totalLineAmount':{
                    'text':'',
                    'attribs':{
                        'detallista:grossAmount':{
                            'text':'',
                            'attribs':{
                                'detallista:Amount':line['Item']['totalLineAmount.node.grossAmount.node.Amount.value'],
                            },
                            'attribs_types':{
                                'detallista:Amount':'textNode',
                            },
                        },
                        'detallista:netAmount':{
                            'text':'',
                            'attribs':{
                                'detallista:Amount':line['Item']['totalLineAmount.node.netAmount.node.Amount.value'],
                            },
                            'attribs_types':{
                                'detallista:Amount':'textNode',
                            },
                        },
                    },
                    'attribs_types':{
                        'detallista:grossAmount':'textNodeAttrib',
                        'detallista:netAmount':'textNodeAttrib',
                    },
                    'attribs_order':[
                        'detallista:grossAmount',
                        'detallista:netAmount',
                    ],
                },
            }
            
            item_attribs_types = {
                'type':'attribute',
                'number':'attribute',
                'detallista:tradeItemIdentification':'textNodeAttrib',
                'detallista:alternateTradeItemIdentification':'textNodeAttrib',
                'detallista:tradeItemDescriptionInformation':'textNodeAttrib',
                'detallista:invoicedQuantity':'textNodeAttrib',
                'detallista:grossPrice':'textNodeAttrib',
                'detallista:netPrice':'textNodeAttrib',
                'detallista:totalLineAmount':'textNodeAttrib',
            }

            item_attribs_order = [
                    'type',
                    'number',
                    'detallista:tradeItemIdentification',
                    'detallista:alternateTradeItemIdentification',
                    'detallista:tradeItemDescriptionInformation',
                    'detallista:invoicedQuantity',
                    'detallista:grossPrice',
                    'detallista:netPrice',
                    'detallista:totalLineAmount',
                ]
            
            lineItems.append({
                                'nodeName':'detallista:lineItem', 
                                'text':'',
                                'attribs': item_attribs, 
                                'attribs_types': item_attribs_types,
                                'attribs_order': item_attribs_order,
            })
	
            item_consecutive_num = item_consecutive_num + 1
	        
        ### Fin Ciclo lineItem ###	    
        ##########################
        return lineItems
	     
    def det_format_data_dict(self, invoice=None):
        data = {}

        tipo = 'INVOICE'
        if invoice:
            if invoice.type == 'out_invoice':
                tipo = 'INVOICE'
            elif invoice.type == 'out_refund':
                tipo = 'CREDIT_NOTE'

        ### 1.1 - Request For Payment Identification
        data['requestForPaymentIdentification.node.entityType.value'] = tipo

        ### 1.2 - Special Instruction
        data['specialInstruction.attrib.code'] = 'ZZZ'
        data['specialInstruction.node.text.value'] = invoice.amount_to_text #Incorporado en l10n_mx_factuare

        ### 1.3 - Order Identification
        data['orderIdentification.node.referenceIdentification.value'] = invoice.name.strip() # Orden de Compra: Referencia de Factura
        data['orderIdentification.node.referenceIdentification.attrib.type'] = 'ON'
        data['orderIdentification.node.ReferenceDate.value'] = datetime.strptime( invoice.det_oi_ref_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') #Incorporado en l10n_mx_facturae_detallista

        ### 1.4 - Additional Information
        data['AdditionalInformation.node.referenceIdentification.attrib.type'] = 'ATZ'
        data['AdditionalInformation.node.referenceIdentification.value'] = invoice.det_ai_ref.strip() #Incorporado en l10n_mx_facturae_detallista

        ### 1.5 - Delivery Note
        data['DeliveryNote.node.referenceIdentification.value'] = invoice.det_dn_ref.strip() #Incorporado en l10n_mx_facturae_detallista
        data['DeliveryNote.node.ReferenceDate.value'] = datetime.strptime( invoice.det_dn_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') #Incorporado en l10n_mx_facturae_detallista

        ### 1.6 - Buyer
        data['buyer.node.gln.value'] = invoice.partner_id.ref.strip()
        data['buyer.node.contactInformation.node.personOrDepartmentName.node.text.value'] = invoice.det_buyer_name.strip() #Incorporado en l10n_mx_facturae_detallista

        ### 1.7 - Seller
        data['seller.node.gln.value'] = invoice.company_emitter_id.partner_id.ref.strip() #Incorporado en l10n_mx_facturae_pac
        data['seller.node.alternatePartyIdentification.attrib.type'] = 'SELLER_ASSIGNED_IDENTIFIER_FOR_A_PARTY'
        data['seller.node.alternatePartyIdentification.value'] = invoice.partner_id.num_proveedor.strip() #En modulo l10n_mx_facturae_addenda

        ### 1.8  -> shipTo (0, 1)
        
        ### 1.9  -> InvoiceCreator (0, 1)
        # data['InvoiceCreator.node.gln.value'] =
        # data['InvoiceCreator.node.alternatePartyIdentification.attrib.type']
        # data['InvoiceCreator.node.alternatePartyIdentification.value']
        # data['InvoiceCreator.node.nameAndAddress.node.name.value']
        # data['InvoiceCreator.node.nameAndAddress.node.streetAddressOne.value']
        # data['InvoiceCreator.node.nameAndAddress.node.city.value']
        # data['InvoiceCreator.node.nameAndAddress.node.postalCode.value']

        ### 1.10 -> Customs (0, 999999)
        ### 1.11 -> currency (0, 3)
        ### 1.12 -> paymentTerms (0, 1)
        ### 1.13 -> shipmentDetail (0, 1)

        ### 1.14 - AllowanceCharge
        data['allowanceCharge.attrib.settlementType'] = 'OFF_INVOICE'
        data['allowanceCharge.attrib.allowanceChargeType'] = 'ALLOWANCE_GLOBAL'
        data['allowanceCharge.node.specialServicesType.value'] = 'AJ'
        data['allowanceCharge.node.monetaryAmountOrPercentage.node.rate.attrib.base'] = 'INVOICE_VALUE'
        data['allowanceCharge.node.monetaryAmountOrPercentage.node.rate.node.percentage.value'] = str(invoice.global_discount_percent) #l10n_mx_invoice_discount

        ### 1.15 - lineItem

        # Inicia seccion Invoice Line
        data['lineItem'] = []

        for line in invoice.invoice_line:
            # Unit Price
            price_unit = line.quantity != 0 and line.price_subtotal / \
	        line.quantity or 0.0
            
            # GTIN - EAN13
            gtin_code = line.product_id and line.product_id.ean13.strip() or ''
            
            # Product Code
            product_code = line.product_id and line.product_id.default_code.strip() or ''
            
            # Unidad
            unidad = line.uos_id and line.uos_id.name or 'PCE'
            
            ### Determinar Calificadores de EDIFACT
            unidad = unidad.lower()
            
            if unidad.startswith('caj'):
                unidad = 'CS'
            else:
                unidad = 'PCE'
            
            item = {
                'tradeItemIdentification.node.gtin.value':gtin_code,
                'alternateTradeItemIdentification.attrib.type':'BUYER_ASSIGNED',
                'alternateTradeItemIdentification.value':gtin_code,
                'tradeItemDescriptionInformation.attrib.language':'ES',
                'tradeItemDescriptionInformation.node.longText.value':line.name[:35],
                'invoicedQuantity.attrib.unitOfMeasure':unidad,
                'invoicedQuantity.value': "%.2f" % (line.quantity or 0.0),
                'grossPrice.node.Amount.value': "%.2f" % (price_unit or 0.0),
                'netPrice.node.Amount.value': "%.2f" % (line.price_subtotal or 0.0),
                'totalLineAmount.node.grossAmount.node.Amount.value': "%.2f" % (line.price_subtotal or 0.0),  # round(line.price_unit *(1-(line.discount/100)),2) or 0.00),#Calc: iva, disc, qty
                'totalLineAmount.node.netAmount.node.Amount.value': "%.2f" % (line.price_subtotal or 0.0),  # round(line.price_unit *(1-(line.discount/100)),2) or 0.00),#Calc: iva, disc, qty
            }
            
            data['lineItem'].append({'Item': item})
            # Termina seccion Invoice Line

        ### 1.16 -> totalAmount (0, 1)
        data['totalAmount.node.Amount.value'] = str(invoice.amount_total)

        ### 1.17 -> TotalAllowanceCharge (0, 999999)
        data['TotalAllowanceCharge.attrib.allowanceOrChargeType'] = "ALLOWANCE"
        data['TotalAllowanceCharge.node.specialServicesType.value'] = "AJ"
        data['TotalAllowanceCharge.node.Amount.value'] = str(invoice.global_discount_amount) #Incorporado en l10n_mx_invoice_discount

        return data

    _columns = {
        ## 1.2
        'det_oi_ref_date': fields.datetime('Fecha Orden de Compra', help="Especifica la fecha de la orden de compra(comprador) a la que hace referencia la factura"),
        ## 1.3
        'det_ai_ref': fields.char('Referencia Adicional', size=35, help='Especifica el número de referencia adicional.'),
        ## 1.4
        'det_dn_ref': fields.char('No. Contra-Recibo', size=35, help="Especifica el numero de folio. Número emitido por el comprador cuando recibe la mercancía que es facturada."),
        'det_dn_date': fields.datetime('Fecha Contra-Recibo', help="Especifica la fecha en que fue asignado el no. de folio de recibo"),
        ## 1.5
        'det_buyer_name': fields.char('Nombre/No. de Depto.', size=35, help="Especifica el contacto de compras. Numero de Departamento."),
    }
account_invoice()

