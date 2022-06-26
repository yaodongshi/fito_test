import requests
import logging
import json
import base64
from odoo import fields, models, _
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class whatsappScanQRCode(models.TransientModel):
    _name = 'whatsapp.scan.qr.code'
    _description = 'Scan WhatsApp QR Code'

    def _get_default_image(self):
        param = self.env['res.config.settings'].sudo().get_values()
        Param_set = self.env['ir.config_parameter'].sudo()
        try:
            url = param.get('whatsapp_endpoint') + '/status?token=' + param.get('whatsapp_token')
            response = requests.get(url)
        except Exception as e_log:
            _logger.exception(e_log)
            raise UserError(_('Please add proper whatsapp endpoint or whatsapp token'))
        json_response = json.loads(response.text)
        if response.status_code == 201 or response.status_code == 200:
            # qr_code_image
            if json_response.get('accountStatus') == 'got qr code':
                qr_code_url = param.get('whatsapp_endpoint') + '/qr_code?token=' + param.get('whatsapp_token')
                response_qr_code = requests.get(qr_code_url)
                img = base64.b64encode(response_qr_code.content)
                Param_set.set_param("pragtech_whatsapp_base.whatsapp_authenticate", True)
                return img
            elif json_response.get('accountStatus') == 'authenticated':
                raise UserError(_('QR code is already scanned from chat api'))
        elif response.status_code > 200:
            raise UserError(_('There is issue in chat api'))

    qr_code_img_data = fields.Binary(default=_get_default_image)