# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
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

import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


            
class account_config_settings(osv.osv_memory):
    _inherit = 'account.config.settings'
    _columns = {
    
    'unidad_tributaria': fields.float('Unidad Tributaria', help="Ingrese el valor de la Unidad Tributaria "),
    }
    
    def get_default_ut(self, cr, uid,fields,context=None):
        config_id=self.search(cr, uid, [],limit=1,order="id desc")
        config = self.browse(cr, uid,config_id, context)
        #~ dp = self.pool.get('ir.model.data').get_object(cr, uid, 'product','decimal_account')
        return {'unidad_tributaria':16}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
