{
    'name': ' Product Insight Manager',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends':[
        'product',
        'contacts'

    ],

    'data':[
          'security/ir.model.access.csv',
          'views/product_price_wizard_views.xml',
         'views/product_product_views.xml',

],
    'installable':True,
    'application': True

}