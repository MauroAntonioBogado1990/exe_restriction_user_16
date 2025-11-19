from odoo import models
from odoo.exceptions import AccessError

# Inventario
class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    def search(self, args, **kwargs):
        if self.env.user.has_group('exe_restriction_user_16.group_no_permission'):
            raise AccessError("No tenés permiso para ver Inventario.")
        return super().search(args, **kwargs)

# Fabricación
class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def search(self, args, **kwargs):
        if self.env.user.has_group('exe_restriction_user_16.group_no_permission'):
            raise AccessError("No tenés permiso para ver Fabricación.")
        return super().search(args, **kwargs)

# Empleadosgt
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def search(self, args, **kwargs):
        if self.env.user.has_group('exe_restriction_user_16.group_no_permission'):
            raise AccessError("No tenés permiso para ver Empleados.")
        return super().search(args, **kwargs)

# Sitio Web (ajustado para evitar romper vistas públicas)
class Website(models.Model):
    _inherit = 'website'

    def search(self, args, **kwargs):
        if self.env.user.has_group('exe_restriction_user_16.group_no_permission'):
            # Mostrar solo el sitio web principal (o ninguno si querés ocultar todo)
            args = [('id', '=', -1)] + args  # dominio siempre falso
        return super().search(args, **kwargs)
#esta es una opcion para poder mostrar que no tiene permisos

# ---------------------------------------------------------
# RESTRICCIÓN PARA TABLEROS (DASHBOARDS)
# ---------------------------------------------------------
class SpreadsheetDashboard(models.Model):
    # Este es el modelo que se ve en tu captura de pantalla (Tableros)
    _inherit = 'spreadsheet.dashboard'

    def search(self, args, **kwargs):
        if self._is_restricted():
            raise AccessError("No tenés permiso para ver los Tableros.")
        return super(SpreadsheetDashboard, self).search(args, **kwargs)

    def read(self, fields=None, load='_classic_read'):
        if self._is_restricted():
            raise AccessError("No tenés permiso para ver los Tableros.")
        return super(SpreadsheetDashboard, self).read(fields, load)

    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if self._is_restricted():
            raise AccessError("No tenés permiso para ver los Tableros.")
        return super(SpreadsheetDashboard, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    def _is_restricted(self):
        # Verificamos si el usuario pertenece al grupo restringido y no es superusuario
        return (
            self.env.user.has_group('exe_restriction_user_16.group_no_permission')
            and not self.env.is_superuser
        )




# Tableros: devolver conjunto vacío para usuarios restringidos
# (no levantar AccessError para no romper vistas que esperan recordsets)

class Board(models.AbstractModel):
    _inherit = 'board.board'

    def _is_restricted_user(self):
        return self.env.user.has_group('exe_restriction_user.group_no_permission')

    def search(self, args=None, **kwargs):
        if self._is_restricted_user():
            raise AccessError("No tenés permiso para ver Tableros.")
        return super().search(args or [], **kwargs)

    def read(self, fields=None, load='_classic_read'):
        if self._is_restricted_user():
            raise AccessError("No tenés permiso para ver Tableros.")
        return super().read(fields, load)

    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if self._is_restricted_user():
            raise AccessError("No tenés permiso para ver Tableros.")
        return super().read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

# Aplicaciones (Apps)
class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def search(self, args, **kwargs):
        if self._is_restricted():
            raise AccessError("No tenés permiso para ver Aplicaciones.")
        return super().search(args, **kwargs)

    def read(self, fields=None, load='_classic_read'):
        if self._is_restricted():
            raise AccessError("No tenés permiso para ver Aplicaciones.")
        return super().read(fields, load)

    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if self._is_restricted():
            raise AccessError("No tenés permiso para ver Aplicaciones.")
        return super().read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    def _is_restricted(self):
        return (
            self.env.user.has_group('exe_restriction_user_16.group_no_permission')
            and not self.env.context.get('frontend_asset_loading')
            and not self.env.context.get('website_id')
            and not self.env.is_superuser
        )
    

#en sale.order solo puede ver sus presupuestos y pedidos
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def search(self, args, **kwargs):
        if self.env.user.has_group('exe_restriction_user_16.group_no_permission'):
            # Mostrar solo los presupuestos creados por el usuario actual
            domain = [('create_uid', '=', self.env.uid)]
            args = domain + args
        return super().search(args, **kwargs)
