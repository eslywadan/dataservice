from flask import Blueprint
from flask_restplus import Api

api = Api(Blueprint)

from .apis.mfg import api as nsmfg
from .apis.int import api as nsint
from .apis.eng import api as nseng
from .apis.piza import api as nspiza

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint
    ,title='My Title',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(ns1mfg)
api.add_namespace(ns2int)
api.add_namespace(ns3eng)
api.add_namespace(nstpiza)