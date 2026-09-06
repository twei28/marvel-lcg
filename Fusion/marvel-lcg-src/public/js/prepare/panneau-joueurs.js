// panneau-joueurs.js — bouton « 👥 Joueurs & tchat » sur l'écran de
// préparation, qui
// ouvre la liste des titulaires de compte, le tchat général et les tchats
// privés. Le panneau se déplace à la souris et retient sa place.
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
// réservées au siège 0, et une conversation privée n'est servie qu'à ses deux
// participants. Un invité qui lirait ce fichier n'y gagne rien.

(function () {
  'use strict';

  var LANGUE = (function () {
    try { return localStorage.getItem('marvel-langue') === 'en' ? 'en' : 'fr'; }
    catch (e) { return 'fr'; }
  })();
  var DICO_EN_LOCAL = {
    // « Joueurs » seul se lisait comme un reglage du nombre de heros, juste
    // sous les tuiles de mode. Le libelle nomme donc les DEUX choses que le
    // panneau contient : qui est connecte, et de quoi leur ecrire.
    'Joueurs & tchat': 'Players & chat',
    'Qui est connecté, et le tchat': 'Who is connected, and the chat',
    'Général': 'General',
    'Tout le monde': 'Everyone',
    'Personne d’autre pour l’instant.': 'Nobody else yet.',
    'Écris un message…': 'Write a message…',
    'Message privé à': 'Private message to',
    'Envoyer': 'Send',
    'en partie': 'in a game',
    'en ligne': 'online',
    'jamais venu': 'never came',
    'toi': 'you'
  };
  function t(fr) {
    return LANGUE === 'en' && Object.prototype.hasOwnProperty.call(DICO_EN_LOCAL, fr)
      ? DICO_EN_LOCAL[fr] : fr;
  }

  var CLE_POS = 'marvel-pj-position';
  var CLE_VU = 'marvel-pj-prives-vus';
  var RYTHME_OUVERT = 5000;    // le tchat doit paraître vivant
  var RYTHME_FERME = 60000;    // simple signe de vie : « je suis en ligne »

  function lireJSON(cle, defaut) {
    try {
      var brut = localStorage.getItem(cle);
      return brut ? JSON.parse(brut) : defaut;
    } catch (e) { return defaut; }
  }
  function ecrireJSON(cle, valeur) {
    try { localStorage.setItem(cle, JSON.stringify(valeur)); } catch (e) { /* tant pis */ }
  }

  var etat = {
    ouvert: false,
    moi: '',
    conv: '',                    // '' = général, sinon le pseudo du correspondant
    fils: { '': { messages: [], dernier: 0 } },
    joueurs: [],
    prives: {},                  // pseudo -> id du dernier message échangé
    vus: lireJSON(CLE_VU, {}),   // pseudo -> id déjà affiché
    minuteur: null
  };
  var panneau = null, listeEl = null, filEl = null, champEl = null, envoyerEl = null;

  function fil(conv) {
    if (!etat.fils[conv]) etat.fils[conv] = { messages: [], dernier: 0 };
    return etat.fils[conv];
  }

  function styles() {
    var style = document.createElement('style');
    style.textContent =
      // ⚠ CETTE REGLE EST INDISPENSABLE. `display: flex` ci-dessous est une
      // regle d'AUTEUR : elle bat le `[hidden] { display: none }` de la
      // feuille du navigateur, qui n'est qu'une regle d'agent utilisateur. Sans
      // cette ligne, le panneau restait affiche quoi qu'on fasse du bouton.
      '.pj-panneau[hidden] { display: none !important; }' +
      '.pj-panneau { position: fixed; top: 124px; right: 12px; z-index: 901;' +
      ' width: 320px; max-width: calc(100vw - 24px); max-height: 70vh;' +
      ' display: flex; flex-direction: column; border: 1px solid #666;' +
      ' border-radius: 10px; background: #1c1c1c; color: #ddd;' +
      ' box-shadow: 0 10px 30px rgba(0,0,0,.5); font-size: .85rem; }' +
      '.pj-titre { display: flex; justify-content: space-between; align-items: center;' +
      ' gap: 8px; padding: 9px 12px; border-bottom: 1px solid #333; font-weight: 700;' +
      ' cursor: move; user-select: none; }' +
      '.pj-fermer { background: none; border: 0; color: #999; cursor: pointer;' +
      ' font-size: 1rem; padding: 0 2px; }' +
      '.pj-fermer:hover { color: #fff; }' +
      '.pj-liste { list-style: none; margin: 0; padding: 6px 0; max-height: 30vh;' +
      ' overflow-y: auto; border-bottom: 1px solid #333; }' +
      '.pj-liste li { display: flex; align-items: center; gap: 8px; padding: 4px 12px;' +
      ' cursor: pointer; }' +
      '.pj-liste li:hover { background: rgba(255,255,255,.06); }' +
      '.pj-liste li.sel { background: rgba(255,212,90,.14); }' +
      '.pj-point { width: 8px; height: 8px; border-radius: 50%; flex: none;' +
      ' background: #555; }' +
      '.pj-point.partie { background: #e0a020; }' +
      '.pj-point.ligne { background: #3fb950; }' +
      '.pj-point.general { background: #6ea8fe; }' +
      '.pj-nom { font-weight: 700; }' +
      '.pj-etat { color: #8b8b8b; font-size: .78rem; margin-left: auto; }' +
      '.pj-neuf { width: 7px; height: 7px; border-radius: 50%; background: #f85149;' +
      ' flex: none; margin-left: 6px; }' +
      '.pj-vide { color: #8b8b8b; padding: 6px 12px; cursor: default; }' +
      '.pj-vide:hover { background: none; }' +
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

  /* ---------------- Déplacement ---------------- */

  function poser(x, y) {
    // On borne dans la fenêtre : une position enregistrée sur grand écran ne
    // doit pas rendre le panneau inatteignable sur un petit.
    var large = panneau.offsetWidth || 320;
    var haut = panneau.offsetHeight || 200;
    x = Math.max(0, Math.min(x, window.innerWidth - Math.min(large, window.innerWidth)));
    y = Math.max(0, Math.min(y, Math.max(0, window.innerHeight - 40)));
    panneau.style.left = x + 'px';
    panneau.style.top = y + 'px';
    panneau.style.right = 'auto';
    panneau.style.bottom = 'auto';
  }

  function rendreDeplacable(poignee) {
    var glisse = null;
    poignee.addEventListener('mousedown', function (ev) {
      if (ev.target.closest('.pj-fermer')) return;   // la croix ferme, ne traîne pas
      var boite = panneau.getBoundingClientRect();
      glisse = { dx: ev.clientX - boite.left, dy: ev.clientY - boite.top };
      ev.preventDefault();
    });
    document.addEventListener('mousemove', function (ev) {
      if (!glisse) return;
      poser(ev.clientX - glisse.dx, ev.clientY - glisse.dy);
    });
    document.addEventListener('mouseup', function () {
      if (!glisse) return;
      glisse = null;
      var boite = panneau.getBoundingClientRect();
      ecrireJSON(CLE_POS, { x: boite.left, y: boite.top });
    });
    window.addEventListener('resize', function () {
      var pos = lireJSON(CLE_POS, null);
      if (pos) poser(pos.x, pos.y);
    });
  }

  /* ---------------- Construction ---------------- */

  function construirePanneau() {
    panneau = document.createElement('div');
    panneau.className = 'pj-panneau';
    panneau.hidden = true;

    var titre = document.createElement('div');
    titre.className = 'pj-titre';
    var nom = document.createElement('span');
    nom.textContent = '👥 ' + t('Joueurs & tchat');
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
    envoyerEl = document.createElement('button');
    envoyerEl.type = 'button';
    envoyerEl.textContent = t('Envoyer');
    envoyerEl.addEventListener('click', dire);
    champEl.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { ev.preventDefault(); dire(); }
    });
    saisie.append(champEl, envoyerEl);

    panneau.append(titre, listeEl, filEl, saisie);
    document.body.append(panneau);
    rendreDeplacable(titre);

    var pos = lireJSON(CLE_POS, null);
    if (pos) poser(pos.x, pos.y);
  }

  function dire() {
    var texte = champEl.value.trim();
    if (!texte) return;
    champEl.value = '';
    envoyerEl.disabled = true;
    fetch('/post_salon_message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texte: texte, a: etat.conv })
    }).then(function () { return rafraichir(); })
      .catch(function () { /* message perdu : le champ est déjà vidé */ })
      .then(function () { envoyerEl.disabled = false; champEl.focus(); });
  }

  /* ---------------- Rendu ---------------- */

  function placeholder() {
    champEl.placeholder = etat.conv
      ? t('Message privé à') + ' ' + etat.conv + '…'
      : t('Écris un message…');
  }

  function choisir(conv) {
    etat.conv = conv;
    if (conv && etat.prives[conv]) {
      etat.vus[conv] = etat.prives[conv];
      ecrireJSON(CLE_VU, etat.vus);
    }
    placeholder();
    rendreListe();
    rendreMessages();
    rafraichir();
    champEl.focus();
  }

  function ligneListe(conv, classePoint, libelle, etatTexte, neuf) {
    var li = document.createElement('li');
    if (etat.conv === conv) li.className = 'sel';
    var point = document.createElement('span');
    point.className = 'pj-point ' + classePoint;
    var nom = document.createElement('span');
    nom.className = 'pj-nom';
    nom.textContent = libelle;
    var quoi = document.createElement('span');
    quoi.className = 'pj-etat';
    quoi.textContent = etatTexte;
    li.append(point, nom, quoi);
    if (neuf) {
      var pastille = document.createElement('span');
      pastille.className = 'pj-neuf';
      li.append(pastille);
    }
    li.addEventListener('click', function () { choisir(conv); });
    listeEl.append(li);
  }

  function rendreListe() {
    listeEl.replaceChildren();
    ligneListe('', 'general', t('Général'), t('Tout le monde'), false);
    var autres = 0;
    etat.joueurs.forEach(function (j) {
      if (j.pseudo === etat.moi) {
        ligneListe('', 'ligne', j.pseudo + ' (' + t('toi') + ')', t(j.detail), false);
        return;
      }
      autres += 1;
      var neuf = (etat.prives[j.pseudo] || 0) > (etat.vus[j.pseudo] || 0);
      ligneListe(j.pseudo, j.etat, j.pseudo, t(j.detail), neuf);
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
    fil(etat.conv).messages.forEach(function (m) {
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

  /* ---------------- Va-et-vient ---------------- */

  function rafraichir() {
    var conv = etat.conv;
    var f = fil(conv);
    return fetch('/get_salon_joueurs?depuis=' + f.dernier
                 + '&avec=' + encodeURIComponent(conv)).then(function (r) {
      return r.ok ? r.json() : { actif: false };
    }).then(function (data) {
      if (!data || !data.actif) return;
      etat.moi = data.pseudo || etat.moi;
      etat.joueurs = data.joueurs || [];
      etat.prives = data.prives || {};
      // ⚠ On n'écrase pas le fil : le serveur ne rend que les messages APRÈS
      // `depuis`. Les remplacer viderait la conversation à chaque tour.
      if (data.messages && data.messages.length) {
        f.messages = f.messages.concat(data.messages).slice(-200);
        f.dernier = data.dernier;
        if (conv) { etat.vus[conv] = f.dernier; ecrireJSON(CLE_VU, etat.vus); }
      }
      if (etat.ouvert && conv === etat.conv) { rendreListe(); rendreMessages(); }
    }).catch(function () { /* moteur ou site momentanément muet */ });
  }

  function battre() {
    if (etat.minuteur) clearInterval(etat.minuteur);
    etat.minuteur = setInterval(rafraichir, etat.ouvert ? RYTHME_OUVERT : RYTHME_FERME);
  }

  function basculer(ouvrir) {
    etat.ouvert = !!ouvrir;
    panneau.hidden = !etat.ouvert;
    if (etat.ouvert) { placeholder(); rendreListe(); rendreMessages(); rafraichir(); champEl.focus(); }
    battre();
  }

  // Le bouton n'apparaît que si le site répond : moteur lancé à la main, ou
  // client qui ne tient pas le siège 0, il n'y a rien à montrer.
  fetch('/get_salon_joueurs?depuis=0').then(function (r) {
    return r.ok ? r.json() : { actif: false };
  }).then(function (data) {
    if (!data || !data.actif) return;
    etat.moi = data.pseudo || '';
    etat.joueurs = data.joueurs || [];
    etat.prives = data.prives || {};
    if (data.messages && data.messages.length) {
      fil('').messages = data.messages;
      fil('').dernier = data.dernier;
    }
    styles();
    construirePanneau();
    var bouton = document.createElement('button');
    bouton.type = 'button';
    bouton.textContent = '👥 ' + t('Joueurs & tchat');
    bouton.title = t('Qui est connecté, et le tchat');
    bouton.addEventListener('click', function () { basculer(!etat.ouvert); });
    rangeeBoutons().append(bouton);
    battre();
  }).catch(function () {
    // Route absente (moteur d'une version antérieure) : pas de bouton.
  });
})();
