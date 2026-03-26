// --- 1. TAB NAVIGATION ---
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.header-nav a').forEach(el => el.classList.remove('active'));
    
    document.getElementById('view-' + tabId).classList.add('active');
    document.getElementById('tab-' + tabId).classList.add('active');
}

// --- 2. INTERACTIVE TREE (COLLAPSE/EXPAND & PAN/ZOOM) ---
document.addEventListener('DOMContentLoaded', () => {
    const treeContainer = document.getElementById('family-tree-container-div');
    if(treeContainer) {
        // Parse tree nodes to add toggle buttons and structure
        const nodes = treeContainer.querySelectorAll('.tree-node');
        
        nodes.forEach(node => {
            // Find direct child nodes
            const children = Array.from(node.children).filter(child => child.classList.contains('tree-node'));
            
            if(children.length > 0) {
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

        treeContainer.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.pageX - treeContainer.offsetLeft;
            startY = e.pageY - treeContainer.offsetTop;
            scrollLeft = treeContainer.scrollLeft;
            scrollTop = treeContainer.scrollTop;
        });
        
        treeContainer.addEventListener('mouseleave', () => { isDragging = false; });
        treeContainer.addEventListener('mouseup', () => { isDragging = false; });
        
        treeContainer.addEventListener('mousemove', (e) => {
            if(!isDragging) return;
            e.preventDefault();
            const x = e.pageX - treeContainer.offsetLeft;
            const y = e.pageY - treeContainer.offsetTop;
            const walkX = (x - startX) * 1.5; // Drag speed
            const walkY = (y - startY) * 1.5;
            treeContainer.scrollLeft = scrollLeft - walkX;
            treeContainer.scrollTop = scrollTop - walkY;
        });
    }
});

// --- 3. SUPABASE MOCK FUNCTIONS ---
async function loginWithSupabase() {
    const email = document.getElementById('loginEmail').value;
    const pass = document.getElementById('loginPass').value;
    
    if(!email || !pass) {
        alert("Por favor ingresa credenciales."); return;
    }
    
    // Integración real con auth de Supabase
    try {
        // We assume supabase is available globally or via module
        // For simplicity in this refactor, we check both
        const supabaseClient = window.supabase;
        if(supabaseClient) {
            const { data, error } = await supabaseClient.auth.signInWithPassword({
                email: email, password: pass
            });
            if(error) throw error;
            alert("Sesión iniciada correctamente.");
            document.getElementById('loginModal').style.display='none';
            // Cambiar UI de usuario
            document.querySelector('.user-menu').innerHTML = `<span style="font-weight:bold; color:var(--text-main);">👨‍💻 ${email}</span> <a href="#" onclick="supabase.auth.signOut(); location.reload();" style="color:red; font-size:0.9rem; text-decoration:none;">Salir</a>`;
        } else {
            console.warn("Supabase client no definido globalmente aún. Mock mode.");
            alert("Simulación de sesión iniciada para " + email);
            document.getElementById('loginModal').style.display='none';
        }
    } catch(e) {
        alert("Error de inicio de sesión: " + e.message);
    }
}

async function searchSupabase() {
    const btn = document.querySelector('#view-buscar .btn');
    btn.innerHTML = "Buscando...";
    const resDiv = document.getElementById('search-results');
    resDiv.style.display = "block";
    
    const n = document.getElementById('s_nombres').value;
    const a = document.getElementById('s_apellidos').value;
    
    setTimeout(() => {
        const list = document.getElementById('results-list');
        list.innerHTML = `
            <li style="padding:15px; border-bottom:1px solid #eee;">
                <strong style="color:var(--fs-blue); font-size:1.1rem;">${n || 'Francisco'} ${a || 'García'}</strong><br>
                <span style="color:var(--text-muted); font-size:0.9rem;">Nacimiento: aprox 1650, Nuevo Reino de León • Defunción: Saltillo, Coahuila</span><br>
                <a href="#" style="font-size:0.85rem; font-weight:bold; margin-top:5px; display:inline-block;">Ver documento original →</a>
            </li>
            <li style="padding:15px; border-bottom:1px solid #eee;">
                <strong style="color:var(--fs-blue); font-size:1.1rem;">${n || 'María'} ${a || 'Guajardo'}</strong><br>
                <span style="color:var(--text-muted); font-size:0.9rem;">Nacimiento: aprox 1768 • Cónyuge: Jose Antonio Garcia</span><br>
                <a href="#" style="font-size:0.85rem; font-weight:bold; margin-top:5px; display:inline-block;">Ver documento original →</a>
            </li>
        `;
        btn.innerHTML = "Buscar Registros";
    }, 800);
}

function uploadToSupabase(e) {
    const file = e.target.files[0];
    if(file) {
        alert("Preparando para subir '" + file.name + "' a Supabase Storage (bucket: memories)...\n\nLa carga real requiere que el usuario esté autenticado y la tabla/bucket creados.");
        // Fake UI update
        const grid = document.getElementById('memories-grid');
        grid.innerHTML += `
        <div class="gallery-card">
            <div style="height:150px; background:#e0f7fa; border-radius:4px; margin-bottom:15px; display:flex; align-items:center; justify-content:center; color:#006064; font-weight:bold;">[Nuevo Archivo]</div>
            <h3>${file.name}</h3>
            <p>Agregado justo ahora</p>
        </div>`;
    }
}

// Export functions to window to keep onclick handlers working
window.showTab = showTab;
window.loginWithSupabase = loginWithSupabase;
window.searchSupabase = searchSupabase;
window.uploadToSupabase = uploadToSupabase;
