// annonce.js — le preavis du site, en haut de l'assistant de preparation.
//
// Pourquoi ce fichier existe : un deploiement fait `systemctl restart narwhal`,
// l'orchestrateur du site emporte tous ses moteurs, et TOUTE PARTIE EN COURS
// EST PERDUE. Le plateau a son propre bandeau (ui-app/src/board/annonce.ts) ;
// celui-ci sert l'autre moitie du besoin : ne pas laisser quelqu'un LANCER une
// partie qui va mourir dans trois minutes.
//
// Module AUTONOME, sur le modele de reprise.js : script classique (defer +
// IIFE), aucune dependance a app.js, ses styles avec lui. Il n'entre pas dans
// le cycle de rendu du wizard — il se pose sur `document.body` et s'efface
// tout seul. Un ecran de preparation qui se redessine ne le derange pas.
//
// ⚠ DEUX HORLOGES. Le serveur envoie les SECONDES QUI RESTENT, jamais une
// heure de fin : le navigateur d'un joueur peut avoir plusieurs minutes
// d'ecart avec celle du serveur. On note l'instant LOCAL de la reponse et on
// decompte a partir de la.
(function () {
  'use strict';

  // Toutes les 30 s : un preavis de dix minutes doit etre vu, pas rate de peu.
  const PERIODE_MS = 30000;

  // Mini t() local, meme contrat que reprise.js : ce fichier n'est pas un
  // module ES et ne peut pas importer langue.js.
  // La langue passe par langue-classique.js (window.MarvelLangue : choix dans le jeu > cookie du site > navigateur > français).
  const EN = (function () {
    try { return window.MarvelLangue ? window.MarvelLangue.actuelle() === 'en' : localStorage.getItem('marvel-langue') === 'en'; }
    catch (e) { return false; }
  })();
  function delaiLisible(secondes) {
    const minutes = Math.floor(Math.max(0, secondes) / 60);
    // Jamais « 0 minute », qui se lirait comme « c'est deja fini » alors qu'il
    // reste le temps de faire quelque chose.
    if (minutes < 1) return EN ? 'less than a minute' : "moins d'une minute";
    if (minutes === 1) return EN ? '1 minute' : '1 minute';
    return minutes + (EN ? ' minutes' : ' minutes');
  }

  const style = document.createElement('style');
  style.textContent = `
    .annonce-site {
      position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
      z-index: 9000; display: flex; align-items: center; gap: 10px;
      max-width: min(640px, calc(100vw - 24px)); padding: 8px 16px;
      border: 1px solid #f2665a; border-radius: 10px;
      background: linear-gradient(180deg, rgba(46,16,14,.98), rgba(24,10,9,.98));
      box-shadow: 0 8px 30px rgba(0,0,0,.55);
      font: 14px/1.4 system-ui, sans-serif;
    }
    .annonce-site-delai {
      flex: none; padding: 2px 10px; font-size: .78rem; font-weight: 800;
      color: #2b0f0d; background: #f2665a; border-radius: 99px; white-space: nowrap;
    }
    .annonce-site-texte { color: #f6c9c4; font-size: .85rem; }
  `;
  document.head.appendChild(style);

  let bandeau = null;
  let texte = '';
  let secondes = 0;
  let recuA = 0;

  function dessiner() {
    const restant = secondes - Math.floor((Date.now() - recuA) / 1000);
    if (!texte || restant <= 0) {
      if (bandeau) { bandeau.remove(); bandeau = null; }
      return;
    }
    if (!bandeau) {
      bandeau = document.createElement('div');
      bandeau.className = 'annonce-site';
      bandeau.setAttribute('role', 'alert');
      bandeau.innerHTML = '<span class="annonce-site-delai"></span>'
                        + '<span class="annonce-site-texte"></span>';
      document.body.appendChild(bandeau);
    }
    bandeau.querySelector('.annonce-site-delai').textContent = delaiLisible(restant);
    bandeau.querySelector('.annonce-site-texte').textContent = texte;
  }

  async function demander() {
    try {
      const r = await fetch('/get_annonce', { cache: 'no-store' });
      if (!r.ok) throw new Error(r.status);
      const j = await r.json();
      texte = String((j && j.texte) || '').trim();
      secondes = Number((j && j.secondes) || 0);
      recuA = Date.now();
    } catch (e) {
      // Moteur muet, partie locale sans site derriere, reseau coupe : on se
      // tait. Rien ici ne doit gener la preparation d'une partie.
      texte = '';
      secondes = 0;
    }
    dessiner();
  }

  demander();
  setInterval(demander, PERIODE_MS);
  setInterval(dessiner, 1000);
})();
