// Moteur de la maquette : une table, une boîte, des étapes jouées au clic.
// Chaque cas = { table: [cartes], etapes: [etape] }. Une étape :
//   { onglet, cadre, titre, sous, corps (html), bouton ('Continuer' | null), montre: [actions], suite: [actions] }
// Les boutons du corps marqués data-suite font passer à l'étape suivante (une réponse à une question).
(function () {
  const J = window.JETONS;
  const reduit = () => document.documentElement.classList.contains('sans-mouvement');
  const DUREE = 650;

  const PILES = {
    paquet: { nom: 'Paquet rencontre', t: 'pile-rencontre' },
    defausse: { nom: 'Défausse rencontre', t: 'pile-defausse' },
    defausseJ: { nom: 'Ta défausse', t: 'pile-joueur' },
    victoire: { nom: 'Victoire', t: 'pile-victoire' },
    retire: { nom: 'Retirées', t: 'pile-retire' },
    main: { nom: 'Ta main', t: 'pile-main' },
  };

  let scene, etat, iEtape, elStage, elBoite, elTable, elSvg, elJetons, enVol, attente;

  function el(html) {
    const d = document.createElement('div');
    d.innerHTML = html.trim();
    return d.firstElementChild;
  }

  function rectDans(e) {
    const s = elStage.getBoundingClientRect();
    const r = e.getBoundingClientRect();
    return { x: r.left - s.left, y: r.top - s.top, w: r.width, h: r.height };
  }

  function cible(ref) {
    if (ref === 'boite') return elBoite.querySelector('.corps');
    if (typeof ref === 'string' && ref.startsWith('b:')) return elBoite.querySelector(`[data-id="${ref.slice(2)}"]`) || elBoite.querySelector('.corps');
    return elTable.querySelector(`[data-carte="${ref}"]`);
  }

  function bord(r, vers) {
    const cx = r.x + r.w / 2, cy = r.y + r.h / 2;
    const dx = vers.x - cx, dy = vers.y - cy;
    if (!dx && !dy) return { x: cx, y: cy };
    const k = Math.min(dx ? r.w / 2 / Math.abs(dx) : Infinity, dy ? r.h / 2 / Math.abs(dy) : Infinity, 1);
    return { x: cx + dx * k, y: cy + dy * k };
  }

  function trace(de, vers) {
    const a = cible(de), b = cible(vers);
    if (!a || !b) return null;
    const ra = rectDans(a), rb = rectDans(b);
    if (!ra.w || !rb.w) return null;
    const ca = { x: ra.x + ra.w / 2, y: ra.y + ra.h / 2 }, cb = { x: rb.x + rb.w / 2, y: rb.y + rb.h / 2 };
    const p0 = bord(ra, cb), p2 = bord(rb, ca);
    const l = Math.hypot(p2.x - p0.x, p2.y - p0.y) || 1;
    let nx = -(p2.y - p0.y) / l, ny = (p2.x - p0.x) / l;
    if (ny > 0) { nx = -nx; ny = -ny; }
    const b2 = Math.min(80, l * 0.22);
    const p1 = { x: (p0.x + p2.x) / 2 + nx * b2, y: (p0.y + p2.y) / 2 + ny * b2 };
    return { p0, p1, p2 };
  }

  function point(t, k) {
    const u = 1 - k;
    return { x: u * u * t.p0.x + 2 * u * k * t.p1.x + k * k * t.p2.x, y: u * u * t.p0.y + 2 * u * k * t.p1.y + k * k * t.p2.y };
  }

  // ---------------------------------------------------------------- la table
  function dessinerTable() {
    elTable.innerHTML = '';
    for (const c of etat.cartes) {
      const pile = PILES[c.pile];
      const e = el(`<div class="carte t-${c.t || (pile && pile.t) || 'pile'}" data-carte="${c.id}" style="left:${c.x}%;top:${c.y}%"></div>`);
      if (c.joueur) e.style.setProperty('--joueur', `var(--j${c.joueur})`);
      e.innerHTML = `<span class="nom">${c.nom || (pile && pile.nom) || ''}</span>${c.sous ? `<span class="type">${c.sous}</span>` : ''}<span class="compteur" ${c.c === undefined ? 'hidden' : ''}>${c.c ?? ''}</span><span class="marque" hidden></span>`;
      elTable.append(e);
      appliquer(c);
    }
  }

  function carteEtat(id) { return etat.cartes.find((c) => c.id === id); }

  function appliquer(c) {
    const e = elTable.querySelector(`[data-carte="${c.id}"]`);
    if (!e) return;
    e.style.left = `${c.x}%`;
    e.style.top = `${c.y}%`;
    e.classList.toggle('cache', !!c.cache);
    e.classList.toggle('pointilles', !!c.pointilles);
    e.classList.toggle('incline', !!c.incline);
    e.classList.toggle('grise', !!c.grise);
    e.classList.toggle('dos', !!c.dos);
    const cp = e.querySelector('.compteur');
    if (c.c !== undefined) { cp.hidden = false; cp.textContent = c.c; } else cp.hidden = true;
    cp.classList.toggle('rouge', !!c.rouge);
    const m = e.querySelector('.marque');
    m.hidden = !c.marque;
    m.innerHTML = c.marque || '';
    e.style.removeProperty('--halo');
    if (c.halo) e.style.setProperty('--halo', `var(--${c.halo})`);
    e.classList.toggle('a-halo', !!c.halo);
  }

  function maj(id, champs) {
    const c = carteEtat(id);
    if (!c) return;
    Object.assign(c, champs);
    appliquer(c);
  }

  // ---------------------------------------------------------------- les traits
  function dessinerTraits() {
    elSvg.innerHTML = '';
    const s = elStage.getBoundingClientRect();
    elSvg.setAttribute('viewBox', `0 0 ${s.width} ${s.height}`);
    for (const t of etat.traits) {
      const tr = trace(t.de, t.vers);
      if (!tr) continue;
      const ang = Math.atan2(tr.p2.y - tr.p1.y, tr.p2.x - tr.p1.x);
      const q = (a) => `${tr.p2.x - 12 * Math.cos(ang + a)},${tr.p2.y - 12 * Math.sin(ang + a)}`;
      const coul = `var(--${t.couleur || 'acier'})`;
      elSvg.insertAdjacentHTML('beforeend', `<path class="trait ${reduit() ? '' : 'anime'}" d="M${tr.p0.x},${tr.p0.y} Q${tr.p1.x},${tr.p1.y} ${tr.p2.x},${tr.p2.y}" style="stroke:${coul}"/><path d="M${tr.p2.x},${tr.p2.y} L${q(0.45)} L${q(-0.45)} Z" style="fill:${coul}"/>`);
    }
  }

  // ---------------------------------------------------------------- les jetons
  function poserJetons() {
    for (const j of etat.jetons) {
      const tr = trace(j.de, j.vers);
      if (!tr) continue;
      let e = elJetons.querySelector(`[data-jeton="${j.id}"]`);
      if (!e) {
        e = el(`<div class="jeton j-${j.genre}" data-jeton="${j.id}"><img alt="" src="${J[j.genre === 'degats' ? 'degats' : j.genre === 'acceleration' ? 'acceleration' : 'menace']}"><b>${j.label}</b></div>`);
        elJetons.append(e);
      }
      e.style.transform = `translate(${tr.p0.x}px,${tr.p0.y}px) translate(-50%,-50%)`;
    }
  }

  function volerJeton(id, puis) {
    const j = etat.jetons.find((x) => x.id === id);
    const e = elJetons.querySelector(`[data-jeton="${id}"]`);
    etat.jetons = etat.jetons.filter((x) => x.id !== id);
    const fin = () => { e && e.remove(); if (puis) maj(puis.carte, puis.etat || { c: puis.c }); son(); };
    if (!j || !e || reduit()) return fin();
    const tr = trace(j.de, j.vers);
    if (!tr) return fin();
    const cles = Array.from({ length: 13 }, (_, k) => { const p = point(tr, k / 12); return { transform: `translate(${p.x}px,${p.y}px) translate(-50%,-50%)` }; });
    const a = e.animate(cles, { duration: DUREE, easing: 'cubic-bezier(.3,.7,.2,1)', fill: 'forwards' });
    enVol.push({ a, fin });
    a.onfinish = fin;
  }

  // ---------------------------------------------------------------- les cartes qui volent
  function volerCopie(de, vers, texte, fondu) {
    return new Promise((ok) => {
      const a = cible(de), b = cible(vers);
      if (!a || !b || reduit()) return ok();
      const ra = rectDans(a), rb = rectDans(b);
      const w = Math.min(ra.w, 70), h = Math.min(ra.h, 96);
      const c = el(`<div class="copie">${texte || ''}</div>`);
      Object.assign(c.style, { left: `${ra.x + ra.w / 2 - w / 2}px`, top: `${ra.y + ra.h / 2 - h / 2}px`, width: `${w}px`, height: `${h}px` });
      elJetons.append(c);
      const dx = rb.x + rb.w / 2 - (ra.x + ra.w / 2), dy = rb.y + rb.h / 2 - (ra.y + ra.h / 2);
      const an = c.animate([{ transform: 'translate(0,0)', opacity: 1 }, { transform: `translate(${dx}px,${dy}px)`, opacity: fondu ? 0.2 : 1 }], { duration: DUREE, easing: 'cubic-bezier(.3,.7,.2,1)', fill: 'forwards' });
      const fin = () => { c.remove(); ok(); };
      enVol.push({ a: an, fin });
      an.onfinish = fin;
    });
  }

  // ---------------------------------------------------------------- les actions
  const ACTIONS = {
    trait: (a) => etat.traits.push(a),
    jeton: (a) => etat.jetons.push(a),
    vole: (a) => volerJeton(a.id, a.puis),
    maj: (a) => maj(a.carte, a.etat),
    place: (a) => maj(a.carte, { cache: false, pointilles: true }),
    arrive: (a) => {
      const c = carteEtat(a.carte);
      maj(a.carte, { cache: false, pointilles: true });
      const t = setTimeout(() => volerCopie(a.de, a.carte, c && c.nom).then(() => maj(a.carte, { pointilles: false, ...(a.etat || {}) })), a.delai || 0);
      attente.push(t);
    },
    part: (a) => {
      const c = carteEtat(a.carte);
      const t = setTimeout(() => {
        const p = volerCopie(a.carte, a.vers, c && c.nom, true);
        maj(a.carte, { cache: true, halo: null, marque: null });
        p.then(() => {});
      }, a.delai || 0);
      attente.push(t);
    },
    copie: (a) => { const t = setTimeout(() => volerCopie(a.de, a.vers, a.texte, a.fondu), a.delai || 0); attente.push(t); },
    secousse: () => { if (!reduit()) elBoite.animate([{ transform: 'translateX(0)' }, { transform: 'translateX(-6px)' }, { transform: 'translateX(6px)' }, { transform: 'translateX(-3px)' }, { transform: 'translateX(0)' }], { duration: 320 }); },
    fondu: (a) => { for (const id of a.cartes) { const e = elTable.querySelector(`[data-carte="${id}"]`); if (e && !reduit()) e.animate([{ opacity: 1 }, { opacity: 0 }], { duration: DUREE, fill: 'forwards' }); const t = setTimeout(() => maj(id, { cache: true }), reduit() ? 0 : DUREE); attente.push(t); } },
  };

  function jouer(actions) { for (const a of actions || []) ACTIONS[a.f](a); }

  let audio;
  function son() {
    if (!document.getElementById('son')?.checked) return;
    try {
      audio = audio || new AudioContext();
      const o = audio.createOscillator(), g = audio.createGain();
      o.frequency.value = 520; g.gain.value = 0.06;
      o.connect(g).connect(audio.destination);
      o.start(); g.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + 0.09); o.stop(audio.currentTime + 0.1);
    } catch (e) { /* pas de son */ }
  }

  // ---------------------------------------------------------------- la boîte
  const ONGLETS = [['1', 'Menaces'], ['2A', 'Méchant'], ['2B', 'Sbires'], ['3', 'Cartes rencontre'], ['B', 'Bilan']];

  function dessinerBoite() {
    const et = scene.etapes[iEtape];
    elBoite.className = `boite cadre-${et.cadre || 'commun'}${et.rouge ? ' est-rouge' : ''}`;
    const onglets = ONGLETS.map(([k, n]) => {
      const vide = (et.ongletsVides || []).includes(k);
      return `<li class="${k === et.onglet ? 'actif' : ''}${vide ? ' vide' : ''}"><b>${k === 'B' ? '✓' : k}</b> ${vide ? '—' : n}</li>`;
    }).join('');
    const pastille = et.joueur ? `<span class="pastille" style="--joueur:var(--j${et.joueur})">J${et.joueur}</span>` : '';
    const reponse = et.reponse ? `<button class="pastille-reponse" data-suite type="button">1 réponse possible · ${et.reponse}</button>` : '';
    elBoite.innerHTML = `
      <ol class="onglets">${onglets}</ol>
      <header class="tete"><div><h3>${et.titre}</h3>${et.sous ? `<p class="sous">${et.sous}</p>` : ''}</div><div class="outils">${reponse}${pastille}</div></header>
      <div class="corps">${et.corps}</div>
      <footer class="pied">${et.bouton === null ? '' : `<button class="continuer" type="button" data-suite>${et.bouton || 'Continuer'} <kbd>Espace</kbd></button>`}</footer>`;
    elBoite.querySelectorAll('[data-suite]').forEach((b) => b.addEventListener('click', suivant));
    const compte = document.getElementById('compte-etape');
    compte.textContent = `Écran ${iEtape + 1} / ${scene.etapes.length}`;
  }

  function nettoyer() {
    for (const v of enVol.splice(0)) { try { v.a.finish(); } catch (e) { /* fini */ } v.fin(); }
    for (const t of attente.splice(0)) clearTimeout(t);
  }

  function montrer() {
    etat.traits = [];
    for (const c of etat.cartes) if (c.halo && !c.haloGarde) { c.halo = null; appliquer(c); }
    dessinerBoite();
    jouer(scene.etapes[iEtape].montre);
    requestAnimationFrame(() => { dessinerTraits(); poserJetons(); });
  }

  function suivant() {
    if (iEtape >= scene.etapes.length - 1) {
      jouer(scene.etapes[iEtape].suite);
      elBoite.querySelector('.pied')?.replaceChildren(el('<span class="fin">Fin du cas · <button type="button" class="lien" id="rejouer-bas">Rejouer</button></span>'));
      document.getElementById('rejouer-bas')?.addEventListener('click', () => lancer(scene));
      etat.traits = []; dessinerTraits();
      return;
    }
    nettoyer();
    jouer(scene.etapes[iEtape].suite);
    iEtape += 1;
    montrer();
  }

  function lancer(s) {
    nettoyer();
    scene = s;
    etat = { cartes: s.table.map((c) => ({ ...c })), traits: [], jetons: [] };
    iEtape = 0;
    elJetons.innerHTML = '';
    dessinerTable();
    montrer();
  }

  window.MAQUETTE = {
    init() {
      elStage = document.getElementById('stage');
      elBoite = document.getElementById('boite');
      elTable = document.getElementById('table');
      elSvg = document.getElementById('traits');
      elJetons = document.getElementById('jetons');
      enVol = []; attente = [];
      window.addEventListener('resize', () => { if (scene) { dessinerTraits(); poserJetons(); } });
      document.addEventListener('keydown', (e) => {
        if (e.key !== ' ' || e.target.closest('input,button,select')) return;
        const b = elBoite.querySelector('.continuer');
        if (b) { e.preventDefault(); b.click(); }
      });
    },
    lancer,
  };
})();
