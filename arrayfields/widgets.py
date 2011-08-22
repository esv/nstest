from django.forms.widgets import Widget, TextInput

from django.utils.safestring import mark_safe

class StringArrayRenderer(object):
    """
    An object used by StringArray
    """

    def __init__(self, name, value, attrs):
        self.name, self.value, self.attrs = name, value, attrs

    def __iter__(self):
        name = self.name #+ '[]'
        i = 0
        for v in self.value:
            yield TextInput().render(name, v, self.attrs)
            i += 1
        yield TextInput().render(name, '', self.attrs)

    def __getitem__(self, idx):
        return TextInput(self.value[idx])

    def __unicode__(self):
        return self.render()

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
                % w for w in self]))

class StringArray(Widget):
    renderer = StringArrayRenderer

    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs)
        return self.renderer(name, value, final_attrs)

    def render(self, name, value, attrs=None):
        return self.get_renderer(name, value, attrs).render()

    def value_from_datadict(self, data, files, name):
        return data.getlist(name)
