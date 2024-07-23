from django.db import models

# Create your models here.


class Preacher(models.Model):
    preacher_name = models.CharField(max_length=100)
    church_name = models.CharField(max_length=100)
    stream_link_id = models.CharField(max_length=100, blank=True)
    thumbnail = models.ImageField()
    is_live = models.BooleanField(default=True)
    pinned_list_id = models.IntegerField(default=0)
    title = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.preacher_name}•{self.church_name} LIVE'
