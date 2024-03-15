# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api

class SalesCommissionsModel(models.Model):
    _name = 'sales.targets'
    _description = 'Sales Targets'

    name = fields.Char(string="Quarter")
    quarter_start_date = fields.Date(string="Start Date")
    quarter_end_date = fields.Date(string="End Date")
    target_amount = fields.Float(string="Amount")
    #Relational Fields
    commission_plan_id = fields.Many2one('sales.commissions.plans')
    
    # SQL Constraints
    _sql_constraints = [
        ('check_target_amount_positive', 'CHECK(target_amount >= 0)', 'Target amount must be positive.'),
        ('check_dates', 'CHECK(quarter_start_date < quarter_end_date)', 'End date must be after start date.'),
    ]
