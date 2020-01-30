# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
import time
from openerp.report import report_sxw




class autorizacion_wizard(osv.TransientModel):
    _name = 'autorizacion.wizard'
    _columns = {
        
        'date_start': fields.datetime('Desde ', required=False),
        'date_end': fields.datetime('Hasta', required=False),
    }
   
    
    
    
    def imprimir_reporte(self, cr, uid, ids, context=None):
        values = {
            'ids': ids,
            'model': 'autorizacion',
            'form': self.read(cr, uid, ids, context=context)[0]
        }
        return self.pool['report'].get_action(cr, uid, [], 'autorizacion.id_template_autorizacion_qweb', data=values, context=context)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
