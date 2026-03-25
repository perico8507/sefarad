import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the tree
tree_match = re.search(r'(<div class=\'family-tree-container\' id=\'family-tree-container-div\'.*?</div>\s*</div>)', content, re.DOTALL)
tree_html = tree_match.group(1) if tree_match else ''

# Extract the transcriptions
transcripciones_match = re.search(r'(<div id="transcripciones".*?</div>\s*</div>)', content, re.DOTALL)
transcripciones_html = transcripciones_match.group(1) if transcripciones_match else ''

# We will build a new HTML from scratch, embedding the extracted parts.

new_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sefarad MX - Archivo Histórico</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Libre Baskerville', serif;
            background-color: #f4f1ea;
            color: #2c3e50;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        header {
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://upload.wikimedia.org/wikipedia/commons/1/15/Map_of_New_Spain_1744.jpg') no-repeat center center;
            background-size: cover;
            color: white;
            text-align: center;
            padding: 80px 20px;
            border-bottom: 5px solid #d4af37;
        }
        header h1 {
            font-family: 'Cinzel', serif;
            font-size: 4em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            letter-spacing: 2px;
            color: #f8f9fa;
        }
        header p {
            font-size: 1.2em;
            font-style: italic;
            max-width: 600px;
            margin: 20px auto;
            color: #eaddd0;
        }
        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }
        h2, h3 {
            font-family: 'Cinzel', serif;
            color: #1a1a1a;
            border-bottom: 2px solid #d4af37;
            padding-bottom: 10px;
        }
        .hero-section {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
            margin-bottom: 50px;
            background: white;
            padding: 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            border-radius: 8px;
            border-left: 5px solid #8b7355;
        }
        .hero-text {
            flex: 1;
            min-width: 300px;
        }
        .hero-image {
            flex: 1;
            min-width: 300px;
            text-align: center;
        }
        .hero-image img {
            max-width: 100%;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border: 3px solid #eaddd0;
        }
        .colonists-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }
        .colonist-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            border-top: 4px solid #d4af37;
        }
        .colonist-card h3 {
            border: none;
            color: #8b7355;
            margin-top: 0;
            padding-bottom: 0;
        }
        .document-list-container {
            background: #faf7f2; 
            border: 1px solid #d4af37; 
            padding: 30px; 
            margin: 20px 0;
        }
        .document-list-container ul {
            list-style: none; padding: 0;
        }
        .document-list-container li {
            margin-bottom: 15px; border-bottom: 1px solid #eaddd0; padding-bottom: 10px;
        }
        a {
            color: #8b7355;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            color: #d4af37;
            text-decoration: underline;
        }
        .footer {
            background: #1a1a1a;
            color: #f8f9fa;
            text-align: center;
            padding: 20px;
            font-family: 'Cinzel', serif;
            margin-top: 50px;
            border-top: 5px solid #d4af37;
        }
    </style>
</head>
<body>

<header>
    <h1>SEFARAD MX</h1>
    <p>Archivo Histórico de los Colonizadores Sefardíes del Noreste de México. Memoria, Genealogía e Identidad.</p>
</header>

<div class="container">

    <div class="hero-section">
        <div class="hero-text">
            <h2>El Legado Sefardí en el Noreste</h2>
            <p><strong>Sefarad MX</strong> representa uno de los archivos históricos más rigurosos dedicados a los linajes fundadores del noreste de México, con fuertes vínculos documentados a la diáspora judía originaria de Sefarad (la península ibérica).</p>
            <p>La migración de familias sefardíes, conversos o criptojudíos hacia la Nueva España en los siglos XVI y XVII fue un fenómeno documentado. Buscando escapar del alcance de la Santa Inquisición en el centro del virreinato, muchos cruzaron el Atlántico y se adentraron en los territorios de frontera extrema, fundando el Nuevo Reino de León y la Nueva Extremadura (hoy Coahuila, Nuevo León y Tamaulipas).</p>
            <p>Familias pioneras preservaron en el desierto no solo su sobrevivencia física frente a adversidades inmensas, sino también, a través del arraigo endogámico, indicios de su antigua fe y prácticas.</p>
        </div>
        <div class="hero-image">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Fundacion_de_Monterrey_por_Diego_de_Montemayor_1596.jpg" alt="Fundación de Monterrey">
            <p style="font-size: 0.8em; color: #555; margin-top: 10px;">Diego de Montemayor y los doce capitanes fundadores, muchos de ellos de origen sefardí, en la fundación de Monterrey (1596).</p>
        </div>
    </div>

    <h2>Los Patriarcas Colonizadores</h2>
    <div class="colonists-grid">
        <div class="colonist-card">
            <h3>Capitán Lucas García</h3>
            <p><strong>Fundador de Monterrey y Santa Catarina</strong></p>
            <p>Hijo de <em>Baltasar de Sosa</em> (identificado históricamente como cristiano nuevo de origen portugués) e <em>Inés Rodríguez de Montemayor</em>. Lucas fue uno de los doce capitanes de Diego de Montemayor en la fundación definitiva de Monterrey en 1596.</p>
            <p>Para evadir el escrutinio inquisitorial que asociaba ciertos apellidos con el judaísmo (tras el encarcelamiento de la familia Carvajal), Lucas y sus hermanos adoptaron los apellidos maternos "García" y "Rodríguez". Se le otorgaron las mercedes de la estancia de Santa Catalina, origen de la actual Santa Catarina, N.L.</p>
        </div>

        <div class="colonist-card">
            <h3>Lorenzo García Gutiérrez</h3>
            <p><strong>Alférez y Colonizador de Coahuila</strong></p>
            <p>Conocido como Lorenzo García Gutiérrez de Ábrego, hijo de Lorenzo Agustín García y Leonor de Ábrego. Su linaje fue crucial en la consolidación de Saltillo, Parras y las expediciones hacia Monclova.</p>
            <p>Su red de parentesco dio origen a linajes vitales del noreste como los <strong>García de la Garza</strong>. Integrados estrechamente con los Cavazos, Treviño y Garza, estos patriarcas formaron la élite empresarial, agrícola y ganadera que domó la región, conservando fuertemente el arraigo familiar característico de los descendientes conversos.</p>
        </div>
    </div>

    <h2>Archivo Digital de Registros Originales</h2>
    <p>A continuación se listan las actas y documentos digitalizados que certifican el linaje histórico. Cada documento ha sido nombrado conforme a su titular para garantizar la integridad del archivo.</p>
    
    <div class="document-list-container">
        <ul>
            <li><a href="perfiles/hermilo_garcia_garcia.html">Acta de Bautismo: Hermilo García García (1925)</a> - General Cepeda, Coahuila.</li>
            <li><a href="Acta_Bautismo_Francisco_Garcia_Peña_y_Martina_Garcia_Rodriguez.jpg" target="_blank">Acta de Bautismo: Francisco García Peña (1883)</a> - San Francisco de Patos.</li>
            <li><a href="Acta_Defuncion_Francisco_Garcia_Peña_General_Cepeda.jpg" target="_blank">Acta de Defunción: Francisco García Peña (1962)</a> - General Cepeda, Coahuila.</li>
            <li><a href="Acta_Defuncion_Asencion_Flores_Villanueva_General_Cepeda.jpg" target="_blank">Acta de Defunción: Asunción Flores Villanueva (1962)</a> - General Cepeda, Coahuila.</li>
            <li><a href="imagenes/Documento_Historico_Mateo_Garcia_y_Lucia_de_la_Cerda.jpg" target="_blank">Documento Histórico: Mateo García y Lucía de la Cerda</a> - Archivo de Saltillo.</li>
            <li><a href="imagenes/Acta_Bautismo_Emilio_Garcia_Peña_1887.jpg" target="_blank">Acta de Bautismo: Emilio García Peña (1887)</a> - San Francisco de Patos.</li>
            <li><a href="imagenes/Acta_Defuncion_Amador_Garcia_Peña_1957.jpg" target="_blank">Acta de Defunción: Amador García Peña (1957)</a> - General Cepeda, Coahuila.</li>
        </ul>
    </div>

    <!-- Injecting dynamically generated components -->
    INSERT_TRANSCRIPCIONES
    INSERT_TREE

</div>

<footer class="footer">
    <p>&copy; 2026 Frente Cardenista - Archivo Sefarad MX. Preservando el legado histórico e institucional.</p>
</footer>

</body>
</html>
"""

new_html = new_html.replace('INSERT_TRANSCRIPCIONES', transcripciones_html)
new_html = new_html.replace('INSERT_TREE', tree_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("index.html completely redesigned.")
