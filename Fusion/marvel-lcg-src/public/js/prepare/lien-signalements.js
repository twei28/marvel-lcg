// lien-signalements.js — le bouton « 🎫 Mes signalements » sur l'écran de
// préparation, pour TOUT LE MONDE, pas seulement l'administrateur.
//
// Manquait depuis le 16/09/2026 : la page existe côté site, la pastille
// s'affiche quand une réponse attend, mais rien ne permettait d'y aller de
// soi-même. « Une page qu'on ne trouve qu'une fois » disait déjà le code du
// site ; c'était le cas.
//
// ⚠ UNE ADRESSE ABSOLUE, ET C'EST TOUT LE PROBLÈME. La page de jeu est servie
// depuis `pN.<domaine>`, le site depuis `<domaine>` : un lien relatif vers
// `/signalements` tombe sur le MOTEUR, qui sert une image pour tout chemin
// inconnu — un onglet qui s'ouvre sur rien. On demande donc l'adresse au
// moteur (`/get_site_url`, renseignée par l'orchestrateur), et on n'affiche
// le bouton que s'il y en a une : un moteur lancé à la main n'a pas de site
// derrière lui.
//
// Même forme que lien-admin.js : script CLASSIQUE (defer + IIFE), donc pas
// d'import de js/prepare/langue.js ; on duplique la lecture de
// localStorage['marvel-langue'] et un mini dictionnaire local. Il réutilise la
// rangée .reprise-boutons si un autre module l'a déjà créée.

(function () {
  'use strict';

  // La langue passe par langue-classique.js (window.MarvelLangue : choix dans le jeu > cookie du site > navigateur > français).
  var LANGUE = (function () {
    try { return window.MarvelLangue ? window.MarvelLangue.actuelle() : (localStorage.getItem('marvel-langue') === 'en' ? 'en' : 'fr'); }
    catch (e) { return 'fr'; }
  })();
  var DICO_EN_LOCAL = {
    'Mes signalements': 'My reports',
    'Suivre les bugs que tu as signalés': 'Follow the bugs you reported',
  };
  function t(fr) {
    return LANGUE === 'en' && Object.prototype.hasOwnProperty.call(DICO_EN_LOCAL, fr)
      ? DICO_EN_LOCAL[fr] : fr;
  }

  function rangeeBoutons() {
    var rangee = document.querySelector('.reprise-boutons');
    if (rangee) return rangee;
    var style = document.createElement('style');
    style.textContent =
      '.reprise-boutons { display: flex; gap: 8px; align-items: center;' +
      ' flex-wrap: wrap; }' +
      '.reprise-boutons.est-flottante { position: fixed; top: 82px; right: 12px;' +
      ' z-index: 900; justify-content: flex-end; }' +
      '.reprise-boutons button { padding: 7px 13px; border-radius: 8px;' +
      ' border: 1px solid #666; background: #2e2e2e; color: #ddd; font-weight: 700;' +
      ' cursor: pointer; font-size: .85rem; }' +
      '.reprise-boutons button:hover { background: #3d3d3d; }';
    document.head.append(style);
    rangee = document.createElement('div');
    rangee.className = 'reprise-boutons';
    var etapes = document.querySelector('header.progress .steps');
    if (etapes) etapes.parentElement.insertBefore(rangee, etapes);
    else { rangee.classList.add('est-flottante'); document.body.append(rangee); }
    return rangee;
  }

  fetch('/get_site_url').then(function (r) {
    return r.ok ? r.json() : { url: '' };
  }).then(function (data) {
    var url = data && data.url;
    if (!url) return;   // moteur lancé à la main : pas de site, pas de bouton
    var bouton = document.createElement('button');
    bouton.type = 'button';
    bouton.textContent = '🎫 ' + t('Mes signalements');
    bouton.title = t('Suivre les bugs que tu as signalés');
    bouton.addEventListener('click', function () {
      // ⚠ UN NOUVEL ONGLET. Même raison que la pastille : ce bouton s'affiche
      // aussi quand une partie est en cours derrière, et remplacer la page
      // sortirait le joueur de sa table.
      window.open(url.replace(/\/+$/, '') + '/signalements', '_blank', 'noopener');
    });
    rangeeBoutons().append(bouton);
  }).catch(function () {
    // Route absente (moteur d'avant ce bouton) : pas de bouton, pas d'erreur.
  });
})();
