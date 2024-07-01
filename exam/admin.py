from django.contrib import admin
from exam.models import Test,TestSeries,TestType,Question,Answer,Subscription,TestAttempt
# Register your models here.
admin.site.register(Test)
admin.site.register(TestType)
admin.site.register(TestSeries)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Subscription)
admin.site.register(TestAttempt)
