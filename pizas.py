import csv
from rdflib import Graph, Literal, URIRef


class Shape:
    def __init__(self, shape):
        self.name = shape


class Size:
    def __init__(self, size):
        self.name = size
    

class Shade:
    def __init__(self, shade):
        self.name = shade


class PizaClass:
    def __init__(self, _class):
        self.name = _class


class Crust:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
    
    
class Filling:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
    

class Piza:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)


def test_piza():
    p1 = Piza(example='ex1', shape=Shape(1), crust=Crust(size=Size(1), shade=Shade(1)),
              filling=Filling(size=Size(1), shade=Shade(1)), pizaclass=PizaClass(1))


class Pizas:
    def __init__(self):
        self.g = Graph()
        self.samples = []
        self.read_data()

    def read_data(self):
        file = open('piza_data.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        print(header)
        rows = []
        for row in csvreader:
            rows.append(row)
            self.samples.append(Piza(example=row[0],shape=row[1], crust=Crust(size=row[2], shade=row[3]),
                                     filling=Filling(size=row[4], shade=row[5]), pizaclass=row[6]))
            self._graph(header, row)

        file.close()
        self.header = header
        self.rows = rows

    def _graph(self, header, row):
        subject = URIRef(row[0])
        self.g.add((subject, URIRef(header[1]), Literal(row[1])))
        self.g.add((subject, URIRef(header[2]), Literal(row[2])))
        self.g.add((subject, URIRef(header[3]), Literal(row[3])))
        self.g.add((subject, URIRef(header[4]), Literal(row[4])))
        self.g.add((subject, URIRef(header[5]), Literal(row[5])))
        self.g.add((subject, URIRef(header[6]), Literal(row[6])))


    def query_graph(self, sub=None, predicate=None, obj=None):
        for s, p, o in self.g.triples((sub, predicate, obj)):
            print(f'{s}:{p}:{o}')

    def query_graph_byid(self, subject_id,sub=None, predicate=None, obj=None):
        res = []
        for s, p, o in self.g.triples((sub, predicate, obj)):
            if s.__str__() == subject_id:
                print(f'{s}; Subject = {subject_id}')
                res.append(f'{s}:{p}:{o}')
        return res


if __name__ == '__main__':
    pizas = Pizas()
    query_graph(pizas.g, sub=None, predicate=None, obj=Literal('pos'))
    query_graph(pizas.g, sub=None, predicate=URIRef('Shape'), obj=Literal('Circle'))