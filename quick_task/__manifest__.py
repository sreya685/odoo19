{
    'name': 'quick tasks',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends':[
        'product',
        'project',
        'purchase',
         'mail'
    ],

    'data':[
          'views/project_task_view.xml',
         'views/product_views.xml',
        'views/purchase_order_view.xml',

],
    'installable':True,
    'application': True

}