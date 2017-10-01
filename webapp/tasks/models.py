from django.utils.timezone import now
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from .OcrRequester import OcrRequester

class Task(models.Model):
    STATUS = (
        ('requested', 'Requested'),
        ('progressing', 'Progressing'),
        ('done', 'Done'),
    )

    status = models.CharField(max_length=32, choices=STATUS, default='requested')
    type = models.CharField(max_length=100, default='ocr')
    resource = models.URLField()
    result = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_tablespace = "tables"

    @receiver(OcrRequester.ocr_finished, sender=OcrRequester)
    def write_result(sender, **kwargs):
        id = kwargs.get('id')
        result = kwargs.get('result')
        print('for task id:', id)
        print(" [.] Got", result)
        task = Task.objects.get(pk=id)
        task.result = result
        task.status = 'done'
        task.resolved_at = now()
        task.save()


@receiver(post_save, sender=Task)
def request_ocr(sender, **kwargs):
    task = kwargs.get('instance')

    if task.status == 'requested':
        ocr_requester = OcrRequester()

        ocr_request = {
            "id": task.id,
            "image_url": task.resource
        }
        ocr_requester.send(ocr_request)