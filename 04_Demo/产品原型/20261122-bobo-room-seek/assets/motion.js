/* 2026-11-22 房间寻踪 · 动效衔接（CMQ-Demo · 动效）
 * 不改玩法状态机。只补：窗边挪步保持、减少动态效果时的静止态、结束压暗窗边光。
 * 互动玩法已声明的 class / data 挂钩保持可用。
 */
(function () {
  'use strict';

  var actor = document.getElementById('actor');
  var motion = document.getElementById('actorMotion');
  var scene = document.getElementById('scene');
  var reduced = false;
  try {
    reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  } catch (e) {
    reduced = false;
  }

  function hasLook() {
    return !!(motion && (motion.classList.contains('is-look-window') || motion.classList.contains('is-look-lamp')));
  }

  function applyStep() {
    if (!actor) return;
    if (actor.hidden || actor.classList.contains('is-hidden')) return;
    actor.classList.add('is-window-step');
    /* placeActor 写的是行内 left，必须改行内才能真正挪步并停下 */
    actor.style.left = '38%';
    if (motion) motion.classList.remove('is-ear-hold');
  }
  function clearStep() {
    if (actor) {
      actor.classList.remove('is-window-step');
      if (actor.style.left === '38%') actor.style.left = '45%';
    }
    if (motion) motion.classList.remove('is-ear-hold');
  }

  function holdEar() {
    if (!motion) return;
    motion.classList.add('is-ear-hold');
    if (motion._earHoldTimer) clearTimeout(motion._earHoldTimer);
    motion._earHoldTimer = setTimeout(function () {
      motion.classList.remove('is-ear-hold');
    }, 1800);
  }

  function dimWindow(on) {
    if (!scene) return;
    scene.classList.toggle('is-window-dim', !!on);
  }

  function onMotionClass() {
    if (!motion || !actor) return;
    var approaching = motion.classList.contains('anim-approach') && !hasLook();
    if (approaching) {
      /* 先看窗，再挪步并停下 */
      if (motion._stepTimer) clearTimeout(motion._stepTimer);
      motion._stepTimer = setTimeout(function () {
        if (!motion.classList.contains('anim-approach') && !actor.classList.contains('is-window-step')) {
          /* 动画类可能已结束，仍补上停步 */
        }
        if (actor.classList.contains('is-hidden') || actor.hidden) return;
        applyStep();
      }, reduced ? 0 : 520);
    }
    if (motion.classList.contains('anim-confirm') && reduced) holdEar();
    if (motion.classList.contains('anim-confirm') ||
        motion.classList.contains('anim-approach') ||
        motion.classList.contains('anim-prop') ||
        motion.classList.contains('anim-night') ||
        motion.classList.contains('anim-guang') ||
        motion.classList.contains('anim-tremble') ||
        motion.classList.contains('anim-leave')) {
      stopSpeakEar();
    }
    if (motion.classList.contains('anim-night') || motion.classList.contains('anim-guang')) {
      dimWindow(true);
    }
    if (motion.classList.contains('anim-leave') || (actor && actor.classList.contains('is-hidden'))) {
      clearStep();
    }
  }

  if (motion && typeof MutationObserver === 'function') {
    new MutationObserver(onMotionClass).observe(motion, { attributes: true, attributeFilter: ['class'] });
  }
  if (actor && typeof MutationObserver === 'function') {
    new MutationObserver(function () {
      if (actor.hidden || actor.classList.contains('is-hidden')) clearStep();
    }).observe(actor, { attributes: true, attributeFilter: ['class', 'hidden'] });
  }

  var greet = document.getElementById('btnGreet');
  if (greet) {
    greet.addEventListener('click', function () {
      if (reduced) holdEar();
    });
  }
  var hotWindow = document.getElementById('hotWindow');
  if (hotWindow) {
    hotWindow.addEventListener('click', function () {
      if (!actor || actor.hidden) return;
      setTimeout(function () {
        if (actor.hidden || actor.classList.contains('is-hidden')) return;
        if (motion && hasLook()) return;
        applyStep();
      }, reduced ? 0 : 520);
    });
  }

  var btnEnd = document.getElementById('btnEnd');
  if (btnEnd) {
    btnEnd.addEventListener('click', function () {
      dimWindow(true);
    });
  }
  var backHome = document.getElementById('btnBackHome');
  if (backHome) {
    backHome.addEventListener('click', function () {
      dimWindow(false);
      clearStep();
    });
  }
  var startBtn = document.getElementById('btnStartTonight');
  if (startBtn) {
    startBtn.addEventListener('click', function () {
      dimWindow(false);
      clearStep();
    });
  }

  function actionBusy() {
    if (!actor || actor.hidden || actor.classList.contains('is-hidden')) return true;
    if (!motion) return true;
    var names = ['anim-confirm', 'anim-approach', 'anim-prop', 'anim-night', 'anim-guang', 'anim-tremble', 'anim-leave', 'anim-return'];
    var i;
    for (i = 0; i < names.length; i++) {
      if (motion.classList.contains(names[i])) return true;
    }
    return false;
  }

  function stopSpeakEar() {
    if (!motion) return;
    motion.classList.remove('is-dialogue-ear');
    if (motion._dlgTimer) {
      clearTimeout(motion._dlgTimer);
      motion._dlgTimer = null;
    }
  }

  /* 对白开口轻倾：只跟可见对白层走，不调用 setHooks，以免盖掉玩法的钩子。
   * 跳过或关闭会隐藏图层，动作立即停。不出声的打招呼/看窗/盖章优先。 */
  function speakEar() {
    if (!motion || actionBusy()) return;
    motion.classList.remove('is-dialogue-ear');
    void motion.offsetWidth;
    motion.classList.add('is-dialogue-ear');
    if (motion._dlgTimer) clearTimeout(motion._dlgTimer);
    motion._dlgTimer = setTimeout(function () {
      motion.classList.remove('is-dialogue-ear');
      motion._dlgTimer = null;
    }, reduced ? 900 : 1500);
  }

  var dialogueLayer = document.getElementById('dialogueLayer');
  var dialogueLine = document.getElementById('dialogueLine');
  if (dialogueLayer && typeof MutationObserver === 'function') {
    new MutationObserver(function () {
      if (dialogueLayer.hidden) stopSpeakEar();
      else speakEar();
    }).observe(dialogueLayer, { attributes: true, attributeFilter: ['hidden'] });
  }
  if (dialogueLine && dialogueLayer && typeof MutationObserver === 'function') {
    new MutationObserver(function () {
      if (dialogueLayer.hidden) return;
      if (!String(dialogueLine.textContent || '').replace(/^\s+|\s+$/g, '')) return;
      speakEar();
    }).observe(dialogueLine, { childList: true, characterData: true, subtree: true });
  }

  window.MianyuMotion = {
    stepToWindow: function () {
      if (actor) applyStep();
    },
    holdEar: holdEar,
    speakEar: speakEar,
    stopSpeakEar: stopSpeakEar,
    dimWindow: dimWindow,
    clear: function () {
      dimWindow(false);
      clearStep();
      stopSpeakEar();
    },
    reduced: reduced
  };
})();
