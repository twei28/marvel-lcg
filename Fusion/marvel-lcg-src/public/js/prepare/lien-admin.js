// lien-admin.js — ajoute les boutons d'administration sur l'écran de
// préparation, quand la partie a été lancée par le site ET que c'est le compte
// administrateur qui joue : « ⚙ Administration » (le site), « 🖼 Relevé des
// illustrations » (la page qui dit qui est dessiné sur chaque carte) et
// « 🎨 Palettes des héros » (la couleur du fond de plateau, corrigée à la main) et
// « ✨ Créer » (un menu : le créateur de cartes, ou l'atelier d'images de pack).
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

  // La langue passe par langue-classique.js (window.MarvelLangue : choix dans le jeu > cookie du site > navigateur > français).
  var LANGUE = (function () {
    try { return window.MarvelLangue ? window.MarvelLangue.actuelle() : (localStorage.getItem('marvel-langue') === 'en' ? 'en' : 'fr'); }
    catch (e) { return 'fr'; }
  })();
  var DICO_EN_LOCAL = {
    'Administration': 'Admin',
    'Comptes et invitations du site': 'Site accounts and invitations',
    'Relevé des illustrations': 'Artwork survey',
    'Dire qui est dessiné sur chaque carte': 'Record who is drawn on each card',
    'Palettes des héros': 'Hero palettes',
    'Créer': 'Create',
    'Fabriquer des cartes ou des images de pack': 'Make cards or pack images',
    'Que veux-tu fabriquer ?': 'What do you want to make?',
    'Cartes': 'Cards',
    'Créer des cartes, des héros, des scénarios et des pochettes de pack': 'Create cards, heroes, scenarios and pack covers',
    'Fabriquer une carte Marvel Champions (23 types) et l’exporter en image ou en planche à imprimer': 'Make a Marvel Champions card (23 types) and export it as an image or a print sheet',
    'Fabriquer l’affiche d’un pack (héros, scénario, modulaire) à partir du gabarit': 'Make a pack cover (hero, scenario, modular) from the template',
    'Corriger la couleur du fond de plateau': 'Fix the board background colour',
    'Sauvegarde du code': 'Code backup',
    'Télécharger tout le projet sans les images (5 dernières sauvegardes)': 'Download the whole project without images (last 5 backups)',
    'Masquer tous mes accès en plus, comme un compte classique ; la langue, l’affichage et la phase du méchant seront redemandés': 'Hide all my extra access, like a regular account; language, display and villain phase will be asked again',
    'Tu vois le site comme un compte classique ; clique pour retrouver tes accès et tes réglages': 'You see the site like a regular account; click to get your access and settings back',
    'Export ZIP cartes': 'Card ZIP export',
    'Toutes les images de cartes (en/, fr/, en_voile_fr/) dans un seul ZIP': 'Every card image (en/, fr/, en_voile_fr/) in a single ZIP',
    'Export ZIP des images de cartes': 'Card image ZIP export',
    'Dernier ZIP': 'Latest ZIP',
    'Aucun ZIP généré pour l’instant.': 'No ZIP built yet.',
    'Sous-ensemble': 'Subset',
    'cartes': 'cards',
    'Génération en cours depuis': 'Build running for',
    'Lecture du catalogue': 'Reading the catalogue',
    'Recherche des scans': 'Looking for scans',
    'Préparation du voile FR': 'Preparing the FR overlay',
    'Rendu du voile FR': 'Rendering the FR overlay',
    'Écriture du ZIP': 'Writing the ZIP',
    'La dernière génération a échoué': 'The last build failed',
    'Régénérer le ZIP': 'Rebuild the ZIP',
    'Télécharger': 'Download',
    'Le ZIP précédent reste téléchargeable pendant la génération': 'The previous ZIP stays downloadable during the build',
    'Reconstruire le ZIP de toutes les cartes ? Cela tourne en tâche de fond et peut prendre plus d’une demi-heure.': 'Rebuild the ZIP of every card? It runs in the background and may take over half an hour.',
    'Lancement impossible': 'Could not start',
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

  // --- Export ZIP des images de cartes ------------------------------------
  var PHASES_EXPORT = {
    'catalogue': 'Lecture du catalogue',
    'scans': 'Recherche des scans',
    'voile-preparation': 'Préparation du voile FR',
    'voile': 'Rendu du voile FR',
    'zip': 'Écriture du ZIP',
  };

  function taillePropre(octets) {
    if (octets >= 1e9) return (octets / 1e9).toFixed(2).replace('.', ',') + ' Go';
    if (octets >= 1e6) return Math.round(octets / 1e6) + ' Mo';
    return Math.round(octets / 1e3) + ' ko';
  }

  function dateLisible(secondes) {
    try { return new Date(secondes * 1000).toLocaleString(LANGUE === 'en' ? 'en-GB' : 'fr-FR'); }
    catch (e) { return ''; }
  }

  function boutonExportCartes() {
    var style = document.createElement('style');
    style.textContent =
      '.export-cartes-panneau { position: fixed; z-index: 950; width: 340px; max-width: calc(100vw - 32px);' +
      ' background: #1f2328; color: #ddd; border: 1px solid #666; border-radius: 10px; padding: 12px 14px;' +
      ' box-shadow: 0 8px 24px rgba(0,0,0,.5); font-size: .85rem; line-height: 1.4; }' +
      '.export-cartes-panneau h3 { margin: 0 0 8px; font-size: .95rem; }' +
      '.export-cartes-panneau p { margin: 4px 0; }' +
      '.export-cartes-panneau .export-cartes-actions { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }' +
      '.export-cartes-panneau button { padding: 6px 12px; border-radius: 8px; border: 1px solid #666;' +
      ' background: #2e2e2e; color: #ddd; font-weight: 700; cursor: pointer; }' +
      '.export-cartes-panneau button:hover:not(:disabled) { background: #3d3d3d; }' +
      '.export-cartes-panneau button:disabled { opacity: .45; cursor: default; }' +
      '.export-cartes-panneau .export-cartes-en-cours { color: #f0b95f; }' +
      '.export-cartes-panneau .export-cartes-erreur { color: #ff8a80; }';
    document.head.append(style);

    var bouton = document.createElement('button');
    bouton.type = 'button';
    bouton.textContent = '📦 ' + t('Export ZIP cartes');
    bouton.title = t('Toutes les images de cartes (en/, fr/, en_voile_fr/) dans un seul ZIP');

    var panneau = null;
    var minuterie = null;
    var dernier = null;

    function fermer() {
      if (minuterie) { clearTimeout(minuterie); minuterie = null; }
      if (panneau) { panneau.remove(); panneau = null; }
      document.removeEventListener('mousedown', clicDehors, true);
    }
    function clicDehors(e) {
      if (panneau && !panneau.contains(e.target) && e.target !== bouton) fermer();
    }

    function afficher(etat) {
      if (!panneau) return;
      dernier = etat;
      panneau.innerHTML = '';
      var titre = document.createElement('h3');
      titre.textContent = '📦 ' + t('Export ZIP des images de cartes');
      panneau.append(titre);

      var ligneZip = document.createElement('p');
      ligneZip.textContent = etat.zip
        ? t('Dernier ZIP') + ' : ' + taillePropre(etat.zip.taille) + ', ' + dateLisible(etat.zip.date)
        : t('Aucun ZIP généré pour l’instant.');
      panneau.append(ligneZip);

      var detail = etat.etat || {};
      if (detail.resultat && etat.zip && !etat.en_cours) {
        var r = detail.resultat;
        var contenu = document.createElement('p');
        contenu.textContent = (Array.isArray(r.packs) ? t('Sous-ensemble') + ' (' + r.packs.join(', ') + ') : ' : '') +
          r.cartes + ' ' + t('cartes') + ' — en/ ' + r.en + ', fr/ ' + r.fr + ', en_voile_fr/ ' + r.en_voile_fr;
        panneau.append(contenu);
      }

      if (etat.en_cours) {
        var minutes = Math.max(0, Math.floor(((etat.maintenant || Date.now() / 1000) - (etat.depuis || detail.debut || 0)) / 60));
        var cours = document.createElement('p');
        cours.className = 'export-cartes-en-cours';
        var phase = PHASES_EXPORT[detail.phase] ? t(PHASES_EXPORT[detail.phase]) : '';
        var avance = detail.total ? ' (' + (detail.fait || 0) + '/' + detail.total + ')' : '';
        cours.textContent = '⏳ ' + t('Génération en cours depuis') + ' ' + minutes + ' min' +
          (phase ? ' — ' + phase + avance : '');
        panneau.append(cours);
      } else if (detail.phase === 'echec') {
        var echec = document.createElement('p');
        echec.className = 'export-cartes-erreur';
        echec.textContent = t('La dernière génération a échoué') + ' : ' + (detail.erreur || '?');
        panneau.append(echec);
      }

      var actions = document.createElement('div');
      actions.className = 'export-cartes-actions';
      var regenerer = document.createElement('button');
      regenerer.type = 'button';
      regenerer.textContent = '🔄 ' + t('Régénérer le ZIP');
      regenerer.disabled = !!etat.en_cours || etat.disponible === false;
      regenerer.addEventListener('click', function () {
        if (!window.confirm(t('Reconstruire le ZIP de toutes les cartes ? Cela tourne en tâche de fond et peut prendre plus d’une demi-heure.'))) return;
        regenerer.disabled = true;
        fetch('/post_export_cartes_regenerer', {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}',
        }).then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (d) {
            if (!r.ok && r.status !== 409) window.alert(t('Lancement impossible') + ' : ' + (d.error || r.status));
          });
        }).catch(function () {}).then(rafraichir);
      });
      var telecharger = document.createElement('button');
      telecharger.type = 'button';
      telecharger.textContent = '⬇️ ' + t('Télécharger');
      telecharger.disabled = !etat.zip;
      telecharger.title = etat.en_cours ? t('Le ZIP précédent reste téléchargeable pendant la génération') : '';
      telecharger.addEventListener('click', function () {
        window.location.href = '/telecharger_export_cartes';
      });
      actions.append(regenerer, telecharger);
      panneau.append(actions);
    }

    function rafraichir() {
      if (!panneau) return;
      if (minuterie) { clearTimeout(minuterie); minuterie = null; }
      fetch('/get_export_cartes', { cache: 'no-store' }).then(function (r) {
        return r.ok ? r.json() : null;
      }).then(function (etat) {
        if (!panneau) return;
        if (etat) afficher(etat);
        // Pendant une génération, l'état se relit toutes les 3 s ; sinon toutes les 30 s.
        minuterie = setTimeout(rafraichir, etat && etat.en_cours ? 3000 : 30000);
      }).catch(function () {
        if (panneau) minuterie = setTimeout(rafraichir, 10000);
      });
    }

    bouton.addEventListener('click', function () {
      if (panneau) { fermer(); return; }
      panneau = document.createElement('div');
      panneau.className = 'export-cartes-panneau';
      var rect = bouton.getBoundingClientRect();
      panneau.style.top = Math.round(rect.bottom + 6) + 'px';
      panneau.style.left = Math.max(16, Math.min(Math.round(rect.left), window.innerWidth - 356)) + 'px';
      panneau.textContent = '…';
      document.body.append(panneau);
      if (dernier) afficher(dernier);
      document.addEventListener('mousedown', clicDehors, true);
      rafraichir();
    });
    return bouton;
  }

  fetch('/get_site_admin').then(function (r) {
    return r.ok ? r.json() : { url: '' };
  }).then(function (data) {
    var url = data && data.url;
    if (!url) return;   // pas de site devant, ou pas l'administrateur
    // ⚠ CHEMIN ABSOLU, PAS RACINE-RELATIF (29/10/2026, signale par l'utilisateur en jeu : le Card Maker
    // ne demarrait pas, erreur "is not valid JSON"). Ce script tourne aussi bien servi par le SITE que
    // par une instance de Play (p1.narwhalchampions.com, un serveur DIFFERENT, sans ces pages statiques
    // ni ces routes) : un lien "/createur-cartes.html" s'ouvrait alors sur Play, pas sur le site. `url`
    // (reponse de /get_site_admin, toujours une adresse absolue du site) donne l'origine correcte, deja
    // utilisee ainsi par le bouton Sauvegarde juste en dessous.
    var origineSite = url.replace(/\/admin\/?$/, '')

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
      window.open(origineSite + '/releve-images.html', '_blank', 'noopener');
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
      window.open(origineSite + '/palettes-heros.html', '_blank', 'noopener');
    });
    rangee.append(palettes);

    // Un seul bouton « Create » pour les deux outils de fabrication (29/10/2026) :
    // le créateur de cartes et l'atelier d'images de pack. Les pages sont
    // statiques et n'écrivent rien sur le serveur ; le menu demande laquelle ouvrir.
    var creer = document.createElement('button');
    creer.type = 'button';
    creer.textContent = '✨ ' + t('Créer');
    creer.title = t('Fabriquer des cartes ou des images de pack');
    var menuCreer = null;
    function fermerMenuCreer() {
      if (menuCreer) { menuCreer.remove(); menuCreer = null; }
      document.removeEventListener('mousedown', clicDehorsCreer, true);
    }
    function clicDehorsCreer(e) {
      if (menuCreer && !menuCreer.contains(e.target) && !creer.contains(e.target)) fermerMenuCreer();
    }
    creer.addEventListener('click', function () {
      if (menuCreer) { fermerMenuCreer(); return; }
      menuCreer = document.createElement('div');
      menuCreer.setAttribute('role', 'menu');
      menuCreer.style.cssText = 'position:fixed;z-index:950;width:280px;max-width:calc(100vw - 32px);' +
        'background:#1f2328;color:#ddd;border:1px solid #666;border-radius:10px;padding:10px;' +
        'box-shadow:0 8px 24px rgba(0,0,0,.5);font-size:.85rem;line-height:1.4;';
      var rect = creer.getBoundingClientRect();
      menuCreer.style.top = Math.round(rect.bottom + 6) + 'px';
      menuCreer.style.left = Math.max(16, Math.min(Math.round(rect.left), window.innerWidth - 296)) + 'px';
      var titre = document.createElement('div');
      titre.textContent = t('Que veux-tu fabriquer ?');
      titre.style.cssText = 'font-weight:700;margin:0 0 8px;';
      menuCreer.append(titre);
      [
        ['🃏 MC Creator', t('Créer des cartes, des héros, des scénarios et des pochettes de pack'), origineSite + '/mc-creator'],
      ].forEach(function (choix) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('role', 'menuitem');
        b.style.cssText = 'display:block;width:100%;text-align:left;margin:0 0 6px;padding:8px 10px;' +
          'border-radius:8px;border:1px solid #666;background:#2e2e2e;color:#ddd;cursor:pointer;';
        var nom = document.createElement('div');
        nom.textContent = choix[0];
        nom.style.fontWeight = '700';
        var detail = document.createElement('div');
        detail.textContent = choix[1];
        detail.style.cssText = 'font-size:.75rem;opacity:.75;margin-top:2px;';
        b.append(nom, detail);
        b.addEventListener('click', function () {
          fermerMenuCreer();
          window.open(choix[2], '_blank', 'noopener');
        });
        menuCreer.append(b);
      });
      document.body.append(menuCreer);
      document.addEventListener('mousedown', clicDehorsCreer, true);
    });
    rangee.append(creer);

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

    // L'export ZIP des images de cartes (27/10/2026) : en/, fr/ et
    // en_voile_fr/ dans un seul ZIP. Le bouton ouvre un petit panneau à deux
    // actions. « Régénérer » lance la construction en tâche de fond sur le
    // serveur (un processus à part : les parties continuent) ; « Télécharger »
    // sert le dernier ZIP construit, tel quel. Les trois routes refusent (403)
    // qui n'est pas l'administrateur, quoi que montre ce bouton.
    rangee.append(boutonExportCartes());
  }).catch(function () {
    // Moteur lancé à la main, route absente : pas de bouton, pas d'erreur.
  });
})();
