from flask import Flask, Response, request, render_template
from flask_pymongo import PyMongo
import logging, json
from bson.objectid import ObjectId

app = Flask(__name__)


logging.basicConfig(filename='errorlog.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app.config['JSON_SORT_KEYS']=False
app.config['MONGO_DBNAME'] = 'Project'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Movie'
mongo = PyMongo(app)
mycollection = mongo.db.moviestore


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return Response(response="Ooppss......Something went wrong..!!!")


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
            return Response(response="No Movies Found")
        else:
            return Response(response=json.dumps(docs))
    except Exception as err:
        return server_error(err)



@app.route('/movie_update/<id>', methods = ['PUT'])
def update_movie(id):
    try:
        update_query = mycollection.find_one_and_update({'_id':ObjectId(id)},{'$set':{'name':request.form['name'],'img':request.form['img'],'summary':request.form['summary']}})
        return Response(response="Records updated successfully")
    except Exception as err:
        return Response(response="Movie not found")
        return server_error(err)



@app.route('/remove/<id>', methods=['DELETE'])
def remove_movie(id):
    try:
        delete_query = list(mycollection.find_one_and_delete({'_id':ObjectId(id)}))
        return Response(response='Record deleted successfully..!!!',status=200)
    except Exception as e:
        return Response(response="Movie not found...!!", status = 500)
        return server_error(e)


if __name__ == '__main__':
    app.run(debug=True)