import itertools
import os
import sys
from enum import IntEnum
from random import Random
from typing import Tuple, List, Dict, Optional

from tqdm import tqdm


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common import *
from ontology_populator.implementations.core import Implementation, Component, CopyTransformation, Transformation


# def add_random_children(graph: Graph, namespace: Namespace, edge: Optional[URIRef], parent: URIRef, min_children: int,
#                         max_children: int, child_type: URIRef) -> List[URIRef]:
#     num_children = Random().randint(min_children, max_children)
#     children = []
#     for i in range(num_children):
#         child = namespace.term(f'{parent.fragment}_{i}')
#         children.append(child)
#         graph.add((child, RDF.type, child_type))
#         if edge is not None:
#             graph.add((child, edge, parent))
#     return children


# def generate_problems(cbox: Graph, num_problems: int = 100) -> \
#         Tuple[Dict[URIRef, URIRef], Dict[URIRef, List[URIRef]], List[URIRef]]:
#     cbox.add((cb.Problem, RDF.type, tb.Problem))

#     next_problems = add_random_children(cbox, cb, tb.subProblemOf, tb.Problem, 1, 4, cb.Problem)
#     parent = {p: cb.Problem for p in next_problems}
#     children = {cb.Problem: next_problems}

#     while len(parent) < num_problems - 1:
#         problem = next_problems.pop(0)
#         problem_children = add_random_children(cbox, cb, tb.subProblemOf, problem, 1 if len(next_problems) == 0 else 0,
#                                                min(4, num_problems - len(parent)), cb.Problem)
#         next_problems.extend(problem_children)
#         parent.update({p: problem for p in problem_children})
#         children.update({problem: problem_children})

#     return parent, children, [p for p in parent.keys() if p not in children]


def generate_main_tasks(graph: Graph) -> List[URIRef]:
    graph.add((cb.MainTask, RDF.type, tb.Task))
    graph.add((cb.DataProcessingTask, RDF.type, tb.Task))
    return [cb.MainTask, cb.DataProcessingTask]


def generate_algorithms(graph: Graph, tasks: List[URIRef]) -> List[URIRef]:
    algorithms = []
    for t in tasks:
        a = t.fragment.replace('Task', 'Algorithm')
        algorithms.append(cb[a])
        graph.add((cb[a], RDF.type, tb.Algorithm))
        graph.add((cb[a], tb.solves, t))
    return algorithms


def generate_datatags(graph: Graph, num_constraints: int) -> Tuple[URIRef, List[Tuple[URIRef, URIRef]]]:
    # Base Shape
    graph.add((cb['TabularDataset'], RDF.type, tb.DataTag))
    graph.add((cb['TabularDataset'], RDF.type, SH.NodeShape))
    graph.add((cb['TabularDataset'], SH.targetClass, dmop.TabularDataset))

    datatags = []
    for i in range(num_constraints):
        datatag = cb[f'Constraint_{i}']
        datatags.append((datatag, cb[f'constraint_{i}']))

        # Tag
        graph.add((datatag, RDF.type, tb.DataTag))
        graph.add((datatag, RDF.type, SH.NodeShape))
        graph.add((datatag, SH.targetClass, dmop.TabularDataset))
        graph.add((datatag, SH.property, cb[f'has_constraint_{i}']))

        # Constraint
        graph.add((cb[f'has_constraint_{i}'], RDF.type, SH.PropertyConstraintComponent))
        graph.add((cb[f'has_constraint_{i}'], SH.path, cb[f'constraint_{i}']))
        graph.add((cb[f'has_constraint_{i}'], SH.datatype, XSD.boolean))
        graph.add((cb[f'has_constraint_{i}'], SH.hasValue, Literal(True)))

    return cb['TabularDataset'], datatags


# def generate_rules(graph: Graph, num_rules: int) -> Tuple[URIRef, List[Tuple[URIRef, URIRef]]]:

#     graph.add((cb['TabularDataset'], RDF.type, tb.DataTag))
#     graph.add((cb['TabularDataset'], RDF.type, SH.NodeShape))
#     graph.add((cb['TabularDataset'], SH.targetClass, dmop.TabularDataset))

#     rules = []

#     for i in range(num_rules):
#         rule = cb[f'Rule_{i}']
#         rules.append((rule, cb[f'rule_{i}']))

#         graph.add((rule, RDF.type, tb.DataTag))
#         graph.add((rule, RDF.type, SH.NodeShape))
#         graph.add((rule, SH.targetClass, dmop.TabularDataset))
#         graph.add((rule, SH.property, cb[f'has_constraint_{i}']))

#         graph.add((cb[f'has_rule_{i}'], RDF.type, SH.PropertyConstraintComponent))
#         graph.add((cb[f'has_rule_{i}'], SH.path, cb[f'rule_{i}']))
#         graph.add((cb[f'has_rule_{i}'], SH.datatype, XSD.boolean))
#         graph.add((cb[f'has_rule_{i}'], SH.hasValue, Literal(True)))

#     return cb['TabularDataset'], rules



class RandomMethod(IntEnum):
    max = 0
    uniform = 1
    quadratic = 2


def get_random_up_to(components_per_requirement: int, method: RandomMethod = RandomMethod.quadratic) -> int:
    if method == RandomMethod.max:
        values = [components_per_requirement]
    elif method == RandomMethod.uniform:
        values = [i + 1 for i in range(components_per_requirement)]
    else:
        values = [i + 1 for i in range(components_per_requirement) for _ in range(2 ** i)]
    return Random().choice(values)


def generate_transformations(graph: Graph, datatags: List[Tuple[URIRef, URIRef]], components_per_requirement: int,
                             method: RandomMethod = RandomMethod.quadratic) -> \
        List[URIRef]:
    transformations = []
    for datatag, edge in datatags:
        num_components = get_random_up_to(components_per_requirement, method)
        for i in range(num_components):
            # Implementation
            implementation = Implementation(f'{datatag.fragment}_Implementation_{i}', cb.DataProcessingAlgorithm,
                                            [], [cb['TabularDataset']], [datatag], namespace=cb)
            component = Component(f'{datatag.fragment}_Component_{i}', implementation, [
                CopyTransformation(1, 1),
                Transformation(
                    query=f'''
INSERT DATA {{
    $output1 {edge.n3()} true.
}}
''',
                ),
            ], namespace=cb)

            implementation.add_to_graph(graph)
            component.add_to_graph(graph)

    return transformations


def genereate_components(cbox: Graph, num_components: int, num_requirements_per_component: int,
                         datatags: List[Tuple[URIRef, URIRef]],
                         method: RandomMethod = RandomMethod.quadratic) -> List[URIRef]:
    components = []
    for i in range(num_components):
        num_requirements = get_random_up_to(num_requirements_per_component, method)
        requirements = Random().sample([x for x, _ in datatags], num_requirements)
        # Implementation
        implementation = Implementation(f'Implementation_{i}', cb.MainAlgorithm, [], [requirements], [],
                                        namespace=cb)
        component = Component(f'Component_{i}', implementation, [], namespace=cb)

        implementation.add_to_graph(cbox)
        component.add_to_graph(cbox)

        components.append(component.uri_ref)
    return components


def generate_fake_abox(num_components: int, num_requirements_per_component: int, num_components_per_requirement: int,
                       overlap: float, folder: str):
    assert 0 <= overlap <= 1
    assert num_components > 0
    assert num_requirements_per_component > 0
    assert num_components_per_requirement > 0

    cbox = get_graph_xp()
    tasks = generate_main_tasks(cbox)
    algorithms = generate_algorithms(cbox, tasks)
    base_shape, datatags = generate_datatags(cbox, num_constraints=10)
    # base_shape2, rules = generate_rules(cbox, num_rules=5)
    transformations = generate_transformations(cbox, datatags, num_components_per_requirement, RandomMethod.max)
    components = genereate_components(cbox, num_components, num_requirements_per_component, datatags,
                                      RandomMethod.max)

    file_name = f'cbox_{num_components}c_{num_requirements_per_component}rpc' \
                f'_{num_components_per_requirement}cpr_{int(overlap * 100)}o.ttl'
    cbox.serialize(os.path.join(folder, file_name), format='turtle')


def generate_experiment_suite(folder: str):
    num_components = [5, 10, 100]
    num_requirements_per_component = [1, 2, 3, 4, 5]
    num_components_per_requirement = [1, 2, 3, 4, 5]
    overlap = 0
    for nc, nrpc, ncpr in tqdm(itertools.product(num_components, num_requirements_per_component,
                                                 num_components_per_requirement)):
        generate_fake_abox(nc, nrpc, ncpr, overlap, folder)


if __name__ == '__main__':
    generate_experiment_suite('./fake_cboxes')
