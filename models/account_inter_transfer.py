
from locale import currency
from datetime import datetime
import time
from odoo import models, api, fields


class Account_inter_transfer(models.Model):
    _name = "account.inter.transfer" 
    

    date = fields.Date(string="Fecha", default=datetime.now().strftime('%Y-%m-%d'))
    diario = fields.Many2one('account.journal',string="Diario")
    diario_destino = fields.Many2one('account.journal',string="Diario destino")
    amount = fields.Float(string="Importe")
    currency_id = fields.Many2one('res.currency', string="Moneda")