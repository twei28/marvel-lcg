// GARDE : le recap de fin de phase (« Menace », « Heros et allies », « Nouveautes sur la table ») est
// lisible sur un telephone : aucun mot coupe lettre par lettre, aucun debordement horizontal.
//
//   cd ui-app && npx vitest run src/board/bilan-telephone.pires-cas.test.tsx   (ecrit le HTML du bilan)
//   cd ui-check && node scripts/garde-bilan-telephone.mjs                      (code de sortie 1 au moindre ecart)
//   BILAN_CSS_DIR=/chemin/vers/assets node scripts/garde-bilan-telephone.mjs   (autre feuille que ui-app/dist)
//   BILAN_CAPTURES=/dossier node scripts/garde-bilan-telephone.mjs             (ecrit une capture par taille)
//
// POURQUOI (26/10/2026) : sur un telephone (412 px), la scene de la phase se pose en bas, pleine largeur
// (`.deroule-phase:has(~ .plateau-portrait)`, mobile/portrait.css) ; les trois colonnes du bilan ne
// faisaient alors qu'une centaine de pixels et « Underground Distribution » s'ecrivait une lettre par ligne.
// Ce garde monte le VRAI HTML (ecrit par le test des pires cas) avec la VRAIE feuille construite, dans la meme
// disposition (la section suivie d'un `.plateau-portrait`), sur plusieurs tailles de telephone, et mesure.
import { chromium } from '@playwright/test'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const RACINE = path.resolve(ICI, '..', '..')
const ASSETS = process.env.BILAN_CSS_DIR || path.join(RACINE, 'ui-app/dist/assets')
const POLICES = path.join(RACINE, 'Fusion/marvel-lcg-src/public/fonts')
const CAS = path.join(os.tmpdir(), 'marvel-bilan-telephone')
const CAPTURES = process.env.BILAN_CAPTURES || ''
// Telephones en portrait, puis en paysage, puis le PC (qui ne doit pas etre degrade).
const TAILLES = [
  { nom: 'tel-412x915', l: 412, h: 915, portrait: true },
  { nom: 'tel-390x844', l: 390, h: 844, portrait: true },
  { nom: 'tel-360x740', l: 360, h: 740, portrait: true },
  { nom: 'tel-paysage-915x412', l: 915, h: 412, portrait: true },
  { nom: 'pc-1440x789', l: 1440, h: 789, portrait: false },
]

if (!fs.existsSync(CAS) || fs.readdirSync(CAS).length === 0) {
  console.error(`Aucun bilan dans ${CAS} : lancer d'abord le test bilan-telephone.pires-cas.`)
  process.exit(1)
}
const css = fs.readdirSync(ASSETS).filter((f) => f.endsWith('.css')).map((f) => fs.readFileSync(path.join(ASSETS, f), 'utf8')).join('\n')
const fichiers = fs.readdirSync(CAS).filter((f) => f.endsWith('.html'))
if (CAPTURES) fs.mkdirSync(CAPTURES, { recursive: true })

let page = ''
const navigateur = await chromium.launch()
const ecarts = []
for (const t of TAILLES) {
  const onglet = await navigateur.newPage({ viewport: { width: t.l, height: t.h }, hasTouch: t.portrait, isMobile: t.portrait })
  await onglet.route('http://garde.local/**', async (route) => {
    const chemin = new URL(route.request().url()).pathname
    if (chemin.startsWith('/public/fonts/')) {
      const f = path.join(POLICES, path.basename(chemin))
      if (fs.existsSync(f)) return route.fulfill({ body: fs.readFileSync(f), contentType: 'font/ttf' })
      return route.fulfill({ status: 404, body: '' })
    }
    return route.fulfill({ body: page, contentType: 'text/html' })
  })
  for (const fichier of fichiers) {
    const html = fs.readFileSync(path.join(CAS, fichier), 'utf8')
    // Sur telephone, la section est suivie du plateau portrait (c'est ce qui la pose en bas, pleine largeur).
    const suite = t.portrait ? '<div class="plateau-portrait"></div>' : ''
    page = `<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width, initial-scale=1"><style>${css}</style><style>*,*::before,*::after{animation:none!important;transition:none!important}</style><body class="${t.portrait ? 'mode-plateau-portrait ' : ''}cartouche-scene"><div id="racine">${html}${suite}</div></body>`
    await onglet.goto('http://garde.local/')
    await onglet.evaluate(() => document.fonts.ready)
    const m = await onglet.evaluate(() => {
      const bilan = document.querySelector('.deroule-bilan')
      const section = document.querySelector('.deroule-phase')
      if (!bilan || !section) return { erreur: 'bilan introuvable' }
      const coupes = []
      const marcheur = document.createTreeWalker(bilan, NodeFilter.SHOW_TEXT)
      for (let noeud = marcheur.nextNode(); noeud; noeud = marcheur.nextNode()) {
        const texte = noeud.textContent || ''
        for (const mot of texte.matchAll(/\S+/g)) {
          if (mot[0].length < 4) continue
          // La ligne (la position verticale) de chaque lettre : un saut de ligne ailleurs qu'apres un trait d'union coupe le mot.
          let derniere = null
          let coupe = false
          for (let i = 0; i < mot[0].length; i++) {
            const r = document.createRange()
            r.setStart(noeud, mot.index + i)
            r.setEnd(noeud, mot.index + i + 1)
            const rect = r.getBoundingClientRect()
            if (!rect.height) continue
            if (derniere !== null && Math.abs(rect.top - derniere) > 4 && mot[0][i - 1] !== '-') coupe = true
            derniere = rect.top
          }
          if (coupe) coupes.push(mot[0])
        }
      }
      // Une ligne de « La phase en bref » coupee par des points de suspension est illisible.
      const lignesCoupees = [...bilan.querySelectorAll('.essai-bilan-ligne')].filter((l) => l.scrollWidth > l.clientWidth + 1).length
      const b = bilan.getBoundingClientRect()
      const s = section.getBoundingClientRect()
      let hors = 0
      for (const el of bilan.querySelectorAll('*')) {
        if (el.closest('.scan-fallback')) continue
        const r = el.getBoundingClientRect()
        if (!r.width || !r.height) continue
        hors = Math.max(hors, r.right - s.right, s.left - r.left)
      }
      // Une colonne trop etroite (< 140 px) rend le texte illisible meme sans coupure de mot.
      const colonnes = [...bilan.querySelectorAll(':scope > .deroule-colonne')].map((c) => Math.round(c.getBoundingClientRect().width))
      return {
        coupes,
        lignesCoupees,
        hors: Math.round(hors),
        debordeBilan: Math.max(0, bilan.scrollWidth - bilan.clientWidth),
        debordeSection: Math.max(0, section.scrollWidth - section.clientWidth),
        colonneMin: colonnes.length ? Math.min(...colonnes) : 0,
        largeurBilan: Math.round(b.width),
      }
    })
    if (CAPTURES) await onglet.screenshot({ path: path.join(CAPTURES, `${t.nom}-${fichier.replace('.html', '')}.png`) })
    const nom = `${t.nom} ${fichier}`
    if (m.erreur) ecarts.push(`${nom} : ${m.erreur}`)
    else {
      if (m.coupes.length) ecarts.push(`${nom} : mots coupes lettre par lettre : ${[...new Set(m.coupes)].slice(0, 6).join(', ')}`)
      if (t.portrait && m.lignesCoupees > 0) ecarts.push(`${nom} : ${m.lignesCoupees} ligne(s) de « La phase en bref » coupee(s) par des points de suspension`)
      if (m.hors > 2) ecarts.push(`${nom} : du contenu sort de la boite de ${m.hors} px`)
      // Le defilement de la SECTION entiere (l'en-tete des onglets, +7 px) n'est pas le bilan : signale, sans faire echouer.
      if (m.debordeBilan > 1) ecarts.push(`${nom} : le bilan deborde de ${m.debordeBilan} px`)
      if (m.debordeSection > 1) console.log(`note ${nom} : la section deborde de ${m.debordeSection} px (en-tete des onglets, hors bilan)`)
      if (t.portrait && m.colonneMin > 0 && m.colonneMin < 140) ecarts.push(`${nom} : une section ne fait que ${m.colonneMin} px de large (< 140)`)
      if (!ecarts.some((e) => e.startsWith(nom))) console.log(`ok  ${nom} : sections >= ${m.colonneMin} px, bilan ${m.largeurBilan} px`)
    }
  }
  await onglet.close()
}
await navigateur.close()
if (ecarts.length) {
  console.error('\nECARTS :\n' + ecarts.map((e) => '  - ' + e).join('\n'))
  process.exit(1)
}
console.log(`OK : ${fichiers.length} bilan(s) x ${TAILLES.length} tailles, aucun mot coupe, aucun debordement`)
