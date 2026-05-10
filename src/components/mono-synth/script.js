class MonoSynth extends MonoBaseElement {
  constructor() {
    super();
    this.mountTemplate('mono-synth-template');

    // UI Elements
    this.canvas = this.shadowRoot.querySelector('.synth-scope');
    this.ctx = this.canvas.getContext('2d');
    this.knobs = this.shadowRoot.querySelectorAll('.knob');
    this.keyboardInner = this.shadowRoot.querySelector('.keyboard-inner');
    this.startOverlay = this.shadowRoot.querySelector('.overlay-start');
    this.startBtn = this.shadowRoot.querySelector('.start-btn');

    // Tone.js nodes
    this.synth = null;
    this.analyzer = null;
    this.isToneLoaded = false;
    this.isAudioStarted = false;

    // State
    this.activePointers = new Map(); // For multi-touch keyboard
    this.animationFrameId = null;

    // Bindings
    this.drawScope = this.drawScope.bind(this);
    this.initAudio = this.initAudio.bind(this);
  }

  connectedCallback() {
    this.generateKeyboard();
    this.setupKnobs();

    this.startBtn.addEventListener('click', this.initAudio);

    // Resize observer for canvas
    const resizeObserver = new ResizeObserver(() => {
      if (this.canvas.clientWidth && this.canvas.clientHeight) {
        this.canvas.width = this.canvas.clientWidth;
        this.canvas.height = this.canvas.clientHeight;
      }
    });
    resizeObserver.observe(this.canvas);

    this.loadToneJs();
  }

  disconnectedCallback() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    if (this.synth) {
      this.synth.dispose();
    }
    if (this.analyzer) {
      this.analyzer.dispose();
    }
  }

  loadToneJs() {
    if (window.Tone) {
      this.isToneLoaded = true;
      return;
    }

    if (!document.getElementById('tone-js')) {
      const script = document.createElement('script');
      script.id = 'tone-js';
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js';
      script.onload = () => {
        this.isToneLoaded = true;
      };
      document.head.appendChild(script);
    } else {
      // Script is already loading, wait for it
      const checkTone = setInterval(() => {
        if (window.Tone) {
          this.isToneLoaded = true;
          clearInterval(checkTone);
        }
      }, 100);
    }
  }

  async initAudio() {
    if (!this.isToneLoaded) {
      console.warn("Tone.js not yet loaded");
      return;
    }

    try {
      await window.Tone.start();
      this.isAudioStarted = true;
      this.startOverlay.classList.add('hidden');

      this.setupSynth();
      this.updateSynthParams(); // Apply initial knob values
      this.drawScope();
    } catch (e) {
      console.error("Audio context start failed", e);
    }
  }

  setupSynth() {
    this.analyzer = new window.Tone.Analyser('waveform', 512);

    // We use a MonoSynth which combines Osc, Env, and Filter
    this.synth = new window.Tone.MonoSynth({
      oscillator: { type: "sine" },
      filter: { Q: 1, type: "lowpass", rolloff: -24 },
      envelope: { attack: 0.1, decay: 0.2, sustain: 0.5, release: 1 },
      filterEnvelope: { attack: 0.1, decay: 0.2, sustain: 0.5, release: 1, baseFrequency: 200, octaves: 4 }
    }).chain(this.analyzer, window.Tone.Destination);

    // Master volume routing
    this.volumeNode = new window.Tone.Volume(-12).toDestination();
    this.synth.disconnect();
    this.synth.chain(this.analyzer, this.volumeNode);

    // Check for custom sample
    const sampleUrl = this.getAttribute('sample');
    if (sampleUrl) {
      // We'll set up a Sampler parallel to the MonoSynth if needed,
      // but for simplicity, we'll keep it as a MonoSynth unless specifically asked to switch
      console.log("Sample URL provided:", sampleUrl);
    }
  }

  // --- UI Logic ---

  generateKeyboard() {
    // Generate 2 octaves (C3 to B4)
    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const startOctave = 3;
    const numOctaves = 2;

    for (let oct = startOctave; oct < startOctave + numOctaves; oct++) {
      for (let i = 0; i < notes.length; i++) {
        const note = notes[i];
        const isBlack = note.includes('#');
        const el = document.createElement('div');
        el.className = `key ${isBlack ? 'key-black' : 'key-white'}`;
        el.dataset.note = `${note}${oct}`;

        // Event listeners for keys
        const startNote = (e) => {
          e.preventDefault();
          if (!this.isAudioStarted) return;
          el.classList.add('active');
          const noteName = el.dataset.note;
          // Trigger attack
          this.synth.triggerAttack(noteName, window.Tone.now());
        };

        const stopNote = (e) => {
          e.preventDefault();
          el.classList.remove('active');
          if (!this.isAudioStarted) return;
          this.synth.triggerRelease(window.Tone.now());
        };

        el.addEventListener('mousedown', startNote);
        el.addEventListener('mouseup', stopNote);
        el.addEventListener('mouseleave', stopNote);

        el.addEventListener('touchstart', startNote, {passive: false});
        el.addEventListener('touchend', stopNote, {passive: false});
        el.addEventListener('touchcancel', stopNote, {passive: false});

        this.keyboardInner.appendChild(el);
      }
    }
  }

  setupKnobs() {
    let activeKnob = null;
    let startY = 0;
    let startVal = 0;

    const onPointerDown = (e, knob) => {
      e.preventDefault();
      activeKnob = knob;
      startY = e.clientY || e.touches[0].clientY;

      const type = knob.dataset.type;
      if (type === 'enum') {
        startVal = knob.dataset.idx ? parseInt(knob.dataset.idx) : 0;
      } else {
        const min = parseFloat(knob.dataset.min);
        const max = parseFloat(knob.dataset.max);
        const val = parseFloat(knob.dataset.value);
        startVal = (val - min) / (max - min); // 0 to 1
      }

      document.addEventListener('mousemove', onPointerMove);
      document.addEventListener('mouseup', onPointerUp);
      document.addEventListener('touchmove', onPointerMove, {passive: false});
      document.addEventListener('touchend', onPointerUp);
    };

    const onPointerMove = (e) => {
      if (!activeKnob) return;
      e.preventDefault();
      const clientY = e.clientY || (e.touches && e.touches[0].clientY);
      const deltaY = startY - clientY;

      const type = activeKnob.dataset.type;
      if (type === 'enum') {
        const options = activeKnob.dataset.options.split(',');
        // slower change for enums
        const step = Math.floor(deltaY / 20);
        let idx = startVal + step;
        idx = Math.max(0, Math.min(options.length - 1, idx));
        activeKnob.dataset.idx = idx;
        const valStr = options[idx];
        activeKnob.dataset.value = valStr;
        this.updateKnobDisplay(activeKnob, idx / (options.length - 1), valStr);
      } else {
        const min = parseFloat(activeKnob.dataset.min);
        const max = parseFloat(activeKnob.dataset.max);
        let newVal = startVal + (deltaY / 150); // Sensitivity
        newVal = Math.max(0, Math.min(1, newVal));

        let realVal;
        if (activeKnob.dataset.scale === 'log') {
          // simple log scale mapping
          const logMin = Math.log(min || 0.1);
          const logMax = Math.log(max);
          realVal = Math.exp(logMin + newVal * (logMax - logMin));
        } else {
          realVal = min + newVal * (max - min);
        }

        activeKnob.dataset.value = realVal;

        // Format display
        let displayVal = realVal;
        if (realVal >= 1000) displayVal = (realVal/1000).toFixed(1) + 'k';
        else if (realVal < 10) displayVal = realVal.toFixed(2);
        else displayVal = Math.round(realVal);

        this.updateKnobDisplay(activeKnob, newVal, displayVal);
      }

      this.updateSynthParams();
    };

    const onPointerUp = () => {
      activeKnob = null;
      document.removeEventListener('mousemove', onPointerMove);
      document.removeEventListener('mouseup', onPointerUp);
      document.removeEventListener('touchmove', onPointerMove);
      document.removeEventListener('touchend', onPointerUp);
    };

    this.knobs.forEach(knob => {
      // init display
      const type = knob.dataset.type;
      if (type === 'enum') {
        knob.dataset.idx = 0;
        knob.dataset.value = knob.dataset.options.split(',')[0];
        this.updateKnobDisplay(knob, 0, knob.dataset.value);
      } else {
        const min = parseFloat(knob.dataset.min);
        const max = parseFloat(knob.dataset.max);
        const val = parseFloat(knob.dataset.value);
        let norm = (val - min) / (max - min);
        if (knob.dataset.scale === 'log') {
          const logMin = Math.log(min || 0.1);
          const logMax = Math.log(max);
          norm = (Math.log(val) - logMin) / (logMax - logMin);
        }
        let displayVal = val;
        if (val >= 1000) displayVal = (val/1000).toFixed(1) + 'k';
        this.updateKnobDisplay(knob, norm, displayVal);
      }

      knob.addEventListener('mousedown', e => onPointerDown(e, knob));
      knob.addEventListener('touchstart', e => onPointerDown(e, knob), {passive: false});
    });
  }

  updateKnobDisplay(knob, normValue, labelStr) {
    const dial = knob.querySelector('.knob-dial');
    const valueEl = knob.parentElement.querySelector('.knob-value');
    // Rotate from -135deg to 135deg (270deg range)
    const angle = -135 + (normValue * 270);
    dial.style.transform = `rotate(${angle}deg)`;
    if (valueEl) valueEl.textContent = labelStr;
  }

  updateSynthParams() {
    if (!this.synth || !this.volumeNode) return;

    const params = {};
    this.knobs.forEach(k => {
      params[k.dataset.param] = k.dataset.type === 'enum' ? k.dataset.value : parseFloat(k.dataset.value);
    });

    // Update Tone.js nodes
    if (params.oscType !== 'sample') {
      this.synth.oscillator.type = params.oscType;
    }

    this.synth.filter.frequency.value = params.filterFreq;
    this.synth.filter.Q.value = params.filterRes;

    this.synth.envelope.attack = params.envA;
    this.synth.envelope.decay = params.envD;
    this.synth.envelope.sustain = params.envS;
    this.synth.envelope.release = params.envR;

    // Keep filter envelope synced with amp envelope for simplicity
    this.synth.filterEnvelope.attack = params.envA;
    this.synth.filterEnvelope.decay = params.envD;
    this.synth.filterEnvelope.sustain = params.envS;
    this.synth.filterEnvelope.release = params.envR;
    this.synth.filterEnvelope.baseFrequency = params.filterFreq / 4;

    this.volumeNode.volume.value = params.volume;
  }

  drawScope() {
    if (!this.analyzer || !this.isAudioStarted) return;

    this.animationFrameId = requestAnimationFrame(this.drawScope);

    const values = this.analyzer.getValue();
    const width = this.canvas.width;
    const height = this.canvas.height;

    this.ctx.fillStyle = 'rgba(17, 17, 17, 0.4)'; // Trail effect
    this.ctx.fillRect(0, 0, width, height);

    this.ctx.lineWidth = 2;
    this.ctx.strokeStyle = '#55ff55';
    this.ctx.beginPath();

    const sliceWidth = width * 1.0 / values.length;
    let x = 0;

    for (let i = 0; i < values.length; i++) {
      const v = values[i]; // -1 to 1
      const y = (v * 0.5 + 0.5) * height;

      if (i === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }
      x += sliceWidth;
    }

    this.ctx.stroke();
  }
}

customElements.define('mono-synth', MonoSynth);
