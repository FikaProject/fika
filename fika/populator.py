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
        self.context['course_modules'] = factories['CourseModules']()


def includeme(config):
    config.add_populator(FikaPopulator)

# def populate_database():
#     from fika.models.site import SiteRoot
#     from fika.models.user import User
#     from fika.models.users import Users
#     from fika.models.courses import Courses
#     from fika.models.course_modules import CourseModules
#     from fika.security import ROLE_ADMIN
#     from fika.security import get_security
#     from fika.models.interfaces import IFlashMessages
#     from pyramid.threadlocal import get_current_request
#     site = SiteRoot()
#     site['users'] = Users()
#     admin = User(password = 'admin', email = 'admin@admin.com')
#     site['users'][admin.uid] = admin
#     sec = get_security(site)
#     sec.add_groups(admin.userid, [ROLE_ADMIN])
#     site['courses'] = Courses()
#     site['course_modules'] = CourseModules()
#     request = get_current_request()
#     fm = request.registry.queryAdapter(request, IFlashMessages)
#     if fm: #To avoid having to deal with this during tests
#         _ = FikaTSF #_ enables translations to be found
#         msg = _(u"site_populated_info",
#                 default = u"Since this is the first time you're using Fika, the site has been populated "
#                     u"with a default user. You may login with <b>admin@admin.com</b> and password <b>admin</b>. ")
#         fm.add(msg, auto_destruct = False)
#     return site