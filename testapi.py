from flask import Blueprint
from flask_restplus import Api, Resource, fields, reqparse
import json
from pizas import *

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
class PizasExp(Resource):
  @pizza_api.doc()
  @pizza_api.marshal_with(piza_model, envelope='pizas')
  def get(self, **kwargs):
    data = pizas.samples
    return data
  
@pizza_bd.route('/piza/<string:example>')
def singlepiza(example):
  data = pizas.query_graph_byid(example)
  return data

@pizza_api.route('/piza/')
class PizaGraph(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('ex', help='Specify sample')
  @pizza_api.doc(parser=parser)
  @pizza_api.marshal_with(piza_model, envelope='piza')
  def get(self, **kwargs):
    args = self.parser.parse_args()
    piza_id = args['ex']
    data = pizas.query_graph_byid(piza_id)
    return data
  
  
  
  

