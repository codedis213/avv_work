from django.contrib import admin

from .models import *


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'pub_date', 'was_published_recently')
#     list_filter = ['pub_date']
#     search_fields = ['question_text']
#
# admin.site.register(Question, QuestionAdmin)


class AvvBlogScrapTableAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Domain',               {'fields': ['domain_name', 'domain_link'], 'classes': ['collapse']}),
        ('Main',               {'fields': ['main_title', 'main_title_link'], 'classes': ['collapse']}),
        ('Blog',               {'fields': ['blog_title', 'blog_link'], 'classes': ['collapse']}),
        ('Category',               {'fields': ['category_title', 'category_link'], 'classes': ['collapse']}),
        ('Sub category',               {'fields': ['sub_category_link', 'sub_category_title'], 'classes': ['collapse']}),
        ('Entry content', {'fields': ['entry_content_html', 'entry_content_text'], 'classes': ['collapse']}),
    ]
    list_display = ('domain_name', 'blog_title', 'blog_link')
    list_filter = ['created_on']
    search_fields = ['domain_name', 'blog_link', 'blog_link', 'category_title', ]


admin.site.register(AvvBlogScrapTable, AvvBlogScrapTableAdmin)


class LinkHandlingAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'domain_link', 'active', 'created_on', 'changed_on')
    list_filter = ['domain_name', 'domain_link', 'active', 'created_on', 'changed_on']
    search_fields = ['domain_name', 'domain_link']

admin.site.register(LinkHandling, LinkHandlingAdmin)

class EmailHandlingAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'created_on', 'changed_on')
    list_filter = ['email', 'is_staff', 'is_active', 'created_on', 'changed_on']
    search_fields = ['email']

admin.site.register(EmailHandling, EmailHandlingAdmin)




