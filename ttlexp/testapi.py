from flask import Blueprint
from flask_restx import Api, Resource, fields, reqparse
import json
from ttlsap.pizas import Pizas

pizza_bd = Blueprint('piza_api', __name__)
pizza_api = Api(pizza_bd)

piza_model = pizza_api.model('Pizas', {
  'Ex': fields.String(attribute='example'),
  'Shape': fields.String(attribute='shape'),
  'Crust.size': fields.String(attribute='crust.size'),
  'Crust.shade': fields.String(attribute='crust.shade'),
  'Filling.size': fields.String(attribute='filling.size'),
  'Filling.shade': fields.String(attribute='filling.shade'),
  'Class': fields.String(attribute='pizaclass')
})


### Gens Domain Ontology & OWL Graph In the begin ###

pizas = Pizas()


@pizza_api.route('/pizas/') 
@pizza_api.route('/piza/<example>/', methods=['POST'])
class PizasExp(Resource):
    @pizza_api.doc()
    @pizza_api.marshal_with(piza_model, envelope='pizas')
    def get(self):
        data = pizas.samples
        return data
  
    @pizza_api.doc()
    @pizza_api.marshal_with(piza_model, envelope='pizas')
    def post(self, example):
        print(example)
        data = pizas.query_graph_byid(example)
        print(data)
        return data

@pizza_api.route('/graph/piza/')
class PizaGraph(Resource):
    @pizza_api.doc()
    @pizza_api.marshal_with(piza_model, envelope='piza')
    def get(self, **kwargs):
        args = self.parser.parse_args()
        piza_id = args['ex']
        data = pizas.query_graph_byid(piza_id)
        return data
  
  
  
  

