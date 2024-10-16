import zipfile
import sys
import os

from rdflib.term import Node

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from pipeline_generator.optimized_pipeline_generator import *


def abstract_planner(ontology: Graph, intent: Graph) -> Tuple[
    Dict[Node, Dict[Node, List[Node]]], Dict[Node, List[Node]]]:
    dataset, task, algorithm, intent_iri = get_intent_info(intent)

    algs = get_algorithms_from_task(ontology, task)

    impls = get_potential_implementations(ontology, task, algorithm)

    algs_shapes = {}
    alg_plans = {alg: [] for alg in algs}
    for impl in impls:
        alg = next(ontology.objects(impl[0], tb.implements)), 
        (impl[0], RDF.type, tb.Implementation) in ontology and (tb.ApplierImplementation not in ontology.objects(impl[0], RDF.type))

        algs_shapes[alg[0]] = impl[1::][0][0]

        alg_plans[alg[0]].append(impl)

    
    plans = {}
    for alg in algs:
        if cb.TrainTabularDatasetShape in algs_shapes[alg]:
            trainer = cb.term(alg.fragment + '-Train')
            plans[alg] = {
                cb.DataLoading: [cb.TrainTestSplit],
                cb.TrainTestSplit: [trainer, alg],
                trainer: [alg],
                alg: [cb.DataStoring],
                cb.DataStoring: []
            }
        else:
            plans[alg] = {
                cb.DataLoading: [alg],
                alg: [],
            }

    return plans, alg_plans


def workflow_planner(ontology: Graph, implementations: List, intent: Graph):
    dataset, task, algorithm, intent_iri = get_intent_info(intent)
    components = [
        (c, impl, inputs)
        for impl, inputs in implementations
        for c in get_implementation_components(ontology, impl)
    ]
    workflow_order = 0

    workflows = []

    for component, implementation, inputs in tqdm(components, desc='Components', position=1):
        shapes_to_satisfy = identify_data_io(ontology, inputs)
        assert shapes_to_satisfy is not None and len(shapes_to_satisfy) > 0

        unsatisfied_shapes = [shape for shape in shapes_to_satisfy if
                              not satisfies_shape(ontology, ontology, shape, dataset)]

        available_transformations = {
            shape: find_components_to_satisfy_shape(ontology, shape, exclude_appliers=True)
            for shape in unsatisfied_shapes
        }

        for transformation, methods in available_transformations.items():
            best_components = get_best_components(ontology, methods, dataset)

            available_transformations[transformation] = list(best_components.keys())


        transformation_combinations = list(
            enumerate(itertools.product(*available_transformations.values())))
        # TODO - check if the combination is valid and whether further transformations are needed

        for i, transformation_combination in tqdm(transformation_combinations, desc='Transformations', position=0,
                                                  leave=False):
            workflow_name = f'workflow_{workflow_order}_{intent_iri.fragment}_{uuid.uuid4()}'.replace('-', '_')
            wg, w = build_general_workflow(workflow_name, ontology, dataset, component,
                                              transformation_combination) #need to add visualization details

            wg.add((w, tb.generatedFor, intent_iri))
            wg.add((intent_iri, RDF.type, tb.Intent))

            workflows.append(wg)
            workflow_order += 1
    return workflows


def logical_planner(ontology: Graph, workflow_plans: List[Graph]):
    logical_plans = {}
    mapper = {}
    counter = {}
    for workflow_plan in workflow_plans:
        steps = list(workflow_plan.subjects(RDF.type, tb.Step))
        step_components = {step: next(workflow_plan.objects(step, tb.runs)) for step in steps}
        step_next = {step: list(workflow_plan.objects(step, tb.followedBy)) for step in steps}
        logical_plan = {
            step_components[step]: [step_components[s] for s in nexts] for step, nexts in step_next.items()
        }
        main_component = next(
            comp for comp in logical_plan.keys() if logical_plan[comp] == [cb.term('component-csv_local_writer')])
        if (main_component, RDF.type, tb.ApplierImplementation) in ontology:
            options = list(ontology.objects(main_component, tb.hasLearner))
            main_component = next(o for o in options if (None, None, o) in workflow_plan)
        if main_component not in counter:
            counter[main_component] = 0
        plan_id = (f'{main_component.fragment.split("-")[1].replace("_", " ").replace(" learner", "").title()} '
                   f'{counter[main_component]}')
        counter[main_component] += 1
        logical_plans[plan_id] = logical_plan
        mapper[plan_id] = workflow_plan

    return logical_plans, mapper


def compress(folder: str, destination: str) -> None:
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, folder)
                zipf.write(file_path, arcname=os.path.join(os.path.basename(folder), archive_path))
