from django.contrib import admin
from .models import *


class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)

class MessageDescriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(MessageDescription, MessageDescriptionAdmin)

class DataUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(DataUser, DataUserAdmin)

