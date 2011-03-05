from django.contrib import admin
from bom.models import Supplier, PartType, PartSubType, Part, Order, Board, PartLine

class PartSubTypeAdmin(admin.ModelAdmin):
	list_display = ('type', 'name')

class PartAdmin(admin.ModelAdmin):
	list_display = ('type', 'subtype', 'value', 'desc', 'package', 'mfr', 'pn', 'price', 'minQty', 'supplier')
	search_fields = ('supplier', 'pn', 'type', 'subtype', 'value', 'desc', 'package', 'mfr', 'comment')
	list_filter = ('type', 'subtype', 'package')

class BoardAdmin(admin.ModelAdmin):
	list_display = ('pn', 'rev', 'desc', 'created')
	
class OrderAdmin(admin.ModelAdmin):
	list_display = ('created',  'supplier', 'comment')
	
admin.site.register(Supplier)
admin.site.register(PartType)
admin.site.register(PartSubType, PartSubTypeAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PartLine)