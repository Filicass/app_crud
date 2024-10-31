import unittest
from app import app, db
from models import Todo

class TestecrudFuncional(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #configuração inicial da aplicação e do cliente teste
        cls.app = app
        cls.app.testing = True
        cls.client = cls.app.test_client()

        #limpando o banco de dados antes dos testes funcionais
        with cls.app.app_context():
            db.drop_all()
            db.create_all()

    def test_full_crud_flow(self):
        #1. criar um novo item(POST)
        response = self.client.post('/todos', json={'title': 'Item Teste', 'description': 'Item criado no teste Funcional'})
        self.assertEqual(response.status_code, 201)
        item_data = response.get_json()
        item_id = item_data['id'] #pegando o id do item criado

        #2 Ler o item criado(GET)
        response = self.client.get(f'/todos/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get.get_json()['title'], 'Item Teste')

        #3 Actualizar o item(PUT)
        response = self.cliente.put(f'/todos/{item_id}', json={'title': 'Item Atualizado', 'description': 'Descrição actualizada'})
        self.assertEqual(response.status_code, 200)
        #Verificando se o item foi actualizado
        response = self.client.get(f'/todos{item_id}')
        self.assertEqual(response.get_json()['title'], 'Item Actualizado')
        self.assertEqual(response.get_json()['description'], 'Descrição atualizada')

        #4 Deletear o item (DELETE)
        response = self.client.delete(f'/todos/{item_id}')
        #verificar se o item foi removido(GET)
        response = self.client.get('/todos/{item_id}')
        self.assertEqual((response.status_code, 404)) #O item nao deve mais existir

    @classmethod
    def tearDownClass(cls):
         #Limpar  banco de dados apos os testes
        with cls.app.app_context():
            db.drop_all()
if __name__ == '__main__':
    unittest.main
    