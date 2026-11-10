from flask import Flask, render_template_string, request, jsonify, redirect, url_for

app = Flask(__name__)

# In-memory storage for submissions
submissions = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Assignment Submission Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; }
        .container { max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input, button { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background: #28a745; color: white; border: none; font-size: 16px; cursor: pointer; }
        button:hover { background: #218838; }
        .error { color: red; margin-bottom: 10px; }
        .success { color: green; margin-bottom: 10px; }
        ul { padding-left: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Assignment Submission Portal</h2>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        {% if success %}
            <div class="success">{{ success }}</div>
        {% endif %}
        <form method="POST" action="/submit">
            <label>Student Name:</label>
            <input type="text" name="name" required>
            
            <label>Registration Number:</label>
            <input type="text" name="reg_no">
            
            <label>Assignment Title:</label>
            <input type="text" name="title" required>
            
            <label>Submission URL:</label>
            <input type="url" name="url" required>
            
            <button type="submit">Submit Assignment</button>
        </form>

        <h3>Submitted Assignments</h3>
        <ul>
            {% for sub in submissions %}
                <li><strong>{{ sub.name }}</strong> ({{ sub.reg_no }}) - {{ sub.title }}: <a href="{{ sub.url }}" target="_blank">{{ sub.url }}</a></li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, submissions=submissions)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    reg_no = request.form.get('reg_no', '').strip()
    title = request.form.get('title', '').strip()
    sub_url = request.form.get('url', '').strip()

    # Validation rules as per requirement
    if not reg_no:
        return render_template_string(HTML_TEMPLATE, error="Registration number is missing!", submissions=submissions), 400
    
    if not sub_url.startswith('http://') and not sub_url.startswith('https://'):
        return render_template_string(HTML_TEMPLATE, error="Invalid submission URL!", submissions=submissions), 400

    # Save submission
    submissions.append({"name": name, "reg_no": reg_no, "title": title, "url": sub_url})
    return render_template_string(HTML_TEMPLATE, success="Assignment submitted successfully!", submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)