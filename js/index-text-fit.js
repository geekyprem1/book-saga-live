(() => {
  // The page builder positions text boxes independently of the content below them.
  const scopes = document.querySelectorAll('.cvt-1568371626-box .te-scope');
  const fittedBlocks = new Set();
  let frame;

  function fits(scope) {
    return scope.scrollHeight <= scope.clientHeight + 1 &&
      scope.scrollWidth <= scope.clientWidth + 1;
  }

  function fitCopy() {
    for (const block of fittedBlocks) block.style.removeProperty('zoom');
    fittedBlocks.clear();

    for (const scope of scopes) {
      if (!scope.clientWidth || !scope.clientHeight || fits(scope)) continue;
      const blocks = Array.from(scope.children);
      if (!blocks.length) continue;

      let lower = 0.5;
      let upper = 1;
      for (let pass = 0; pass < 8; pass++) {
        const scale = (lower + upper) / 2;
        for (const block of blocks) block.style.zoom = scale;
        if (fits(scope)) lower = scale;
        else upper = scale;
      }

      for (const block of blocks) {
        block.style.zoom = lower;
        fittedBlocks.add(block);
      }
    }
  }

  function scheduleFit() {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(fitCopy);
  }

  scheduleFit();
  window.addEventListener('resize', scheduleFit, { passive: true });
  document.fonts.ready.then(scheduleFit);
  document.fonts.addEventListener('loadingdone', scheduleFit);
})();
