from django.db import router
from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField, RECURSIVE_RELATIONSHIP_CONSTANT

from django.utils.translation import (ugettext_lazy as _, string_concat,
    ungettext, ugettext)

from django import forms

from arrayfields.widgets import StringArray

class ArrayManyToManyRel(object):
    def __init__(self, to, limit_choices_to=None, related_name=None, manager_name=None):
        self.to = to
        self.limit_choices_to = limit_choices_to or {}
        self.related_name = related_name
        self.manager_name = manager_name
        self.multiple = True
        self.field_name = self.to._meta.pk.name

    def is_hidden(sel):
        return False

    def get_related_field(self):
        return self.to._meta.pk

class ArrayManyToManyField(RelatedField, Field):
    description = _("Many-to-many relationship via array db field")
    def __init__(self, to, **kwargs):
        try:
            assert not to._meta.abstract, "%s cannot define a relation with abstract class %s" % (self.__class__.__name__, to._meta.object_name)
        except AttributeError: # to._meta doesn't exist, so it must be RECURSIVE_RELATIONSHIP_CONSTANT
            assert isinstance(to, basestring), "%s(%r) is invalid. First parameter to ManyToManyField must be either a model, a model name, or the string %r" % (self.__class__.__name__, to, RECURSIVE_RELATIONSHIP_CONSTANT)

        kwargs['verbose_name'] = kwargs.get('verbose_name', None)
        kwargs['rel'] = ArrayManyToManyRel(to,
            limit_choices_to=kwargs.pop('limit_choices_to', None),
            related_name=kwargs.pop('related_name', None),
            manager_name=kwargs.pop('manager_name', None))

        Field.__init__(self, **kwargs)

        msg = _('Hold down "Control", or "Command" on a Mac, to select more than one.')
        self.help_text = string_concat(self.help_text, ' ', msg)

    def get_choices_default(self):
        return Field.get_choices(self, include_blank=False)

    def contribute_to_class(self, cls, name):
        super(ArrayManyToManyField, self).contribute_to_class(cls, name)
        setattr(cls, self.rel.manager_name, ArrayReverseManyRelatedObjectsDescriptor(self))

        if isinstance(self.rel.to, basestring):
            target = self.rel.to
        else:
            target = self.rel.to._meta.db_table
        cls._meta.duplicate_targets[self.column] = (target, "am2m")

    def contribute_to_related_class(self, cls, related):
        pass

    def set_attributes_from_rel(self):
        pass

    def value_from_object(self, obj):
        return getattr(obj, self.rel.manager_name).all()

    def save_form_data(self, instance, data):
        setattr(instance, self.attname, data)

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        defaults = {
            'form_class': forms.ModelMultipleChoiceField,
            'queryset': self.rel.to._default_manager.using(db).complex_filter(self.rel.limit_choices_to)
        }
        defaults.update(kwargs)
        # If initial is passed in, it's a list of related objects, but the
        # MultipleChoiceField takes a list of IDs.
        if defaults.get('initial') is not None:
            initial = defaults['initial']
            if callable(initial):
                initial = initial()
            defaults['initial'] = [i._get_pk_val() for i in initial]
        return super(ArrayManyToManyField, self).formfield(**defaults)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if value and hasattr(value, '__iter__') and isinstance(value[0], self.rel.to):
            return [i._get_pk_val() for i in value]
        else:
            return value


class ArrayReverseManyRelatedObjectsDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        superclass = self.field.rel.to._default_manager.__class__
        return self.create_manager(instance, superclass)

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("Manager must be accessed via instance")

        manager = self.__get__(instance)
        # If the foreign key can support nulls, then completely clear the related set.
        # Otherwise, just move the named objects into the set.
        if self.field.null:
            manager.clear()
        manager.add(*value)

    def create_manager(self, instance, superclass):

        # field in our model, rather in related
        field = self.field
        rel_model = self.field.rel.to

        foreign_pk = field.rel.get_related_field().name

        class ArrayManyRelatedManager(superclass):
            def _get_ids_set(self, instance):
                if not hasattr(instance, '_' + field.name + '_set'):
                    setattr(instance, '_' + field.name + '_set', set(getattr(instance, field.name) or []))
                return getattr(instance, '_' + field.name + '_set')

            def get_query_set(self):
                db = self._db or router.db_for_read(rel_model, instance=instance)
                return superclass.get_query_set(self).using(db).filter(**(self.core_filters))

            def add(self, *objs):
                ids = getattr(instance, field.name) or []
                ids_set = self._get_ids_set(instance)
                for obj in objs:
                    if not isinstance(obj, rel_model):
                        raise TypeError("'%s' instance expected" % rel_model._meta.object_name)
                    if getattr(obj, foreign_pk) not in ids_set:
                        ids.append(getattr(obj, foreign_pk))
                setattr(instance, field.name, ids)
                instance.save()

            add.alters_data = True

            def create(self, **kwargs):
                db = router.db_for_write(rel_model, instance=instance)
                obj = super(ArrayManyRelatedManager, self.db_manager(db)).create(**kwargs)
                self.add(obj)
                return obj
            create.alters_data = True

            def get_or_create(self, **kwargs):
                db = router.db_for_write(rel_model, instance=instance)
                obj, created = super(ArrayManyRelatedManager, self.db_manager(db)).get_or_create(**kwargs)
                self.add(obj)
                return obj, created
            get_or_create.alters_data = True

            # remove() and clear() are only provided if the ForeignKey can have a value of null.
            def remove(self, *objs):
                ids = getattr(instance, field.name) or []
                ids_set = self._get_ids_set(instance)
                for obj in objs:
                    # Is obj actually part of this descriptor set?
                    if getattr(obj, foreign_pk) in ids_set:
                        ids.remove(getattr(obj, foreign_pk))
                    else:
                        raise field.rel.to.DoesNotExist("%r is not related to %r." % (obj, instance))
                setattr(instance, field.name, ids)
                instance.save()
            remove.alters_data = True

            if field.null:
                def clear(self):
                    setattr(instance, field.name, null)
                    instance.save()
                clear.alters_data = True

        manager = ArrayManyRelatedManager()
        attname = field.attname
        manager.core_filters = {'%s__in' % foreign_pk:
                getattr(instance, attname)}
        manager.model = field.rel.to

        return manager

class LinksMultiWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        super(LinksMultiWidget, self).__init__((forms.TextInput(), forms.TextInput()), attrs)

    def render(self, name, value, attrs=None):
        #self.widgets = [forms.TextInput() for i in range(3)] #len(value)+5
        #self.field.fields = [forms.CharField(required=False) for i in range(3)]
        super(LinksMultiWidget, self).render(name, value, attrs)

    def decompress(self,value):
        return ['','','']


class StringArrayFormField(forms.Field):
    """
    Form field
    """
    widget = StringArray

class StringArrayField(Field):
    """
    Model field
    """

    def formfield(self, **kwargs):
        defaults = {'required': False, 'form_class': StringArrayFormField}
        defaults.update(kwargs)
        
        return super(StringArrayField, self).formfield(**defaults)
