====================================
Jupyterhub REMOTE_USER Authenticator
====================================

Authenticate to Jupyterhub using an authenticating proxy that can set
the REMOTE_USER header.

------------
Installation
------------

This package can be installed with `pip`:

    cd jhub_remote_user_authenticator
    pip install .

Alternately, you can add this project folder must be on your PYTHONPATH.

You should edit your :file:`jupyterhub_config.py` to set the authenticator 
class::

    c.JupyterHub.authenticator_class = 'remote_user.RemoteUserAuthenticator'

You should be able to start jupyterhub.  The "/login" resource
will look for the authenticated user name in the HTTP header "REMOTE_USER".
If found, and not blank, you will be logged in as that user.

