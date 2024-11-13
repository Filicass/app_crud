from run import app
import unittest
from app import app, db
from models import Todo

class TestCrudAPI(unittest.TestCase):
    def setUp(self):
        #configurando o app para o testes
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' #Banco de dados em memoria
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            #Inserindo um Item de teste
            new_item = Todo(title='Test Item', description='Justa test item')
            db.session.add(new_item)
            db.session.commit()


    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_create_item(self):
        #Teste para criação de um novo Todo
        response = self.client.post('/todos', json={'title': 'Item Teste', 'description': 'Just a test Item'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        print(f"Response data: {data}")
        self.assertEqual(data['title'], 'Item Teste')
    
    def test_get_item(self):
        #Teste para recuperar um item existente
        post_response = self.client.post('/todos', json={'title': 'Item Teste', 'description': 'Just a test Item'})
        self.assertEqual(post_response.status_code, 201) #confirmando que o item foi criado

        #Capturar o id do item criado
        item_id = post_response.get_json().get('id')
        self.assertIsNotNone(item_id, 'O ID do item criado nao deve ser None')

        #Tentar Recuperar o item criado usando o id capturado
        get_response = self.client.get(f'/todos/{item_id}')
        self.assertEqual(get_response.status_code, 200, 'A resposta ao buscar deve ser 200')
        self.assertIn('Item Teste', get_response.get_data(as_text=True),'O titulo do item deve estar na' )

    def test_update_item(self):
        #Teste para actualizar um  item existente
        self.client.post('/todos', json={'title': 'Item Teste', 'description': 'Just a test Item'})
        response = self.client.put('/todos/1', json={'title': 'Item Actualizado', 'description': 'Just a test Item'})
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        #Teste para deletar um item existente
        post_response = self.client.post('/todos', json={'title': 'Item Teste', 'description': 'Just a test Item'})
        self.assertEqual(post_response.status_code,201) #confirmando que o item foi criado

        #capturando o id do item criado
        item_id = post_response.get_json().get('id')
        self.assertIsNotNone(item_id, 'O id do item criado nao deve ser None')

        #Temtar deletar o item criado usando o id da cptura
        delete_response = self.client.delete(f'/todos/{item_id}')
        self.assertEqual(delete_response.status_code, 204,) #a resposta ao deletar deve ser 204

        #verificação da excluão
        get_response = self.client.get(f'/todos/{item_id}')
        self.assertEqual(get_response.status_code, 404) #item não encontrado após a exlusão

if __name__=='__main__':
    unittest.main()
