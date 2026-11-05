/* ============================================================
   Moteur de navigation + coloration syntaxique — slides SpaceData
   100% vanilla JS, aucune dépendance externe (fonctionne hors-ligne)
   ============================================================ */
(function () {
  "use strict";

  var deck = document.getElementById("deck");
  var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  var counter = document.getElementById("counter");
  var fill = document.getElementById("progressFill");
  var total = slides.length;

  function currentIndex() {
    var idx = 0, min = Infinity, top = deck.scrollTop;
    slides.forEach(function (s, i) {
      var d = Math.abs(s.offsetTop - top);
      if (d < min) { min = d; idx = i; }
    });
    return idx;
  }

  function update() {
    var idx = currentIndex();
    if (counter) counter.textContent = (idx + 1) + " / " + total;
    if (fill) fill.style.width = ((idx + 1) / total * 100) + "%";
    if (history.replaceState) history.replaceState(null, "", "#" + (idx + 1));
  }

  function goTo(idx) {
    idx = Math.max(0, Math.min(total - 1, idx));
    slides[idx].scrollIntoView({ behavior: "smooth", block: "start" });
  }

  var scrollTimer = null;
  deck.addEventListener("scroll", function () {
    if (scrollTimer) window.cancelAnimationFrame(scrollTimer);
    scrollTimer = window.requestAnimationFrame(update);
  }, { passive: true });

  window.addEventListener("keydown", function (e) {
    var idx = currentIndex();
    if (["ArrowDown", "ArrowRight", "PageDown", " "].indexOf(e.key) !== -1) {
      e.preventDefault(); goTo(idx + 1);
    } else if (["ArrowUp", "ArrowLeft", "PageUp"].indexOf(e.key) !== -1) {
      e.preventDefault(); goTo(idx - 1);
    } else if (e.key === "Home") {
      e.preventDefault(); goTo(0);
    } else if (e.key === "End") {
      e.preventDefault(); goTo(total - 1);
    } else if (e.key === "f" || e.key === "F") {
      toggleFullscreen();
    }
  });

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      (document.documentElement.requestFullscreen || function () {}).call(document.documentElement);
    } else {
      (document.exitFullscreen || function () {}).call(document);
    }
  }

  var prevBtn = document.getElementById("prevBtn");
  var nextBtn = document.getElementById("nextBtn");
  if (prevBtn) prevBtn.addEventListener("click", function () { goTo(currentIndex() - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { goTo(currentIndex() + 1); });

  var initialHash = parseInt((location.hash || "").replace("#", ""), 10);
  if (!isNaN(initialHash) && initialHash >= 1 && initialHash <= total) {
    window.requestAnimationFrame(function () { goTo(initialHash - 1); });
  }
  update();

  /* ---------------- Coloration syntaxique (mini, sans dépendance) ---------------- */
  var KEYWORDS = {
    python: ["import", "from", "as", "def", "return", "if", "elif", "else", "for", "in",
      "while", "try", "except", "finally", "with", "class", "pass", "None", "True", "False",
      "and", "or", "not", "is", "lambda", "yield", "raise", "global"],
    sql: ["SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY", "HAVING", "JOIN", "LEFT JOIN",
      "INNER JOIN", "ON", "AS", "COUNT", "AVG", "SUM", "MIN", "MAX", "LIMIT", "INSERT INTO",
      "VALUES", "CREATE TABLE", "AND", "OR", "NOT", "NULL", "DESC", "ASC", "DISTINCT"],
    bash: ["cd", "source", "pip", "pip3", "python3", "uvicorn", "export", "curl", "jupyter", "git"],
    json: ["true", "false", "null"]
  };

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function buildRules(lang) {
    var rules = [];
    if (lang === "python" || lang === "bash") rules.push({ type: "com", src: "#.*" });
    if (lang === "sql") rules.push({ type: "com", src: "--.*" });
    if (lang === "json") rules.push({ type: "key", src: '"(?:[^"\\\\]|\\\\.)*"(?=\\s*:)' });
    rules.push({ type: "str", src: "\"(?:[^\"\\\\]|\\\\.)*\"|'(?:[^'\\\\]|\\\\.)*'" });
    rules.push({ type: "num", src: "\\b\\d+\\.?\\d*\\b" });
    var kw = KEYWORDS[lang];
    if (kw && kw.length) {
      rules.push({ type: "kw", src: "\\b(?:" + kw.join("|") + ")\\b" });
    }
    if (lang === "python") rules.push({ type: "fn", src: "\\b[a-zA-Z_][a-zA-Z0-9_]*(?=\\()" });
    return rules;
  }

  function highlight(code, lang) {
    var rules = buildRules(lang);
    var combined = new RegExp(rules.map(function (r) { return "(" + r.src + ")"; }).join("|"), "gm");
    var result = "", lastIndex = 0, m;
    while ((m = combined.exec(code)) !== null) {
      result += escapeHtml(code.slice(lastIndex, m.index));
      for (var i = 0; i < rules.length; i++) {
        if (m[i + 1] !== undefined) {
          result += '<span class="tok-' + rules[i].type + '">' + escapeHtml(m[i + 1]) + "</span>";
          break;
        }
      }
      lastIndex = combined.lastIndex;
      if (m.index === combined.lastIndex) combined.lastIndex++;
    }
    result += escapeHtml(code.slice(lastIndex));
    return result;
  }

  Array.prototype.slice.call(document.querySelectorAll("code[data-lang]")).forEach(function (el) {
    var lang = el.getAttribute("data-lang");
    el.innerHTML = highlight(el.textContent, lang);
  });

  /* ---------------- Mini-carte interactive (survol, clic, pan, zoom) ---------------- */
  Array.prototype.slice.call(document.querySelectorAll(".map-demo:not(.map-demo--static)")).forEach(function (container) {
    var svg = container.querySelector("svg");
    var group = container.querySelector(".map-group");
    var tooltip = container.querySelector(".map-tooltip");
    if (!svg || !group) return;

    var scale = 1, tx = 0, ty = 0, dragging = false, lastX = 0, lastY = 0;
    function applyTransform() {
      group.setAttribute("transform", "translate(" + tx + "," + ty + ") scale(" + scale + ")");
    }

    Array.prototype.slice.call(container.querySelectorAll(".city-dot")).forEach(function (dot) {
      dot.addEventListener("mouseenter", function () {
        if (!tooltip) return;
        tooltip.innerHTML = "<strong>" + dot.getAttribute("data-name") + "</strong><br>" + dot.getAttribute("data-info");
        tooltip.classList.add("is-visible");
      });
      dot.addEventListener("mousemove", function (e) {
        if (!tooltip) return;
        var rect = container.getBoundingClientRect();
        tooltip.style.left = (e.clientX - rect.left) + "px";
        tooltip.style.top = (e.clientY - rect.top) + "px";
      });
      dot.addEventListener("mouseleave", function () {
        if (tooltip) tooltip.classList.remove("is-visible");
      });
      dot.addEventListener("click", function () { dot.classList.toggle("is-selected"); });
    });

    svg.addEventListener("mousedown", function (e) {
      dragging = true; lastX = e.clientX; lastY = e.clientY; container.classList.add("dragging");
    });
    window.addEventListener("mousemove", function (e) {
      if (!dragging) return;
      tx += (e.clientX - lastX); ty += (e.clientY - lastY);
      lastX = e.clientX; lastY = e.clientY;
      applyTransform();
    });
    window.addEventListener("mouseup", function () {
      dragging = false; container.classList.remove("dragging");
    });

    var zoomIn = container.querySelector('[data-zoom="in"]');
    var zoomOut = container.querySelector('[data-zoom="out"]');
    var zoomReset = container.querySelector('[data-zoom="reset"]');
    if (zoomIn) zoomIn.addEventListener("click", function () { scale = Math.min(scale * 1.3, 4); applyTransform(); });
    if (zoomOut) zoomOut.addEventListener("click", function () { scale = Math.max(scale / 1.3, 0.6); applyTransform(); });
    if (zoomReset) zoomReset.addEventListener("click", function () { scale = 1; tx = 0; ty = 0; applyTransform(); });
  });
})();
