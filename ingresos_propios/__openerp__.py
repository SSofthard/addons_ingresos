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
{
        "name" : "Ingresos Propios",
        "version" : "0.3",
        "author" : "Victor Davila",
        "website" : "http://inparques.gov.ve",
        "category" : "Unknown",
        "description":  """
    Registro del Primer Modulo de Ingresos Propios
    
        Registro de Parques 
        
        Registro de Regiones
        
        Registro de Ambitos
        
        Registro de Tipo de Parques 
        
        Registro de Configuraciones de Formularios
    """,
        "depends" : ['base_setup','product','sale','stock','unidad_tributaria','account_numero_pago','conversion_letras','account_journal'],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : [ ],
        "data" : [
         'data/redi.xml',
         'data/estados.xml',
         'data/municipios.xml',
         'data/parroquias.xml',
         'data/cod_concesion_data.xml',
         'data/autorizacion_sequence.xml',
         'data/requisitos_data.xml',
         'data/canon_sequence.xml',
         'data/punto_cuenta_secuence.xml',
         'data/config_telecomunicacion.xml',
         'data/infraestructura.xml',
         'data/alcance.xml',
         'data/punto_cuenta_telecom_sequence.xml',
         'data/canon_telecom_sequence.xml',
         'cargos/cargos_view.xml',
         'partner/partner_view.xml',
         'ingresos_propios_view.xml',
         'report/carta_aceptacion.xml',
         'views/carta_aceptacion_template.xml',
         'factconcesion/factconcesion_view.xml',
         'embarcacion/embarcacion_view.xml',
         'embarcacion/etiqueta_view.xml',
         'embarcacion/asignar_etiqueta_view.xml',
         'embarcacion/generar_etiqueta_view.xml',
         'embarcacion/marinas_view.xml',
         'punto_cuenta/punto_cuenta_view.xml',
         'punto_cuenta/views/punto_cuenta_template.xml',
         'report/punto_cuenta_report.xml',
         'autorizacion/views/autorizacion_view.xml',
         'autorizacion/views/autorizacion_template.xml',
         'autorizacion/report/autorizacion_report.xml',
         'boletos/boletos_view.xml',
         'boletos/stock_boletos_view.xml',
         'boletos/boletos_asignar_view.xml',
         'boletos/boletos_incidencia_view.xml',
         'boletos/rendicion_boletos_view.xml',
         'promedio_visitante/promedio_visitantes_view.xml',
         'requisitos/requisitos_view.xml',
         'config_captacion_visitantes/config_captacion_visitantes_view.xml',
         'config_ingresos_brutos/config_ingresos_brutos_view.xml',
         'confg_max_min/max_min_view.xml',
         #~ 'canon/canon_view.xml',
         'puesto_control_vigilancia/puesto_control_vigilancia_view.xml',
         'pago_especie/pago_especie_concesion_view.xml',
         'voucher_parque/voucher_parque.xml',
         'wizard/rendicion_general_wizard.xml',
         'report/rendicion_general_report.xml',
         'views/rendicion_general1_template.xml',
         'productos_varios/productos_varios_view.xml',
         'productos_varios/rendicion_varios_view.xml',
         'estacion_parque/estacion_parques_view.xml',
         'config_puntocuenta_telecomunicacion/punto_cuenta_telecom_view.xml',
         'config_telecomunicacion/confg_telecom_view.xml',
         'security/ir.model.access.csv',
         'security/ingresos_propios_roles.xml',
         'boletos/security/per_director_ingresos_propios/ir.model.access.csv',
        ],
        "installable": True
}
