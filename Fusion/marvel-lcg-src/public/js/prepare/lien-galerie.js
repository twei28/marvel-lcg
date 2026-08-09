// lien-galerie.js — ajoute un bouton « 🃏 Galerie » sur l'écran de
// préparation, qui ouvre la galerie de cartes (/galerie.html).
//
// Module autonome, même pattern que reprise.js : script CLASSIQUE (defer +
// IIFE), donc pas d'import de js/prepare/langue.js ; on duplique la lecture
// de localStorage['marvel-langue'] et un mini dictionnaire local. Il réutilise
// la rangée .reprise-boutons si un autre module l'a déjà créée, sinon la crée.

(function () {
  'use strict';

  var LANGUE = (function () {
    try { return localStorage.getItem('marvel-langue') === 'en' ? 'en' : 'fr'; }
    catch (e) { return 'fr'; }
  })();
  var DICO_EN_LOCAL = {
    'Galerie': 'Gallery',
    'Parcourir toutes les cartes du jeu': 'Browse every card in the game',
  };
  function t(fr) {
    return LANGUE === 'en' && Object.prototype.hasOwnProperty.call(DICO_EN_LOCAL, fr)
      ? DICO_EN_LOCAL[fr] : fr;
  }

  var rangee = document.querySelector('.reprise-boutons');
  if (!rangee) {
    // reprise.js n'est pas passé : on crée la rangée et son style minimal
    // (mêmes règles que dans reprise.js, dupliquées sans risque).
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
  }

  var bouton = document.createElement('button');
  bouton.type = 'button';
  bouton.textContent = '\u{1F0CF} ' + t('Galerie');
  bouton.title = t('Parcourir toutes les cartes du jeu');
  bouton.addEventListener('click', function () {
    window.location.href = '/galerie.html';
  });
  rangee.append(bouton);
})();
