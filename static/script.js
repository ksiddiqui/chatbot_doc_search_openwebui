/* =========  Drawer Content  ========= */
const CONTENT = {
    details: {
      title: 'Prototype Details',
      body: `
        <ul class="space-y-4 text-slate-300">
          <li><strong>Prototype&nbsp;Name:</strong> Multi-Agentic Document Search</li>
          <li><strong>Developer:</strong> Kashif Ali Siddiqui</li>
          <li><strong>Location:</strong> Islamabad, Pakistan</li>
          <li><strong>Dated:</strong> July 2025</li>
          <li>
            <strong>GitHub:</strong>
            <a class="text-pink-400 underline" href="https://github.com/ksiddiqui" target="_blank">
              https://github.com/ksiddiqui
            </a>
          </li>
          <li>
            <strong>LinkedIn:</strong>
            <a class="text-pink-400 underline" href="https://www.linkedin.com/in/ksiddiqui" target="_blank">
              https://www.linkedin.com/in/ksiddiqui
            </a>
          </li>
          <li>
            <strong>Email:</strong>
            <a class="text-pink-400 underline" href="mailto:kashif.ali.siddiqui@gmail.com">
              kashif.ali.siddiqui@gmail.com
            </a>
          </li>
        </ul>
      `
    },
    tech: {
      title: 'Tech Stack',
      body: `
        <ul class="space-y-3 text-slate-300 list-disc list-inside">
          <li><strong>Docling:</strong> document parsing & cleansing</li>
          <li><strong>LlamaIndex:</strong> indexing & retrieval layer</li>
          <li><strong>PGVector + PostgreSQL:</strong> vector storage</li>
          <li><strong>Ollama:</strong> local LLM hosting (embedding & generation)</li>
          <li><strong>Crew.AI:</strong> agentic framework & prompt orchestration</li>
          <li><strong>Arize Phoenix:</strong> prompt playground & tracing</li>
          <li><strong>RAGAs:</strong> LLMOps evaluation metrics</li>
          <li><strong>Open WebUI:</strong> chatbot interface</li>
        </ul>
        <p class="mt-6 text-sm text-slate-400">
          All components run locally for security and reproducibility.
        </p>
      `
    }
  };
  
  /* =========  DOM Helpers  ========= */
  const drawer   = document.getElementById('drawer');
  const titleEl  = document.getElementById('drawer-title');
  const bodyEl   = document.getElementById('drawer-content');
  const closeBtn = document.getElementById('close-drawer');
  
  function openDrawer(key) {
    const { title, body } = CONTENT[key];
    titleEl.textContent = title;
    bodyEl.innerHTML    = body;
    drawer.classList.remove('translate-x-full');
  }
  
  function closeDrawer() {
    drawer.classList.add('translate-x-full');
  }
  
  /* =========  Event Listeners  ========= */
  document.getElementById('btn-details').addEventListener('click', () => openDrawer('details'));
  document.getElementById('btn-tech').addEventListener('click',   () => openDrawer('tech'));
  closeBtn.addEventListener('click', closeDrawer);
  
  /* Close drawer on outside click */
  drawer.addEventListener('click', e => {
    if (e.target === drawer) closeDrawer();
  });