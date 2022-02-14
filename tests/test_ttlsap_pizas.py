from nose.tools import assert_equal
from ttlsap.pizas import *

def test_ttlsap_pizas():
    """ test the pizas """
    pizas = Pizas()
    res = pizas.query_graph(pizas.g, sub="ex1", predicate=None, obj=Literal('pos'))