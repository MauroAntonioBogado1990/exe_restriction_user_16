{
    'name': 'Exe Restricción por usuario version 16',
    'version': '16.0',
    'category': 'Tools',
    'author':'Mauro Bogado,Exemax',
    'depends': ['stock', 'mrp', 'hr', 'website', 'base','sale','board'],
    'data': [

    'data/groups.xml',
    #'security/ir.model.access.csv',
    'security/record_rules.xml',
    'views/hide_menus.xml',
    # 'views/hide_board_menu.xml' removed because it attempted to update a menu
    # that may not exist in all installations and caused ParseError on upgrade.
    ],

    'installable': True,
    'application': False,
}
