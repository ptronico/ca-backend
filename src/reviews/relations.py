from rest_framework.reverse import reverse
from rest_framework.relations import HyperlinkedIdentityField


class HackedHyperlinkedIdentityField(HyperlinkedIdentityField):
    """
    Represents the instance, or a property on the instance, using hyperlinking.
    Based on https://github.com/encode/django-rest-framework/issues/1024#issue-17611250
    """
    def __init__(self, *args, **kwargs):
        self.the_args = kwargs.pop('the_args', [])
        super().__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.
        """
        args = []
        for arg in self.the_args:
            args.append(eval(f'obj.{arg}'))
        return reverse(view_name, args=args, request=request, format=format)
