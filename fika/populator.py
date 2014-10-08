from __future__ import unicode_literals

from arche.populators import Populator
from arche.utils import get_content_factories

from fika import _


class FikaPopulator(Populator):
    name = 'fika'
    title = _("Fika site")
    description = _("Setup and install Fika")

    def populate(self, **kw):
        factories = get_content_factories()
        self.context['courses'] = factories['Courses']()


def includeme(config):
    config.add_populator(FikaPopulator)
