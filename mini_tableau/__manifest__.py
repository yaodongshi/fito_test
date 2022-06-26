{
    'name':
    "Mini Tableau",
    'summary':
    """A Odoo Module for Bussiness Intelligence and Analytics.""",
    'description':
    """
        This module is a mini version of any Business Intelligence tools such as Power BI or Tableau wherein you can
        get the power to directly see all the tables in your Odoo database, write real time custom SQL queries and
        see the results. You can export the data into Excel and even illustrate the same graphically with the chart
        of your choice. The usage and design is similar to a BI tool however, the functionalities just enough to
        help you build a dashboard in order to see a wholistic view of your data just by a simple refresh. The
        queries and graphs can be saved and you can simply click on the saved report any time you want to see on
        live data.
    """,
    'author': "Techneith",
    'website': 'https://www.techneith.com',

    'price': 379,
    'currency': 'USD',
    'license': 'LGPL-3',

    'images': ['static/description/banner.png'],

    'category':'Reports',
    'version':'0.1',

    'depends': ['base', 'website'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/resources.xml',
        'views/query_dashboard.xml',
        'views/report_dashboard.xml',
        'views/saved_report.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
