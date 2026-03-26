// js/tree.js - Dynamic Lineage Engine for Sefarad MX
let genealogicalData = null;

async function loadGenealogicalData() {
    if (genealogicalData) return genealogicalData;
    try {
        const response = await fetch('../supabase_data.json');
        genealogicalData = await response.json();
        return genealogicalData;
    } catch (e) {
        console.error("Error loading genealogical data:", e);
        return null;
    }
}

async function buildDynamicTree(rootIndiId) {
    const data = await loadGenealogicalData();
    if (!data || !data.individuals[rootIndiId]) {
        document.getElementById('tree-content').innerHTML = "<p>Expediente genealógico no vinculado.</p>";
        return;
    }

    const container = document.getElementById('tree-content');
    container.innerHTML = ""; // Clear loader

    const treeRoot = document.createElement('div');
    treeRoot.className = 'tree-view';
    
    // Build Descendancy (or Ancestry, here we do a simple recursive descent from the person)
    renderPerson(rootIndiId, treeRoot, data, 0);
    container.appendChild(treeRoot);
}

function renderPerson(indiId, container, data, level) {
    const person = data.individuals[indiId];
    if (!person) return;

    const node = document.createElement('div');
    node.className = 'tree-node-dynamic';
    node.style.marginLeft = (level * 20) + "px";
    
    const info = document.createElement('div');
    info.className = 'node-info';
    
    const name = document.createElement('strong');
    name.textContent = person.full_name;
    
    const meta = document.createElement('span');
    meta.className = 'node-meta';
    const dates = [person.birth_date, person.death_date].filter(d => d).join(' - ');
    meta.textContent = dates ? ` (${dates})` : "";
    
    info.appendChild(name);
    info.appendChild(meta);
    node.appendChild(info);
    container.appendChild(node);

    // Find children through families
    // Note: This requires scanning families where this person is HUSB or WIFE
    for (const famId in data.families) {
        const fam = data.families[famId];
        if (fam.husb === indiId || fam.wife === indiId) {
            fam.chil.forEach(childId => {
                renderPerson(childId, container, data, level + 1);
            });
        }
    }
}

// Initialize when called from profile
window.initDynamicTree = buildDynamicTree;
