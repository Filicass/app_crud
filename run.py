from flask import request, jsonify
from app import app, db
from models import Todo
from repositorio import TodoRepository

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'Bem-vindo ao seu gerenciador de tarefas!'

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = TodoRepository.get_all()
    return jsonify([{"id": todo.id, "title": todo.title, "description": todo.description, "done": todo.done} for todo in todos])

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo_by_id(todo_id):
    todo = TodoRepository.get_by_id(todo_id)
    if todo:
        return jsonify({"id": todo.id, "title": todo.title, "description": todo.description, "done": todo.done})
    return jsonify({"message": "Todo not found"}), 404

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = TodoRepository.create(title=data['title'], description=data.get('description'))
    return jsonify({"id": new_todo.id, "title": new_todo.title, "description": new_todo.description, "done": new_todo.done})

if __name__ == '__main__':
    app.run(debug=True)
            