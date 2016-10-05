
import re
import os,os.path

from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode

_EMAIL_RE = re.compile(r'[\w\d._%+-]+@[\w\d.-]+\.\w{2,}')

class RemoteUserLoginHandler(BaseHandler):

    @staticmethod
    def email_to_user(username):
        if _EMAIL_RE.match(username):
            return re.sub(r'^[\w]','_',username)
        else:
            return username
    
    def get(self):
        header_name = self.authenticator.header_name
        remote_user = self.request.headers.get(header_name, "")
        if remote_user == "":
            raise web.HTTPError(401)
        else:
            remote_user = self.email_to_user(username)
            if not os.path.exists('/home/'+remote_user):
                raise web.HTTPError(reason="directory does not exist, to gain access, please contact ithelp@geos.ed.ac.uk",status_code=403)
            user = self.user_from_username(remote_user)
            self.set_login_cookie(user)
            self.redirect(url_path_join(self.hub.server.base_url, 'home'))


class RemoteUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    """
    header_name = Unicode(
        default_value='REMOTE_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()

