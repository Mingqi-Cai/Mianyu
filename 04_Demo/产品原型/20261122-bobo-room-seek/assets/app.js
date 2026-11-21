/* 眠语 Demo · 20261122 房间寻踪改版（互动玩法规则）
 * 工作目录：20261122-bobo-room-seek/work/。不改写 11-21 基线、recut-2146 或仓库。
 * 不调用 getUserMedia，不接麦克风，不做语音识别或监测宣称。
 * 方向传感器只在用户主动点「转动手机找」后请求。
 */
(function () {
  'use strict';

  var STATES = {
    Idle: 'Idle',
    InScreenPlay: 'InScreenPlay',
    Companion: 'Companion',
    Hidden: 'Hidden',
    Found: 'Found',
    SilentComm: 'SilentComm',
    Outro: 'Outro',
    Ended: 'Ended',
    SpaceDemo: 'SpaceDemo'
  };

  /* 可配置的短暂陪伴时间（毫秒）。页面不显示倒计时。 */
  var COMPANION_MS = 32000;
  var IDLE_RESUME_MS = 1400;
  var WINDOW_PLACE_X = 0.45;

  /* 房间寻踪起步参数，可调整。 */
  var SEEK_NEAR_DEG = 20;
  var SEEK_DWELL_MS = 350;
  var SEEK_HINT_MS = 10000;
  var SEEK_FOV_DEG = 72;
  var SEEK_YAW_SMOOTH = 0.28;
  /* 为 null 时随机选一个藏点，再换到相邻点一次。演示可写成 ['curtain','rack']，或在地址栏加 ?seekRoute=curtain,rack */
  var SEEK_FIXED_ROUTE = null;

  /* 四个可辨认角落：入口朝向标定在 0°（两角之间的墙面），藏点不出现在开场视野里。 */
  var SEEK_CORNERS = [
    { id: 'curtain', name: '窗帘边', yaw: 60, hint: '窗帘边好像有点动静' },
    { id: 'rack', name: '行李架旁', yaw: 150, hint: '行李架那边好像有点动静' },
    { id: 'bedfoot', name: '床尾', yaw: 240, hint: '床尾那边好像有点动静' },
    { id: 'nightstand', name: '床头柜', yaw: 330, hint: '床头柜那边好像有点动静' }
  ];

  var HIDE_SPOTS = [
    { id: 'window', x: 0.26, clue: '窗边好像有一点动静。' },
    { id: 'lamp', x: 0.74, clue: '暖光那边，好像安静了一点。' },
    { id: 'bag', x: 0.58, clue: '行李旁边，好像藏进去了。' }
  ];

  var ANIM_MS = {
    'anim-confirm': 2200,
    'anim-tremble': 800,
    'anim-approach': 2600,
    'anim-night': 3200,
    'anim-prop': 2600,
    'anim-ritual': 2800,
    'anim-settle': 1600,
    'anim-guang': 2800,
    'anim-chat': 1600,
    'anim-leave': 1600,
    'anim-return': 2000
  };

  var el = {
    phoneScale: document.getElementById('phoneScale'),
    screen: document.getElementById('screen'),
    stateTag: document.getElementById('stateTag'),
    viewSplash: document.getElementById('viewSplash'),
    viewHome: document.getElementById('viewHome'),
    viewPlay: document.getElementById('viewPlay'),
    viewEnd: document.getElementById('viewEnd'),
    scene: document.getElementById('scene'),
    sceneTouch: document.getElementById('sceneTouch'),
    actor: document.getElementById('actor'),
    actorMotion: document.getElementById('actorMotion'),
    insertA: document.getElementById('insertA'),
    insertB: document.getElementById('insertB'),
    palmGlow: document.getElementById('palmGlow'),
    sheet: document.getElementById('sheet'),
    modal: document.getElementById('modal'),
    modalCard: document.getElementById('modalCard'),
    btnEnd: document.getElementById('btnEnd'),
    btnStartTonight: document.getElementById('btnStartTonight'),
    btnBackHome: document.getElementById('btnBackHome'),
    tapRipple: document.getElementById('tapRipple'),
    roomDock: document.getElementById('roomDock'),
    dockCaption: document.getElementById('dockCaption'),
    btnGreet: document.getElementById('btnGreet'),
    btnSeek: document.getElementById('btnSeek'),
    seekLayer: document.getElementById('seekLayer'),
    seekPrompt: document.getElementById('seekPrompt'),
    seekRoom: document.getElementById('seekRoom'),
    seekPan: document.getElementById('seekPan'),
    seekTrail: document.getElementById('seekTrail'),
    btnSeekGyro: document.getElementById('btnSeekGyro'),
    btnFound: document.getElementById('btnFound'),
    btnRecall: document.getElementById('btnRecall'),
    btnSeekCancel: document.getElementById('btnSeekCancel'),
    stampLayer: document.getElementById('stampLayer'),
    stampTag: document.getElementById('stampTag'),
    btnStamp: document.getElementById('btnStamp'),
    btnStampCancel: document.getElementById('btnStampCancel'),
    btnStampWindow: document.getElementById('btnStampWindow'),
    btnStampLamp: document.getElementById('btnStampLamp')
  };

  var S = null;
  var timers = [];
  var animLock = false;
  var companionTimer = null;
  var companionLeft = COMPANION_MS;
  var companionStartedAt = 0;
  var companionRunning = false;
  var idleResumeTimer = null;
  var reducedMotion = false;
  var stayStampEl = null;
  var seekPeekEl = null;
  var seek = null;
  var seekPointer = null;

  try {
    reducedMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  } catch (e) {
    reducedMotion = false;
  }
  /* HeadlessChrome（--disable-gpu）下 anim-leave / anim-confirm 会卡住主线程；真机仍播离开窗边。 */
  var headlessMotionUnsafe = false;
  try {
    headlessMotionUnsafe = /HeadlessChrome/i.test(navigator.userAgent || '');
  } catch (e2) {
    headlessMotionUnsafe = false;
  }

  function later(fn, ms) {
    var id = setTimeout(fn, ms);
    timers.push(id);
    return id;
  }
  function clearTimers() {
    timers.forEach(function (id) { clearTimeout(id); });
    timers = [];
  }

  function freshSession() {
    return {
      screen: 'S1',
      mode: 'inscreen',
      placed: false,
      confirmedPlace: false,
      placeX: WINDOW_PLACE_X,
      hideId: null,
      hideX: 0.26,
      foundHow: null,
      ritualDone: false,
      replies: 0,
      insert: 'a',
      approached: false,
      typedUsed: false,
      lastInput: '',
      endedFrom: null,
      seekShell: false,
      stampChoice: null,
      stamped: null
    };
  }

  function labelOf() {
    var play = S && S.screen;
    if (!play || play === 'S1' || play === 'S0') return STATES.Idle;
    if (play === 'S11') return STATES.SpaceDemo;
    if (play === 'S10') return STATES.Ended;
    if (play === 'S3') return STATES.Companion;
    if (play === 'S4' || play === 'S5') return STATES.Hidden;
    if (play === 'S6') return STATES.Found;
    if (play === 'S8') return STATES.SilentComm;
    if (play === 'S9') return STATES.Outro;
    return STATES.InScreenPlay;
  }

  function setLabel() {
    if (el.stateTag) el.stateTag.textContent = labelOf();
  }

  function showView(name) {
    el.viewSplash.hidden = name !== 'splash';
    el.viewHome.hidden = name !== 'home';
    el.viewPlay.hidden = name !== 'play';
    el.viewEnd.hidden = name !== 'end';
    el.screen.classList.toggle('is-ended', name === 'end');
    syncRoomChrome();
  }

  function isSeekOpen() {
    return !!(el.seekLayer && !el.seekLayer.hidden);
  }
  function isStampOpen() {
    return !!(el.stampLayer && !el.stampLayer.hidden);
  }

  /* 寻踪时不要用 [hidden]{display:none} 收起正在播动效的角色：
     与 motion.css 叠加时会卡住合成（已在无界面 Chrome 复核）。改用可见性隐藏。 */
  function isActorAway() {
    return !!(el.actor && (el.actor.hidden || el.actor.classList.contains('is-seek-away')));
  }
  function hideActorForSeek() {
    if (!el.actor) return;
    el.actor.classList.add('is-seek-away');
    el.actor.classList.remove('is-found');
    el.actor.setAttribute('aria-hidden', 'true');
  }
  function showActorAfterSeek() {
    if (!el.actor) return;
    el.actor.classList.remove('is-seek-away', 'is-hidden');
    el.actor.removeAttribute('aria-hidden');
    el.actor.hidden = false;
  }

  function syncExitChrome() {
    var play = el.viewPlay && !el.viewPlay.hidden;
    var sheetHasExit = S && S.screen === 'S9';
    el.btnEnd.hidden = !play || sheetHasExit;
    el.screen.classList.toggle('sheet-low', play && sheetHasExit);
  }

  function syncRoomChrome() {
    var play = el.viewPlay && !el.viewPlay.hidden;
    var companion = play && S && S.screen === 'S3' && !isSeekOpen() && !isStampOpen();
    if (el.roomDock) el.roomDock.hidden = !companion;
    syncExitChrome();
  }

  function hideModal() {
    el.modal.hidden = true;
    el.modalCard.innerHTML = '';
  }

  function showModal(html) {
    pauseCompanion();
    el.modalCard.innerHTML = html;
    el.modal.hidden = false;
  }

  function placeActor(x, instant, opts) {
    opts = opts || {};
    var min = opts.hide ? 0.16 : 0.30;
    var max = opts.hide ? 0.78 : 0.72;
    x = Math.max(min, Math.min(max, x));
    if (instant) el.actor.style.transition = 'none';
    el.actor.style.left = (x * 100) + '%';
    if (instant) {
      void el.actor.offsetWidth;
      el.actor.style.transition = '';
    }
    return x;
  }

  function resetActorVisual() {
    el.actor.classList.remove('is-hidden', 'is-seek-away', 'is-found', 'is-ritual', 'is-look-window', 'is-look-lamp');
    el.actorMotion.classList.remove(
      'anim-confirm', 'anim-approach', 'anim-chat', 'anim-night',
      'anim-guang', 'anim-ritual', 'anim-tremble', 'anim-prop', 'anim-settle',
      'anim-leave', 'anim-return',
      'is-look-window', 'is-look-lamp'
    );
    if (el.insertA) el.insertA.classList.add('on');
    if (el.insertB) el.insertB.classList.remove('on');
    el.palmGlow.style.opacity = '';
    animLock = false;
    if (S) {
      S.insert = 'a';
      S.approached = false;
      S.ritualDone = false;
    }
  }

  function playAnim(name, then, force) {
    var decorative = (name === 'anim-settle');
    if (animLock && !force && !decorative) return false;
    if (reducedMotion || (headlessMotionUnsafe && name !== 'anim-settle' && name !== 'anim-return')) {
      if (!decorative) animLock = false;
      if (then) later(then, 0);
      return true;
    }
    if (!decorative) animLock = true;
    el.actorMotion.classList.remove(
      'anim-confirm', 'anim-approach', 'anim-chat', 'anim-night',
      'anim-guang', 'anim-ritual', 'anim-tremble', 'anim-prop', 'anim-settle',
      'anim-leave', 'anim-return'
    );
    void el.actorMotion.offsetWidth;
    el.actorMotion.classList.add(name);
    var ms = ANIM_MS[name] || 2000;
    later(function () {
      if (name !== 'anim-guang' && name !== 'anim-night') {
        el.actorMotion.classList.remove(name);
      }
      if (!decorative) animLock = false;
      if (then) then();
    }, ms);
    return true;
  }

  function clampTapX(clientX) {
    var r = el.scene.getBoundingClientRect();
    return (clientX - r.left) / r.width;
  }

  function distanceToActor(clientX, clientY) {
    var r = el.actor.getBoundingClientRect();
    var cx = r.left + r.width * 0.5;
    var cy = r.top + r.height * 0.55;
    var dx = clientX - cx, dy = clientY - cy;
    return Math.sqrt(dx * dx + dy * dy);
  }

  function isExploring() {
    if (!S) return false;
    var sc = S.screen;
    return sc === 'S4' || sc === 'S5' || sc === 'S6' || sc === 'S8' || sc === 'S9' || isSeekOpen() || isStampOpen();
  }

  function canAutoEnd() {
    if (!S || S.screen !== 'S3') return false;
    if (isSeekOpen() || isStampOpen()) return false;
    if (seek && seek.active) return false;
    if (el.modal && !el.modal.hidden) return false;
    var ae = document.activeElement;
    if (ae && (ae.id === 'sayInput' || ae.getAttribute('data-role') === 'say')) return false;
    return true;
  }

  function pauseCompanion() {
    if (idleResumeTimer) {
      clearTimeout(idleResumeTimer);
      idleResumeTimer = null;
    }
    if (!companionRunning) return;
    companionLeft -= Date.now() - companionStartedAt;
    if (companionLeft < 0) companionLeft = 0;
    clearTimeout(companionTimer);
    companionTimer = null;
    companionRunning = false;
  }

  function resumeCompanion() {
    if (companionRunning) return;
    if (!canAutoEnd()) return;
    if (companionLeft <= 0) {
      startOutro();
      return;
    }
    companionStartedAt = Date.now();
    companionRunning = true;
    companionTimer = setTimeout(function () {
      companionRunning = false;
      companionTimer = null;
      if (canAutoEnd()) startOutro();
    }, companionLeft);
  }

  function maybeResumeCompanion() {
    if (idleResumeTimer) {
      clearTimeout(idleResumeTimer);
      idleResumeTimer = null;
    }
    if (!canAutoEnd()) return;
    idleResumeTimer = setTimeout(function () {
      idleResumeTimer = null;
      resumeCompanion();
    }, IDLE_RESUME_MS);
  }

  function noteExplore() {
    pauseCompanion();
    maybeResumeCompanion();
  }

  function clearCompanion() {
    pauseCompanion();
    companionLeft = COMPANION_MS;
    companionStartedAt = 0;
  }

  function discardInput() {
    if (S) {
      S.lastInput = '';
      S.typedUsed = false;
    }
    var input = document.getElementById('sayInput');
    if (input) input.value = '';
  }

  /* ---------- angle / room helpers ---------- */

  function wrapDeg(a) {
    a = a % 360;
    if (a < 0) a += 360;
    return a;
  }
  function deltaDeg(a, b) {
    var d = wrapDeg(a - b);
    if (d > 180) d -= 360;
    return d;
  }
  function absDelta(a, b) {
    return Math.abs(deltaDeg(a, b));
  }
  function cornerById(id) {
    var i;
    for (i = 0; i < SEEK_CORNERS.length; i++) {
      if (SEEK_CORNERS[i].id === id) return SEEK_CORNERS[i];
    }
    return null;
  }
  function adjacentIds(id) {
    var ids = SEEK_CORNERS.map(function (c) { return c.id; });
    var i = ids.indexOf(id);
    if (i < 0) return [ids[0], ids[1]];
    return [ids[(i + ids.length - 1) % ids.length], ids[(i + 1) % ids.length]];
  }
  function readSeekRoute() {
    var fixed = SEEK_FIXED_ROUTE;
    try {
      var q = new URLSearchParams(window.location.search).get('seekRoute');
      if (q) {
        var parts = q.split(',').map(function (s) { return String(s || '').replace(/^\s+|\s+$/g, ''); });
        if (parts.length >= 2 && cornerById(parts[0]) && cornerById(parts[1]) && parts[0] !== parts[1]) {
          fixed = [parts[0], parts[1]];
        }
      }
    } catch (e) {}
    return fixed;
  }
  function pickHideSpots() {
    var route = readSeekRoute();
    var first;
    var second;
    var adj;
    if (route) {
      first = route[0];
      second = route[1];
      adj = adjacentIds(first);
      if (adj.indexOf(second) < 0) second = adj[1];
    } else {
      first = SEEK_CORNERS[Math.floor(Math.random() * SEEK_CORNERS.length)].id;
      adj = adjacentIds(first);
      second = adj[Math.floor(Math.random() * adj.length)];
    }
    return { a: first, b: second };
  }

  function setSeekPrompt(text) {
    if (el.seekPrompt) el.seekPrompt.textContent = text;
  }

  function syncSeekData() {
    if (!el.seekLayer) return;
    var phase = seek && seek.active ? seek.phase : '';
    el.seekLayer.setAttribute('data-phase', phase);
    el.seekLayer.setAttribute('data-hide-a', (seek && seek.hideA) || '');
    el.seekLayer.setAttribute('data-hide-b', (seek && seek.hideB) || '');
    el.seekLayer.setAttribute('data-yaw', seek ? String(Math.round(wrapDeg(seek.yaw) * 10) / 10) : '');
    el.seekLayer.setAttribute('data-found-ready', (seek && seek.foundReady) ? '1' : '0');
    el.seekLayer.setAttribute('data-escaped', (seek && seek.escaped) ? '1' : '0');
    if (el.btnFound) {
      if (seek && seek.foundReady) el.btnFound.removeAttribute('disabled');
      else el.btnFound.setAttribute('disabled', 'disabled');
    }
  }

  function freshSeekState() {
    return {
      active: false,
      phase: '',
      hideA: null,
      hideB: null,
      yaw: 0,
      targetYaw: 0,
      dwellId: null,
      dwellAt: 0,
      escaped: false,
      foundReady: false,
      hintShown: false,
      hintTimer: null,
      raf: 0,
      gyroOn: false,
      gyroHandler: null,
      gyroZero: null,
      keysOn: false,
      keyHandler: null,
      pointerOn: false
    };
  }

  function onSeekPeekClick(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    if (!seek || !seek.active) return;
    if (seekPointer && seekPointer.moved) return;
    if (!seek.escaped) return;
    if (seek.foundReady) confirmFound('peek');
  }
  function ensureSeekBg() {
    if (!el.seekPan) return null;
    var bg = el.seekPan.querySelector('.seek-bg');
    if (bg) return bg;
    bg = document.createElement('div');
    bg.className = 'seek-bg';
    bg.setAttribute('aria-hidden', 'true');
    var i;
    for (i = 0; i < 3; i++) {
      var slice = document.createElement('div');
      slice.className = 'seek-bg-slice';
      bg.appendChild(slice);
    }
    el.seekPan.insertBefore(bg, el.seekPan.firstChild);
    return bg;
  }
  function layoutSeekBg() {
    if (!seek || !el.seekRoom || !el.seekPan) return;
    var bg = ensureSeekBg();
    if (!bg) return;
    var roomW = el.seekRoom.clientWidth || 1;
    var stripW = (360 / SEEK_FOV_DEG) * roomW;
    bg.style.width = (stripW * 3) + 'px';
    bg.style.left = (roomW / 2 - stripW * 1.5 - (wrapDeg(seek.yaw) / 360) * stripW) + 'px';
    var slices = bg.querySelectorAll('.seek-bg-slice');
    var i;
    for (i = 0; i < slices.length; i++) {
      slices[i].style.width = stripW + 'px';
    }
  }

  function ensureSeekPeek() {
    if (seekPeekEl && seekPeekEl.parentNode) return seekPeekEl;
    var wrap = document.createElement('div');
    wrap.className = 'seek-peek';
    wrap.id = 'seekPeek';
    wrap.setAttribute('role', 'button');
    wrap.setAttribute('aria-label', '露出的牌耳');
    wrap.hidden = true;
    var img = document.createElement('img');
    img.src = 'assets/bobo-figure.png';
    img.alt = '';
    wrap.appendChild(img);
    wrap.addEventListener('click', onSeekPeekClick);
    if (el.seekPan) el.seekPan.appendChild(wrap);
    seekPeekEl = wrap;
    return wrap;
  }

  function placePeekAt(cornerId, mode) {
    var peek = ensureSeekPeek();
    var corner = cornerById(cornerId);
    if (!corner || !el.seekRoom) {
      peek.hidden = true;
      return;
    }
    var half = SEEK_FOV_DEG / 2;
    var d = deltaDeg(corner.yaw, seek.yaw);
    if (Math.abs(d) > half + 16) {
      peek.hidden = true;
      return;
    }
    var w = el.seekRoom.clientWidth || 1;
    var x = (0.5 + d / SEEK_FOV_DEG) * w;
    peek.hidden = false;
    peek.className = 'seek-peek' + (mode ? ' is-' + mode : '');
    peek.style.left = x + 'px';
  }

  function hidePeek() {
    if (seekPeekEl) {
      seekPeekEl.hidden = true;
      seekPeekEl.className = 'seek-peek';
    }
  }

  function clearTrailMarks() {
    if (!el.seekPan) return;
    var marks = el.seekPan.querySelectorAll('.seek-mark');
    var i;
    for (i = 0; i < marks.length; i++) {
      if (marks[i].parentNode) marks[i].parentNode.removeChild(marks[i]);
    }
    if (el.seekTrail) {
      el.seekTrail.innerHTML = '';
      el.seekTrail.className = 'seek-trail';
      el.seekTrail.removeAttribute('data-from');
      el.seekTrail.removeAttribute('data-to');
      el.seekTrail.removeAttribute('data-dir');
    }
  }

  function layoutTrail() {
    if (!seek || !seek.escaped || !el.seekRoom || !el.seekPan) return;
    var a = cornerById(seek.hideA);
    var b = cornerById(seek.hideB);
    if (!a || !b) return;
    var dir = deltaDeg(b.yaw, a.yaw);
    var sign = dir >= 0 ? 1 : -1;
    var span = Math.abs(dir);
    /* 轨迹落在两点之间，末端在下一处遮挡前收住。 */
    var startYaw = wrapDeg(a.yaw + sign * Math.min(18, span * 0.22));
    var endYaw = wrapDeg(b.yaw - sign * Math.min(16, span * 0.2));
    var n = reducedMotion ? 2 : 3;
    var marks = el.seekPan.querySelectorAll('.seek-mark');
    if (marks.length !== n) {
      clearTrailMarks();
      var i;
      for (i = 0; i < n; i++) {
        var m = document.createElement('span');
        m.className = 'seek-mark';
        m.setAttribute('data-i', String(i));
        m.setAttribute('aria-hidden', 'true');
        el.seekPan.appendChild(m);
      }
      marks = el.seekPan.querySelectorAll('.seek-mark');
    }
    var w = el.seekRoom.clientWidth || 1;
    var half = SEEK_FOV_DEG / 2;
    var j;
    for (j = 0; j < marks.length; j++) {
      var t = marks.length === 1 ? 0.5 : j / (marks.length - 1);
      var yaw = wrapDeg(startYaw + deltaDeg(endYaw, startYaw) * t);
      var d = deltaDeg(yaw, seek.yaw);
      var visible = Math.abs(d) <= half + 10;
      marks[j].style.left = (0.5 + d / SEEK_FOV_DEG) * w + 'px';
      marks[j].classList.toggle('is-on', visible && seek.marksOn);
      marks[j].classList.toggle('is-offscreen', !visible);
    }
    if (el.seekTrail) {
      el.seekTrail.setAttribute('data-from', seek.hideA);
      el.seekTrail.setAttribute('data-to', seek.hideB);
      el.seekTrail.setAttribute('data-dir', sign > 0 ? 'cw' : 'ccw');
      el.seekTrail.classList.add('is-on');
    }
  }

  function applySeekView() {
    if (!seek || !seek.active || !el.seekRoom || !el.seekPan) return;
    layoutSeekBg();
    var w = el.seekRoom.clientWidth || 1;
    var half = SEEK_FOV_DEG / 2;
    var nodes = el.seekPan.querySelectorAll('[data-corner]');
    var i;
    for (i = 0; i < nodes.length; i++) {
      var id = nodes[i].getAttribute('data-corner');
      var corner = cornerById(id);
      if (!corner) continue;
      var d = deltaDeg(corner.yaw, seek.yaw);
      var inView = Math.abs(d) <= half;
      nodes[i].classList.toggle('is-in-view', inView);
      nodes[i].classList.toggle('is-hide-a', id === seek.hideA);
      nodes[i].classList.toggle('is-hide-b', id === seek.hideB);
      if (inView) {
        nodes[i].removeAttribute('hidden');
        nodes[i].style.left = (0.5 + d / SEEK_FOV_DEG) * w + 'px';
      } else {
        nodes[i].setAttribute('hidden', 'hidden');
      }
    }
    if (seek.phase === 'hid' || (seek.phase === 'near' && !seek.escaped)) {
      hidePeek();
    } else if (seek.escaped && !seek.foundReady) {
      /* 旧藏点可回看弱线索；新藏点在靠近后露出牌耳。 */
      if (absDelta(seek.yaw, cornerById(seek.hideA).yaw) <= half) placePeekAt(seek.hideA, 'weak');
      else hidePeek();
    } else if (seek.foundReady) {
      placePeekAt(seek.hideB, reducedMotion ? 'static' : 'peek');
    }
    if (seek.escaped) layoutTrail();
    syncSeekData();
  }

  function inNear(id) {
    var c = cornerById(id);
    return !!(c && absDelta(seek.yaw, c.yaw) <= SEEK_NEAR_DEG);
  }
  function inView(id) {
    var c = cornerById(id);
    return !!(c && absDelta(seek.yaw, c.yaw) <= SEEK_FOV_DEG / 2);
  }

  function startHintTimer() {
    if (!seek || seek.hintTimer || seek.hintShown) return;
    seek.hintTimer = setTimeout(function () {
      seek.hintTimer = null;
      if (!seek || !seek.active || seek.phase === 'found') return;
      if (seek.hintShown) return;
      var next = cornerById(seek.hideB);
      if (!next) return;
      seek.hintShown = true;
      setSeekPrompt(next.hint + '。');
    }, SEEK_HINT_MS);
  }

  function clearHintTimer() {
    if (seek && seek.hintTimer) {
      clearTimeout(seek.hintTimer);
      seek.hintTimer = null;
    }
  }

  function triggerEscape() {
    if (!seek || !seek.active || seek.escaped) return;
    seek.phase = 'near';
    seek.escaped = true;
    seek.dwellId = null;
    seek.dwellAt = 0;
    placePeekAt(seek.hideA, 'peek');
    if (el.seekPan) el.seekPan.classList.add(reducedMotion ? 'is-static-escape' : 'is-slipping');
    var slipMs = reducedMotion ? 0 : 720;
    later(function () {
      if (!seek || !seek.active) return;
      seek.phase = 'follow';
      seek.marksOn = false;
      layoutTrail();
      /* 减少动态效果：两枚印记顺次淡入，静态探头；完成条件相同。 */
      var marks = el.seekPan ? el.seekPan.querySelectorAll('.seek-mark') : [];
      var delay = reducedMotion ? 160 : 80;
      var i;
      for (i = 0; i < marks.length; i++) {
        (function (node, step) {
          later(function () {
            if (!seek || !seek.active) return;
            seek.marksOn = true;
            node.classList.add('is-on');
          }, delay * (step + 1));
        })(marks[i], i);
      }
      later(function () {
        if (!seek || !seek.active) return;
        seek.marksOn = true;
        hidePeek();
        applySeekView();
      }, slipMs);
      startHintTimer();
      applySeekView();
    }, reducedMotion ? 80 : 420);
    applySeekView();
  }

  function updateFoundReady() {
    if (!seek || !seek.active || !seek.escaped) {
      if (seek) seek.foundReady = false;
      return;
    }
    seek.foundReady = inView(seek.hideB) || inNear(seek.hideB);
  }

  function checkSeekNear(now) {
    if (!seek || !seek.active) return;
    now = now || Date.now();
    if (!seek.escaped) {
      if (inNear(seek.hideA)) {
        if (seek.dwellId !== seek.hideA) {
          seek.dwellId = seek.hideA;
          seek.dwellAt = now;
        } else if (now - seek.dwellAt >= SEEK_DWELL_MS) {
          triggerEscape();
        }
      } else {
        seek.dwellId = null;
        seek.dwellAt = 0;
      }
    } else {
      updateFoundReady();
    }
  }

  function seekTick() {
    if (!seek || !seek.active) return;
    var diff = deltaDeg(seek.targetYaw, seek.yaw);
    if (Math.abs(diff) > 0.05) {
      seek.yaw = wrapDeg(seek.yaw + diff * SEEK_YAW_SMOOTH);
    } else {
      seek.yaw = wrapDeg(seek.targetYaw);
    }
    checkSeekNear(Date.now());
    applySeekView();
    seek.raf = requestAnimationFrame(seekTick);
  }

  function turnSeek(delta) {
    if (!seek || !seek.active) return;
    seek.targetYaw = wrapDeg(seek.targetYaw + delta);
  }

  function peekCorner(id) {
    if (!seek || !seek.active) return;
    if (!inView(id)) return;
    if (!seek.escaped) {
      if (id === seek.hideA) triggerEscape();
      return;
    }
    if (id === seek.hideB && (inView(id) || inNear(id))) {
      confirmFound('peek');
    }
  }

  function headingFromEvent(ev) {
    if (!ev) return null;
    if (typeof ev.webkitCompassHeading === 'number' && !isNaN(ev.webkitCompassHeading)) {
      return ev.webkitCompassHeading;
    }
    if (typeof ev.alpha === 'number' && !isNaN(ev.alpha)) {
      return ev.alpha;
    }
    return null;
  }

  function stopSeekGyro() {
    if (seek && seek.gyroHandler) {
      window.removeEventListener('deviceorientation', seek.gyroHandler, true);
      window.removeEventListener('deviceorientationabsolute', seek.gyroHandler, true);
    }
    if (seek) {
      seek.gyroHandler = null;
      seek.gyroOn = false;
      seek.gyroZero = null;
    }
    if (el.btnSeekGyro) el.btnSeekGyro.setAttribute('aria-pressed', 'false');
  }

  function startSeekGyro() {
    if (!seek || !seek.active || seek.gyroOn) return;
    seek.gyroZero = null;
    seek.gyroHandler = function (ev) {
      if (!seek || !seek.active) return;
      var raw = headingFromEvent(ev);
      if (raw == null) return;
      if (seek.gyroZero == null) {
        seek.gyroZero = wrapDeg(raw - seek.yaw);
      }
      /* 以开场标定的相对转角更新朝向，避免授权瞬间跳视。 */
      seek.targetYaw = wrapDeg(raw - seek.gyroZero);
    };
    window.addEventListener('deviceorientation', seek.gyroHandler, true);
    seek.gyroOn = true;
    if (el.btnSeekGyro) el.btnSeekGyro.setAttribute('aria-pressed', 'true');
  }

  function requestSeekGyro() {
    if (!seek || !seek.active) return;
    if (seek.gyroOn) return;
    var started = false;
    function grant() {
      if (started) return;
      started = true;
      startSeekGyro();
    }
    try {
      if (typeof DeviceOrientationEvent !== 'undefined' &&
          typeof DeviceOrientationEvent.requestPermission === 'function') {
        DeviceOrientationEvent.requestPermission().then(function (state) {
          if (state === 'granted') grant();
        }).catch(function () { /* 拒绝或本地文件受限：拖动与方向键仍可用 */ });
        return;
      }
      if (typeof DeviceOrientationEvent !== 'undefined' || 'ondeviceorientation' in window) {
        grant();
        return;
      }
    } catch (e) {}
  }

  function onSeekKey(e) {
    if (!seek || !seek.active) return;
    if (!e) return;
    var k = e.key || e.code;
    if (k === 'ArrowLeft' || k === 'Left') {
      e.preventDefault();
      turnSeek(-8);
    } else if (k === 'ArrowRight' || k === 'Right') {
      e.preventDefault();
      turnSeek(8);
    }
  }

  function bindSeekKeys() {
    if (!seek || seek.keysOn) return;
    seek.keyHandler = onSeekKey;
    window.addEventListener('keydown', seek.keyHandler, true);
    seek.keysOn = true;
  }
  function unbindSeekKeys() {
    if (seek && seek.keyHandler) {
      window.removeEventListener('keydown', seek.keyHandler, true);
    }
    if (seek) {
      seek.keyHandler = null;
      seek.keysOn = false;
    }
  }

  function bindSeekPointers() {
    if (!el.seekRoom || !seek || seek.pointerOn) return;
    seekPointer = { down: false, moved: false, x: 0, yaw: 0, id: null };
    el.seekRoom.addEventListener('pointerdown', onSeekPointerDown);
    el.seekRoom.addEventListener('pointermove', onSeekPointerMove);
    el.seekRoom.addEventListener('pointerup', onSeekPointerUp);
    el.seekRoom.addEventListener('pointercancel', onSeekPointerUp);
    el.seekRoom.addEventListener('click', onSeekRoomClick, true);
    seek.pointerOn = true;
  }
  function unbindSeekPointers() {
    if (el.seekRoom) {
      el.seekRoom.removeEventListener('pointerdown', onSeekPointerDown);
      el.seekRoom.removeEventListener('pointermove', onSeekPointerMove);
      el.seekRoom.removeEventListener('pointerup', onSeekPointerUp);
      el.seekRoom.removeEventListener('pointercancel', onSeekPointerUp);
      el.seekRoom.removeEventListener('click', onSeekRoomClick, true);
    }
    seekPointer = null;
    if (seek) seek.pointerOn = false;
  }

  function onSeekPointerDown(e) {
    if (!seek || !seek.active || !e) return;
    if (e.button != null && e.button !== 0) return;
    seekPointer = seekPointer || {};
    seekPointer.down = true;
    seekPointer.moved = false;
    seekPointer.x = e.clientX;
    seekPointer.yaw = seek.targetYaw;
    seekPointer.id = e.pointerId;
    try { el.seekRoom.setPointerCapture(e.pointerId); } catch (err) {}
  }
  function onSeekPointerMove(e) {
    if (!seek || !seek.active || !seekPointer || !seekPointer.down) return;
    var dx = e.clientX - seekPointer.x;
    if (Math.abs(dx) > 6) seekPointer.moved = true;
    var roomW = (el.seekRoom && el.seekRoom.clientWidth) || 1;
    /* 手指往右拖，画面跟随，相当于向左转。 */
    var deg = -(dx / roomW) * SEEK_FOV_DEG;
    seek.targetYaw = wrapDeg(seekPointer.yaw + deg);
    seek.yaw = seek.targetYaw;
    applySeekView();
  }
  function onSeekPointerUp(e) {
    if (!seekPointer) return;
    seekPointer.down = false;
    try {
      if (e && el.seekRoom && el.seekRoom.releasePointerCapture) {
        el.seekRoom.releasePointerCapture(e.pointerId);
      }
    } catch (err) {}
  }
  function onSeekRoomClick(e) {
    if (!seek || !seek.active) return;
    if (seekPointer && seekPointer.moved) {
      e.preventDefault();
      e.stopPropagation();
      return;
    }
    var btn = e.target && e.target.closest ? e.target.closest('[data-corner]') : null;
    if (btn) {
      peekCorner(btn.getAttribute('data-corner'));
    }
  }

  function cleanupSeek() {
    if (seek && seek.raf) {
      cancelAnimationFrame(seek.raf);
      seek.raf = 0;
    }
    clearHintTimer();
    stopSeekGyro();
    unbindSeekKeys();
    unbindSeekPointers();
    hidePeek();
    clearTrailMarks();
    if (el.seekPan) {
      el.seekPan.classList.remove('is-slipping', 'is-static-escape');
      var bg = el.seekPan.querySelector('.seek-bg');
      if (bg) bg.remove();
    }
    if (el.seekLayer) {
      el.seekLayer.hidden = true;
      el.seekLayer.setAttribute('data-phase', '');
      el.seekLayer.setAttribute('data-hide-a', '');
      el.seekLayer.setAttribute('data-hide-b', '');
      el.seekLayer.setAttribute('data-yaw', '');
      el.seekLayer.setAttribute('data-found-ready', '0');
      el.seekLayer.setAttribute('data-escaped', '0');
    }
    if (el.btnFound) el.btnFound.setAttribute('disabled', 'disabled');
    if (el.btnSeekGyro) el.btnSeekGyro.setAttribute('aria-pressed', 'false');
    if (seek) seek.active = false;
    if (S) S.seekShell = false;
  }

  function startSeek() {
    if (!S || (S.screen !== 'S3' && S.screen !== 'S6' && S.screen !== 'S8')) return;
    if (S.screen !== 'S3') return;
    pauseCompanion();
    if (el.stampLayer) el.stampLayer.hidden = true;
    cleanupSeek();
    seek = freshSeekState();
    var spots = pickHideSpots();
    seek.active = true;
    seek.phase = 'hid';
    seek.hideA = spots.a;
    seek.hideB = spots.b;
    seek.yaw = 0;
    seek.targetYaw = 0;
    S.seekShell = true;
    S.confirmedPlace = true;
    S.foundHow = null;
    S.hideId = seek.hideA;
    S.screen = 'S5';
    clearDialogueLine();
    setSeekPrompt('泊泊好像躲到房间另一边了');
    setLabel();
    syncRoomChrome();
    var opened = false;
    function revealSeekRoom() {
      if (opened) return;
      opened = true;
      if (el.actorMotion) el.actorMotion.classList.remove('anim-leave', 'anim-return', 'anim-confirm');
      hideActorForSeek();
      if (el.seekLayer) el.seekLayer.hidden = false;
      if (el.sheet) el.sheet.hidden = true;
      ensureSeekBg();
      ensureSeekPeek();
      hidePeek();
      bindSeekPointers();
      bindSeekKeys();
      if (seek.raf) cancelAnimationFrame(seek.raf);
      seek.raf = requestAnimationFrame(seekTick);
      applySeekView();
      renderSheet();
      setLabel();
      syncRoomChrome();
    }
    if (reducedMotion || headlessMotionUnsafe || !el.actor || isActorAway()) {
      revealSeekRoom();
    } else {
      var ok = playAnim('anim-leave', revealSeekRoom);
      if (!ok) revealSeekRoom();
    }
  }

  function returnActorToWindow(then) {
    if (!el.actor) return;
    if (el.actorMotion) el.actorMotion.classList.remove('anim-leave', 'anim-confirm', 'anim-return');
    el.actor.style.transition = 'none';
    showActorAfterSeek();
    el.actor.classList.add('is-found');
    placeActor(S && S.placeX != null ? S.placeX : WINDOW_PLACE_X, true);
    void el.actor.offsetWidth;
    el.actor.style.transition = '';
    later(function () {
      /* 回窗用预留的 anim-return。anim-confirm（牌耳铰链+遮罩）在当前无界面 Chrome 会卡住主线程，即使未进寻踪也会，故不在回窗后接着播。 */
      playAnim('anim-return', then);
    }, reducedMotion ? 0 : 40);
  }

  function endSeek(how) {
    if (!seek || !seek.active) {
      if (el.seekLayer) el.seekLayer.hidden = true;
      if (S) S.seekShell = false;
      syncRoomChrome();
      return;
    }
    cleanupSeek();
    seek = freshSeekState();
    if (how === 'cancel') {
      if (S) {
        S.screen = 'S3';
        S.hideId = null;
      }
      if (el.actor) {
        showActorAfterSeek();
        placeActor(S && S.placeX != null ? S.placeX : WINDOW_PLACE_X, true);
      }
      setSeekPrompt('慢慢转动手机，看看泊泊藏在哪个角落。');
      renderSheet();
      setLabel();
      syncRoomChrome();
      maybeResumeCompanion();
      return;
    }
    if (how === 'summon' || how === 'find' || how === 'peek') {
      if (S) {
        S.foundHow = how === 'summon' ? 'summon' : 'find';
        S.screen = 'S6';
      }
      setSeekPrompt('慢慢转动手机，看看泊泊藏在哪个角落。');
      renderSheet();
      setLabel();
      syncRoomChrome();
      returnActorToWindow();
      return;
    }
    /* exit / outro：只清监听与计时，并把角色重新放到窗边 */
    showActorAfterSeek();
    setSeekPrompt('慢慢转动手机，看看泊泊藏在哪个角落。');
    syncRoomChrome();
  }

  function confirmFound(how) {
    if (!seek || !seek.active) return;
    if (!seek.escaped) return;
    updateFoundReady();
    if (!seek.foundReady && how !== 'summon') return;
    clearHintTimer();
    seek.phase = 'found';
    endSeek(how || 'find');
  }

  /* ---------- stamp ---------- */

  function ensureStayStamp() {
    if (stayStampEl && stayStampEl.parentNode) return stayStampEl;
    var node = document.createElement('div');
    node.className = 'stamp-stay';
    node.id = 'stayStamp';
    node.setAttribute('aria-hidden', 'true');
    node.hidden = true;
    if (el.scene) el.scene.appendChild(node);
    stayStampEl = node;
    return node;
  }

  function showStayStamp(kind) {
    var node = ensureStayStamp();
    node.hidden = false;
    node.className = 'stamp-stay is-pattern-' + kind;
    node.setAttribute('data-pattern', kind);
  }

  function clearStayStamp() {
    if (stayStampEl) {
      stayStampEl.hidden = true;
      stayStampEl.className = 'stamp-stay';
      stayStampEl.removeAttribute('data-pattern');
    }
  }

  function syncStampPattern(kind) {
    if (!el.stampTag) return;
    el.stampTag.classList.remove('is-pattern-window', 'is-pattern-lamp');
    if (kind === 'window' || kind === 'lamp') {
      el.stampTag.classList.add('is-pattern-' + kind);
      el.stampTag.setAttribute('data-pattern', kind);
    } else {
      el.stampTag.removeAttribute('data-pattern');
    }
  }

  function closeStampShell() {
    if (el.stampLayer) el.stampLayer.hidden = true;
    if (el.stampCard) el.stampCard.classList.remove('is-need-choice');
    var card = document.querySelector('.stamp-card');
    if (card) card.classList.remove('is-need-choice');
    if (!S || !S.stamped) {
      if (el.btnStampWindow) el.btnStampWindow.setAttribute('aria-pressed', 'false');
      if (el.btnStampLamp) el.btnStampLamp.setAttribute('aria-pressed', 'false');
      if (S) S.stampChoice = null;
      syncStampPattern(null);
    }
    syncRoomChrome();
    if (S && S.screen === 'S3') maybeResumeCompanion();
  }

  function openStampShell() {
    if (!S || S.screen !== 'S3') return;
    if (isSeekOpen() || (seek && seek.active)) return;
    pauseCompanion();
    if (el.seekLayer) el.seekLayer.hidden = true;
    if (el.btnStampWindow) el.btnStampWindow.setAttribute('aria-pressed', S.stampChoice === 'window' || S.stamped === 'window' ? 'true' : 'false');
    if (el.btnStampLamp) el.btnStampLamp.setAttribute('aria-pressed', S.stampChoice === 'lamp' || S.stamped === 'lamp' ? 'true' : 'false');
    syncStampPattern(S.stamped || S.stampChoice);
    clearDialogueLine();
    if (el.stampLayer) el.stampLayer.hidden = false;
    if (el.sheet) el.sheet.hidden = true;
    syncRoomChrome();
  }

  function onStampChoice(which) {
    if (!S) return;
    S.stampChoice = which;
    if (el.btnStampWindow) el.btnStampWindow.setAttribute('aria-pressed', which === 'window' ? 'true' : 'false');
    if (el.btnStampLamp) el.btnStampLamp.setAttribute('aria-pressed', which === 'lamp' ? 'true' : 'false');
    syncStampPattern(which);
    var card = document.querySelector('.stamp-card');
    if (card) card.classList.remove('is-need-choice');
  }

  function doStamp() {
    if (!S || S.screen !== 'S3') return;
    if (S.stamped) {
      closeStampShell();
      return;
    }
    if (!S.stampChoice) {
      var card = document.querySelector('.stamp-card');
      if (card) {
        card.classList.remove('is-need-choice');
        void card.offsetWidth;
        card.classList.add('is-need-choice');
      }
      return;
    }
    var kind = S.stampChoice;
    S.stamped = kind;
    S.ritualDone = true;
    showStayStamp(kind);
    closeStampShell();
    showActorAfterSeek();
    el.actor.classList.add('is-ritual');
    el.actorMotion.classList.remove('is-look-window', 'is-look-lamp');
    el.actorMotion.classList.add(kind === 'window' ? 'is-look-window' : 'is-look-lamp');
    showDialogueLine(DIALOGUE_LINE.stay);
    /* 盖章看向与低头：真机播 approach/tremble + anim-prop；无界面 Chrome 下这些类会卡住主线程，改为只留看向姿态。 */
    if (reducedMotion || headlessMotionUnsafe) return;
    var lookAnim = kind === 'window' ? 'anim-approach' : 'anim-tremble';
    playAnim(lookAnim, function () {
      playAnim('anim-prop', function () {
        if (el.actorMotion) el.actorMotion.classList.remove('is-look-window', 'is-look-lamp');
      }, true);
    }, true);
  }

  function clearSessionVisuals() {
    cleanupSeek();
    clearDialogueLine();
    clearTimers();
    clearCompanion();
    animLock = false;
    hideModal();
    discardInput();
    resetActorVisual();
    hideActorForSeek();
    el.actor.style.left = '';
    el.screen.classList.remove('kb-open');
    el.screen.style.removeProperty('--kb-inset');
    if (el.tapRipple) {
      el.tapRipple.hidden = true;
      el.tapRipple.classList.remove('is-on');
    }
    if (el.seekLayer) el.seekLayer.hidden = true;
    if (el.stampLayer) el.stampLayer.hidden = true;
    if (el.roomDock) el.roomDock.hidden = true;
    if (el.btnStampWindow) el.btnStampWindow.setAttribute('aria-pressed', 'false');
    if (el.btnStampLamp) el.btnStampLamp.setAttribute('aria-pressed', 'false');
    syncStampPattern(null);
    clearStayStamp();
    setSeekPrompt('慢慢转动手机，看看泊泊藏在哪个角落。');
  }

  /* ---------- screens ---------- */

  function goHome() {
    clearSessionVisuals();
    S = freshSession();
    showView('home');
    setLabel();
  }


  /* 对白薄层：句子取自第二轮人物稿 7.2 / 7.3，全部待确认，不是正式台词。
     只在用户打开对白时出现；跳过或关闭不挡住动作，也不暂停自动收尾。 */
  var DIALOGUE_LINE = {
    here: '今晚在这儿。',
    look: '先看窗。',
    near: '我看窗。',
    stay: '这行字留下。',
    end: '今晚就到这儿。'
  };
  function dialogueApi() {
    try { return window.MianyuDialogue || null; } catch (e) { return null; }
  }
  function showDialogueLine(text) {
    var api = dialogueApi();
    if (!api || typeof api.showLine !== 'function' || !text) return;
    api.showLine(text);
  }
  function clearDialogueLine() {
    var api = dialogueApi();
    if (api && typeof api.clearLine === 'function') api.clearLine();
  }
  function maybeLineOnEnable() {
    if (!S) return;
    if (S.screen === 'S3' && !isSeekOpen() && !isStampOpen()) showDialogueLine(DIALOGUE_LINE.here);
    else if (S.screen === 'S9') showDialogueLine(DIALOGUE_LINE.end);
  }
  function bindDialogueToggles() {
    var api = dialogueApi();
    if (!api || typeof api.isEnabled !== 'function') return false;
    if (bindDialogueToggles.done) return true;
    bindDialogueToggles.done = true;
    /* 不调用 setHooks，也不调动效开口接口。开关在 dialogue.js 先切状态，这里后挂监听。 */
    ['btnDialogueToggle', 'btnDialogueToggleDock'].forEach(function (id) {
      var btn = document.getElementById(id);
      if (!btn) return;
      btn.addEventListener('click', function () {
        if (!api.isEnabled()) return;
        maybeLineOnEnable();
      });
    });
    return true;
  }
  function scheduleDialogueToggles() {
    if (bindDialogueToggles()) return;
    if (scheduleDialogueToggles.tries > 20) return;
    scheduleDialogueToggles.tries = (scheduleDialogueToggles.tries || 0) + 1;
    setTimeout(scheduleDialogueToggles, 50);
  }

  function startTonight() {
    clearSessionVisuals();
    S = freshSession();
    S.placed = true;
    S.placeX = WINDOW_PLACE_X;
    S.screen = 'S3';
    showView('play');
    showActorAfterSeek();
    placeActor(S.placeX, true);
    resetActorVisual();
    later(function () { playAnim('anim-settle'); }, 40);
    renderSheet();
    setLabel();
    companionLeft = COMPANION_MS;
    resumeCompanion();
    showDialogueLine(DIALOGUE_LINE.here);
  }

  function renderSheet() {
    var sc = S.screen;
    var html = '';
    var compact = (sc === 'S4' || sc === 'S5' || sc === 'S6' || sc === 'S8');
    el.sheet.classList.toggle('sheet-compact', compact);
    if (sc === 'S3') {
      html = '';
    } else if (sc === 'S4' || sc === 'S5') {
      html = '';
    } else if (sc === 'S6') {
      html += '<p>' + (S.foundHow === 'summon' ? '泊泊回来了。' : '找到了。') + '</p>';
      html += '<div class="btn-row">';
      html += '<button type="button" class="btn btn-primary" data-act="to-talk">试一句话</button>';
      html += '<button type="button" class="btn btn-ghost" data-act="watch">先看着</button>';
      html += '</div>';
    } else if (sc === 'S8') {
      html += '<p class="sim-label">演示用文字模拟语音</p>';
      html += '<p>点一句，或写一句。这是本地文字模拟，不会开麦，也不会播报。</p>';
      html += '<div class="intent-row">';
      html += '<button type="button" class="chip" data-act="say" data-text="在吗">在吗</button>';
      html += '<button type="button" class="chip" data-act="say" data-text="过来一点">过来一点</button>';
      html += '<button type="button" class="chip" data-act="say" data-text="晚安">晚安</button>';
      html += '</div>';
      html += '<form class="say-form" id="sayForm" action="#">';
      html += '<input type="text" id="sayInput" data-role="say" maxlength="40" autocomplete="off" enterkeyhint="send" placeholder="也可以写一句">';
      html += '<button type="submit" class="btn btn-quiet btn-send" id="btnSaySend">发送</button>';
      html += '</form>';
    } else if (sc === 'S9') {
      html += '<h2>今晚就到这儿</h2>';
      html += '<p>灯光慢慢收起来。</p>';
    }
    el.sheet.innerHTML = html;
    el.sheet.hidden = !html || isSeekOpen() || isStampOpen();
    bindSayForm();
    syncRoomChrome();
  }

  function bindSayForm() {
    var form = document.getElementById('sayForm');
    var input = document.getElementById('sayInput');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var val = input ? input.value : '';
      handleSay(val, true);
    });
    if (input) {
      input.addEventListener('focus', function () {
        pauseCompanion();
        later(syncKeyboard, 50);
      });
      input.addEventListener('blur', function () {
        later(function () {
          syncKeyboard();
          maybeResumeCompanion();
        }, 120);
      });
    }
  }

  /* 旧「一起藏」入口已从界面拆除，保留函数以免误接，并转入房间寻踪规则。 */
  function startHide() {
    startSeek();
  }

  function onFound(how) {
    S.foundHow = how;
    S.screen = 'S6';
    showActorAfterSeek();
    el.actor.classList.add('is-found');
    placeActor(S.placeX, false);
    later(function () { playAnim('anim-confirm'); }, 400);
    renderSheet();
    setLabel();
  }

  function goTalk() {
    pauseCompanion();
    S.screen = 'S8';
    renderSheet();
    setLabel();
  }

  function goWatch() {
    S.screen = 'S3';
    showActorAfterSeek();
    el.actor.classList.add('is-found');
    placeActor(S.placeX, true);
    renderSheet();
    setLabel();
    maybeResumeCompanion();
  }

  /* 混合意图优先级：晚安 > 靠近 > 确认 > 道具 > 其他 */
  function mapIntent(text) {
    var t = String(text || '').replace(/^\s+|\s+$/g, '');
    if (!t) return null;
    var night = /晚安|再见|拜拜|先这样|就到这/;
    var near = /过来|靠近|近一点|过来一点|这边|来这边/;
    var ack = /在吗|在不在|在嘛|你好|嗨|嘿/;
    var prop = /盖章|胸口|写牌|牌子|行李牌|印章|章/;
    if (night.test(t)) return 'night';
    if (near.test(t)) return 'near';
    if (ack.test(t)) return 'ack';
    if (prop.test(t)) return 'prop';
    return 'other';
  }

  function handleSay(text, fromTyped) {
    if (S.screen !== 'S8') return;
    var t = String(text || '').replace(/^\s+|\s+$/g, '');
    if (!t) return;
    if (animLock) return;
    var kind = mapIntent(t);
    if (!kind) return;
    S.lastInput = t;
    if (fromTyped) {
      var input = document.getElementById('sayInput');
      if (input) input.value = '';
      S.typedUsed = true;
    }
    playReply(kind);
  }

  function playReply(kind) {
    S.replies += 1;
    noteExplore();
    if (kind === 'ack') {
      showDialogueLine(DIALOGUE_LINE.here);
      playAnim('anim-confirm');
    } else if (kind === 'near') {
      showDialogueLine(DIALOGUE_LINE.near);
      playAnim('anim-approach');
      S.approached = true;
    } else if (kind === 'prop') {
      showDialogueLine(DIALOGUE_LINE.stay);
      el.actor.classList.add('is-ritual');
      S.ritualDone = true;
      playAnim('anim-prop');
    } else if (kind === 'night') {
      showDialogueLine(DIALOGUE_LINE.end);
      playAnim('anim-night', function () {
        startOutro();
      });
    } else {
      playAnim('anim-tremble');
    }
  }

  function startOutro() {
    pauseCompanion();
    hideModal();
    discardInput();
    if (seek && seek.active) endSeek('exit');
    else cleanupSeek();
    if (el.stampLayer) el.stampLayer.hidden = true;
    if (!S) S = freshSession();
    S.screen = 'S9';
    showView('play');
    if (isActorAway()) {
      goEnded();
      return;
    }
    animLock = false;
    if (!headlessMotionUnsafe) playAnim('anim-guang', null, true);
    el.palmGlow.style.opacity = '0';
    renderSheet();
    setLabel();
    showDialogueLine(DIALOGUE_LINE.end);
    later(function () {
      if (!S || S.screen !== 'S9') return;
      goEnded();
    }, (reducedMotion || headlessMotionUnsafe) ? 200 : 2800);
  }

  function goEnded() {
    cleanupSeek();
    clearDialogueLine();
    clearTimers();
    clearCompanion();
    animLock = false;
    discardInput();
    hideModal();
    resetActorVisual();
    if (el.stampLayer) el.stampLayer.hidden = true;
    if (S) S.screen = 'S10';
    showView('end');
    setLabel();
  }

  function showRipple(clientX, clientY) {
    if (!el.tapRipple) return;
    var r = el.scene.getBoundingClientRect();
    el.tapRipple.style.left = (clientX - r.left) + 'px';
    el.tapRipple.style.top = (clientY - r.top) + 'px';
    el.tapRipple.hidden = false;
    el.tapRipple.classList.remove('is-on');
    void el.tapRipple.offsetWidth;
    el.tapRipple.classList.add('is-on');
    later(function () {
      el.tapRipple.classList.remove('is-on');
      el.tapRipple.hidden = true;
    }, 720);
  }

  function lightRespond(source) {
    if (S.screen !== 'S3') return;
    noteExplore();
    /* 打招呼与看窗复用已有动作，独立图层由动效接入。 */
    if (source === 'window') {
      showDialogueLine(DIALOGUE_LINE.look);
      playAnim('anim-approach');
    } else if (source === 'actor' || source === 'greet') {
      showDialogueLine(DIALOGUE_LINE.here);
      playAnim('anim-confirm');
    } else if (source === 'lamp') {
      playAnim('anim-tremble');
    }
  }

  /* ---------- events ---------- */

  el.btnStartTonight.addEventListener('click', startTonight);
  el.btnBackHome.addEventListener('click', goHome);
  el.btnGreet.addEventListener('click', function () {
    if (!S || S.screen !== 'S3' || isSeekOpen() || isStampOpen()) return;
    lightRespond('greet');
  });
  el.btnSeek.addEventListener('click', function () {
    startSeek();
  });
  el.btnSeekCancel.addEventListener('click', function () {
    endSeek('cancel');
  });
  el.btnRecall.addEventListener('click', function () {
    endSeek('summon');
  });
  el.btnFound.addEventListener('click', function () {
    confirmFound('find');
  });
  el.btnSeekGyro.addEventListener('click', function () {
    requestSeekGyro();
  });
  el.btnStampCancel.addEventListener('click', function () {
    closeStampShell();
  });
  el.btnStamp.addEventListener('click', function () {
    doStamp();
  });
  el.btnStampWindow.addEventListener('click', function () { onStampChoice('window'); });
  el.btnStampLamp.addEventListener('click', function () { onStampChoice('lamp'); });
  el.btnEnd.addEventListener('click', function () {
    if (!S) { goEnded(); return; }
    if (S.screen === 'S1' || S.screen === 'S0' || S.screen === 'S10') {
      goEnded();
      return;
    }
    S.endedFrom = S.screen;
    if (S.placed) startOutro();
    else goEnded();
  });

  el.sheet.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-act]');
    if (!btn) return;
    var act = btn.getAttribute('data-act');
    if (act === 'hide-play') {
      startHide();
    } else if (act === 'summon') {
      if (seek && seek.active) endSeek('summon');
      else onFound('summon');
    } else if (act === 'to-talk') {
      goTalk();
    } else if (act === 'watch') {
      goWatch();
    } else if (act === 'say') {
      handleSay(btn.getAttribute('data-text') || '', false);
    }
  });

  el.modal.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-act]');
    if (btn && btn.getAttribute('data-act') === 'modal-close') {
      hideModal();
      maybeResumeCompanion();
      return;
    }
    if (e.target === el.modal) {
      hideModal();
      maybeResumeCompanion();
    }
  });

  el.scene.addEventListener('click', function (e) {
    if (!S) return;
    if (isSeekOpen() || isStampOpen()) return;
    if (e.target.closest('.sheet') || e.target.closest('.end-fab') || e.target.closest('.room-dock') || e.target.closest('.seek-layer') || e.target.closest('.stamp-layer') || e.target.closest('.dialogue-layer')) return;

    if (S.screen === 'S5') {
      var box = el.actor.getBoundingClientRect();
      var hitR = Math.max(44, box.width * 0.62);
      var hit = distanceToActor(e.clientX, e.clientY) < hitR;
      if (hit) {
        onFound('find');
        return;
      }
      showRipple(e.clientX, e.clientY);
      return;
    }

    if (S.screen === 'S3') {
      var hot = e.target.closest('[data-hot]');
      var actorBox = el.actor.getBoundingClientRect();
      var onActor = !isActorAway() && distanceToActor(e.clientX, e.clientY) < Math.max(44, actorBox.width * 0.62);
      showRipple(e.clientX, e.clientY);
      if (hot && hot.getAttribute('data-hot') === 'bag') {
        openStampShell();
      } else if (onActor) {
        lightRespond('actor');
      } else if (hot) {
        lightRespond(hot.getAttribute('data-hot'));
      } else {
        noteExplore();
      }
      return;
    }

    if (S.screen === 'S8' || S.screen === 'S6') {
      var actorBox2 = el.actor.getBoundingClientRect();
      var onActor2 = !isActorAway() && distanceToActor(e.clientX, e.clientY) < Math.max(44, actorBox2.width * 0.62);
      showRipple(e.clientX, e.clientY);
      if (onActor2 && S.screen === 'S8' && !animLock) {
        playAnim('anim-tremble');
      }
    }
  });

  function isNarrow() {
    return window.innerWidth <= 520;
  }

  function fitPhone() {
    if (isNarrow()) {
      el.phoneScale.style.transform = 'none';
      el.phoneScale.style.transformOrigin = 'center center';
      return;
    }
    var s = Math.min(1, (window.innerHeight - 48) / 844, (window.innerWidth - 24) / 390);
    if (s < 0.2) s = 0.2;
    el.phoneScale.style.transform = 'scale(' + s + ')';
    el.phoneScale.style.transformOrigin = 'center center';
  }

  function syncKeyboard() {
    var vv = window.visualViewport;
    if (!vv) {
      el.screen.classList.remove('kb-open');
      el.screen.style.removeProperty('--kb-inset');
      return;
    }
    var overlap = Math.max(0, window.innerHeight - (vv.height + vv.offsetTop));
    var open = overlap > 60;
    el.screen.classList.toggle('kb-open', open);
    el.screen.style.setProperty('--kb-inset', open ? overlap + 'px' : '0px');
    if (open) {
      var send = document.getElementById('btnSaySend');
      if (send && send.scrollIntoView) {
        try { send.scrollIntoView({ block: 'nearest', inline: 'nearest' }); } catch (e) {}
      }
      if (!el.btnEnd.hidden && el.btnEnd.scrollIntoView) {
        try { el.btnEnd.scrollIntoView({ block: 'nearest', inline: 'nearest' }); } catch (e) {}
      }
    }
  }

  window.addEventListener('resize', function () {
    fitPhone();
    syncKeyboard();
    if (seek && seek.active) applySeekView();
  });
  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', syncKeyboard);
    window.visualViewport.addEventListener('scroll', syncKeyboard);
  }
  fitPhone();

  /* dialogue.js 在 app.js 之后加载；用独立计时，避免被 clearTimers 清掉。 */
  scheduleDialogueToggles();

  /* 直接进入首页：首屏可见泊泊与「开始今晚」，不问相机，不请求方向传感器 */
  S = freshSession();
  showView('home');
  setLabel();
})();
