import os

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///{}'.format(os.path.join(os.getcwd(), "moderated_owens.db")))


OIDC_ISSUER = os.environ.get('API_QUOTEFAULT_OIDC_ISSUER', 'https://sso.csh.rit.edu/realms/csh')
OIDC_CLIENT_CONFIG = {
    'client_id': os.environ.get('API_QUOTEFAULT_OIDC_CLIENT_ID', 'quotefault-api'),
    'client_secret': os.environ.get('POT_OIDC_CLIENT_SECRET', ''),
    'post_logout_redirect_uris': [os.environ.get('POT_OIDC_LOGOUT_REDIRECT_URI', 'https://quotefault-api.csh.rit.edu/logout')]
}
