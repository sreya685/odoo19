{
    'name': 'Advanced New',
    'author' : 'Advanced New',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends':[
       'base',
       'sales_team',
        # 'user'

    ],

    'data':[
      'security/ir.model.access.csv',
      # 'data/sequence.xml',
      'views/res_users.xml',
      'views/revenue_commission_view.xml',
      'views/crm_commission_view.xml',
      'views/menu.xml',
],
    'installable':True,
    'application': True

}