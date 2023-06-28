from flask import Flask, render_template, request, send_from_directory 
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'img'

namefiles =""

@app.route('/', methods=['GET', 'POST'])
def index():
    global namefiles

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if request.method == 'POST':
        file = request.files['file']
        namefiles = file.filename
        if file:
            # Leer el archivo CSV
            file.save(os.path.join(UPLOAD_FOLDER, namefiles))
            
            file = open(os.path.join(UPLOAD_FOLDER, namefiles), 'r')
            df = pd.read_csv(file)

            # Obtener las columnas disponibles en el archivo
            columns = df.columns.tolist()

            return render_template('index.html', columns=columns)

    return render_template('index.html', columns=None)

@app.route('/generate_plot', methods=['POST'])
def generate_plot():
    selected_columns = request.form.getlist('columns')

    # Leer el archivo CSV nuevamente
    file = open(os.path.join(UPLOAD_FOLDER, namefiles), 'r')
    df = pd.read_csv(file)

    # Filtrar el DataFrame según las columnas seleccionadas
    filtered_df = df[selected_columns]

    # Generar el gráfico estadístico
    
    plot = filtered_df.plot()
    filename = 'plot.png'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    plt.savefig(filepath)

    # Guardar el gráfico en un objeto BytesIO
    #image_stream = BytesIO()
    #plt.savefig(image_stream, format='png')
    #plt.close()

    # Codificar la imagen en base64 para su visualización en HTML
    #encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    #root_dir = 'C://Users//usser//Desktop//Infografia//Final//img'
    root_dir = os.getcwd()
    
    return send_from_directory(os.path.join(root_dir,'img'), filename)
    #return render_template('index.html', columns=selected_columns, plot=encoded_image)

if __name__ == '__main__':
    app.run(debug=True)

