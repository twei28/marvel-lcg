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

  // La langue passe par langue-classique.js (window.MarvelLangue : choix dans le jeu > cookie du site > navigateur > français).
  const EN = (function () {
    try { return window.MarvelLangue ? window.MarvelLangue.actuelle() === 'en' : localStorage.getItem('marvel-langue') === 'en'; }
    catch (e) { return false; }
  })();
  const T = {
    un: EN ? 'A message for you' : 'Un message pour toi',
    plusieurs: EN ? 'messages for you' : 'messages pour toi',
    ouvrir: EN ? 'Open' : 'Ouvrir',
    ticketUn: EN ? 'A reply to your bug report' : 'Une réponse à ton signalement',
    ticketPlusieurs: EN ? 'replies to your bug reports' : 'réponses à tes signalements',
    ticketOuvrir: EN ? 'Read' : 'Lire',
  };

  // ⚠ L'ADRESSE DU SITE, ABSOLUE. La page est servie depuis `pN.<domaine>` et
  // le site depuis `<domaine>` : un `window.open('/signalements')` tombait sur
  // le MOTEUR, qui sert une image pour tout chemin inconnu — un onglet ouvert
  // sur rien (corrige le 19/09/2026, avec le bouton « Mes signalements » de
  // l'ecran de preparation). On demande l'adresse une fois, et on retombe sur
  // le chemin relatif quand il n'y a pas de site devant : en local, c'est la
  // meme machine.
  let adresseSignalements = '/signalements';
  fetch('/get_site_url').then((r) => (r.ok ? r.json() : { url: '' })).then((data) => {
    const url = data && data.url;
    if (url) adresseSignalements = url.replace(/\/+$/, '') + '/signalements';
  }).catch(() => {});

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
    /* ⚠ DEUX PASTILLES DISTINCTES (16/09/2026), pas une qui compte les deux.
       Quand un message ET une réponse de signalement attendent en même temps,
       une pastille unique devrait choisir où elle mène, et l'autre destination
       passerait à la trappe. Couleur différente, destination différente. */
    .tkt-pastille {
      position: fixed; right: 14px; bottom: 14px; z-index: 9000;
      display: flex; align-items: center; gap: 10px;
      padding: 8px 14px; border: 2px solid #1f6feb; border-radius: 10px;
      background: linear-gradient(180deg, rgba(12,24,48,.98), rgba(8,14,30,.98));
      box-shadow: 0 8px 30px rgba(0,0,0,.55);
      font: 14px/1.3 system-ui, sans-serif; color: #b7d3f0; cursor: pointer;
    }
    .tkt-pastille:hover { filter: brightness(1.15); }
    .tkt-pastille b { color: #fff; }
    /* Quand les deux sont là, celle des signalements monte d'un cran. */
    .msg-pastille + .tkt-pastille, .tkt-pastille.avec-message { bottom: 66px; }
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

  let pastilleTicket = null;

  /** La pastille des réponses de signalement. Même règle que l'autre : rien ne
   *  s'affiche tant que rien n'attend.
   *
   *  ⚠ ELLE N'APPELLE PAS `/post_messages_lus`. Ce sont deux compteurs
   *  distincts : ouvrir /signalements marque les réponses lues, côté site, et
   *  marquer les messages privés ici éteindrait la mauvaise pastille. */
  function dessinerTicket(combien, avecMessage) {
    if (!combien) {
      if (pastilleTicket) { pastilleTicket.remove(); pastilleTicket = null; }
      return;
    }
    if (!pastilleTicket) {
      pastilleTicket = document.createElement('button');
      pastilleTicket.type = 'button';
      pastilleTicket.className = 'tkt-pastille';
      // ⚠ UN NOUVEL ONGLET, comme pour les messages : ce module tourne aussi
      // sur le PLATEAU, et remplacer la page sortirait quelqu'un de sa partie.
      pastilleTicket.addEventListener('click', () => {
        window.open(adresseSignalements, '_blank', 'noopener');
      });
      document.body.appendChild(pastilleTicket);
    }
    pastilleTicket.classList.toggle('avec-message', !!avecMessage);
    pastilleTicket.innerHTML = '';
    const texte = document.createElement('span');
    texte.innerHTML = combien > 1
      ? '<b>' + combien + '</b> ' + T.ticketPlusieurs
      : '<b>' + T.ticketUn + '</b>';
    const bouton = document.createElement('span');
    bouton.textContent = '→ ' + T.ticketOuvrir;
    pastilleTicket.append(texte, bouton);
  }

  async function demander() {
    try {
      const r = await fetch('/get_messages_prives', { cache: 'no-store' });
      if (!r.ok) throw new Error(r.status);
      const j = await r.json();
      const nouveaux = Number((j && j.nouveaux) || 0);
      dessiner(nouveaux, (j && j.de) || []);
      // `tickets` est absent des anciennes reponses du site : Number(undefined)
      // vaudrait NaN, d'ou le `|| 0`. Une pastille ne doit jamais dependre
      // d'un deploiement du site pour ne PAS s'afficher.
      dessinerTicket(Number((j && j.tickets) || 0), nouveaux > 0);
    } catch (e) {
      // Partie locale sans site derrière, moteur muet, réseau coupé : on se
      // tait. Rien ici ne doit gêner la préparation d'une partie.
      dessiner(0, []);
      dessinerTicket(0, false);
    }
  }

  demander();
  setInterval(demander, PERIODE_MS);
})();
