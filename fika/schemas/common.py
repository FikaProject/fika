import colander

from fika import FikaTSF as _


class NoDuplicates(object):
    """ Validator which succeeds if the iterable passed doesn't have duplicates. """

    def __call__(self, node, value):
        pool = set()
        for v in value:
            pool.add(v)
        if len(pool) != len(value):
            err = _("Must only contain unique values")
            raise colander.Invalid(node, err)

