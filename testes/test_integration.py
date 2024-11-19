import unittest
from app import app, db
from models import Todo
from testes.test_unit import ConfigTeste

class TesteCrudIntegration(ConfigTeste):
    def test_full_crud_flow(self):
        #1 criação
        response = self.client.post('/todos', json={'title': 'Novo Item', 'description': 'Teste de Integração'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        item_id = data['id']

        #2 leitura
        response = self.client.get(f'/todos/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Novo Item', response.get_data(as_text=True))

        #3 Atualização
        response = self.client.put(f'/todos/{item_id}', json={'title': 'Item Atualizado', 'done': True})
        self.assertEqual(response.status_code, 200)

        #4 confirmação de actualização
        response = self.client.get(f'/todos/{item_id}')
        data = response.get_json()
        self.assertEqual(data['title'],'Item Atualizado')
        self.assertTrue(data['done'])

        #5 Excusão
        response = self.client.delete(f'/todos/{item_id}')
        self.assertEqual(response.status_code, 204)

        #6 confirmação da exclusão
        response = self.client.get(f'/todos/{item_id}')
        self.assertEqual(response.status_code, 404) #item nao encontrado apos a exclusão

if __name__ == '__main__':
    unittest.main()
    