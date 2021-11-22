from flask import Flask, request, jsonify, make_response
import read_data
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
def my_query(player_name):
    my_data = read_data.read_csv_player_all_weeks_flask(player_name, '2019')
    return my_data
    

@app.route('/players/<user_id>', methods=['GET'])
@cross_origin()
def players(user_id):
    print(user_id)
    my_data = my_query(user_id)
    print(my_data.keys())
    my_map = {'tyreek': 1}
    res = make_response(jsonify(my_data))
    return res

if __name__ == '__main__':
    app.run()   