# -*- coding: utf-8 -*-
#Part of Odoo. See LICENSE file for full copyright and licensing details
{
    'name' : "Sales Commission",
    'version' : "1.0",
    'summary' : "A module to track sales commission to assign to sales teams.",
    'depends': ['sale_management'],
    'data': [      
        'security/ir.model.access.csv',
          
        'views/sales_targets_view.xml',  
        'views/sales_commissions_view.xml',   
        'views/sales_commission_plans_views.xml',
        'views/sales_commission_reporting_view.xml',
        'views/sale_order_inherited_view.xml',
        'views/sales_commission_menu.xml'
    ],
    'installable' : True,
    'license' : "LGPL-3",
}
