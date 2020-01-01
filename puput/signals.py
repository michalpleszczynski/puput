from django.conf import settings

from .comments import get_num_comments_for_provider, SUPPORTED_PROVIDERS


def update_comment_count(sender, **kwargs):
    comment = kwargs['comment']
    entry_page = comment.content_object
    if settings.PUPUT_COMMENTS_PROVIDER in SUPPORTED_PROVIDERS:
        num_comments = get_num_comments_for_provider(settings.PUPUT_COMMENTS_PROVIDER, None, entry_page)
        entry_page.num_comments = num_comments
        entry_page.save(update_fields=('num_comments',))


try:
    from django_comments.signals import comment_was_posted

    comment_was_posted.connect(update_comment_count, dispatch_uid="puput_comment_posted_id")
except ImportError:
    pass
