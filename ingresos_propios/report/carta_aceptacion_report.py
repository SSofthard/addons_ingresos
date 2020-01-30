# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#    Copyright (C) 2004 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from openerp.osv import osv
import time
from openerp.report import report_sxw

class carta_aceptacion_report(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(carta_aceptacion_report,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,

        })
        self.context = context
        


class report_carta_aceptacion(osv.AbstractModel):
    _name = "ingresos_propios.report.id_carta_aceptacion"
    _inherit = "report.abstract_report"
    _template = "ingresos_propios.id_carta_aceptacion"
    _wrapped_report_class = carta_aceptacion_report    
# report_sxw.report_sxw('ingresos_propios', 'concesiones', 'local_addons/ingresos_propios/report/carta_aceptacion.rml', parser=carta_aceptacion_report)

