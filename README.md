# Sistema de Busca ANS

Este projeto tem duas estapas, a primeira consiste em um WEBscraping em python que baixa arquivos pdf de uma pagina especifica trata seu dados para .csv, depois adiciona arquivos .csv a um banco de dados e faz consultas especificas nesses dados, a segunda etapa é uma interface web para busca de dados do relatório CADOP da ANS, integrando um backend Python com um frontend Vue.js.

## Estrutura do Projeto

O projeto está organizado em tres partes principais:

1. **Backend (Python)**
   - `main.py`: funcao principal do Webscraping
   - `/src`: pasta que contem os componentes usados 

2. **Backend (Python)**
   - `servidor.py`: Servidor Flask que processa as requisições de busca
   - `dados_ans/`: Diretório contendo o arquivo CSV com os dados das operadoras
   - `requirements.txt`: Lista de dependências Python

3. **Frontend (Vue.js)**
   - `frontend/`: Diretório contendo a aplicação Vue.js
   - `frontend/src/components/ProcurarComponente.vue`: Componente principal de busca
   - `frontend/src/App.vue`: Componente raiz da aplicação

## Configuração e Instalação

### Backend 1

1. Crie um ambiente virtual Python:
   ```bash
   python -m venv venv
   ```

2. Ative o ambiente virtual:
   - No Windows: `venv\Scripts\activate`
   - No macOS/Linux: `source venv/bin/activate`

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o servidor:
   ```bash
   python main.py
   ```
   O controle desta aplicação é feita no próprio console

### Backend 2

1. Crie um ambiente virtual Python:
   ```bash
   python -m venv venv
   ```

2. Ative o ambiente virtual:
   - No Windows: `venv\Scripts\activate`
   - No macOS/Linux: `source venv/bin/activate`

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o servidor:
   ```bash
   python servidor.py
   ```
   O servidor estará disponível em `http://localhost:5001`

### Frontend

1. Navegue até o diretório frontend:
   ```bash
   cd frontend
   ```

2. Instale as dependências:
   ```bash
   npm install
   ```

3. Execute o servidor de desenvolvimento:
   ```bash
   npm run serve
   ```
   A aplicação estará disponível em `http://localhost:8080`

## Funcionalidades

- **Busca em tempo real**: A busca é executada automaticamente enquanto o usuário digita
- **Resultados em tabela**: Os resultados são exibidos em uma tabela com scroll horizontal
- **Tratamento de erros**: Mensagens de erro amigáveis são exibidas quando ocorrem problemas
- **Suporte a caracteres especiais**: O sistema lida corretamente com acentos e caracteres UTF-8
- **Cache de dados**: O servidor mantém os dados em cache para melhorar o desempenho

## Tecnologias Utilizadas

- **Backend**:
  - Flask: Framework web para Python
  - Pandas: Manipulação de dados tabulares
  - Flask-CORS: Suporte a CORS para comunicação entre frontend e backend

- **Frontend**:
  - Vue.js: Framework JavaScript para interfaces de usuário
  - Axios: Cliente HTTP para requisições AJAX
  - CSS moderno: Estilos responsivos e interativos

## Endpoints da API

- `GET /api/search?q=termo`: Realiza uma busca pelo termo especificado
- `GET /api/health`: Verifica o status do servidor e retorna o número de registros carregados
