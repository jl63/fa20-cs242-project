import time
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

def init_db():
    """Connect database"""
    client = MongoClient(port=27017)
    database = client['local']
    return database

db = init_db()

ATTRIBUTES = ['name','price','size','url','brand','image_url','description','instruction','ingredients','rating','review_count']

def get_search_result(items,collection):
    brand = None
    if collection == db.shiseido:
        brand = 'Shiseido'
    elif collection == db.urbanDecay:
        brand = 'Urban Decay'
    elif collection == db.tomford:
        brand = 'Tom Ford'
    elif collection == db.nars:
        brand = 'Nars'
    result = []
    for item in items:
        for attri in ATTRIBUTES:
            if attri not in item:
                item[attri] = ''
        if '_id' in item:
            del item['_id']
        if 'reviews' not in item:
            item['reviews'] = []
        if '$' not in str(item['price']):
            item['price'] = '$'+str(item['price'])
        if brand is not None:
            item['brand'] = brand
        for key in item:
            if item[key] == None:
                item[key] = ''
        result.append(item)
    return result

def get_search_result_for_nm(items):
    result = []
    for item in items:
        for attri in ATTRIBUTES:
            if attri not in item:
                item[attri] = ''
        if '_id' in item:
            del item['_id']
        item['reviews'] = []
        for key in item:
            if item[key] == None:
                item[key] = ''
        description = ''
        for key in item['description']:
            if key == 'How to Use' or 'Usage':
                item['instruction'] = item['description'][key]
            if key == 'Key Ingredients':
                item['ingredients'] = item['description'][key]
            if key == 'Fragrance Description' or 'What It Is':
                description = item['description'][key]
        item['description'] = description
        result.append(item)
    return result

def get_search_result_for_sephora(items):
    result = []
    for item in items:
        for attri in ATTRIBUTES:
            if attri not in item:
                item[attri] = ''
        if '_id' in item:
            del item['_id']
        item['reviews'] = []
        for key in item:
            if item[key] == None:
                item[key] = ''
        description = ''
        for key in item['description']:
            if key == 'Fragrance Description' or 'What it Is':
                description = item['description'][key]
        item['description'] = description
        result.append(item)
    return result

@app.route('/ulta')
def get_ulta_search_result():
    result = get_search_result(db.ulta.find({}),db.ulta)
    print(type(result))
    return {'result':result}

@app.route('/lf')
def get_lf_search_result():
    result = get_search_result(db.LookFantastic.find({}),db.LookFantastic)
    return {'result':result}

@app.route('/nm')
def get_nm_search_result():
    result = get_search_result_for_nm(db.NeimanMarcus.find({}))
    return {'result':result}

@app.route('/sephora')
def get_sephora_search_result():
    result = get_search_result_for_sephora(db.sephora.find({}))
    return {'result':result}

@app.route('/shiseido')
def get_shiseido_search_result():
    result = get_search_result(db.shiseido.find({}),db.shiseido)
    return {'result':result}

@app.route('/urbandecay')
def get_urbandecay_search_result():
    result = get_search_result(db.urbanDecay.find({}),db.urbanDecay)
    return {'result':result}

@app.route('/tomford')
def get_tomford_search_result():
    result = get_search_result(db.tomford.find({}),db.tomford)
    return {'result':result}

@app.route('/nars')
def get_nars_search_result():
    result = get_search_result(db.nars.find({}),db.nars)
    return {'result':result}

@app.route('/search', methods=['POST'])
def get_search_browsing_result():
    keyword = request.args.get('keyword')
    collections = [db.ulta, db.LookFantastic, db.shiseido, db.urbanDecay, db.tomford, db.nars]
    result = []
    for collection in collections:
        result += get_search_result(collection.find({'name': {'$regex': keyword, '$options': 'i'}}),collection)
    result += get_search_result_for_nm(db.NeimanMarcus.find({'name': {'$regex': keyword, '$options': 'i'}}))
    result += get_search_result_for_sephora(db.sephora.find({'name': {'$regex': keyword, '$options': 'i'}}))
    return {'result':result}
