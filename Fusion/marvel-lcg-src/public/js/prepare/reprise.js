// Reprise de partie, relecture et statistiques — module autonome du wizard.
//
// Volontairement SEPARE de app.js (qui est dense) : ce fichier n'y touche pas,
// il ajoute deux boutons flottants en haut a droite de l'ecran de preparation :
//   ⏵ Resume  -> liste des sauvegardes (replays/) : Reprendre / Revoir / Import
//   📊 Stats  -> statistiques globales + journal des parties (winrates)
//
// Cote serveur : /list_replay_files, /get_replay_json?<nom>, /debug?/load
// <nom>:-1 (reprendre au dernier pas), /load_replay_data (import),
// /get_statistics_json, /get_games_history (ajouts locaux).

(function () {
  'use strict';

  // ---------------------------------------------------------------- langue --
  // Mini t() local : ce fichier est un script CLASSIQUE (defer + IIFE), pas un
  // module ES — il ne peut donc pas importer js/prepare/langue.js. On duplique
  // la lecture de localStorage['marvel-langue'] et un petit dictionnaire local
  // limité aux libellés de ce fichier (même contrat : clé FR -> texte EN,
  // clé absente = FR conservé).
  const LANGUE = (function () {
    try { return localStorage.getItem('marvel-langue') === 'en' ? 'en' : 'fr'; }
    catch { return 'fr'; }
  })();
  const DICO_EN_LOCAL = {
    'Reprendre une partie': 'Resume a game',
    'Chargement...': 'Loading...',
    'Importer un fichier .json': 'Import a .json file',
    "Aucune sauvegarde pour l'instant. En partie, bouton \u{1F4BE} Save du plateau.":
      "No saves yet. In game, use the board's \u{1F4BE} Save button.",
    'Reprendre': 'Resume',
    'Revoir': 'Replay',
    'pas': 'step',
    'Fermer': 'Close',
    'Import impossible : fichier invalide ?': 'Import failed: invalid file?',
    'Statistiques': 'Statistics',
    'parties terminees': 'games finished',
    'victoires / defaites': 'wins / losses',
    'taux de victoire': 'win rate',
    'degats infliges': 'damage dealt',
    'degats subis': 'damage taken',
    'degats soignes': 'damage healed',
    'cartes piochees': 'cards drawn',
    'menace retiree': 'threat removed',
    'plus gros coup': 'biggest hit',
    'Succes debloques': 'Achievements unlocked',
    'premier sang': 'first blood',
    'double K.O.': 'double kill',
    'triple K.O.': 'triple kill',
    'quadruple K.O.': 'ultra kill',
    'dechainement': 'rampage',
    'Le journal des parties demarre maintenant : chaque partie terminee s’ajoutera ici (heros, vilain, resultat).':
      'The game log starts now: every finished game will be added here (heroes, villain, result).',
    'Heros': 'Hero',
    'Parties': 'Games',
    'Resultat': 'Result',
    'Victoire': 'Won',
    'Defaite': 'Lost',
    'Reprendre ou revoir une partie sauvegardee': 'Resume or replay a saved game',
    'Statistiques et journal des parties': 'Statistics and game log',
    'Hauts faits': 'Feats',
    'Hauts faits debloques et progression': 'Unlocked feats and progress',
  };
  function t(fr) {
    return LANGUE === 'en' && Object.prototype.hasOwnProperty.call(DICO_EN_LOCAL, fr)
      ? DICO_EN_LOCAL[fr] : fr;
  }

  // ---------------------------------------------------------------- utils --
  function el(tag, attrs, ...enfants) {
    const noeud = document.createElement(tag);
    if (attrs) {
      for (const [cle, valeur] of Object.entries(attrs)) {
        if (cle === 'onclick') noeud.addEventListener('click', valeur);
        else if (cle === 'style') noeud.style.cssText = valeur;
        else noeud.setAttribute(cle, valeur);
      }
    }
    for (const enfant of enfants) {
      if (enfant == null) continue;
      noeud.append(enfant.nodeType ? enfant : document.createTextNode(String(enfant)));
    }
    return noeud;
  }

  async function lireJson(url) {
    try {
      const reponse = await fetch(url, { cache: 'no-store' });
      if (!reponse.ok) return undefined;
      return await reponse.json();
    } catch {
      return undefined;
    }
  }

  function dateLisible(secondes) {
    try {
      return new Date(secondes * 1000).toLocaleDateString(LANGUE === 'en' ? 'en-GB' : 'fr-FR', {
        day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit',
      });
    } catch {
      return '';
    }
  }

  // ---------------------------------------------------------------- style --
  const style = document.createElement('style');
  style.textContent = `
    .reprise-boutons { display: flex; gap: 8px; align-items: center;
      flex-wrap: wrap; }
    .reprise-boutons.est-flottante { position: fixed; top: 82px; right: 12px;
      z-index: 900; justify-content: flex-end; }
    .reprise-boutons button { padding: 7px 13px; border-radius: 8px;
      border: 1px solid #666; background: #2e2e2e; color: #ddd; font-weight: 700;
      cursor: pointer; font-size: .85rem; }
    .reprise-boutons button:hover { background: #3d3d3d; }
    .reprise-sous-titre { margin: 1.1rem 0 .5rem; font-size: .9rem;
      color: #ffd45a; }
    .reprise-voile { position: fixed; inset: 0; z-index: 950;
      background: rgba(0,0,0,.65); display: flex; justify-content: center;
      align-items: flex-start; padding: 6vh 16px; overflow: auto; }
    .reprise-panneau { width: 100%; max-width: 760px; background: #262626;
      border: 1px solid #555; border-radius: 10px; padding: 1.2rem 1.4rem;
      color: #ddd; font-family: system-ui, sans-serif; }
    .reprise-panneau h2 { margin: 0 0 1rem; color: #fff; font-size: 1.2rem;
      display: flex; justify-content: space-between; align-items: center; }
    .reprise-panneau h2 button { background: none; border: none; color: #aaa;
      font-size: 1.4rem; cursor: pointer; }
    .reprise-ligne { display: flex; align-items: center; gap: 10px;
      padding: .55rem .4rem; border-bottom: 1px solid #3a3a3a; }
    .reprise-ligne .info { flex: 1; line-height: 1.3; }
    .reprise-ligne .info small { color: #999; }
    .reprise-ligne button { padding: 5px 11px; border-radius: 7px;
      border: 1px solid #666; background: #333; color: #ddd; cursor: pointer;
      font-size: .8rem; font-weight: 700; }
    .reprise-ligne button:hover { background: #454545; }
    .reprise-ligne button.principal { background: #b3202b; border-color: #b3202b; color: #fff; }
    .reprise-ligne button.principal:hover { background: #d02733; }
    .stats-grille { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 10px; margin-bottom: 1.1rem; }
    .stats-tuile { background: #1e1e1e; border: 1px solid #444; border-radius: 8px;
      padding: .6rem .75rem; }
    .stats-tuile b { display: block; font-size: 1.3rem; color: #fff; }
    .stats-tuile span { font-size: .75rem; color: #999; }
    .stats-table { width: 100%; border-collapse: collapse; font-size: .82rem; }
    .stats-table th, .stats-table td { padding: .35rem .5rem; text-align: left;
      border-bottom: 1px solid #3a3a3a; }
    .stats-table th { color: #999; font-weight: 600; }
    .stats-victoire { color: #6fbf73; font-weight: 700; }
    .stats-defaite { color: #e06c65; font-weight: 700; }
    .reprise-vide { color: #999; padding: 1rem 0; }
  `;
  document.head.append(style);

  // ------------------------------------------------------------- overlays --
  let voile = null;
  function fermer() {
    if (voile) { voile.remove(); voile = null; }
  }
  function ouvrir(panneau) {
    fermer();
    voile = el('div', { class: 'reprise-voile', onclick: (e) => { if (e.target === voile) fermer(); } }, panneau);
    document.body.append(voile);
  }
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') fermer(); });

  function titre(texte) {
    return el('h2', null, texte, el('button', { onclick: fermer, 'aria-label': t('Fermer') }, '×'));
  }

  // -------------------------------------------------------------- reprise --
  async function chargerEtOuvrir(nom, revoir, pas) {
    // `:-1` = dernier pas (reprendre) ; pour revoir, on charge puis on remet le
    // curseur au debut cote plateau (barre de relecture).
    await fetch(`/debug?/load ${nom}:-1`).catch(() => undefined);
    const url = revoir ? `/app/board.html?p=0&revoir=1&pas=${pas || 0}` : '/app/board.html?p=0';
    window.location.href = url;
  }

  async function ouvrirReprise() {
    const panneau = el('div', { class: 'reprise-panneau' }, titre(t('Reprendre une partie')));
    const zone = el('div', null, el('div', { class: 'reprise-vide' }, t('Chargement...')));
    panneau.append(zone);

    const importer = el('input', { type: 'file', accept: '.json', style: 'display:none' });
    importer.addEventListener('change', async () => {
      const fichier = importer.files && importer.files[0];
      if (!fichier) return;
      const texte = await fichier.text();
      const reponse = await fetch('/load_replay_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: texte }),
      }).catch(() => undefined);
      if (reponse && reponse.ok) window.location.href = '/app/board.html?p=0';
      else alert(t('Import impossible : fichier invalide ?'));
    });
    panneau.append(
      importer,
      el('div', { style: 'margin-top:.9rem; text-align:right;' },
        el('button', {
          class: 'principal', style: 'padding:7px 13px; border-radius:7px; border:none; cursor:pointer; background:#444; color:#ddd;',
          onclick: () => importer.click(),
        }, t('Importer un fichier .json')))
    );
    ouvrir(panneau);

    const noms = (await lireJson('/list_replay_files')) || [];
    zone.textContent = '';
    if (!Array.isArray(noms) || noms.length === 0) {
      zone.append(el('div', { class: 'reprise-vide' },
        t("Aucune sauvegarde pour l'instant. En partie, bouton \u{1F4BE} Save du plateau.")));
      return;
    }
    const lignes = await Promise.all(noms.slice(0, 40).map(async (nom) => {
      const meta = (await lireJson(`/get_replay_json?${nom}`)) || {};
      return { nom, meta };
    }));
    for (const { nom, meta } of lignes) {
      const heros = Array.isArray(meta.players) ? meta.players.join(', ') : '';
      zone.append(el('div', { class: 'reprise-ligne' },
        el('div', { class: 'info' },
          el('div', null, `${meta.villain || nom}`),
          el('small', null, `${nom} · ${t('pas')} ${meta.step ?? '?'} ${meta.time ? '· ' + meta.time : ''} ${heros ? '· ' + heros : ''}`)),
        el('button', { class: 'principal', onclick: () => chargerEtOuvrir(nom, false) }, t('Reprendre')),
        el('button', { onclick: () => chargerEtOuvrir(nom, true, meta.step || 0) }, t('Revoir'))));
    }
  }

  // ---------------------------------------------------------------- stats --
  async function ouvrirStats() {
    const panneau = el('div', { class: 'reprise-panneau' }, titre(t('Statistiques')));
    const zone = el('div', null, el('div', { class: 'reprise-vide' }, t('Chargement...')));
    panneau.append(zone);
    ouvrir(panneau);

    const [stats, histoire] = await Promise.all([
      lireJson('/get_statistics_json'),
      lireJson('/get_games_history'),
    ]);
    zone.textContent = '';

    const s = stats || {};
    const jouees = (s.games_won || 0) + (s.games_lost || 0);
    const winrate = jouees ? Math.round((100 * (s.games_won || 0)) / jouees) : 0;
    const tuile = (valeur, libelle) =>
      el('div', { class: 'stats-tuile' }, el('b', null, String(valeur)), el('span', null, libelle));
    zone.append(el('div', { class: 'stats-grille' },
      tuile(jouees, t('parties terminees')),
      tuile(`${s.games_won || 0} / ${s.games_lost || 0}`, t('victoires / defaites')),
      tuile(`${winrate}%`, t('taux de victoire')),
      tuile(s.total_damage_dealt || 0, t('degats infliges')),
      tuile(s.total_damage_taken || 0, t('degats subis')),
      tuile(s.total_damage_healed || 0, t('degats soignes')),
      tuile(s.total_cards_drawn || 0, t('cartes piochees')),
      tuile(s.total_threats_removed || 0, t('menace retiree')),
      tuile(s.max_single_damage_dealt || 0, t('plus gros coup'))));

    // Succes cumules (game/rule/achievement.py) : montres seulement si au
    // moins un a ete debloque, pour ne pas surcharger l'ecran.
    const succes = [
      [s.achievement_first_blood || 0, t('premier sang')],
      [s.achievement_double_kill || 0, t('double K.O.')],
      [s.achievement_triple_kill || 0, t('triple K.O.')],
      [s.achievement_ultra_kill || 0, t('quadruple K.O.')],
      [s.achievement_rampage || 0, t('dechainement')],
    ].filter(([n]) => n > 0);
    if (succes.length) {
      zone.append(el('h3', { class: 'reprise-sous-titre' }, '\u{1F3C6} ' + t('Succes debloques')));
      zone.append(el('div', { class: 'stats-grille' },
        ...succes.map(([n, libelle]) => tuile(n, libelle))));
    }

    const parties = Array.isArray(histoire) ? histoire : [];
    if (parties.length === 0) {
      zone.append(el('div', { class: 'reprise-vide' },
        t('Le journal des parties demarre maintenant : chaque partie terminee s’ajoutera ici (heros, vilain, resultat).')));
      return;
    }

    // Winrate par heros et par scenario.
    const agreger = (cle) => {
      const table = new Map();
      for (const partie of parties) {
        const cles = cle === 'scenario'
          ? [partie.scenario || '?']
          : (partie.heroes || []).map((h) => h.name || '?');
        for (const nom of cles) {
          const ligne = table.get(nom) || { jouees: 0, gagnees: 0 };
          ligne.jouees += 1;
          if (partie.won) ligne.gagnees += 1;
          table.set(nom, ligne);
        }
      }
      return [...table.entries()].sort((a, b) => b[1].jouees - a[1].jouees);
    };
    const tableAgregat = (titreTexte, entrees) => {
      const table = el('table', { class: 'stats-table' },
        el('tr', null, el('th', null, titreTexte), el('th', null, t('Parties')), el('th', null, 'Winrate')));
      for (const [nom, ligne] of entrees.slice(0, 12)) {
        table.append(el('tr', null,
          el('td', null, nom),
          el('td', null, `${ligne.gagnees}/${ligne.jouees}`),
          el('td', null, `${Math.round((100 * ligne.gagnees) / ligne.jouees)}%`)));
      }
      return el('div', { style: 'margin-bottom:1.1rem;' }, table);
    };
    zone.append(tableAgregat(t('Heros'), agreger('hero')), tableAgregat('Scenario', agreger('scenario')));

    const derniers = el('table', { class: 'stats-table' },
      el('tr', null, el('th', null, 'Date'), el('th', null, t('Heros')), el('th', null, 'Scenario'),
        el('th', null, 'Rounds'), el('th', null, t('Resultat'))));
    for (const partie of parties.slice(-20).reverse()) {
      derniers.append(el('tr', null,
        el('td', null, dateLisible(partie.time)),
        el('td', null, (partie.heroes || []).map((h) => h.name).join(', ')),
        el('td', null, `${partie.scenario || ''}${partie.expert ? ' (Expert)' : ''}`),
        el('td', null, String(partie.rounds ?? '')),
        el('td', { class: partie.won ? 'stats-victoire' : 'stats-defaite' },
          partie.won ? t('Victoire') : t('Defaite'))));
    }
    zone.append(derniers);
  }

  // ------------------------------------------------------------- montage --
  // Reutilise la rangee si un autre module (puzzles.js) l'a deja creee.
  // Elle vit DANS le header du wizard, a cote du bouton langue ; si le header
  // n'est pas encore rendu (app.js charge ses donnees), elle flotte en
  // attendant que progressBar() l'adopte au premier rendu.
  let rangee = document.querySelector('.reprise-boutons');
  if (!rangee) {
    rangee = el('div', { class: 'reprise-boutons' });
    const etapes = document.querySelector('header.progress .steps');
    if (etapes) etapes.parentElement.insertBefore(rangee, etapes);
    else { rangee.classList.add('est-flottante'); document.body.append(rangee); }
  }
  rangee.append(
    el('button', { onclick: ouvrirReprise, title: t('Reprendre ou revoir une partie sauvegardee') }, '⏵ ' + t('Reprendre')),
    el('button', { onclick: ouvrirStats, title: t('Statistiques et journal des parties') }, '\u{1F4CA} Stats'));

  // Hauts faits : DEBRANCHE a la demande de l'utilisateur, comme la banniere
  // du plateau. La page /achievements.html reste en place et continue d'etre
  // alimentee : il suffit de remettre ce bouton dans le append ci-dessus pour
  // la rallumer.
  //
  // el('button', {
  //   onclick: () => { window.location.href = '/achievements.html'; },
  //   title: t('Hauts faits debloques et progression'),
  // }, '\u{1F3C6} ' + t('Hauts faits'))

})();
