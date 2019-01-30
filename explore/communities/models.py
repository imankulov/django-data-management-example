from django.db import models


class Group(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    urlname = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    lat = models.TextField()  # This field type is a guess.
    lon = models.TextField()  # This field type is a guess.
    members = models.BigIntegerField()
    who = models.TextField(blank=True, null=True)
    organizer_id = models.BigIntegerField()
    organizer_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'

    def __str__(self):
        return self.name
