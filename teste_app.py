from app import app, db
from models import Todo
from repositorio import TodoRepository

#Contexto da aplicação
with app.app_context():
    #Limpar o banc de dados(opcional, omeçar do zer)
    db.drop_all()
    db.create_all()

    # Teste: Criar uma nova tarefa
    print('Criando uma nova tarefa...')
    todo = TodoRepository.create(title='Aprendendo Flask', description='Estudar framework Flask')
    print(f'tarefa criada: {todo.title}, {todo.description}, {todo.done}')

    #Recuperar todas as tarefas
    print('\nListando todas as tarefas...')
    todos = TodoRepository.get_all()
    for t in todos:
        print(f'tarefa:{t.title}, {t.description}, {t.done}')
    
    #Atualizar uma tarefa
    print('\nactualizando tarefa...')
    todo = TodoRepository.update(todo_id=1, done=True)
    print(f'tarefa actualizada:{todo.title}, {todo.description}, {todo.done}')

    #Buscar uma tarefa pelo ID
    print('\ndeletando a tarefa...')
    success = TodoRepository.delete(todo_id=1)
    print(f'tarefa deletada: {success}')

    #verificando se a tarefa foi deletada
    print('\nVerificando se a tarefa foi deletada...')
    todos = TodoRepository.get_all()
    print(f'Tarefas restantes: {todos}')
