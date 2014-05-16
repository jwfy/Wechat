import sae
from WeChat import wsgi

application = sae.create_wsgi_app(wsgi.application)