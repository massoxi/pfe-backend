from django.contrib import admin
from .models import Protocole, Temoin, Medicin, Victime, Cas, Cas_F, Cas_N, Signes_N, Signes_F, Message

class MedecinAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'username')
    list_display = ('first_name', 'last_name', 'username')

class TemoinAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'username')
    list_display = ('first_name', 'last_name', 'username')


class MessageAdmin(admin.ModelAdmin):
    fields = ('expediteur', 'destinateur', 'contenu', 'date', 'diffusion')
    list_display = ('contenu', 'date', 'expediteur', 'destinateur', 'diffusion')

class ProtocoleAdmin(admin.ModelAdmin):
    list_display = ('type', 'cas_precis', 'img')

admin.site.register(Temoin, TemoinAdmin)
admin.site.register(Medicin, MedecinAdmin)
admin.site.register(Victime)
admin.site.register(Cas)
admin.site.register(Cas_N)
admin.site.register(Cas_F)
admin.site.register(Signes_N)
admin.site.register(Signes_F)
admin.site.register(Message, MessageAdmin)
admin.site.register(Protocole, ProtocoleAdmin)