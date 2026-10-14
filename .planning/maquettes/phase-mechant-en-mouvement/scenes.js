// Les 18 encadrés de la phase du méchant et tous leurs cas, d'après les décisions
// de .planning/todos/2026-10-12-phase-mechant-schema-et-questions.md (13/10/2026).
(function () {
  // ------------------------------------------------------------ petits morceaux de boîte
  const mini = (id, nom, t, o = {}) =>
    `<div class="mini t-${t}${o.dos ? ' dos' : ''}${o.incline ? ' incline' : ''}${o.pale ? ' pale' : ''}${o.raye ? ' raye' : ''}" data-id="${id}" ${o.joueur ? `style="--joueur:var(--j${o.joueur})"` : ''}>` +
    `<span class="nom">${o.dos ? '' : nom}</span>${o.gros ? `<b class="gros ${o.grosTon || ''}">${o.gros}</b>` : ''}${o.tampon ? `<i class="tampon ${o.tamponTon || ''}">${o.tampon}</i>` : ''}${o.etoile ? '<i class="etoile">★</i>' : ''}${o.num ? `<i class="num">(${o.num})</i>` : ''}</div>`;
  const rangee = (...m) => `<div class="rangee">${m.join('')}</div>`;
  const ligne = (label, val, o = {}) =>
    `<div class="ligne${o.ton ? ` ${o.ton}` : ''}">${o.carte ? `<span class="vignette t-${o.carte}"></span>` : ''}${o.pastilles ? o.pastilles.map((j) => `<span class="pastille-mini" style="--joueur:var(--j${j})"></span>`).join('') : ''}<span class="l">${label}</span><span class="v">${o.barre ? `<s>${o.barre}</s> ` : ''}${val}</span></div>`;
  const total = (txt, o = {}) => `<div class="total ${o.ton || ''}">${txt}</div>`;
  const note = (txt, ton = '') => `<p class="note ${ton}">${txt}</p>`;
  const bandeau = (txt) => `<div class="bandeau">${txt}</div>`;
  const texte = (txt) => `<p class="texte-carte">${txt}</p>`;
  const btn = (txt, ton = 'vert', o = {}) => `<button type="button" class="choix ${ton}${o.grise ? ' grise' : ''}" ${o.grise ? 'disabled' : 'data-suite'}>${o.def ? `<span class="def">${o.def}<small>DÉF</small></span>` : ''}<span>${txt}</span></button>`;
  const choix = (...b) => `<div class="choix-liste">${b.join('')}</div>`;
  const jauge = (av, ap, max, ton = '') => `<div class="jauge ${ton}"><span style="width:${(ap / max) * 100}%"></span><em>${av} → ${ap} / ${max}</em></div>`;

  // ------------------------------------------------------------ la table type
  // Positions en % de la table. Piles à gauche, méchant et manigances en haut,
  // sbires au milieu, héros en bas, chaque joueur dans sa couleur.
  const T = {
    paquet: { id: 'paquet', pile: 'paquet', x: 2, y: 3 },
    defausse: { id: 'defausse', pile: 'defausse', x: 14, y: 3 },
    klaw: { id: 'klaw', nom: 'Klaw', sous: 'Méchant · stade I', t: 'vilain', x: 29, y: 3, c: '24/24' },
    trafic: { id: 'trafic', nom: 'Trafic Clandestin', sous: 'Manigance principale', t: 'principale', x: 43, y: 3, c: '1/6' },
    reseau: { id: 'reseau', nom: 'Réseau de Distribution', sous: 'Annexe ⚡', t: 'annexe', x: 57, y: 3, c: '3/3' },
    retire: { id: 'retire', pile: 'retire', x: 86, y: 3 },
    victoire: { id: 'victoire', pile: 'victoire', x: 86, y: 37 },
    ironheart: { id: 'ironheart', nom: 'Ironheart', sous: 'Héros · J1', t: 'heros', joueur: 1, x: 29, y: 68, c: '11/11' },
    brawn: { id: 'brawn', nom: 'Brawn', sous: 'Allié', t: 'allie', joueur: 1, x: 43, y: 68, c: '5/5' },
    cap: { id: 'cap', nom: 'Captain America', sous: 'Héros · J2', t: 'heros', joueur: 2, x: 64, y: 68, c: '11/11' },
    main: { id: 'main', pile: 'main', x: 2, y: 68 },
    defausseJ: { id: 'defausseJ', pile: 'defausseJ', x: 14, y: 68 },
  };
  const table = (...ids) => ids.map((x) => (typeof x === 'string' ? { ...T[x] } : x));
  const carte = (id, nom, sous, t, x, y, o = {}) => ({ id, nom, sous, t, x, y, ...o });

  const E = (onglet, titre, corps, o = {}) => ({ onglet, titre, corps, ...o });
  const trait = (de, vers, couleur) => ({ f: 'trait', de, vers, couleur });
  const jeton = (id, genre, label, de, vers) => ({ f: 'jeton', id, genre, label, de, vers });
  const vole = (id, carte, c, plus = {}) => ({ f: 'vole', id, puis: { carte, etat: { c, ...plus } } });
  const maj = (carte, etat) => ({ f: 'maj', carte, etat });
  const place = (carte) => ({ f: 'place', carte });
  const arrive = (carte, de, delai, etat) => ({ f: 'arrive', carte, de, delai, etat });
  const part = (carte, vers, delai) => ({ f: 'part', carte, vers, delai });
  const copie = (de, vers, texte, delai, fondu) => ({ f: 'copie', de, vers, texte, delai, fondu });
  const halo = (c, couleur = 'acier') => maj(c, { halo: couleur });

  const ENCADRES = [];
  const enc = (id, phase, nom, decisions, cas) => ENCADRES.push({ id, phase, nom, decisions, cas });

  // ===================================================================== ① MENACE
  const calculSimple = ligne('Trafic Clandestin : 1 par joueur × 1 joueur', '+1', { carte: 'principale', pastilles: [1] });
  enc('①', '1 Menaces', 'Menace posée sur une manigance', [
    'Un écran par manigance qui reçoit de la menace.',
    'Chaque source avec sa carte, total en bas.',
    'Phrase rouge « Encore N avant la défaite » à 2 ou moins de la fin.',
    'Valeur réduite : barrée, avec la carte responsable.',
    'Pastille « 1 réponse possible » quand une carte de ta main peut réagir.',
    'Icônes de la manigance expliquées sous la carte.',
    'Multijoueur : « 1 par joueur × 3 joueurs » et leurs pastilles.',
    'Petit « tac » quand le jeton se pose. Jamais d’écran sauté.',
    'Halo gris acier bien visible autour de la manigance visée.',
  ], [
    {
      nom: 'Solo, cas simple',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'brawn', 'main', 'defausseJ'),
      etapes: [
        E('1', 'Menace', rangee(mini('m', 'Trafic Clandestin', 'principale')) + calculSimple + total('+1 menace') + jauge(1, 2, 6) + note('🔺 Crise : aucune. ⚡ Accélération : aucune.'),
          { montre: [halo('trafic'), trait('boite', 'trafic'), jeton('j1', 'menace', '+1', 'boite', 'trafic')], suite: [vole('j1', 'trafic', '2/6')] }),
        E('2A', 'Attaque de Klaw', note('L’étape 2A commence : le jeton vient de se poser, la manigance est passée à 2/6.'), { bouton: null }),
      ],
    },
    {
      nom: 'Multijoueur, accélération',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'reseau', 'ironheart', 'cap', { ...T.brawn, x: 43 }),
      etapes: [
        E('1', 'Menace',
          rangee(mini('m', 'Trafic Clandestin', 'principale')) +
          ligne('Trafic Clandestin : 1 par joueur × 2 joueurs', '+2', { carte: 'principale', pastilles: [1, 2] }) +
          ligne('Icône ⚡ de Réseau de Distribution', '+1', { carte: 'annexe' }) +
          ligne('Jeton d’accélération (paquet remélangé)', '+1', { carte: 'acceleration' }) +
          total('+4 menaces') + jauge(1, 5, 6, 'rouge') + note('Encore 1 avant la défaite', 'rouge'),
          { montre: [halo('trafic'), trait('boite', 'trafic'), jeton('j1', 'menace', '+4', 'boite', 'trafic')], suite: [vole('j1', 'trafic', '5/6', { rouge: true })] }),
        E('2A', 'Attaque de Klaw', note('Le compteur est à 5/6, en rouge sur la table.'), { bouton: null }),
      ],
    },
    {
      nom: 'Menace réduite par une carte',
      table: table('paquet', 'defausse', 'klaw', 'trafic', carte('surv', 'Surveillance', 'Amélioration J1', 'amelioration', 57, 3, { joueur: 1 }), 'ironheart'),
      etapes: [
        E('1', 'Menace', rangee(mini('m', 'Trafic Clandestin', 'principale')) +
          ligne('Trafic Clandestin : 1 par joueur × 1 joueur', '+1', { carte: 'principale', pastilles: [1] }) +
          ligne('Icône ⚡ d’une annexe', '+1', { carte: 'annexe' }) +
          ligne('Surveillance : 1 menace de moins', '−1', { carte: 'amelioration', ton: 'vert' }) +
          total('<s>+2</s> → +1 menace') + jauge(1, 2, 6),
          { montre: [halo('trafic'), halo('surv', 'vert'), trait('surv', 'trafic', 'vert'), trait('boite', 'trafic'), jeton('j1', 'menace', '+1', 'boite', 'trafic')], suite: [vole('j1', 'trafic', '2/6')] }),
        E('2A', 'Attaque de Klaw', note('Le jeton portait le montant final, +1.'), { bouton: null }),
      ],
    },
    {
      nom: 'Une carte de ta main peut réagir',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'main'),
      etapes: [
        E('1', 'Menace', rangee(mini('m', 'Trafic Clandestin', 'principale')) + calculSimple + total('+1 menace') + jauge(1, 2, 6),
          { reponse: 'Cran d’arrêt', montre: [halo('trafic'), halo('main', 'dore'), trait('boite', 'trafic'), jeton('j1', 'menace', '+1', 'boite', 'trafic')] }),
        E('1', 'Menace · ta réponse', rangee(mini('m', 'Trafic Clandestin', 'principale'), mini('r', 'Cran d’arrêt', 'evenement', { joueur: 1 })) +
          texte('Interruption : quand de la menace serait placée sur une manigance, place 1 menace de moins.') +
          choix(btn('Jouer Cran d’arrêt (1 ressource)', 'dore'), btn('Ne rien jouer', 'gris')), { bouton: null }),
        E('1', 'Menace', rangee(mini('m', 'Trafic Clandestin', 'principale')) + calculSimple + ligne('Cran d’arrêt', '−1', { carte: 'evenement', ton: 'vert' }) + total('<s>+1</s> → 0 menace', { ton: 'vert' }) + note('AUCUNE MENACE', 'vert'),
          { montre: [copie('main', 'defausseJ', 'Cran d’arrêt')] }),
      ],
    },
  ]);

  // ===================================================================== ② STADE
  enc('②', '1 Menaces', 'Manigance complétée, changement de stade', [
    'Avant → après en grand, puis la suite.',
    'Dernier stade : écran rouge, puis écran de fin.',
    'Une annexe n’a pas de seuil : pas d’écran pour elle (Rules Reference).',
    'Un écran par chose : avant → après, face A, face B ; un écran sans effet est sauté.',
    'L’ancienne carte part, la nouvelle vole, son jeton de départ vole ensuite.',
    'Le méchant qui change de stade : même écran.',
    'Paquet rencontre vide : petit écran, jeton d’accélération qui vole.',
    'Onglet courant + « (pendant 2A) », puis « la phase continue ».',
    'Carte Victoire X : vers la pile de victoire.',
    'Secousse légère + son (rien en mode sobre).',
  ], [
    {
      nom: 'La principale passe au stade 2',
      table: table('paquet', 'defausse', 'klaw', { ...T.trafic, c: '6/6', rouge: true }, carte('trafic2', 'Distribution d’Armes', 'Principale · stade 2', 'principale', 43, 3, { cache: true, c: '0/12' }), carte('agent', 'Agent de Klaw', 'Attachement', 'attachement', 43, 34), 'retire', 'ironheart'),
      etapes: [
        E('2A', 'Manigance complétée (pendant 2A)', rangee(mini('a', 'Trafic Clandestin', 'principale', { gros: '6/6', grosTon: 'rouge' }), '<span class="fleche">→</span>', mini('b', 'Distribution d’Armes', 'principale', { gros: '0/12' })) +
          ligne('Menace en trop', 'perdue') + ligne('Agent de Klaw (attaché)', 'défaussé', { carte: 'attachement' }) + ligne('Menace de départ : 2 par joueur × 1', '+2', { carte: 'principale', pastilles: [1] }),
          { rouge: true, montre: [{ f: 'secousse' }, halo('trafic', 'rouge')], suite: [part('trafic', 'retire'), part('agent', 'defausse', 100), arrive('trafic2', 'b:b', 250)] }),
        E('2A', 'Distribution d’Armes · menace de départ', rangee(mini('b', 'Distribution d’Armes', 'principale')) + total('+2 menaces') + jauge(0, 2, 12),
          { montre: [trait('boite', 'trafic2'), jeton('j1', 'menace', '+2', 'boite', 'trafic2')], suite: [vole('j1', 'trafic2', '2/12')] }),
        E('2A', 'Face B · Une fois révélée', rangee(mini('b', 'Distribution d’Armes', 'principale'), mini('s', 'Contrebande', 'annexe')) + texte('Une fois révélée : mettez en jeu la manigance annexe Contrebande.') + bandeau('NOUVELLE MANIGANCE'),
          { table: [], montre: [], suite: [] }),
        E('2A', 'La phase continue', note('Retour à l’activation de Klaw.'), { bouton: null }),
      ],
      ajouts: [carte('contrebande', 'Contrebande', 'Annexe', 'annexe', 57, 3, { cache: true, c: '3' })],
    },
    {
      nom: 'Dernier stade : défaite',
      table: table('klaw', { ...T.trafic, nom: 'Distribution d’Armes', c: '12/12', rouge: true }, 'ironheart'),
      etapes: [
        E('2A', 'La manigance est complétée', rangee(mini('a', 'Distribution d’Armes', 'principale', { gros: '12/12', grosTon: 'rouge' })) + `<p class="enorme">Klaw gagne</p>` + note('C’était le dernier stade.'), { rouge: true, montre: [{ f: 'secousse' }, halo('trafic', 'rouge')], bouton: 'Voir la fin de partie' }),
        E('B', 'Fin de partie', note('L’écran de fin de partie s’ouvre (le même qu’après un coup fatal).'), { rouge: true, bouton: null }),
      ],
    },
    {
      nom: 'Le méchant change de stade',
      table: table('klaw', carte('klaw2', 'Klaw', 'Méchant · stade II', 'vilain', 29, 3, { cache: true, c: '30/30' }), 'trafic', carte('sonne', 'Sonné', 'Statut', 'statut', 29, 34), 'ironheart', 'retire', 'defausse'),
      etapes: [
        E('2A', 'Klaw vaincu → Klaw II', rangee(mini('a', 'Klaw I', 'vilain', { gros: '0/24', grosTon: 'rouge' }), '<span class="fleche">→</span>', mini('b', 'Klaw II', 'vilain', { gros: '30/30' })) +
          ligne('Nouvelles stats', 'ATQ 2 → 3 · MAN 2 → 2') + ligne('Sonné', 'retiré', { carte: 'statut' }),
          { montre: [{ f: 'secousse' }, maj('klaw', { c: '0/24', rouge: true })], suite: [part('klaw', 'retire'), part('sonne', 'defausse', 80), arrive('klaw2', 'b:b', 250)] }),
        E('2A', 'Klaw II · Une fois révélé', rangee(mini('b', 'Klaw II', 'vilain')) + texte('Une fois révélé : chaque joueur reçoit 1 carte rencontre.'), {}),
        E('2A', 'La phase continue', note('Dernier stade vaincu : écran de victoire à la place.'), { bouton: null }),
      ],
    },
    {
      nom: 'Paquet rencontre vide',
      table: table({ ...T.paquet, c: '0' }, { ...T.defausse, c: '14' }, 'klaw', 'trafic', 'ironheart'),
      etapes: [
        E('3', 'Paquet rencontre vide', note('La défausse est remélangée pour faire un nouveau paquet.') + ligne('Jeton d’accélération sur la principale', '+1', { carte: 'acceleration' }) + note('À partir de maintenant : +1 menace à chaque étape 1.'),
          { montre: [copie('defausse', 'paquet', '14 cartes'), maj('paquet', { c: '14' }), maj('defausse', { c: '0' }), trait('boite', 'trafic'), jeton('a1', 'acceleration', '', 'boite', 'trafic')], suite: [vole('a1', 'trafic', '1/6 ⚡')] }),
        E('3', 'La phase continue', note('Le jeton d’accélération est posé sur la principale.'), { bouton: null }),
      ],
    },
    {
      nom: 'Carte Victoire vaincue',
      table: table('klaw', 'trafic', carte('garde', 'Garde d’Élite', 'Sbire · Victoire 1', 'sbire', 43, 34, { c: '1/4' }), 'ironheart', 'victoire'),
      etapes: [
        E('2B', 'Riposte', rangee(mini('g', 'Garde d’Élite', 'sbire', { tampon: 'VAINCU' })) + ligne('Ironheart : Riposte 1', '−1') + note('Victoire 1 : la carte va dans la pile de victoire.'),
          { montre: [trait('ironheart', 'garde', 'j1'), jeton('d1', 'degats', '−1', 'ironheart', 'garde')], suite: [vole('d1', 'garde', '0/4'), part('garde', 'victoire', 500)] }),
        E('2B', 'La phase continue', note('La carte est rangée en victoire, pas à la défausse.'), { bouton: null }),
      ],
    },
  ]);

  // ===================================================================== ③ DÉFENSE
  const tableDef = () => table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'brawn', carte('spidey', 'Spider-Woman', 'Alliée · épuisée', 'allie', 57, 72, { joueur: 1, incline: true, c: '3/3' }), { ...T.cap, x: 76 }, 'main');
  const annonce = (o = {}) => rangee(mini('k', 'Klaw', 'vilain'), mini('b1', '', 'boost', { dos: true }), mini('b2', '', 'boost', { dos: true }), '<span class="fleche">→</span>', mini('d1', 'Ironheart', 'heros', { joueur: 1, num: 1 }), mini('d2', 'Brawn', 'allie', { joueur: 1, num: 2 }), mini('d3', 'Spider-Woman', 'allie', { joueur: 1, incline: true, num: 3 })) +
    note('ATQ 2 + 2 boosts cachés') + note('PERÇANT : défausse les cartes Robuste de la cible avant les dégâts.', 'mot-cle') + (o.reac ? '' : '');
  enc('③', '2A Méchant', 'Annonce d’attaque et choix du défenseur', [
    'L’annonce dit l’ATQ, les boosts cachés et les mots-clés actifs, expliqués.',
    'Bouton « Défendre avec X » : la DÉF seule.',
    'Pas de prévision de dégâts.',
    'Défenseur indisponible : grisé avec la raison, carte inclinée.',
    'Interruptions possibles : rangée à part, boutons dorés.',
    'Table : halo vert sur les défenseurs, clic direct.',
    '« Demander à X de défendre » : bouton bleu, avant « Ne pas défendre ».',
    'Un autre joueur choisit : son écran grisé, « X choisit… ».',
    'Pas d’avertissement ni de rappel alter ego.',
  ], [
    {
      nom: 'Solo : héros, allié, allié épuisé',
      table: tableDef(),
      etapes: [
        E('2A', 'Attaque de Klaw', annonce() + choix(btn('Défendre avec Ironheart', 'vert', { def: 3 }), btn('Défendre avec Brawn', 'vert'), btn('Défendre avec Spider-Woman · épuisée', 'vert', { grise: true }), btn('Ne pas défendre (ATQ 2 + 2 boosts)', 'gris')),
          { cadre: 'j1', joueur: 1, bouton: null, montre: [trait('klaw', 'ironheart', 'j1'), halo('ironheart', 'vert'), halo('brawn', 'vert')] }),
        E('2A', 'Ironheart défend', note('Suite : les boosts se retournent (encadré ④).'), { cadre: 'j1', joueur: 1, bouton: null, montre: [trait('klaw', 'ironheart', 'j1')] }),
      ],
    },
    {
      nom: 'Une carte de ta main avant de défendre',
      table: tableDef(),
      etapes: [
        E('2A', 'Attaque de Klaw', annonce() + choix(btn('Défendre avec Ironheart', 'vert', { def: 3 }), btn('Défendre avec Brawn', 'vert')) +
          `<p class="sous-titre-choix">Avant de défendre, tu peux jouer :</p>` + choix(btn('Jouer Bloc (+2 DÉF)', 'dore'), btn('Jouer Repli (annule l’attaque)', 'dore')) + choix(btn('Ne pas défendre (ATQ 2 + 2 boosts)', 'gris')),
          { cadre: 'j1', joueur: 1, bouton: null, montre: [trait('klaw', 'ironheart', 'j1'), halo('ironheart', 'vert'), halo('brawn', 'vert'), halo('main', 'dore')] }),
        E('2A', 'Bloc joué', rangee(mini('bl', 'Bloc', 'evenement', { joueur: 1, gros: '+2 DÉF' })) + note('Ironheart défend avec 5 DÉF.'), { cadre: 'j1', joueur: 1, montre: [copie('main', 'defausseJ', 'Bloc')] }),
      ],
    },
    {
      nom: 'Demander à un ami de défendre',
      table: tableDef(),
      etapes: [
        E('2A', 'Attaque de Klaw', annonce() + choix(btn('Défendre avec Ironheart', 'vert', { def: 3 }), btn('Défendre avec Brawn', 'vert'), btn('Demander à Captain America de défendre', 'bleu'), btn('Ne pas défendre (ATQ 2 + 2 boosts)', 'gris')),
          { cadre: 'j1', joueur: 1, bouton: null, montre: [trait('klaw', 'ironheart', 'j1'), halo('ironheart', 'vert'), halo('brawn', 'vert'), halo('cap', 'bleu')] }),
        E('2A', 'Captain America choisit comment défendre…', note('Chez toi : l’écran de Captain America, grisé, sans bouton.') + rangee(mini('c1', 'Captain America', 'heros', { joueur: 2, pale: true })), { cadre: 'j2', joueur: 2, montre: [trait('cap', 'ironheart', 'j2')] }),
        E('2A', 'Vue de Captain America', note('Chez lui (J2) :') + choix(btn('Défendre pour Ironheart avec Captain America', 'bleu', { def: 3 }), btn('Ne pas défendre', 'gris')), { cadre: 'j2', joueur: 2, bouton: null, montre: [halo('cap', 'vert')] }),
        E('2A', 'Captain America défend', note('L’attaque vise Ironheart, Captain America encaisse.'), { cadre: 'j2', joueur: 2, bouton: null, montre: [trait('klaw', 'cap', 'j2')] }),
      ],
    },
    {
      nom: 'Vue d’un autre joueur',
      table: tableDef(),
      etapes: [
        E('2A', 'Ironheart choisit comment défendre…', rangee(mini('k', 'Klaw', 'vilain'), '<span class="fleche">→</span>', mini('d1', 'Ironheart', 'heros', { joueur: 1, pale: true }), mini('d2', 'Brawn', 'allie', { joueur: 1, pale: true })) + note('Tu vois ses défenseurs en gris, sans pouvoir cliquer.') + choix(btn('Défendre pour Ironheart', 'bleu', { grise: true })) + note('Ce bouton s’allume s’il ne défend pas.'),
          { cadre: 'j1', joueur: 1, bouton: null, montre: [trait('klaw', 'ironheart', 'j1')] }),
      ],
    },
  ]);

  // ===================================================================== ④ RÉSULTAT
  const tableRes = () => table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'brawn', 'main', 'defausseJ', carte('robuste', 'Robuste', 'Statut', 'statut', 29, 46));
  enc('④', '2A Méchant', 'Boosts et résultat de l’attaque', [
    'Tous les boosts arrivent cachés, un clic les retourne ensemble.',
    'Ligne de calcul posée, chaque nombre sous sa carte, puis « X 11 → 9 PV ».',
    'Boosts de même taille que les autres cartes, gros « +2 », ★ doré.',
    'Boost à 0 : « +0 » gris.',
    'Dégâts bloqués ou réduits : ligne barrée et raison ; à 0, « AUCUN DÉGÂT » en vert.',
    'Allié vaincu : tampon, jeton, puis la carte vers la défausse.',
    'Statut ou effet : sous le calcul, la carte statut vole.',
    'Réponse après le résultat : dans la même boîte.',
    'Boosts vers la défausse rencontre au clic.',
    'Héros à 0 PV : calcul en rouge et tampon « K.O. ».',
    'Pied : Continuer seul.',
  ], [
    {
      nom: 'Attaque défendue, 2 boosts',
      table: tableRes(),
      etapes: [
        E('2A', 'Attaque de Klaw', rangee(mini('k', 'Klaw', 'vilain'), mini('b1', '', 'boost', { dos: true }), mini('b2', '', 'boost', { dos: true }), '<span class="fleche">→</span>', mini('d', 'Ironheart', 'heros', { joueur: 1 })) + note('ATQ 2 + 2 boosts cachés · Ironheart défend (DÉF 3)'),
          { cadre: 'j1', joueur: 1, bouton: 'Retourner les boosts', montre: [trait('klaw', 'ironheart', 'j1')] }),
        E('2A', 'Attaque de Klaw', rangee(mini('k', 'Klaw', 'vilain', { gros: '2' }), mini('b1', 'Manipulation du Son', 'boost', { gros: '+2' }), mini('b2', 'Raté', 'boost', { gros: '+0', grosTon: 'gris', pale: true }), '<span class="fleche">→</span>', mini('d', 'Ironheart', 'heros', { joueur: 1, gros: '−3', grosTon: 'vert' })) +
          total('ATQ 2 + 2 + 0 − DÉF 3 = 1 dégât') + ligne('Ironheart', '11 → 10 PV'),
          { cadre: 'j1', joueur: 1, montre: [trait('klaw', 'ironheart', 'j1'), jeton('d1', 'degats', '−1', 'klaw', 'ironheart')], suite: [vole('d1', 'ironheart', '10/11'), copie('b:b1', 'defausse', 'Boost', 0, true), copie('b:b2', 'defausse', 'Boost', 80, true)] }),
        E('2B', 'Sbires', note('Les boosts sont partis à la défausse, Ironheart est à 10.'), { bouton: null }),
      ],
    },
    {
      nom: 'Tout est bloqué (Robuste)',
      table: tableRes(),
      etapes: [
        E('2A', 'Attaque de Klaw', rangee(mini('k', 'Klaw', 'vilain', { gros: '2' }), mini('b1', 'Assaut', 'boost', { gros: '+2' }), '<span class="fleche">→</span>', mini('d', 'Ironheart', 'heros', { joueur: 1 }), mini('r', 'Robuste', 'statut')) +
          total('<s>4 dégâts</s> → 0') + ligne('Robuste : absorbe tous les dégâts, puis est défaussé', '', { carte: 'statut', ton: 'vert' }) + `<p class="enorme vert">AUCUN DÉGÂT</p>`,
          { cadre: 'j1', joueur: 1, montre: [trait('klaw', 'ironheart', 'j1')], suite: [part('robuste', 'defausse')] }),
        E('2B', 'Sbires', note('Pas de jeton : rien n’a été infligé.'), { bouton: null }),
      ],
    },
    {
      nom: 'L’allié meurt, Débordement',
      table: tableRes(),
      etapes: [
        E('2A', 'Attaque de Klaw', rangee(mini('k', 'Klaw', 'vilain', { gros: '4' }), mini('b1', 'Assaut', 'boost', { gros: '+3' }), '<span class="fleche">→</span>', mini('d', 'Brawn', 'allie', { joueur: 1, tampon: 'VAINCU' })) +
          total('ATQ 4 + 3 = 7 dégâts') + ligne('Brawn', '5 → 0 PV', { ton: 'rouge' }) + ligne('DÉBORDEMENT : 2 dégâts en trop → Ironheart', '11 → 9'),
          { cadre: 'j1', joueur: 1, montre: [trait('klaw', 'brawn', 'j1'), trait('brawn', 'ironheart', 'j1'), jeton('d1', 'degats', '−5', 'klaw', 'brawn'), jeton('d2', 'degats', '−2', 'brawn', 'ironheart')], suite: [vole('d1', 'brawn', '0/5'), vole('d2', 'ironheart', '9/11'), part('brawn', 'defausseJ', 500)] }),
        E('2B', 'Sbires', note('Brawn est dans ta défausse.'), { bouton: null }),
      ],
    },
    {
      nom: 'Statut infligé et carte de ta main',
      table: tableRes(),
      etapes: [
        E('2A', 'Attaque de Klaw', rangee(mini('k', 'Klaw', 'vilain', { gros: '2' }), mini('b1', 'Onde de Choc', 'boost', { gros: '+1', etoile: true }), '<span class="fleche">→</span>', mini('d', 'Ironheart', 'heros', { joueur: 1 })) +
          total('ATQ 2 + 1 = 3 dégâts') + ligne('Ironheart', '11 → 8 PV') + ligne('+ SONNÉ', '', { carte: 'statut', ton: 'rouge' }),
          { cadre: 'j1', joueur: 1, montre: [trait('klaw', 'ironheart', 'j1'), jeton('d1', 'degats', '−3', 'klaw', 'ironheart')], suite: [vole('d1', 'ironheart', '8/11'), copie('b:b1', 'ironheart', 'Sonné', 200)] }),
        E('2A', 'Attaque de Klaw', rangee(mini('d', 'Ironheart', 'heros', { joueur: 1, gros: '8/11' })) + note('Tu peux réagir :') + choix(btn('Jouer Adrénaline (soigne 2)', 'dore'), btn('Ne rien jouer', 'gris')),
          { cadre: 'j1', joueur: 1, bouton: null, montre: [halo('main', 'dore')] }),
        E('2A', 'Adrénaline jouée', ligne('Ironheart', '8 → 10 PV', { ton: 'vert' }), { cadre: 'j1', joueur: 1, montre: [copie('main', 'defausseJ', 'Adrénaline'), maj('ironheart', { c: '10/11' })] }),
      ],
    },
    {
      nom: 'Le héros tombe',
      table: table('klaw', 'trafic', { ...T.ironheart, c: '2/11' }),
      etapes: [
        E('2A', 'Attaque de Klaw', rangee(mini('k', 'Klaw', 'vilain', { gros: '3' }), '<span class="fleche">→</span>', mini('d', 'Ironheart', 'heros', { joueur: 1, tampon: 'K.O.' })) + total('3 dégâts', { ton: 'rouge' }) + ligne('Ironheart', '2 → 0 PV', { ton: 'rouge' }),
          { cadre: 'j1', joueur: 1, rouge: true, montre: [trait('klaw', 'ironheart', 'rouge'), jeton('d1', 'degats', '−3', 'klaw', 'ironheart')], suite: [vole('d1', 'ironheart', '0/11', { rouge: true })] }),
        E('2A', 'Coup fatal', note('Solo : écran de fin. Multijoueur : encadré ⑧.'), { rouge: true, bouton: null }),
      ],
    },
  ]);

  // ===================================================================== ⑤ MANIGANCE DU MÉCHANT
  enc('⑤', '2A Méchant', 'Manigance du méchant', [
    'Avant les boosts : MAN, dos des boosts, manigance visée.',
    'Toute valeur réduite est barrée avec sa carte.',
    'Le reste suit ① et ④ (calcul, jeton, halo, boosts, pied).',
    'Boost ★ qui met en jeu : place en pointillés, la carte arrive au clic.',
  ], [
    {
      nom: 'Avec un boost ★ qui met un sbire en jeu',
      table: table('paquet', 'defausse', 'klaw', { ...T.trafic, nom: 'Distribution d’Armes', c: '2/12' }, carte('trafiquant', 'Trafiquant d’Armes', 'Sbire', 'sbire', 43, 34, { cache: true, c: '3/3', joueur: 1 }), 'ironheart'),
      etapes: [
        E('2A', 'Manigance de Klaw', rangee(mini('k', 'Klaw', 'vilain'), mini('b1', '', 'boost', { dos: true }), '<span class="fleche">→</span>', mini('m', 'Distribution d’Armes', 'principale')) + note('MAN 2 + 1 boost caché'),
          { bouton: 'Retourner le boost', montre: [halo('trafic'), trait('boite', 'trafic')] }),
        E('2A', 'Manigance de Klaw', rangee(mini('k', 'Klaw', 'vilain', { gros: '2' }), mini('b1', 'Trafiquant d’Armes', 'boost', { gros: '+1', etoile: true })) + bandeau('NOUVEAU SBIRE · entre en jeu, s’activera en 2B') +
          total('MAN 2 + 1 = +3 menaces') + jauge(2, 5, 12),
          { montre: [halo('trafic'), place('trafiquant'), trait('boite', 'trafic'), trait('b:b1', 'trafiquant', 'j1'), jeton('j1', 'menace', '+3', 'boite', 'trafic')], suite: [vole('j1', 'trafic', '5/12'), arrive('trafiquant', 'b:b1')] }),
        E('2B', 'Sbires', note('Le jeton s’est posé, le sbire a volé de la boîte à sa place.'), { bouton: null }),
      ],
    },
  ]);

  // ===================================================================== ⑥ ★ DIFFÉRÉ
  enc('⑥', '2A Méchant', 'Effet ★ différé', [
    'La carte ★, son texte, et ce qui s’est passé.',
    '« Au hasard » : dos mélangés, puis la carte tirée.',
    'Effet à choix : dans l’écran ★, sous son texte.',
    'Plusieurs ★ à effet : un écran chacun.',
    '★ sans effet : une ligne sur l’écran du résultat.',
  ], [
    {
      nom: 'Défausse au hasard',
      table: table('klaw', 'ironheart', { ...T.main, c: '5' }, 'defausseJ'),
      etapes: [
        E('2A', 'Boost ★ : Sonic Boom', rangee(mini('s', 'Sonic Boom', 'boost', { etoile: true })) + texte('Boost ★ : si cette attaque inflige des dégâts, défaussez 1 carte au hasard de votre main.') + note('Ironheart a subi des dégâts →') +
          `<div class="melange">${[1, 2, 3, 4, 5].map((i) => `<span class="dos-main" style="--i:${i}"></span>`).join('')}<span class="tiree">Bouclier</span></div>`,
          { cadre: 'j1', joueur: 1, montre: [halo('main', 'rouge')], suite: [copie('main', 'defausseJ', 'Bouclier'), maj('main', { c: '4' })] }),
        E('2A', 'La phase continue', note('Bouclier est dans ta défausse.'), { bouton: null }),
      ],
    },
    {
      nom: 'Effet à choix',
      table: table('klaw', 'ironheart', 'brawn', 'main'),
      etapes: [
        E('2A', 'Boost ★ : Ondes Graves', rangee(mini('s', 'Ondes Graves', 'boost', { etoile: true })) + texte('Boost ★ : choisissez : subir 2 dégâts, ou épuiser un allié.') + choix(btn('Subir 2 dégâts', 'gris'), btn('Épuiser un allié', 'gris')) + note('Tu peux aussi cliquer l’allié directement sur la table.', 'astuce'),
          { cadre: 'j1', joueur: 1, bouton: null, montre: [halo('brawn', 'dore')] }),
        E('2A', 'Brawn épuisé', note('Brawn est incliné sur la table.'), { montre: [maj('brawn', { incline: true })] }),
      ],
    },
    {
      nom: 'Sans effet (une ligne)',
      table: table('klaw', 'ironheart'),
      etapes: [
        E('2A', 'Attaque de Klaw', rangee(mini('k', 'Klaw', 'vilain', { gros: '2' }), mini('b1', 'Sonic Boom', 'boost', { gros: '+1', etoile: true }), '<span class="fleche">→</span>', mini('d', 'Ironheart', 'heros', { joueur: 1 })) + total('<s>3 dégâts</s> → 0') + ligne('DÉF 3 bloque 3', '') + note('★ Sonic Boom : sans effet (aucun dégât)', 'gris'),
          { cadre: 'j1', joueur: 1, montre: [trait('klaw', 'ironheart', 'j1')] }),
      ],
    },
  ]);

  // ===================================================================== ⑦ RIPOSTE
  const fondeur = carte('fondeur', 'Le Fondeur', 'Sbire', 'sbire', 43, 34, { c: '4/4', joueur: 1 });
  enc('⑦', '2B Sbires', 'Riposte', [
    'Écran juste après le résultat, trait inverse.',
    'Une ligne par source, total, un seul jeton (les valeurs s’additionnent).',
    'Sbire achevé : tampon, puis la carte vers la défausse ; son « Une fois vaincu » ensuite.',
  ], [
    {
      nom: 'Deux sources de Riposte',
      table: table('klaw', 'trafic', fondeur, 'ironheart', carte('armure', 'Armure Mk V', 'Amélioration', 'amelioration', 43, 68, { joueur: 1 })),
      etapes: [
        E('2B', 'Riposte', rangee(mini('d', 'Ironheart', 'heros', { joueur: 1 }), '<span class="fleche">→</span>', mini('f', 'Le Fondeur', 'sbire')) + ligne('Ironheart : Riposte 1', '1', { carte: 'heros' }) + ligne('Armure Mk V : Riposte 1', '1', { carte: 'amelioration' }) + total('2 dégâts au Fondeur') + ligne('Le Fondeur', '4 → 2 PV'),
          { cadre: 'j1', joueur: 1, montre: [trait('ironheart', 'fondeur', 'j1'), jeton('d1', 'degats', '−2', 'ironheart', 'fondeur')], suite: [vole('d1', 'fondeur', '2/4')] }),
        E('2B', 'La phase continue', note('Le Fondeur est à 2.'), { bouton: null }),
      ],
    },
    {
      nom: 'Le sbire est vaincu',
      table: table('klaw', 'trafic', { ...fondeur, c: '1/4' }, 'ironheart', 'defausse'),
      etapes: [
        E('2B', 'Riposte', rangee(mini('d', 'Ironheart', 'heros', { joueur: 1 }), '<span class="fleche">→</span>', mini('f', 'Le Fondeur', 'sbire', { tampon: 'VAINCU' })) + ligne('Ironheart : Riposte 1', '1') + ligne('Le Fondeur', '1 → 0 PV', { ton: 'rouge' }),
          { cadre: 'j1', joueur: 1, montre: [trait('ironheart', 'fondeur', 'j1'), jeton('d1', 'degats', '−1', 'ironheart', 'fondeur')], suite: [vole('d1', 'fondeur', '0/4'), part('fondeur', 'defausse', 500)] }),
        E('2B', 'Le Fondeur · Une fois vaincu', texte('Une fois vaincu : retirez 1 menace de la manigance principale.') + total('−1 menace', { ton: 'vert' }), { montre: [maj('trafic', { c: '0/6' })] }),
      ],
    },
  ]);

  // ===================================================================== ⑧ ÉLIMINÉ
  const tableMulti = () => table('klaw', 'trafic', 'ironheart', { ...T.cap, c: '0/11' }, carte('requin', 'Le Requin-Tigre', 'Sbire', 'sbire', 64, 34, { c: '4/4', joueur: 2 }), carte('jeton1', '1er joueur', 'Jeton', 'jeton', 78, 68, { joueur: 2 }));
  enc('⑧', '2A Méchant', 'Héros éliminé (multijoueur)', [
    'Écran dédié : « X ÉLIMINÉ », ses sbires vers leur nouveau joueur, jeton premier joueur, « la phase continue ».',
    'Il gagne ou perd avec le groupe : c’est dit.',
    'Ses cartes s’effacent ensemble au clic.',
    'Ses cartes rencontre non révélées : rien à montrer.',
    'Toi éliminé : mode spectateur clair.',
  ], [
    {
      nom: 'Un autre joueur est éliminé',
      table: tableMulti(),
      etapes: [
        E('2A', 'Captain America éliminé', rangee(mini('c', 'Captain America', 'heros', { joueur: 2, tampon: 'ÉLIMINÉ', tamponTon: 'rouge' })) + ligne('Le Requin-Tigre', 'passe à Ironheart', { carte: 'sbire' }) + ligne('Jeton premier joueur', 'passe à Ironheart', { carte: 'jeton' }) + note('Il reste dans la partie : il gagne ou perd avec son équipe.') + note('La phase continue.'),
          { cadre: 'j2', joueur: 2, rouge: true, montre: [trait('requin', 'ironheart', 'j1'), trait('jeton1', 'ironheart', 'j1')], suite: [{ f: 'fondu', cartes: ['cap'] }, maj('requin', { x: 43 }), copie('requin', 'ironheart', 'Requin-Tigre'), copie('jeton1', 'ironheart', '1er joueur', 100), { f: 'fondu', cartes: ['jeton1'] }] }),
        E('2B', 'Sbires', note('Le Requin-Tigre est maintenant engagé avec Ironheart.'), { bouton: null }),
      ],
    },
    {
      nom: 'C’est toi qui es éliminé',
      table: tableMulti(),
      etapes: [
        E('2A', 'Tu es éliminé', rangee(mini('c', 'Captain America', 'heros', { joueur: 2, tampon: 'ÉLIMINÉ', tamponTon: 'rouge' })) + note('Tu restes dans la partie : tu gagnes ou tu perds avec ton équipe.') + note('Tu regardes la suite.'),
          { cadre: 'j2', joueur: 2, rouge: true, suite: [{ f: 'fondu', cartes: ['cap'] }] }),
        E('2B', 'Ironheart choisit l’ordre des sbires…', note('Tu suis chaque écran, sans bouton.') + `<p class="discret"><button class="lien" type="button">Quitter la partie</button></p>`, { cadre: 'j1', joueur: 1, bouton: null }),
      ],
    },
  ]);

  // ===================================================================== ⑨ 2E ACTIVATION
  enc('⑨', '2A Méchant', 'Deuxième activation', [
    'Annonce sur la carte qui la cause, puis un écran à part.',
    'Titre « Attaque de Klaw (2e, Hydra Jet-Trooper) », frise sur 2A.',
    'Causée en étape 3 : sous la carte qui l’a causée, frise sur 3.',
    'Le reste suit ③ ④ ⑤.',
  ], [
    {
      nom: 'Un boost fait réattaquer',
      table: table('klaw', 'trafic', 'ironheart'),
      etapes: [
        E('2A', 'Attaque de Klaw', rangee(mini('b1', 'Hydra Jet-Trooper', 'boost', { gros: '+1' })) + note('Klaw attaquera encore après cette attaque.', 'dore'), { montre: [trait('klaw', 'ironheart', 'j1')] }),
        E('2A', 'Attaque de Klaw (2e, Hydra Jet-Trooper)', annonce() + choix(btn('Défendre avec Ironheart', 'vert', { def: 3 }), btn('Ne pas défendre', 'gris')), { cadre: 'j1', joueur: 1, bouton: null, montre: [trait('klaw', 'ironheart', 'j1'), halo('ironheart', 'vert')] }),
      ],
    },
    {
      nom: 'Causée par une carte révélée',
      table: table('klaw', 'trafic', 'ironheart'),
      etapes: [
        E('3', 'Attaque de Klaw (Explosion Sonique)', rangee(mini('t', 'Explosion Sonique', 'traitrise'), mini('k', 'Klaw', 'vilain')) + texte('Une fois révélée : Klaw vous attaque.') + choix(btn('Défendre avec Ironheart', 'vert', { def: 3 }), btn('Ne pas défendre', 'gris')),
          { cadre: 'j1', joueur: 1, sous: 'Carte rencontre 1/1 · Ironheart', bouton: null, montre: [trait('klaw', 'ironheart', 'j1')] }),
      ],
    },
  ]);

  // ===================================================================== ⑩ ORDRE DES SBIRES
  const sbires = () => [carte('s1', 'Le Fondeur', 'Sbire', 'sbire', 36, 34, { c: '4/4', joueur: 1 }), carte('s2', 'Le Tourbillon', 'Sbire · Sonné', 'sbire', 50, 34, { c: '3/3', joueur: 1 }), carte('s3', 'L’Homme-Radioactif', 'Sbire', 'sbire', 64, 34, { c: '5/5', joueur: 1 })];
  enc('⑩', '2B Sbires', 'Ordre et enchaînement des sbires', [
    'Sbires identiques : pas de question, ordre de la table annoncé.',
    'Juste les cartes à ordonner.',
    'Numéros 1, 2, 3 sur la table pendant 2B, « Sbire 2/3 » dans le titre, numéro barré une fois passé.',
    'Aucun sbire : onglet 2B grisé et sauté.',
    'Sonné (n’empêche que l’attaque) ou Désorienté (que la manigance) : écran court « ne fait rien ».',
    'Activations chez plusieurs joueurs : le premier joueur range, vignettes bordées de la couleur du joueur visé.',
  ], [
    {
      nom: 'Choisir l’ordre puis l’enchaîner',
      table: table('klaw', 'trafic', 'ironheart', ...sbires()),
      etapes: [
        E('2B', 'Choisir l’ordre', rangee(mini('a', 'Le Fondeur', 'sbire', { num: 1 }), mini('b', 'Le Tourbillon', 'sbire', { num: 2 }), mini('c', 'L’Homme-Radioactif', 'sbire', { num: 3 })) + note('Tu peux aussi cliquer les cartes directement sur la table.', 'astuce') + choix(btn('Ordre de la table', 'gris'), btn('Confirmer', 'dore')),
          { cadre: 'j1', joueur: 1, bouton: null, montre: [halo('s1', 'dore'), halo('s2', 'dore'), halo('s3', 'dore')] }),
        E('2B', 'Attaque du Fondeur (sbire 1/3)', note('Comme en 2A : annonce, défense, boosts, résultat.'), { cadre: 'j1', joueur: 1, montre: [maj('s1', { marque: '1', haloGarde: true }), maj('s2', { marque: '2' }), maj('s3', { marque: '3' }), halo('s1', 'rouge'), trait('s1', 'ironheart', 'j1')] }),
        E('2B', 'Le Tourbillon est Sonné (sbire 2/3)', rangee(mini('b', 'Le Tourbillon', 'sbire'), mini('st', 'Sonné', 'statut')) + note('Il n’attaque pas : il défausse son statut à la place.'),
          { cadre: 'j1', joueur: 1, montre: [maj('s1', { marque: '<s>1</s>' }), halo('s2', 'acier')], suite: [copie('b:st', 'paquet', 'Sonné', 0, true), maj('s2', { sous: 'Sbire', marque: '<s>2</s>' })] }),
        E('2B', 'Attaque de L’Homme-Radioactif (sbire 3/3)', note('Le dernier de l’ordre.'), { cadre: 'j1', joueur: 1, bouton: null, montre: [trait('s3', 'ironheart', 'j1')] }),
      ],
    },
    {
      nom: 'Aucun sbire',
      table: table('klaw', 'trafic', 'ironheart'),
      etapes: [E('3', 'Distribution', note('L’onglet 2B est grisé « — » : on passe directement à l’étape 3.'), { ongletsVides: ['2B'], bouton: null })],
    },
    {
      nom: 'Plusieurs joueurs (le premier range)',
      table: table('klaw', 'trafic', 'ironheart', 'cap', carte('s1', 'Le Fondeur', 'Sbire', 'sbire', 36, 34, { joueur: 1 }), carte('s3', 'Le Requin-Tigre', 'Sbire', 'sbire', 64, 34, { joueur: 2 })),
      etapes: [
        E('2B', 'Choisis l’ordre des activations', rangee(mini('a', 'Le Fondeur → Ironheart', 'sbire', { joueur: 1, raye: true, num: 1 }), mini('b', 'Le Requin-Tigre → Cap', 'sbire', { joueur: 2, raye: true, num: 2 })) + note('Les autres voient « Ironheart choisit l’ordre… ».') + choix(btn('Confirmer', 'dore')),
          { cadre: 'j1', joueur: 1, bouton: null, montre: [trait('s1', 'ironheart', 'j1'), trait('s3', 'cap', 'j2')] }),
      ],
    },
  ]);

  // ===================================================================== ⑪ DISTRIBUTION
  const dos = (id, x, y) => carte(id, '', 'Carte rencontre', 'dos', x, y, { cache: true, dos: true });
  enc('⑪', '3 Cartes rencontre', 'Distribution', [
    'Titre « Distribution : 3 cartes rencontre », une ligne par joueur avec pastille.',
    'Raisons en petite carte source avec icône (Danger…).',
    'Les dos volent du paquet vers chaque joueur au clic et y restent jusqu’à leur révélation.',
    'Solo avec une seule carte et sans raison : écran sauté, le dos vole quand même.',
  ], [
    {
      nom: 'Deux joueurs et un Danger',
      table: table('paquet', 'defausse', 'klaw', 'trafic', { ...T.reseau, sous: 'Annexe ☠ Danger' }, 'ironheart', 'cap', dos('d1', 36, 50), dos('d2', 44, 50), dos('d3', 71, 50)),
      etapes: [
        E('3', 'Distribution : 3 cartes rencontre', ligne('Ironheart : 1 + Danger de Réseau de Distribution', '2', { pastilles: [1], carte: 'annexe' }) + ligne('Captain America : 1', '1', { pastilles: [2] }),
          { suite: [arrive('d1', 'paquet', 0, { dos: true }), arrive('d2', 'paquet', 150, { dos: true }), arrive('d3', 'paquet', 300, { dos: true })] }),
        E('3', 'Carte rencontre 1/2 · Ironheart', note('Les dos attendent devant chaque joueur.'), { joueur: 1, cadre: 'j1', bouton: null }),
      ],
    },
    {
      nom: 'Solo, une seule carte',
      table: table('paquet', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50)),
      etapes: [
        E('2B', 'Dernier sbire', note('Pas d’écran de distribution : au clic, le dos vole vers toi et on passe à sa révélation.'), { suite: [arrive('d1', 'paquet', 0, { dos: true })] }),
        E('3', 'Carte rencontre 1/1 · Ironheart', note('Écran suivant : sa révélation.'), { joueur: 1, cadre: 'j1', bouton: null }),
      ],
    },
  ]);

  // ===================================================================== ⑫ TRAÎTRISE
  const tableT = () => table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'brawn', 'main', 'defausseJ', dos('d1', 36, 50));
  const revele = (titre, nom, type, contenu, o = {}) => [
    E('3', titre, rangee(mini('t', '', type, { dos: true })) + note('Clique pour la retourner.'), { joueur: 1, cadre: 'j1', sous: '', bouton: 'Retourner la carte', montre: [maj('d1', { cache: false }), trait('d1', 'boite', 'j1')], suite: [maj('d1', { cache: true })] }),
    E('3', titre, contenu, { joueur: 1, cadre: 'j1', sous: `${nom} (${type === 'traitrise' ? 'traîtrise' : type})`, ...o }),
  ];
  enc('⑫', '3 Cartes rencontre', 'Traîtrise révélée', [
    'Titre « Carte rencontre 1/2 · Ironheart », la carte dessous ; compte par joueur.',
    'Dos, puis retournement au premier clic.',
    'Texte de la carte (branche non appliquée en gris) et « → ce qui s’est passé ».',
    'Choix : boutons avec le texte de la carte seul.',
    'Annulée : tampon « ANNULÉE ».',
    'Puis vers la défausse rencontre au clic.',
    'Touche tous les joueurs : une ligne et un jeton par joueur.',
    'Recherche : « Aucun trouvé » et « paquet mélangé », ou la carte trouvée qui vole.',
    'Effet compté : « 3 sbires × 1 = 3 dégâts ».',
    'Sans effet : écran gardé, « Sans effet » en vert.',
    'Péril : « PÉRIL : Ironheart est seul », les cartes des autres grisées.',
  ], [
    {
      nom: 'Dégâts, cas simple',
      table: tableT(),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Explosion Sonique', 'traitrise',
          rangee(mini('t', 'Explosion Sonique', 'traitrise')) + texte('Une fois révélée : subissez 2 dégâts. <span class="gris">Si vous êtes en alter ego, placez 1 menace à la place.</span>') + total('→ Ironheart subit 2 dégâts') + ligne('Ironheart', '11 → 9 PV'),
          { montre: [trait('b:t', 'ironheart', 'j1'), jeton('d1j', 'degats', '−2', 'b:t', 'ironheart')], suite: [vole('d1j', 'ironheart', '9/11'), copie('b:t', 'defausse', 'Explosion Sonique', 100, true)] }),
        E('B', 'Bilan', note('La traîtrise est dans la défausse rencontre.'), { bouton: null }),
      ],
    },
    {
      nom: 'Tous les joueurs',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'cap', dos('d1', 36, 50)),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Onde Sonore', 'traitrise',
          rangee(mini('t', 'Onde Sonore', 'traitrise')) + texte('Une fois révélée : chaque joueur subit 1 dégât.') + ligne('Ironheart', '11 → 10', { pastilles: [1] }) + ligne('Captain America', '11 → 10', { pastilles: [2] }),
          { montre: [trait('b:t', 'ironheart', 'j1'), trait('b:t', 'cap', 'j2'), jeton('a', 'degats', '−1', 'b:t', 'ironheart'), jeton('b', 'degats', '−1', 'b:t', 'cap')], suite: [vole('a', 'ironheart', '10/11'), vole('b', 'cap', '10/11'), copie('b:t', 'defausse', 'Onde Sonore', 100, true)] }),
        E('B', 'Bilan', note('Deux jetons partis au même clic.'), { bouton: null }),
      ],
    },
    {
      nom: 'Traîtrise à choix',
      table: tableT(),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Pression', 'traitrise',
          rangee(mini('t', 'Pression', 'traitrise')) + texte('Une fois révélée : choisissez :') + choix(btn('Subir 3 dégâts', 'gris'), btn('Défausser 2 cartes de votre main', 'gris')),
          { bouton: null }),
        E('3', 'Pression', total('→ Ironheart subit 3 dégâts') + ligne('Ironheart', '11 → 8'), { joueur: 1, cadre: 'j1', montre: [trait('boite', 'ironheart', 'j1'), jeton('x', 'degats', '−3', 'boite', 'ironheart')], suite: [vole('x', 'ironheart', '8/11')] }),
      ],
    },
    {
      nom: 'Effet compté',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50), ...sbires()),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Encerclé', 'traitrise',
          rangee(mini('t', 'Encerclé', 'traitrise')) + texte('Une fois révélée : subissez 1 dégât par sbire engagé avec vous.') + rangee(mini('a', 'Le Fondeur', 'sbire'), mini('b', 'Le Tourbillon', 'sbire'), mini('c', 'L’Homme-Radioactif', 'sbire')) + total('3 sbires × 1 = 3 dégâts'),
          { montre: [halo('s1'), halo('s2'), halo('s3'), trait('b:t', 'ironheart', 'j1'), jeton('x', 'degats', '−3', 'b:t', 'ironheart')], suite: [vole('x', 'ironheart', '8/11')] }),
      ],
    },
    {
      nom: 'Sans effet',
      table: tableT(),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Filature', 'traitrise',
          rangee(mini('t', 'Filature', 'traitrise')) + texte('<span class="gris">Une fois révélée : si vous êtes en alter ego, placez 2 menaces sur la principale.</span>') + `<p class="enorme vert">Sans effet : tu es en héros</p>`,
          { suite: [copie('b:t', 'defausse', 'Filature', 0, true)] }),
      ],
    },
    {
      nom: 'Recherche : trouvée',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50), carte('trouve', 'Le Requin-Tigre', 'Sbire', 'sbire', 50, 34, { cache: true, c: '4/4', joueur: 1 })),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Maîtres du Chaos', 'traitrise',
          rangee(mini('t', 'Maîtres du Chaos', 'traitrise')) + texte('Une fois révélée : <span class="gris">chaque sbire Maîtres du Mal attaque. Si aucune attaque n’a lieu,</span> cherchez un sbire Maîtres du Mal dans le paquet ou la défausse et mettez-le en jeu, engagé avec vous.') + note('Aucun sbire engagé : recherche.') + bandeau('TROUVÉ : Le Requin-Tigre · NOUVEAU SBIRE') + note('Paquet rencontre mélangé.'),
          { montre: [place('trouve'), trait('paquet', 'trouve', 'j1')], suite: [arrive('trouve', 'paquet')] }),
      ],
    },
    {
      nom: 'Recherche : rien trouvé',
      table: tableT(),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Maîtres du Chaos', 'traitrise',
          rangee(mini('t', 'Maîtres du Chaos', 'traitrise')) + texte('Une fois révélée : … cherchez un sbire Maîtres du Mal dans le paquet ou la défausse.') + note('Recherche dans le paquet et la défausse : aucun sbire Maîtres du Mal.') + note('Paquet rencontre mélangé.'),
          { montre: [halo('paquet'), halo('defausse')], suite: [copie('b:t', 'defausse', 'Maîtres du Chaos', 0, true)] }),
      ],
    },
    {
      nom: 'Tu peux l’annuler',
      table: tableT(),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Explosion Sonique', 'traitrise',
          rangee(mini('t', 'Explosion Sonique', 'traitrise')) + texte('Une fois révélée : subissez 2 dégâts.') + note('Tu peux réagir :') + choix(btn('Jouer Contre-mesure (annule la carte)', 'dore'), btn('Ne rien jouer', 'gris')),
          { bouton: null, reponse: 'Contre-mesure', montre: [halo('main', 'dore')] }),
        E('3', 'Carte rencontre 1/1 · Ironheart', rangee(mini('t', 'Explosion Sonique', 'traitrise', { tampon: 'ANNULÉE', tamponTon: 'rouge' }), mini('cm', 'Contre-mesure', 'evenement', { joueur: 1 })) + note('Aucun effet.'),
          { joueur: 1, cadre: 'j1', sous: 'Explosion Sonique (traîtrise)', montre: [copie('main', 'defausseJ', 'Contre-mesure')], suite: [copie('b:t', 'defausse', 'Explosion Sonique', 0, true)] }),
      ],
    },
    {
      nom: 'Péril (multijoueur)',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'cap', dos('d1', 36, 50)),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Embuscade', 'traitrise',
          bandeau('PÉRIL : Ironheart est seul') + rangee(mini('t', 'Embuscade', 'traitrise')) + texte('Péril. Une fois révélée : subissez 4 dégâts, sauf si vous défaussez un allié.') + note('Les autres joueurs ne peuvent rien jouer : leurs cartes sont grisées chez eux.'),
          { montre: [maj('cap', { grise: true }), trait('b:t', 'ironheart', 'j1')] }),
      ],
    },
  ]);

  // ===================================================================== ⑬ SBIRE RÉVÉLÉ
  enc('⑬', '3 Cartes rencontre', 'Sbire révélé', [
    'Bandeau « NOUVEAU SBIRE · engagé avec X », puis son « Une fois révélé » sur le même écran.',
    'Mots-clés expliqués en une ligne.',
    'Place en pointillés, trait dans la couleur du joueur, la carte vole au clic.',
    'Rapide : annonce, puis écran d’attaque titré « Attaque Rapide ».',
  ], [
    {
      nom: 'Avec Garde et « Une fois révélé »',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50), carte('garde', 'Garde Blindé', 'Sbire · Garde', 'sbire', 50, 34, { cache: true, c: '3/3', joueur: 1 })),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Garde Blindé', 'sbire',
          rangee(mini('t', 'Garde Blindé', 'sbire')) + bandeau('NOUVEAU SBIRE · engagé avec Ironheart') + note('GARDE : tu ne peux pas attaquer Klaw tant qu’il est là.', 'mot-cle') + texte('Une fois révélé : placez 1 menace sur la principale.') + total('+1 menace'),
          { montre: [place('garde'), trait('b:t', 'garde', 'j1'), trait('boite', 'trafic'), jeton('m', 'menace', '+1', 'boite', 'trafic')], suite: [arrive('garde', 'b:t'), vole('m', 'trafic', '2/6')] }),
      ],
    },
    {
      nom: 'Rapide',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50), carte('rapide', 'Mercenaire', 'Sbire · Rapide', 'sbire', 50, 34, { cache: true, c: '2/2', joueur: 1 })),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Mercenaire', 'sbire',
          rangee(mini('t', 'Mercenaire', 'sbire')) + bandeau('NOUVEAU SBIRE · engagé avec Ironheart') + note('RAPIDE : il attaque tout de suite.', 'mot-cle'),
          { montre: [place('rapide'), trait('b:t', 'rapide', 'j1')], suite: [arrive('rapide', 'b:t')] }),
        E('3', 'Attaque Rapide du Mercenaire', choix(btn('Défendre avec Ironheart', 'vert', { def: 3 }), btn('Ne pas défendre', 'gris')), { joueur: 1, cadre: 'j1', bouton: null, montre: [trait('rapide', 'ironheart', 'j1'), halo('ironheart', 'vert')] }),
      ],
    },
  ]);

  // ===================================================================== ⑭ ANNEXE / ATTACHEMENT / ENVIRONNEMENT
  enc('⑭', '3 Cartes rencontre', 'Annexe, attachement ou environnement révélé', [
    'Annexe : menace de départ calculée et icônes expliquées ; la carte vole, puis son jeton.',
    'Attachement : trait vers sa cible, stat avant → après ; il se glisse sous la carte.',
    'Environnement : « NOUVEL ENVIRONNEMENT », son effet permanent en une ligne.',
  ], [
    {
      nom: 'Manigance annexe',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'cap', dos('d1', 36, 50), carte('annexe', 'Bombe à Retardement', 'Annexe 🔺', 'annexe', 57, 3, { cache: true, c: '0' })),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Bombe à Retardement', 'annexe',
          rangee(mini('t', 'Bombe à Retardement', 'annexe')) + bandeau('NOUVELLE MANIGANCE') + ligne('Menace de départ : 3 par joueur × 2', '6', { pastilles: [1, 2] }) + note('🔺 Crise : impossible de contrecarrer la principale tant qu’elle est là.', 'mot-cle'),
          { montre: [place('annexe'), trait('b:t', 'annexe')], suite: [arrive('annexe', 'b:t')] }),
        E('3', 'Bombe à Retardement · menace de départ', total('+6 menaces'), { montre: [trait('boite', 'annexe'), jeton('m', 'menace', '+6', 'boite', 'annexe')], suite: [vole('m', 'annexe', '6')] }),
      ],
    },
    {
      nom: 'Attachement',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50), carte('att', 'Armure Sonique', 'Attachement', 'attachement', 29, 34, { cache: true })),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Armure Sonique', 'attachement',
          rangee(mini('t', 'Armure Sonique', 'attachement'), '<span class="fleche">→</span>', mini('k', 'Klaw', 'vilain')) + bandeau('S’ATTACHE À KLAW') + ligne('Klaw', 'ATQ 2 → 3'),
          { montre: [place('att'), trait('b:t', 'klaw')], suite: [arrive('att', 'b:t'), maj('klaw', { sous: 'Méchant · ATQ 3' })] }),
      ],
    },
    {
      nom: 'Environnement',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50), carte('env', 'Entrepôt', 'Environnement', 'environnement', 71, 34, { cache: true })),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Entrepôt', 'environnement',
          rangee(mini('t', 'Entrepôt', 'environnement')) + bandeau('NOUVEL ENVIRONNEMENT') + note('Tant qu’il est en jeu : chaque sbire gagne +1 PV.', 'mot-cle'),
          { montre: [place('env'), trait('b:t', 'env')], suite: [arrive('env', 'b:t')] }),
      ],
    },
  ]);

  // ===================================================================== ⑮ OBLIGATION
  enc('⑮', '3 Cartes rencontre', 'Obligation', [
    '« TON OBLIGATION » dans ta couleur ; chez les autres « Obligation de X ».',
    'Dos, retournement, texte et « → ce qui s’est passé ».',
    'Choix : boutons avec le texte de la carte.',
    'Si elle reste en jeu : place en pointillés dans TA zone ; sinon vers la défausse.',
  ], [
    {
      nom: 'Ton obligation, à choix',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50), carte('oblig', 'Pression Familiale', 'Obligation', 'obligation', 43, 50, { cache: true, joueur: 1 })),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Pression Familiale', 'obligation',
          `<div class="bandeau-joueur" style="--joueur:var(--j1)">TON OBLIGATION</div>` + rangee(mini('t', 'Pression Familiale', 'obligation', { joueur: 1 })) + texte('Une fois révélée : épuisez votre identité, ou laissez cette carte en jeu (elle vous coûte 1 ressource par tour).') + choix(btn('Épuiser Ironheart', 'gris'), btn('La laisser en jeu', 'gris')),
          { bouton: null }),
        E('3', 'Pression Familiale', note('Elle reste en jeu, dans ta zone.'), { joueur: 1, cadre: 'j1', montre: [place('oblig'), trait('boite', 'oblig', 'j1')], suite: [arrive('oblig', 'boite')] }),
      ],
    },
    {
      nom: 'L’obligation d’un autre',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', 'cap'),
      etapes: [
        E('3', 'Carte rencontre 1/1 · Captain America', `<div class="bandeau-joueur" style="--joueur:var(--j2)">Obligation de Captain America</div>` + rangee(mini('t', 'Devoir de Soldat', 'obligation', { joueur: 2, pale: true })) + note('Captain America choisit…'), { joueur: 2, cadre: 'j2', sous: 'Devoir de Soldat (obligation)', bouton: null }),
      ],
    },
  ]);

  // ===================================================================== ⑯ RENFORT
  enc('⑯', '3 Cartes rencontre', 'Renfort', [
    'Titre « Carte rencontre 2/2 · Ironheart (Renfort) » ; le total du joueur monte dès que le Renfort est connu.',
    'Flèche de la carte à Renfort vers celle qu’elle ajoute.',
  ], [
    {
      nom: 'Une carte à Renfort',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', dos('d1', 36, 50)),
      etapes: [
        ...revele('Carte rencontre 1/1 · Ironheart', 'Agent Double', 'traitrise',
          rangee(mini('t', 'Agent Double', 'traitrise')) + texte('Renfort. Une fois révélée : placez 1 menace sur la principale.') + note('RENFORT : une carte de plus pour Ironheart.', 'mot-cle') + total('+1 menace'),
          { montre: [trait('boite', 'trafic'), jeton('m', 'menace', '+1', 'boite', 'trafic')], suite: [vole('m', 'trafic', '2/6')] }),
        E('3', 'Carte rencontre 2/2 · Ironheart (Renfort)', rangee(mini('a', 'Agent Double', 'traitrise', { pale: true }), '<span class="fleche dore">→</span>', mini('t', '', 'traitrise', { dos: true })) + note('Le total est passé de 1/1 à 2/2.'),
          { joueur: 1, cadre: 'j1', bouton: 'Retourner la carte', montre: [trait('b:a', 'b:t', 'dore')] }),
      ],
    },
  ]);

  // ===================================================================== ⑰ ANNULÉE
  enc('⑰', '3 Cartes rencontre', 'Carte annulée et remplacée', [
    'Tampon « ANNULÉE » et la carte qui annule à côté.',
    'La carte annulée vole vers la défausse au clic.',
    'Une remplaçante dit « (remplace X) ».',
  ], [
    {
      nom: 'Annulée puis remplacée',
      table: table('paquet', 'defausse', 'klaw', 'trafic', 'ironheart', carte('cuckoos', 'Stepford Cuckoos', 'Alliée', 'allie', 43, 68, { joueur: 1 })),
      etapes: [
        E('3', 'Carte rencontre 1/2 · Ironheart', rangee(mini('t', 'Trafiquant', 'sbire', { tampon: 'ANNULÉE', tamponTon: 'rouge' }), mini('c', 'Stepford Cuckoos', 'allie', { joueur: 1 })) + note('Stepford Cuckoos défausse la carte et en révèle une autre.'),
          { joueur: 1, cadre: 'j1', sous: 'Trafiquant (sbire)', montre: [trait('cuckoos', 'boite', 'j1')], suite: [copie('b:t', 'defausse', 'Trafiquant', 0, true)] }),
        E('3', 'Carte rencontre 2/2 · Ironheart', rangee(mini('t', 'Explosion Sonique', 'traitrise')) + note('(remplace Trafiquant)', 'gris'), { joueur: 1, cadre: 'j1', sous: 'Explosion Sonique (traîtrise)', bouton: null }),
      ],
    },
  ]);

  // ===================================================================== ⑱ BILAN
  enc('⑱', 'Bilan', 'Bilan de fin de phase', [
    'Totaux par joueur avec pastille : dégâts subis, menace posée par manigance, cartes entrées en jeu.',
    'Chaque ligne est cliquable pour revoir la carte.',
    'Phase sans conséquence : « Rien de grave cette phase ».',
    'Bouton « Terminer » seul, aucun effet.',
  ], [
    {
      nom: 'Phase chargée',
      table: table('klaw', { ...T.trafic, c: '5/6', rouge: true }, { ...T.ironheart, c: '7/11' }, { ...T.cap, c: '9/11' }),
      etapes: [
        E('B', 'Bilan', ligne('Ironheart', '−4 PV (11 → 7)', { pastilles: [1] }) + ligne('Captain America', '−2 PV (11 → 9)', { pastilles: [2] }) + ligne('Trafic Clandestin', '+4 menaces (1 → 5 / 6)', { carte: 'principale', ton: 'rouge' }) + ligne('Entrés en jeu', 'Trafiquant d’Armes, Bombe à Retardement', { carte: 'sbire' }),
          { bouton: 'Terminer', montre: [halo('ironheart', 'j1'), halo('cap', 'j2'), halo('trafic', 'rouge')] }),
      ],
    },
    {
      nom: 'Rien de grave',
      table: table('klaw', 'trafic', 'ironheart'),
      etapes: [E('B', 'Bilan', `<p class="enorme vert">Rien de grave cette phase</p>`, { bouton: 'Terminer' })],
    },
  ]);

  // Les cartes ajoutées après coup (une carte qui entre plus tard dans un cas).
  for (const e of ENCADRES) for (const c of e.cas) if (c.ajouts) c.table.push(...c.ajouts);
  // ② cas 1 : la face B met Contrebande en jeu.
  const stade = ENCADRES[1].cas[0];
  stade.etapes[2].montre = [place('contrebande'), trait('b:s', 'contrebande')];
  stade.etapes[2].suite = [arrive('contrebande', 'b:s')];

  window.ENCADRES = ENCADRES;
})();
