# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Logs(models.Model):
    _name = 'translation.logs'

    product_tmpl_id = fields.Integer(string='id')
    original_name = fields.Char(string="original")
    spanish_name = fields.Char(string="spanish")
    
class translation_modifier(models.Model):

    _inherit = 'ir.translation'
    _description = 'update english translation in database'

    
    def write(self, values):

        record = super(translation_modifier, self).write(values)
        if len(self)==1:
            if self.name == 'product.template,name' and self.lang == 'es_CO':
                self.update_es_CO_translation_in_db(product_id=self.res_id,translated_value=values['value'])
        return record

    def update_es_CO_translation_in_db(self,product_id,translated_value):
        
        translated_value = translated_value.replace("'","")
        self.env.cr.execute(f'''
                                    UPDATE product_template SET
                                    name = '{translated_value}'
                                    WHERE
                                    id = {product_id}
                                    ''')
        self.env.cr.execute(f'''
                                    UPDATE ir_translation SET
                                    src = '{translated_value}'
                                    WHERE
                                    res_id = {product_id} and name ='product.template,name'
                                    ''')