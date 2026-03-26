// js/tree.js - Advanced Visual Lineage Engine
let genealogicalData = null;
let profileMapping = {};

async function loadGenealogicalData() {
    if (genealogicalData) return genealogicalData;
    try {
        const response = await fetch('../supabase_data.json');
        genealogicalData = await response.json();
        
        // Build a simplified name-to-filename mapping for linking
        // This is a heuristic since we don't have a direct DB link for all
        // In a real DB this would be a column.
        return genealogicalData;
    } catch (e) {
        console.error("Error loading genealogical data:", e);
        return null;
    }
}

function normalize(s) {
    return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]/g, "");
}

async function buildDynamicTree(rootIndiId) {
    const data = await loadGenealogicalData();
    if (!data || !data.individuals[rootIndiId]) {
        document.getElementById('tree-content').innerHTML = "<p>Expediente genealógico no vinculado.</p>";
        return;
    }

    const container = document.getElementById('tree-content');
    container.innerHTML = ""; 
    container.className = "tree-container-pro";

    const treeRoot = document.createElement('div');
    treeRoot.className = 'tree-view-pro';
    
    renderLevel(rootIndiId, treeRoot, data, 0, 3); // Max 3 generations for clarity
    container.appendChild(treeRoot);
}

function renderLevel(indiId, container, data, level, maxLevel) {
    if (level > maxLevel) return;

    const person = data.individuals[indiId];
    if (!person) return;

    const row = document.createElement('div');
    row.className = 'tree-row';
    
    const node = document.createElement('div');
    node.className = 'tree-node-pro';
    
    // Heuristic link: check if we can find a profile for this person
    const cleanName = normalize(person.full_name);
    // In actual use, we'd have a mapping. For now, we link if it's the root or matches a known pattern.
    
    node.innerHTML = `
        <strong>${person.full_name}</strong>
        <span>${person.birth_date || '?'} — ${person.death_date || '?'}</span>
    `;

    // Add "Ver Expediente" if it's not the current one (placeholder logic)
    if (level > 0) {
        const link = document.createElement('a');
        link.href = "#";
        link.className = "record-link";
        link.innerHTML = "📜 Ver Acta";
        link.onclick = () => alert("Abriendo archivo digital para: " + person.full_name);
        node.appendChild(link);
    }

    row.appendChild(node);
    container.appendChild(row);

    // Find children
    const childrenIds = [];
    for (const famId in data.families) {
        const fam = data.families[famId];
        if (fam.husb === indiId || fam.wife === indiId) {
            fam.chil.forEach(cid => { if(!childrenIds.includes(cid)) childrenIds.push(cid); });
        }
    }

    if (childrenIds.length > 0) {
        const childrenContainer = document.createElement('div');
        childrenContainer.className = 'children-container';
        childrenContainer.style.display = "flex";
        childrenContainer.style.gap = "20px";
        
        childrenIds.forEach(cid => {
            const childCol = document.createElement('div');
            renderLevel(cid, childCol, data, level + 1, maxLevel);
            childrenContainer.appendChild(childCol);
        });
        container.appendChild(childrenContainer);
    }
}

window.initDynamicTree = buildDynamicTree;
