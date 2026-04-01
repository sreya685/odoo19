{
    'name': 'Manufacturing Order',
    'author' : 'Manufacturing Order',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends':[
       'base',
       'product',
       'mrp'
    ],

    'data':[
    'security/ir.model.access.csv',
    'data/sequence.xml',
    'views/product_view.xml',
    'views/mrp_production_ext_view.xml',
    # 'views/mrp_production_material_line_view.xml',
    'views/menu.xml',
],
    'installable':True,
    'application': True

}