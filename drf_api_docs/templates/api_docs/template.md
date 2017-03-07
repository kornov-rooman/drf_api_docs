{% load i18n %}
# {{ project_name }}
---------------------


{% for name, obj in api.items %}
## {{ name }}
{% for link_name, link in obj.links.items %}
### {{ link_name }}
```
{% trans 'URL' %}: {{ link.url }}
{% trans 'Method' %}: {{ link.action|upper }}
{% trans 'Encoding' %}: {% if link.encoding %}{{ link.encoding }}{% else %}---{% endif %}
```

{% trans 'Fields' %}:
{% for field in link.fields %}
- `{{ field.name }}` required={{ field.required }}{% if field.type %} ({{ field.type }}){% endif %} {% if field.description %} - {{ field.description }}{% endif %}{% endfor %}


{% if link.description %}{% trans 'Description' %}: {{ link.description }}{% endif %}

{% endfor %}
{% endfor %}
