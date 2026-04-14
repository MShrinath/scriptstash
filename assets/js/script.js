const archiveData = [
    { year: '2023-2024', term: 'Even', subject: '2023-2024_Even', courseCode: '32708', _MID1: 'M1', _MID2: 'M2' },
    
    { year: '2023-2024', term: 'Odd', subject: '2023-2024_Odd', courseCode: '32708', _MID1: 'M1', _MID2: 'M2' },
    
    { year: '2023-2024', term: 'SummerTerm', subject: '2023-2024_SummerTerm', courseCode: '32708', _MID1: 'M1', _MID2: 'M2' },

    { year: '2024-2025', term: 'Even', subject: '2024-2025_Even', courseCode: '32708', _MID1: 'M1', _MID2: 'M2' },

    { year: '2024-2025', term: 'Odd', subject: '2024-2025_Odd', courseCode: '32708', _MID1: 'M1', _MID2: 'M2' },
    
    { year: '2025-2026', term: 'Even', subject: '2025-2026_Even', courseCode: '32708', _MID1: 'M1', _MID2: 'M2' },
    
    { year: '2025-2026', term: 'Odd', subject: '2025-2026_Odd', courseCode: '32708', _MID1: 'M1', _MID2: 'M2' }
];

const sidebar = document.getElementById("sidebar");
const content = document.getElementById("content");

function getYears() {
    return [...new Set(archiveData.map(d => d.year))];
}

function getTerms(year) {
    const terms = [...new Set(
        archiveData
        .filter(d => d.year === year)
        .map(d => d.term)
    )];

    const order = ["Odd", "Even", "SummerTerm"];

    return terms.sort((a, b) => order.indexOf(a) - order.indexOf(b));
}

function getSubjects(year, term) {
    return archiveData.filter(
        d => d.year === year && d.term === term
    );
}

function buildTree() {
    sidebar.innerHTML = "";

    getYears().forEach(year => {
        const yearContainer = document.createElement("div");

        const yearEl = createItem("▶ " + year);
        yearEl.classList.add("folder");

        const termsContainer = document.createElement("div");
        termsContainer.style.display = "none";
        termsContainer.style.marginLeft = "15px";

        yearEl.onclick = () => {
            const isOpen = termsContainer.style.display === "block";
            termsContainer.style.display = isOpen ? "none" : "block";
            yearEl.textContent = (isOpen ? "▶ " : "▼ ") + year;
        };

        getTerms(year).forEach(term => {
            const termEl = createItem("📁 " + term);
            termEl.onclick = (e) => {
                e.stopPropagation();
                showSubjects(year, term);
            };

            termsContainer.appendChild(termEl);
        });

        yearContainer.appendChild(yearEl);
        yearContainer.appendChild(termsContainer);
        sidebar.appendChild(yearContainer);
    });
}

function createItem(text) {
    const div = document.createElement("div");
    div.className = "tree-item";
    div.textContent = text;
    return div;
}

function showSubjects(year, term) {
    content.innerHTML = `<h2>${year} / ${term}</h2>`;

    getSubjects(year, term).forEach(s => {
        const div = document.createElement("div");
        div.className = "file";

        div.innerHTML = `
      <b>${s.subject}</b><br>
      <small>${s.courseCode}</small><br>
      ${
        s._MID1
          ? `<button onclick="openPDF('${year}','${term}','${s.subject}','_MID1')">Mid1</button>`
          : ""
      }
      ${
        s._MID2
          ? `<button onclick="openPDF('${year}','${term}','${s.subject}','_MID2')">Mid2</button>`
          : ""
      }
    `;

        content.appendChild(div);
    });
}

function openPDF(year, term, subject, midLabel) {
    const subjectKey = subject
        .replace(/\s+/g, '_')
        .toUpperCase();

    const filename = `${year}_${term}_${subjectKey}${midLabel}.pdf`;
    // const path = `assets/${year}/${term}/${filename}`;
    const path = `assets/pdf.pdf`;  // test

    document.getElementById("content").innerHTML = 
    `
    <iframe src="${path}" style="width:100%; height:89vh; border:none;"></iframe>
    `;
}

document.addEventListener("DOMContentLoaded", buildTree);