// maj.js — « Une mise à jour du jeu est arrivée », sur l'écran de préparation.
//
// ⚠ POURQUOI CE FICHIER EXISTE, ET C'EST UNE REMARQUE DE L'UTILISATEUR.
// Après un déploiement, un onglet resté ouvert garde le JavaScript qu'il a
// chargé, indéfiniment. Les empreintes anti-cache (`?v=…`) ne servent qu'au
// PROCHAIN chargement de la page : elles ne réveillent personne.
//
// Constaté en production le 16/09/2026 : un onglet interrogeait encore le
// serveur toutes les deux secondes, des heures après le déploiement du
// correctif qui espace ces appels. Ma réponse avait été « pense à recharger ta
// page ». Réponse de l'utilisateur : « je n'ai pas pensé à ça, les autres
// joueurs ne vont pas y penser ».
//
// ⚠ AUCUN CHANGEMENT CÔTÉ SERVEUR. La page relit SON PROPRE HTML et compare
// l'empreinte de son script principal à celle qu'elle a chargée. Le
// déploiement recalcule cette empreinte depuis le contenu
// (`ui-app/deployer.sh`) : elle change si et seulement si le code a changé.
//
// Module AUTONOME, sur le modèle de annonce.js et messages.js : script
// classique (defer + IIFE), aucune dépendance à app.js, ses styles avec lui.
(function () {
  'use strict';

  // Toutes les cinq minutes : un déploiement n'est pas une urgence, et on vient
  // justement de réduire le bavardage de cet écran avec le serveur.
  const PERIODE_MS = 300000;

  const EN = (function () {
    try { return localStorage.getItem('marvel-langue') === 'en'; }
    catch (e) { return false; }
  })();
  const T = {
    arrivee: EN ? 'A game update has arrived.' : 'Une mise à jour du jeu est arrivée.',
    recharger: EN ? 'Reload' : 'Recharger',
  };

  /** L'empreinte citée par un HTML, ou '' si on ne sait pas la lire. */
  function empreinteDe(texte) {
    const requete = texte.match(/app\.js\?v=([A-Za-z0-9.]+)/);
    return requete ? requete[1] : '';
  }

  const chargee = empreinteDe(document.documentElement.innerHTML);
  // ⚠ ON NE FAIT RIEN QUAND ON NE SAIT PAS. Sans empreinte lisible, toute
  // comparaison serait un coup de dé, et proposer un rechargement ferait
  // tourner le joueur en rond sans rien corriger.
  if (!chargee) return;

  const style = document.createElement('style');
  style.textContent = `
    .maj-bandeau {
      position: fixed; left: 50%; bottom: 14px; transform: translateX(-50%);
      z-index: 9000; display: flex; align-items: center; gap: 12px;
      padding: 8px 14px; border: 2px solid #f0b429; border-radius: 10px;
      background: linear-gradient(180deg, rgba(40,32,6,.97), rgba(24,19,4,.97));
      color: #f6e3b4; font: 14px/1.3 system-ui, sans-serif;
      box-shadow: 0 8px 30px rgba(0,0,0,.55);
    }
    .maj-bandeau button {
      font: inherit; padding: 4px 12px; border: 2px solid #f0b429;
      border-radius: 6px; background: transparent; color: #fff; cursor: pointer;
    }
    .maj-bandeau button:hover { background: rgba(240,180,41,.18); }
  `;
  document.head.appendChild(style);

  let pose = false;
  function poser() {
    if (pose) return;
    pose = true;
    const bandeau = document.createElement('div');
    bandeau.className = 'maj-bandeau';
    bandeau.setAttribute('role', 'status');
    const texte = document.createElement('span');
    texte.textContent = T.arrivee;
    const bouton = document.createElement('button');
    bouton.type = 'button';
    bouton.textContent = T.recharger;
    bouton.addEventListener('click', function () { location.reload(); });
    bandeau.append(texte, bouton);
    document.body.appendChild(bandeau);
  }

  async function verifier() {
    if (pose || document.hidden) return;
    try {
      // ⚠ `no-store` : sans cela le navigateur rendrait la copie qu'il a déjà,
      // c'est-à-dire exactement celle qu'on cherche à dépasser.
      const reponse = await fetch(location.pathname, { cache: 'no-store' });
      if (!reponse.ok) return;
      const servie = empreinteDe(await reponse.text());
      if (servie && servie !== chargee) poser();
    } catch (e) {
      // Réseau coupé, serveur qui redémarre : on se tait. Ce n'est pas le
      // moment de réclamer un rechargement.
    }
  }

  // ⚠ AUSSI AU RETOUR SUR L'ONGLET : quelqu'un qui revient après deux heures ne
  // doit pas attendre cinq minutes de plus pour l'apprendre, et c'est
  // justement le moment où il va se remettre à jouer.
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) void verifier();
  });
  setInterval(verifier, PERIODE_MS);
  void verifier();
})();
