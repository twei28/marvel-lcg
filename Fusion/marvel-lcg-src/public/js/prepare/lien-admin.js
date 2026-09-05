// lien-admin.js — ajoute un bouton « ⚙ Administration » sur l'écran de
// préparation, quand la partie a été lancée par le site ET que c'est le compte
// administrateur qui joue.
//
// Même pattern que lien-galerie.js : script CLASSIQUE (defer + IIFE), donc pas
// d'import de js/prepare/langue.js ; on duplique la lecture de
// localStorage['marvel-langue'] et un mini dictionnaire local. Il réutilise la
// rangée .reprise-boutons si un autre module l'a déjà créée.
//
// ⚠ C'est le SERVEUR qui décide, jamais ce script : /get_site_admin ne rend une
// adresse que si `site_admin_url` est configurée (l'orchestrateur ne la met que
// pour la partie de l'administrateur) et que le client tient le siège 0. Un
// invité qui lirait ce fichier n'y gagne rien.

(function () {
  'use strict';

  var LANGUE = (function () {
    try { return localStorage.getItem('marvel-langue') === 'en' ? 'en' : 'fr'; }
    catch (e) { return 'fr'; }
  })();
  var DICO_EN_LOCAL = {
    'Administration': 'Admin',
    'Comptes et invitations du site': 'Site accounts and invitations',
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

  fetch('/get_site_admin').then(function (r) {
    return r.ok ? r.json() : { url: '' };
  }).then(function (data) {
    var url = data && data.url;
    if (!url) return;   // pas de site devant, ou pas l'administrateur
    var bouton = document.createElement('button');
    bouton.type = 'button';
    bouton.textContent = '⚙️ ' + t('Administration');
    bouton.title = t('Comptes et invitations du site');
    bouton.addEventListener('click', function () {
      window.open(url, '_blank', 'noopener');
    });
    rangeeBoutons().append(bouton);
  }).catch(function () {
    // Moteur lancé à la main, route absente : pas de bouton, pas d'erreur.
  });
})();
