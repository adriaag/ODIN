from typing import Union

import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from common import *
from urllib.parse import quote


class ParameterSpecification:
    def __init__(self, parameter: URIRef,
                 value: Union[URIRef, Literal] = None,
                 namespace: Namespace = ab) -> None:
        super().__init__()
        self.parameter = parameter
        self.value = value
        self.namespace = namespace

        self.url_name = quote(f'{self.parameter.url_name}_{self.value}_specification'.replace(' ', '_').lower(), safe=":/-_")

        self.uri_ref = namespace[self.url_name]
    
    
    # def add_to_graph(self, g: Graph):

    #     # Base triples
    #     g.add(self.uri_ref, RDF.type, tb.ParameterSpecification)
    #     g.add(self.uri_ref, RDF.label, self.url_name)

    #     if isinstance(self.value, Literal):
    #         g.add(self.uri_ref, tb.hasValue, self.value)
    #     else:
    #         g.add(self.uri_ref, tb.hasValue, Literal(self.value))

    #     # Parameter
    #     g.add(self.parameter, tb.specifiedBy, self.uri_ref)

        
    #     return self.uri_ref