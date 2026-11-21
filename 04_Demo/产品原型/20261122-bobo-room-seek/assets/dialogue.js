/* 2026-11-22 房间寻踪 · 对白层入口骨架（CMQ-Demo · HTML制作）
 * 只预留可关、可跳过的低密度对白层。默认关闭。
 * 不替代打招呼、看窗、寻踪、盖章、退出等动作主路径，不暂停自动收尾。
 * 词句由互动玩法通过 window.MianyuDialogue.showLine 接入；本文件不写入对白正文。
 * 不调用 getUserMedia，不加对外口径。
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'mianyu-dialogue-on';
  var layer = document.getElementById('dialogueLayer');
  var lineEl = document.getElementById('dialogueLine');
  var btnSkip = document.getElementById('btnDialogueSkip');
  var btnOff = document.getElementById('btnDialogueOff');
  var toggles = [
    document.getElementById('btnDialogueToggle'),
    document.getElementById('btnDialogueToggleDock')
  ];

  var enabled = false;
  var currentLine = '';
  var hooks = {
    onEnable: null,
    onDisable: null,
    onSkip: null,
    onClose: null
  };

  function readPref() {
    try {
      return sessionStorage.getItem(STORAGE_KEY) === '1';
    } catch (e) {
      return false;
    }
  }

  function writePref(on) {
    try {
      sessionStorage.setItem(STORAGE_KEY, on ? '1' : '0');
    } catch (e) {}
  }

  function syncToggles() {
    toggles.forEach(function (btn) {
      if (!btn) return;
      btn.setAttribute('aria-pressed', enabled ? 'true' : 'false');
      btn.textContent = enabled ? '关闭对白' : '打开对白';
    });
  }

  function syncLayer() {
    if (!layer) return;
    var show = enabled && !!currentLine;
    layer.hidden = !show;
    if (lineEl) lineEl.textContent = currentLine || '';
  }

  function setEnabled(on, source) {
    var next = !!on;
    var was = enabled;
    enabled = next;
    writePref(enabled);
    if (!enabled) currentLine = '';
    syncToggles();
    syncLayer();
    if (enabled && !was && typeof hooks.onEnable === 'function') hooks.onEnable(source || 'toggle');
    if (!enabled && was && typeof hooks.onDisable === 'function') hooks.onDisable(source || 'toggle');
    if (!enabled && was && source === 'close' && typeof hooks.onClose === 'function') hooks.onClose();
  }

  function skip() {
    currentLine = '';
    syncLayer();
    if (typeof hooks.onSkip === 'function') hooks.onSkip();
  }

  function showLine(text) {
    if (!enabled) return false;
    currentLine = text ? String(text) : '';
    syncLayer();
    return !!currentLine;
  }

  function clearLine() {
    currentLine = '';
    syncLayer();
  }

  window.MianyuDialogue = {
    isEnabled: function () { return enabled; },
    setEnabled: function (on) { setEnabled(on, 'api'); },
    showLine: showLine,
    clearLine: clearLine,
    skip: skip,
    setHooks: function (next) {
      if (!next) return;
      if ('onEnable' in next) hooks.onEnable = next.onEnable;
      if ('onDisable' in next) hooks.onDisable = next.onDisable;
      if ('onSkip' in next) hooks.onSkip = next.onSkip;
      if ('onClose' in next) hooks.onClose = next.onClose;
    }
  };

  if (btnSkip) {
    btnSkip.addEventListener('click', function (e) {
      e.stopPropagation();
      skip();
    });
  }
  if (btnOff) {
    btnOff.addEventListener('click', function (e) {
      e.stopPropagation();
      setEnabled(false, 'close');
    });
  }
  toggles.forEach(function (btn) {
    if (!btn) return;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      setEnabled(!enabled, 'toggle');
    });
  });

  enabled = readPref();
  syncToggles();
  syncLayer();
})();
