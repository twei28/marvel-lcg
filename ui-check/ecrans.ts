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
    marqueur: '#mode',
    // Le numero de "seed" est tire au hasard a chaque ouverture de la page.
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
    // Les deux blocs de la page sont masques tant que le serveur n'a pas
    // repondu : on se contente de la page elle-meme, le garde-fou contre la
    // page d'avertissement de cache est fait autrement (voir captures.spec.ts).
    marqueur: 'body',
  },
];

// Le plateau de jeu (marvel.html) n'est VOLONTAIREMENT pas dans cette liste :
// son apparence depend d'une partie en cours, donc d'un etat non reproductible.
// Il sera couvert par les fixtures, pas par une capture d'URL.
