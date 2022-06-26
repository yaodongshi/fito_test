# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    has_google_tagmanager = fields.Boolean(
        string="Google Tag Manager",
        config_parameter='odoo_google_tag_manager.has_google_tagmanager')
    google_tagmanager_key = fields.Char(
        string='Google container ID', 
        related='website_id.google_tagmanager_key',
        readonly=False)

    @api.onchange('has_google_tagmanager')
    def onchange_has_google_tagmanager(self):
        if not self.has_google_tagmanager:
            self.google_tagmanager_key = False
