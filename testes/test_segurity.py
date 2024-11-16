import unittest
from app import app
from testes.test_unit import ConfigTeste

class TesteSeguranca(ConfigTeste):
    def test_acesso_sem_autenticação(self):
        #Tentando acessar um recurso protegido sem autenticação
        response = self.client.get('/todos')
        self.assertEqual(response.status_code, 401, 'Deveria retornar 401 para o acesso não autenticado')

    def test_acesso_com_token_invalido(self):
        #Tentando um recurso protegido com token invalido
        headers = {'Authorization': 'Bearer token_invalido'}
        response = self.client.get('/todos', headers = headers)
        self.assertEqual(response.status_code, 401, 'Deveria retornar 401 para token ivalido')

    def test_sql_injection(self):
        #Tentando injeção sql
        injection_data = {'title': "Teste'; DROP TABLE todos; --", 'description': 'Injection SQL'}
        response = self.client.post('/todos', json=injection_data)
        #Verificando que a resposta nao deve ser bem-sucedida(deveria retornar um erro e nao criar um item)
        self.assertNotEqual(response.status_code, 201, 'Injeção SQL nao deveria funcionar')
        self.assertNotIn('DROP TABLE', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
    