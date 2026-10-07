// GARDE : la boite de question du centre (« Défendre avec… ») n'a JAMAIS de barre de defilement et ne
// deborde JAMAIS, quel que soit le nombre de defenseurs et la taille de la fenetre.
//
//   cd ui-check && node scripts/garde-boite-defense.mjs        (code de sortie 1 au moindre ecart)
//
// POURQUOI (07/10/2026) : « cette barre de scroll degueulasse… il faut jamais avoir de barre de scroll ».
// Les boutons de defense restent sur une ligne (boutons-bd.css) et sont agrandis (zoom) : un long
// « Défendre avec Captain America (DÉF 2 + 1 Bouclier de Captain America) » depassait la boite et faisait
// apparaitre une barre horizontale. Ce garde monte la VRAIE feuille de style (board.css, boutons-bd.css,
// tokens.css, police Bangers) sur la structure de DemandeCentrale.tsx, sans moteur ni serveur : il tourne
// n'importe quand.
import { chromium } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const RACINE = path.resolve(ICI, '..', '..')
const FICHIERS = {
  '/board.css': path.join(RACINE, 'ui-app/src/board/board.css'),
  '/boutons-bd.css': path.join(RACINE, 'ui-app/src/board/boutons-bd.css'),
  '/tokens.css': path.join(RACINE, 'ui-app/styles/tokens.css'),
  '/public/fonts/Bangers-Regular.ttf': path.join(RACINE, 'Fusion/marvel-lcg-src/public/fonts/Bangers-Regular.ttf'),
}
const TYPES = { '.css': 'text/css', '.ttf': 'font/ttf' }

// Le pire cas reel : un nom de defenseur avec son bonus en clair, plus long que tous ceux du jeu de base.
const LONG = 'Captain America (DÉF 2 + 1 Bouclier de Captain America)'
const TAILLES = [[1280, 720], [1366, 768], [1600, 900], [1920, 1080]]

function page(n) {
  // Memes classes que DemandeCentrale.tsx (tailleDesChoix : compact a 4, liste a 7).
  const classe = n >= 7 ? ' dc-liste' : n >= 4 ? ' dc-compact' : ''
  const noms = [LONG, ...Array.from({ length: n - 1 }, (_, i) => `${LONG.slice(0, 18 + (i % 20))} ${i + 2}`)]
  const choix = noms
    .map((nom) => `<span class="af-action-wrap a-vignette"><span class="dc-vignette"><div class="scan-card" style="width:var(--card-w,104px);aspect-ratio:63/88;background:#456"></div></span><button class="af-action est-defense"><span>Défendre avec ${nom}</span></button></span>`)
    .join('')
  return `<!doctype html><meta charset=utf-8><link rel=stylesheet href="/tokens.css"><link rel=stylesheet href="/board.css"><link rel=stylesheet href="/boutons-bd.css">
<body style="margin:0;height:100vh;background:#10131c"><section class="demande-centrale${classe}" role="dialog">
<div class="dc-texte"><span class="plateau-eyebrow">À toi de jouer</span><strong>Captain America est attaqué par Klaw</strong><span class="dc-reagit">Captain America peut réagir</span></div>
<div class="af-boutons dc-boutons">${choix}<span class="af-action-wrap dc-refus"><button class="af-action tonalite-general dc-pass est-defense">Ne pas défendre (ATQ 0 + 2 cartes boost)</button></span></div>
</section></body>`
}

const navigateur = await chromium.launch()
const ecarts = []
for (const [l, h] of TAILLES) {
  const onglet = await navigateur.newPage({ viewport: { width: l, height: h } })
  await onglet.route('http://garde.local/**', async (route) => {
    const chemin = new URL(route.request().url()).pathname
    if (FICHIERS[chemin]) {
      return route.fulfill({ body: fs.readFileSync(FICHIERS[chemin]), contentType: TYPES[path.extname(chemin)] })
    }
    const n = Number(chemin.slice(1))
    return route.fulfill({ body: page(n), contentType: 'text/html' })
  })
  for (let n = 1; n <= 14; n += 1) {
    await onglet.goto(`http://garde.local/${n}`)
    await onglet.evaluate(() => document.fonts.ready)
    const m = await onglet.evaluate(() => {
      const boite = document.querySelector('.demande-centrale').getBoundingClientRect()
      const d = document.querySelector('.dc-boutons')
      const refus = document.querySelector('.dc-pass').getBoundingClientRect()
      const boutons = [...d.querySelectorAll('.af-action')].map((b) => b.getBoundingClientRect())
      const cadre = d.getBoundingClientRect()
      return {
        debordeLargeur: d.scrollWidth - d.clientWidth,
        barre: d.offsetWidth - d.clientWidth > 1 || d.offsetHeight - d.clientHeight > 1,
        boutonCoupe: boutons.some((b) => b.left < cadre.left - 1 || b.right > cadre.right + 1),
        horsFenetre: boite.top < 0 || boite.bottom > innerHeight || boite.left < 0 || boite.right > innerWidth,
        refusVisible: refus.top >= 0 && refus.bottom <= innerHeight && refus.left >= 0 && refus.right <= innerWidth,
      }
    })
    const probleme = [
      m.debordeLargeur > 1 && `deborde en largeur de ${m.debordeLargeur} px`,
      m.barre && 'barre de defilement visible',
      m.boutonCoupe && 'un bouton sort de la boite',
      m.horsFenetre && 'la boite sort de la fenetre',
      !m.refusVisible && '« Ne pas defendre » hors de l’ecran',
    ].filter(Boolean)
    if (probleme.length) ecarts.push(`${n} defenseur(s) en ${l}x${h} : ${probleme.join(', ')}`)
  }
  await onglet.close()
}
await navigateur.close()
console.log(ecarts.length ? ecarts.join('\n') : `OK : 14 tailles de liste x ${TAILLES.length} fenetres, aucune barre, aucun debordement`)
process.exit(ecarts.length ? 1 : 0)
