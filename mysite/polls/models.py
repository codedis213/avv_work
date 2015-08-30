from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):              # __unicode__ on Python 2
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text



class AvvBlogScrapTable(models.Model):
    domain_name = models.CharField(max_length=70)
    domain_link = models.URLField()
    main_title = models.CharField(max_length=70)
    main_title_link = models.URLField()
    blog_title = models.CharField(max_length=70)
    blog_link = models.URLField()
    category_title = models.CharField(max_length=70, null=True)
    category_link = models.URLField(null=True)
    sub_category_title = models.CharField(max_length=70, null=True, blank=True)
    sub_category_link = models.URLField(blank=True, null=True)
    entry_content_html = models.TextField()
    entry_content_text = models.TextField(null=True, blank= True)
    created_on = models.DateTimeField(auto_now_add=True)
    changed_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "avv_blog_scrap_table"

    def __str__(self):              # __unicode__ on Python 2
        return "%s ==> %s" %(self.domain_name, self.main_title)


class LinkHandling(models.Model):
    domain_name = models.CharField(max_length=70, blank=True, null=True)
    domain_link = models.URLField()
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    changed_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "avv_blog_link_handling_table"

    def __str__(self):              # __unicode__ on Python 2
        return "%s" %(self.domain_name)



class EmailHandling(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    changed_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "avv_blog_email_handling_table"

    def __str__(self):              # __unicode__ on Python 2
        return "%s" %(self.email)


