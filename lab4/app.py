from flask import Flask, render_template, request, redirect, url_for,session,flash, abort
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('data.csv')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        id_type = request.form.get('ID')
        id_val = request.form.get('id_value')

        if not id_val:
            return render_template('details.html', error=True)

        try:
            val = int(id_val)
        except ValueError:
            return render_template('details.html', error=True)

        if id_type == 'student_id':
            # FIX: Use the mask to filter the DataFrame
            student_data = df[df['Student id'] == val]
            if student_data.empty:
                return render_template('details.html', error=True)
            return render_template('details.html', type='student', data=student_data, total=student_data['Marks'].sum())

        elif id_type == 'course_id':
            # FIX: Use the mask to filter the DataFrame
            course_data = df[df['Course id'] == val]
            if course_data.empty:
                return render_template('details.html', error=True)
            return render_template('details.html', type='course', avg=course_data['Marks'].mean(), max=course_data['Marks'].max())
        
        return render_template('details.html', error=True)
    
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, port=4999)