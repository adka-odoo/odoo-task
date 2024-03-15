# -*- coding: utf-8 -*-
#Part of Odoo. See LICENSE file for full copyright and licensing details
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SalesCommissionsPlans(models.Model):
    _name = "sales.commissions.plans.report"
    _description = "Sales Commission Plan Reports"
    
    commission_plan_id = fields.Many2one('sales.commissions.plans', string="Commission Plan")
    target_id = fields.Many2one('sales.targets', string="Target Quarter")
    achieved_amount = fields.Float(default=0, compute='_compute_achieved_amount')
    target_amount = fields.Float(compute='_compute_tree_values')
    salesperson_id = fields.Many2one('res.users', string="Salesperson", compute='_compute_tree_values')
    team_id = fields.Many2one('crm.team', string="Sales Team", compute='_compute_tree_values')
    desired_commission_rate = fields.Float(string="Commission Rate",compute='_compute_desired_commission_rate')
    pivot_achieved_amount = fields.Float(string="Achieved Amount", default=0, store=True)
    pivot_target_amount = fields.Float(string="Target Amount", store=True)
    
    #Function to compute Amount Achieved from commissions from the particular sale orders.
    def _compute_achieved_amount(self):
        for record in self:
            orders = self.env['sale.order.line'].search([
                 ('salesman_id.id', '=', record.commission_plan_id.salesperson_id.id),
                 ('order_id.date_order', '>=', record.target_id.quarter_start_date),
                 ('order_id.date_order', '<=', record.target_id.quarter_end_date),
                ])
            temp = 0
            for order in orders:
                if order.product_id.id in record.commission_plan_id.product_ids.ids:
                    temp += order.price_subtotal
            record.achieved_amount = temp
            record.pivot_achieved_amount = record.achieved_amount
            record.pivot_target_amount = record.target_amount
            
    #Function to use fields in our reporting view by getting them using relational fields.
    @api.depends('target_id', 'commission_plan_id')
    def _compute_tree_values(self):
        for record in self:
            record.target_amount = record.target_id.target_amount
            record.salesperson_id = record.commission_plan_id.salesperson_id
            record.team_id = record.commission_plan_id.team_id
    
    #Function to compute the Commission Rate allotted on the provided parameters 
    @api.depends('commission_plan_id', 'achieved_amount')
    def _compute_desired_commission_rate(self):
        for record in self:
            record.desired_commission_rate = 0
            if record.commission_plan_id:
                achievement_percent = (record.achieved_amount / record.target_amount) * 100 if record.target_amount != 0 else 0
                desired_rate = 0
                for commission in record.commission_plan_id.commissions_ids:
                    if commission.min_achievement <= achievement_percent:
                        desired_rate = commission.commission_rate
                    else:
                        break
                record.desired_commission_rate = desired_rate
