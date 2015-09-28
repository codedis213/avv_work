from django.contrib import admin

from .models import *
import MySQLdb
import requests


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

    def __init__(self, model, admin_site):
        admin.ModelAdmin.__init__(self, model, admin_site)
        self.db = MySQLdb.connect("localhost", "root", "root", "avv_blog_scrap" )
        self.cursor = self.db.cursor()
        sql_email_rows = """select email from avv_blog_email_handling_table"""
        self.cursor.execute(sql_email_rows)
        email_rows = self.cursor.fetchall()
        self.to = [em[0] for em in email_rows]
        self.to.extend(["jaiprakashsingh213@gmail.com", 'santosh.kumar@wisepromo.com' ])

    def __del__(self):
        self.db.close()

    def send_simple_message(self, to, subject, message):
        return requests.post(
            "https://api.mailgun.net/v3/sandboxa87eb15ddb8c420d87d5c8db15f80a69.mailgun.org/messages",
            auth=("api", "key-761deed87c5ec92e3372b3a4747df079"),
            data={"from": "Excited User <mailgun@sandboxa87eb15ddb8c420d87d5c8db15f80a69.mailgun.org>",
                  "to": to,
                  "subject": subject,
                  "text": message})


    def save_model(self, request, obj, form, change):
        domain_link = request.POST.get("domain_link")
        domain_name = request.POST.get("domain_name")

        to = self.to

        subject = "new domain:-  %s added" %(domain_name)
        message = """Hi

                     new domain:-  %s have added to your admin
                     with domian link:- %s"""

        message = message % (domain_name, domain_link)

        self.send_simple_message(to, subject, message)
        obj.save()


admin.site.register(LinkHandling, LinkHandlingAdmin)


class EmailHandlingAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        admin.ModelAdmin.__init__(self, model, admin_site)
        self.db = MySQLdb.connect("localhost", "root", "root", "avv_blog_scrap" )
        self.cursor = self.db.cursor()
        sql_email_rows = """select email from avv_blog_email_handling_table"""
        self.cursor.execute(sql_email_rows)
        email_rows = self.cursor.fetchall()
        self.to = [em[0] for em in email_rows]
        self.to.extend(["jaiprakashsingh213@gmail.com", 'santosh.kumar@wisepromo.com' ])

    def __del__(self):
        self.db.close()

    def send_simple_message(self, to, subject, message):
        return requests.post(
            "https://api.mailgun.net/v3/sandboxa87eb15ddb8c420d87d5c8db15f80a69.mailgun.org/messages",
            auth=("api", "key-761deed87c5ec92e3372b3a4747df079"),
            data={"from": "Excited User <mailgun@sandboxa87eb15ddb8c420d87d5c8db15f80a69.mailgun.org>",
                  "to": to,
                  "subject": subject,
                  "text": message})

    list_display = ('email', 'is_staff', 'is_active', 'created_on', 'changed_on')
    list_filter = ['email', 'is_staff', 'is_active', 'created_on', 'changed_on']
    search_fields = ['email']

    def save_model(self, request, obj, form, change):
        email = request.POST.get("email")
        to = self.to
        subject = "new email:-  %s added" %(email)
        message = """Hi
                    new email %s have added to your admin"""
        message = message % email

        self.send_simple_message(to, subject, message)
        obj.save()

admin.site.register(EmailHandling, EmailHandlingAdmin)




