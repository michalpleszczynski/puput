DISQUS = 'disqus'
DJANGO_COMMENTS = 'django_comments'
SUPPORTED_PROVIDERS = (DISQUS, DJANGO_COMMENTS)


def get_context_for_provider(provider_name, blog_page, entry):
    if provider_name == DISQUS:
        return {
            'disqus_shortname': blog_page.disqus_shortname,
            'disqus_identifier': entry.id
        }
    if provider_name == DJANGO_COMMENTS:
        return {
            'entry': entry
        }
    return {}


def get_num_comments_for_provider(provider_name, blog_page, entry_page):
    if provider_name == DISQUS:
        try:
            from tapioca.exceptions import ClientError
            from tapioca_disqus import Disqus

            disqus_client = Disqus(api_secret=blog_page.disqus_api_secret)
            try:
                params = {'forum': blog_page.disqus_shortname, 'thread': 'ident:{}'.format(entry_page.id)}
                thread = disqus_client.threads_details().get(params=params)
                return thread.response.posts().data()
            except ClientError:
                return 0
        except ImportError:
            raise Exception('You need to install tapioca-disqus before using Disqus as comment system.')
    if provider_name == DJANGO_COMMENTS:
        try:
            from django_comments.models import Comment
            from django.contrib.contenttypes.models import ContentType

            entry_page_type = ContentType.objects.get(app_label='puput', model='entrypage')
            return Comment.objects.filter(content_type=entry_page_type, object_pk=entry_page.pk).count()
        except ImportError:
            raise Exception('You need to install django-comments before using it as comment system.')
