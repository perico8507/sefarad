import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

transcriptions_html = """
<div id="transcripciones" style="background: #fbfbfb; border: 1px solid #d4af37; padding: 30px; margin: 20px 0; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
    <h3 style='font-family: "Cinzel", serif; color: #1a1a1a; margin-top:0; border-bottom: 2px solid #d4af37; padding-bottom: 10px;'>Fichas de Extracción de Documentos Históricos</h3>
    <p style="font-family: 'Libre Baskerville', serif; color: #4a4a4a; font-size: 0.95em;">
        A continuación se presenta la información extraída de los manuscritos del Registro Civil y Parroquial de General Cepeda, Coahuila:
    </p>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;">
        <!-- Ficha 1 -->
        <div style="background: white; padding: 15px; border-left: 4px solid #8b7355; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="margin:0 0 10px 0; color: #2c3e50;">Francisco García Peña</h4>
            <ul style="margin:0; padding-left: 20px; font-size: 0.9em; color: #555;">
                <li><strong>Nacimiento / Bautismo:</strong> ~1883, San Francisco de Patos.</li>
                <li><strong>Defunción:</strong> 1962, General Cepeda, Coahuila.</li>
                <li><strong>Cónyuge:</strong> Martina García Rodríguez.</li>
                <li><strong>Hijos documentados:</strong> Hermilo García García.</li>
            </ul>
        </div>

        <!-- Ficha 2 -->
        <div style="background: white; padding: 15px; border-left: 4px solid #8b7355; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="margin:0 0 10px 0; color: #2c3e50;">Emilio García Peña</h4>
            <ul style="margin:0; padding-left: 20px; font-size: 0.9em; color: #555;">
                <li><strong>Nacimiento / Bautismo:</strong> 1887, San Francisco de Patos.</li>
                <li><strong>Padres:</strong> (Pendiente de confirmación paleográfica).</li>
                <li><strong>Nota:</strong> Registro ubicado en FamilySearch, Imagen 29 de 727, Grupo 004896335.</li>
            </ul>
        </div>
        
        <!-- Ficha 3 -->
        <div style="background: white; padding: 15px; border-left: 4px solid #8b7355; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="margin:0 0 10px 0; color: #2c3e50;">Hermilo García García</h4>
            <ul style="margin:0; padding-left: 20px; font-size: 0.9em; color: #555;">
                <li><strong>Nacimiento / Bautismo:</strong> 1925, General Cepeda, Coahuila.</li>
                <li><strong>Padres:</strong> Francisco García Peña y Martina García Rodríguez.</li>
                <li><strong>Abuelos Paternos:</strong> Familia García Peña.</li>
            </ul>
        </div>
        
        <!-- Ficha 4 -->
        <div style="background: white; padding: 15px; border-left: 4px solid #8b7355; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="margin:0 0 10px 0; color: #2c3e50;">Asunción Flores Villanueva</h4>
            <ul style="margin:0; padding-left: 20px; font-size: 0.9em; color: #555;">
                <li><strong>Defunción:</strong> 1962, General Cepeda, Coahuila.</li>
                <li><strong>Nota:</strong> Documento custodiado en el Archivo del Registro Civil.</li>
            </ul>
        </div>
    </div>
</div>
"""

insertion_point = '<h2><span class="mw-headline" id="El_Legado_Sefardí">'

if insertion_point in content:
    new_content = content.replace(insertion_point, transcriptions_html + '\n\n' + insertion_point)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Transcriptions injected successfully.")
else:
    print("Insertion point not found.")
