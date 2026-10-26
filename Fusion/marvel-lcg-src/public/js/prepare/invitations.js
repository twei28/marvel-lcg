// invitations.js — « Arnaud t'invite à sa partie · Rejoindre / Refuser ».
//
// Demande de l'utilisateur, 13/10/2026 : l'hôte invite d'un clic quelqu'un de
// connecté, et l'invité voit l'invitation sur n'importe quelle page du site.
// Décisions : .planning/todos/2026-10-13-inviter-un-connecte.md.
//
// Module AUTONOME, sur le modèle de messages.js : script classique (defer +
// IIFE), aucune dépendance à app.js, ses styles avec lui. À poser sur toute
// page que le titulaire du compte ouvre sur SA table (préparation, deck
// builder, campagnes...). Le moteur ne répond qu'au siège 0 : sur la table
// d'un autre, ce module se tait.
//
// ⚠ IL SE TAIT AUSSI QUAND L'ONGLET EST CACHÉ, et ce n'est pas une économie :
// côté site, ce sondage vaut SIGNE DE VIE (« connecté » = une page ouverte
// sous ses yeux). Un onglet oublié derrière les autres ne doit pas faire
// apparaître son propriétaire dans la liste de l'hôte.
(function () {
  'use strict';

  const PERIODE_MS = 8000;

  // La langue passe par langue-classique.js (window.MarvelLangue : choix dans le jeu > cookie du site > navigateur > français).
  const EN = (function () {
    try { return window.MarvelLangue ? window.MarvelLangue.actuelle() === 'en' : localStorage.getItem('marvel-langue') === 'en'; }
    catch (e) { return false; }
  })();
  const T = {
    invite: EN ? 'invites you to their game' : 't’invite à sa partie',
    // « Joueur 2 », comme l'hôte le lit dans sa préparation (le siège 1).
    siege: EN ? 'Player' : 'Joueur',
    rejoindre: EN ? 'Join' : 'Rejoindre',
    refuser: EN ? 'Decline' : 'Refuser',
    expiree: EN ? 'This invitation has expired.' : 'Cette invitation a expiré.',
  };

  const style = document.createElement('style');
  style.textContent = `
    .inv-fenetre {
      position: fixed; right: 14px; top: 14px; z-index: 9100;
      display: flex; flex-direction: column; gap: 10px; max-width: min(360px, calc(100vw - 28px));
      padding: 12px 14px; border: 2px solid #f0b95f; border-radius: 10px;
      background: linear-gradient(180deg, rgba(40,30,10,.98), rgba(24,18,6,.98));
      box-shadow: 0 8px 30px rgba(0,0,0,.6);
      font: 14px/1.35 system-ui, sans-serif; color: #f5e3bd;
    }
    .inv-fenetre b { color: #fff; }
    .inv-fenetre small { opacity: .75; }
    .inv-boutons { display: flex; gap: 8px; justify-content: flex-end; }
    .inv-boutons button {
      min-height: 34px; padding: 6px 16px; border-radius: 6px; cursor: pointer;
      font: 700 13px system-ui, sans-serif; border: 1px solid #f0b95f;
    }
    .inv-oui { background: #f0b95f; color: #1b1405; }
    .inv-non { background: transparent; color: #f5e3bd; }
  `;
  document.head.appendChild(style);

  let fenetre = null;
  let affichee = '';
  let occupe = false;

  function fermer() {
    if (fenetre) fenetre.remove();
    fenetre = null;
    affichee = '';
  }

  async function repondre(inv, oui) {
    if (occupe) return;
    occupe = true;
    try {
      const reponse = await fetch('/post_invitation_reponse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: inv.id, oui }),
      });
      const brut = reponse.ok ? await reponse.json() : null;
      if (oui && brut && brut.lien) {
        location.href = brut.lien;
        return;
      }
      if (oui) {
        const texte = fenetre && fenetre.querySelector('small');
        if (texte) texte.textContent = T.expiree;
        setTimeout(fermer, 2500);
        return;
      }
      fermer();
    } catch (e) {
      /* site muet : la fenêtre reste, on peut recliquer */
    } finally {
      occupe = false;
    }
  }

  function montrer(inv) {
    if (affichee === inv.id) return;
    fermer();
    affichee = inv.id;
    fenetre = document.createElement('div');
    fenetre.className = 'inv-fenetre';
    fenetre.setAttribute('role', 'alertdialog');
    const ligne = document.createElement('div');
    const qui = document.createElement('b');
    qui.textContent = inv.hote;
    ligne.append(qui, ' ' + T.invite);
    const detail = document.createElement('small');
    detail.textContent = `${T.siege} ${Number(inv.siege) + 1}`;
    const boutons = document.createElement('div');
    boutons.className = 'inv-boutons';
    const non = document.createElement('button');
    non.type = 'button';
    non.className = 'inv-non';
    non.textContent = T.refuser;
    non.onclick = () => repondre(inv, false);
    const oui = document.createElement('button');
    oui.type = 'button';
    oui.className = 'inv-oui';
    oui.textContent = T.rejoindre;
    oui.onclick = () => repondre(inv, true);
    boutons.append(non, oui);
    fenetre.append(ligne, detail, boutons);
    document.body.appendChild(fenetre);
  }

  async function sonder() {
    if (document.hidden || occupe) return;
    try {
      const reponse = await fetch('/get_invitations', { cache: 'no-store' });
      if (!reponse.ok) return;
      const brut = await reponse.json();
      const liste = Array.isArray(brut && brut.invitations) ? brut.invitations : [];
      // La plus récente d'abord : une nouvelle invitation remplace la précédente.
      const derniere = liste[liste.length - 1];
      if (derniere && derniere.id && derniere.hote) montrer(derniere);
      else fermer();
    } catch (e) {
      /* table ou site muet : on réessaiera */
    }
  }

  sonder();
  setInterval(sonder, PERIODE_MS);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) sonder(); });
})();
