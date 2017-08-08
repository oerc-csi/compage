'''
   Routing for the data
'''

from flask import Flask, request, redirect, url_for, render_template, flash, json
import json

from combined import JoinGraph

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def get_single_data():
   
    graph = request.get_json()
    data = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').get_original(graph['data'])
    return response_template(data, 200)

@app.route('/search')
def search_data():
    search = request.args.get('term')
    data = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').search_data(search)
    return response_template(data, 200)

@app.route('/')
def get_index():
    return render_template('search.html')

@app.route('/predicates', methods=['POST'])
def sparql():
    '''
       Searches the predicates associated with an object
    '''
    graph = request.get_json()
    data = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').search_predicates(graph['entity'])
    return response_template(data, 200)

@app.route('/predicates/workset', methods=['POST'])
def search_pred_obj():
    '''
       Search (predicate, object) associated with a workset
    '''
    graph = request.get_json()
    data = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').search_predicates_object(graph['pred'], graph['obj'], graph['ws'])
    return response_template(data, 200)

@app.route('/predicates/similarity', methods=['POST'])
@app.route('/predicates/similarity/workset', methods=['POST'])
def similarity_works():
    '''
       Route to return similarity counts for predicates
    '''
    graph = request.get_json()
    data = None
    if "flag" in graph:
        data = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').search_similarities(graph['dataObj'], ws=graph['flag'])
    else:
        data = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').search_similarities(graph['dataObj'])
    return response_template(data, 200)

@app.route('/subject', methods=['GET', 'POST'])
def get_linked_subjects():
    graph = request.get_json()
    data = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').search_subject(graph['subject'])
    return response_template(data, 200)

@app.route('/links', methods=['GET', 'POST'])
def get_linked_graphs():
    graph = request.get_json()
    data = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').join_graphs(graph['graph'])
    return response_template(data, 200)

@app.route('/worksets', methods=['POST'])
def get_workset():
    _id = request.get_json();
    ws = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').worksets()
    return response_template(ws, 200)

@app.route('/worksets/items', methods=['POST'])
def get_workset_items():
    ws_id = request.get_json()
    ws = JoinGraph('http://129.67.193.130:10080/blazegraph/sparql').worksets_by_id(ws_id['id'])
    return response_template(ws, 200)

@app.route('/weight', methods=['POST'])
def store_weight():
    weight = request.get_json()
    return response_template("stored", 200)
    

def response_template(data, resp_status):
    '''
       Helper function for the JSON response template
    '''
    response = app.response_class(
        response=data,
        status=resp_status,
        mimetype='application/json'
    )
    return response
