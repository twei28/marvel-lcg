import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import checker from 'vite-plugin-checker'
import { resolve } from 'node:path'

export default defineConfig({
  // Adresse reellement servie par le serveur Python (verifie en direct).
  base: '/app/',

  plugins: [react(), checker({ typescript: true })],

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
      },
    },
  },
})
