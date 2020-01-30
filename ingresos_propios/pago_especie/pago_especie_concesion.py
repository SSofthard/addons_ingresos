# -*- coding: utf-8 -*-


from openerp.osv import fields,osv
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import *

class concesiones(osv.osv):
    _inherit='concesiones'
    
    _columns={
        'pago_especie_concesion_ids':fields.one2many('pago_especie_concesion','especie_concesion_id','Pago en Especies'),
    }
    

class pago_especie_concesion(osv.osv):
    _name="pago_especie_concesion"
    
    _columns={
            'especie_concesion_id':fields.many2one('concesiones', 'Pago en especie concesion'),
            'especie_id':fields.many2one('especie', 'Nombre de Pago en epecie'),
            'condicion_id':fields.text('condicion', help='Describa la condicion actual del pago'),
            'fecha_pago':fields.date('Fecha de pago', required=True, help='Fecha en que se realiza el pago.'),
            'state': fields.selection([
                ('draft','Borrador'),
                ('unexecuted','NO ejecutado'),
                ('executed','Ejecutado'),
                ('overdue','En Mora')],
                'status', required=True),
            }
                
    _defaults= {
            'state':'draft',
            }
    
    
    def no_ejecutado(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'unexecuted',})
        
    def ejecutado(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'executed',})
                    
    def mora(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'overdue',})
    


class especie(osv.osv):
    _name="especie" 
    _rec_name="nombre"
    
    
    _columns={
            'nombre':fields.char('Nombre',size=80,required=True,help='Indique el nombre del pago en especie'),
    
            }
    
