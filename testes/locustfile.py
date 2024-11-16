from locust import HttpUser, task, between

class CrudperformanceTest(HttpUser):
    #Definindo um tempo aleatoiro entre as requisições para simular usuarios reais
    wait_time = between(1, 5)

    @task
    def create_todo(self):
        #Teste de criação
        response = self.client.post('todos', json={'title': 'Item Teste', 'description': 'Teste Performance' })
        if response.status_code == 201:
            todo_id = response.json().get('id')
            self.read_todo(todo_id)
            self.update_todo(todo_id)
            self.delete_todo(todo_id)

    def read_todo(self, todo_id):
        #Teste de Leitura
        self.client.get(f'/todos/{todo_id}')

    def update_todo(self, todo_id):
        #Teste de actualização
        self.client.put(f'/todos/{todo_id}', json={'tiltle': 'Item Teste Atualizado', 'done': True})

    def delete_todo(self, todo_id):
        #Teste de exclusão
        self.client.delete(f'/todos/{todo_id}')
        