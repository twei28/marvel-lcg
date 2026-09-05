// panneau-joueurs.js — bouton « 👥 Joueurs » sur l'écran de préparation, qui
// ouvre la liste des titulaires de compte et leur tchat.
//
// Même pattern que lien-galerie.js et lien-admin.js : script CLASSIQUE
// (defer + IIFE), donc pas d'import de js/prepare/langue.js ; on duplique la
// lecture de localStorage['marvel-langue'] et un mini dictionnaire local.
//
// ⚠ RIEN NE PART VERS LE SITE DEPUIS ICI. Le navigateur est servi depuis
// `p<N>.<domaine>` et le site depuis `<domaine>` : une requête directe serait
// croisée. On parle donc au MOTEUR (/get_salon_joueurs, /post_salon_message),
// qui relaie en 127.0.0.1 avec le jeton de la partie. Le jeton ne descend
// jamais jusqu'ici.
//
// ⚠ C'est le SERVEUR qui décide qui a le droit : ces deux routes sont
// réservées au siège 0. Un invité qui lirait ce fichier n'y gagne rien.

(function () {
  'use strict';

  var LANGUE = (function () {
    try { return localStorage.getItem('marvel-langue') === 'en' ? 'en' : 'fr'; }
    catch (e) { return 'fr'; }
  })();
  var DICO_EN_LOCAL = {
    'Joueurs': 'Players',
    'Qui est là, et le tchat': 'Who is around, and the chat',
    'Personne d’autre pour l’instant.': 'Nobody else yet.',
    'Écris un message…': 'Write a message…',
    'Envoyer': 'Send',
    'en partie': 'in a game',
    'en ligne': 'online',
    'jamais venu': 'never came',
    'Le tchat est indisponible.': 'The chat is unavailable.',
    'toi': 'you'
  };
  function t(fr) {
    return LANGUE === 'en' && Object.prototype.hasOwnProperty.call(DICO_EN_LOCAL, fr)
      ? DICO_EN_LOCAL[fr] : fr;
  }

  // Le site rend « en partie », « en ligne », « jamais venu » ou « vu il y a
  // 3 min ». Les trois premiers se traduisent ; le dernier est composé, on le
  // laisse tel quel plutôt que d'en refaire l'analyse ici.
  function detail(texte) { return t(texte); }

  var RYTHME_OUVERT = 5000;    // le tchat doit paraître vivant
  var RYTHME_FERME = 60000;    // simple signe de vie : « je suis en ligne »

  var etat = { ouvert: false, dernier: 0, moi: '', minuteur: null, messages: [] };
  var panneau = null, listeEl = null, filEl = null, champEl = null, boutonEl = null;

  function styles() {
    var style = document.createElement('style');
    style.textContent =
      '.pj-panneau { position: fixed; top: 124px; right: 12px; z-index: 901;' +
      ' width: 320px; max-width: calc(100vw - 24px); max-height: 70vh;' +
      ' display: flex; flex-direction: column; border: 1px solid #666;' +
      ' border-radius: 10px; background: #1c1c1c; color: #ddd;' +
      ' box-shadow: 0 10px 30px rgba(0,0,0,.5); font-size: .85rem; }' +
      '.pj-titre { display: flex; justify-content: space-between; align-items: center;' +
      ' gap: 8px; padding: 9px 12px; border-bottom: 1px solid #333; font-weight: 700; }' +
      '.pj-fermer { background: none; border: 0; color: #999; cursor: pointer;' +
      ' font-size: 1rem; padding: 0 2px; }' +
      '.pj-fermer:hover { color: #fff; }' +
      '.pj-liste { list-style: none; margin: 0; padding: 8px 12px; max-height: 30vh;' +
      ' overflow-y: auto; border-bottom: 1px solid #333; }' +
      '.pj-liste li { display: flex; align-items: center; gap: 8px; padding: 3px 0; }' +
      '.pj-point { width: 8px; height: 8px; border-radius: 50%; flex: none;' +
      ' background: #555; }' +
      '.pj-point.partie { background: #e0a020; }' +
      '.pj-point.ligne { background: #3fb950; }' +
      '.pj-nom { font-weight: 700; }' +
      '.pj-etat { color: #8b8b8b; font-size: .78rem; margin-left: auto; }' +
      '.pj-vide { color: #8b8b8b; padding: 8px 12px; }' +
      '.pj-fil { flex: 1 1 auto; overflow-y: auto; padding: 8px 12px;' +
      ' display: flex; flex-direction: column; gap: 5px; min-height: 90px; }' +
      '.pj-msg { line-height: 1.35; word-wrap: break-word; overflow-wrap: anywhere; }' +
      '.pj-msg b { color: #ffd45a; }' +
      '.pj-msg.moi b { color: #6ea8fe; }' +
      '.pj-msg span { color: #6e6e6e; font-size: .72rem; margin-left: 4px; }' +
      '.pj-saisie { display: flex; gap: 6px; padding: 8px 12px; border-top: 1px solid #333; }' +
      '.pj-saisie input { flex: 1 1 auto; min-width: 0; font: inherit; color: inherit;' +
      ' background: #111; border: 1px solid #444; border-radius: 6px; padding: 6px 9px; }' +
      '.pj-saisie button { font: inherit; font-weight: 700; color: #1c1c1c;' +
      ' background: #ffd45a; border: 0; border-radius: 6px; padding: 6px 12px;' +
      ' cursor: pointer; }' +
      '.pj-saisie button:disabled { opacity: .5; cursor: default; }';
    document.head.append(style);
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

  function construirePanneau() {
    panneau = document.createElement('div');
    panneau.className = 'pj-panneau';
    panneau.hidden = true;

    var titre = document.createElement('div');
    titre.className = 'pj-titre';
    var nom = document.createElement('span');
    nom.textContent = '👥 ' + t('Joueurs');
    var fermer = document.createElement('button');
    fermer.className = 'pj-fermer';
    fermer.type = 'button';
    fermer.textContent = '✕';
    fermer.addEventListener('click', function () { basculer(false); });
    titre.append(nom, fermer);

    listeEl = document.createElement('ul');
    listeEl.className = 'pj-liste';

    filEl = document.createElement('div');
    filEl.className = 'pj-fil';

    var saisie = document.createElement('div');
    saisie.className = 'pj-saisie';
    champEl = document.createElement('input');
    champEl.type = 'text';
    champEl.maxLength = 500;
    champEl.placeholder = t('Écris un message…');
    var envoyer = document.createElement('button');
    envoyer.type = 'button';
    envoyer.textContent = t('Envoyer');
    function dire() {
      var texte = champEl.value.trim();
      if (!texte) return;
      champEl.value = '';
      envoyer.disabled = true;
      fetch('/post_salon_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texte: texte })
      }).then(function () { return rafraichir(); })
        .catch(function () { /* message perdu : le champ est déjà vidé */ })
        .then(function () { envoyer.disabled = false; champEl.focus(); });
    }
    envoyer.addEventListener('click', dire);
    champEl.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { ev.preventDefault(); dire(); }
    });
    saisie.append(champEl, envoyer);

    panneau.append(titre, listeEl, filEl, saisie);
    document.body.append(panneau);
  }

  function rendreListe(joueurs) {
    listeEl.replaceChildren();
    var autres = 0;
    (joueurs || []).forEach(function (j) {
      if (j.pseudo !== etat.moi) autres += 1;
      var li = document.createElement('li');
      var point = document.createElement('span');
      point.className = 'pj-point ' + j.etat;
      var nom = document.createElement('span');
      nom.className = 'pj-nom';
      nom.textContent = j.pseudo + (j.pseudo === etat.moi ? ' (' + t('toi') + ')' : '');
      var quoi = document.createElement('span');
      quoi.className = 'pj-etat';
      quoi.textContent = detail(j.detail);
      li.append(point, nom, quoi);
      listeEl.append(li);
    });
    if (!autres) {
      var vide = document.createElement('li');
      vide.className = 'pj-vide';
      vide.textContent = t('Personne d’autre pour l’instant.');
      listeEl.append(vide);
    }
  }

  function rendreMessages() {
    filEl.replaceChildren();
    etat.messages.forEach(function (m) {
      var ligne = document.createElement('div');
      ligne.className = 'pj-msg' + (m.pseudo === etat.moi ? ' moi' : '');
      var qui = document.createElement('b');
      qui.textContent = m.pseudo + ' : ';
      var quand = document.createElement('span');
      quand.textContent = m.quand;
      ligne.append(qui, document.createTextNode(m.texte), quand);
      filEl.append(ligne);
    });
    filEl.scrollTop = filEl.scrollHeight;
  }

  function rafraichir() {
    return fetch('/get_salon_joueurs?depuis=' + etat.dernier).then(function (r) {
      return r.ok ? r.json() : { actif: false };
    }).then(function (data) {
      if (!data || !data.actif) return;
      etat.moi = data.pseudo || etat.moi;
      // ⚠ On n'ecrase pas le fil : le serveur ne rend que les messages APRES
      // `depuis`. Les remplacer viderait la conversation a chaque tour.
      if (data.messages && data.messages.length) {
        etat.messages = etat.messages.concat(data.messages).slice(-200);
        etat.dernier = data.dernier;
      }
      if (etat.ouvert) { rendreListe(data.joueurs); rendreMessages(); }
    }).catch(function () { /* moteur ou site momentanément muet */ });
  }

  function battre() {
    if (etat.minuteur) clearInterval(etat.minuteur);
    etat.minuteur = setInterval(rafraichir, etat.ouvert ? RYTHME_OUVERT : RYTHME_FERME);
  }

  function basculer(ouvrir) {
    etat.ouvert = !!ouvrir;
    panneau.hidden = !etat.ouvert;
    if (etat.ouvert) { rafraichir(); champEl.focus(); }
    battre();
  }

  // Le bouton n'apparaît que si le site répond : moteur lancé à la main, ou
  // client qui ne tient pas le siège 0, il n'y a rien à montrer.
  fetch('/get_salon_joueurs?depuis=0').then(function (r) {
    return r.ok ? r.json() : { actif: false };
  }).then(function (data) {
    if (!data || !data.actif) return;
    etat.moi = data.pseudo || '';
    if (data.messages && data.messages.length) {
      etat.messages = data.messages;
      etat.dernier = data.dernier;
    }
    styles();
    construirePanneau();
    boutonEl = document.createElement('button');
    boutonEl.type = 'button';
    boutonEl.textContent = '👥 ' + t('Joueurs');
    boutonEl.title = t('Qui est là, et le tchat');
    boutonEl.addEventListener('click', function () { basculer(!etat.ouvert); });
    rangeeBoutons().append(boutonEl);
    battre();
  }).catch(function () {
    // Route absente (moteur d'une version antérieure) : pas de bouton.
  });
})();
