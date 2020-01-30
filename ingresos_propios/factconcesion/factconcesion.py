# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
class facturas_por_generara(osv.osv):
    """Registro de los Parques"""
    _name = 'conc.facturas.por.generara'
    _rec_name= 'nombre'
    _columns = {
        'concesion_id': fields.many2one(
                'concesiones', 
                'Concesión',
                help='Nombre de la Concesión que se Genera la Factura'),
        'estado': fields.selection([
                ('por_generar', 'Por Generar'), 
                ('vencida', 'Vencida'), 
                ('generada', 'Generada'), 
                ('canclada', 'Cancelada'),
                ('pagada', 'Pagada')], 
                'Estado',
                help='Estado que se encuentra la Factura'),
        'nombre': fields.char(
                'Nombre', 
                size=100, 
                help='Nombre de la Factura que se Genero'),
        'account_invoice_id': fields.integer('Relacion de la Factura con la Concesion'),
        'ut_id': fields.char(
                'Valor de la UT', 
                size=100, 
                help='Valor de la Unidad Tributaria Actual'),
        'pago_mensual': fields.char(
                'Pago de la UT Mensual', 
                size=100, 
                help='Cantidad de Unidades Tributarias a Cancelar'),
        'total_pagar': fields.char(
                'Total a Cancelar', 
                size=100, 
                help='Pago Mensual de la Factura del Mes'),
        'fecha_facturar': fields.date(
                'Fecha ', 
                required=True, 
                help='Feha de la Factura'),
    }
    _defaults = {
        'estado': 'por_generar',
    }
