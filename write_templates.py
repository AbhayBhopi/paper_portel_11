import os

os.makedirs('templates/auth', exist_ok=True)
os.makedirs('templates/admin', exist_ok=True)
os.makedirs('templates/teacher', exist_ok=True)

base = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question Paper Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-dark bg-dark px-3 d-flex justify-content-between">
    <span class="navbar-brand">Question Paper Portal</span>
    {% if session.user_id %}
    <div>
        <span class="text-light me-3">{{ session.full_name }} ({{ session.role }})</span>
        <a href="{{ url_for('auth.logout') }}" class="btn btn-sm btn-outline-light">Logout</a>
    </div>
    {% endif %}
</nav>
<div class="container-fluid">
  <div class="row">
    {% if session.user_id %}
    <div class="col-md-2 bg-secondary min-vh-100 pt-3">
      {% if session.role == 'admin' %}
        <a href="{{ url_for('admin.dashboard') }}" class="d-block text-white p-2">Dashboard</a>
        <a href="{{ url_for('admin.create_teacher') }}" class="d-block text-white p-2">Add Teacher</a>
        <a href="{{ url_for('admin.view_papers') }}" class="d-block text-white p-2">View Papers</a>
      {% else %}
        <a href="{{ url_for('teacher.dashboard') }}" class="d-block text-white p-2">Dashboard</a>
        <a href="{{ url_for('teacher.question_bank') }}" class="d-block text-white p-2">Question Bank</a>
        <a href="{{ url_for('teacher.dashboard') }}" class="d-block text-white p-2">New Paper</a>
      {% endif %}
    </div>
    <div class="col-md-10 p-4">
    {% else %}
    <div class="col-12 p-4">
    {% endif %}
        {% with messages = get_flashed_messages() %}
          {% if messages %}{% for msg in messages %}
            <div class="alert alert-warning alert-dismissible fade show">{{ msg }}
              <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
          {% endfor %}{% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

login = """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-md-4">
    <div class="card shadow">
      <div class="card-body p-4">
        <h3 class="text-center mb-4">Login</h3>
        <form method="POST">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" name="username" class="form-control" required autofocus>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" name="password" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}"""

admin_dashboard = """{% extends 'base.html' %}
{% block content %}
<h2>Admin Dashboard</h2>
<div class="row mt-4">
  <div class="col-md-3">
    <div class="card text-white bg-primary mb-3">
      <div class="card-body">
        <h5>Teachers</h5>
        <p class="display-6">{{ teachers|length }}</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-success mb-3">
      <div class="card-body">
        <h5>Subjects</h5>
        <p class="display-6">{{ subjects|length }}</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-warning mb-3">
      <div class="card-body">
        <h5>Papers</h5>
        <p class="display-6">{{ papers|length }}</p>
      </div>
    </div>
  </div>
</div>
<h4 class="mt-4">Teachers List</h4>
<table class="table table-bordered bg-white">
  <thead class="table-dark">
    <tr><th>Name</th><th>Username</th><th>Subjects</th></tr>
  </thead>
  <tbody>
    {% for t in teachers %}
    <tr>
      <td>{{ t.full_name }}</td>
      <td>{{ t.username }}</td>
      <td>{{ t.subjects|map(attribute='name')|join(', ') or 'None' }}</td>
    </tr>
    {% else %}
    <tr><td colspan="3" class="text-center">No teachers yet.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}"""

create_teacher = """{% extends 'base.html' %}
{% block content %}
<h2>Add New Teacher</h2>
<div class="card shadow mt-3" style="max-width:500px">
  <div class="card-body p-4">
    <form method="POST">
      <div class="mb-3">
        <label class="form-label">Full Name</label>
        <input type="text" name="full_name" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input type="text" name="username" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" name="password" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Assign Subjects</label>
        {% for subject in subjects %}
        <div class="form-check">
          <input class="form-check-input" type="checkbox" name="subjects" value="{{ subject.id }}">
          <label class="form-check-label">{{ subject.name }} ({{ subject.code }})</label>
        </div>
        {% endfor %}
      </div>
      <button type="submit" class="btn btn-success w-100">Create Teacher</button>
    </form>
  </div>
</div>
{% endblock %}"""

view_papers = """{% extends 'base.html' %}
{% block content %}
<h2>All Papers</h2>
<table class="table table-bordered bg-white mt-3">
  <thead class="table-dark">
    <tr><th>Title</th><th>Subject</th><th>Teacher</th><th>Status</th><th>Date</th><th>Actions</th></tr>
  </thead>
  <tbody>
    {% for paper in papers %}
    <tr>
      <td>{{ paper.title }}</td>
      <td>{{ paper.subject.name }}</td>
      <td>{{ paper.teacher.full_name }}</td>
      <td><span class="badge bg-{{ 'success' if paper.status == 'submitted' else 'secondary' }}">{{ paper.status }}</span></td>
      <td>{{ paper.created_at.strftime('%d-%m-%Y') }}</td>
      <td>
        <a href="{{ url_for('admin.download_paper', paper_id=paper.id, fmt='pdf') }}" class="btn btn-sm btn-danger">PDF</a>
        <a href="{{ url_for('admin.download_paper', paper_id=paper.id, fmt='docx') }}" class="btn btn-sm btn-primary">DOCX</a>
      </td>
    </tr>
    {% else %}
    <tr><td colspan="6" class="text-center">No papers yet.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}"""

teacher_dashboard = """{% extends 'base.html' %}
{% block content %}
<h2>Teacher Dashboard</h2>
<p class="text-muted">Welcome, {{ session.full_name }}!</p>
<div class="row mt-3">
  <div class="col-md-3">
    <div class="card text-white bg-info mb-3">
      <div class="card-body">
        <h5>My Papers</h5>
        <p class="display-6">{{ papers|length }}</p>
      </div>
    </div>
  </div>
</div>
<div class="d-flex justify-content-between align-items-center mt-3">
  <h4>My Papers</h4>
  <a href="{{ url_for('teacher.create_paper') }}" class="btn btn-primary">+ New Paper</a>
</div>
<table class="table table-bordered bg-white mt-2">
  <thead class="table-dark">
    <tr><th>Title</th><th>Subject</th><th>Status</th><th>Created</th><th>Actions</th></tr>
  </thead>
  <tbody>
    {% for paper in papers %}
    <tr>
      <td>{{ paper.title }}</td>
      <td>{{ paper.subject.name }}</td>
      <td><span class="badge bg-{{ 'success' if paper.status == 'submitted' else 'secondary' }}">{{ paper.status }}</span></td>
      <td>{{ paper.created_at.strftime('%d-%m-%Y') }}</td>
      <td>
        <a href="{{ url_for('teacher.build_paper', paper_id=paper.id) }}" class="btn btn-sm btn-warning">Edit</a>
      </td>
    </tr>
    {% else %}
    <tr><td colspan="5" class="text-center">No papers yet. <a href="{{ url_for('teacher.create_paper') }}">Create one!</a></td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}"""

question_bank = """{% extends 'base.html' %}
{% block content %}
<h2>Question Bank</h2>
<div class="card shadow mb-4" style="max-width:600px">
  <div class="card-body">
    <h5>Add New Question</h5>
    <form method="POST">
      <div class="mb-2">
        <label class="form-label">Subject</label>
        <select name="subject_id" class="form-select" required>
          {% for s in subjects %}
          <option value="{{ s.id }}">{{ s.name }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="mb-2">
        <label class="form-label">Question Text</label>
        <textarea name="question_text" class="form-control" rows="3" required></textarea>
      </div>
      <div class="row">
        <div class="col">
          <label class="form-label">Marks</label>
          <input type="number" name="marks" class="form-control" value="1" min="1" required>
        </div>
        <div class="col">
          <label class="form-label">Type</label>
          <select name="q_type" class="form-select">
            <option value="short">Short</option>
            <option value="long">Long</option>
            <option value="mcq">MCQ</option>
          </select>
        </div>
      </div>
      <button type="submit" class="btn btn-primary mt-3">Add Question</button>
    </form>
  </div>
</div>
<h4>Existing Questions</h4>
<table class="table table-bordered bg-white">
  <thead class="table-dark">
    <tr><th>Subject</th><th>Question</th><th>Marks</th><th>Type</th></tr>
  </thead>
  <tbody>
    {% for q in questions %}
    <tr>
      <td>{{ q.subject.name }}</td>
      <td>{{ q.question_text }}</td>
      <td>{{ q.marks }}</td>
      <td>{{ q.q_type }}</td>
    </tr>
    {% else %}
    <tr><td colspan="4" class="text-center">No questions yet.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}"""

paper_builder = """{% extends 'base.html' %}
{% block content %}
<h2>{{ 'Edit Paper' if paper else 'New Paper' }}</h2>
<div class="row">
  <div class="col-md-5">
    <div class="card shadow mb-3">
      <div class="card-body">
        <h5>Paper Details</h5>
        <form method="POST">
          <div class="mb-2">
            <label class="form-label">Title</label>
            <input type="text" name="title" class="form-control" value="{{ paper.title if paper else '' }}" required>
          </div>
          <div class="mb-2">
            <label class="form-label">Subject</label>
            <select name="subject_id" class="form-select" required>
              {% for s in subjects %}
              <option value="{{ s.id }}" {{ 'selected' if paper and paper.subject_id == s.id }}>{{ s.name }}</option>
              {% endfor %}
            </select>
          </div>
          <button type="submit" class="btn btn-success w-100">Save Paper</button>
        </form>
      </div>
    </div>
    {% if paper %}
    <div class="card shadow">
      <div class="card-body">
        <h5>Add Question from Bank</h5>
        <form method="POST" action="{{ url_for('teacher.add_question', paper_id=paper.id) }}">
          <select name="question_id" class="form-select mb-2">
            {% for q in questions %}
            <option value="{{ q.id }}">[{{ q.q_type }}] {{ q.question_text[:60] }}</option>
            {% else %}
            <option disabled>No questions in bank yet</option>
            {% endfor %}
          </select>
          <button type="submit" class="btn btn-primary w-100">Add to Paper</button>
        </form>
      </div>
    </div>
    {% endif %}
  </div>
  <div class="col-md-7">
    {% if paper %}
    <h5>Questions in this Paper</h5>
    <table class="table table-bordered bg-white">
      <thead class="table-dark">
        <tr><th>#</th><th>Question</th><th>Marks</th><th>Remove</th></tr>
      </thead>
      <tbody>
        {% for pq in paper.questions %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>{{ pq.question.question_text }}</td>
          <td>{{ pq.question.marks }}</td>
          <td><a href="{{ url_for('teacher.remove_question', paper_id=paper.id, pq_id=pq.id) }}" class="btn btn-sm btn-danger">X</a></td>
        </tr>
        {% else %}
        <tr><td colspan="4" class="text-center">No questions added yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
    {% if paper.status == 'draft' %}
    <form method="POST" action="{{ url_for('teacher.submit_paper', paper_id=paper.id) }}" class="mt-2">
      <button type="submit" class="btn btn-success">Submit Paper to HOD</button>
    </form>
    {% endif %}
    {% endif %}
  </div>
</div>
{% endblock %}"""

files = {
    'templates/base.html': base,
    'templates/auth/login.html': login,
    'templates/admin/dashboard.html': admin_dashboard,
    'templates/admin/create_teacher.html': create_teacher,
    'templates/admin/view_papers.html': view_papers,
    'templates/teacher/dashboard.html': teacher_dashboard,
    'templates/teacher/question_bank.html': question_bank,
    'templates/teacher/paper_builder.html': paper_builder,
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {path}')

print('\nAll templates written successfully!')
