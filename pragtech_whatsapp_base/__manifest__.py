{
    'name': 'Whatsapp Base',
    'version': '13.0.0',
    'category': 'Connector',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': 'pragtech.co.in',
    'summary': 'whatsapp connector whatsapp integration odoo Whatsapp crm Whatsapp lead Whatsapp task Whatsapp sale order Whatsapp purchase order Whatsapp invoice Whatsapp payment reminder Whatsapp pos Whatsapp so Whatsapp point of sale whats app communication',
    'description': """
Whatsapp base is a base module that handles the authentication process for the vendor https://chat-api.com.

Customer needs to install this module first and then they can use its dependent module developed by pragmatic
    """,
    'depends': ['base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_view.xml',
        'wizard/whatsapp_scan_qr_code_view.xml'
    ],

    'images': [''],
    'live_test_url': 'https://www.pragtech.co.in/company/proposal-form.html?id=103&name=odoo-whatsapp-integration',
    'price': 0,
    'currency': 'USD',
    'license': 'OPL-1',
    'application': False,
    'auto_install': False,
    'installable': True,
}
