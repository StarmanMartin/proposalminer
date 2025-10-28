from django.db import models
from django.db.models import Max


class Proposal(models.Model):
    proposal_key = models.CharField(max_length=255)  # required max_length
    name = models.CharField(max_length=255, null=True, default=None)  # required max_length
    group = models.IntegerField(null=True, default=None)
    collection = models.IntegerField(null=True, default=None)
    research_plan = models.IntegerField(null=True, default=None)
    research_plan_status_table = models.CharField(max_length=255, null=True, default=None)


class Report(models.Model):
    proposal_id = models.CharField(max_length=255, null=True)
    date = models.IntegerField(null=True, default=None)
    data = models.JSONField(null=True)
    technology = models.CharField(max_length=255, null=True, default=None)
    synced = models.BooleanField(default=False)


    class Meta:
        unique_together = ('date', 'proposal_id', "technology",)


class Call(models.Model):
    number = models.IntegerField(unique=True)
    done = models.BooleanField(default=False)

    @classmethod
    def add_calls(cls, *calls):
        for call in calls:
            cls.objects.get_or_create(number=call)

    @classmethod
    def call_done(cls, last_open_call: int):
        cls.objects.get_or_create(number=last_open_call-1)
        cls.objects.filter(number__lt=last_open_call).update(done=True)

    @classmethod
    def latest_call(cls):
        max_val = cls.objects.filter(done=True).aggregate(Max('number')).get('number__max')
        if max_val is None:
            return 0
        return max_val
