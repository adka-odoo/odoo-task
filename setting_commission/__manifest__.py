# -*- coding: utf-8 -*-
#Part of Odoo. See LICENSE file for full copyright and licensing details
{
    'name' : "Sales Commission Handling",
    'version' : "1.0",
    'summary' : "Manage sales and team targets commissions",
    'depends': ['sale_management'],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    'installable' : True,
    'auto_install' : True,
    'license' : "LGPL-3",
}
