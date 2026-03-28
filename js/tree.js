// js/tree.js - Gramps-Style Pedigree Engine
let genealogicalData = null;
let profileMap = null;

async function loadData() {
    if (genealogicalData && profileMap) return;
    const [gRes, mRes] = await Promise.all([
        fetch('../supabase_data.json'),
        fetch('../profile_map.json')
    ]);
    genealogicalData = await gRes.json();
    profileMap = await mRes.json();
}

function normalize(s) {
    if (!s) return "";
    return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]/g, "");
}

async function buildDynamicTree(rootId) {
    await loadData();
    const container = document.getElementById('tree-content');
    container.innerHTML = "";
    container.className = "pedigree-container";

    const person = genealogicalData.individuals[rootId];
    if (!person) {
        container.innerHTML = "<p>Expediente genealógico no disponible.</p>";
        return;
    }

    const chart = document.createElement('div');
    chart.className = "pedigree-chart";
    
    // Current Person Node
    const rootNode = createNode(rootId, true);
    chart.appendChild(rootNode);

    // Render Ancestors (Simplified FamilySearch logic)
    const parents = findParents(rootId);
    if (parents.husb || parents.wife) {
        const ancestorsCol = document.createElement('div');
        ancestorsCol.style.display = "flex";
        ancestorsCol.style.flexDirection = "column";
        ancestorsCol.style.gap = "40px";
        
        if (parents.husb) ancestorsCol.appendChild(createNode(parents.husb));
        if (parents.wife) ancestorsCol.appendChild(createNode(parents.wife));
        
        chart.appendChild(ancestorsCol);
    }

    container.appendChild(chart);
    
    // Pan capability
    let isDown = false; let startX; let scrollLeft;
    container.addEventListener('mousedown', (e) => { isDown = true; startX = e.pageX - container.offsetLeft; scrollLeft = container.scrollLeft; });
    container.addEventListener('mouseleave', () => { isDown = false; });
    container.addEventListener('mouseup', () => { isDown = false; });
    container.addEventListener('mousemove', (e) => { if(!isDown) return; e.preventDefault(); const x = e.pageX - container.offsetLeft; const walk = (x - startX) * 2; container.scrollLeft = scrollLeft - walk; });
}

function createNode(indiId, isRoot = false) {
    const p = genealogicalData.individuals[indiId];
    if (!p) return document.createElement('div');

    const el = document.createElement('div');
    el.className = `pedigree-node ${isRoot ? 'root-node' : ''}`;
    
    const clean = normalize(p.full_name);
    const profileUrl = profileMap[clean] ? `../perfiles/${profileMap[clean]}` : null;

    el.innerHTML = `
        <div class="gender-indicator gender-${p.gender}"></div>
        <strong>${p.full_name}</strong>
        <span>${p.birth_date || '?'} — ${p.death_date || '?'}</span>
        ${profileUrl && !isRoot ? `<a href="${profileUrl}" class="pedigree-link">📜 Ver Acta</a>` : ''}
    `;
    return el;
}

function findParents(indiId) {
    for (const famId in genealogicalData.families) {
        const fam = genealogicalData.families[famId];
        if (fam.chil.includes(indiId)) {
            return { husb: fam.husb, wife: fam.wife };
        }
    }
    return { husb: null, wife: null };
}

window.initDynamicTree = buildDynamicTree;
