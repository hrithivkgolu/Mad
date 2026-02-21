import sys,pyhtml,jinja2,matplotlib.pyplot as plt


def render_error():
    error_template = """<!DOCTYPE html>
<html>
<head>
    <title>Something Went Wrong</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
</body>
</html>"""
    with open('output.html', 'w') as f:
        f.write(error_template)




def main():
    if len(sys.argv) != 3:
        render_error()
        return

    mode = sys.argv[1]
    search_id = sys.argv[2]

    data = []
    try:
        with open('data.csv', 'r') as f:
            lines = f.readlines()
            headers = [h.strip() for h in lines[0].split(',')]
            for line in lines[1:]:
                if not line.strip(): continue
                values = [v.strip() for v in line.split(',')]
                data.append(dict(zip(headers, values)))
    except FileNotFoundError:
        render_error()
        return

    if mode == '-s':
        student_data = [row for row in data if row['Student id'] == search_id]
        
        if not student_data:
            render_error()
            return
        
        total_marks = sum(int(row['Marks']) for row in student_data)
        
        template_str = """<!DOCTYPE html>
<html>
<head>
    <title>Student Details</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1">
        <thead>
            <tr>
                <th>Student ID</th>
                <th>Course ID</th>
                <th>Marks</th>
            </tr>
        </thead>
        <tbody>
            {% for row in student_data %}
            <tr>
                <td>{{ row['Student id'] }}</td>
                <td>{{ row['Course id'] }}</td>
                <td>{{ row['Marks'] }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="2" style="text-align:center">Total Marks</td>
                <td>{{ total_marks }}</td>
            </tr>
        </tbody>
    </table>
</body>
</html>"""
        template = jinja2.Template(template_str)
        content = template.render(student_data=student_data, total_marks=total_marks)
        with open('output.html', 'w') as f:
            f.write(content)

    elif mode == '-c':
        course_marks = [int(row['Marks']) for row in data if row['Course id'] == search_id]
        
        if not course_marks:
            render_error()
            return
        
        avg_marks = sum(course_marks) / len(course_marks)
        max_marks = max(course_marks)

        plt.hist(course_marks)
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig('hist.png')
        plt.close() 
        template_str = """<!DOCTYPE html>
<html>
<head><title>Course Details</title></head>
<body>
    <h1>Course Details</h1>
    <table border="1" id="course-table">
        <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
        </tr>
        <tr>
            <td>{{ avg_marks }}</td>
            <td>{{ max_marks }}</td>
        </tr>
    </table>
    <img src="hist.png" id="histogram">
</body>
</html>"""
        template = jinja2.Template(template_str)
        with open('output.html', 'w') as f:
            f.write(template.render(avg_marks=avg_marks, max_marks=max_marks))
            
    else:
        render_error()

if __name__ == "__main__":
    main()