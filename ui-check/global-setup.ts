// Preparation commune a tous les tests, executee une seule fois au demarrage.
//
// Deux roles :
//  1. Poser le cookie de version. Sans lui, le serveur renvoie une page
//     d'avertissement de cache A LA PLACE de chaque ecran, avec un code 200
//     (donc sans erreur visible). On figerait 18 fois la meme image.
//  2. Verifier tout de suite que le jeu est bien lance. Mieux vaut un message
//     clair en francais qu'une serie de captures fausses.
import { chromium, type FullConfig } from '@playwright/test';
import fs from 'node:fs';
import { ADRESSE_JEU } from './playwright.config';

export default async function globalSetup(_config: FullConfig) {
  // Meme adresse que les tests : par defaut 127.0.0.1:2345, surchargeable par
  // UI_CHECK_BASE quand une partie multijoueur occupe deja ce port.
  const base = ADRESSE_JEU;
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();

  try {
    // /get_version pose le cookie app_version (accessible, sans authentification).
    await page.goto(`${base}/get_version`, { waitUntil: 'domcontentloaded' });

    // Garde-fou : on s'arrete ici si le menu ne se charge pas.
    await page.goto(`${base}/main.html`, { waitUntil: 'domcontentloaded' });
    const titre = await page.title();
    if (!/Marvel/i.test(titre)) {
      throw new Error(
        `Le serveur ne sert pas le menu du jeu (titre recu : "${titre}"). ` +
          `Le jeu est-il bien lance sur ${base} ? ` +
          `Si oui, relance-le avec launcher_fast.py, puis reessaie.`
      );
    }

    fs.mkdirSync('./.auth', { recursive: true });
    await ctx.storageState({ path: './.auth/state.json' });
  } catch (erreur) {
    if (erreur instanceof Error && /ECONNREFUSED|ERR_CONNECTION_REFUSED/.test(erreur.message)) {
      throw new Error(
        `Impossible de joindre le jeu sur ${base}. ` +
          `Le serveur est-il lance ? (launcher_fast.py)`
      );
    }
    throw erreur;
  } finally {
    await browser.close();
  }
}
