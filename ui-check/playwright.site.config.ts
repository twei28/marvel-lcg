// Configuration MINIMALE pour les pages du SITE (orchestrateur), qui n'ont pas
// besoin du jeu : pas de globalSetup (il exige le jeu sur le port 2345).
//   python3 site/serveur_essai_decks_admin.py 8097 &
//   SITE=http://127.0.0.1:8097 npx playwright test -c playwright.site.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: /(admin-decks-joueurs|connexion-site)\.spec\.ts/,
  workers: 1,
  retries: 0,
  reporter: [['list']],
  use: { viewport: { width: 1280, height: 720 }, reducedMotion: 'reduce', locale: 'fr-FR' },
});
