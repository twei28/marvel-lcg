// lien-admin.js — ajoute les boutons d'administration sur l'écran de
// préparation, quand la partie a été lancée par le site ET que c'est le compte
// administrateur qui joue : « ⚙ Administration » (le site), « 🖼 Relevé des
// illustrations » (la page qui dit qui est dessiné sur chaque carte) et
// « 🎨 Palettes des héros » (la couleur du fond de plateau, corrigée à la main).
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
    'Relevé des illustrations': 'Artwork survey',
    'Dire qui est dessiné sur chaque carte': 'Record who is drawn on each card',
    'Palettes des héros': 'Hero palettes',
    'Corriger la couleur du fond de plateau': 'Fix the board background colour',
    'Voir comme un joueur': 'View as a player',
    'Masquer tous mes accès en plus, comme un compte classique': 'Hide all my extra access, like a regular account',
    'Vue joueur · revenir en admin': 'Player view · back to admin',
    'Tu vois le site comme un compte classique ; clique pour retrouver tes accès': 'You see the site like a regular account; click to get your access back',
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

    // « Voir comme un compte classique » (08/10/2026). Le choix est gardé dans
    // ce navigateur jusqu'au prochain clic ; il est lu par le plateau
    // (ui-app/src/board/essais.ts), les palettes et le relevé. En vue joueur,
    // ce bouton est la SEULE trace des accès en plus : sans lui, pas de retour.
    var CLE_VUE_JOUEUR = 'mc_vue_joueur';
    var vueJoueur = false;
    try { vueJoueur = localStorage.getItem(CLE_VUE_JOUEUR) === 'oui'; } catch (e) { vueJoueur = false; }
    var bascule = document.createElement('button');
    bascule.type = 'button';
    bascule.className = 'bouton-vue-joueur' + (vueJoueur ? ' est-actif' : '');
    bascule.textContent = '👁️ ' + (vueJoueur ? t('Vue joueur · revenir en admin') : t('Voir comme un joueur'));
    bascule.title = vueJoueur
      ? t('Tu vois le site comme un compte classique ; clique pour retrouver tes accès')
      : t('Masquer tous mes accès en plus, comme un compte classique');
    if (vueJoueur) {
      bascule.style.background = '#f0b95f';
      bascule.style.color = '#0d1116';
      bascule.style.borderColor = '#f0b95f';
    }
    bascule.addEventListener('click', function () {
      try {
        if (vueJoueur) localStorage.removeItem(CLE_VUE_JOUEUR);
        else localStorage.setItem(CLE_VUE_JOUEUR, 'oui');
      } catch (e) { /* stockage indisponible : rien ne change */ }
      window.location.reload();
    });
    rangeeBoutons().append(bascule);
    if (vueJoueur) return;

    var bouton = document.createElement('button');
    bouton.type = 'button';
    bouton.textContent = '⚙️ ' + t('Administration');
    bouton.title = t('Comptes et invitations du site');
    bouton.addEventListener('click', function () {
      window.open(url, '_blank', 'noopener');
    });
    var rangee = rangeeBoutons();
    rangee.append(bouton);

    // Le relevé des illustrations. Même condition d'affichage, et même
    // remarque : /save_images_cartes refuse l'écriture (403) à qui n'est pas
    // l'administrateur, quoi que montre ce bouton.
    var releve = document.createElement('button');
    releve.type = 'button';
    releve.textContent = '🖼️ ' + t('Relevé des illustrations');
    releve.title = t('Dire qui est dessiné sur chaque carte');
    releve.addEventListener('click', function () {
      window.open('/releve-images.html', '_blank', 'noopener');
    });
    rangee.append(releve);

    // Les palettes de héros. Même condition d'affichage, même remarque :
    // /save_palette_heros refuse l'écriture (403) à qui n'est pas
    // l'administrateur, quoi que montre ce bouton.
    var palettes = document.createElement('button');
    palettes.type = 'button';
    palettes.textContent = '🎨 ' + t('Palettes des héros');
    palettes.title = t('Corriger la couleur du fond de plateau');
    palettes.addEventListener('click', function () {
      window.open('/palettes-heros.html', '_blank', 'noopener');
    });
    rangee.append(palettes);
  }).catch(function () {
    // Moteur lancé à la main, route absente : pas de bouton, pas d'erreur.
  });
})();
