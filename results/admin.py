from django.contrib import admin
from .models import Result
# from quizes.models import Region, Filial, School
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources, widgets
from django.contrib.admin import SimpleListFilter

class ResultFilter(SimpleListFilter):
    title = 'Region' # or use _('country') for translated title
    parameter_name = 'region'

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            ("myFilial", "MyFilial"),
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        if self.value() == "filial":
            # Get websites that have at least one page.
            #TODO добавить фильты по филалу которому пренадлежит этот результат
            return queryset.distinct().filter(region__isnull=False)
        if self.value():
            # Get websites that don't have any pages.
            return queryset.distinct().filter(region__isnull=True)

class ResultResource(resources.ModelResource):
    class Meta:
        model = Result

class ResulNameResource(resources.ModelResource):
    class Meta:
        model = Result
        fields = ['id', 'quiz', 'user', 'score']
        export_order = ('id', 'quiz', 'user', 'score')

class ResultAdmin(ImportExportModelAdmin):
    # list_filter = [ResultFilter]
    resource_classes = [ResultResource, ResulNameResource]
    search_fields = ('region', 'school', 'class_name')
    list_display = ('region', 'school', 'class_name', 'quiz', 'user_first_name', 'score', 'created')
    
    def user_first_name(self, obj):
        return obj.user.first_name + " " +obj.user.last_name

admin.site.register(Result, ResultAdmin)
