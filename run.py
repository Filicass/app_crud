from flask import request, jsonify
from app import app, db
from models import Todo
from repositorio import TodoRepository

with app.app_context():
    db.create_all() 

@app.route('/')
def home():
    return 'Bem-vindo ao seu gerenciador de tarefas!'

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todos = TodoRepository.get_all()
    return jsonify([{"id": todo.id, "title": todo.title, "description": todo.description, "done": todo.done} for todo in todos])

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({'error':'Title is required'}), 400
    new_todo = TodoRepository.create(title=data['title'], description=data.get('description'))
    print(f"New todo created: {new_todo.id} - {new_todo.title}")
    return jsonify({"id": new_todo.id, "title": new_todo.title, "description": new_todo.description, "done": new_todo.done}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '') #Definindo um valor padrão
    done = data.get('done')
    updated_todo = TodoRepository.update(todo_id, title=title, description=description, done=done)
    if updated_todo:
        return jsonify({'id': updated_todo.id, 'title': updated_todo.title, 'description': updated_todo.description, 'done': updated_todo.done}), 200
    return jsonify({'message': 'Todo not found'}), 404

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if TodoRepository.delete(todo_id):
        return '', 204
    return jsonify({'message': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
            