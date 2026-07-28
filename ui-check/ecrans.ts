// La liste des ecrans surveilles.
//
// C'EST LE SEUL FICHIER A COMPRENDRE pour ajouter ou retirer un ecran du
// filet de securite : une ligne = un ecran. Chaque ecran est capture dans les
// 3 gabarits definis dans playwright.config.ts (ordinateur, tablette, telephone).
//
//   cle       : le nom du dossier d'images. Sans accent ni espace.
//   titre     : le nom lisible, affiche dans les rapports et la page de comparaison.
//   url       : l'adresse de la page sur le serveur de jeu.
//   marqueur  : un element qui prouve que la BONNE page s'est chargee. Sans lui,
//               on risquerait de figer 18 fois la meme page d'avertissement.
//   masques   : zones a neutraliser parce qu'elles changent a chaque chargement
//               (un numero tire au hasard, une date...). Elles sont peintes en rose.
//   etape     : numero du panneau du wizard a ouvrir avant la photo (0 a 3).
//               Sans lui, seul le panneau affiche au chargement est photographie.
//   depliages : boutons a cliquer avant la photo, pour montrer un contenu que la
//               page replie par defaut. Sans eux, une partie du panneau reste
//               invisible et donc hors surveillance.
//   preuves   : elements qui doivent etre visibles une fois l'etape ouverte. Ils
//               prouvent que le CONTENU du panneau est bien dans la photo, et
//               pas seulement son entete.

export type Ecran = {
  cle: string;
  titre: string;
  url: string;
  marqueur: string;
  masques?: string[];
  etape?: number;
  depliages?: string[];
  preuves?: string[];
};

export const ECRANS: Ecran[] = [
  {
    cle: 'menu',
    titre: 'Menu principal',
    url: '/main.html',
    marqueur: '.menu',
  },
  {
    cle: 'preparation',
    titre: 'Preparation (ancienne)',
    url: '/scene.html',
    // La barre d'etapes du wizard : c'est le seul repere visible au chargement.
    // Les panneaux d'etapes (#mode, #rules...) sont masques tant qu'on n'y est pas.
    marqueur: '#w-stepper',
    // Le numero de "seed" est tire au hasard a chaque ouverture de la page.
    // Il est aujourd'hui dans une etape masquee, mais on garde le masque en
    // filet : il redeviendra utile si l'etape s'ouvre par defaut un jour.
    masques: ['#seed_div'],
  },
  // Les 3 entrees suivantes existent parce que scene.html n'affiche QU'UN SEUL
  // de ses 4 panneaux au chargement (l'entree 'preparation' ci-dessus couvre le
  // panneau 0, Scenario). Or la majorite des declarations !important de
  // css/menu/wizard.css agit sur les panneaux 1, 2 et 3 : environ 45 sur 105.
  // Sans ces photos, la purge de ces !important se ferait a l'aveugle et un
  // "npm run captures" vert apres la purge ne prouverait rien.
  {
    cle: 'preparation-rencontre',
    titre: 'Preparation ancienne - etape 2 Rencontre',
    url: '/scene.html',
    marqueur: '#w-stepper',
    masques: ['#seed_div'],
    etape: 1,
    // Les sets modulaires sont replies au chargement : le conteneur porte la
    // classe 'hide-not-click', qui masque tout set non selectionne. Sans ce
    // clic, la photo ne montrerait AUCUN set modulaire, alors que la moitie des
    // !important de ce panneau visent "#modular-sets button" et
    // "#modular-sets img". On vise le bouton par son comportement (son onclick)
    // et non par son libelle, qui pourrait etre traduit.
    depliages: ['button[onclick*="hide-not-click"]'],
    preuves: ['#encounter-sets button', '#modular-sets button'],
  },
  {
    cle: 'preparation-heros',
    titre: 'Preparation ancienne - etape 3 Heros',
    url: '/scene.html',
    marqueur: '#w-stepper',
    masques: ['#seed_div'],
    etape: 2,
    preuves: ['.w-step-panel[data-panel="2"] legend'],
  },
  {
    cle: 'preparation-lancement',
    titre: 'Preparation ancienne - etape 4 Lancement',
    url: '/scene.html',
    marqueur: '#w-stepper',
    // Le champ "seed" est DANS ce panneau : sans le masque, chaque photo
    // differerait de la precedente.
    masques: ['#seed_div'],
    etape: 3,
    preuves: ['#play-buttons', '#game-start'],
  },
  {
    cle: 'preparation-nouvelle',
    titre: 'Preparation (nouvelle)',
    url: '/prepare.html',
    marqueur: '#app',
  },
  {
    cle: 'cartes',
    titre: 'Galerie de cartes',
    url: '/cards.html',
    marqueur: '#found_cards',
  },
  {
    cle: 'decks',
    titre: 'Gestion de decks',
    url: '/deck.html',
    marqueur: '#deck_editor',
  },
  {
    cle: 'replay',
    titre: 'Replays',
    url: '/replay.html',
    // Le bloc "Game Replay" n'apparait qu'une fois la liste chargee : c'est
    // donc une bonne preuve que la page a vraiment fini de s'afficher.
    // Note : cet ecran est presque vide tant qu'aucune partie n'a ete enregistree.
    marqueur: '#replay-items',
  },
];

// Le plateau de jeu (marvel.html) n'est VOLONTAIREMENT pas dans cette liste :
// son apparence depend d'une partie en cours, donc d'un etat non reproductible.
// Il sera couvert par les fixtures, pas par une capture d'URL.
