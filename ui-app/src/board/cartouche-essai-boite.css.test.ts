// La boite de la phase du mechant (essai, refonte du 12/10/2026) : verrous sur
// la feuille. La mesure reelle (« Continuer » au meme pixel) se fait dans un
// navigateur sur un moteur d'essai ; ici, ce qui la garantit dans la feuille.
import { describe, expect, it } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'

const css = fs.readFileSync(path.join(__dirname, 'cartouche-essai.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')
const tel = fs.readFileSync(path.join(__dirname, 'cartouche-essai-tel.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')
const bloc = css.slice(css.indexOf('@media (min-width: 768px)'))

function regle(selecteur: string): string {
  const i = bloc.indexOf(`${selecteur} {`)
  expect(i, selecteur).toBeGreaterThan(-1)
  return bloc.slice(i, bloc.indexOf('}', i))
}

describe('la boite fixe de la colonne de gauche', () => {
  it('largeur et hauteur fixes, en position fixe a gauche, jamais au centre', () => {
    const r = regle('.deroule-phase.est-scene.est-essai.est-essai')
    expect(r).toMatch(/position:\s*fixed/)
    expect(r).toMatch(/left:\s*var\(--essai-marge\)/)
    expect(r).toMatch(/width:\s*var\(--essai-l\)/)
    // Toute la hauteur disponible (13/10/2026), sans plafond.
    expect(r).toMatch(/height:\s*calc\(100dvh - var\(--colonne-haut, 48px\) - 2 \* var\(--essai-marge\)\)/)
    expect(r).toMatch(/border:\s*3px solid var\(--cadre-joueur/)
  })

  it('600 px de large, 520 px sous 1500 px de large', () => {
    expect(regle(':root')).toMatch(/--essai-l:\s*600px/)
    const i = bloc.indexOf('@media (max-width: 1499px)')
    expect(i).toBeGreaterThan(-1)
    expect(bloc.slice(i, bloc.indexOf('}', i))).toMatch(/--essai-l:\s*520px/)
    // L'onglet le plus long garde sa police lisible a 520 px. La regle vient
    // APRES celle de la finition (1.45) : avant, elle etait sans effet.
    const j = bloc.lastIndexOf('@media (max-width: 1499px)')
    expect(j).toBeGreaterThan(bloc.indexOf('flex-grow: 1.45'))
    expect(bloc.slice(j)).toMatch(/\.deroule-pastille:nth-child\(4\) \{\s*flex-grow:\s*1\.8/)
    expect(bloc.slice(j)).toMatch(/\.deroule-bilan \.deroule-lignes li \{\s*flex-wrap:\s*wrap/)
  })

  it('la table se decale de la largeur de la boite : rien ne la couvre', () => {
    expect(regle('body.phase-essai-colonne .plateau-cadre')).toMatch(/margin-left:\s*calc\(var\(--essai-l\)/)
  })

  it('« Continuer » a une taille fixe dans un pied de hauteur fixe', () => {
    expect(regle('.deroule-phase.est-scene.est-essai.est-essai .deroule-boutons')).toMatch(/height:\s*84px/)
    const bouton = regle('.deroule-phase.est-scene.est-essai.est-essai .deroule-boutons .deroule-suivant')
    expect(bouton).toMatch(/width:\s*220px/)
    expect(bouton).toMatch(/height:\s*52px/)
  })

  it('le corps ne pousse jamais le pied, sans barre de defilement', () => {
    const r = regle('.deroule-phase.est-scene.est-essai.est-essai .deroule-corps')
    expect(r).toMatch(/flex:\s*1 1 0/)
    expect(r).toMatch(/overflow:\s*hidden/)
  })
})

describe('le telephone', () => {
  it('feuille basse a environ 40 % de la hauteur (decision 30)', () => {
    expect(tel).toMatch(/height:\s*40dvh/)
    // 70 % seulement le temps d'une question (finition du 12/10/2026), jamais en regle generale.
    const sansQuestion = tel.replace(/\.deroule-phase\.est-scene\.est-essai\.a-question:not\(\.est-reduit\) \{[^}]*\}/, '')
    expect(sansQuestion).not.toMatch(/70dvh/)
  })
})

describe('lot 2 : une seule taille de carte par ecran', () => {
  const lot2 = css.slice(css.indexOf('.deroule-phase.est-scene.est-essai.est-essai,\n.deroule-phase.est-scene.est-essai.est-essai * {'))

  it('toutes les hauteurs de carte de la boite suivent --essai-carte-h, sur chaque element', () => {
    expect(lot2.length, 'la regle du lot 2').toBeGreaterThan(0)
    const r = lot2.slice(0, lot2.indexOf('}'))
    expect(r).toMatch(/--vignette-h:\s*var\(--essai-carte-h, 170px\) !important/)
    expect(r).toMatch(/--grande-h:\s*var\(--essai-carte-h, 170px\) !important/)
  })

  it('les nouveautes du bilan ne sont plus a 70 %', () => {
    expect(lot2).toMatch(/\.deroule-nouveautes \.deroule-vignette \.scan-card \{\s*--card-w: calc\(var\(--vignette-h\) \* 127 \/ 176\)/)
  })

  it('aucun agrandissement sur place au survol dans la boite', () => {
    expect(lot2).toMatch(/\.est-essai \.scan-card:hover \.scan-visuel \{\s*transform: none/)
  })
})

describe('finition (12/10/2026) : rien ne pousse « Continuer », rien n est coupe', () => {
  it('le pied reste sur une ligne : de longues mentions ne font plus descendre Continuer', () => {
    expect(regle('.deroule-phase.est-scene.est-essai.est-essai > .deroule-boutons')).toMatch(/flex-wrap:\s*nowrap/)
  })

  it('« X est vaincu » prend toute la largeur, sous les cartes', () => {
    expect(regle('.deroule-phase.est-scene.est-essai.est-essai .deroule-corps > .deroule-defaite')).toMatch(/flex:\s*0 0 100%/)
  })

  it('le titre tient en deux lignes au plus', () => {
    expect(regle('.deroule-phase.est-scene.est-essai.est-essai .essai-titre-ligne .deroule-titre-court')).toMatch(/-webkit-line-clamp:\s*2/)
  })

  it('le refus agrandi 1,5 fois se borne a la boite', () => {
    expect(regle('.deroule-phase.est-scene.est-essai.est-essai .deroule-boutons [data-refus]')).toMatch(/max-width:\s*calc\(\(var\(--essai-l\) - 48px\) \/ 1\.5\)/)
  })

  it('au telephone, la feuille monte a 70 % le temps d une question seulement', () => {
    const i = tel.indexOf('.deroule-phase.est-scene.est-essai.a-question:not(.est-reduit) {')
    expect(i).toBeGreaterThan(-1)
    expect(tel.slice(i, tel.indexOf('}', i))).toMatch(/height:\s*70dvh/)
  })
})
