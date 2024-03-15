# -*- coding: utf-8 -*-
#Part of Odoo. See LICENSE file for full copyright and licensing details
from odoo import fields, models, api

from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    commission_plan_ids = fields.Many2many('sales.commissions.plans', string="Commission Plans", compute='_compute_commission_plans', store=True)

    @api.depends('product_id')
    def _compute_commission_plans(self):
        for line in self:
            commission_plans = self.env['sales.commissions.plans'].search([])
            arr = []
            for plan in commission_plans:
                if line.product_id.id in plan.product_ids.ids:
                    arr.append(plan.id)
            line.commission_plan_ids = [(6, 0, arr)]