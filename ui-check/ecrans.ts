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

export type Ecran = {
  cle: string;
  titre: string;
  url: string;
  marqueur: string;
  masques?: string[];
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
