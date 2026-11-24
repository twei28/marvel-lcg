// noms-fr-fanmade.ts — nom français des cartes FAN-MADE qui ont un vrai
// scan français déposé (assets/pics-fr/fr_<card_id>.jpg).
//
// ÉCRIT À LA MAIN, à la différence de noms-fr.ts (généré depuis marvelcdb,
// qui ne connaît pas les cartes fan-made — voir son commentaire d'en-tête).
// Nécessaire car le JOUEUR VOIT le nom français sur le scan, mais le champ
// `name` du moteur reste en anglais (c'est une clé de logique, jamais
// traduite à la source, voir noms-cartes-fr.ts) : sans ce dictionnaire, les
// boîtes de dialogue (titre de choix, etc.) qui recomposent un titre à partir
// de `name` affichent l'anglais alors que la carte à l'écran est en français.
//
// Signalement mobile du 05/11/2026 (nicodede62, pack Blade) : « Vampire Bite »
// affiché dans le titre d'une boîte de choix alors que le scan dit
// « Morsure de Vampire ».
//
// N'AJOUTER UNE CARTE ICI QUE SI SON SCAN FR EXISTE VRAIMENT
// (assets/pics-fr/fr_<card_id>.jpg) : sinon le nom affiché divergerait du
// scan anglais que le joueur a sous les yeux (même piège que noms-fr.ts).
// Noms relevés directement sur les scans déposés le 04/11/2026 (Blade,
// préfixe bl, auteur Rainy) ; bl001a/bl001b/bl009 omis car identiques à
// l'anglais (« Blade », « Eric Brooks », « Daywalker ») ; bl010 et suivants
// ont été déposés depuis (16/11/2026 : bl010 à bl017, relevés sur les scans).
export const NOMS_FR_FANMADE: Readonly<Record<string, string | undefined>> = {
  bl002: 'Préparer la Chasse',
  bl003: 'En Plein Cœur',
  bl004: 'En Pleine Traque',
  bl005: 'Morsure de Vampire',
  bl006: 'Réflexes Vampiriques',
  bl007: 'Pieux en Bandoulière',
  bl008: 'Épée de Blade',
  // bl010 à bl017 : scans FR déposés après coup, noms relevés le 16/11/2026 (Blade : « pareil sur Blade », signalement n°134).
  // bl013 « Dracula » et bl014 « Vampire » sont identiques à l'anglais.
  bl010: 'Instincts de Prédateur',
  bl011: 'La Soif',
  bl012: 'Chasse au Sang',
  bl015: 'Pieux en Bandoulière',
  bl016: 'Étreinte',
  bl017: 'Transformé',
  // Pack Dazzler (dz, 24 scans FR deposes) : noms releves sur les scans le 16/11/2026, apres le signalement n°134
  // (nicodede62 : « encore quelques infos en anglais »). dz001a/dz001b/dz002/dz014/dz020 sont identiques a l'anglais.
  dz003: '"Le Rêve d\'une Petite Fille"',
  dz004: '"Belle Rêveuse"',
  dz005: '"La Belle et la Bête"',
  dz006: '"Poupée"',
  dz007: '"Chut, Mon Bébé"',
  dz008: '"Dans la Lumière la Plus Sombre"',
  dz009: '"Fière et Assumée"',
  dz010: '"Ange Fortuné"',
  dz011: '"Le Serpent Arrive"',
  dz012: '"Trop Beau pour Être Vrai"',
  dz013: '"Ciel Velouté"',
  dz015: 'Patins à Roulettes de Dazzler',
  dz016: 'Combinaison à Collecteur de Sons',
  dz017a: 'Concert en Direct',
  dz017b: 'En Scène !',
  dz019: 'Angoisse de Performance',
  dz021: 'Corps de Son Solidifié',
  dz022: 'Vol de Son',
  dz023: 'Lumière Provocatrice',
  // Pack Yondu (yd, 19 scans FR) : noms relevés sur les scans le 22/11/2026. yd001a/yd001b/yd011/yd015 identiques à l'anglais.
  yd002: 'Coup Bas',
  yd003: 'Coup Fourré',
  yd004: 'Sifflez en Travaillant',
  yd005: 'Sacré Dur à Cuire',
  yd006: "Ça Vir' et Ça Vrill'",
  yd007: 'Jackpot !',
  yd008: 'Ravageurs Sacrifiables',
  yd009: 'Investissement',
  yd010: 'Ravage',
  yd012: 'Flèche Yaka',
  yd013: 'Banni',
  yd014: 'Une Prime sur Votre Tête',
  yd016: 'Bras-Épée-Fusil',
  yd017: 'Dur à Abattre',
  yd018: 'Dévastation Sauvage',
  // Pack mk : noms relevés sur les scans FR le 22/11/2026 (les cartes identiques à l'anglais sont omises).
  mk005: 'Différentes Personnes',
  mk006: 'Différents Talents',
  mk007: 'Se Mettre à Couvert',
  mk008: 'Frapper ou Déjouer',
  mk009: 'Se Préparer',
  mk010: 'Où Est-il Passé ?',
  mk011: 'Polyvalence',
  mk012: "Chercher de l'Aide",
  mk014: 'Mano a Mano',
  mk015: 'Éliminer les Faibles',
  mk016: 'Couteau de Bushman',
  // Pack sr : noms relevés sur les scans FR le 22/11/2026 (les cartes identiques à l'anglais sont omises).
  sr003: 'Thwip !',
  sr004: 'Barrage de Toiles',
  sr005: 'Coup de Toile',
  sr006: 'Pris dans la Toile',
  sr007: 'Un Grand Pouvoir',
  sr008: 'De Grandes Responsabilités',
  sr010: "Sens d'Araignée",
  sr011: 'Lance-Toiles',
  sr012: 'Effet des Toiles',
  sr013: 'Mauvaise Publicité',
  sr014: 'Et pour Mon Prochain Tour…',
  sr016: "Sursaut d'Effroi",
  sr017: 'Poudre aux Yeux',
  // Pack mt : noms relevés sur les scans FR le 22/11/2026 (les cartes identiques à l'anglais sont omises).
  mt003: 'Précognition',
  mt004: 'Frappe aux Points de Pression',
  mt005: 'Prouesse Psychique',
  mt006: 'Biopathie',
  mt007: 'Atrium de Méditation',
  mt008: 'Esprit Renforcé',
  mt009: 'Blocage Mental Psionique',
  mt010: 'La Madone Céleste',
  mt011: 'Secousse Psychique',
  mt012: "L'Éclosion de la Fleur de Mort",
  mt013: 'Le Spadassin',
  mt014: "L'Homme-Plante",
  mt015: 'Résilience des Cotatis',
  mt016: 'Lien Mental',
}
