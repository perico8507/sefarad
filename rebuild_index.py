import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the tree
tree_match = re.search(r'(<div class=\'family-tree-container\' id=\'family-tree-container-div\'.*?</div>\s*</div>)', content, re.DOTALL)
tree_html = tree_match.group(1) if tree_match else ''

# Extract the transcriptions
transcripciones_match = re.search(r'(<div id="transcripciones".*?</div>\s*</div>)', content, re.DOTALL)
transcripciones_html = transcripciones_match.group(1) if transcripciones_match else ''

# Clean up existing inline styles from injected content to fit the dark museum theme
if tree_html:
    tree_html = tree_html.replace('background: #faf7f2;', 'background: #1a1a1a;')
    tree_html = tree_html.replace('color: #1a1a1a;', 'color: #eaddd0;')
    tree_html = tree_html.replace('color: #2c3e50;', 'color: #d4af37;')
    tree_html = tree_html.replace('color: #555;', 'color: #a0a0a0;')

if transcripciones_html:
    transcripciones_html = transcripciones_html.replace('background: #fbfbfb;', 'background: #111;')
    transcripciones_html = transcripciones_html.replace('background: white;', 'background: #1a1a1a;')
    transcripciones_html = transcripciones_html.replace('color: #1a1a1a;', 'color: #eaddd0;')
    transcripciones_html = transcripciones_html.replace('color: #4a4a4a;', 'color: #ccc;')
    transcripciones_html = transcripciones_html.replace('color: #2c3e50;', 'color: #d4af37;')
    transcripciones_html = transcripciones_html.replace('color: #555;', 'color: #a0a0a0;')
    transcripciones_html = transcripciones_html.replace('border-left: 4px solid #8b7355;', 'border-left: 4px solid #d4af37;')

new_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sefarad MX - Museo y Archivo Histórico</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0d0c0b; /* Very dark warm museum gray/black */
            --text-main: #e8e3d9; /* Off-white parchment */
            --accent-gold: #d4af37;
            --accent-gold-dim: #8b7355;
            --card-bg: #161513;
            --border-glow: 0 0 15px rgba(212, 175, 55, 0.15);
        }
        
        body {
            font-family: 'Libre Baskerville', serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.7;
            background-image: radial-gradient(circle at center, #1a1816 0%, #0d0c0b 100%);
            background-attachment: fixed;
        }

        /* MUSEUM HEADER */
        header {
            position: relative;
            height: 70vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border-bottom: 2px solid var(--accent-gold-dim);
            overflow: hidden;
        }
        
        .header-bg {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: url('https://upload.wikimedia.org/wikipedia/commons/1/15/Map_of_New_Spain_1744.jpg') no-repeat center center;
            background-size: cover;
            opacity: 0.15;
            z-index: 0;
            filter: grayscale(50%) sepia(30%);
        }
        
        .header-content {
            position: relative;
            z-index: 1;
            padding: 0 20px;
        }

        header h1 {
            font-family: 'Cinzel', serif;
            font-size: 5vw;
            margin: 0;
            font-weight: 700;
            letter-spacing: 8px;
            color: var(--accent-gold);
            text-transform: uppercase;
            text-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
        }
        
        header p {
            font-size: 1.3em;
            font-style: italic;
            max-width: 800px;
            margin: 30px auto 0;
            color: #b5b0a1;
            letter-spacing: 1px;
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 60px 20px;
        }

        /* TYPOGRAPHY */
        h2, h3 {
            font-family: 'Cinzel', serif;
            color: var(--accent-gold);
            font-weight: 600;
        }
        
        h2 {
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 50px;
            position: relative;
            padding-bottom: 20px;
        }
        
        h2::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 2px;
            background: var(--accent-gold-dim);
        }

        /* EXHIBIT HERO SECTION */
        .exhibit-section {
            display: flex;
            flex-wrap: wrap;
            gap: 50px;
            margin-bottom: 100px;
            align-items: center;
        }

        .exhibit-text {
            flex: 1;
            min-width: 300px;
            font-size: 1.1em;
            color: #d1cbc0;
        }

        .exhibit-text p {
            margin-bottom: 20px;
            text-align: justify;
        }

        /* FRAME / PAINTING EFFECT */
        .exhibit-frame {
            flex: 1;
            min-width: 300px;
            text-align: center;
            padding: 20px;
            background: #000;
            border: 1px solid #333;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8), var(--border-glow);
            position: relative;
        }
        
        .exhibit-frame::before {
            content: '';
            position: absolute;
            top: 10px; left: 10px; right: 10px; bottom: 10px;
            border: 2px solid var(--accent-gold-dim);
            pointer-events: none;
        }

        .exhibit-frame img {
            max-width: 100%;
            display: block;
            filter: brightness(0.9) contrast(1.1);
            transition: transform 0.5s ease, filter 0.5s ease;
        }
        
        .exhibit-frame:hover img {
            transform: scale(1.02);
            filter: brightness(1) contrast(1.1);
        }

        .exhibit-caption {
            font-size: 0.85em;
            color: #888;
            margin-top: 15px;
            font-family: 'Libre Baskerville', serif;
            font-style: italic;
        }

        /* GALLERY GRID */
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 40px;
            margin-bottom: 100px;
        }

        /* PEDESTAL CARD EFFECT */
        .gallery-card {
            background: var(--card-bg);
            padding: 40px 30px;
            border: 1px solid #2a2620;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: all 0.4s ease;
            position: relative;
            text-align: center;
        }
        
        .gallery-card::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; width: 100%; height: 3px;
            background: var(--accent-gold-dim);
            transition: height 0.3s ease, background 0.3s ease;
        }

        .gallery-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.8), var(--border-glow);
            border-color: var(--accent-gold-dim);
        }
        
        .gallery-card:hover::after {
            height: 5px;
            background: var(--accent-gold);
        }

        .gallery-card h3 {
            font-size: 1.5em;
            margin-top: 0;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }

        /* DOCUMENTS GALLERY */
        .documents-hall {
            background: #111;
            border: 1px solid #333;
            padding: 50px;
            margin: 50px 0;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
        }
        
        .documents-hall ul {
            list-style: none;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
        }

        .documents-hall li {
            background: var(--card-bg);
            padding: 20px;
            border-left: 3px solid var(--accent-gold-dim);
            transition: all 0.3s ease;
        }

        .documents-hall li:hover {
            background: #1a1815;
            border-left-color: var(--accent-gold);
            transform: translateX(5px);
        }

        a {
            color: var(--accent-gold);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        a:hover {
            color: #fff;
        }

        /* FOOTER */
        .footer {
            background: #050505;
            color: #666;
            text-align: center;
            padding: 40px 20px;
            font-family: 'Cinzel', serif;
            border-top: 1px solid #222;
            letter-spacing: 2px;
            font-size: 0.9em;
        }
        
        /* OVERRIDE FOR INJECTED CONTENT TO FIT MUSEUM THEME */
        #transcripciones, #family-tree-container-div {
            background: #111 !important;
            border-color: #333 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        }
    </style>
</head>
<body>

<header>
    <div class="header-bg"></div>
    <div class="header-content">
        <h1>SEFARAD MX</h1>
        <p>Archivo Histórico y Museo Digital de los Colonizadores Sefardíes del Noreste de México. Memoria, Genealogía e Identidad.</p>
    </div>
</header>

<div class="container">

    <div class="exhibit-section">
        <div class="exhibit-text">
            <h2>El Legado en la Frontera</h2>
            <p><strong>Sefarad MX</strong> representa uno de los archivos históricos más rigurosos dedicados a los linajes fundadores del noreste de México, con fuertes vínculos documentados a la diáspora judía originaria de Sefarad (la península ibérica).</p>
            <p>La migración de familias sefardíes, conversos o criptojudíos hacia la Nueva España en los siglos XVI y XVII fue un fenómeno documentado. Buscando escapar del alcance de la Santa Inquisición en el centro del virreinato, cruzaron el Atlántico y se adentraron en los territorios de frontera extrema, fundando el Nuevo Reino de León y la Nueva Extremadura (hoy Coahuila, Nuevo León y Tamaulipas).</p>
            <p>En este museo digital preservamos las actas, manuscritos y la memoria viva de aquellos pioneros que forjaron su supervivencia en el desierto, manteniendo en el arraigo endogámico indicios de su origen.</p>
        </div>
        <div class="exhibit-frame">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Fundacion_de_Monterrey_por_Diego_de_Montemayor_1596.jpg" alt="Fundación de Monterrey">
            <div class="exhibit-caption">Óleo representativo: Diego de Montemayor y los doce capitanes fundadores, de linaje converso, en la fundación de Monterrey (1596).</div>
        </div>
    </div>

    <h2>Sala de Patriarcas</h2>
    <div class="gallery-grid">
        <div class="gallery-card">
            <h3>Capitán Lucas García</h3>
            <p style="color: var(--accent-gold-dim); font-size: 0.9em; font-family: 'Cinzel', serif;">Fundador de Monterrey y Santa Catarina</p>
            <p style="font-size: 0.95em; color: #b5b0a1; text-align: justify; margin-top: 20px;">Hijo de <em>Baltasar de Sosa</em> (cristiano nuevo de origen portugués) e <em>Inés Rodríguez de Montemayor</em>. Uno de los doce capitanes de Diego de Montemayor en la fundación de Monterrey (1596).</p>
            <p style="font-size: 0.95em; color: #b5b0a1; text-align: justify;">Para evadir la persecución inquisitorial tras el caso Carvajal, adoptó apellidos maternos. Recibió mercedes en Santa Catalina, hoy Santa Catarina, N.L.</p>
        </div>

        <div class="gallery-card">
            <h3>Lorenzo García Gutiérrez</h3>
            <p style="color: var(--accent-gold-dim); font-size: 0.9em; font-family: 'Cinzel', serif;">Alférez y Colonizador de Coahuila</p>
            <p style="font-size: 0.95em; color: #b5b0a1; text-align: justify; margin-top: 20px;">Conocido como Lorenzo García Gutiérrez de Ábrego. Su linaje fue crucial en la consolidación de Saltillo, Parras y las expediciones hacia Monclova.</p>
            <p style="font-size: 0.95em; color: #b5b0a1; text-align: justify;">Patriarca vital de la región, dando origen a los <strong>García de la Garza</strong>. Integrados con los Cavazos, Treviño y Garza, dominaron la ganadería y agricultura regional conservando fuerte endogamia.</p>
        </div>
    </div>

    <h2>Bóveda de Documentos Originales</h2>
    <div class="documents-hall">
        <ul>
            <li><a href="perfiles/hermilo_garcia_garcia.html">Acta de Bautismo: Hermilo García García (1925)</a><br><span style="font-size: 0.8em; color: #888;">General Cepeda, Coahuila</span></li>
            <li><a href="Acta_Bautismo_Francisco_Garcia_Peña_y_Martina_Garcia_Rodriguez.jpg" target="_blank">Acta de Bautismo: Francisco García Peña (1883)</a><br><span style="font-size: 0.8em; color: #888;">San Francisco de Patos</span></li>
            <li><a href="Acta_Defuncion_Francisco_Garcia_Peña_General_Cepeda.jpg" target="_blank">Acta de Defunción: Francisco García Peña (1962)</a><br><span style="font-size: 0.8em; color: #888;">General Cepeda, Coahuila</span></li>
            <li><a href="Acta_Defuncion_Asencion_Flores_Villanueva_General_Cepeda.jpg" target="_blank">Acta de Defunción: Asunción Flores Villanueva (1962)</a><br><span style="font-size: 0.8em; color: #888;">General Cepeda, Coahuila</span></li>
            <li><a href="imagenes/Documento_Historico_Mateo_Garcia_y_Lucia_de_la_Cerda.jpg" target="_blank">Documento Histórico: Mateo García y Lucía de la Cerda</a><br><span style="font-size: 0.8em; color: #888;">Archivo de Saltillo</span></li>
            <li><a href="imagenes/Acta_Bautismo_Emilio_Garcia_Peña_1887.jpg" target="_blank">Acta de Bautismo: Emilio García Peña (1887)</a><br><span style="font-size: 0.8em; color: #888;">San Francisco de Patos</span></li>
            <li><a href="imagenes/Acta_Defuncion_Amador_Garcia_Peña_1957.jpg" target="_blank">Acta de Defunción: Amador García Peña (1957)</a><br><span style="font-size: 0.8em; color: #888;">General Cepeda, Coahuila</span></li>
        </ul>
    </div>

    <!-- Injecting dynamically generated components -->
    INSERT_TRANSCRIPCIONES
    INSERT_TREE

</div>

<footer class="footer">
    <p>&copy; 2026 GRUPO EMPRESARIAL GARGA & FRENTE CARDENISTA<br>Archivo Sefarad MX. Custodiando la Memoria Institucional.</p>
</footer>

</body>
</html>
"""

new_html = new_html.replace('INSERT_TRANSCRIPCIONES', transcripciones_html)
new_html = new_html.replace('INSERT_TREE', tree_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("index.html completely redesigned with Museum Theme.")
