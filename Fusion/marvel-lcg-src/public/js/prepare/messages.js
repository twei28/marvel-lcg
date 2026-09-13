// messages.js — la pastille « un message t'attend », et rien d'autre.
//
// ⚠ RIEN NE S'AFFICHE TANT QUE PERSONNE N'ECRIT. Le tchat a été retiré du jeu
// le 12/09/2026, à la demande de l'utilisateur : personne ne s'en servait, et
// il encombrait deux écrans pour rien. Ce module ne le remet pas. Il ne pose
// une pastille que lorsqu'un message attend vraiment, et disparaît dès qu'elle
// est lue.
//
// Module AUTONOME, sur le modèle de annonce.js et reprise.js : script classique
// (defer + IIFE), aucune dépendance à app.js, ses styles avec lui.
//
// Chaîne complète : l'administrateur écrit depuis /admin, le site range le
// message, le moteur le relaie sur /get_messages_prives (il est le seul à
// pouvoir parler au site : le navigateur est sur p<N>.<domaine> et son cookie
// ne voyagerait pas), et ce module l'interroge.
(function () {
  'use strict';

  // Toutes les 20 s : on veut qu'un message adressé à quelqu'un qui joue lui
  // arrive pendant sa partie, pas à sa prochaine visite.
  const PERIODE_MS = 20000;

  const EN = (function () {
    try { return localStorage.getItem('marvel-langue') === 'en'; }
    catch (e) { return false; }
  })();
  const T = {
    un: EN ? 'A message for you' : 'Un message pour toi',
    plusieurs: EN ? 'messages for you' : 'messages pour toi',
    ouvrir: EN ? 'Open' : 'Ouvrir',
  };

  const style = document.createElement('style');
  style.textContent = `
    .msg-pastille {
      position: fixed; right: 14px; bottom: 14px; z-index: 9000;
      display: flex; align-items: center; gap: 10px;
      padding: 8px 14px; border: 2px solid #3fb950; border-radius: 10px;
      background: linear-gradient(180deg, rgba(12,40,20,.98), rgba(8,24,12,.98));
      box-shadow: 0 8px 30px rgba(0,0,0,.55);
      font: 14px/1.3 system-ui, sans-serif; color: #b7f0c2; cursor: pointer;
    }
    .msg-pastille:hover { filter: brightness(1.15); }
    .msg-pastille b { color: #fff; }
  `;
  document.head.appendChild(style);

  let pastille = null;

  function dessiner(nouveaux, de) {
    if (!nouveaux) {
      if (pastille) { pastille.remove(); pastille = null; }
      return;
    }
    if (!pastille) {
      pastille = document.createElement('button');
      pastille.type = 'button';
      pastille.className = 'msg-pastille';
      // ⚠ La page du salon existe depuis toujours et sait déjà tout faire :
      // lister les joueurs, ouvrir une conversation, répondre. On y envoie
      // plutôt que d'en réécrire une moitié ici.
      // ⚠ UN NOUVEL ONGLET, JAMAIS LA MEME PAGE. Ce module tourne aussi sur
      // le PLATEAU : y remplacer la page reviendrait a sortir quelqu'un de sa
      // partie pour lire un message.
      pastille.addEventListener('click', () => {
        fetch('/post_messages_lus', { method: 'POST' })
          .catch(() => undefined)
          .finally(() => { window.open('/salon.html', '_blank', 'noopener'); });
      });
      document.body.appendChild(pastille);
    }
    const qui = (de && de.length) ? ' — ' + de.join(', ') : '';
    pastille.innerHTML = '';
    const texte = document.createElement('span');
    texte.innerHTML = nouveaux > 1
      ? '<b>' + nouveaux + '</b> ' + T.plusieurs + qui
      : '<b>' + T.un + '</b>' + qui;
    const bouton = document.createElement('span');
    bouton.textContent = '→ ' + T.ouvrir;
    pastille.append(texte, bouton);
  }

  async function demander() {
    try {
      const r = await fetch('/get_messages_prives', { cache: 'no-store' });
      if (!r.ok) throw new Error(r.status);
      const j = await r.json();
      dessiner(Number((j && j.nouveaux) || 0), (j && j.de) || []);
    } catch (e) {
      // Partie locale sans site derrière, moteur muet, réseau coupé : on se
      // tait. Rien ici ne doit gêner la préparation d'une partie.
      dessiner(0, []);
    }
  }

  demander();
  setInterval(demander, PERIODE_MS);
})();
