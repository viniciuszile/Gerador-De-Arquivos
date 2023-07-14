from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
import os
import shutil


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/download")
def download():
    return render_template("download.html")
    
# Rota para servir o arquivo ZIP
@app.route("/Aquivos/<path:filename>")
def serve_zip(filename):
    return send_from_directory("Aquivos", filename)

@app.route("/criar_arquivos", methods=["POST"])
def criar_arquivos():
    data = request.get_json()
    
    nome = data.get("nome")
    extensao = data.get("extensao")
    quantidade = data.get("quantidade")
    
    i = 0
    qtd_int = 0
    flag = False
    
    local = "Aquivos\\Arquivos_Criados"
    zip_filename = f"{nome}_arquivos.zip"
    
    if not os.path.exists(local):
        os.makedirs(local)
    
    try:
        qtd_int = int(quantidade)
        flag = True
    except ValueError:
        return jsonify({"success": False, "message": "Informe um número inteiro positivo."})
    
    try:
        if extensao[0] != ".":
            raise ValueError
        flag = True
    except ValueError:
        return jsonify({"success": False, "message": "Informe uma extensão válida."})
    
    if flag:
        while i < qtd_int:
            i += 1
            arquivo_nome = f"{nome}{i}{extensao}"
            arquivo_path = os.path.join(local, arquivo_nome)
            
            with open(arquivo_path, "w") as arquivo:
                arquivo.write("'Meu GitHub: viniciuszile'\n")
                arquivo.write("'Meu Instagram: viniciuszile'\n")
                arquivo.write("'Obrigado por usar.'\n")
        
        # Compacta os arquivos em um arquivo ZIP
        shutil.make_archive(local, "zip", local)
        
        # Exclui os arquivos individuais
        shutil.rmtree(local)
        
        # Retorna o arquivo ZIP para o usuário fazer o download
        return send_file(
            f"{local}.zip",
            as_attachment=True,
            attachment_filename=zip_filename
        )

if __name__ == "__main__":
    app.run()
