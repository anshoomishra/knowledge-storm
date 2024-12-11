from django.contrib import admin
from exam.models import Test,TestSeries,TestType,Question,Answer,Subscription,TestAttempt,QuestionAttempt
# Register your models here.

class AnswerInline(admin.TabularInline):  # Or use StackedInline for a different layout
    model = Answer
    extra = 1  # Number of empty answer forms to display
    fields = ['text', 'is_correct']  # Fields to display in the inline form
    readonly_fields = ['id']  # Optionally make ID read-only

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]  # Include the inline in the question admin
    list_display = ['text', 'created_by', 'max_marks', 'is_objective']  # Customize the list view
    search_fields = ['text']  # Add search functionality
    list_filter = ['is_objective', 'test']  # Add filters

admin.site.register(Test)
admin.site.register(TestType)
admin.site.register(TestSeries)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Subscription)
admin.site.register(TestAttempt)
admin.site.register(QuestionAttempt)
