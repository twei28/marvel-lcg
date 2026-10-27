// Banc de rendu du voile FR pour l'export ZIP des images de cartes (27/10/2026).
//
// Pourquoi un vrai navigateur : le voile n'est pas qu'une analyse de pixels. La
// zone est lue sur le scan (traduction-posee.ts), le fond est nettoyé de ses
// lettres (effacer-texte.ts, dans un Worker), puis le français est MIS EN PAGE
// par le navigateur (polices de la carte, flottants `shape-outside`, police qui
// rétrécit jusqu'à tenir). Rejouer la mise en page ailleurs serait une seconde
// implémentation, qui divergerait. On monte donc ICI le composant même du
// plateau, `TraductionPosee`, avec le même texte que le plateau choisirait, et
// rendre-voile.mjs photographie le résultat.
//
// API exposée à Playwright : window.exportVoile.texte(code) et .poser(carte).
import { createRoot, type Root } from 'react-dom/client'
import { TraductionPosee, zoneDuScan } from '../../src/board/TraductionPosee'
import { chargerCatalogue } from '../../src/board/catalogue'
import { codeCarteConnu } from '../../src/board/marvelcdb'
import { TEXTES_FR } from '../../src/board/textes-fr'
import { TEXTES_FR_FANMADE } from '../../src/board/textes-fr-fanmade'
import { coteDuTexte, typeDeBoite } from '../../src/board/traduction-carte'
import { VOILE_UNI } from '../../src/board/zones-corrections'

type Complets = Readonly<Record<string, string | undefined>>
let complets: Promise<Complets> | undefined

/**
 * Le texte français que le site connaît pour cette carte, ou null.
 *
 * Mêmes dictionnaires, dans le même ordre, que `useTraductionFr`
 * (traduction-carte.tsx) : textes-fr (officielles sans scan FR), puis le
 * fan-made traduit à la main, puis le texte officiel complet. Le plateau ne
 * prend ce dernier que pour un art alternatif (ailleurs il montre le scan FR) ;
 * l'export, lui, veut le voile de TOUTE carte traduite, scan FR ou non.
 * Même filtre de code aussi (`codeCarteConnu`) : une carte que le plateau ne
 * traduit jamais n'a pas de voile ici non plus.
 */
async function texte(codeCarte: string): Promise<{ texte: string; traits: string[] } | null> {
  const code = codeCarteConnu(codeCarte)
  if (!code) return null
  let trouve = TEXTES_FR[code] ?? TEXTES_FR_FANMADE[code]
  if (!trouve) {
    complets ??= import('../../src/board/textes-fr-complets').then((m) => m.TEXTES_FR_COMPLETS)
    trouve = (await complets)[code]
  }
  if (!trouve) return null
  const catalogue = await chargerCatalogue()
  return { texte: trouve, traits: catalogue.traits?.(code) ?? [] }
}

type Carte = { code: string; url: string; largeur: number; hauteur: number; type?: string; texte: string; traits: string[] }
type Resultat = { pose: boolean; fondNettoye: boolean; raison?: string }

const attendre = (ms: number) => new Promise((r) => setTimeout(r, ms))
const image = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))

let racine: Root | null = null

/** Monte la carte dans un cadre de la taille EXACTE du scan (pas de rognage : `zoneDansLeCadre` ne déplace rien). */
async function poser(carte: Carte): Promise<Resultat> {
  await chargerCatalogue()
  const scene = document.getElementById('scene') as HTMLDivElement
  racine?.unmount()
  scene.innerHTML = ''
  racine = createRoot(scene)
  const cote = coteDuTexte(typeDeBoite(carte.type))
  // Paysage : rendre-voile.mjs n'envoie que des complots déjà couchés (le script Python les tourne comme le plateau).
  const paysage = carte.largeur > carte.hauteur ? cote : undefined
  if (carte.largeur > carte.hauteur && !paysage) return { pose: false, fondNettoye: false, raison: 'paysage-sans-boite' }
  racine.render(
    <div className="cadre" style={{ position: 'relative', width: carte.largeur, height: carte.hauteur, overflow: 'hidden' }}>
      <img src={carte.url} alt="" style={{ display: 'block', width: '100%', height: '100%', objectFit: 'cover' }} />
      <TraductionPosee url={carte.url} texte={carte.texte} traits={carte.traits} paysage={paysage} />
    </div>
  )
  // Même promesse (cache par adresse) que celle qu'attend le composant.
  const zone = await zoneDuScan(carte.url, paysage)
  if (!zone) return { pose: false, fondNettoye: false, raison: 'zone-non-reconnue' }
  const img = scene.querySelector('img')
  if (img && !img.complete) await new Promise((r) => img.addEventListener('load', r, { once: true }))
  // Le fond nettoyé arrive du Worker : on l'attend (15 s au plus), sauf pour les cartes en voile uni.
  const uni = VOILE_UNI.has(carte.code)
  let fondNettoye = false
  for (let i = 0; i < 300; i += 1) {
    const boite = scene.querySelector<HTMLElement>('.traduction-posee')
    if (boite && (uni || boite.style.background.includes('url('))) {
      fondNettoye = !uni
      break
    }
    await attendre(50)
  }
  await document.fonts.ready
  // La police se règle dans un useLayoutEffect, puis une seconde fois quand les polices sont prêtes : on laisse passer.
  await image()
  await attendre(120)
  await image()
  return { pose: scene.querySelector('.traduction-posee') !== null, fondNettoye }
}

declare global {
  interface Window {
    exportVoile: { texte: typeof texte; poser: typeof poser; pret: boolean }
  }
}
window.exportVoile = { texte, poser, pret: true }
