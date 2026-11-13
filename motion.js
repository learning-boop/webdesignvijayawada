// Scroll-driven animations: smooth scroll, split headline, logo dot reveal,
// stacking service cards with live demos, and magnetic buttons.
// Needs GSAP + ScrollTrigger (+ Lenis for smooth scroll). Without them the page stays static.
;(() => {
  const root = document.documentElement
  if (!root.classList.contains('motion')) return
  if (!window.gsap || !window.ScrollTrigger) {
    root.classList.remove('motion')
    return
  }
  window.__motionReady = true
  gsap.registerPlugin(ScrollTrigger)

  const onIntroDone = (fn) =>
    window.__introDone ? fn() : window.addEventListener('intro:done', fn, { once: true })

  /* ---------- Smooth scroll ---------- */
  let lenis = null
  if (window.Lenis) {
    lenis = new Lenis({ lerp: 0.1 })
    lenis.on('scroll', ScrollTrigger.update)
    gsap.ticker.add((time) => lenis.raf(time * 1000))
    gsap.ticker.lagSmoothing(0)
    if (!window.__introDone) lenis.stop()

    // In-page links glide instead of jumping
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[href^="#"]:not(.skip)')
      if (!link) return
      const hash = link.getAttribute('href')
      const target = hash === '#top' ? 0 : document.querySelector(hash)
      if (target === null) return
      e.preventDefault()
      lenis.scrollTo(target, { offset: hash === '#top' ? 0 : -90, duration: 1.4 })
      history.replaceState(null, '', hash)
    })
  }

  onIntroDone(() => {
    lenis?.start()
    ScrollTrigger.refresh()
  })
  document.fonts?.ready.then(() => ScrollTrigger.refresh())
  // Filtering projects shortens the pinned showcase. Jump to its start first (which doesn't move),
  // let the scroll position settle for a frame, then re-measure.
  document.querySelectorAll('.filter').forEach((b) =>
    b.addEventListener('click', () => {
      const pin = ScrollTrigger.getById('work')
      if (pin) lenis ? lenis.scrollTo(pin.start, { immediate: true, force: true }) : scrollTo(0, pin.start)
      requestAnimationFrame(() => requestAnimationFrame(() => ScrollTrigger.refresh()))
    }),
  )
  // Opening an FAQ changes the page height
  document.addEventListener('toggle', () => ScrollTrigger.refresh(), true)

  /* ---------- Split-text headline ---------- */
  const wrapWord = (content) => {
    const outer = document.createElement('span')
    const inner = document.createElement('span')
    outer.className = 'w'
    inner.className = 'wi'
    inner.append(content)
    outer.append(inner)
    return outer
  }
  const splitWords = (el) => {
    ;[...el.childNodes].forEach((node) => {
      if (node.nodeType === Node.TEXT_NODE) {
        const frag = document.createDocumentFragment()
        node.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return
          frag.append(/^\s+$/.test(part) ? ' ' : wrapWord(part))
        })
        node.replaceWith(frag)
      } else if (node.tagName === 'EM') {
        // Keep the gradient word whole so its colour sweep stays intact
        const word = wrapWord('')
        node.replaceWith(word)
        word.firstChild.append(node)
      } else {
        splitWords(node)
      }
    })
  }

  const title = document.getElementById('heroTitle')
  if (title) {
    splitWords(title)
    const titleWords = title.querySelectorAll('.wi')
    gsap.set(titleWords, { yPercent: 115 })
    title.classList.add('is-split')
    onIntroDone(() =>
      gsap.to(titleWords, { yPercent: 0, duration: 1.1, ease: 'power4.out', stagger: 0.07, delay: 0.05 }),
    )
  }

  /* ---------- Logo story: hands part, dot grows into the panel ---------- */
  const reveal = document.querySelector('.dotreveal')
  if (reveal) {
    const panel = reveal.querySelector('.dr-panel')
    const logo = reveal.querySelector('.dr-logo')
    const dot = reveal.querySelector('.dr-dot')
    const drText = reveal.querySelector('.dr-text')

    const words = drText.textContent.trim().split(/\s+/)
    drText.textContent = ''
    words.forEach((w, i) => {
      const span = document.createElement('span')
      span.className = 'w'
      span.textContent = w
      drText.append(span, i < words.length - 1 ? ' ' : '')
    })

    // The green dot is ~17.8% of the logo's width
    const dotRadius = () => logo.offsetWidth * 0.089
    const fullRadius = () => Math.hypot(innerWidth, innerHeight) / 2 + 40

    gsap
      .timeline({
        defaults: { ease: 'none' },
        scrollTrigger: {
          trigger: reveal,
          start: 'top top',
          end: 'bottom bottom',
          scrub: 0.8,
          invalidateOnRefresh: true,
        },
      })
      // fromTo everywhere: invalidateOnRefresh re-reads start values, which would break plain from/to
      .fromTo(panel, { '--r': dotRadius }, { '--r': fullRadius, duration: 0.4, ease: 'power2.in' }, 0)
      .fromTo(logo.querySelector('.hand-blue'), { xPercent: 0, yPercent: 0, rotate: 0 }, { xPercent: -95, yPercent: -85, rotate: -30, duration: 0.4, ease: 'power1.in' }, 0)
      .fromTo(logo.querySelector('.hand-pink'), { xPercent: 0, yPercent: 0, rotate: 0 }, { xPercent: 95, yPercent: 85, rotate: -30, duration: 0.4, ease: 'power1.in' }, 0)
      .fromTo(logo, { opacity: 1 }, { opacity: 0, duration: 0.1 }, 0.3)
      .fromTo(dot, { opacity: 1 }, { opacity: 0, duration: 0.18 }, 0.14)
      .fromTo(reveal.querySelector('.dr-content'), { opacity: 0 }, { opacity: 1, duration: 0.12 }, 0.22)
      .fromTo(reveal.querySelector('.eyebrow'), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.08 }, 0.36)
      .fromTo(drText.querySelectorAll('.w'), { opacity: 0.28 }, { opacity: 1, stagger: 0.012, duration: 0.05 }, 0.4)
      .fromTo(reveal.querySelectorAll('.dr-points li'), { opacity: 0, y: 40 }, { opacity: 1, y: 0, stagger: 0.05, duration: 0.12 }, 0.78)
  }

  /* ---------- Sideways project showcase (desktop) ---------- */
  const work = document.querySelector('.work')
  if (work) {
    const track = work.querySelector('.work-track')
    const bar = work.querySelector('.work-progress u')
    const countEl = work.querySelector('.work-count b')
    const totalEl = work.querySelector('.work-total')
    const pad = (n) => String(n).padStart(2, '0')

    gsap.matchMedia().add('(min-width: 861px) and (min-height: 641px)', () => {
      const distance = () => Math.max(0, track.scrollWidth - innerWidth)
      const skew = gsap.quickTo(track, 'skewX', { duration: 0.5, ease: 'power3.out' })
      const settle = () => skew(0)
      ScrollTrigger.addEventListener('scrollEnd', settle)

      gsap.fromTo(track, { x: 0 }, {
        x: () => -distance(),
        ease: 'none',
        scrollTrigger: {
          id: 'work',
          trigger: work,
          start: 'top top',
          end: () => `+=${distance()}`,
          pin: true,
          scrub: 0.6,
          anticipatePin: 1,
          invalidateOnRefresh: true,
          onRefresh: (self) => self.vars.onUpdate(self),
          onUpdate: (self) => {
            const total = track.querySelectorAll('.work-card:not([hidden])').length
            bar.style.transform = `scaleX(${self.progress})`
            countEl.textContent = pad(Math.min(total, 1 + Math.floor(self.progress * total)))
            totalEl.textContent = pad(total)
            // Lean slightly into fast scrolling
            skew(gsap.utils.clamp(-4, 4, self.getVelocity() / -300))
          },
        },
      })

      return () => ScrollTrigger.removeEventListener('scrollEnd', settle)
    })
  }

  /* ---------- Stacking service cards ---------- */
  const cards = gsap.utils.toArray('.scard')
  gsap.matchMedia().add('(min-width: 861px) and (min-height: 641px)', () => {
    cards.forEach((card, i) => {
      const next = cards[i + 1]
      if (!next) return
      gsap.to(card, {
        scale: 0.93,
        ease: 'none',
        scrollTrigger: {
          trigger: next,
          start: 'top bottom',
          end: () => `top ${96 + (i + 1) * 18}px`,
          scrub: true,
        },
      })
    })
  })

  /* ---------- Live demos inside the cards (play only while visible) ---------- */
  const counter = (el, to, duration) => {
    const obj = { v: 0 }
    return gsap.to(obj, {
      v: to,
      duration,
      ease: 'power2.out',
      onStart: () => (el.textContent = 0),
      onUpdate: () => (el.textContent = Math.round(obj.v)),
    })
  }

  const demos = {
    speed(card) {
      return gsap
        .timeline({ repeat: -1, repeatDelay: 2.5 })
        .fromTo(card.querySelector('.speed-arc'), { strokeDashoffset: 314 }, { strokeDashoffset: 6, duration: 1.8, ease: 'power2.out' })
        .add(counter(card.querySelector('.speed-num'), 98, 1.8), 0)
        .fromTo(card.querySelectorAll('.metrics u'), { scaleX: 0 }, { scaleX: 1, duration: 1, stagger: 0.15, ease: 'power3.out' }, 0.2)
    },

    seo(card) {
      const q = card.querySelector('.search-q')
      const query = 'web designers in vijayawada'
      const rows = [...card.querySelectorAll('.serp-row')]
      const you = card.querySelector('.serp-you')
      const rank = card.querySelector('.serp-rank')
      const typed = { n: 0 }
      const tl = gsap
        .timeline({ repeat: -1, repeatDelay: 2.2 })
        .set(rows, { y: 0 })
        .call(() => (rank.textContent = '#4'))
        .fromTo(typed, { n: 0 }, {
          n: query.length,
          duration: 1.4,
          ease: 'none',
          onUpdate: () => (q.textContent = query.slice(0, Math.round(typed.n))),
        })
      // Climb one place at a time, pushing each competitor down
      for (let step = 1; step <= 3; step++) {
        tl.to(you, { y: -step * 64, duration: 0.55, ease: 'power3.inOut' }, step === 1 ? '+=0.4' : '+=0.25')
          .to(rows[3 - step], { y: 64, duration: 0.55, ease: 'power3.inOut' }, '<')
          .call(() => (rank.textContent = `#${4 - step}`))
      }
      return tl
    },

    chat(card) {
      const [in1, typing, out1, in2, out2] = card.querySelectorAll('.msg')
      const show = (el) => ({ display: el === typing ? 'inline-flex' : 'block' })
      const pop = { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: 'back.out(1.8)' }
      const from = { opacity: 0, y: 10, scale: 0.96 }
      return gsap
        .timeline({ repeat: -1, repeatDelay: 1.5 })
        .set([in1, typing, out1, in2, out2], { display: 'none', ...from })
        .set(in1, show(in1)).to(in1, pop, '+=0.3')
        .set(typing, show(typing), '+=0.4').to(typing, pop)
        .set(typing, { display: 'none' }, '+=1')
        .set(out1, show(out1)).to(out1, pop)
        .set(in2, show(in2), '+=0.9').to(in2, pop)
        .set(typing, show(typing), '+=0.4').to(typing, pop)
        .set(typing, { display: 'none' }, '+=0.9')
        .set(out2, show(out2)).to(out2, pop)
        .to([in1, out1, in2, out2], { opacity: 0, duration: 0.4 }, '+=2.6')
    },

    ads(card) {
      return gsap
        .timeline({ repeat: -1, repeatDelay: 2.5 })
        .fromTo(card.querySelector('.ads-chart'), { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 2, ease: 'power2.inOut' })
        .add(counter(card.querySelector('.ads-num'), 148, 2), 0)
        .fromTo(card.querySelectorAll('.ads-split span'), { opacity: 0, y: 8 }, { opacity: 1, y: 0, stagger: 0.12, duration: 0.4 }, 0.6)
    },
  }

  cards.forEach((card) => {
    const tl = demos[card.dataset.live]?.(card)
    if (!tl) return
    tl.pause(0)
    ScrollTrigger.create({
      trigger: card,
      start: 'top 80%',
      endTrigger: '.stack',
      end: 'bottom top',
      onToggle: (self) => (self.isActive ? tl.play() : tl.pause()),
    })
  })

  /* ---------- Magnetic buttons (mouse only) ---------- */
  if (matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.btn:not(.btn-block), .icon-circle, .menu-btn, .filter').forEach((el) => {
      el.classList.add('is-magnetic')
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect()
        gsap.to(el, {
          x: (e.clientX - r.left - r.width / 2) * 0.35,
          y: (e.clientY - r.top - r.height / 2) * 0.35,
          duration: 0.5,
          ease: 'power3.out',
          overwrite: 'auto',
        })
      })
      el.addEventListener('pointerleave', () =>
        gsap.to(el, { x: 0, y: 0, duration: 0.9, ease: 'elastic.out(1, 0.4)', overwrite: 'auto' }),
      )
    })
  }
})()
