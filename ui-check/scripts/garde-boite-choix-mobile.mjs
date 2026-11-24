// GARDE : la boite de question du centre (« <Carte> — Choisis une option », hors
// cartouche, ex. un Hero Action à choix comme Go for the Heart) n'a JAMAIS de
// bouton inatteignable sur TÉLÉPHONE (body.mode-plateau-portrait), quel que
// soit le nombre d'options et la taille réelle d'écran.
//
//   cd ui-check && node scripts/garde-boite-choix-mobile.mjs   (code de sortie 1 au moindre ecart)
//
// POURQUOI (05/11/2026, signalement nicodede62, pack Blade « Go for the Heart ») :
// « je ne peux pas choisir la 2e option et je suis obligé de fermer la fenêtre.
// Ce qui annule le coup. » `garde-boite-defense.mjs` existait déjà pour CE MEME
// panneau (.demande-centrale:not(.est-en-scene)) mais seulement pour le cas
// DEFENSE (.est-defense, boutons sur une ligne) et seulement sur des tailles
// de FENETRE D'ORDINATEUR (1280px et plus) : aucun garde n'avait jamais monté
// `menus-mobile.css` (qui transforme ce panneau en feuille basse plein écran
// sur téléphone, body.mode-plateau-portrait, posée par PlateauMobile.tsx) ni
// testé une largeur de téléphone réelle (~390-412px). Ce garde comble les deux
// trous à la fois : la VRAIE feuille mobile, sur de VRAIES largeurs de téléphone,
// pour un choix ORDINAIRE (pas défense) avec une vignette de carte au-dessus,
// comme Go for the Heart ou Vampire Bite.
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
  '/menus-mobile.css': path.join(RACINE, 'ui-app/src/board/mobile/menus-mobile.css'),
  '/public/fonts/Bangers-Regular.ttf': path.join(RACINE, 'Fusion/marvel-lcg-src/public/fonts/Bangers-Regular.ttf'),
}
const TYPES = { '.css': 'text/css', '.ttf': 'font/ttf' }

// Tailles de téléphone REELLES (zone utile, barre d'adresse deduite), pas des
// fenetres d'ordinateur redimensionnees. 390x844 (iPhone 12/13/14, le plus
// courant), 412x915 (Android, Pixel/Galaxy courants).
const TAILLES = [[390, 844], [412, 915]]

// Pire cas réel : le texte de bouton le plus long vu en jeu, un choix « Exhaust
// a WEAPON upgrade you control to stun that enemy » (bl003 Go for the Heart,
// traduit en francais par vocabulaire-moteur.ts), plus la vignette de carte et
// le texte de capacite au-dessus, comme le montre la vraie boite.
const LONG_BOUTON = 'Incliner une amélioration ARME que vous contrôlez pour sonner cet ennemi'
const TEXTE_CAPACITE = "Action de héros (attaque) : infligez 4 dégâts à un ennemi. Cette attaque gagne Perçant. Vous pouvez incliner une amélioration ARME que vous contrôlez pour sonner cet ennemi."

function page(nOptions) {
  // n options ordinaires (ForChoiceAbility) + le refus (Annuler), comme
  // ChooseAbilities(forced=False) : modele exact de bl003 Go for the Heart.
  const classe = nOptions >= 7 ? ' dc-liste' : nOptions >= 4 ? ' dc-compact' : ''
  const options = Array.from({ length: nOptions }, (_, i) =>
    `<span class="af-action-wrap"><button class="af-action tonalite-attaque"><span>${LONG_BOUTON} ${i + 1}</span></button></span>`
  ).join('')
  return `<!doctype html><meta charset=utf-8>
<link rel=stylesheet href="/tokens.css"><link rel=stylesheet href="/board.css">
<link rel=stylesheet href="/boutons-bd.css"><link rel=stylesheet href="/menus-mobile.css">
<body class="mode-plateau-portrait" style="margin:0;height:100vh;background:#10131c">
<section class="demande-centrale${classe}" role="dialog">
<div class="dc-texte"><span class="plateau-eyebrow">À toi de jouer</span><strong>En Plein Cœur — Choisis une option</strong></div>
<div class="dc-vignette"><div class="scan-card" style="width:var(--card-w,104px);aspect-ratio:63/88;background:#456"></div></div>
<p class="dc-capacite-texte">${TEXTE_CAPACITE}</p>
<div class="af-boutons dc-boutons">${options}<span class="af-action-wrap dc-refus"><button class="af-action tonalite-general dc-pass">Annuler</button></span></div>
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
  for (let n = 1; n <= 4; n += 1) {
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
        boutonCoupeEnLargeur: boutons.some((b) => b.left < cadre.left - 1 || b.right > cadre.right + 1),
        boitehorsFenetre: boite.top < 0 || boite.left < 0 || boite.right > innerWidth,
        // Le refus doit etre ATTEIGNABLE (dans la fenetre OU dans la zone de
        // defilement de la boite elle-meme), pas forcement visible sans scroll :
        // c'est le defilement qui doit marcher, verifie separement ci-dessous.
        refusDansLaBoite: refus.top >= boite.top - 1 && refus.left >= cadre.left - 1 && refus.right <= cadre.right + 1,
      }
    })
    // Le defilement doit vraiment ATTEINDRE le refus : on le scrolle en vue et
    // on verifie qu'il devient CLIQUABLE (dans le viewport), pas juste present
    // dans le DOM. C'est exactement ce qui a bloque le joueur (bouton present
    // mais jamais atteignable au doigt).
    const atteint = await onglet.evaluate(async () => {
      const refus = document.querySelector('.dc-pass')
      refus.scrollIntoView({ block: 'nearest' })
      await new Promise((r) => setTimeout(r, 50))
      const r = refus.getBoundingClientRect()
      return r.top >= 0 && r.bottom <= innerHeight && r.left >= 0 && r.right <= innerWidth
    })
    const probleme = [
      m.debordeLargeur > 1 && `deborde en largeur de ${m.debordeLargeur} px`,
      m.boutonCoupeEnLargeur && 'un bouton sort de la boite en largeur',
      m.boitehorsFenetre && 'la boite sort de la fenetre',
      !atteint && '« Annuler » reste inatteignable meme apres defilement',
    ].filter(Boolean)
    if (probleme.length) ecarts.push(`${n} option(s) en ${l}x${h} : ${probleme.join(', ')}`)
  }
  await onglet.close()
}
await navigateur.close()
console.log(ecarts.length ? ecarts.join('\n') : `OK : 4 tailles de liste x ${TAILLES.length} telephones, aucun debordement, « Annuler » toujours atteignable`)
process.exit(ecarts.length ? 1 : 0)
