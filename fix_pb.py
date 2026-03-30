content = """{% extends 'base.html' %}
{% block content %}
<h2>{{ 'Edit Paper' if paper else 'New Paper' }}</h2>
<div class="row">
  <div class="col-md-5">
    <div class="card shadow mb-3">
      <div class="card-body">
        <h5>Paper Details</h5>
        <form method="POST" action="/teacher/paper/create">
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
        <form method="POST" action="/teacher/paper/{{ paper.id }}/add-question">
          <select name="question_id" class="form-select mb-2">
            {% for q in all_questions %}
            {% if q.id not in added_ids %}
            <option value="{{ q.id }}">[{{ q.q_type }}] {{ q.question_text[:60] }}</option>
            {% endif %}
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
          <td>
            <form method="POST" action="/teacher/paper/{{ paper.id }}/remove-question/{{ pq.id }}">
              <button type="submit" class="btn btn-sm btn-danger">X</button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="4" class="text-center">No questions added yet.</td></tr>
        {% endfor %}
      </tbody>
    </table>
    {% if paper.status == 'draft' %}
    <form method="POST" action="/teacher/paper/{{ paper.id }}/submit">
      <button type="submit" class="btn btn-success mt-2">Submit Paper to HOD</button>
    </form>
    {% endif %}
    {% endif %}
  </div>
</div>
{% endblock %}"""

with open('templates/teacher/paper_builder.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")