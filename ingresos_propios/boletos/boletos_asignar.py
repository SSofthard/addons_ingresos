# -*- coding: utf-8 -*-
##############################################################################
#

#
##############################################################################

from openerp.osv import fields, osv



class asignar_boletos (osv.osv):
     
    _name="ip.asignar.boletos"
    _inherit = ['mail.thread']
    _rec_name="producto_id"

    def cantidad_guardados_mostrar_asignar(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        for i in self.browse(cr,uid,ids):
            res[i.id]=int(i.ultimo_val_asig)+int(i.cantidad_asignar)
        return res
    
    def boletos_desde(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        for i in self.browse(cr,uid,ids):
            if i.prefijo:
                stock_boletos_obj=self.pool.get('ip.stock.boletos')
                stock_boletos_ids=stock_boletos_obj.search(cr,uid,[('producto_id','=',int(i.producto_id)),('prefijo','=',i.prefijo.upper())],limit=1,order='id desc',context=context)
                stock_boletos_datos=stock_boletos_obj.browse(cr,uid,stock_boletos_ids,context=context)
                res[i.id]=str(i.prefijo.upper())+'-'+str(i.ultimo_val_asig+1).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                for d in res[i.id]:
                    res[i.id]=d 
        return res
     
    def boletos_hasta(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        for i in self.browse(cr,uid,ids):
            if i.prefijo:
                stock_boletos_obj=self.pool.get('ip.stock.boletos')
                stock_boletos_ids=stock_boletos_obj.search(cr,uid,[('producto_id','=',int(i.producto_id)),('prefijo','=',i.prefijo.upper())],limit=1,order='id desc',context=context)
                stock_boletos_datos=stock_boletos_obj.browse(cr,uid,stock_boletos_ids,context=context)
                res[i.id]=str(i.prefijo.upper())+'-'+str(i.cantidad_asignar+i.ultimo_val_asig).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                for h in res[i.id]:
                    res[i.id]=h
        return res
    
    
        
    _columns = {
        'producto_id':fields.many2one(
                    'ip.boletos',
                    'Boleto',
                    required=True,),
        'parque_id':fields.many2one(
                    'registro_parque',
                    'Parque',
                    required=True,
                    help='Esta es el parque a asignar el boleto'),
                
        'prefijo_disp':fields.char(
                        'Boletos Disponible', 
                        type='char', 
                        readonly=True,
                        help="Prefijo y cantidad de boletos disponibles para asignar.",),
        'prefijo':fields.char(
                    'Prefijo', 
                    help="Este es el prefijo del boleto a asignar.",
                    required=True),
        'ultimo_val_asig':fields.integer(
                            'Boletos Asignados',
                            readonly=False,
                            help='Este es el ultimo boleto asignado'),
        'ultimo_valor_asig_2':fields.function(
                                cantidad_guardados_mostrar_asignar,
                                'Boletos asignados',
                                type='integer',
                                help='Este es el ultimo boleto registrado'),
        'cantidad_asignar':fields.integer(
                            'Cantidad para asignar',
                            size=10,
                            required=True,
                            help='Cantidad de boletos para asignar',
                            ),
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
        'state': fields.selection([
                    ('asignado', 'Asignado'),
                    ('despachado', 'Despachado'),
                    ('recibido', 'Recibido'),
                    ('nunca_recibido', 'Nunca Recibido'),
                    ('reenviar', 'Reenviar'),
                    ('validar', 'Validado nunca recibido'),
                    ('eliminar', 'Eliminado'),
                    ('reasignar', 'Reasignar'),
            
            ], 'Estado', readonly=True, copy=False,select=True),
    
    }

    _defaults = {
        'state': 'asignado',
        }
    
    def recibido_boleto (self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'recibido'},context=context)
        return True
        
    def eliminar_boleto_asignado (self, cr, uid, ids, context=None):
        for r in self.browse(cr,uid,ids):
            inventario_boleto_parque_obj=self.pool.get('ip.inventario.boletos.parque')
            inventario_boleto_parque_id=inventario_boleto_parque_obj.search(cr,uid,[('prefijo','=',r.prefijo.upper()),('producto_id','=',int(r.producto_id)),('parque_id','=',int(r.parque_id))])
            inventario_boleto_parque_datos=inventario_boleto_parque_obj.browse(cr,uid,inventario_boleto_parque_id,context=context)
            cantidad=inventario_boleto_parque_datos['existente']-r.cantidad_asignar
            inventario_boleto_parque_obj.write(cr, uid, inventario_boleto_parque_id, {'existente':cantidad},context=context)
            self.write(cr, uid, ids, {'state': 'eliminar'},context=context)
        return True
        
    #~ def reasignar_boleto (self, cr, uid, ids, context=None):
        #~ print ids
        #~ print ids
        #~ print ids
        #~ print ids
        #~ for r in self.browse(cr,uid,ids):
            #~ inventario_boleto_parque_id=self.search(cr,uid,[('prefijo','=',r.prefijo.upper()),('producto_id','=',int(r.producto_id)),('parque_id','=',int(r.parque_id)),('id','=',int(r.id))])
            #~ inventario_boleto_parque_datos=self.browse(cr,uid,inventario_boleto_parque_id,context=context)
            #~ print inventario_boleto_parque_id
            #~ print inventario_boleto_parque_id
            #~ print inventario_boleto_parque_datos['parque_id']
            #~ print r.parque_id
            #~ if int(inventario_boleto_parque_datos['parque_id'])!=int(r.parque_id):
                #~ if inventario_boleto_parque_datos['producto_id']==r.producto_id:
                    #~ if inventario_boleto_parque_datos['prefijo']==r.prefijo:
                        #~ if inventario_boleto_parque_datos['cantidad_asignar']==r.cantidad_asignar and inventario_boleto_parque_datos['boleto_desde']==r.boleto_desde and inventario_boleto_parque_datos['boleto_hasta']==r.boleto_hasta:
                #~ print 'hola'
                #~ print 'hola'
                #~ print 'hola'
                #~ print 'hola'
                #~ raise osv.except_osv(
                    #~ ('Error'),
                    #~ ('Para poder reasignar debe cambiar el nombre del parque'))
           
                
            
        #~ self.write(cr, uid, ids, {'state': 'recibido'},context=context)
        #~ return True
        
    def nunca_recibido_boleto (self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'nunca_recibido'},context=context)
        return True
        
    def despachar_boleto (self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'despachado'},context=context)
        return True
        
    def reenviar_boleto (self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'asignado'},context=context)
        return True
        
    def validar_nunca_recibido (self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'validar'},context=context)
        return True

    def buscar_prefijos(self,cr,uid,ids,producto_id, context=None):
        res={}
        prefijos=' '
        if producto_id:
            prefijo_list=[]
            stock_inventario_obj=self.pool.get('ip.inventario.boletos')
            stock_inventario_ids=stock_inventario_obj.search(cr,uid,[('producto_id','=',producto_id)],context=context)
            stock_inventario_datos=stock_inventario_obj.browse(cr,uid,stock_inventario_ids,context=context)
            cantidad=0
            for s in stock_inventario_datos:
                prefijo_list.append(str(s.prefijo)+'='+str(s.existente))
            for p in prefijo_list:
                prefijos=prefijos+' '+p
            res={
                'prefijo_disp':prefijos,
                'prefijo':'',
                'ultimo_valor_asig_2':'',
                'ultimo_val_asig':'',
                'cantidad_asignar':'',
                'boleto_desde':'',
                'boleto_hasta':'',
                'boleto_desde_2':'',
                'boleto_hasta_2':'' ,
                }
        return {'value':res}
    
    def cantidad_guardados(self,cr,uid,ids,producto_id,prefijo,context=None):
        res={}
        if isinstance(ids,(int,long)):
            ids=[ids]
        if prefijo:
            boletos_asig_id=self.search(cr,uid,[('producto_id','=',producto_id),('prefijo','=',prefijo.upper())],limit=1,order='id desc',context=context)
            boleto_asig=self.browse(cr,uid,boletos_asig_id,context=context)
           
            res={
                'ultimo_valor_asig_2':boleto_asig['ultimo_valor_asig_2'],
                'ultimo_val_asig':boleto_asig['ultimo_val_asig']+boleto_asig['cantidad_asignar'],
                   
                }                        
        else:
            res={
                'ultimo_valor_asig_2':'',
                'ultimo_val_asig':'',
                'cantidad_digitos':'',
                'cantidad_asignar':'',
                'boleto_desde':'',
                'boleto_hasta':'',
                'boleto_desde_2':'',
                'boleto_hasta_2':'' ,
                }
        return {'value':res,}
    
    
    def cantidad_asigna(self,cr,uid,ids,producto_id,cantidad_asignar,prefijo,ultimo_val_asig,context=None):
        if isinstance(ids,(int,long)):
            ids=[ids]
        res={}
        if prefijo:
            
            stock_boletos_obj=self.pool.get('ip.stock.boletos')
            stock_boletos_ids=stock_boletos_obj.search(cr,uid,[('producto_id','=',producto_id),('prefijo','=',prefijo.upper())],limit=1,order='id desc',context=context)
            stock_boletos_datos=stock_boletos_obj.browse(cr,uid,stock_boletos_ids,context=context)
            stock_inventario_obj=self.pool.get('ip.inventario.boletos')
            stock_inventario_ids=stock_inventario_obj.search(cr,uid,[('producto_id','=',producto_id),('prefijo','=',prefijo.upper())],context=context)
            stock_inventario_datos=stock_inventario_obj.browse(cr,uid,stock_inventario_ids,context=context)
            for i in stock_inventario_datos:
                if prefijo.upper() and cantidad_asignar:
                    if i.existente>=cantidad_asignar:
                        cantidad_asignar=cantidad_asignar+ultimo_val_asig
                        ultimo_val_asig=ultimo_val_asig+1
                        res={
                        'boleto_desde':str(prefijo.upper())+'-'+str(ultimo_val_asig).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                        'boleto_hasta':str(prefijo.upper())+'-'+str(cantidad_asignar).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                        'boleto_desde_2':str(prefijo.upper())+'-'+str(ultimo_val_asig).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                        'boleto_hasta_2': str(prefijo.upper())+'-'+str(cantidad_asignar).rjust(stock_boletos_datos['cantidad_digitos'],'0'),
                        }
                    else:
                        raise osv.except_osv(('Error !'), ('Cantidad de Boletos con el prefijo '+prefijo.upper()+ ' no disponible'))
        return {
            'value':res,
            }
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'prefijo':vals['prefijo'].upper()
                })
        inventario_boleto_val=[]
        inventario_boleto_obj=self.pool.get('ip.inventario.boletos')
        inventario_boleto_id=inventario_boleto_obj.search(cr,uid,[('prefijo','=',vals['prefijo']),('producto_id','=',vals['producto_id'])])
        inventario_boleto_datos=inventario_boleto_obj.browse(cr,uid,inventario_boleto_id,context=context)
        if vals['cantidad_asignar']<=0:
            raise osv.except_osv(
                    ('Error'),
                    ('La cantidad no puede ser menor a uno.'))
        elif vals['cantidad_asignar']>inventario_boleto_datos['existente']:
            raise osv.except_osv(
                ('Error de cantidad'),
                ('La cantidad de boletos con el prefijo '+vals['prefijo'].upper()+' no esta disponible.'))	
        else:       
            inventario_boleto_data=inventario_boleto_obj.browse(cr,uid,inventario_boleto_id)
            inventario_boleto_val={
                'existente':inventario_boleto_data['existente']-vals['cantidad_asignar'],
                }
            inventario_boleto_obj.write(cr, uid,inventario_boleto_id, inventario_boleto_val)
        inventario_boleto_parque_obj=self.pool.get('ip.inventario.boletos.parque')
        inventario_boleto_parque_id=inventario_boleto_parque_obj.search(cr,uid,[('prefijo','=',vals['prefijo']),('producto_id','=',vals['producto_id']),('parque_id','=',vals['parque_id'])])
        inventario_boleto_parque_datos=inventario_boleto_parque_obj.browse(cr,uid,inventario_boleto_parque_id,context=context)
        if len(inventario_boleto_parque_id)==0:
            inventario_boleto_val={
                'producto_id':vals['producto_id'],
                'parque_id':vals['parque_id'],
                'prefijo':vals['prefijo'],
                'existente':vals['cantidad_asignar']
                }
            inventario_boleto_parque_obj.create(cr, uid, inventario_boleto_val, context=context)
        else:
            inventario_boleto_val={
                'existente':vals['cantidad_asignar']+inventario_boleto_parque_datos['existente'],
                }
            inventario_boleto_parque_obj.write(cr, uid,inventario_boleto_parque_id, inventario_boleto_val)
        return super(asignar_boletos, self).create(cr, uid, vals, context=context)


class inventerio_boleto_parque(osv.osv):
    _name='ip.inventario.boletos.parque'
    _rec_name="parque_id"
    _columns = {
        'producto_id':fields.many2one(
                    'ip.boletos',
                    'Boleto'),
        'parque_id':fields.many2one(
                    'registro_parque',
                    'Parque',
                    required=True,
                    help='Esta es el parque'),
        'prefijo':fields.char(
                    'Prefijo', 
                    help="Este es el prefijo del boleto a asignar.",
                    required=True),
        
        'existente':fields.integer(
                    'Inventario',
                    readonly=False,
                help='Esta es la cantidad total de boletos en inventario'),
            }
            



    
    
    
    
    
    
    
    
