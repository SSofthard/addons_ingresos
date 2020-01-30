# -*- coding: utf-8 -*-


from openerp.osv import fields,osv
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import *


class promedio_visitantes(osv.osv):
    _name="promedio_visitantes"
    _rec_name="parque_id"
    
    def _get_selection(self, cursor, user_id, context=None):
        format="%Y"
        hoy=date.today()
        ant2=hoy+relativedelta(years=-2)
        ant=hoy+relativedelta(years=-1)
        prox=hoy+relativedelta(years=+1)
        ant2=ant2.strftime(format)
        ant=ant.strftime(format)
        hoy=hoy.strftime(format)
        prox=prox.strftime(format)
        return (
            (ant2,ant2),
            (ant,ant),
            (hoy,hoy),
            (prox,prox))
 
    def _get_selection(self, cursor, user_id, context=None):
        format="%Y"
        hoy=date.today()
        ant5=hoy-relativedelta(years=+5)
        ant4=hoy+relativedelta(years=-4)
        ant3=hoy+relativedelta(years=-3)
        ant2=hoy+relativedelta(years=-2)
        ant1=hoy+relativedelta(years=-1)
        ant5=ant5.strftime(format)
        ant4=ant4.strftime(format)
        ant3=ant3.strftime(format)
        ant2=ant2.strftime(format)
        ant1=ant1.strftime(format)
        hoy=hoy.strftime(format)
        return (
            (ant5,ant5),
            (ant4,ant4),
            (ant3,ant3),
            (ant2,ant2),
            (ant1,ant1),
            (hoy,hoy),)
            
    def function_total(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        for i in self.browse(cr,uid,ids):
            if (i.menor_edad or i.adultos or i.tercera_edad):
                resultado=0
                resultado= int(i.menor_edad)+int(i.adultos)+int(i.tercera_edad)
                res[i.id]=resultado 
        return res
            
            
    _columns={
        
            'parque_id': fields.many2one('registro_parque', 'Seleccione Parque',size=10, required=True, help='Seleccione el parque.'),
            'mes':fields.selection([('Enero','ENERO'),
                                    ('Febrero','FEBRERO'),
                                    ('Marzo','MARZO'),
                                    ('Abril','ABRIL'),
                                    ('Mayo','MAYO'),
                                    ('Junio','JUNIO'),
                                    ('Julio','JULIO'),
                                    ('Agosto','AGOSTO'),
                                    ('Septiembre','SEPTIEMBRE'),
                                    ('Octubre','OCTUBRE'),
                                    ('Noviembre','NOVIEMBRE'),
                                    ('Diciembre','DICIEMBRE')],
                                    'Mes',required=True, help='Indique el mes en que desea realizar el promedio' ),
            'anio':fields.selection(_get_selection,'Año',required=True),
            'menor_edad':fields.integer('Menores de edad:',size=10,required=False,help='Ingrese la cantidad de menores de edad que visitaron el parque en la fecha indicada'),
            'adultos':fields.integer('Adultos',required=False,help='Ingrese la cantidad de adultos que visitaron el parque en la fecha indicada'),
            'tercera_edad':fields.integer('Adultos Mayor',size=10,required=False,help='Ingrese la cantidad de personas de la tercera edad  que visitaron el parque en la fecha indicada'),
            'total_function':fields.function(function_total,'Total', type='integer', store=True),
            }

    _sql_constraints = [
        ('mes_uniq', 'unique(mes, parque_id, anio)', 'El Mes, el Año y el Parque Seleccionado ya fueron Registrados Verifique!!!'),
    ]
    
    def total_visitantes(self,cr,uid,ids,menor_edad,adultos,tercera_edad,context=None):
        res={}
        if (menor_edad or adultos or tercera_edad):
            resultado=0
            resultado= int(menor_edad)+int(adultos)+int(tercera_edad)
            res['total_function']=resultado
            return {'value':res}
            
