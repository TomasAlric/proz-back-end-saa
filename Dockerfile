# Usando uma imagem base com Python
FROM python:3.9

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para dentro do container
COPY . /app

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o Flask usa (padrão: 5000)
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "server.py"]