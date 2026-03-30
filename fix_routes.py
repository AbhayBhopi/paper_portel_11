# Fix question_bank.html
with open('templates/teacher/question_bank.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<form method="POST">',
    '<form method="POST" action="/teacher/questions/add">'
)

with open('templates/teacher/question_bank.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed question_bank.html")

# Fix dashboard.html - replace any create_paper GET links with a form
with open('templates/teacher/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'href="{{ url_for(\'teacher.create_paper\') }}"',
    'href="#" data-bs-toggle="modal" data-bs-target="#newPaperModal"'
)

with open('templates/teacher/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed dashboard.html")
print("Done!")