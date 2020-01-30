# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields
from openerp.osv import osv
from openerp.tools import config
import time
from openerp.report import report_sxw


class rendicion_general__report_wizard(osv.TransientModel):
    """Registro de Rendicion general"""
    
    _name = "rendicion_general.report.wizard"
    _rec_name = 'date_start'
    
    _columns = {
                #~ 'registro_parque_id2':fields.many2many('registro_parque','parques_reporte','parque_id','reporte_id', required=False),
                'registro_parque_id':fields.many2one('registro_parque','Parques',required=True,help='Registro Parques'),
                'date_start':fields.datetime('fecha inicio'),
                'date_end':fields.datetime('fecha fin'),
                
                }
                
    def print_report(self, cr, uid, ids, context=None):
        data = {
             'ids': ids,
             'model': 'account.voucher',
             'form': self.read(cr, uid, ids, context=context)[0]
        }
        return self.pool['report'].get_action(cr, uid, [], 'ingresos_propios.id_rendicion_general1_report_qweb', data= data, context=context) 
         

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
