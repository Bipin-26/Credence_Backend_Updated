from flask import Flask, Response, request, render_template
from flask_pymongo import PyMongo
import logging, json
from bson.objectid import ObjectId

app = Flask(__name__)

logging.basicConfig(filename='errorlog.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return Response(response=json.dumps({"message":"Ooppss......Something went wrong..!!!"}),status=500)

try:
    db_config = json.loads(open('./data_modules/db.json').read())

    app.config['JSON_SORT_KEYS'] = False 
    app.config['MONGO_DBNAME'] = f"{db_config['dbname']}"
    app.config['MONGO_URI'] = f"{db_config['database']}://{db_config['hostname']}:{db_config['port']}/{db_config['dbname']}"

    mongo = PyMongo(app)
    mycollection = mongo.db.moviestore
except Exception as err:
    server_error(err)

@app.route('/insert_movie', methods=['POST'])
def insert():
    try:
        movie = {
            'name' : request.form['name'],
            'img' : request.form['img'],
            'summary' : request.form['summary']
        }
        insert_query = mycollection.insert_one(movie)
        if(insert_query.inserted_id):        
            return Response(response=json.dumps({"message":"Value inserted","id":f"{insert_query.inserted_id}"}), status=200, mimetype="application/json")
        else:
            return Response(response=json.dumps({"message":"Value cannot be inserted"}), status=500, mimetype="application/json")
    except Exception as err:
        return server_error(err)
        

@app.route('/display',methods=['GET'])
def display_movie_list():
    try:
        docs = list(mycollection.find())
        for item in docs:
            item['_id'] = str(item['_id'])
        if len(docs) == 0:
            return Response(response=json.dumps({"message":"No Movies Found"}),status=500)
        else:
            return Response(response=json.dumps(docs))
    except Exception as err:
        return server_error(err)


@app.route('/movie_update/<id>', methods = ['PUT'])
def update_movie(id):
    try:
        update_query = list(mycollection.find_one_and_update({'_id':ObjectId(id)},{'$set':{'name':request.form['name'],'img':request.form['img'],'summary':request.form['summary']}}))
        return Response(response=json.dumps({"message":f"Records updated successfully for id - {ObjectId(id)}"}),status=200)
    except Exception as err:
        return Response(response=json.dumps({"message":"No Movies Found"}),status=500)
        return server_error(err)


@app.route('/remove/<id>', methods=['DELETE'])
def remove_movie(id):
    try:
        delete_query = list(mycollection.find_one_and_delete({'_id':ObjectId(id)}))
        return Response(response=json.dumps({"message":'Record deleted successfully..!!!',"id":f"{ObjectId(id)}"}),status=200)
    except Exception as err:
        return Response(response=json.dumps({"message":"No Movies Found"}),status=500)
        return server_error(err)



if __name__ == '__main__':
    app.run(debug=True)
