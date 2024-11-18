from app import db

class Todo(db.Model):
    task_daive = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id, 
            'title': self.title, 
            'description':self.description, 
            'done': self.done
        }
        