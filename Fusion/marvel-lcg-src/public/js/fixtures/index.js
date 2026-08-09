// Catalogue des états de jeu enregistrés.
//
// Chaque entrée pointe vers un module qui exporte le descripteur renvoyé par
// /get_world à cet instant précis d'une vraie partie. Ces états ont été
// enregistrés par des parties jouées automatiquement (bot d'autoplay) : ils
// servent à travailler l'affichage du plateau sans avoir à lancer une partie.
//
// Pour en régénérer : ~/marvel-work/tools/run_dump.sh <port> <scenario> <heros>
// (les fichiers .js du dossier sont réécrits, ce catalogue est tenu à la main).
//
// Champs : fichier (module à importer), titre (libellé affiché), description
// (ce que l'état montre), scenario / heros / cas (pour filtrer).

export const FIXTURES = [
  // ---------------------------------------------------------------- Rhino / Spider-Man
  { fichier: 'rhino__spider_man__mise-en-place.js', titre: 'Rhino / Spider-Man — mise en place',
    description: 'Plateau installé, cartes distribuées, avant le premier tour.',
    scenario: 'rhino', heros: 'spider_man', cas: 'mise-en-place' },
  { fichier: 'rhino__spider_man__debut-de-tour.js', titre: 'Rhino / Spider-Man — début de partie',
    description: 'Premier tour de jeu, le héros n\'a encore rien joué.',
    scenario: 'rhino', heros: 'spider_man', cas: 'debut-de-tour' },
  { fichier: 'rhino__spider_man__main-pleine.js', titre: 'Rhino / Spider-Man — main la plus remplie',
    description: 'Moment de la partie où le joueur avait le plus de cartes en main.',
    scenario: 'rhino', heros: 'spider_man', cas: 'main-pleine' },
  { fichier: 'rhino__spider_man__sbire-en-jeu.js', titre: 'Rhino / Spider-Man — un sbire en jeu',
    description: 'Un sbire accompagne le vilain sur le plateau.',
    scenario: 'rhino', heros: 'spider_man', cas: 'sbire-en-jeu' },
  { fichier: 'rhino__spider_man__statuts.js', titre: 'Rhino / Spider-Man — cartes de statut',
    description: 'Au moins une carte de statut (résistant, étourdi, confus) est posée.',
    scenario: 'rhino', heros: 'spider_man', cas: 'statuts' },
  { fichier: 'rhino__spider_man__side-scheme.js', titre: 'Rhino / Spider-Man — complot annexe',
    description: 'Un complot annexe est en jeu à côté du complot principal.',
    scenario: 'rhino', heros: 'spider_man', cas: 'side-scheme' },
  { fichier: 'rhino__spider_man__defausse-rencontre-pleine.js', titre: 'Rhino / Spider-Man — défausse de rencontre chargée',
    description: 'Moment où la défausse du deck de rencontre était la plus fournie.',
    scenario: 'rhino', heros: 'spider_man', cas: 'defausse-rencontre-pleine' },
  { fichier: 'rhino__spider_man__fin-de-partie.js', titre: 'Rhino / Spider-Man — fin de partie',
    description: 'Dernier état affiché : la partie est terminée (complot principal achevé).',
    scenario: 'rhino', heros: 'spider_man', cas: 'fin-de-partie' },

  // ---------------------------------------------------------------- Rhino / Daredevil
  { fichier: 'rhino__daredevil__mise-en-place.js', titre: 'Rhino / Daredevil — mise en place',
    description: 'Même scénario, autre héros : le plateau juste après l\'installation.',
    scenario: 'rhino', heros: 'daredevil', cas: 'mise-en-place' },
  { fichier: 'rhino__daredevil__debut-de-tour.js', titre: 'Rhino / Daredevil — début de partie',
    description: 'Premier tour de jeu.',
    scenario: 'rhino', heros: 'daredevil', cas: 'debut-de-tour' },
  { fichier: 'rhino__daredevil__statuts.js', titre: 'Rhino / Daredevil — cartes de statut',
    description: 'Une carte de statut est en jeu.',
    scenario: 'rhino', heros: 'daredevil', cas: 'statuts' },
  { fichier: 'rhino__daredevil__sbire-en-jeu.js', titre: 'Rhino / Daredevil — un sbire en jeu',
    description: 'Un sbire est entré en jeu.',
    scenario: 'rhino', heros: 'daredevil', cas: 'sbire-en-jeu' },
  { fichier: 'rhino__daredevil__fin-de-partie.js', titre: 'Rhino / Daredevil — fin de partie',
    description: 'Dernier état affiché : la partie est terminée.',
    scenario: 'rhino', heros: 'daredevil', cas: 'fin-de-partie' },

  // ---------------------------------------------------------------- Klaw / Captain Marvel
  { fichier: 'klaw__captain_marvel__mise-en-place.js', titre: 'Klaw / Captain Marvel — mise en place',
    description: 'Installation du scénario Klaw, avant le premier tour.',
    scenario: 'klaw', heros: 'captain_marvel', cas: 'mise-en-place' },
  { fichier: 'klaw__captain_marvel__side-scheme.js', titre: 'Klaw / Captain Marvel — complot annexe',
    description: 'Un complot annexe est en jeu dès le début de la partie.',
    scenario: 'klaw', heros: 'captain_marvel', cas: 'side-scheme' },
  { fichier: 'klaw__captain_marvel__sbire-en-jeu.js', titre: 'Klaw / Captain Marvel — un sbire en jeu',
    description: 'Un sbire accompagne le vilain.',
    scenario: 'klaw', heros: 'captain_marvel', cas: 'sbire-en-jeu' },
  { fichier: 'klaw__captain_marvel__debut-de-tour.js', titre: 'Klaw / Captain Marvel — début de partie',
    description: 'Premier tour de jeu.',
    scenario: 'klaw', heros: 'captain_marvel', cas: 'debut-de-tour' },
  { fichier: 'klaw__captain_marvel__stade-2.js', titre: 'Klaw / Captain Marvel — vilain au stade 2',
    description: 'Le complot principal est passé à son deuxième stade.',
    scenario: 'klaw', heros: 'captain_marvel', cas: 'stade-2' },
  { fichier: 'klaw__captain_marvel__statuts.js', titre: 'Klaw / Captain Marvel — cartes de statut',
    description: 'Une carte de statut est posée sur un personnage.',
    scenario: 'klaw', heros: 'captain_marvel', cas: 'statuts' },
  { fichier: 'klaw__captain_marvel__defausse-rencontre-pleine.js', titre: 'Klaw / Captain Marvel — défausse de rencontre chargée',
    description: 'Fin de partie approchant : beaucoup de cartes rencontre défaussées.',
    scenario: 'klaw', heros: 'captain_marvel', cas: 'defausse-rencontre-pleine' },
  { fichier: 'klaw__captain_marvel__fin-de-partie.js', titre: 'Klaw / Captain Marvel — fin de partie',
    description: 'Dernier état affiché : la partie est terminée.',
    scenario: 'klaw', heros: 'captain_marvel', cas: 'fin-de-partie' },

  // ---------------------------------------------------------------- Dieu du Mensonge / Hercule
  { fichier: 'god_of_lies__hercules__mise-en-place.js', titre: 'Dieu du Mensonge / Hercule — mise en place',
    description: 'Scénario à decks supplémentaires (travaux et présents d\'Hercule).',
    scenario: 'god_of_lies', heros: 'hercules', cas: 'mise-en-place' },
  { fichier: 'god_of_lies__hercules__carte-mise-de-cote.js', titre: 'Dieu du Mensonge / Hercule — cartes mises de côté',
    description: 'Des cartes attendent dans la zone « mise de côté ».',
    scenario: 'god_of_lies', heros: 'hercules', cas: 'carte-mise-de-cote' },
  { fichier: 'god_of_lies__hercules__debut-de-tour.js', titre: 'Dieu du Mensonge / Hercule — début de partie',
    description: 'Premier tour de jeu.',
    scenario: 'god_of_lies', heros: 'hercules', cas: 'debut-de-tour' },
  { fichier: 'god_of_lies__hercules__sbire-en-jeu.js', titre: 'Dieu du Mensonge / Hercule — un sbire en jeu',
    description: 'Un sbire est en jeu face au héros.',
    scenario: 'god_of_lies', heros: 'hercules', cas: 'sbire-en-jeu' },
  { fichier: 'god_of_lies__hercules__side-scheme.js', titre: 'Dieu du Mensonge / Hercule — complot annexe',
    description: 'Un complot annexe est en jeu.',
    scenario: 'god_of_lies', heros: 'hercules', cas: 'side-scheme' },
  { fichier: 'god_of_lies__hercules__defausse-rencontre-pleine.js', titre: 'Dieu du Mensonge / Hercule — défausse de rencontre chargée',
    description: 'Moment où la défausse du deck de rencontre était la plus fournie.',
    scenario: 'god_of_lies', heros: 'hercules', cas: 'defausse-rencontre-pleine' },
  { fichier: 'god_of_lies__hercules__fin-de-partie.js', titre: 'Dieu du Mensonge / Hercule — fin de partie',
    description: 'Dernier état affiché : la partie est terminée.',
    scenario: 'god_of_lies', heros: 'hercules', cas: 'fin-de-partie' },

  // ---------------------------------------------------------------- Absorbing Man / She-Hulk
  { fichier: 'absorbing_man__she_hulk__mise-en-place.js', titre: 'Absorbing Man / She-Hulk — mise en place',
    description: 'Installation du scénario Absorbing Man, avant le premier tour.',
    scenario: 'absorbing_man', heros: 'she_hulk', cas: 'mise-en-place' },
  { fichier: 'absorbing_man__she_hulk__debut-de-tour.js', titre: 'Absorbing Man / She-Hulk — début de partie',
    description: 'Premier tour de jeu.',
    scenario: 'absorbing_man', heros: 'she_hulk', cas: 'debut-de-tour' },
  { fichier: 'absorbing_man__she_hulk__statuts.js', titre: 'Absorbing Man / She-Hulk — cartes de statut',
    description: 'Une carte de statut est en jeu.',
    scenario: 'absorbing_man', heros: 'she_hulk', cas: 'statuts' },
  { fichier: 'absorbing_man__she_hulk__side-scheme.js', titre: 'Absorbing Man / She-Hulk — complot annexe',
    description: 'Un complot annexe est en jeu.',
    scenario: 'absorbing_man', heros: 'she_hulk', cas: 'side-scheme' },
  { fichier: 'absorbing_man__she_hulk__sbire-en-jeu.js', titre: 'Absorbing Man / She-Hulk — un sbire en jeu',
    description: 'Un sbire est en jeu face au héros.',
    scenario: 'absorbing_man', heros: 'she_hulk', cas: 'sbire-en-jeu' },
  { fichier: 'absorbing_man__she_hulk__fin-de-partie.js', titre: 'Absorbing Man / She-Hulk — fin de partie',
    description: 'Dernier état affiché : la partie est terminée.',
    scenario: 'absorbing_man', heros: 'she_hulk', cas: 'fin-de-partie' },
];

export default FIXTURES;
