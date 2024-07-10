from django.contrib import admin
from .models import *
from django.db.models import Sum

# Register your models here.
from .models import *

admin.site.register(Recipe)
admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(SubjectMarks)

class SubjectMarkAdmin(admin.ModelAdmin):
    list_display = ['student' , 'subject' , 'marks']


class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student' , 'student_rank', 'total_marks' ,'date_of_report_card_generation']

    ordering = ['student_rank']

    def total_marks(self , obj):
        subject_marks = Subject.objects.filter(student=obj.student)
        marks = (obj.aggregate(marks = Sum('marks'))).marks
        print()
        return marks['marks']   

admin.site.register(ReportCard,ReportCardAdmin)    