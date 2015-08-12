from django.contrib import admin

from .models import Choice, Question, AvvBlogScrapTable


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)


class AvvBlogScrapTableAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Html Content  ', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('domain_name', 'main_title', 'main_title_link')
    list_filter = ['created_on']
    search_fields = ['domain_name', 'main_title', 'main_title_link', 'category_title', ]



admin.site.register(AvvBlogScrapTable, AvvBlogScrapTableAdmin)

