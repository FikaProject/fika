from arche.views.base import BaseView

from fika.models.interfaces import IFikaUser


class FikaBaseView(BaseView):
    
    @property
    def fikaProfile(self):
        return IFikaUser(self.profile, None)
