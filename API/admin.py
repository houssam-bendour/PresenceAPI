from django.contrib import admin
from .models import *

# Optionnel: Personnaliser l'affichage des modèles dans l'admin

class UserAdmin(admin.ModelAdmin):
    list_display = ['email','rfid', 'CNE','id','first_name','last_name','username' ,'password', 'user_type','is_superuser','is_staff']
    search_fields = ['email']
    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'id','prof_id']
    search_fields = ['name']

class PresenceAdmin(admin.ModelAdmin):
    list_display = ['id','student_id','session_id','pointing']
    search_fields = ['student_id', 'session_id']

class InscrireAdmin(admin.ModelAdmin):
    list_display = ['student_id','module_id']
    search_fields = ['student_id', 'module_id']

class SessionAdmin(admin.ModelAdmin):
    list_display = ['titre','prof_id','date','start_time','end_time','module_id','id','discreption']
    search_fields = ['titre', 'id','date']

class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'CNE','email','first_name','last_name','seances_ratees','new_seances']
    search_fields = ['id', 'CNE','first_name']

# Enregistrer vos modèles ici
# admin.site.register(User)  # Si vous souhaitez inclure User sans personnalisation spécifique
admin.site.register(User, UserAdmin)
admin.site.register(StudentInfo, StudentInfoAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Presence, PresenceAdmin)
admin.site.register(Inscrire, InscrireAdmin)
admin.site.register(Session, SessionAdmin)
