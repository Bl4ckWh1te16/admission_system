from django.contrib import admin
from .models import Applicant, EducationProgram, Application

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'phone', 'email')
    search_fields = ('full_name', 'phone', 'email')
    list_filter = ('gender', 'created_at')

@admin.register(EducationProgram)
class EducationProgramAdmin(admin.ModelAdmin):
    list_display = (
        'code', 
        'name', 
        'level_display',
        'duration',
        'budget_places', 
        'paid_places',
        'tuition_fee_display',
        'created_at'
    )
    list_filter = ('level', 'created_at')
    search_fields = ('name', 'code')
    list_editable = ('budget_places', 'paid_places')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'code', 'level', 'description', 'duration')
        }),
        ('Места и стоимость', {
            'fields': ('budget_places', 'paid_places', 'tuition_fee'),
            'classes': ('collapse',)
        }),
    )
    
    def level_display(self, obj):
        return obj.get_level_display()
    level_display.short_description = 'Уровень'
    
    def tuition_fee_display(self, obj):
        if obj.tuition_fee:
            return f"{obj.tuition_fee:,.2f} ₽"
        return "-"
    tuition_fee_display.short_description = 'Стоимость'
    
    def save_model(self, request, obj, form, change):
        # Автоматически устанавливаем стоимость для платных мест
        if obj.paid_places > 0 and not obj.tuition_fee:
            # Здесь можно добавить логику расчета стоимости
            obj.tuition_fee = 150000.00  # Пример значения по умолчанию
        super().save_model(request, obj, form, change)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'program', 'status', 'application_date')
    list_filter = ('status', 'program')
    search_fields = ('applicant__full_name', 'program__name')
    raw_id_fields = ('applicant', 'program')