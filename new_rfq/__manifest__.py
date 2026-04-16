{
    'name': 'rfq creation',
    'sequence': 1,
    'version': '1.0',

    'license': 'LGPL-3',
    'depends':[
          'purchase',
          'base'
    ],

    'data':[
          'security/ir.model.access.csv',
          'views/product_product_views.xml',
          'views/wizard_po_views.xml',
],
    'installable':True,
    'application': True

}