def get_context_for_provider(provider_name, blog_page, entry):
    if provider_name == 'disqus':
        return {
            'disqus_shortname': blog_page.disqus_shortname,
            'disqus_identifier': entry.id
        }
    if provider_name == 'django_comments':
        return {
            'entry': entry
        }
    return {}


def get_num_comments_with_disqus(blog_page, entry_page):
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
