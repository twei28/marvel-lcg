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

// Les 3 formats d'ecran captures pour chaque page.
const GABARITS = {
  pc: { width: 1920, height: 1080 }, // Ordinateur
  tablette: { width: 1180, height: 820 }, // iPad Air, paysage
  mobile: { width: 390, height: 844 }, // iPhone 12/13/14
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
    baseURL: 'http://127.0.0.1:2345',
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

  projects: Object.entries(GABARITS).map(([name, viewport]) => ({
    name,
    use: { viewport },
  })),
});
