import shutil
import sys
import os

from flask import Flask, request, send_file, Response, jsonify
from flask_cors import CORS
from .functions import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from common.common import *
from pipeline_translator.general_pipeline_translator import translate_graph_folder, translate_graph

app = Flask(__name__)
CORS(app)

# TODO Change folder
files_folder = os.path.abspath(r'./demo/demo_api/temp_files')

ontology = get_ontology_graph()
intent: Optional[Graph] = None
abstract_plans = {}
algorithm_implementations = {}
logical_plans = {}
logical_to_workflows = {}
workflow_plans = {}
selected_plans = []


@app.get('/datasets')
def get_datasets():
    datasets = {n.fragment: n for n in ontology.subjects(RDF.type, dmop.TabularDataset)}
    return datasets


@app.get('/problems')
def get_problems():
    problems = {n.fragment: n for n in ontology.subjects(RDF.type, tb.Task)}
    return problems


@app.post('/abstract_planner')
def run_abstract_planner():
    intent_graph = get_graph_xp()

    data = request.json

    # print(f'DATA: {data}')

    intent_name = data.get('intent_name', '')
    dataset = data.get('dataset', '')
    task = data.get('problem', '')

    # print(f'INTENT: {intent_name}')
    print(f'DATASET: {dataset}')
    # print(f'TASK: {task}')

    intent_graph.add((ab.term(intent_name), RDF.type, tb.Intent))
    intent_graph.add((ab.term(intent_name), tb.overData, URIRef(dataset)))
    intent_graph.add((URIRef(task), tb.tackles, ab.term(intent_name)))

    global abstract_plans, algorithm_implementations, intent
    intent = intent_graph

    # print(f'INTENT GRAPH: {intent}')

    print('ABOUT TO RUN ABSTRACT PLANNING...')

    abstract_plans, algorithm_implementations = abstract_planner(ontology, intent)

    # print(f'ABST PLNS:{abstract_plans}')
    # print(f'ALGO IMPS:{algorithm_implementations}')

    print('SUCCESSFULLY FINISHED ABSTRACT PLANNING')
    
    return Response(status=204)


@app.get('/visualization_algorithms')
def get_visualization_algorithms():
    viz_algorithms = {n.fragment: n for n in ontology.subjects(tb.solves, cb.DataVisualization)}
    return viz_algorithms


@app.post('/dataset_columns/dataset')
def get_dataset_columns(dataset: URIRef):
    data = request.json

    dataset = data.get('dataset', '')
    dataset_uri = URIRef(dataset)

    print(f'DATASET: {dataset}')

    dataset_columns = {n.fragment: n for n in ontology.subjects(RDF.type, dmop.Column) if (dataset_uri, dmop.hasColumn, n) in ontology}
    return dataset_columns


@app.get('/abstract_plans')
def get_abstract_plans():
    global abstract_plans
    return abstract_plans


@app.post('/logical_planner')
def run_logical_planner():
    global logical_plans, workflow_plans, logical_to_workflows

    plan_ids = request.json

    print(plan_ids)

    impls = [impl
             for alg, impls in algorithm_implementations.items() if str(alg) in plan_ids
             for impl in impls]

    workflow_plans = workflow_planner(ontology, impls, intent)

    logical_plans, logical_to_workflows = logical_planner(ontology, workflow_plans)

    return Response(status=204)


@app.get('/logical_plans')
def get_logical_plans():
    global logical_plans
    return logical_plans


@app.post('/workflow_planner')
def run_workflow_planner():
    plan_ids = request.json

    global selected_plans
    selected_plans = plan_ids

    return Response(status=204)


@app.get('/workflow_plans')
def get_workflow_plans():
    global selected_plans

    return selected_plans


@app.get('/workflow_plans/rdf/all')
def download_all_rdf():
    folder = os.path.join(files_folder, 'rdf')
    os.makedirs(folder, exist_ok=True)
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

    global logical_to_workflows, selected_plans

    for plan_id, workflow in logical_to_workflows.items():
        if plan_id not in selected_plans:
            continue
        file_path = os.path.join(folder, f'{plan_id}.ttl')
        workflow.serialize(file_path, format='turtle')
    compress(folder, folder + '.zip')
    return send_file(folder + '.zip', as_attachment=True)


@app.get('/workflow_plans/rdf/<plan_id>')
def download_rdf(plan_id):
    global logical_to_workflows
    workflow = logical_to_workflows[plan_id]
    file_path = os.path.join(files_folder, f'{plan_id}.ttl')
    workflow.serialize(file_path, format='turtle')
    return send_file(file_path, as_attachment=True)


@app.get('/workflow_plans/knime/all')
def download_all_knime():
    folder = os.path.join(files_folder, 'rdf_to_trans')
    os.makedirs(folder, exist_ok=True)
    knime_folder = os.path.join(files_folder, 'knime')
    os.makedirs(knime_folder, exist_ok=True)

    if os.path.exists(folder):
        shutil.rmtree(folder)
    if os.path.exists(knime_folder):
        shutil.rmtree(knime_folder)
    os.mkdir(folder)
    os.mkdir(knime_folder)

    global logical_to_workflows, selected_plans

    for plan_id, workflow in logical_to_workflows.items():
        if plan_id not in selected_plans:
            continue
        file_path = os.path.join(folder, f'{plan_id}.ttl')
        workflow.serialize(file_path, format='turtle')

    translate_graph_folder(ontology, folder, knime_folder, keep_folder=False)

    compress(knime_folder, knime_folder + '.zip')
    return send_file(knime_folder + '.zip', as_attachment=True)


@app.get('/workflow_plans/knime/<plan_id>')
def download_knime(plan_id):
    global logical_to_workflows
    workflow = logical_to_workflows[plan_id]
    file_path = os.path.join(files_folder, f'{plan_id}.ttl')
    workflow.serialize(file_path, format='turtle')

    knime_file_path = file_path[:-4] + '.knwf'
    translate_graph(ontology, file_path, knime_file_path)

    return send_file(knime_file_path, as_attachment=True)
