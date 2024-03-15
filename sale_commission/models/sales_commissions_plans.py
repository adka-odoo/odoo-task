# -*- coding: utf-8 -*-
#Part of Odoo. See LICENSE file for full copyright and licensing details
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SalesCommissionsPlans(models.Model):
    _name = "sales.commissions.plans"
    _description = "Sales Commission Plans"
    active = fields.Boolean(default=True)
    
    name = fields.Char(string="Commission Plan", required=True)
    start_date = fields.Date(required=True, default=fields.date.today())
    end_date = fields.Date(required=True)
    target = fields.Float(string="Target", compute="_compute_total_target")
    stage = fields.Selection([('draft', "Draft"), ('approved', "Approved"), ('done', "Done"), ('cancelled', "Cancelled")], default="draft")
    #Relational Fields (from external modules' models)
    product_ids = fields.Many2many('product.product', string="Products")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    team_id = fields.Many2one('crm.team', string="Sales Team", required=True)
    salesperson_id = fields.Many2one('res.users', string="Salesperson")
    #Relational Fields (from this module's models)
    commissions_ids = fields.One2many('sales.commissions', 'commission_plan_id', string="Commissions")
    target_ids = fields.One2many('sales.targets', 'commission_plan_id', string="Targets")


    '''    @api.depends('salesperson_id', 'team_id')
    def _compute_display_name(self):
        for record in self:
            name = record.salesperson_id.name
            if record.salesperson_id:
                name = f"{record.salesperson_id.name} ({record.team_id.name})"
            record.display_name = name'''


    #Function to show salesperson name in the desired format


    #Function to calculate total target from summing all the targets
    @api.depends('target_ids.target_amount')
    def _compute_total_target(self):
        self.target = sum(self.target_ids.mapped('target_amount'))
    
    #Function to Approve a Commission Plan
    def action_stage_approve(self):
        for line in self:
            if line.stage=='cancelled':
                raise ValidationError("Cancelled commission plan can't be approved")
            elif line.stage=='approved':
                raise ValidationError("Commission plan already approved")
            elif line.stage=='done':
                raise ValidationError("Commission plan already done")
            line.stage='approved'
    
    #Function to Cancel a Commission Plan
    def action_stage_cancelled(self):
        for line in self:
            if line.stage=='done':
                raise ValidationError("This commission plan can't be cancelled as it is already done")
            line.stage='cancelled'

    #Function to Mark a Commission Plan as Done
    def action_stage_done(self):
        for line in self:
            line.stage='done'
