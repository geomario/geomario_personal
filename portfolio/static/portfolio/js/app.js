// Vanilla-JS equivalent of the React version's useState hooks.
// Two independent pieces of UI state, each mirrored with plain DOM
// attributes instead of a virtual DOM: the Projects/Writing tab, and
// the focus-area filter.

document.addEventListener("DOMContentLoaded", () => {
  initWorkTabs();
  initFocusFilter();
});

function initWorkTabs() {
  const tabs = document.querySelectorAll("#work-tabs .tab");
  const projectsPanel = document.getElementById("projects-panel");
  const writingPanel = document.getElementById("writing-panel");
  const focusSection = document.getElementById("focus");
  const countEl = document.getElementById("work-count");
  if (!tabs.length || !projectsPanel || !writingPanel || !countEl) return;

  const projectCount = projectsPanel.querySelectorAll(".project").length;
  const writingCount = writingPanel.querySelectorAll(".tile").length;

  function updateCount(tab) {
    if (tab === "projects") {
      const visible = projectsPanel.querySelectorAll(".project:not([hidden])").length;
      countEl.textContent = `${visible} / ${projectCount}`;
    } else {
      countEl.textContent = `${writingCount} posts`;
    }
  }

  function setTab(tab) {
    tabs.forEach((btn) => {
      const active = btn.dataset.tab === tab;
      btn.classList.toggle("active", active);
      btn.setAttribute("aria-selected", String(active));
      // Only the active tab is in the Tab order; arrow keys move between tabs.
      btn.tabIndex = active ? 0 : -1;
    });
    projectsPanel.hidden = tab !== "projects";
    writingPanel.hidden = tab !== "writing";
    if (focusSection) focusSection.hidden = tab !== "projects";
    updateCount(tab);
  }

  tabs.forEach((btn, i) => {
    btn.addEventListener("click", () => setTab(btn.dataset.tab));
    btn.addEventListener("keydown", (event) => {
      const keys = { ArrowRight: 1, ArrowLeft: -1, Home: -i, End: tabs.length - 1 - i };
      if (!(event.key in keys)) return;
      event.preventDefault();
      const next = tabs[(i + keys[event.key] + tabs.length) % tabs.length];
      setTab(next.dataset.tab);
      next.focus();
    });
  });
  setTab("projects");
}

function initFocusFilter() {
  const chips = document.querySelectorAll("#focus .chip");
  const projectsPanel = document.getElementById("projects-panel");
  const emptyNote = document.getElementById("projects-empty");
  const countEl = document.getElementById("work-count");
  if (!chips.length || !projectsPanel) return;

  const projectCount = projectsPanel.querySelectorAll(".project").length;
  let activeFilter = null;

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const tag = chip.dataset.filter;
      activeFilter = activeFilter === tag ? null : tag;

      chips.forEach((c) => {
        const on = c.dataset.filter === activeFilter;
        c.classList.toggle("active", on);
        c.setAttribute("aria-pressed", String(on));
      });

      let visible = 0;
      projectsPanel.querySelectorAll(".project").forEach((card) => {
        const matches = !activeFilter || card.dataset.tag === activeFilter;
        card.hidden = !matches;
        if (matches) visible += 1;
      });

      if (emptyNote) emptyNote.hidden = visible !== 0;
      if (countEl) countEl.textContent = `${visible} / ${projectCount}`;
    });
  });
}
