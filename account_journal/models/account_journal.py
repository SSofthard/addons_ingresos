# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class account_journal(osv.osv):
    """Account Journal"""
    _name = 'account.journal'
    _inherit='account.journal'
    
    _columns = {
        'comision': fields.float('Comision por pago', size=50, help='Porcentaje de comision para el metodo de pago'),
        'default_credit_commission_account_id': fields.many2one('account.account', 'Default Credit Account Commission', domain="[('type','!=','view')]", help="It acts as a default account for credit amount"),
    }



