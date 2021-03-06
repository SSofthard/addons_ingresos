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
# Generated by the OpenERP plugin for Dia !
from openerp.osv import fields, osv


class registro_parque(osv.osv):
    _name='registro_parque'
    _inherit='registro_parque'
    
    _columns={
        'puesto_vig_ids':fields.one2many('puesto_vigilancia','registro_parque_id','Puesto de Control'),
    }
    
    
class jornada_laboral(osv.osv):
    _name= 'jornada_laboral'
    
    _columns = {
    
    'resource_ids2':fields.many2one('puesto_vigilancia','Planificación de trabajo',required=True,ondelete='cascade'),
    'name' : fields.char("Name", required=True),
    'dayofweek': fields.selection([('0','Lunes'),('1','Martes'),('2','Miércoles'),('3','Jueves'),('4','Viernes'),('5','Sábado'),('6','Domingo')], 'Day of Week', required=True, select=True),
    'hour_from' : fields.float('Work from', required=True, help="Start and End time of working.", select=True),
    'hour_to' : fields.float("Work to", required=True),
    }
    
    def validar_hora(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids):
            if ((i.hour_from >= 00.00 and i.hour_from<=24.00) and (i.hour_to>=00.00 and i.hour_to<=24.00)):
                print "Hora Correcta"
            else:
                raise osv.except_osv(('Error!!!'),('Coloca una Hora Valida'))
            return True
            
    _constraints = [
        (validar_hora, 'Introduzca una hora valida', ['hour_from','hour_to']),
    ]
  
    
class puesto_vigilancia(osv.osv):
    _name="puesto_vigilancia"
    _description = "Puesto de Vigilancia"
    
    _columns={
    
        'nombre':fields.char('Nombre',size=80,help='Este es el Nombre del Puesto de vigincia'),
        'latitud':fields.float('Latitud',size=05,help='Latitud Puesto de Vigilancia'),
        'longitud':fields.float('Longitud',size=05,help=' Puesto de Vigilancia'),
        'puesto_ids1': fields.selection([('guarda_par', 'Guarda Parque'),('vig_par','Vigilancia')]),
        'registro_parque_id':fields.many2one('registro_parque','Puesto'),
        'resource_ids':fields.one2many('jornada_laboral','resource_ids2','Horario Laboral'),
    }




