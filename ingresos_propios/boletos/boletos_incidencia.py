    # -*- coding: utf-8 -*-
##############################################################################
#

#
##############################################################################

from openerp.osv import fields, osv


class incidencia_boletos(osv.osv):
    
    def boletos_desde(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        for i in self.browse(cr,uid,ids):
            stock_boletos_obj=self.pool.get('ip.stock.boletos')
            stock_boletos_ids=stock_boletos_obj.search(cr,uid,[('producto_id','=',int(i.producto_id)),('prefijo','=',i.prefijo.upper())],limit=1,order='id desc',context=context)
            stock_boletos_datos=stock_boletos_obj.browse(cr,uid,stock_boletos_ids,context=context)
            res[i.id]=str(i.prefijo.upper())+'-'+str(i.cantidad_desde).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
            for d in res[i.id]:
                res[i.id]=d
        return res
        
    def boletos_hasta(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        for i in self.browse(cr,uid,ids):
            stock_boletos_obj=self.pool.get('ip.stock.boletos')
            stock_boletos_ids=stock_boletos_obj.search(cr,uid,[('producto_id','=',int(i.producto_id)),('prefijo','=',i.prefijo.upper())],limit=1,order='id desc',context=context)
            stock_boletos_datos=stock_boletos_obj.browse(cr,uid,stock_boletos_ids,context=context)
            res[i.id]=str(i.prefijo.upper())+'-'+str(i.cantidad_hasta).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
            for h in res[i.id]:
                res[i.id]=h
        return res
     
    _name="ip.incidencia.boletos"
    _inherit = ['mail.thread']
    _rec_name="producto_id"
    _description="Incidencia de los Boletos"

        
    _columns = {
        'producto_id':fields.many2one(
                    'ip.boletos',
                    'Boleto',
                    required=True,),
        'parque_id':fields.many2one(
                    'registro_parque',
                    'Parque',
                    required=True,
                    help='Esta es el parque que reportara la incidencia'),
        'prefijo':fields.char(
                    'Prefijo', 
                    help="Este es el prefijo del boleto a reportar.",
                    required=True),
        'cantidad_desde':fields.integer(
                            'Desde',
                            readonly=False,
                            required=True,),
        'cantidad_hasta':fields.integer(
                            'Hasta',
                            readonly=False,
                            required=True,),
        'boleto_desde':fields.char(
                'Desde',
                size=10,
                readonly=False,),
        'boleto_desde_2':fields.function(
                boletos_desde,
                'Desde',
                type='char',
                ),
        'boleto_hasta':fields.char(
                'Hasta',
                size=10,
                readonly=False,),
        'boleto_hasta_2':fields.function(
                boletos_hasta,
                'Hasta',
                type='char',
                ),
        'incidencia':fields.selection([
                    ('deteriorado', 'Deteriorado'),
                    ('extraviado', 'Extraviado'),
                    ('otro', 'Otro')], 'Incidencia',
                    required=True,),
        'descripcion':fields.text('Descripción',
                        required=True,),
        'state': fields.selection([
                    ('reportado', 'Reportado'),
                    ('validar', 'Validado'),
                    ('negado', 'Negado'),
                    ], 'Estado', readonly=True, copy=False,select=True),
    }

    _defaults = {
        'incidencia': '',
        'state':'reportado'
        }
        
    def validar_prefijo (self,cr,uid,ids,producto_id,parque_id,prefijo,context=None):
        if prefijo:
            asignar_boleto_obj=self.pool.get('ip.asignar.boletos')
            asignar_boleto_id=asignar_boleto_obj.search(cr,uid,[('producto_id','=',producto_id),('parque_id','=',parque_id),('prefijo','=',prefijo.upper())],limit=1,order='id desc',context=context)
            asignar_boleto_datos=asignar_boleto_obj.browse(cr,uid,asignar_boleto_id,context=context)
            if len (asignar_boleto_id)==0:
                raise osv.except_osv(
                                ('Error de prefijo'),
                                ('El prefijo '+prefijo.upper()+' no esta asignado al parque.'))
        return True
    
    def reportar_boleto(self,cr,uid,ids,producto_id,prefijo,cantidad_desde,cantidad_hasta,context=None):
        res={}
        if prefijo and cantidad_desde and cantidad_hasta:
            if cantidad_hasta>=cantidad_desde:
                stock_boletos_obj=self.pool.get('ip.stock.boletos')
                stock_boletos_ids=stock_boletos_obj.search(cr,uid,[('producto_id','=',producto_id),('prefijo','=',prefijo.upper())],limit=1,order='id desc',context=context)
                stock_boletos_datos=stock_boletos_obj.browse(cr,uid,stock_boletos_ids,context=context)
                res={
                    'boleto_desde':str(prefijo.upper())+'-'+str(cantidad_desde).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                    'boleto_hasta':str(prefijo.upper())+'-'+str(cantidad_hasta).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                    'boleto_desde_2':str(prefijo.upper())+'-'+str(cantidad_desde).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                    'boleto_hasta_2':str(prefijo.upper())+'-'+str(cantidad_hasta).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                    }
            else:
                raise osv.except_osv(
                                ('Error '),
                                ('La cantidad final no puede ser menor a la cantidad inicial'))
        else:
            res={
                'cantidad_hasta':'',
                }
        return {
            'value':res
            }
    def validar_incidencia (self, cr, uid, ids, context=None):
        for r in self.browse(cr,uid,ids):
            inventario_boletos_parque_obj=self.pool.get('ip.inventario.boletos.parque')
            inventario_boletos_parque_ids=inventario_boletos_parque_obj.search(cr,uid,[('producto_id','=',int(r.producto_id)),('parque_id','=',int(r.parque_id)),('prefijo','=',r.prefijo.upper())],context=context)
            inventario_boletos_parque_datos=inventario_boletos_parque_obj.browse(cr,uid,inventario_boletos_parque_ids,context=context)
            cant_report=r.cantidad_hasta-r.cantidad_desde+1
            cantidad=inventario_boletos_parque_datos['existente']-cant_report
            inventario_boletos_parque_obj.write(cr, uid, inventario_boletos_parque_ids, {'existente': cantidad},context=context)
            self.write(cr, uid, ids, {'state': 'validar'},context=context)
        return True
   
    def negar_incidencia (self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'negado'},context=context)
        return True
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'prefijo':vals['prefijo'].upper()
                })
        asignar_boleto_obj=self.pool.get('ip.asignar.boletos')
        asignar_boleto_id=asignar_boleto_obj.search(cr,uid,[('producto_id','=',vals['producto_id']),('parque_id','=',vals['parque_id']),('prefijo','=',vals['prefijo'].upper())],context=context)
        if vals['prefijo']:
            if len (asignar_boleto_id)==0:
                raise osv.except_osv(
                                ('Error de prefijo'),
                                ('El prefijo '+vals['prefijo'].upper()+' no esta asignado al parque.'))
            if vals['cantidad_hasta']<vals['cantidad_desde']:
                raise osv.except_osv(
                                ('Error '),
                                ('La cantidad final no puede ser menor a la cantidad inicial'))
        lis_rango=[]
        boleto_incidencia_ids=self.search(cr,uid,[('producto_id','=',vals['producto_id']),('parque_id','=',vals['parque_id']),('prefijo','=',vals['prefijo'].upper())],context=context)
        print boleto_incidencia_ids
        print boleto_incidencia_ids
        print boleto_incidencia_ids
        print boleto_incidencia_ids
        list_rango=[]
        for i in self.browse(cr,uid,boleto_incidencia_ids,context=context):
            print 'hola'
            print 'hola'
            print 'hola'
            if (int(i.cantidad_desde) <= vals['cantidad_desde'] and int(i.cantidad_hasta)>=vals['cantidad_hasta']) or (int(i.cantidad_desde) >= vals['cantidad_desde'] and int(i.cantidad_hasta)<=vals['cantidad_desde'] ) or (int(i.cantidad_hasta)<=vals['cantidad_hasta'] and int(i.cantidad_hasta)>=vals['cantidad_desde']):
                list_rango.append(str(i.cantidad_desde)+'-'+str(i.cantidad_hasta))
                print list_rango
                print list_rango
                print list_rango
        if len(list_rango)>=1:
            raise osv.except_osv(
                                ('Error'),
                                ('Las cantidades ingresadas se encuentran dentro del rango de boletos ya reportados por el parque '))
           
        for r in asignar_boleto_obj.browse(cr,uid,asignar_boleto_id,context=context):
            p,d=r.boleto_desde.split('-')
            l,h=r.boleto_hasta.split('-')
            if int(d) <= vals['cantidad_desde'] and int(h)>=vals['cantidad_hasta']:
                    lis_rango.append(d+'-'+h)
        if len(lis_rango)==0:
            raise osv.except_osv(
                                ('Error'),
                                ('Las cantidades ingresadas no estan en el rango de boletos asignados al parque '))
        return super(incidencia_boletos, self).create(cr, uid, vals, context=context)
 
