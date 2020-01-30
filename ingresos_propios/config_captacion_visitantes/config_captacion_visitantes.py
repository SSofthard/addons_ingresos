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
from openerp.osv import fields, osv


class config_captacion_visitantes(osv.osv):
    _name = 'config_captacion_visitantes'
    _rec_name = 'nombre'
    
    _columns = {
        'nombre':fields.char('Nombre',size=100,required=True),
        'porcentaje':fields.float('Porcentaje',required=False),
    }


    def get_default_cap_vis(self, cr, uid, ids, fields,context=None):
        res=[]
        for r in self.browse(cr,uid,ids):
            resultado=r.porcentaje*100
            resultado1=r.nombre
            
            resul1=''
            res={
                'nombre':resultado1,
                'porcentaje':resultado,
                    }
        return {'value':res}

        
    
    
    
    
    
    #~ def registro(self,cr,uid,ids,context=None):
    
    
        #~ captacion_visitantes_obj.self.pool.get('config_captacion_visitantes')
        #~ cr.execute("select * from config_captacion_visitantes")
        #~ for row in cr.fetchall():
                    #~ row=set(row)
                    #~ print row
                    #~ print row
                    #~ print row
                    #~ print row
                    #~ print row
                    #~ print row
                    #~ awning_ids=set(awning_ids)
                    #~ awning_ids=awning_ids-row
                    #~ print (awning_ids)
        #~ 
        #~ return awning_ids


#~ config_id=self.search(cr, uid, [])
        #~ config = self.browse(cr, uid,config_id, context)
        #~ dp = self.pool.get('ir.model.data').get_object(cr, uid, 'product','decimal_account')
        #~ return {'config_captacion_visitantes':round(config.unidad_tributaria,dp.digits)}
    #~ 
    #~ 
#~ 
     #~ Calcular el precio de venta de la Etiqueta
    #~ def funcion_cal_precio_venta(self,cr,uid,ids,field_name,arg,context=None):
            #~ res={}
            #~ for r in self.browse(cr,uid,ids):
                #~ res[r.id]=r.unidad_tributaria*r.cant_unid_tribut
            #~ return res
    
