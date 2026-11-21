/* 眠语 Demo 第一节点 · 影盏静态原型
 * 状态机写在本文件，供验收查看。不调用 getUserMedia，不接真麦克风，不做语音识别。
 */
(function () {
  'use strict';

  var STATES = {
    Idle: 'Idle',
    InScreenPlay: 'InScreenPlay',
    AskingCamera: 'AskingCamera',
    ArSession: 'ArSession',
    Placing: 'Placing',
    Hidden: 'Hidden',
    Found: 'Found',
    SilentComm: 'SilentComm',
    Outro: 'Outro',
    Ended: 'Ended',
    ErrorDegraded: 'ErrorDegraded'
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
    btnHomeSpace: document.getElementById('btnHomeSpace'),
    btnPlaySpace: document.getElementById('btnPlaySpace'),
    btnBackHome: document.getElementById('btnBackHome'),
    btnEndSpace: document.getElementById('btnEndSpace')
  };

  var S = null;
  var timers = [];

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
      placeX: 0.58,
      relocatesLeft: 1,
      findLeft: 2,
      hideX: 0.78,
      foundHow: null,
      ritualDone: false,
      mic: 'none',
      replies: 0,
      insert: 'a',
      approached: false,
      afterCam: 'place',
      endedFrom: null
    };
  }

  function labelOf() {
    var play = S.screen;
    if (play === 'S1' || play === 'S0') return STATES.Idle;
    if (play === 'S11') return STATES.AskingCamera;
    if (play === 'S11b') return STATES.ArSession;
    if (play === 'S12') return STATES.ErrorDegraded;
    if (play === 'S10') return STATES.Ended;
    var phase;
    if (play === 'S2' || play === 'S3') phase = STATES.Placing;
    else if (play === 'S4' || play === 'S5') phase = STATES.Hidden;
    else if (play === 'S6') phase = STATES.Found;
    else if (play === 'S7' || play === 'S8') phase = STATES.SilentComm;
    else if (play === 'S9') phase = STATES.Outro;
    else phase = STATES.InScreenPlay;
    return STATES.InScreenPlay + ' · ' + phase;
  }

  function setLabel() {
    el.stateTag.textContent = labelOf();
  }

  function showView(name) {
    el.viewSplash.hidden = name !== 'splash';
    el.viewHome.hidden = name !== 'home';
    el.viewPlay.hidden = name !== 'play';
    el.viewEnd.hidden = name !== 'end';
    el.screen.classList.toggle('is-ended', name === 'end');
    el.btnEnd.hidden = name === 'end' || name === 'splash';
  }

  function hideModal() {
    el.modal.hidden = true;
    el.modalCard.innerHTML = '';
  }

  function showModal(html) {
    el.modalCard.innerHTML = html;
    el.modal.hidden = false;
  }

  function placeActor(x, instant, opts) {
    opts = opts || {};
    var min = opts.hide ? 0.16 : 0.30;
    var max = opts.hide ? 0.42 : 0.78;
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
    el.actor.classList.remove('is-hidden', 'is-found', 'is-ritual');
    el.actorMotion.classList.remove('anim-confirm', 'anim-approach', 'anim-chat', 'anim-night', 'anim-guang', 'anim-ritual');
    el.insertA.classList.add('on');
    el.insertB.classList.remove('on');
    el.palmGlow.style.opacity = '';
    S.insert = 'a';
    S.approached = false;
    S.ritualDone = false;
  }

  function playAnim(name) {
    el.actorMotion.classList.remove('anim-confirm', 'anim-approach', 'anim-chat', 'anim-night', 'anim-guang', 'anim-ritual');
    void el.actorMotion.offsetWidth;
    el.actorMotion.classList.add(name);
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

  /* ---------- screens ---------- */

  function goHome() {
    clearTimers();
    S = freshSession();
    hideModal();
    resetActorVisual();
    el.actor.hidden = true;
    showView('home');
    setLabel();
  }

  function startInScreen(opts) {
    opts = opts || {};
    hideModal();
    if (!opts.keepProgress) {
      var afterCam = S && S.afterCam;
      S = freshSession();
      S.afterCam = afterCam || 'place';
    }
    S.screen = 'S2';
    showView('play');
    el.btnPlaySpace.hidden = false;
    if (!S.placed) {
      el.actor.hidden = true;
      resetActorVisual();
    } else {
      el.actor.hidden = false;
      placeActor(S.placeX, true);
    }
    renderSheet();
    setLabel();
  }

  function renderSheet() {
    var sc = S.screen;
    var html = '';
    var compact = (sc === 'S6' || sc === 'S7' || sc === 'S8');
    el.sheet.classList.toggle('sheet-compact', compact);
    if (sc === 'S2' || sc === 'S3') {
      html += '<h2>落位</h2>';
      if (!S.placed) {
        html += '<p>轻点桌面、地面或墙边，让影盏坐下或靠在墙边。它不会飘起来。</p>';
        html += '<p class="meta">点墙边会贴着墙的意象坐下，脚不离开桌面。</p>';
      } else if (!S.confirmedPlace) {
        html += '<p>影盏已经坐下。脚落在「地」上，没有上浮。</p>';
        if (S.relocatesLeft > 0) {
          html += '<p class="meta">落好后还可以换一次位置。开始躲藏后就不能再改。</p>';
        } else {
          html += '<p class="meta">这一局的位置已经换过一次，确认后就开始躲藏。</p>';
        }
        html += '<div class="btn-row">';
        if (S.relocatesLeft > 0) {
          html += '<button type="button" class="btn btn-quiet" data-act="relocate">换个位置</button>';
        }
        html += '<button type="button" class="btn btn-primary" data-act="confirm-place">就在这儿</button>';
        html += '</div>';
      }
    } else if (sc === 'S4') {
      html += '<h2>躲起来了</h2>';
      html += '<p>影盏沿左边墙的暖光挪开，藏进贴墙的意象里。这是意象遮挡，不是真遮挡。</p>';
    } else if (sc === 'S5') {
      html += '<h2>找一找</h2>';
      html += '<p>轻轻点墙边它藏着的地方。还可以点 ' + S.findLeft + ' 次。</p>';
      html += '<p class="meta">找不到也可以叫它回来。藏点是意象，不是真遮挡。</p>';
      html += '<button type="button" class="btn btn-ghost" data-act="summon">算了，回来吧</button>';
    } else if (sc === 'S6') {
      html += '<h2>' + (S.foundHow === 'summon' ? '它回来了' : '找到了') + '</h2>';
      html += '<p>可先做插片确认，再进入静默沟通；也可先看着，或直接关光结束。</p>';
      if (!S.ritualDone) {
        html += '<button type="button" class="btn btn-quiet" data-act="ritual">插片确认</button>';
      } else {
        html += '<p class="meta">插片确认已完成。头上插片还留着暖光。</p>';
      }
      html += '<button type="button" class="btn btn-primary" data-act="to-mic">开始静默沟通</button>';
      html += '<button type="button" class="btn btn-ghost" data-act="watch">先看着</button>';
      html += '<button type="button" class="btn btn-ghost" data-act="end-now">今晚就到这儿</button>';
    } else if (sc === 'S7') {
      html += '<h2>开麦之前</h2>';
      html += '<p>如果打开麦克风，影盏会用动作回应你说的话。语音只用来触发角色动作，可以随时关掉。这是娱乐互动，不是监测，也不是咨询。</p>';
      html += '<p class="warn meta">本原型不真开麦、不做语音识别。下面用意图按钮模拟「听懂」。</p>';
      html += '<button type="button" class="btn btn-primary" data-act="sim-mic">开麦试试看</button>';
      html += '<button type="button" class="btn btn-ghost" data-act="watch">先看着（不采集语音）</button>';
      html += '<button type="button" class="btn btn-ghost" data-act="skip-comm">跳过</button>';
    } else if (sc === 'S8') {
      html += '<h2>静默沟通</h2>';
      if (S.mic === 'listen') {
        html += '<p class="mic-state">听着呢（模拟，未接真麦克风）</p>';
        html += '<p>点意图，影盏用动作短短回应。只动、不说话。</p>';
        html += '<div class="intent-row">';
        html += '<button type="button" class="chip" data-act="intent" data-intent="ack">确认</button>';
        html += '<button type="button" class="chip" data-act="intent" data-intent="near">靠近</button>';
        html += '<button type="button" class="chip" data-act="intent" data-intent="chat">闲聊</button>';
        html += '<button type="button" class="chip" data-act="intent" data-intent="night">晚安</button>';
        html += '</div>';
        html += '<button type="button" class="btn btn-ghost" data-act="close-mic">关麦</button>';
      } else if (S.mic === 'closed') {
        html += '<p class="mic-state">已关麦</p>';
        html += '<p>已停止「听」。影盏还在，可继续看着或结束。</p>';
      } else {
        html += '<p class="mic-state">先看着，未开麦</p>';
        html += '<p>没有采集语音。影盏静坐在场。</p>';
      }
      if (S.replies >= 2) {
        html += '<p class="meta">今晚可以到这儿了。结束时会关光。</p>';
          html += '<button type="button" class="btn btn-primary" data-act="end-now">今晚就到这儿</button>';
      } else {
        html += '<button type="button" class="btn btn-ghost" data-act="end-now">今晚就到这儿</button>';
      }
    } else if (sc === 'S9') {
      html += '<h2>今晚就到这儿</h2>';
      html += '<p>影盏正在关光。掌心和边缘的暖光慢慢收起来。</p>';
    }
    el.sheet.innerHTML = html;
    el.sheet.hidden = !html;
  }

  function startHide() {
    S.confirmedPlace = true;
    S.screen = 'S4';
    S.findLeft = 2;
    /* 优先贴左墙（门框一侧），位移加大；不是真遮挡 */
    var target = Math.min(S.placeX - 0.36, 0.22);
    if (S.placeX <= 0.40) target = 0.16;
    S.hideX = placeActor(target, false, { hide: true });
    el.actor.classList.remove('is-found');
    el.actor.classList.add('is-hidden');
    renderSheet();
    setLabel();
    later(function () {
      if (S.screen !== 'S4') return;
      S.screen = 'S5';
      renderSheet();
      setLabel();
    }, 1900);
  }

  function onFound(how) {
    S.foundHow = how;
    S.screen = 'S6';
    el.actor.classList.remove('is-hidden');
    el.actor.classList.add('is-found');
    placeActor(S.placeX, false);
    later(function () { playAnim('anim-confirm'); }, 400);
    renderSheet();
    setLabel();
  }

  function doRitual() {
    S.ritualDone = true;
    el.actor.classList.add('is-ritual');
    playAnim('anim-ritual');
    renderSheet();
  }

  function goMicNotice() {
    S.screen = 'S7';
    renderSheet();
    setLabel();
  }

  function goSilent(mode) {
    S.screen = 'S8';
    S.mic = mode;
    renderSheet();
    setLabel();
  }

  function doIntent(kind) {
    if (S.mic !== 'listen') return;
    if (kind === 'ack') playAnim('anim-confirm');
    else if (kind === 'near') {
      playAnim('anim-approach');
      S.approached = true;
    } else if (kind === 'chat') playAnim('anim-chat');
    else if (kind === 'night') {
      playAnim('anim-night');
      swapInsert();
    }
    S.replies += 1;
    renderSheet();
  }

  function swapInsert() {
    if (S.insert === 'a') {
      el.insertA.classList.remove('on');
      el.insertB.classList.add('on');
      S.insert = 'b';
    } else {
      el.insertB.classList.remove('on');
      el.insertA.classList.add('on');
      S.insert = 'a';
    }
  }

  function closeMic() {
    if (S.mic === 'listen') S.mic = 'closed';
    renderSheet();
  }

  function startOutro() {
    hideModal();
    S.screen = 'S9';
    playAnim('anim-guang');
    el.palmGlow.style.opacity = '0';
    renderSheet();
    setLabel();
    later(function () {
      if (S.screen !== 'S9') return;
      goEnded();
    }, 2800);
  }

  function goEnded() {
    S.screen = 'S10';
    showView('end');
    hideModal();
    setLabel();
  }

  /* Camera: 仅用户主动进入空间后示意询问；允许或拒绝后都降级回屏内同玩法。不调用相机 API。 */
  function openCameraAsk(from) {
    S.afterCam = from;
    S.screen = 'S11';
    setLabel();
    showModal(
      '<h2 id="modalTitle">进入空间</h2>' +
      '<p>进入空间需要使用相机，把影盏放到你面前的桌面、地面或墙边。这是娱乐互动，不是监测或医疗。也可以先在屏内继续。</p>' +
      '<p class="warn">本原型不接真机相机，不代表已实现 AR。无论允许还是先在屏内继续，都会回到屏内同一套玩法。</p>' +
      '<button type="button" class="btn btn-primary" data-act="cam-allow">允许</button>' +
      '<button type="button" class="btn btn-ghost" data-act="cam-deny">先在屏内继续</button>'
    );
    el.btnPlaySpace.hidden = true;
  }

  function afterCamera(allowed) {
    if (allowed) {
      S.screen = 'S11b';
      setLabel();
      showModal(
        '<h2 id="modalTitle">空间示意</h2>' +
        '<p class="warn">本原型不接真机相机，不代表已实现 AR。不会进入真机会话。</p>' +
        '<p>即将回到屏内同玩法。</p>'
      );
      later(function () { degradeToInScreen(); }, 1200);
    } else {
      degradeToInScreen();
    }
  }

  function degradeToInScreen() {
    S.screen = 'S12';
    setLabel();
    showModal(
      '<h2 id="modalTitle">我们在屏内继续</h2>' +
      '<p>这次没能进入空间，我们在屏内继续。</p>' +
      '<p class="warn">本原型不接真机相机，不代表已实现 AR。</p>'
    );
    later(function () {
      hideModal();
      var from = S.afterCam;
      if (from === 'play' && (S.placed || S.screen === 'S12')) {
        if (S.placed) {
          if (S.foundHow) S.screen = 'S6';
          else if (S.confirmedPlace) S.screen = 'S5';
          else S.screen = 'S3';
          showView('play');
          el.actor.hidden = false;
          var hideNow = S.confirmedPlace && !S.foundHow;
          placeActor(hideNow ? S.hideX : S.placeX, true, hideNow ? { hide: true } : {});
          if (hideNow) el.actor.classList.add('is-hidden');
          el.btnPlaySpace.hidden = false;
          renderSheet();
          setLabel();
        } else {
          startInScreen({ keepProgress: true });
        }
      } else {
        startInScreen({ keepProgress: false });
      }
    }, 1400);
  }

  /* ---------- events ---------- */

  el.btnStartTonight.addEventListener('click', function () {
    startInScreen({ keepProgress: false });
  });
  el.btnHomeSpace.addEventListener('click', function () {
    if (!S) S = freshSession();
    openCameraAsk('home');
  });
  el.btnPlaySpace.addEventListener('click', function () {
    openCameraAsk('play');
  });
  el.btnEndSpace.addEventListener('click', function () {
    openCameraAsk('end');
  });
  el.btnBackHome.addEventListener('click', goHome);
  el.btnEnd.addEventListener('click', function () {
    if (!S) { goEnded(); return; }
    if (S.screen === 'S1' || S.screen === 'S0' || S.screen === 'S10') {
      goEnded();
      return;
    }
    if (S.placed) startOutro();
    else goEnded();
  });

  el.sheet.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-act]');
    if (!btn) return;
    var act = btn.getAttribute('data-act');
    if (act === 'relocate') {
      S.relocatesLeft -= 1;
      S.placed = false;
      S.screen = 'S2';
      el.actor.hidden = true;
      renderSheet();
    } else if (act === 'confirm-place') {
      startHide();
    } else if (act === 'summon') {
      onFound('summon');
    } else if (act === 'ritual') {
      doRitual();
    } else if (act === 'to-mic') {
      goMicNotice();
    } else if (act === 'sim-mic') {
      goSilent('listen');
    } else if (act === 'watch') {
      goSilent('watch');
    } else if (act === 'skip-comm') {
      startOutro();
    } else if (act === 'close-mic') {
      closeMic();
    } else if (act === 'intent') {
      doIntent(btn.getAttribute('data-intent'));
    } else if (act === 'end-now') {
      startOutro();
    }
  });

  el.modal.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-act]');
    if (!btn) return;
    var act = btn.getAttribute('data-act');
    if (act === 'cam-allow') afterCamera(true);
    else if (act === 'cam-deny') afterCamera(false);
  });

  el.sceneTouch.addEventListener('click', function (e) {
    if (S.screen === 'S2' || (S.screen === 'S3' && !S.placed)) {
      S.placeX = placeActor(clampTapX(e.clientX), true);
      S.placed = true;
      S.screen = 'S3';
      el.actor.hidden = false;
      el.actor.classList.remove('is-hidden');
      resetActorVisual();
      later(function () { playAnim('anim-confirm'); }, 80);
      renderSheet();
      setLabel();
      return;
    }
    if (S.screen === 'S5') {
      var box = el.actor.getBoundingClientRect();
      var hitR = Math.max(44, box.width * 0.62);
      var hit = distanceToActor(e.clientX, e.clientY) < hitR;
      if (hit) {
        onFound('find');
        return;
      }
      S.findLeft -= 1;
      if (S.findLeft <= 0) {
        onFound('summon');
      } else {
        renderSheet();
        var note = el.sheet.querySelector('p');
        if (note) note.textContent = '还没找到，再轻轻点一次。还可以点 ' + S.findLeft + ' 次，或让它回来。';
      }
    }
  });

  function fitPhone() {
    var s = Math.min(1, (window.innerHeight - 48) / 844, (window.innerWidth - 24) / 390);
    if (s < 0.2) s = 0.2;
    el.phoneScale.style.transform = 'scale(' + s + ')';
    el.phoneScale.style.transformOrigin = 'center center';
  }
  window.addEventListener('resize', fitPhone);
  fitPhone();

  /* short splash then home; 启动不问相机 */
  S = freshSession();
  S.screen = 'S0';
  showView('splash');
  setLabel();
  later(function () {
    goHome();
  }, 900);
})();
