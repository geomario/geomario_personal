// Small progressive enhancements; every page works without them.
// - the light/dark theme switch (a saved choice is applied by an inline script in <head>)
// - the focus-area filter on the Projects page
// - a soft light that follows the mouse

document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initFocusFilter();
  initPointerGlow();
});

function initThemeToggle() {
  const button = document.querySelector(".theme-toggle");
  if (!button) return;
  const root = document.documentElement;
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)");
  const current = () => root.dataset.theme || (systemDark.matches ? "dark" : "light");

  function sync() {
    const theme = current();
    const label = theme === "dark" ? "Switch to light theme" : "Switch to dark theme";
    button.dataset.current = theme;
    button.setAttribute("aria-label", label);
    button.title = label;
  }

  button.addEventListener("click", () => {
    const next = current() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try {
      localStorage.setItem("theme", next);
    } catch {
      // Storage can be blocked (private mode); the switch still works for this page.
    }
    sync();
  });
  systemDark.addEventListener("change", sync);
  sync();
  button.hidden = false;
}

function initFocusFilter() {
  const chips = document.querySelectorAll("#focus .chip");
  const cards = document.querySelectorAll("#projects-panel .project");
  const emptyNote = document.getElementById("projects-empty");
  const countEl = document.getElementById("project-count");
  if (!chips.length || !cards.length) return;

  const total = cards.length;
  const allLabel = countEl ? countEl.textContent : "";
  let activeFilter = null;

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const tag = chip.dataset.filter;
      activeFilter = activeFilter === tag ? null : tag;

      chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.filter === activeFilter)));

      let visible = 0;
      cards.forEach((card) => {
        const matches = !activeFilter || card.dataset.tag === activeFilter;
        card.hidden = !matches;
        if (matches) visible += 1;
      });

      if (emptyNote) emptyNote.hidden = visible !== 0;
      if (countEl) countEl.textContent = activeFilter ? `${visible} of ${total}` : allLabel;
    });
  });
}

function initPointerGlow() {
  const glow = document.querySelector(".glow");
  const finePointer = window.matchMedia("(pointer: fine)").matches;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!glow || !finePointer || reducedMotion) return;

  let pending = 0;
  window.addEventListener(
    "pointermove",
    (event) => {
      if (pending) return;
      pending = requestAnimationFrame(() => {
        glow.style.setProperty("--gx", `${event.clientX}px`);
        glow.style.setProperty("--gy", `${event.clientY}px`);
        glow.classList.add("on");
        pending = 0;
      });
    },
    { passive: true },
  );
}
