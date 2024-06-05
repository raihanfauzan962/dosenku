from django.contrib import admin
from .models import Professor, Department, School, Major, Subject

class SubjectInline(admin.TabularInline):
    model = Professor.subjects.through
    extra = 1

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'major', 'list_subjects')
    list_filter = ('department', 'major', 'subjects')
    search_fields = ('name', 'department__name', 'major__name', 'subjects__name')
    inlines = [SubjectInline]

    def list_subjects(self, obj):
        """Custom method to display subjects."""
        return ", ".join([subject.name for subject in obj.subjects.all()])

    list_subjects.short_description = 'Subjects'

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('name', 'school__name')

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

class MajorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(Subject, SubjectAdmin)
