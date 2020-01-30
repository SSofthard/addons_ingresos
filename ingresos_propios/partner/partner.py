# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
ADDRESS_FIELDS = ('estado_id', 'municipio_id', 'parroquia_id')
class partner(osv.osv):
    """Registro de laas Personas y Empresas"""
    _name = 'res.partner'
    _inherit="res.partner"
    
    def open_parent2(self, cr, uid, ids, context=None):
        """ Utility method used to add an "Open Parent" button in partner views """
        partner = self.browse(cr, uid, ids[0], context=context)
        return {'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': partner.parent_id.id,
                'target': 'new',
                'flags': {'form': {'action_buttons': True}}}
   
    _columns = {
        'rif': fields.char('RIF',
                size=20, 
                required=True, 
                help='Numero del RIF de la Persona Natural o Juridica que se va a Registrar'
                ),
        'correo': fields.char('Correo', 
                size=50, 
                help='Correo Electronico de la Persona Natural o Juridica que se va a Registrar'
                ),
        'objeto': fields.text('Objeto', 
                    required=True, 
                    help='Objeto de la Persona Natural o Juridica que se va a Registrar'
                    ),
        'redi_id': fields.many2one('redi', 
                    'REDI', 
                    help='Region Estrategica de Defensa Integral'
                    ),
        'estado_id': fields.many2one('estados', 
                    'Estado', 
                    help='Estado que pertenece la Persona Natural o Juridica que se va a Registrar'
                    ),
        'municipio_id': fields.many2one('municipios', 
                        'Municipio', 
                        help='Municipio que pertenece la Persona Natural o Juridica que se va a Registrar'
                        ),
        'parroquia_id': fields.many2one('parroquias', 
                        'Parroquia', 
                        help='Parroquia que pertenece la Persona Natural o Juridica que se va a Registrar'
                        ),
        'partner_id': fields.many2one('res.partner', 
                        'Parner', 
                        ondelete="cascade", 
                        required=True
                        ),
        'sector': fields.char('Sector', 
                        size=50, 
                        help='Sector de la Persona Natural o Juridica que se va a Registrar'
                        ),
        'referencia': fields.char('Punto de Referencia', 
                        size=100, 
                        help='Punto de Referencia  que pertenece la Persona Natural o Juridica que se va a Registrar'
                        ),
        'telefonos_ids': fields.one2many('telefono_jur_nat', 
                        'juridico_natural_id', 
                        'Telefonos', 
                        help='Relacion de la Persona Natura o Juridica con los Tlefonos'
                        ),
        'documentos_ids': fields.one2many('documentos_cliente', 
                        'cliente_id', 
                        'Documentos', 
                        help='Relacion de la Persona Natura o Juridica con los Documentos'
                        ),
    }
    
class documentos_cliente(osv.osv):
    """Registro de Documentos"""
    _name = 'documentos_cliente'
    _rec_name = 'nombre'
    
    _columns = {
        'cliente_id': fields.many2one('res.partner', 'Empresa/Persona', help='Documentos que posee la Persona Natural o Juridica: RIF, Solvencias, etc'),
        'nombre': fields.char('Nombre del Documento', size=100, required=True, help='Nombre que posee el Documento'),
        'descripcion': fields.text('Descripcion', size=200, help='Descripcion del Documento'),
        'fecha_exp': fields.date('Fecha de Expedicion', required=True, help='Fecha de Expedicion que posee el Documento'),
        'fecha_venc': fields.date('Fecha de Venciemiento', help='Fecha de Vencimiento del Documento '),
    }
    
    
