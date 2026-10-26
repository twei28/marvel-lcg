// LE RECAP DE FIN DE PHASE SUR TELEPHONE (26/10/2026).
//
// Signale par l'utilisateur sur son telephone (412 px de large, partie en ligne) : le bilan de
// la phase du mechant (« Menace », « Heros et allies », « Nouveautes sur la table ») mettait les
// lettres l'une sous l'autre, car les trois colonnes ne faisaient qu'une centaine de pixels
// chacune. Ce fichier monte le VRAI bilan (CartouchePhase, essai) avec les noms les plus longs
// d'une vraie partie, verifie sa structure, et ecrit son HTML dans le dossier temporaire du
// systeme : `ui-check/scripts/garde-bilan-telephone.mjs` le monte ensuite dans Chromium, avec
// la vraie feuille construite, sur plusieurs tailles de telephone, et mesure qu'aucun mot n'est
// coupe lettre par lettre et que rien ne depasse.
import { cleanup, render } from '@testing-library/react'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import { CartouchePhase, type CartouchePhaseProps } from './CartouchePhase'
import type { EtapeDeroule } from './deroule-phase'

export const DOSSIER_BILAN_TELEPHONE = path.join(os.tmpdir(), 'marvel-bilan-telephone')

class RO {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeAll(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = RO
  fs.mkdirSync(DOSSIER_BILAN_TELEPHONE, { recursive: true })
})
afterEach(() => cleanup())

const scan = (id: number): ScanCardProps => ({ id: String(id), name: `carte ${id}`, kind: 'minion', imageUrl: '' })

const SHANG = 12
const MANIGANCE = 70
const GARDE = 61
const menace: EtapeDeroule = {
  cle: 'menace:1', temps: 'menace', titre: 'menace', regle: '', cibleId: MANIGANCE, cibleNom: 'Underground Distribution',
  montant: 1, restant: 2, plafond: 6, boosts: [],
}
const attaque: EtapeDeroule = {
  cle: 'activation:3', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu', carteId: 50, cibleId: SHANG,
  auteurNom: 'Armored Guard', cibleNom: 'Shang-Chi', base: 5, montant: 5, restant: 5, boosts: [],
}
const revelee: EtapeDeroule = {
  cle: 'revelation:2', temps: 'revelation', titre: 'revelation', regle: '', carteId: GARDE, auteurNom: 'Klaw',
  cibleNom: 'Armored Guard', typeCarte: 'Minion', boosts: [],
}
const bilan: EtapeDeroule = { cle: 'bilan', temps: 'bilan', titre: 'bilan', regle: '', boosts: [] }
const ETAPES = [menace, revelee, attaque, bilan]
const g = { onPointerDown: () => {}, onPointerMove: () => {}, onPointerUp: () => {}, onPointerCancel: () => {} }

function monter(dynamique: boolean, bis: boolean) {
  const props: CartouchePhaseProps = {
    refCartouche: () => {}, gestes: g, etape: bilan, etapes: ETAPES, index: 3, efface: false, questionAuJoueur: false,
    avancer: vi.fn(), enAttente: false, attendUnAutreJoueur: false, defaiteLocale: false, boostsMontres: 99,
    tempsParDecision: 0, cartesDistribuees: 0, carteScene: scan, pvMaxParNom: new Map([['Shang-Chi', 12]]),
    essai: true, dynamique, bis,
  }
  return render(<CartouchePhase {...props} />)
}

describe('le recap de fin de phase sur telephone', () => {
  // `bis` : la presentation « Etape par etape » (le bilan prend toute la largeur de la boite, comme sur le telephone) ;
  // `dynamique` : la presentation dynamique (une seule colonne, deja lisible). Les trois variantes sont ecrites pour le garde.
  const VARIANTES = [
    { nom: 'dynamique', dynamique: true, bis: true },
    { nom: 'etape-par-etape', dynamique: false, bis: true },
    { nom: 'sans-bis', dynamique: false, bis: false },
  ]
  for (const v of VARIANTES) {
    it(`${v.nom} : trois sections, ecrites pour le garde`, () => {
      const { container } = monter(v.dynamique, v.bis)
      const bilanEl = container.querySelector('.deroule-bilan')
      expect(bilanEl, 'le bilan existe').not.toBeNull()
      expect(bilanEl?.querySelectorAll('.deroule-colonne').length).toBeGreaterThanOrEqual(3)
      expect(container.textContent).toContain('Underground Distribution')
      fs.writeFileSync(path.join(DOSSIER_BILAN_TELEPHONE, `bilan-${v.nom}.html`), container.innerHTML)
    })
  }
})

// ⚠ LE PIEGE DES COUCHES (26/10/2026) : les regles du bilan (cartouche-phase.css, cartouche-essai.css) ne sont dans
// AUCUNE `@layer`, et une regle sans couche l'emporte toujours sur une regle en couche. La premiere ecriture de
// l'empilement, dans `@layer utilitaires`, etait sans effet. Ce test garde la regle HORS couche et sous 600 px.
describe("la regle d'empilement du bilan sur telephone", () => {
  it('est hors de toute @layer, sous 600 px, et empile les sections en une colonne', () => {
    const css = fs.readFileSync(path.join(__dirname, 'mobile', 'portrait.css'), 'utf8')
    const debut = css.indexOf('/* Le recap de fin de phase')
    expect(debut, 'le commentaire de la regle existe').toBeGreaterThan(0)
    // Les commentaires parlent de `@layer` : on ne mesure que le code.
    const bloc = css.slice(debut).replace(/\/\*[\s\S]*?\*\//g, '')
    expect(bloc.includes('@layer')).toBe(false)
    const regle = bloc.match(/@media \(max-width: 600px\) \{([\s\S]*?)\n\}\s*$/)
    expect(regle, 'un @media (max-width: 600px) termine le fichier').not.toBeNull()
    expect(regle?.[1]).toMatch(/\.deroule-bilan\s*\{[^}]*grid-template-columns:\s*minmax\(0,\s*1fr\)/)
  })
})
