{
    'name': 'Library Management',
    'author':'library',
    'version': '1.0',
    'sequence':1,
    'license': 'LGPL-3',
    'depends':[
        'base_setup',
        'mail',
        'product',
        'account',
         'web',
        'website'
    ],

    'data':[
       'security/library_security.xml',
       'security/ir.model.access.csv',
       'data/penalty.xml',
       'data/remainder_mail_template.xml',
       'data/cron_remainder_template.xml',
       'data/automate_genres.xml',
       'data/sequence.xml',
       'reports/book_borrow_report.xml',
       'views/portal_page.xml',
       'views/donation_form.xml',
       'views/account_move_view.xml',
       'wizard/recommendation_view.xml',
       'wizard/report_wizard_views.xml',
       'wizard/xlsx_report_wizard_view.xml',
       'views/library_report.xml',
       'views/report_views.xml',
       'views/members_view.xml',
       'views/checkout_line_view.xml',
       'views/res_config_settings.xml',
       'views/tag_view.xml',
       'views/library_books_checkouts.xml',
       'views/library_books_genres.xml',
       'views/library_books_publishers.xml',
       'views/library_books_authors_view.xml',
       'views/library_books_view.xml',
       'views/book_menu.xml'

],
    'assets': {
        'web.assets_backend': [
            'library/static/src/js/action_manager.js',

        ]
    },
    'installable':True,
    'application': True

}