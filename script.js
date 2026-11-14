// Web Design in Vijayawada — small progressive enhancements. The page works without this file.
;(() => {
  const WHATSAPP = '919885933339'
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  // Footer year never goes stale
  const year = document.getElementById('year')
  if (year) year.textContent = new Date().getFullYear()

  // Nav background once the page scrolls; WhatsApp pill after the hero
  const nav = document.getElementById('nav')
  const chat = document.querySelector('.float-chat')
  const onScroll = () => {
    nav.classList.toggle('is-scrolled', window.scrollY > 24)
    chat?.classList.toggle('is-shown', window.scrollY > window.innerHeight * 0.7)
  }
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()

  // Mobile menu
  const menuBtn = document.getElementById('menuBtn')
  const menu = document.getElementById('mobileMenu')
  const setMenu = (open) => {
    menu.hidden = !open
    menuBtn.setAttribute('aria-expanded', String(open))
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu')
  }
  menuBtn.addEventListener('click', () => setMenu(menu.hidden))
  menu.addEventListener('click', (e) => e.target.closest('a') && setMenu(false))
  document.addEventListener('keydown', (e) => e.key === 'Escape' && setMenu(false))

  // Intro (home page only): CSS opens the hands and fades the overlay; this removes it and lets
  // the page scroll. Clicking or pressing a key skips it. Inner pages start straight away.
  const intro = document.getElementById('intro')
  let introDone = false
  const finishIntro = () => {
    if (introDone) return
    introDone = true
    intro?.remove()
    document.body.classList.remove('is-loading')
    document.querySelector('.hero')?.classList.add('is-in')
    startReveal()
    window.__introDone = true
    window.dispatchEvent(new Event('intro:done'))
  }
  if (intro) {
    document.body.classList.add('is-loading')
    intro.addEventListener('animationend', (e) => e.animationName === 'intro-out' && finishIntro())
    intro.addEventListener('click', finishIntro)
    window.addEventListener('keydown', finishIntro, { once: true })
    setTimeout(finishIntro, reduceMotion ? 0 : 3600)
  } else {
    setTimeout(finishIntro)
  }

  // Scroll reveal (starts once the intro has gone, so the hero animates in view)
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        entry.target.classList.add('is-visible')
        io.unobserve(entry.target)
      })
    },
    { threshold: 0.15, rootMargin: '0px 0px -40px 0px' },
  )
  function startReveal() {
    document.querySelectorAll('.reveal').forEach((el) => io.observe(el))
  }

  // Project filters (home showcase and portfolio page)
  const filters = document.querySelectorAll('.filter')
  const cards = document.querySelectorAll('[data-cat]')
  filters.forEach((btn) =>
    btn.addEventListener('click', () => {
      const f = btn.dataset.filter
      filters.forEach((b) => {
        b.classList.toggle('is-active', b === btn)
        b.setAttribute('aria-pressed', String(b === btn))
      })
      cards.forEach((card) => {
        card.hidden = f !== 'all' && card.dataset.cat !== f
        if (!card.hidden) card.classList.add('is-visible')
      })
    }),
  )

  // Hero visual: layers drift with the pointer at different depths, blobs move the opposite way
  const hero = document.querySelector('.hero')
  const bg = document.querySelector('.hero-bg')
  if (hero && bg && !reduceMotion && window.matchMedia('(pointer: fine)').matches) {
    const layers = hero.querySelectorAll('[data-depth]')
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect()
      const x = (e.clientX - r.left) / r.width - 0.5
      const y = (e.clientY - r.top) / r.height - 0.5
      bg.style.transform = `translate(${x * -24}px, ${y * -24}px)`
      layers.forEach((el) => {
        const d = Number(el.dataset.depth)
        el.style.transform = `translate(${x * d}px, ${y * d}px)`
      })
    })
    hero.addEventListener('pointerleave', () => {
      bg.style.transform = ''
      layers.forEach((el) => (el.style.transform = ''))
    })
  }

  // Enquiry form → opens WhatsApp with the message pre-filled (no backend needed)
  const form = document.getElementById('enquiry')
  const error = document.getElementById('formError')
  form?.addEventListener('submit', (e) => {
    e.preventDefault()
    const data = new FormData(form)
    const name = String(data.get('name') || '').trim()
    if (!name) {
      error.hidden = false
      form.elements.name.focus()
      return
    }
    error.hidden = true
    const needs = data.getAll('need').join(', ') || 'Not sure yet'
    const lines = [
      `Hi, I'm ${name}${data.get('business') ? ` from ${data.get('business')}` : ''}.`,
      `I'm interested in: ${needs}.`,
      String(data.get('message') || '').trim(),
    ].filter(Boolean)
    window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener')
  })
})()
