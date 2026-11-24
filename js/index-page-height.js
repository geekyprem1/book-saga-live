/* The page builder exports .main-page with a fixed canvas height that is taller
   than the real content, so the white page background shows through below the
   footer. Trim the canvas to the bottom of the last box, per viewport width. */
(() => {
  const section = document.querySelector('.page-section.main-page');
  if (!section) return;

  const MIN_HEIGHT = 400;
  let frame = 0;
  let applied = 0;

  function measure() {
    const origin = section.getBoundingClientRect().top + window.pageYOffset;
    let bottom = 0;

    for (const node of section.querySelectorAll('[id^="box"], .bs-founders-section')) {
      const style = getComputedStyle(node);
      if (style.display === 'none' || style.visibility === 'hidden' || style.position === 'fixed') continue;

      const rect = node.getBoundingClientRect();
      if (rect.width <= 0 && rect.height <= 0) continue;

      const edge = rect.bottom + window.pageYOffset - origin;
      if (edge > bottom) bottom = edge;
    }

    return bottom;
  }

  function apply() {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      const bottom = measure();
      if (!Number.isFinite(bottom) || bottom < MIN_HEIGHT) return;

      const height = Math.round(bottom);
      if (height === applied) return;

      section.style.height = height + 'px';
      applied = height;
    });
  }

  apply();
  window.addEventListener('load', apply);
  window.addEventListener('resize', apply, { passive: true });
  window.addEventListener('orientationchange', apply, { passive: true });
  document.addEventListener('load', apply, true);
  document.addEventListener('transitionend', apply, true);

  if (document.fonts) {
    document.fonts.ready.then(apply);
    document.fonts.addEventListener('loadingdone', apply);
  }
})();
