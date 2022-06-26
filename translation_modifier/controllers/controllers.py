# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request,Response
from odoo.tools import date_utils
import json

class TranslationModifier(http.Controller):
    @http.route('/update/translation/', type='http', auth="none",methods=['POST','OPTIONS'],website=False, csrf=False,cors='*')
    def update_translation(self,**kwargs):

        
        records = request.env.cr.execute(f'''
                                    SELECT res_id AS product_id,value AS translated_value
                                    FROM
                                    ir_translation 
                                    WHERE name = 'product.template,name' AND lang = 'es_CO' AND src LIKE '%(copia)'
                                    ''')
        records = request.env.cr.dictfetchall()
        
        
        if records:
            for rec in records:
                
                request.env.cr.execute(f'''
                                    UPDATE product_template SET
                                    name = "{rec['translated_value']}"
                                    WHERE
                                    id = {rec['product_id']}
                                    ''')       
                request.env.cr.execute(f'''
                                    UPDATE ir_translation SET
                                    src = "{rec['translated_value']}"
                                    WHERE
                                    res_id = {rec['product_id']} and name ='product.template,name'
                                    ''')
        response = Response(
                        json.dumps(
                                    {
                                    'success':True
                                    },
                                    default=date_utils.json_default
                                    ),
                        content_type='application/json',
                        status=200
                                    
                    )
        response.status = '200'
        return response

    @http.route('/update/spanish/translation/', type='http', auth="none",methods=['POST','OPTIONS'],website=False, csrf=False,cors='*')
    def update_spanish_translation(self,**kwargs):

        
        records = request.env.cr.execute(f'''
                                    SELECT res_id AS product_id,src,value AS translated_value
                                    FROM
                                    ir_translation 
                                    WHERE name = 'product.template,name' AND lang = 'es_CO'
                                    ''')
        records = request.env.cr.dictfetchall()
        
        
        if records:
            for rec in records:
                th = request.env['translation.logs'].sudo().create({"product_tmpl_id":rec['product_id'],"original_name":rec['src'],"spanish_name":rec['translated_value']})
                rec['translated_value'] = rec['translated_value'].replace("'","")
                request.env.cr.execute(f'''
                                    UPDATE product_template SET
                                    name = '{rec['translated_value']}'
                                    WHERE
                                    id = {rec['product_id']}
                                    ''')       
                request.env.cr.execute(f'''
                                    UPDATE ir_translation SET
                                    src = '{rec['translated_value']}'
                                    WHERE
                                    res_id = {rec['product_id']} and name ='product.template,name'
                                    ''')
        response = Response(
                        json.dumps(
                                    {
                                    'success':True
                                    },
                                    default=date_utils.json_default
                                    ),
                        content_type='application/json',
                        status=200
                                    
                    )
        response.status = '200'
        return response


