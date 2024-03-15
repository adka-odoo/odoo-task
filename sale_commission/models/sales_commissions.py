# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api

class SalesCommissionsModel(models.Model):
    _name = 'sales.commissions'
    _description = 'Sales Commissions'
    _order = 'min_achievement'

    min_achievement = fields.Float(string="Min. Achievement")
    commission_rate = fields.Float(string="Commission")
    #Relational Fields
    commission_plan_id = fields.Many2one('sales.commissions.plans')
