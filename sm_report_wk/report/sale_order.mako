<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <style type="text/css">
        ${css}

.list_main_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
table.list_main_table {
    margin-top: 20px;
}
.list_main_headers {
    padding: 0;
}
.list_main_headers th {
    border: thin solid #000000;
    padding-right:3px;
    padding-left:3px;
    background-color: #EEEEEE;
    text-align:center;
    font-size:12;
    font-weight:bold;
}
.list_main_table td {
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_main_lines,
.list_main_footers {
    padding: 0;
}
.list_main_footers {
    padding-top: 15px;
}
.list_main_lines td,
.list_main_footers td,
.list_main_footers th {
    border-style: none;
    text-align:left;
    font-size:12;
    padding:0;
}
.list_main_footers th {
    text-align:right;
}

td .total_empty_cell {
    width: 77%;
}
td .total_sum_cell {
    width: 13%;
}

.nobreak {
    page-break-inside: avoid;
}
caption.formatted_note {
    text-align:left;
    border-right:thin solid #EEEEEE;
    border-left:thin solid #EEEEEE;
    border-top:thin solid #EEEEEE;
    padding-left:10px;
    font-size:11;
    caption-side: bottom;
}
caption.formatted_note p {
    margin: 0;
}

.main_col1 {
    width: 40%;
}
td.main_col1 {
    text-align:left;
}
.main_col2,
.main_col3,
.main_col4,
.main_col6 {
    width: 10%;
}
.main_col5 {
    width: 7%;
}
td.main_col5 {
    text-align: center;
    font-style:italic;
    font-size: 10;
}
.main_col7 {
    width: 13%;
}

.right_table {
    right: 4cm;
    width:"100%";
}

.std_text {
    font-size:12;
}

th.date {
    width: 90px;
}

td.amount, th.amount {
    text-align: right;
    white-space: nowrap;
}

td.date {
    white-space: nowrap;
    width: 90px;
}

.address .recipient .shipping .invoice {
    font-size: 12px;
}

.address {
    paddint-top: 10px;
}

    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    <%def name="address(partner)">
        <%doc>
            XXX add a helper for address in report_webkit module as this won't be suported in v8.0
        </%doc>
		<%res_client=get_data_partner(partner_id=partner.id)%>
		
		%if partner.is_company:
			<tr><td class="name">${res_client['name']}</td></tr>
			<tr><td>${res_client['vat']}</td></tr>
		%else:
			<tr><td class="name">${res_client['parent_name']}</td></tr>
			<tr><td class="name">${res_client['name']}</td></tr>
		%endif
		
		<tr>
		    <td>${res_client['street']}
			%if res_client['l10n_mx_street3']:
				No. Ext. ${res_client['l10n_mx_street3']} 
			%endif
			%if res_client['l10n_mx_street4']:
				No. Int:${res_client['l10n_mx_street4']}
			%endif
			</td>
		</tr>
		<tr><td>${res_client['street2'] or ''}</td></tr>
		<tr><td>${res_client['l10n_mx_city2'] or ''}</td></tr>
		<tr><td>${res_client['city'] or ''}, ${res_client['state'] or ''}</td></tr>
		<td>${res_client['zip'] or ''}</td></tr>
		<td>${res_client['phone'] or ''}</td></tr>
    </%def>

    %for order in objects:
    <% setLang(order.partner_id.lang) %>
    <%
      quotation = order.state in ['draft', 'sent']
    %>
    <div class="address">
		<table width="100%">
			<tr>
				<th align="left">${_("Shipping address:")}</th>
				<th align="left">${_("Invoice address:")}</th>
			</tr>
			<tr valign="top">
				<td valign="top">
					<table height="100%" width="100%" class="shipping">
					  ${address(partner=order.partner_shipping_id)}
					</table>
				</td>
				<td valign="top">
					<table height="100%" width="100%"  class="invoice">
						${address(partner=order.partner_invoice_id)}
					</table>
				</td>
			</tr>
		</table>
    </div>

    <h1 style="clear:both;">${quotation and _(u'Quotation N°') or _(u'Order N°') } ${order.name}</h1>

    <table class="basic_table" width="100%">
        <tr>
            <th class="date">${quotation and _("Date Ordered") or _("Quotation Date")}</td>
            <th>${_("Your Reference")}</td>
            <th>${_("Salesman")}</td>
            <th>${_('Carrier')}</td>
        </tr>
        <tr>
            <td class="date">${formatLang(order.date_order, date=True)}</td>
            <td>${order.client_order_ref or ''}</td>
            <td>${order.user_id and order.user_id.name or ''}</td>
            <td>${order.sm_carrier_id and order.sm_carrier_id.name or ''}</td>
        </tr>
    </table>

    <div>
    %if order.note1:
        <p class="std_text"> ${order.note1 | n} </p>
    %endif
    </div>

    <table class="list_main_table" width="100%">
      <thead>
        <tr>
          <th class="list_main_headers" style="width: 100%">
            <table style="width:100%">
              <tr>
                <th class="main_col1">${_("Description")}</th>
                <th class="amount main_col2">${_("Quantity")}</th>
                <th class="amount main_col3">${_("UoM")}</th>
                <th class="amount main_col4">${_("Unit Price")}</th>
                <th class="main_col5">${_("VAT")}</th>
                <th class="amount main_col6">${_("Disc.(%)")}</th>
                <th class="amount main_col7">${_("Price")}</th>
              </tr>
            </table>
          </th>
        </tr>
      </thead>
      <tbody>
        %for line in order.order_line:
          <tr>
            <td class="list_main_lines" style="width: 100%">
              <div class="nobreak">
                <table style="width:100%">
                  <tr>
                    <td class="main_col1">${ line.name }</td>
                    <td class="amount main_col2">${ formatLang(line.product_uos and line.product_uos_qty or line.product_uom_qty) }</td>
                    <td class="amount main_col3">${ line.product_uos and line.product_uos.name or line.product_uom.name }</td>
                    <td class="amount main_col4">${formatLang(line.price_unit)}</td>
                    <td class="main_col5">${ ', '.join([tax.description or tax.name for tax in line.tax_id]) }</td>
                    <td class="amount main_col6">${line.discount and formatLang(line.discount, digits=get_digits(dp='Sale Price')) or ''} ${line.discount and '%' or ''}</td>
                    <td class="amount main_col7">${order.pricelist_id.currency_id.symbol} ${formatLang(line.price_subtotal, digits=get_digits(dp='Sale Price'))}&nbsp;</td>
                  </tr>
                  %if line.formatted_note:
                    <caption class="formatted_note">
                      ${line.formatted_note| n}
                    </caption>
                  %endif
                </table>
              </div>
            </td>
          </tr>
        %endfor
      </tbody>
      <tfoot class="totals">
        <tr>
          <td class="list_main_footers" style="width: 100%">
            <div class="nobreak">
              <table style="width:100%">
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Net Total:")}
                  </th>
                  <td class="amount total_sum_cell">
                    ${order.pricelist_id.currency_id.symbol} ${formatLang(order.amount_untaxed, get_digits(dp='Sale Price'))} 
                  </td>
                </tr>
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Taxes:")}
                  </th>
                  <td class="amount total_sum_cell">
                    ${order.pricelist_id.currency_id.symbol} ${formatLang(order.amount_tax, get_digits(dp='Sale Price'))} 
                  </td>
                </tr>
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Total:")}
                  </th>
                  <td class="amount total_sum_cell">
                    <b>${order.pricelist_id.currency_id.symbol} ${formatLang(order.amount_total, get_digits(dp='Sale Price'))} </b>
                  </td>
                </tr>
              </table>
            </div>
          </td>
        </tr>
      </tfoot>
    </table>

    %if order.note :
        <p class="std_text">${order.note | carriage_returns}</p>
    %endif
    %if order.note2:
        <p class="std_text">${order.note2 | n}</p>
    %endif
    <p class="std_text">Firma de Autorizacion: ________________________</p>

    <p style="page-break-after:always"/>
    %endfor
</body>
</html>
