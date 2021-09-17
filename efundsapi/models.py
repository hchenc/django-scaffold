import uuid
from django.db import models
from django_bulk_update.manager import BulkUpdateManager
from django.utils import timezone


def generate_uuid():
    return uuid.uuid4().hex


class AbstractResource(models.Model):
    uuid = models.CharField(primary_key=True, max_length=36,
                            default=generate_uuid, editable=False)
    id = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = BulkUpdateManager()

    class Meta:
        unique_together = (("id",))
        abstract = True

    @classmethod
    def mark_deleted(cls, id):
        ins = cls.objects.get(id=id)
        ins.deleted = True
        ins.deleted_at = timezone.now()
        ins.save()
        return ins


class Demo(AbstractResource):
    demo_data = models.CharField(max_length=32, null=False, default='')
