import itertools
import os
import sys
import time
import uuid
from datetime import datetime
from typing import Tuple, Any, List, Dict, Optional, Union, Set, Type
import random
import math

from pyshacl import validate
from tqdm import tqdm
from urllib.parse import quote

sys.path.append(os.path.join(os.path.abspath(os.path.join('..'))))
from common import *
from ontology_populator.implementations.core import *
from ontology_populator.implementations.knime.knime_implementation import KnimeParameter

def get_intent_iri(intent_graph: Graph) -> URIRef:
    intent_iri_query = f"""
PREFIX tb: <{tb}>
SELECT ?iri
WHERE {{
    ?iri a tb:Intent .
}}
"""
    result = intent_graph.query(intent_iri_query).bindings
    assert len(result) == 1
    return result[0]['iri']


def get_intent_dataset_task(intent_graph: Graph, intent_iri: URIRef) -> Tuple[URIRef, URIRef]:
    dataset_task_query = f"""
    PREFIX tb: <{tb}>
    SELECT ?dataset ?task ?algorithm
    WHERE {{
        {intent_iri.n3()} a tb:Intent .
        {intent_iri.n3()} tb:overData ?dataset .
        ?task tb:tackles {intent_iri.n3()} .
        OPTIONAL {{?algorithm tb:solves ?task}}
    }}
"""
    result = intent_graph.query(dataset_task_query).bindings[0]
    return result['dataset'], result['task'], result.get('algorithm', None)


def get_algorithms_from_task(ontology: Graph, task: URIRef) -> Tuple[URIRef, URIRef]:

    algorithm_task_query = f"""
    PREFIX tb: <{tb}>
    SELECT ?algorithm
    WHERE{{
        ?algorithm a tb:Algorithm ;
                   tb:solves {task.n3()} .
        ?impl tb:implements ?algorithm .
        FILTER NOT EXISTS{{
            ?algorithm a tb:Algorithm ;
                   tb:solves {task.n3()} .
            ?impl a tb:ApplierImplementation.
        }}
    }}
"""
    result = ontology.query(algorithm_task_query).bindings
    algos = [algo['algorithm'] for algo in result]
    return algos


def get_intent_info(intent_graph: Graph, intent_iri: Optional[URIRef] = None) -> \
        Tuple[URIRef, URIRef, List[Dict[str, Any]], URIRef]:
    if not intent_iri:
        intent_iri = get_intent_iri(intent_graph)

    dataset, task, algorithm = get_intent_dataset_task(intent_graph, intent_iri) 

    return dataset, task, algorithm, intent_iri 

def get_implementation_input_specs(ontology: Graph, implementation: URIRef) -> List[List[URIRef]]:
    input_spec_query = f"""
        PREFIX tb: <{tb}>
        SELECT ?shape
        WHERE {{
            {implementation.n3()} tb:specifiesInput ?spec .
            ?spec a tb:DataSpec ;
                tb:hasDatatag ?shape ;
                tb:has_position ?position .
            ?shape a tb:DataTag .
        }}
        ORDER BY ?position
    """
    results = ontology.query(input_spec_query).bindings
    shapes = [flatten_shape(ontology, result['shape']) for result in results]
    return shapes


def get_implementation_output_specs(ontology: Graph, implementation: URIRef) -> List[List[URIRef]]:
    output_spec_query = f"""
        PREFIX tb: <{tb}>
        SELECT ?shape
        WHERE {{
            {implementation.n3()} tb:specifiesOutput ?spec .
            ?spec a tb:DataSpec ;
                tb:hasDatatag ?shape ;
                tb:has_position ?position .
            ?shape a tb:DataTag .
        }}
        ORDER BY ?position
    """
    results = ontology.query(output_spec_query).bindings
    shapes = [flatten_shape(ontology, result['shape']) for result in results]
    return shapes


def flatten_shape(graph: Graph, shape: URIRef) -> List[URIRef]:
    if (shape, SH['and'], None) in graph:
        subshapes_query = f"""
            PREFIX sh: <{SH}>
            PREFIX rdf: <{RDF}>

            SELECT ?subshape
            WHERE {{
                {shape.n3()} sh:and ?andNode .
                ?andNode rdf:rest*/rdf:first ?subshape .
            }}
        """
        subshapes = graph.query(subshapes_query).bindings

        return [x for subshape in subshapes for x in flatten_shape(graph, subshape['subshape'])]
    else:
        return [shape]

def get_all_implementations(ontology: Graph, task_iri: URIRef = None, algorithm: URIRef = None) -> \
        List[Tuple[URIRef, List[URIRef]]]:
    main_implementation_query = f"""
    PREFIX tb: <{tb}>
    SELECT DISTINCT ?implementation
    WHERE {{
        ?implementation a tb:Implementation ;
            tb:implements {algorithm.n3() if algorithm is not None else '?algorithm'} .
        ?algorithm a tb:Algorithm ;
            tb:solves {task_iri.n3() if task_iri is not None else '?task'} .
        ?subtask tb:subtaskOf* {task_iri.n3() if task_iri is not None else '?task'} .
    }}
"""
    results = ontology.query(main_implementation_query).bindings
    implementations = [result['implementation'] for result in results]

    implementations_with_shapes = [
        (implementation, get_implementation_input_specs(ontology, implementation))
        for implementation in implementations]

    return implementations_with_shapes

def get_potential_implementations(ontology: Graph, task_iri: URIRef, algorithm: URIRef = None) -> \
        List[Tuple[URIRef, List[URIRef]]]:
    main_implementation_query = f"""
    PREFIX tb: <{tb}>
    SELECT DISTINCT ?implementation
    WHERE {{
        ?implementation a tb:Implementation ;
            tb:implements {algorithm.n3() if algorithm is not None else '?algorithm'} .
        ?algorithm a tb:Algorithm ;
            tb:solves {task_iri.n3() if task_iri is not None else '?task'} .
        ?subtask tb:subtaskOf* {task_iri.n3() if task_iri is not None else '?task'} .
        FILTER NOT EXISTS{{
            ?implementation a tb:ApplierImplementation.
        }}
    }}
"""
    results = ontology.query(main_implementation_query).bindings
    implementations = [result['implementation'] for result in results]
    print(f"FOCUSED IMPL: {implementations}")

    implementations_with_shapes = [
        (implementation, get_implementation_input_specs(ontology, implementation))
        for implementation in implementations]

    return implementations_with_shapes

def get_component_implementation(ontology: Graph, component: URIRef) -> URIRef:
    implementation_query = f"""
        PREFIX tb: <{tb}>
        PREFIX cb: <{cb}>
        SELECT ?implementation
        WHERE {{
            {component.n3()} tb:hasImplementation ?implementation .
        }}
    """
    result = ontology.query(implementation_query).bindings
    assert len(result) == 1
    return result[0]['implementation']

def get_implementation_components(ontology: Graph, implementation: URIRef) -> List[URIRef]:
    components_query = f"""
        PREFIX tb: <{tb}>
        SELECT ?component
        WHERE {{
            ?component tb:hasImplementation {implementation.n3()} .
        }}
    """
    results = ontology.query(components_query).bindings
    return [result['component'] for result in results]

def find_components_to_satisfy_shape(ontology: Graph, shape: URIRef, exclude_appliers: bool = False) -> List[URIRef]:
    implementation_query = f"""
        PREFIX tb: <{tb}>
        SELECT ?implementation
        WHERE {{
            {{
                ?implementation a tb:Implementation;
                                tb:specifiesOutput ?spec .
            }}
            FILTER NOT EXISTS {{
                ?implementation a tb:{'Applier' if exclude_appliers else ''}Implementation .
                                # tb:specifiesOutput ?spec .
            }}
            ?spec tb:hasDatatag {shape.n3()} .
        }}
    """
    result = ontology.query(implementation_query).bindings
    implementations = [x['implementation'] for x in result]
    components = [c
                  for implementation in implementations
                  for c in get_implementation_components(ontology, implementation)]
    return components

def identify_data_io(ontology: Graph, ios: List[List[URIRef]], train: bool = False, test: bool = False, return_index: bool = False) -> Union[int, List[URIRef]]:
    for i, io_shapes in enumerate(ios):
        for io_shape in io_shapes:
            if (io_shape, SH.targetClass, dmop.TabularDataset) in ontology or (io_shape, SH.targetClass, cb.TabularDatasetShape):
                if test:
                    test_query = f'''
                    PREFIX sh: <{SH}>
                    PREFIX rdfs: <{RDFS}>
                    PREFIX cb: <{cb}>
                    PREFIX dmop: <{dmop}>

                    ASK {{
                        {{
                        {io_shape.n3()} a sh:NodeShape ;
                                        sh:targetClass dmop:TabularDataset ;
                                        sh:property [
                                            sh:path dmop:isTestDataset ;
                                            sh:hasValue true
                                        ] .
                        }}
                    }}
                    '''
                    result = ontology.query(test_query).askAnswer
                    if result:
                        return i if return_index else io_shapes
                    
                if train:
                    train_query = f'''
                    PREFIX sh: <{SH}>
                    PREFIX rdfs: <{RDFS}>
                    PREFIX cb: <{cb}>
                    PREFIX dmop: <{dmop}>

                    ASK {{
                        {{
                        {io_shape.n3()} a sh:NodeShape ;
                                        sh:targetClass dmop:TabularDataset ;
                                        sh:property [
                                            sh:path dmop:isTrainDataset ;
                                            sh:hasValue true
                                        ] .
                        }}
                    }}
                    '''
                    result = ontology.query(train_query).askAnswer
                    if result:
                        return i if return_index else io_shapes
                
                if not train and not test:
                    return i if return_index else io_shapes
            
def identify_model_io(ontology: Graph, ios: List[List[URIRef]], return_index: bool = False) -> Union[int, List[URIRef]]:
    for i, io_shapes in enumerate(ios):
        for io_shape in io_shapes:
            query = f'''
    PREFIX sh: <{SH}>
    PREFIX rdfs: <{RDFS}>
    PREFIX cb: <{cb}>

    ASK {{
      {{
        {io_shape.n3()} sh:targetClass ?targetClass .
        ?targetClass rdfs:subClassOf* cb:Model .
      }}
      UNION
      {{
        {io_shape.n3()} rdfs:subClassOf* cb:Model .
      }}
    }}
'''
            if ontology.query(query).askAnswer:
                return i if return_index else io_shapes

def identify_visual_io(ontology: Graph, ios: List[List[URIRef]], return_index: bool = False) -> Union[int, List[URIRef]]:
    for i, io_shapes in enumerate(ios):
        for io_shape in io_shapes:
            query = f'''
    PREFIX sh: <{SH}>
    PREFIX rdfs: <{RDFS}>
    PREFIX cb: <{cb}>

    ASK {{
      {{
        {io_shape.n3()} sh:targetClass ?targetClass .
        ?targetClass rdfs:subClassOf* cb:Visualization .
      }}
      UNION
      {{
        {io_shape.n3()} rdfs:subClassOf* cb:Visualization .
      }}
    }}
'''
            if ontology.query(query).askAnswer:
                return i if return_index else io_shapes

def satisfies_shape(data_graph: Graph, shacl_graph: Graph, shape: URIRef, focus: URIRef) -> bool:
    # print(f'SHAPE: {shape.n3()}')
    conforms, g, report = validate(data_graph, shacl_graph=shacl_graph, validate_shapes=[shape], focus=focus)
    # print(f'REPORT: {report}')
    return conforms

def get_shape_target_class(ontology: Graph, shape: URIRef) -> URIRef:
    return ontology.query(f"""
        PREFIX sh: <{SH}>
        SELECT ?targetClass
        WHERE {{
            <{shape}> sh:targetClass ?targetClass .
        }}
    """).bindings[0]['targetClass']


def get_implementation_parameters(ontology: Graph, implementation: URIRef) -> Dict[
    URIRef, Tuple[Literal, Literal, Literal]]:
    parameters_query = f"""
        PREFIX tb: <{tb}>
        SELECT ?parameter ?value ?order ?condition
        WHERE {{
            <{implementation}> tb:hasParameter ?parameter .
            ?parameter tb:has_defaultvalue ?value ;
                       tb:has_condition ?condition ;
                       tb:has_position ?order .
        }}
        ORDER BY ?order
    """
    results = ontology.query(parameters_query).bindings
    return {param['parameter']: (param['value'], param['order'], param['condition']) for param in results}


# def get_component_overriden_parameters(ontology: Graph, component: URIRef) -> Dict[
#     URIRef, Tuple[Literal, Literal, Literal]]:
#     parameters_query = f"""
#         PREFIX tb: <{tb}>
#         SELECT ?parameter ?parameterSpecification ?parameterValue ?position ?condition
#         WHERE {{
#             {component.n3()} tb:overridesParameter ?parameterSpecification .
#             ?parameterSpecification tb:hasValue ?parameterValue .
#             ?parameter tb:specifiedBy ?parameterSpecification ;
#                        tb:has_position ?position ;
#                        tb:has_condition ?condition .
#         }}
#         ORDER BY ?position
#     """
#     results = ontology.query(parameters_query).bindings
#     # print(f"RESULTS: {results}")
#     # for param in results:
#     #     print(f"OVERRIDDEN PARAM: {component.n3()} ---> {param['parameter']}: {param['parameterValue']}")
#     return {param['parameter']: (param['parameterValue'], param['position'], param['condition']) for param in results}

def get_component_non_overriden_parameters(ontology: Graph, component: URIRef) -> Dict[
    URIRef, Tuple[Literal, Literal, Literal]]:
    parameters_query = f"""
        PREFIX tb: <{tb}>
        SELECT ?parameter ?parameterValue ?position ?condition
        WHERE {{
            {component.n3()} tb:hasImplementation ?implementation .
            ?implementation tb:hasParameter ?parameter .
            ?parameter tb:has_defaultvalue ?parameterValue ;
                       tb:has_position ?position ;
                       tb:has_condition ?condition .
            FILTER NOT EXISTS {{
                ?parameter tb:specifiedBy ?parameterSpecification .
            }}
        }}
        ORDER BY ?position
    """
    results = ontology.query(parameters_query).bindings
    # print(f"COMP: {component.n3()} ---> RESULTS: {results}")
    # for param in results:
    #     print(f"NONOVERRIDN PARAM: {component.n3()} ---> {param['parameter']}: {param['parameterValue']}")
    return {param['parameter']: (param['parameterValue'], param['position'], param['condition']) for param in results}


def get_component_parameters(ontology: Graph, component: URIRef) -> Dict[URIRef, Tuple[Literal, Literal, Literal]]:
    # implementation = get_component_implementation(ontology, component)
    # implementation_params = get_implementation_parameters(ontology, implementation)
    # print(f"BIMPL PARAMS: {implementation_params}")
    component_params = get_component_non_overriden_parameters(ontology, component)
    # print(f"CCOMP PARAMS: {component_params}")
    # implementation_params.update(component_params)
    # print(f"AIMPL PARAMS: {implementation_params}")
    return component_params

def test_function(ontology: Graph, component: URIRef):
    test_query = f"""

        PREFIX tb:<{tb}>
        SELECT ?component ?parameterSpec ?parameter ?parameterValue ?position
        WHERE{{
            BIND({component.n3()} AS ?component)
            ?component tb:overridesParameter ?parameterSpec .
            ?parameterSpec tb:hasValue ?parameterValue .
            ?parameter tb:specifiedBy ?parameterSpec ;
                       tb:has_position ?position .
        }}
    """
    results = ontology.query(test_query).bindings
    # print(f"TEST: {component.n3()} ---> {results}")
    print(f"RESULTS: {results}")


def get_component_overridden_paramspecs(ontology: Graph, workflow_graph: Graph, component: URIRef) -> Dict[URIRef, Tuple[URIRef, Literal]]:
    paramspecs_query = f"""

        PREFIX tb:<{tb}>
        SELECT ?parameterSpec ?parameter ?parameterValue ?position
        WHERE{{
            {component.n3()} tb:overridesParameter ?parameterSpec .
            ?parameterSpec tb:hasValue ?parameterValue .
            ?parameter tb:specifiedBy ?parameterSpec ;
                       tb:has_position ?position .
        }}
    """
    results = ontology.query(paramspecs_query).bindings
    # print(f"COMP: {component.n3()} ---> OVER: {results}")

    overridden_paramspecs = {paramspec['parameterSpec']: (paramspec['parameter'], paramspec['parameterValue'], paramspec['position']) for paramspec in results}
    
    # for paramspec in overridden_paramspecs.items():
    #     print(f"OVERRIDN PARAM: {component.n3()} ---> {paramspec[0]}: {paramspec[1][0]}, {paramspec[1][1]}")

    for paramspec, paramval_tup in overridden_paramspecs.items():
        param, value, _ = paramval_tup
        workflow_graph.add((paramspec, RDF.type, tb.ParameterSpecification))
        workflow_graph.add((param, tb.specifiedBy, paramspec))
        workflow_graph.add((paramspec, tb.hasValue, value))

    return overridden_paramspecs


def perform_param_substitution(graph: Graph, implementation: URIRef, parameters: Dict[URIRef, Tuple[Literal, Literal, Literal]],
                               inputs: List[URIRef], vis_necessities: Dict[str, List[str]] = None) -> Dict[URIRef, Tuple[Literal, Literal, Literal]]:
    
    keys = list(parameters.keys())
    for param in keys:
        value, order, condition = parameters[param]
        if condition.value is not None and condition.value != '':
            feature_types = get_inputs_feature_types(graph, inputs)
            if condition.value == '$$INTEGER_COLUMN$$' and int not in feature_types:
                parameters.pop(param)
                continue
            if condition.value == '$$STRING_COLUMN$$' and str not in feature_types:
                parameters.pop(param)
                continue
            if condition.value == '$$FLOAT_COLUMN$$' and float not in feature_types:
                parameters.pop(param)
                continue
        if isinstance(value.value, str) and '$$LABEL$$' in value.value:
            new_value = value.replace('$$LABEL$$', f'{get_inputs_label_name(graph, inputs)}')
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$NUMERIC_COLUMNS$$' in value.value:
            new_value = value.replace('$$NUMERIC_COLUMNS$$', f'{get_inputs_numeric_columns(graph, inputs)}')
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$CSV_PATH$$' in value.value:
            new_value = value.replace('$$CSV_PATH$$', f'{get_csv_path(graph, inputs)}')
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '&amp;' in value.value:
            new_value = value.replace('&amp;', '&')
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$PIE_CATEGORICAL$$' in value.value:
            new_value = value.replace('$$PIE_CATEGORICAL$$', vis_necessities['pie_cat'][0])
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$PIE_FREQUENCY$$' in value.value:
            new_value = value.replace('$$PIE_FREQUENCY$$', vis_necessities['pie_freq'][0] if vis_necessities['pie_freq'] != [] else '')
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$BAR_CATEGORICAL$$' in value.value:
            new_value = value.replace('$$BAR_CATEGORICAL$$', vis_necessities['bar_cat'][0])
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$BAR_FREQUENCY$$' in value.value:
            possible_cols = get_inputs_numeric_columns(graph, inputs)
            if condition.value == '$$BAR_INCLUDED$$':
                assert set(vis_necessities['bar_freq']).issubset(possible_cols)
                # new_value = value.replace('$$BAR_FREQUENCY$$', vis_necessities['bar_freq'])
                parameters[param] = (Literal(vis_necessities['bar_freq']), order, condition)
            elif condition.value == '$$BAR_EXCLUDED$$':
                excluded_cols = list(set(possible_cols) - set(vis_necessities['bar_freq']))
                parameters[param] = (Literal(excluded_cols), order, condition)
        if isinstance(value.value, str) and '$$HISTOGRAM_NUMERICAL$$' in value.value:
            new_value = value.replace('$$HISTOGRAM_NUMERICAL$$', vis_necessities['hist_num'][0])
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$HISTOGRAM_FREQUENCY$$' in value.value:
            possible_cols = get_inputs_numeric_columns(graph, inputs)
            if condition.value == '$$HISTOGRAM_INCLUDED$$':
                assert set(vis_necessities['hist_freq']).issubset(possible_cols)
                # new_value = value.replace('$$HISTOGRAM_FREQUENCY', vis_necessities['hist_freq'])
                parameters[param] = (Literal(vis_necessities['hist_freq']), order, condition)
            elif condition.value == '$$HISTOGRAM_EXCLUDED$$':
                excluded_cols = list(set(possible_cols) - set(vis_necessities['hist_freq'] + vis_necessities['hist_num']))
                parameters[param] = (Literal(excluded_cols), order, condition)
        if isinstance(value.value, str) and '$$SCATTERPLOT_COLUMN$$' in value.value:
            all_cols = get_inputs_all_columns(graph, inputs)
            assert set(vis_necessities['scat_cols']).issubset(all_cols)
            if condition.value == '$$SCATTERPLOT_X$$':
                new_value = value.replace('$$SCATTERPLOT_COLUMN$$', vis_necessities['scat_cols'][0])
                parameters[param] = (Literal(new_value), order, condition)
            elif condition.value == '$$SCATTERPLOT_Y$$':
                new_value = value.replace('$$SCATTERPLOT_COLUMN$$', vis_necessities['scat_cols'][1])
                parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$LINEPLOT_COLUMN$$' in value.value:
            all_cols = get_inputs_all_columns(graph, inputs)
            complete_cols = all_cols + ["<RowID>"]
            if condition.value == '$$LINEPLOT_X$$':
                assert vis_necessities['line_xcol'][0] in complete_cols
                new_value = value.replace('$$LINEPLOT_COLUMN$$', vis_necessities['line_xcol'][0])
                parameters[param] = (Literal(new_value), order, condition)
            elif condition.value == '$$LINEPLOT_INCLUDED$$':
                assert set(vis_necessities['line_ycols']).issubset(complete_cols)
                # new_value = value.replace('$$LINEPLOT_COLUMN$$', vis_necessities['line_ycols'])
                parameters[param] = (Literal(vis_necessities['line_ycols']), order, condition)
            elif condition.value == '$$LINEPLOT_EXCLUDED$$':
                excluded_cols = list(set(all_cols) - set(vis_necessities['line_ycols']))
                parameters[param] = (Literal(excluded_cols), order, condition)
        if isinstance(value.value, str) and '$$HEATMAP_CATEGORICAL$$' in value.value:
            cat_complete_cols = get_inputs_categorical_columns(graph, inputs) + ["<RowID>"]
            assert set(vis_necessities['heatmap_ycol']).issubset(cat_complete_cols) 
            new_value = value.replace('$$HEATMAP_CATEGORICAL$$', vis_necessities['heatmap_ycol'][0])
            parameters[param] = (Literal(new_value), order, condition)
        if isinstance(value.value, str) and '$$HEATMAP_NUMERICAL$$' in value.value:
            num_cols = get_inputs_numeric_columns(graph, inputs)
            if condition.value == '$$HEATMAP_INCLUDED$$':
                assert set(vis_necessities['heatmap_xcols']).issubset(num_cols)
                # new_value = value.replace('$$HEATMAP_NUMERICAL$$', vis_necessities['heatmap_xcols'])
                parameters[param] = (Literal(vis_necessities['heatmap_xcols']), order, condition)
            elif condition.value == '$$HEATMAP_EXCLUDED$$':
                excluded_cols = list(set(num_cols) - set(vis_necessities['heatmap_xcols']))
                parameters[param] = (Literal(excluded_cols), order, condition)

    return parameters


def assign_to_parameter_specs(graph: Graph,
                              parameters: Dict[URIRef, Tuple[Literal, Literal, Literal]])-> Dict[URIRef, Tuple[URIRef, Literal]]:
    
    keys = list(parameters.keys())
    param_specs = {}
    
    for param in keys:

        value, order, _ = parameters[param]
        uri = param.split('#')[-1] if '#' in param else param.split('/')[-1]
        param_spec = ab.term(quote(f'{uri}_{value}_specification'.replace(' ','_').lower(), safe=":/-_"))
        graph.add((param_spec, RDF.type, tb.ParameterSpecification))
        graph.add((param, tb.specifiedBy, param_spec))
        graph.add((param_spec, tb.hasValue, value))

        param_specs[param_spec] = (param, value, order)
    
    return param_specs


def add_step(graph: Graph, pipeline: URIRef, task_name: str, component: URIRef,
             parameter_specs: Dict[URIRef, Tuple[URIRef, Literal]],
             order: int, previous_task: Union[None, list, URIRef] = None, inputs: Optional[List[URIRef]] = None,
             outputs: Optional[List[URIRef]] = None) -> URIRef:
    if outputs is None:
        outputs = []
    if inputs is None:
        inputs = []
    step = ab.term(task_name)
    graph.add((pipeline, tb.hasStep, step))
    graph.add((step, RDF.type, tb.Step))
    graph.add((step, tb.runs, component))
    graph.add((step, tb.has_position, Literal(order)))
    for i, input in enumerate(inputs):
        in_node = BNode()
        graph.add((in_node, RDF.type, tb.Data))
        graph.add((in_node, tb.has_data, input))
        graph.add((in_node, tb.has_position, Literal(i)))
        graph.add((step, tb.hasInput, in_node))
    for o, output in enumerate(outputs):
        out_node = BNode()
        graph.add((out_node, RDF.type, tb.Data))
        graph.add((out_node, tb.has_data, output))
        graph.add((out_node, tb.has_position, Literal(o)))
        graph.add((step, tb.hasOutput, out_node))
    for param, *_ in parameter_specs.values():
        graph.add((step, tb.usesParameter, param))
    if previous_task:
        if isinstance(previous_task, list):
            for previous in previous_task:
                graph.add((previous, tb.followedBy, step))
        else:
            graph.add((previous_task, tb.followedBy, step))
    return step


def get_component_transformations(ontology: Graph, component: URIRef) -> List[URIRef]:
    transformation_query = f'''
        PREFIX tb: <{tb}>
        SELECT ?transformation
        WHERE {{
            <{component}> tb:hasTransformation ?transformation_list .
            ?transformation_list rdf:rest*/rdf:first ?transformation .
        }}
    '''
    transformations = ontology.query(transformation_query).bindings
    return [x['transformation'] for x in transformations]


def get_inputs_all_columns(graph: Graph, inputs: List[URIRef]) -> List:
    data_input = next(i for i in inputs if (i, RDF.type, dmop.TabularDataset) in graph)
    columns_query = f"""
        PREFIX rdfs: <{RDFS}>
        PREFIX dmop: <{dmop}>

        SELECT ?label
        WHERE {{
            {data_input.n3()} dmop:hasColumn ?column .
            ?column dmop:isFeature true ;
                    dmop:hasDataPrimitiveTypeColumn ?type ;
                    dmop:hasColumnName ?label .
        }}
    """
    columns = graph.query(columns_query).bindings
    return [x['label'].value for x in columns]


def get_inputs_label_name(graph: Graph, inputs: List[URIRef]) -> str:
    
    data_input = next(i for i in inputs if (i, RDF.type, dmop.TabularDataset) in graph) #inputs[0]

    label_query = f"""
        PREFIX rdfs: <{RDFS}>
        PREFIX dmop: <{dmop}>

        SELECT ?label
        WHERE {{
            {data_input.n3()} dmop:hasColumn ?column .
            ?column dmop:isLabel true ;
                    dmop:hasColumnName ?label .

        }}
    """
    
    results = graph.query(label_query).bindings
    
    if results is not None and len(results) > 0:
        return results[0]['label']
    

def get_exact_column(graph: Graph, inputs: List[URIRef], column_name: str) -> str:
    
    data_input = next(i for i in inputs if (i, RDF.type, dmop.TabularDataset) in graph) #inputs[0]

    column_query = f"""
        PREFIX rdfs: <{RDFS}>
        PREFIX dmop: <{dmop}>

        SELECT ?label
        WHERE {{
            {data_input.n3()} dmop:hasColumn ?column .
            ?column dmop:hasColumnName ?label .
            FILTER(?label = "{column_name}")
        }}
    """
    
    results = graph.query(column_query).bindings
    
    if results is not None and len(results) > 0:
        return results[0]['label']


def get_inputs_numeric_columns(graph: Graph, inputs: List[URIRef]) -> str:
    data_input = next(i for i in inputs if (i, RDF.type, dmop.TabularDataset) in graph)
    columns_query = f"""
        PREFIX rdfs: <{RDFS}>
        PREFIX dmop: <{dmop}>

        SELECT ?label
        WHERE {{
            {data_input.n3()} dmop:hasColumn ?column .
            ?column dmop:isFeature true ;
                    dmop:hasDataPrimitiveTypeColumn ?type ;
                    dmop:hasColumnName ?label .
            FILTER(?type IN (dmop:Float, dmop:Int, dmop:Number, dmop:Double, dmop:Long, dmop:Short, dmop:Integer))
        }}
    """
    columns = graph.query(columns_query).bindings
 
    return [x['label'].value for x in columns]


def get_inputs_categorical_columns(graph: Graph, inputs: List[URIRef]) -> str:
    data_input = next(i for i in inputs if (i, RDF.type, dmop.TabularDataset) in graph)

    categ_query = f"""
        PREFIX rdfs: <{RDFS}>
        PREFIX dmop: <{dmop}>

        SELECT ?label
        WHERE {{
            {data_input.n3()} dmop:hasColumn ?column .
            ?column dmop:isCategorical true ;
                    dmop:hasDataPrimitiveTypeColumn ?type ;
                    dmop:hasColumnName ?label .
        }}
    """
    columns = graph.query(categ_query).bindings

    return [x['label'].value for x in columns]


def get_csv_path(graph: Graph, inputs: List[URIRef]) -> str:
    data_input = next(i for i in inputs if (i, RDF.type, dmop.TabularDataset) in graph)
    path = next(graph.objects(data_input, dmop.path), True)
    return path.value


def get_inputs_feature_types(graph: Graph, inputs: List[URIRef]) -> Set[Type]:
    data_input = next(i for i in inputs if (i, RDF.type, dmop.TabularDataset) in graph)
    columns_query = f"""
        PREFIX rdfs: <{RDFS}>
        PREFIX dmop: <{dmop}>

        SELECT ?type
        WHERE {{
            {data_input.n3()} dmop:hasColumn ?column .
            ?column dmop:isFeature true ;
                    dmop:hasDataPrimitiveTypeColumn ?type .
        }}
    """
    columns = graph.query(columns_query).bindings
    mapping = {
        dmop.Float: float,
        dmop.Int: int,
        dmop.Integer: int,
        dmop.Number: float,
        dmop.Double: float,
        dmop.String: str,
        dmop.Boolean: bool,
    }
    return set([mapping[x['type']] for x in columns])


def copy_subgraph(source_graph: Graph, source_node: URIRef, destination_graph: Graph, destination_node: URIRef,
                  replace_nodes: bool = True) -> None:
    visited_nodes = set()
    nodes_to_visit = [source_node]
    mappings = {source_node: destination_node}

    while nodes_to_visit:
        current_node = nodes_to_visit.pop()
        visited_nodes.add(current_node)
        for predicate, object in source_graph.predicate_objects(current_node):
            if predicate == OWL.sameAs:
                continue
            if replace_nodes and isinstance(object, IdentifiedNode):
                if predicate == RDF.type or object in dmop:
                    mappings[object] = object
                else:
                    if object not in visited_nodes:
                        nodes_to_visit.append(object)
                    if object not in mappings:
                        mappings[object] = BNode()
                destination_graph.add((mappings[current_node], predicate, mappings[object]))
            else:
                destination_graph.add((mappings[current_node], predicate, object))


def annotate_io_with_spec(ontology: Graph, workflow_graph: Graph, io: URIRef, io_spec: List[URIRef]) -> None:
    
    for spec in io_spec:
        io_spec_class = next(ontology.objects(spec, SH.targetClass, True), None)
        if io_spec_class is None or (io, RDF.type, io_spec_class) in workflow_graph:
            continue
        workflow_graph.add((io, RDF.type, io_spec_class))


def annotate_ios_with_specs(ontology: Graph, workflow_graph: Graph, data_io: List[URIRef],
                            specs: List[List[URIRef]]) -> None:
    assert len(data_io) == len(specs), 'Number of IOs and specs must be the same'
    for io, spec in zip(data_io, specs):
        annotate_io_with_spec(ontology, workflow_graph, io, spec)


def run_copy_transformation(ontology: Graph, workflow_graph: Graph, transformation: URIRef, inputs: List[URIRef],
                            outputs: List[URIRef]):
    input_index = next(ontology.objects(transformation, tb.copy_input, True)).value
    output_index = next(ontology.objects(transformation, tb.copy_output, True)).value
    input = inputs[input_index - 1]
    output = outputs[output_index - 1]

    copy_subgraph(workflow_graph, input, workflow_graph, output)


def run_component_transformation(ontology: Graph, workflow_graph: Graph, component: URIRef, inputs: List[URIRef],
                                 outputs: List[URIRef],
                                 parameters_specs: Dict[URIRef, Tuple[URIRef, Literal, Literal]]) -> None:
    transformations = get_component_transformations(ontology, component)
    for transformation in transformations:
        if (transformation, RDF.type, tb.CopyTransformation) in ontology:
            run_copy_transformation(ontology, workflow_graph, transformation, inputs, outputs)
        elif (transformation, RDF.type, tb.LoaderTransformation) in ontology:
            continue
        else:
            prefixes = f'''
PREFIX tb: <{tb}>
PREFIX ab: <{ab}>
PREFIX rdf: <{RDF}>
PREFIX rdfs: <{RDFS}>
PREFIX owl: <{OWL}>
PREFIX xsd: <{XSD}>
PREFIX dmop: <{dmop}>
'''
            query = next(ontology.objects(transformation, tb.transformation_query, True)).value
            query = prefixes + query
            for i in range(len(inputs)):
                query = query.replace(f'$input{i + 1}', f'{inputs[i].n3()}')
            for i in range(len(outputs)):
                query = query.replace(f'$output{i + 1}', f'{outputs[i].n3()}')
            # print(f"PARAM SPECS: {parameters_specs}")
            for param_spec, (param, value, order) in parameters_specs.items():
                query = query.replace(f'$param{order + 1}', f'{value.n3()}')
                query = query.replace(f'$parameter{order + 1}', f'{value.n3()}')
            workflow_graph.update(query)


def retreive_component_rules(graph: Graph, task:URIRef, component: URIRef):
    preference_query = f"""
        PREFIX rdfs: <{RDFS}>

        SELECT ?datatag ?weight ?component_rank
        WHERE {{
            {component.n3()} tb:hasRule ?rule .
            ?rule tb:relatedtoDatatag ?datatag ;
                  tb:relatedtoTask {task.n3()} ;
                  tb:has_rank ?component_rank .
            ?datatag tb:has_weight ?weight .
        }}
    """
    results = graph.query(preference_query).bindings

    return {result['datatag']: (float(result['weight']), int(result['component_rank'])) for result in results}


def get_best_components(graph: Graph, task: URIRef, components: List[URIRef], dataset: URIRef, percentage: float = None):

    preferred_components = {}
    sorted_components = {}
    for component in components:
        
        component_rules = retreive_component_rules(graph, task, component)
        # print(f'RULES: {component_rules}')
        score = 0

        preferred_components[component] = score

        for datatag, weight_rank in component_rules.items():
            rule_weight = weight_rank[0]
            component_rank = weight_rank[1]
            if satisfies_shape(graph, graph, datatag, dataset):
                score+=rule_weight
            else:
                score-=rule_weight
                
            preferred_components[component] = (score, component_rank)
        
    # print(f'BEFORE SORTING: {preferred_components}')
    sorted_preferred = sorted(preferred_components.items(), key=lambda x: x[1][0], reverse=True)
    # print(f'AFTERI SORTING: {sorted_preferred}')

    if len(sorted_preferred) > 0: ### there are multiple components to choose from
        best_scores = set([comp[1] for comp in sorted_preferred])
        print(f'SCORES: {best_scores}')
        if len(best_scores) == 1:
            sorted_preferred = random.sample(sorted_preferred, int(math.ceil(len(sorted_preferred)*percentage))) if percentage else sorted_preferred
        elif len(best_scores) > 1: ### checking if there is at least one superior component
            sorted_preferred = [x for x in sorted_preferred if x[1] >= sorted_preferred[0][1]]
        # else:
        #     sorted_preferred = random.sample(sorted_preferred, int(math.ceil(len(sorted_preferred)*percentage)))
    # print(f'AFTERI SORTING: {sorted_preferred}')

    for comp, rules_nbr in sorted_preferred:
        sorted_components[comp] = rules_nbr 
    # print(f'AFTER SORTING: {sorted_components}')

    return sorted_components

    


def get_step_name(workflow_name: str, task_order: int, implementation: URIRef) -> str:
    return f'{workflow_name}-step_{task_order}_{implementation.fragment.replace("-", "_")}'


def add_loader_step(ontology: Graph, workflow_graph: Graph, workflow: URIRef, dataset_node: URIRef) -> URIRef:
    loader_component = cb.term('component-csv_local_reader')
    # loader_implementation = get_component_implementation(loader_component)
    loader_step_name = get_step_name(workflow.fragment, 0, loader_component)
    loader_parameters = get_component_parameters(ontology, loader_component)
    loader_overridden_paramspecs = get_component_overridden_paramspecs(ontology, workflow_graph, loader_component)
    # loader_overridden_parameters = get_component_overriden_parameters(ontology, loader_component)
    loader_parameters = perform_param_substitution(workflow_graph, None, loader_parameters, [dataset_node])
    # loader_parameters.update(loader_overridden_parameters)
    loader_param_specs = assign_to_parameter_specs(workflow_graph, loader_parameters)
    loader_param_specs.update(loader_overridden_paramspecs)
    return add_step(workflow_graph, workflow, loader_step_name, loader_component, loader_param_specs, 0, None, None,
                    [dataset_node])


def build_general_workflow(workflow_name: str, ontology: Graph, dataset: URIRef, main_component: URIRef,
                           transformations: List[URIRef], vis_necessities: Dict[str, List[str]] = None) -> Tuple[Graph, URIRef]:
    workflow_graph = get_graph_xp()
    workflow = ab.term(workflow_name)
    workflow_graph.add((workflow, RDF.type, tb.Workflow))
    task_order = 0

    dataset_node = ab.term(f'{workflow_name}-original_dataset')

    copy_subgraph(ontology, dataset, workflow_graph, dataset_node)

    loader_step = add_loader_step(ontology, workflow_graph, workflow, dataset_node)
    task_order += 1

    previous_step = loader_step
    previous_train_step = loader_step
    previous_test_step = None

    previous_node = dataset_node
    train_dataset_node = dataset_node
    test_dataset_node = None


    for train_component in [*transformations, main_component]:
    
        test_component = next(ontology.objects(train_component, tb.hasApplier, True), None)#, train_component)
        same = train_component == test_component
        train_component_implementation = get_component_implementation(ontology, train_component)


        if not test_component:
            
            singular_component = train_component
            # test_function(ontology, singular_component)
            singular_step_name = get_step_name(workflow_name, task_order, singular_component)
            singular_component_implementation = get_component_implementation(ontology, singular_component)
            singular_input_specs = get_implementation_input_specs(ontology, singular_component_implementation)
            singular_input_data_index = identify_data_io(ontology, singular_input_specs, return_index=True)
            singular_transformation_inputs = None
            if singular_input_data_index is not None:
                singular_transformation_inputs = [ab[f'{singular_step_name}-input_{i}'] for i in range(len(singular_input_specs))]
                singular_transformation_inputs[singular_input_data_index] = previous_node
                annotate_ios_with_specs(ontology, workflow_graph, singular_transformation_inputs,
                                        singular_input_specs)
            singular_output_specs = get_implementation_output_specs(ontology, singular_component_implementation)
            singular_transformation_outputs = [ab[f'{singular_step_name}-output_{i}'] for i in range(len(singular_output_specs))]
            annotate_ios_with_specs(ontology, workflow_graph, singular_transformation_outputs,
                                singular_output_specs)
            
            singular_parameters = get_component_parameters(ontology, singular_component)
            singular_overridden_parameters = get_component_overridden_paramspecs(ontology, workflow_graph, singular_component)
            # singular_overridden_parameters = get_component_overriden_parameters(ontology, singular_component)
            singular_parameters = perform_param_substitution(graph=workflow_graph, parameters=singular_parameters,
                                                                implementation=singular_component_implementation,
                                                                inputs=singular_transformation_inputs,
                                                                vis_necessities=vis_necessities)
            # singular_parameters.update(singular_overridden_parameters)
            # print(f'SINGLE: {singular_component}: {singular_parameters}')
            singular_param_specs = assign_to_parameter_specs(workflow_graph, singular_parameters)
            # print(f"NEW PARAM SPECS: {singular_param_specs}")
            # print(f"OVR PARAM SPECS: {singular_overridden_parameters}")
            singular_param_specs.update(singular_overridden_parameters)
            # print(f"PARAM SPECS: {singular_param_specs}")
            # singular_params_merged = join_dicts(singular_parameters, singular_param_specs)
            singular_step = add_step(workflow_graph, workflow,
                                singular_step_name,
                                singular_component,
                                # singular_params_merged,
                                singular_param_specs,
                                task_order, previous_step,
                                [previous_node],
                                singular_transformation_outputs)
            run_component_transformation(ontology, workflow_graph, singular_component,
                                            [previous_node], singular_transformation_outputs, singular_param_specs)
                                            #singular_params_merged)


            train_dataset_index = identify_data_io(ontology, singular_output_specs, train=True, return_index=True)
            
            test_dataset_index = identify_data_io(ontology, singular_output_specs, test=True, return_index=True)

            if train_dataset_index is not None:
                train_dataset_node =  singular_transformation_outputs[train_dataset_index]
            if test_dataset_index is not None:
                test_dataset_node = singular_transformation_outputs[test_dataset_index]
                
            previous_step = singular_step
            previous_train_step = singular_step
            previous_test_step = singular_step
            
            task_order += 1

        else:

            train_step_name = get_step_name(workflow_name, task_order, train_component)

            # test_function(ontology, train_component)

            train_component_implementation = get_component_implementation(ontology, train_component)

            train_input_specs = get_implementation_input_specs(ontology, train_component_implementation)
            train_input_data_index = identify_data_io(ontology, train_input_specs, return_index=True)
            train_transformation_inputs = [ab[f'{train_step_name}-input_{i}'] for i in range(len(train_input_specs))]
            train_transformation_inputs[train_input_data_index] = train_dataset_node 
            annotate_ios_with_specs(ontology, workflow_graph, train_transformation_inputs,
                                    train_input_specs)

            train_output_specs = get_implementation_output_specs(ontology, train_component_implementation)
            train_output_model_index = identify_model_io(ontology, train_output_specs, return_index=True)
            train_output_data_index = identify_data_io(ontology, train_output_specs, return_index=True)
            train_transformation_outputs = [ab[f'{train_step_name}-output_{i}'] for i in range(len(train_output_specs))]
            annotate_ios_with_specs(ontology, workflow_graph, train_transformation_outputs,
                                    train_output_specs)

            train_parameters = get_component_parameters(ontology, train_component)
            train_parameters = perform_param_substitution(graph=workflow_graph, implementation=train_component_implementation,
                                                            parameters=train_parameters,
                                                            inputs=train_transformation_inputs)
            # train_overridden_parameters = get_component_overriden_parameters(ontology, train_component)
            train_overridden_paramspecs = get_component_overridden_paramspecs(ontology, workflow_graph, train_component)
            # train_parameters.update(train_overridden_parameters)
            # print(f'TRAIN: {train_component}: {train_parameters}')
            train_param_specs = assign_to_parameter_specs(workflow_graph, train_parameters)
            # print(f"NEW PARAM SPECS: {train_param_specs}")
            # print(f"OVR PARAM SPECS: {train_overridden_parameters}")
            train_param_specs.update(train_overridden_paramspecs)
            # train_params_merged = join_dicts(train_parameters, train_param_specs)
            train_step = add_step(workflow_graph, workflow,
                                train_step_name,
                                train_component,
                                train_param_specs,
                                # train_params_merged,
                                task_order, previous_train_step,
                                train_transformation_inputs,
                                train_transformation_outputs)

            previous_train_step = train_step 

            run_component_transformation(ontology, workflow_graph, train_component, train_transformation_inputs,
                                        train_transformation_outputs, train_param_specs)
                                        # train_params_merged)

            if train_output_data_index is not None:
                train_dataset_node = train_transformation_outputs[train_output_data_index]

            previous_step = train_step
            previous_node = train_dataset_node

            task_order += 1

            if test_dataset_node is not None:

                test_step_name = get_step_name(workflow_name, task_order, test_component)

                # test_function(ontology, test_component)

                test_input_specs = get_implementation_input_specs(ontology,
                                                                get_component_implementation(ontology, test_component))
                test_input_data_index = identify_data_io(ontology, test_input_specs, test=True, return_index=True)
                test_input_model_index = identify_model_io(ontology, test_input_specs, return_index=True)
                test_transformation_inputs = [ab[f'{test_step_name}-input_{i}'] for i in range(len(test_input_specs))]
                test_transformation_inputs[test_input_data_index] = test_dataset_node
                if train_output_model_index is not None:
                    test_transformation_inputs[test_input_model_index] = train_transformation_outputs[train_output_model_index]
                annotate_ios_with_specs(ontology, workflow_graph, test_transformation_inputs,
                                        test_input_specs)
                
                test_implementation = get_component_implementation(ontology, test_component)
                print(f'TEST IMPL: {test_implementation}')
                test_output_specs = get_implementation_output_specs(ontology, test_implementation)
                print(f'TEST OUT SPECS: {test_output_specs}')
                test_output_data_index = identify_data_io(ontology, test_output_specs, return_index=True)
                print(f'TEST OUT INDEX: {test_output_data_index}')
                test_transformation_outputs = [ab[f'{test_step_name}-output_{i}'] for i in range(len(test_output_specs))]
                annotate_ios_with_specs(ontology, workflow_graph, test_transformation_outputs,
                                        test_output_specs)

                previous_test_steps = [previous_test_step, train_step] if not same else [previous_test_step]
                test_parameters = get_component_parameters(ontology, test_component)
                test_component_implementation = get_component_implementation(ontology, test_component) if test_component else None
                test_parameters = perform_param_substitution(workflow_graph, test_component_implementation, test_parameters, test_transformation_inputs)
                # test_overridden_parameters = get_component_overriden_parameters(ontology, test_component)
                # test_parameters.update(test_overridden_parameters)
                # print(f'TEST: {test_component}: {test_parameters}')
                test_overridden_paramspecs = get_component_overridden_paramspecs(ontology, workflow_graph, train_component)
                test_param_specs = assign_to_parameter_specs(workflow_graph, test_parameters)
                # print(f"NEW PARAM SPECS: {test_param_specs}")
                # print(f"OVR PARAM SPECS: {test_overridden_parameters}")
                test_param_specs.update(test_overridden_paramspecs)
                # test_params_merged = join_dicts(test_parameters, test_param_specs)
                test_step = add_step(workflow_graph, workflow,
                                    test_step_name,
                                    test_component,
                                    test_param_specs,
                                    # test_params_merged,
                                    task_order, previous_test_steps,
                                    test_transformation_inputs,
                                    test_transformation_outputs)

                run_component_transformation(ontology, workflow_graph, test_component, test_transformation_inputs,
                                            test_transformation_outputs, test_param_specs)
                                            # test_params_merged)
                
                print(f'TEST OUTPUT{test_output_data_index}: {test_transformation_outputs}')
                test_dataset_node = test_transformation_outputs[test_output_data_index]
                previous_test_step = test_step
                task_order += 1
            
    
    if test_dataset_node is not None:
        saver_component = cb.term('component-csv_local_writer')
        saver_step_name = get_step_name(workflow_name, task_order, saver_component)
        saver_parameters = get_component_parameters(ontology, saver_component)
        saver_implementation = get_component_implementation(ontology, saver_component)
        saver_parameters = perform_param_substitution(workflow_graph, saver_implementation, saver_parameters, [test_dataset_node])
        # saver_overridden_parameters = get_component_overriden_parameters(ontology, saver_component)
        saver_overridden_paramspecs = get_component_overridden_paramspecs(ontology, workflow_graph, saver_component)
        # saver_parameters.update(saver_overridden_parameters)
        print(f'SAVE: {saver_component}: {saver_parameters}')
        saver_param_specs = assign_to_parameter_specs(workflow_graph, saver_parameters)
        saver_param_specs.update(saver_overridden_paramspecs)
        # saver_params_merged = join_dicts(saver_parameters, saver_param_specs)
        add_step(workflow_graph,
                workflow,
                saver_step_name,
                saver_component,
                saver_param_specs,
                # saver_params_merged, 
                task_order,
                previous_test_step, [test_dataset_node], [])

    return workflow_graph, workflow


def get_exposed_parameters(ontology: Graph, algorithm: URIRef):
    expparams_query = f"""
        PREFIX tb: <{tb}>
        SELECT DISTINCT ?exp_param
        WHERE {{
            {algorithm.n3()} a tb:Algorithm .
            ?imp tb:implements {algorithm.n3()} .
            ?com tb:hasImplementation ?imp ;
                tb:exposesParameter ?exp_param .
        }}
"""
    result = ontology.query(expparams_query).bindings
    return result

def build_workflows(ontology: Graph, intent_graph: Graph, destination_folder: str, log: bool = False) -> None:
    
    dataset, task, algorithm, intent_iri = get_intent_info(intent_graph)
    # algorithm = get_algorithms_from_task(ontology, task) if algorithm is None else [algorithm]

    if log:
        tqdm.write(f'Intent: {intent_iri.fragment}')
        tqdm.write(f'Dataset: {dataset.fragment}')
        tqdm.write(f'Task: {task.fragment}')
        tqdm.write(f'Algorithm: {algorithm.fragment if algorithm is not None else [algo.fragment for algo in get_algorithms_from_task(ontology, task)]}')
        # tqdm.write(f'Intent params: {intent_params}')
        tqdm.write('-------------------------------------------------')

    # exposed_params = [get_exposed_parameters(ontology, alg) for alg in algorithm]
    # print(f'EXPOSED PARAMS: {exposed_params}')

    vis_necessities = {}
    if task.fragment == 'DataVisualization':
        vis_necessities = {
            'pie_cat':[],
            'pie_freq':[],
            'bar_cat':[],
            'bar_freq':[],
            'hist_num':[],
            'hist_freq':[],
            'scat_cols':[],
            'line_xcol':[],
            'line_ycols':[],
            'heatmap_ycol':[],
            'heatmap_xcols':[]
        }
        all_cols = get_inputs_all_columns(ontology, [dataset])
        complete_cols = all_cols + ["<RowID>"]
        cat_cols = get_inputs_categorical_columns(ontology, [dataset])
        num_cols = get_inputs_numeric_columns(ontology, [dataset])
        if algorithm[0].fragment == 'PieChart':
            vis_necessities['pie_cat'] = [input(f"Enter the column from the following {cat_cols}:") or cat_cols[0]]

            vis_necessities['pie_freq'].append(input(f"Enter one of the following columns {num_cols}:" or num_cols[0]))

        elif algorithm[0].fragment == 'BarChart':
            vis_necessities['bar_cat'] = [input(f"Enter the column from the following {cat_cols}:") or cat_cols[0]]
            
            freq_option = [(input("Are there frequency columns you want to include [Yes or No]:") or 'No').lower()]

            if freq_option != 'no':

                freq_num = int(input("How many frequency columns you want to include:"))

                for i in range(freq_num):
                    vis_necessities['bar_freq'].append(input(f"Enter one of the following columns {num_cols}:" or num_cols[0]))
        
        elif algorithm[0].fragment == 'Histogram':
            vis_necessities['hist_num'] = [input(f"Enter the column from the following {num_cols}:") or num_cols[0]]
            
            freq_option = [(input("Are there frequency columns you want to include [Yes or No]:") or 'No').lower()]

            if freq_option != 'no':

                freq_num = int(input("How many frequency columns you want to include:"))

                for i in range(freq_num):
                    vis_necessities['hist_freq'].append(input(f"Enter one of the following columns {num_cols}:") or num_cols[0])

        elif algorithm[0].fragment == 'ScatterPlot':

            vis_necessities['scat_cols'].append(input(f"Enter the column on the x-axis {all_cols}:") or all_cols[0])
            vis_necessities['scat_cols'].append(input(f"Enter the column on the y-axis {all_cols}:") or all_cols[0])

        elif algorithm[0].fragment == 'LinePlot':

            vis_necessities['line_xcol'].append(input(f"Enter the x-axis column {complete_cols}") or complete_cols[-1])
            y_num = int(input("Enter the number of y-axis columns:")) or 0

            # vis_necessities['freq_cols'] = []
            for i in range(y_num):
                vis_necessities['line_ycols'].append(input(f"Enter the y-axis column {all_cols}") or all_cols[0])

        elif algorithm[0].fragment == 'HeatMap':

            vis_necessities['heatmap_ycol'].append(input(f'Enter the y-axis column {cat_cols + ["<RowID>"]}') or cat_cols[-1])
            x_num = int(input("Enter the number of x-axis columns:")) or 0

            # vis_necessities['x_cols'] = []
            for i in range(x_num):
                vis_necessities['heatmap_xcols'].append(input(f"Enter the x-axis column {num_cols}") or num_cols[0])


    impls = get_potential_implementations(ontology, task, algorithm)
    print(f'IMPLS: {impls}')
    components = [
        (c, impl, inputs)
        for impl, inputs in impls
        for c in get_implementation_components(ontology, impl)
    ]

    # for i, (com, imp, inp) in enumerate(components):
    #     print(f'{i}: {com}, {imp}, {inp}')
    # print('-----------------------------------------------------')

    if log:
        for component, implementation, inputs in components:
            tqdm.write(f'Component: {component.fragment} ({implementation.fragment})')
            for im_input in inputs:
                tqdm.write(f'\tInput: {[x.fragment for x in im_input]}')
        tqdm.write('-------------------------------------------------')

    workflow_order = 0

    for component, implementation, inputs in tqdm(components, desc='Components', position=1):
        if log:
            tqdm.write(f'Component: {component.fragment} ({implementation.fragment})')
        shapes_to_satisfy = identify_data_io(ontology, inputs)
        assert shapes_to_satisfy is not None and len(shapes_to_satisfy) > 0
        if log:
            tqdm.write(f'\tData input: {[x.fragment for x in shapes_to_satisfy]}')

        unsatisfied_shapes = [shape for shape in shapes_to_satisfy if
                              not satisfies_shape(ontology, ontology, shape, dataset)]
        print(f'UNSATISFIED SHAPES: {unsatisfied_shapes}')
        available_transformations = {
            shape: find_components_to_satisfy_shape(ontology, shape, exclude_appliers=True)
            for shape in unsatisfied_shapes
        }
        print(f'AVAILABLE TRANSFORMATIONS: {available_transformations}')

        for tr, methods in available_transformations.items():
            # print(f'Possible Components for {tr} --> {methods}')
            best_components = get_best_components(ontology, task, methods, dataset)

            # print(f'PREFERRED COMPONENTS: {best_components}')

            available_transformations[tr] = list(best_components.keys())

        print(f'REFINED TRANSFORMATIONS: {available_transformations}')
                    


        if log:
            tqdm.write(f'\tUnsatisfied shapes: ')
            for shape, transformations in available_transformations.items():
                tqdm.write(f'\t\t{shape.fragment}: {[x.fragment for x in transformations]}')

        transformation_combinations = list(
            enumerate(itertools.product(*available_transformations.values())))
            
        # TODO - check if the combination is valid and whether further transformations are needed

        if log:
            tqdm.write(f'\tTotal combinations: {len(transformation_combinations)}')

        for i, transformation_combination in tqdm(transformation_combinations, desc='Transformations', position=0,
                                                  leave=False):
            if log:
                tqdm.write(
                    f'\t\tCombination {i + 1} / {len(transformation_combinations)}: {[x.fragment for x in transformation_combination]}')

            workflow_name = f'workflow_{workflow_order}_{intent_iri.fragment}_{uuid.uuid4()}'.replace('-', '_')

            wg, w = build_general_workflow(workflow_name, ontology, dataset, component,
                                           transformation_combination, vis_necessities=vis_necessities)

            wg.add((w, tb.generatedFor, intent_iri))
            wg.add((intent_iri, RDF.type, tb.Intent))

            if log:
                tqdm.write(f'\t\tWorkflow {workflow_order}: {w.fragment}')
            wg.serialize(os.path.join(destination_folder, f'{workflow_name}.ttl'), format='turtle')
            workflow_order += 1

def interactive():
    intent_graph = get_graph_xp()
    intent = input('Introduce the intent name [ClassificationIntent]: ') or 'ClassificationIntent' #or 'VisualizationIntent'
    data = input('Introduce the data name [titanic.csv]: ') or 'titanic.csv'
    task = input('Introduce the problem name [Classification]: ') or 'Classification' #or 'DataVisualization'

    

    vis_algorithms = {"piechart": cb.PieChart,
                      "barchart": cb.BarChart,
                      "scatterplot": cb.ScatterPlot,
                      "histogram": cb.Histogram,
                      "lineplot": cb.LinePlot,
                      "heatmap": cb.HeatMap}

    intent_graph.add((ab.term(intent), RDF.type, tb.Intent))
    intent_graph.add((ab.term(intent), tb.overData, ab.term(data)))
    intent_graph.add((cb.term(task), tb.tackles, ab.term(intent)))

    if task == 'DataVisualization':
        vis_algorithm = vis_algorithms[str(input('Choose the Visualization Method:\n-Pie Chart\n-Bar Chart\n-Histogram\n-Scatter Plot\n-Line Plot\n-Heatmap') or 'BarChart').replace(" ","").lower()]
        if vis_algorithm is not None:
            intent_graph.add((vis_algorithm, tb.solves, cb.term(task)))


    ontology = get_ontology_graph()

    folder = input('Introduce the folder to save the workflows: ')
    if folder == '':
        folder = f'./workflows/{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}/'
        tqdm.write(f'No folder introduced, using default ({folder})')
    if not os.path.exists(folder):
        tqdm.write('Directory does not exist, creating it')
        os.makedirs(folder)

    t = time.time()
    build_workflows(ontology, intent_graph, folder, log=True)
    t = time.time() - t

    print(f'Workflows built in {t} seconds')
    print(f'Workflows saved in {folder}')


# interactive()