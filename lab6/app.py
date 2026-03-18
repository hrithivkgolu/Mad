from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
db = SQLAlchemy(app)
api = Api(app)

@app.route("/api/course/<int:course_id>", methods=["GET","POST","PUT"])
def course(course_id):
	if request.method=="GET":
		try:
			conn = sqlite3.connect(DB)
			conn.row_factory = sqlite3.Row
			cur = conn.cursor()
			response = cur.execute("SELECT * FROM course WHERE course_id=?",(course_id,)).fetchone()
			if not response:
				return jsonify({"error":"Course not found"}), 404

			return jsonify(dict(response)), 200
		except Exception as e:
			return jsonify({"error":str(e)}), 500




if __name__ == '__main__':
	app.run()