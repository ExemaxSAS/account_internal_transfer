# -*- coding: utf-8 -*-

from locale import currency
from datetime import datetime
import time
from odoo import models, api, fields

class Account_inter_transfer(models.Model):
    _name = "account.inter.transfer"

    def action_post(self):
        move_out = self.env['account.move'].create({
            'journal_id': self.diario.id,
            'currency_id': self.currency_id.id,
            'company_id': self.company_id.id,
            'line_ids': [(0, 0, {
                 'account_id': self.company_id.account_journal_payment_credit_account_id.id,
                 'partner_id': self.company_id.partner_id.id,
                 'currency_id': self.currency_id.id,
                 'credit': self.amount}),
                 (0, 0, {
                 'account_id': self.company_id.transfer_account_id.id,
                 'partner_id': self.company_id.partner_id.id,
                 'currency_id': self.currency_id.id,
                 'debit': self.amount})]
            })
        move_in = self.env['account.move'].create({
            'journal_id': self.diario_destino.id,
            'currency_id': self.currency_id.id,
            'company_id': self.company_id.id,
            'line_ids': [(0, 0, {
                 'account_id': self.company_id.transfer_account_id.id,
                 'partner_id': self.company_id.partner_id.id,
                 'currency_id': self.currency_id.id,
                 'credit': self.amount}),
                 (0, 0, {
                 'account_id': self.company_id.account_journal_payment_debit_account_id.id,
                 'partner_id': self.company_id.partner_id.id,
                 'currency_id': self.currency_id.id,
                 'debit': self.amount})]
            })
        move_out.action_post()
        move_in.action_post()
        self.state = 'post'

    date = fields.Date(string="Fecha", default=datetime.now().strftime('%Y-%m-%d'))
    diario = fields.Many2one('account.journal', string="Diario")
    diario_destino = fields.Many2one('account.journal', string="Diario destino")
    amount = fields.Float(string="Importe")
    currency_id = fields.Many2one('res.currency', string="Moneda")
    company_id = fields.Many2one('res.company', 'Compañía', default=lambda self: self.env.company)
    state = fields.Selection([('draft', 'Borrador'), ('post', 'Publicado')], string='Estado', default='draft')
