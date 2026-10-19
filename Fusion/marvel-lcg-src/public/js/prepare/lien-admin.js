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
    'Sauvegarde du code': 'Code backup',
    'Télécharger tout le projet sans les images (5 dernières sauvegardes)': 'Download the whole project without images (last 5 backups)',
    'Masquer tous mes accès en plus, comme un compte classique ; la langue, l’affichage et la phase du méchant seront redemandés': 'Hide all my extra access, like a regular account; language, display and villain phase will be asked again',
    'Tu vois le site comme un compte classique ; clique pour retrouver tes accès et tes réglages': 'You see the site like a regular account; click to get your access and settings back',
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
    // Libellés fixes, quelle que soit la langue (demande du 08/10/2026) : le
    // bouton dit OÙ il mène, « Player » depuis l'admin, « Admin » depuis Player.
    bascule.textContent = vueJoueur ? 'Admin' : 'Player';
    bascule.title = vueJoueur
      ? t('Tu vois le site comme un compte classique ; clique pour retrouver tes accès et tes réglages')
      : t('Masquer tous mes accès en plus, comme un compte classique ; la langue, l’affichage et la phase du méchant seront redemandés');
    if (vueJoueur) {
      bascule.style.background = '#f0b95f';
      bascule.style.color = '#0d1116';
      bascule.style.borderColor = '#f0b95f';
    }
    // LES TROIS FENÊTRES DU PREMIER LANCEMENT (langue, affichage, phase du
    // méchant) se rouvrent à chaque passage en Player, comme pour un nouveau
    // joueur ; leurs réponses ne valent que pour la vue Player : les réglages
    // de l'admin sont mis de côté ici et reviennent au retour en Admin. Le
    // compte n'est ni lu ni écrit pour l'affichage pendant la vue Player
    // (affichage.js et ui-app/src/board/affichage.ts).
    var CLE_REGLAGES_ADMIN = 'mc_vue_joueur_reglages_admin';
    var CLES_DU_PREMIER_LANCEMENT = [
      'marvel-langue', 'marvel-langue-choisie', 'marvel-board-scans-fr',
      'mc_affichage_v1', 'marvel-board-mode-phase-mechant', 'mc_phase_mode_vu_v1',
      'mc_phase_presentation', 'mc_phase_trois_choix_migre',
    ];
    bascule.addEventListener('click', function () {
      try {
        if (vueJoueur) {
          var mis = JSON.parse(localStorage.getItem(CLE_REGLAGES_ADMIN) || '{}');
          CLES_DU_PREMIER_LANCEMENT.forEach(function (cle) {
            if (typeof mis[cle] === 'string') localStorage.setItem(cle, mis[cle]);
            else localStorage.removeItem(cle);
          });
          localStorage.removeItem(CLE_REGLAGES_ADMIN);
          localStorage.removeItem(CLE_VUE_JOUEUR);
        } else {
          var aGarder = {};
          CLES_DU_PREMIER_LANCEMENT.forEach(function (cle) {
            var valeur = localStorage.getItem(cle);
            if (valeur !== null) aGarder[cle] = valeur;
            localStorage.removeItem(cle);
          });
          localStorage.setItem(CLE_REGLAGES_ADMIN, JSON.stringify(aGarder));
          localStorage.setItem(CLE_VUE_JOUEUR, 'oui');
        }
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

    // La sauvegarde du code (08/10/2026) : la page du SITE qui liste les 5
    // derniers zips, reservee a l'administrateur par le site lui-meme.
    var sauvegarde = document.createElement('button');
    sauvegarde.type = 'button';
    sauvegarde.textContent = '💾 ' + t('Sauvegarde du code');
    sauvegarde.title = t('Télécharger tout le projet sans les images (5 dernières sauvegardes)');
    sauvegarde.addEventListener('click', function () {
      window.open(url.replace(/\/admin\/?$/, '') + '/admin/sauvegardes', '_blank', 'noopener');
    });
    rangee.append(sauvegarde);
  }).catch(function () {
    // Moteur lancé à la main, route absente : pas de bouton, pas d'erreur.
  });
})();
