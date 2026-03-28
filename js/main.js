// js/main.js - Archivo Central de Operaciones
let sefaradData = null;
let profileMap = null;

async function loadSefaradData() {
    if (sefaradData) return sefaradData;
    try {
        const [dataRes, mapRes] = await Promise.all([
            fetch('supabase_data.json'),
            fetch('profile_map.json')
        ]);
        sefaradData = await dataRes.json();
        profileMap = await mapRes.json();
        return sefaradData;
    } catch (e) {
        console.error("Error cargando archivos de datos:", e);
        return null;
    }
}

function normalize(s) {
    return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]/g, "");
}

// --- TABS ---
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.header-nav a').forEach(el => el.classList.remove('active'));
    
    const view = document.getElementById('view-' + tabId);
    const tab = document.getElementById('tab-' + tabId);
    
    if (view) view.classList.add('active');
    if (tab) tab.classList.add('active');
    
    if (tabId === 'buscar') loadSefaradData();
}

// --- BÚSQUEDA AVANZADA ---
async function searchSupabase() {
    const btn = document.querySelector('#view-buscar .btn');
    btn.innerHTML = "CONSULTANDO...";
    btn.disabled = true;

    const list = document.getElementById('results-list');
    list.innerHTML = "";
    document.getElementById('search-results').style.display = "block";
    
    const queryNombres = document.getElementById('s_nombres').value.toLowerCase().trim();
    const queryApellidos = document.getElementById('s_apellidos').value.toLowerCase().trim();
    const queryLugar = document.getElementById('s_lugar').value.toLowerCase().trim();
    
    const data = await loadSefaradData();
    if (!data) {
        list.innerHTML = "<li style='color:red;'>Error de conexión con el archivo.</li>";
        btn.innerHTML = "REALIZAR CONSULTA"; btn.disabled = false;
        return;
    }

    const results = [];
    for (const id in data.individuals) {
        const p = data.individuals[id];
        const fullName = p.full_name.toLowerCase();
        const place = (p.birth_place || "" + p.death_place || "").toLowerCase();
        
        let match = true;
        if (queryNombres && !fullName.includes(queryNombres)) match = false;
        if (queryApellidos && !fullName.includes(queryApellidos)) match = false;
        if (queryLugar && !place.includes(queryLugar)) match = false;
        
        if (match && (queryNombres || queryApellidos || queryLugar)) {
            results.push({id, ...p});
            if (results.length >= 50) break;
        }
    }

    if (results.length === 0) {
        list.innerHTML = "<li>No se encontraron registros.</li>";
    } else {
        results.forEach(p => {
            const li = document.createElement('li');
            li.className = "search-result-item";
            
            // Check if we have a real profile link
            const clean = normalize(p.full_name);
            const profileUrl = profileMap[clean] ? `perfiles/${profileMap[clean]}` : null;
            
            li.innerHTML = `
                <div style="padding:20px; border-bottom:1px solid #ddd; background:#fff;">
                    <strong style="font-family:'Cinzel',serif; font-size:1.2rem; color:var(--primary-dark);">${p.full_name}</strong><br>
                    <span style="color:#666;">${p.birth_date || '?'} — ${p.death_date || '?'}</span><br>
                    <span style="font-size:0.9rem; font-style:italic;">${p.birth_place || 'Origen no registrado'}</span><br>
                    ${profileUrl ? `<a href="${profileUrl}" style="display:inline-block; margin-top:10px; color:var(--primary-gold-dim); font-weight:bold;">VER EXPEDIENTE COMPLETO 📜</a>` 
                                : `<span style="font-size:0.8rem; color:#999; display:block; margin-top:10px;">(Acta digital en proceso de indexación)</span>`}
                </div>
            `;
            list.appendChild(li);
        });
    }
    btn.innerHTML = "REALIZAR CONSULTA"; btn.disabled = false;
}

// --- AUTH & UPLOAD ---
async function loginWithSupabase() {
    const email = document.getElementById('loginEmail').value;
    const pass = document.getElementById('loginPass').value;
    if(!email || !pass) return;
    try {
        const { error } = await window.supabase.auth.signInWithPassword({ email, password: pass });
        if(error) throw error;
        location.reload();
    } catch(e) { alert(e.message); }
}

async function uploadToSupabase(e) {
    const file = e.target.files[0];
    if(!file) return;
    const { data: { user } } = await window.supabase.auth.getUser();
    if(!user) { document.getElementById('loginModal').style.display='flex'; return; }
    
    const { error } = await window.supabase.storage.from('memories').upload(`${Date.now()}_${file.name}`, file);
    if(error) alert(error.message);
    else { alert("Documento resguardado."); location.reload(); }
}
