from flask import request, jsonify
from app import app, db
from models import Todo
from repositorio import TodoRepository
from flask_jwt_extended import jwt_required

with app.app_context():
    db.create_all() 

@app.route('/')
def home():
    return 'Bem-vindo ao seu gerenciador de tarefas!'

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = TodoRepository.get_by_id(todo_id)
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404 #Retornar erro 404 se não encontrado

    #Retornar o item como um dicionario
    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "done": todo.done
        }), 200

@app.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({'error':'Title is required'}), 400
    new_todo = TodoRepository.create(title=data['title'], description=data.get('description'))
    print(f"New todo created: {new_todo.id} - {new_todo.title}")
    return jsonify({"id": new_todo.id, "title": new_todo.title, "description": new_todo.description, "done": new_todo.done}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    data = request.get_json()
    todo = db.session.get(Todo, todo_id)
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.done = data.get('done', todo.done)
    db.session.commit()
    return jsonify(todo.to_dict()), 200
    

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    if TodoRepository.delete(todo_id):
        return '', 204
    return jsonify({'message': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
            