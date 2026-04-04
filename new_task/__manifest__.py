{
    'name': 'new task',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends':[
        'base',
        'sale',
        'mail',
        'contacts'
    ],

    'data':[
         'views/res_partner_views.xml',
         'views/sale_order_views.xml'

],
    'installable':True,
    'application': True

}