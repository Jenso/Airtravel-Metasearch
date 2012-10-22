from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def bootstrap_less():
    #<link rel="stylesheet/less" href="{{ STATIC_URL }}bootstrap.less">
    #<script src="//cdnjs.cloudflare.com/ajax/libs/less.js/1.3.0/less-1.3.0.min.js"></script>

    if settings.DEVELOPMENT:
        LESS_TAG = '<link rel="stylesheet/less" type="text/css" href="%s%s">'

        output = [LESS_TAG % (settings.STATIC_URL, "bootstrap.less"),
                  '<script src="//cdnjs.cloudflare.com/ajax/libs/less.js/1.3.0/less-1.3.0.min.js" type="text/javascript"></script>',
                  ]
        output = '\n'.join(output)

    else:
        output = '<link charset="utf-8" rel="stylesheet" type="text/css" href="%scss/style.css">' % (settings.STATIC_URL)

    return output

@register.simple_tag
def tornado_api_url():
    if settings.DEVELOPMENT:
        return 'http://localhost:8888/'
    else:
        return '/tornado-api/'
