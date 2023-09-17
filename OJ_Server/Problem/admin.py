from django.contrib import admin
from .models import Tag, Problem, Testcase

admin.site.register(Tag)
admin.site.register(Problem)
admin.site.register(Testcase)
