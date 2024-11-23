import unittest
from app import app, db
from models import Todo
from testes.test_unit import ConfigTeste

class TestecrudFuncional(ConfigTeste):
    def login_and_get_token(self):
        #Simula o login para obeter um token JWT
        response = self.client.post('/login',json={'username': 'Test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200, 'Login falhou')
        data = response.get_json()
        return data.get('access_token')
    
    def test_full_crud_flow(self):
        #Realizanfo um login e obtendo token
        token = self.login_and_get_token()
        headers = {'Authorization': f'Bearer{token}'}

        #1. criar um novo item(POST)
        response = self.client.post('/todos', json={'title': 'Test Item', 'description': 'Item criado no teste Funcional'})
        self.assertEqual(response.status_code, 201)
        item_data = response.get_json()
        item_id = item_data['id'] #pegando o id do item criado

        #2 Ler o item criado(GET)
        response = self.client.get(f'/todos/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], 'Test Item')

        #3 Actualizar o item(PUT)
        response = self.client.put(f'/todos/{item_id}', json={'title': 'Item Atualizado', 'description': 'Descrição atualizada'})
        self.assertEqual(response.status_code, 200)
        #Verificando se o item foi actualizado
        response = self.client.get(f'/todos/{item_id}')
        self.assertEqual(response.get_json()['title'], 'Item Atualizado')
        self.assertEqual(response.get_json()['description'], 'Descrição atualizada')

        #4 Deletear o item (DELETE)
        response = self.client.delete(f'/todos/{item_id}')
        #verificar se o item foi removido(GET)
        response = self.client.get(f'/todos/{item_id}', headers=headers)
        self.assertEqual(response.status_code, 404) #O item nao deve mais existir

if __name__ == '__main__':
    unittest.main
    