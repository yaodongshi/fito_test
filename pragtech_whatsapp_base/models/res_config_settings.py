import logging
import requests
import base64
import json
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class base(models.TransientModel):
    _inherit = "res.config.settings"

    whatsapp_endpoint = fields.Char('Whatsapp Endpoint', help="Whatsapp api endpoint url with instance id")
    whatsapp_token = fields.Char('Whatsapp Token')
    qr_code_image = fields.Binary("QR code")
    whatsapp_authenticate = fields.Boolean('Authenticate', default=False)

    @api.model
    def get_values(self):
        res = super(base, self).get_values()
        param = self.env['ir.config_parameter'].sudo()
        res['whatsapp_endpoint'] = param.sudo().get_param('pragtech_whatsapp_base.whatsapp_endpoint')
        res['whatsapp_token'] = param.sudo().get_param('pragtech_whatsapp_base.whatsapp_token')
        res['whatsapp_authenticate'] = param.sudo().get_param('pragtech_whatsapp_base.whatsapp_authenticate')
        res.update(qr_code_image=param.sudo().get_param('pragtech_whatsapp_base.qr_code_image'))
        return res

    def set_values(self):
        super(base, self).set_values()
        if self.whatsapp_endpoint:
            if (self.whatsapp_endpoint)[-1] == '/':
                self.env['ir.config_parameter'].sudo().set_param('pragtech_whatsapp_base.whatsapp_endpoint', (self.whatsapp_endpoint)[:-1])
            else:
                self.env['ir.config_parameter'].sudo().set_param('pragtech_whatsapp_base.whatsapp_endpoint', self.whatsapp_endpoint)
        self.env['ir.config_parameter'].sudo().set_param('pragtech_whatsapp_base.whatsapp_token', self.whatsapp_token)
        self.env['ir.config_parameter'].sudo().set_param('pragtech_whatsapp_base.qr_code_image', self.qr_code_image)

    def action_get_qr_code(self):
        return {
            'name': _("Scan WhatsApp QR Code"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'whatsapp.scan.qr.code',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_logout_from_whatsapp(self):
        param = self.sudo().get_values()
        try:
            url = param.get('whatsapp_endpoint') + '/logout?token=' + param.get('whatsapp_token')
            headers = {"Content-Type": "application/json"}
            tmp_dict = {"accountStatus": "Logout request sent to WhatsApp" }
            response = requests.post(url, json.dumps(tmp_dict), headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                _logger.info("\nWhatsapp logout successfully")
                self.env['ir.config_parameter'].sudo().set_param('pragtech_whatsapp_base.whatsapp_authenticate', False)
        except Exception as e_log:
            _logger.exception(e_log)
            raise UserError(_('Please add proper whatsapp endpoint or whatsapp token'))
