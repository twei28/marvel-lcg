import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import checker from 'vite-plugin-checker'
import { resolve } from 'node:path'

export default defineConfig({
  // Adresse reellement servie par le serveur Python (verifie en direct).
  base: '/app/',

  plugins: [react(), checker({ typescript: true })],

  // Serveur de DEVELOPPEMENT uniquement (jamais dans le build). Le plateau lit
  // quatre routes du jeu : sans relais, /app/board.html n'a ni etat de partie ni
  // scan a afficher hors du serveur Python.
  //
  // ADRESSE_JEU vise un autre serveur que le port habituel. Depuis WSL, npm
  // passe par cmd.exe : la variable doit etre relayee par WSLENV, comme
  // UI_CHECK_BASE pour le harnais de captures.
  //   export ADRESSE_JEU=http://127.0.0.1:2346 WSLENV=ADRESSE_JEU
  //
  // Le cookie de version est pose par hote, pas par port : ouvrir une fois le
  // jeu sur 127.0.0.1 suffit pour que le relais soit accepte.
  server: {
    proxy: Object.fromEntries(
      [
        '/get_world',
        '/get_cards_json',
        // Les etats de partie enregistres, servis tels quels par le jeu.
        '/public',
        // Les scans. Le prefixe /scan/ n'existe que pour rendre ces requetes
        // relayables : le serveur du jeu ne regarde que le dernier segment.
        '/scan',
        // Les vignettes, meme mecanisme.
        '/vignette',
      ].map((route) => [route, process.env.ADRESSE_JEU ?? 'http://127.0.0.1:2345'])
    ),
  },

  build: {
    outDir: 'dist',        // LOCAL. La recopie vers le jeu est faite par deployer.sh.
    // Le serveur n'a AUCUNE route pour .png / .webp / .woff2 / .json, et sa
    // route .svg ne lit que assets/textures/ a plat. On force donc l'inlining
    // de tout asset importe : rien d'autre que .html / .js / .css ne doit sortir.
    assetsInlineLimit: () => true,
    // .js.map renvoie 404 en mode RELEASE, pose par les deux launchers.
    sourcemap: false,
    // Vite 8 : rollupOptions a ete RENOMME rolldownOptions.
    rolldownOptions: {
      input: {
        vitrine: resolve(import.meta.dirname, 'vitrine.html'),
        board: resolve(import.meta.dirname, 'board.html'),
      },
    },
  },
})
