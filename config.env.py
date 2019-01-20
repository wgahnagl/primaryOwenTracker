import os

SERVER_NAME = os.environ.get('POT_SERVER_NAME', 'pot-local.csh.rit.edu:5000')

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                         'sqlite:///{}'.format(os.path.join(os.getcwd(), "moderated_owens.db")))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'SomethingNotEntirelySecret'

OIDC_ISSUER = os.environ.get('POT_ODIC_ISSUER', 'https://sso.csh.rit.edu/auth/realms/csh')
OIDC_CLIENT_CONFIG = {
    'client_id': os.environ.get('POT_OIDC_CLIENT_ID', 'pot'),
    'client_secret': os.environ.get('POT_OIDC_CLIENT_SECRET', ''),
    'post_logout_redirect_uris': [os.environ.get('SWAG_OIDC_LOGOUT_REDIRECT_URI', 'http://pot-local.csh.rit.edu:5000')]
}
