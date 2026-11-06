// discord.js — ajoute le bouton Discord sur l'écran de préparation, dans la
// rangée d'icônes de l'en-tête (06/11/2026, demande de l'utilisateur : « pas
// assez visible » en simple lien dans le pied de page).
//
// Même pattern que lien-galerie.js : script CLASSIQUE (defer + IIFE), donc
// pas d'import de js/prepare/langue.js ; on duplique la lecture de
// localStorage['marvel-langue'] et un mini dictionnaire local. Il réutilise
// la rangée .reprise-boutons si un autre module l'a déjà créée.
//
// ⚠ ICÔNE EN IMAGE, PAS EN FONT AWESOME (icones-entete.js) : la Font Awesome
// 4.7 déjà chargée sur le site n'a pas d'icône Discord (ajoutée seulement en
// FA5). Le bouton porte donc déjà sa classe « btn-icone » et son
// `dataset.iconise = "1"` : icones-entete.js (qui observe la rangée et
// convertit chaque nouveau bouton) le voit déjà fait et ne le touche pas.

(function () {
  'use strict';

  // La langue passe par langue-classique.js (window.MarvelLangue : choix dans le jeu > cookie du site > navigateur > français).
  var LANGUE = (function () {
    try { return window.MarvelLangue ? window.MarvelLangue.actuelle() : (localStorage.getItem('marvel-langue') === 'en' ? 'en' : 'fr'); }
    catch (e) { return 'fr'; }
  })();
  var DICO_EN_LOCAL = {
    'Discord : surtout en français, mais on parle aussi anglais': 'Discord: mostly French, but English is spoken too',
  };
  function t(fr) {
    return LANGUE === 'en' && Object.prototype.hasOwnProperty.call(DICO_EN_LOCAL, fr)
      ? DICO_EN_LOCAL[fr] : fr;
  }

  var rangee = document.querySelector('.reprise-boutons');
  if (!rangee) {
    // reprise.js n'est pas passé : on crée la rangée et son style minimal
    // (mêmes règles que dans reprise.js/lien-galerie.js, dupliquées sans risque).
    var style = document.createElement('style');
    style.textContent =
      '.reprise-boutons { display: flex; gap: 8px; align-items: center;' +
      ' flex-wrap: wrap; }' +
      '.reprise-boutons.est-flottante { position: fixed; top: 82px; right: 12px;' +
      ' z-index: 900; justify-content: flex-end; }';
    document.head.append(style);
    rangee = document.createElement('div');
    rangee.className = 'reprise-boutons';
    var etapes = document.querySelector('header.progress .steps');
    if (etapes) etapes.parentElement.insertBefore(rangee, etapes);
    else { rangee.classList.add('est-flottante'); document.body.append(rangee); }
  }

  var bouton = document.createElement('a');
  bouton.href = 'https://discord.gg/AzHwxSnVa';
  bouton.target = '_blank';
  bouton.rel = 'noopener';
  bouton.className = 'btn-icone';
  bouton.dataset.iconise = '1';
  bouton.title = t('Discord : surtout en français, mais on parle aussi anglais');
  bouton.setAttribute('aria-label', t('Discord : surtout en français, mais on parle aussi anglais'));

  var logo = document.createElement('img');
  logo.src = '/public/img/discord.webp';
  logo.alt = '';
  logo.width = 20;
  logo.height = 20;
  logo.style.cssText = 'display:block;border-radius:50%;';

  var libelle = document.createElement('span');
  libelle.className = 'rb-libelle';
  libelle.textContent = 'Discord';

  bouton.append(logo, libelle);
  rangee.append(bouton);
})();
