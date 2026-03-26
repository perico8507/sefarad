let sefaradData = null;

async function loadSefaradData() {
    if (sefaradData) return sefaradData;
    try {
        const response = await fetch('supabase_data.json');
        sefaradData = await response.text();
        sefaradData = JSON.parse(sefaradData);
        console.log("Sefarad Data loaded:", Object.keys(sefaradData.individuals).length, "individuals");
        return sefaradData;
    } catch (e) {
        console.error("Failed to load supabase_data.json", e);
        return null;
    }
}

// --- 1. TAB NAVIGATION ---
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.header-nav a').forEach(el => el.classList.remove('active'));
    
    document.getElementById('view-' + tabId).classList.add('active');
    document.getElementById('tab-' + tabId).classList.add('active');
    
    if (tabId === 'buscar') {
        loadSefaradData();
    }
}

// --- 2. INTERACTIVE TREE (COLLAPSE/EXPAND & PAN/ZOOM) ---
function initializeTree() {
    const treeContainer = document.getElementById('family-tree-container-div');
    if(treeContainer) {
        // Parse tree nodes to add toggle buttons and structure
        const nodes = treeContainer.querySelectorAll('.tree-node');
        
        nodes.forEach(node => {
            // Find direct child nodes
            const children = Array.from(node.children).filter(child => child.classList.contains('tree-node'));
            
            if(children.length > 0) {
                // Skip if already has a toggle
                if (node.querySelector('.tree-node-toggle')) return;

                // Create toggle button
                const toggleBtn = document.createElement('span');
                toggleBtn.className = 'tree-node-toggle';
                toggleBtn.innerHTML = '−';
                
                // Wrap children in a container for collapsing
                const childrenContainer = document.createElement('div');
                childrenContainer.className = 'tree-children';
                
                // Move children into container
                children.forEach(child => childrenContainer.appendChild(child));
                node.appendChild(childrenContainer);
                
                // Insert toggle before the strong tag (the name)
                const strongTag = node.querySelector('strong');
                if(strongTag) {
                    node.insertBefore(toggleBtn, strongTag);
                }
                
                // Add click event to toggle
                toggleBtn.onclick = function(e) {
                    e.stopPropagation();
                    const isCollapsed = childrenContainer.classList.contains('collapsed');
                    if(isCollapsed) {
                        childrenContainer.classList.remove('collapsed');
                        toggleBtn.innerHTML = '−';
                    } else {
                        childrenContainer.classList.add('collapsed');
                        toggleBtn.innerHTML = '+';
                    }
                };
                
                // Optionally start with older generations collapsed (e.g., deeply nested)
                const marginLeft = parseInt(node.style.marginLeft || 0);
                if(marginLeft > 150) {
                    childrenContainer.classList.add('collapsed');
                    toggleBtn.innerHTML = '+';
                }
            }
        });
        
        // Pan and Zoom functionality
        let isDragging = false;
        let startX, startY, scrollLeft, scrollTop;

        treeContainer.onmousedown = (e) => {
            isDragging = true;
            startX = e.pageX - treeContainer.offsetLeft;
            startY = e.pageY - treeContainer.offsetTop;
            scrollLeft = treeContainer.scrollLeft;
            scrollTop = treeContainer.scrollTop;
            treeContainer.style.cursor = 'grabbing';
        };
        
        window.onmouseup = () => { 
            isDragging = false; 
            if(treeContainer) treeContainer.style.cursor = 'grab';
        };
        
        window.onmousemove = (e) => {
            if(!isDragging || !treeContainer) return;
            e.preventDefault();
            const x = e.pageX - treeContainer.offsetLeft;
            const y = e.pageY - treeContainer.offsetTop;
            const walkX = (x - startX) * 1.5; // Drag speed
            const walkY = (y - startY) * 1.5;
            treeContainer.scrollLeft = scrollLeft - walkX;
            treeContainer.scrollTop = scrollTop - walkY;
        };
    }
}

document.addEventListener('DOMContentLoaded', initializeTree);
window.initializeTree = initializeTree;

// --- 3. SUPABASE & DATA FUNCTIONS ---
async function loginWithSupabase() {
    const email = document.getElementById('loginEmail').value;
    const pass = document.getElementById('loginPass').value;
    
    if(!email || !pass) {
        alert("Por favor ingresa credenciales."); return;
    }
    
    try {
        const supabaseClient = window.supabase;
        if(supabaseClient) {
            const { data, error } = await supabaseClient.auth.signInWithPassword({
                email: email, password: pass
            });
            if(error) throw error;
            alert("Sesión iniciada correctamente.");
            location.reload();
        } else {
            alert("Sistema de autenticación no disponible.");
        }
    } catch(e) {
        alert("Error: " + e.message);
    }
}

async function searchSupabase() {
    const btn = document.querySelector('#view-buscar .btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = "Consultando Archivo...";
    btn.disabled = true;

    const resDiv = document.getElementById('search-results');
    const list = document.getElementById('results-list');
    list.innerHTML = "";
    resDiv.style.display = "block";
    
    const queryNombres = document.getElementById('s_nombres').value.toLowerCase().trim();
    const queryApellidos = document.getElementById('s_apellidos').value.toLowerCase().trim();
    const queryLugar = document.getElementById('s_lugar') ? document.getElementById('s_lugar').value.toLowerCase().trim() : "";
    
    if (!queryNombres && !queryApellidos && !queryLugar) {
        list.innerHTML = "<li style='padding:15px; color:red;'>Por favor ingrese al menos un criterio de búsqueda.</li>";
        btn.innerHTML = originalText;
        btn.disabled = false;
        return;
    }

    const data = await loadSefaradData();
    if (!data) {
        list.innerHTML = "<li style='padding:15px; color:red;'>Error al cargar el archivo de datos.</li>";
        btn.innerHTML = originalText;
        btn.disabled = false;
        return;
    }

    const results = [];
    for (const id in data.individuals) {
        const p = data.individuals[id];
        const fullName = p.full_name.toLowerCase();
        const birthPlace = (p.birth_place || "").toLowerCase();
        const deathPlace = (p.death_place || "").toLowerCase();
        
        let match = true;
        if (queryNombres && !fullName.includes(queryNombres)) match = false;
        if (queryApellidos && !fullName.includes(queryApellidos)) match = false;
        if (queryLugar && !(birthPlace.includes(queryLugar) || deathPlace.includes(queryLugar))) match = false;
        
        if (match) {
            results.push(p);
            if (results.length >= 50) break; // Limit results
        }
    }

    if (results.length === 0) {
        list.innerHTML = "<li style='padding:15px;'>No se encontraron registros que coincidan con los criterios.</li>";
    } else {
        results.forEach(p => {
            const li = document.createElement('li');
            li.style.padding = "20px";
            li.style.borderBottom = "1px solid var(--border-gold)";
            li.style.background = "white";
            li.style.marginBottom = "10px";
            
            const birth = p.birth_date ? `Nacimiento: ${p.birth_date}` : "";
            const death = p.death_date ? `Defunción: ${p.death_date}` : "";
            const place = p.birth_place || p.death_place || "Origen: Noreste de México";
            
            li.innerHTML = `
                <strong style="color:var(--text-dark); font-size:1.2rem; font-family:'Cinzel', serif;">${p.full_name}</strong><br>
                <span style="color:var(--text-muted); font-size:0.9rem;">${birth} ${death ? ' • ' + death : ''}</span><br>
                <span style="color:var(--text-muted); font-size:0.9rem; font-style:italic;">${place}</span><br>
                <a href="#" onclick="alert('Funcionalidad de perfil detallado en desarrollo para este registro.')" style="font-size:0.85rem; font-weight:bold; margin-top:10px; display:inline-block; color:var(--primary-gold-dim);">Ver Expediente Completo →</a>
            `;
            list.appendChild(li);
        });
    }

    btn.innerHTML = originalText;
    btn.disabled = false;
}

async function uploadToSupabase(e) {
    const file = e.target.files[0];
    if(!file) return;

    const supabaseClient = window.supabase;
    if(!supabaseClient) {
        alert("Cliente Supabase no disponible.");
        return;
    }

    // Check auth
    const { data: { user } } = await supabaseClient.auth.getUser();
    if(!user) {
        alert("Debe iniciar sesión para subir archivos al repositorio institucional.");
        document.getElementById('loginModal').style.display = 'flex';
        return;
    }

    const fileName = `${Date.now()}_${file.name}`;
    const { data, error } = await supabaseClient.storage
        .from('memories')
        .upload(fileName, file);

    if (error) {
        alert("Error al subir archivo: " + error.message);
    } else {
        alert("Documento resguardado exitosamente en la bóveda digital.");
        location.reload();
    }
}
