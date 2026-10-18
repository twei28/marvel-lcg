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

// Les pages de l'ancien client (/main, /scene, /cards, /deck) sont retirees (18/10/2026, elles renvoient a l'accueil) :
// leurs captures ne sont plus faites.
export const ECRANS: Ecran[] = [
  {
    cle: 'preparation-nouvelle',
    titre: 'Preparation (nouvelle)',
    url: '/prepare.html',
    marqueur: '#app',
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
