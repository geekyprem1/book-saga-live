/* BookSaga · OTO pages — checkout wiring + small UX helpers.
   Every CTA reads its destination from window.BS_CFG (set per page in <head>).
   One place to edit per page; no duplicated links in the markup. */
(function () {
  'use strict';

  var cfg = window.BS_CFG || {};
  var buy = (cfg.buy || '').trim();
  var no = (cfg.no || '').trim();

  function markPending(el) {
    el.setAttribute('href', '#');
    el.setAttribute('data-checkout-pending', '1');
    el.setAttribute('aria-disabled', 'true');
    el.addEventListener('click', function (e) {
      e.preventDefault();
      var n = document.getElementById('bs-checkout-notice');
      if (n) {
        n.hidden = false;
        n.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }

  document.querySelectorAll('[data-buy]').forEach(function (el) {
    if (buy) {
      el.setAttribute('href', buy);
      el.removeAttribute('aria-disabled');
    } else {
      markPending(el);
    }
  });

  document.querySelectorAll('[data-no]').forEach(function (el) {
    if (no) el.setAttribute('href', no);
  });

  /* Show the "checkout not configured yet" notice only when a buy URL is missing. */
  var notice = document.getElementById('bs-checkout-notice');
  if (notice && buy) notice.hidden = true;

  /* Mark the current step in the top progress rail. */
  var rail = document.querySelector('.bs-steps');
  if (rail && cfg.step) {
    var el = rail.querySelector('[data-step="' + cfg.step + '"]');
    if (el) el.classList.add('is-now');
  }

  /* Reveal-on-scroll. Fail-safe: content is only hidden once this script has
     run, and a timer un-hides everything shortly after load no matter what.
     If JS never executes, every section stays visible. */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var targets = document.querySelectorAll('[data-reveal]');
  if (targets.length) {
    var revealAll = function () {
      targets.forEach(function (t) { t.classList.add('is-in'); });
    };

    if (!reduce && 'IntersectionObserver' in window) {
      document.documentElement.classList.add('bs-reveal-on');
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

      targets.forEach(function (t) { io.observe(t); });
    }

    /* Whatever happens above, nothing stays hidden. */
    window.setTimeout(revealAll, 1800);
  }
})();
