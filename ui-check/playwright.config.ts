// Configuration du harnais de captures.
//
// Ce que ce fichier decide :
//  - sur quelle adresse le jeu est attendu (baseURL) ;
//  - dans quels formats d'ecran on capture (les 3 "gabarits" : pc, tablette, mobile) ;
//  - ou sont rangees les images de reference (references/<ecran>/<gabarit>.png) ;
//  - a partir de quel ecart on considere qu'un ecran a change.
//
// En principe il n'y a rien a modifier ici au quotidien : les ecrans se declarent
// dans ecrans.ts.
import { defineConfig } from '@playwright/test';

// Adresse du jeu. Par defaut le port habituel du serveur de developpement.
// UI_CHECK_BASE permet de viser un second serveur quand le port 2345 est pris
// par une partie multijoueur (voir scripts/serveur-dev.py). Depuis WSL, npm
// passe par cmd.exe : la variable doit etre relayee par WSLENV.
//   export UI_CHECK_BASE=http://127.0.0.1:2346 WSLENV=UI_CHECK_BASE
export const ADRESSE_JEU = process.env.UI_CHECK_BASE || 'http://127.0.0.1:2345';

// Les 3 formats d'ecran captures pour chaque page, plus s24 et s24paysage
// (voir plus bas : ils ne participent pas aux captures de reference,
// seulement au filet du plateau mobile).
const GABARITS = {
  pc: { width: 1920, height: 1080 }, // Ordinateur
  tablette: { width: 1180, height: 820 }, // iPad Air, paysage
  mobile: { width: 390, height: 844 }, // iPhone 12/13/14
  // Samsung S24 Ultra en portrait : sert a verifier l'ecran « Tourne ton
  // telephone » du plateau paysage, et l'ancien rendu a medaillons (?medaillons).
  s24: { width: 480, height: 1050 },
  // Samsung S24 Ultra en PAYSAGE, plein ecran : l'appareil de reference du
  // plateau paysage (spec du 07/09/2026).
  s24paysage: { width: 1050, height: 480 },
};

export default defineConfig({
  testDir: './tests',

  // Pose le cookie de version avant toute capture (sinon le serveur renvoie
  // une page d'avertissement de cache a la place de chaque ecran).
  globalSetup: './global-setup.ts',

  // Une seule instance du jeu tourne : pas de tests en parallele.
  fullyParallel: false,
  workers: 1,

  // Pas de seconde chance : un ecran instable doit se voir, pas se cacher.
  retries: 0,

  reporter: [['list'], ['html', { open: 'never' }]],

  // references/<ecran>/<gabarit>.png : des noms lisibles par un humain.
  snapshotPathTemplate: '{testDir}/../references/{arg}/{projectName}{ext}',

  use: {
    baseURL: ADRESSE_JEU,
    storageState: './.auth/state.json', // cookie app_version pose par global-setup
    deviceScaleFactor: 1, // sinon les PNG pesent 4x plus lourd pour rien
    reducedMotion: 'reduce',
  },

  expect: {
    toHaveScreenshot: {
      // Les defauts de Playwright sont conserves : animations desactivees,
      // curseur masque, attente des polices, double capture identique.
      maxDiffPixelRatio: 0.002, // ~0,2 % : absorbe l'anticrenelage, pas un vrai decalage
      scale: 'css',
    },
  },

  projects: [
    // pc / tablette / mobile : gabarits "souris", sans emulation tactile.
    // s24 est exclu de cette generation automatique pour ne pas produire deux
    // projets nommes "s24" (un simple, un tactile) : il a son propre projet
    // juste apres, avec les options que son test teste vraiment.
    ...Object.entries(GABARITS)
      .filter(([name]) => name !== 's24' && name !== 's24paysage')
      .map(([name, viewport]) => ({
        name,
        use: { viewport },
      })),
    {
      name: 's24',
      // Sans ce filtre, "npm run captures" (aucun --project) essaierait AUSSI
      // de prendre chaque ecran de ecrans.ts en s24, contre des references
      // qui n'existent pas (references/<ecran>/s24.png). Ce ne serait pas une
      // regression detectee (aucune reference existante ne bouge), mais ca
      // ferait echouer la commande pour une raison hors sujet.
      testMatch: /(plateau-(mobile|paysage)|menus-mobile|assistant-mobile)\.spec\.ts$/,
      // 34 vraies navigations reseau (une par etat enregistre) depassent le
      // budget par defaut de 30s : mesure sur ce poste, la boucle complete
      // prend environ 30s a elle seule, sans marge pour une machine plus
      // lente. N'assouplit aucun seuil d'assertion, seulement le temps
      // alloue pour les executer toutes dans un seul test.
      timeout: 90_000,
      use: {
        viewport: GABARITS.s24,
        hasTouch: true,
        isMobile: true,
        deviceScaleFactor: 1,
      },
    },
    {
      name: 's24-paysage',
      testMatch: /plateau-paysage\.spec\.ts$/,
      // Voir le commentaire sur le projet s24 : meme boucle sur 34 etats.
      timeout: 90_000,
      use: {
        viewport: GABARITS.s24paysage,
        hasTouch: true,
        isMobile: true,
        deviceScaleFactor: 1,
      },
    },
  ],
});
