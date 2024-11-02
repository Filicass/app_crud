from models import Todo
from app  import db

class TodoRepository:
    @staticmethod
    def get_all():
        return Todo.query.all()

    @staticmethod
    def get_by_id(todo_id):
        return db.session.get(Todo, todo_id)
    
    @staticmethod
    def create(title, description=None):
        new_todo = Todo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo

    @staticmethod
    def update(todo_id, title=None, description=None, done=None):
        todo = db.session.get(Todo, todo_id)
        if todo:
            if title:
                todo.title = title
            if description:
                todo.description = description
            if done is not None:
                todo.done = done
            db.session.commit()
        return todo

    @staticmethod
    def delete(todo_id):
        todo = db.session.get(todo_id)
        if todo:
            db.session.delete(todo)
            try:
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f'Error deleting todo: {e}')
        return False
        