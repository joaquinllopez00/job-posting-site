from django import template

from job.models import FavoriteJob

register = template.Library()


@register.simple_tag(name='is_job_already_saved')
def is_job_already_saved(job, user):
    applied = FavoriteJob.objects.filter(job=job, user=user)
    if applied:
        return True
    else:
        return False
