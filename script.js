/* ========================
   SCRIPT.JS – She Makes Scenes
   Real cursor + Soft UI pop sound + all interactions
   ======================== */

document.addEventListener('DOMContentLoaded', () => {

  // ──────────────────────────────
  // 0. GLASSMORPHIC SPLASH — auto slide up
  // ──────────────────────────────
  const splash     = document.getElementById('splash');
  const splashFill = document.getElementById('splashFill');

  // Start progress bar immediately
  requestAnimationFrame(() => {
    if (splashFill) splashFill.style.width = '100%';
  });

  // Add class so hero behind splash is blurred
  document.body.classList.add('splash-active');

  // Slide away after 3.5s — remove blur first (0.1s before slide), then slide up
  setTimeout(() => {
    // Unblur the background FIRST so it's crisp as the curtain rises
    document.body.classList.remove('splash-active');

    // Small pause so the unblur starts, then slide
    setTimeout(() => {
      if (splash) splash.classList.add('slide-away');
      // Trigger scroll animations now that hero is visible
      triggerReveal();
      // Remove from DOM after animation completes
      setTimeout(() => {
        if (splash) splash.style.display = 'none';
      }, 1200);
    }, 200);
  }, 3500);

  // ──────────────────────────────
  // 1. CLICK SOUND – Soft UI pop
  //    Inspired by the 4th click in the "10 Click Sound Effects" pack:
  //    a light, airy "bloop" — short pitched tone with fast pitch drop
  //    and a faint high shimmer. Clean, satisfying, not mechanical.
  // ──────────────────────────────
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  let audioCtx = null;
  let audioReady = false;

  function initAudio() {
    if (!audioCtx) audioCtx = new AudioContext();
  }

  function playMouseClick() {
    if (!audioCtx) return;
    const t = audioCtx.currentTime;
    const SR = audioCtx.sampleRate;

    // ── CLICK (press) ──────────────────────────────
    // Real mouse buttons make two sounds: a sharp transient on press
    // then a slightly lower "clack" as the spring releases ~80ms later.

    function makeClickLayer(startTime, freq, q, noiseDur, noiseLvl, bodyFreq, bodyLvl, bodyDur) {
      // Noise transient — the plastic mechanism impact
      const bufLen = Math.ceil(SR * noiseDur);
      const buf    = audioCtx.createBuffer(1, bufLen, SR);
      const data   = buf.getChannelData(0);
      for (let i = 0; i < bufLen; i++) data[i] = Math.random() * 2 - 1;

      const noiseNode = audioCtx.createBufferSource();
      noiseNode.buffer = buf;

      const bp = audioCtx.createBiquadFilter();
      bp.type            = 'bandpass';
      bp.frequency.value = freq;
      bp.Q.value         = q;

      const nGain = audioCtx.createGain();
      nGain.gain.setValueAtTime(noiseLvl, startTime);
      nGain.gain.exponentialRampToValueAtTime(0.001, startTime + noiseDur);

      noiseNode.connect(bp);
      bp.connect(nGain);
      nGain.connect(audioCtx.destination);
      noiseNode.start(startTime);
      noiseNode.stop(startTime + noiseDur + 0.002);

      // Body resonance — the case vibrating
      const bodyOsc  = audioCtx.createOscillator();
      const bodyGain = audioCtx.createGain();
      bodyOsc.type = 'sine';
      bodyOsc.frequency.setValueAtTime(bodyFreq, startTime);
      bodyOsc.frequency.exponentialRampToValueAtTime(bodyFreq * 0.6, startTime + bodyDur);
      bodyGain.gain.setValueAtTime(bodyLvl, startTime);
      bodyGain.gain.exponentialRampToValueAtTime(0.001, startTime + bodyDur);
      bodyOsc.connect(bodyGain);
      bodyGain.connect(audioCtx.destination);
      bodyOsc.start(startTime);
      bodyOsc.stop(startTime + bodyDur + 0.002);
    }

    // Press: sharp crack at ~4kHz centre, with a 120Hz body thud
    makeClickLayer(t,       4200, 2.5, 0.018, 0.9,  120, 0.22, 0.025);
    // Release: softer "clack" 85ms later, slightly lower ~3kHz, gentler body
    makeClickLayer(t + 0.085, 3200, 2.2, 0.014, 0.55, 95,  0.14, 0.020);
  }

  // Init on very first click (browser policy), then play on every click after
  document.addEventListener('click', () => {
    if (!audioReady) {
      initAudio();
      audioReady = true;
    }
    playMouseClick();
  });

  document.addEventListener('touchstart', () => initAudio(), { once: true });



  // ──────────────────────────────
  // 3. SCROLL REVEAL
  // ──────────────────────────────
  const revealTargets = document.querySelectorAll('.reveal-up, .pop-in');
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  function triggerReveal() {
    revealTargets.forEach(el => revealObserver.observe(el));
  }

  // ──────────────────────────────
  // 4. COUNTER ANIMATION
  // ──────────────────────────────
  const statNums = document.querySelectorAll('.stat-num');
  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  statNums.forEach(el => counterObserver.observe(el));

  function animateCounter(el) {
    const target   = parseInt(el.dataset.target, 10);
    const duration = 1600;
    const start    = performance.now();
    const tick     = now => {
      const progress = Math.min((now - start) / duration, 1);
      const ease     = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(ease * target);
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  // ──────────────────────────────
  // 5. CAMERA FEED — pause on hover
  // ──────────────────────────────
  const feedTrack  = document.querySelector('.cam-feed-track');
  const cameraBody = document.querySelector('.camera-body');
  if (feedTrack && cameraBody) {
    cameraBody.addEventListener('mouseenter', () => feedTrack.style.animationPlayState = 'paused');
    cameraBody.addEventListener('mouseleave', () => feedTrack.style.animationPlayState = 'running');
  }

  // ──────────────────────────────
  // 6. PARALLAX — subject + camera
  // ──────────────────────────────
  const subjectImg = document.getElementById('subjectImg');
  const heroCamera = document.getElementById('heroCamera');

  window.addEventListener('mousemove', e => {
    if (subjectImg) {
      const xd = (e.clientX / window.innerWidth  - 0.5) * 14;
      const yd = (e.clientY / window.innerHeight - 0.5) * 10;
      subjectImg.style.transform = `translate(${xd}px, ${yd}px)`;
    }
    if (heroCamera) {
      const xd = (e.clientX / window.innerWidth  - 0.5) * -20;
      const yd = (e.clientY / window.innerHeight - 0.5) * -14;
      heroCamera.style.transform = `translate(${xd}px, ${yd}px)`;
    }
  // ──────────────────────────────
  // 7. VIDEO LIGHTBOX MODAL
  // ──────────────────────────────
  const videoItems = document.querySelectorAll('.video-item');
  const videoModal = document.getElementById('videoModal');
  const modalVideo = document.getElementById('modalVideo');
  const modalClose = document.getElementById('modalClose');

  if (videoItems.length > 0 && videoModal && modalVideo) {
    videoItems.forEach(item => {
      item.addEventListener('click', () => {
        const videoSrc = item.getAttribute('data-video');
        if (videoSrc) {
          modalVideo.src = videoSrc;
          modalVideo.currentTime = 0;
          document.body.classList.add('modal-open');
          videoModal.classList.add('active');
          modalVideo.play();
        }
      });
    });

    const closeModal = () => {
      document.body.classList.remove('modal-open');
      videoModal.classList.remove('active');
      modalVideo.pause();
      modalVideo.src = ""; // Stop buffering
    };

    if (modalClose) {
      modalClose.addEventListener('click', closeModal);
    }

    // Close on background click
    videoModal.addEventListener('click', (e) => {
      if (e.target === videoModal) {
        closeModal();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && videoModal.classList.contains('active')) {
        closeModal();
      }
    });
  }

});
