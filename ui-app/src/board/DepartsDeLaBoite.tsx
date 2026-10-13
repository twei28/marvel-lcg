// Les cartes de la boîte qui partent à la défausse rencontre au clic (essai, 13/10/2026).
//
// Décisions de l'utilisateur : « les boosts volent ensemble vers la défausse
// rencontre au clic » (encadré ④) et « la traîtrise vole vers la défausse
// rencontre au clic » (encadré ⑫). Ces cartes ne sont jamais sur la table :
// elles vivent dans la boîte le temps de leur écran. On relève leur place à
// chaque rendu ; au clic (un nouvel écran), une copie part de cette place vers
// la défausse. Une carte qu'un boost ★ a mise en jeu est sur la table : elle
// n'est pas concernée (EtoilesEnAttente la fait arriver à sa place).
import { useEffect, useLayoutEffect, useRef } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { carteDeLaTable } from './FlechesPhase'
import { animationsCoupees, copieVolante, voler } from './TrajetsPhase'

/** Les cartes que cet écran envoie à la défausse rencontre quand on le quitte. */
export function cartesQuiPartent(etape: EtapeDeroule | undefined, boostsMontres: number): number[] {
  if (!etape || etape.etat === 'annonce') return []
  if ((etape.titre === 'attaque' || etape.titre === 'manigance') && etape.etat !== 'annule') {
    return etape.boosts.slice(0, boostsMontres).map((boost) => boost.cibleId)
  }
  if (etape.titre === 'revelation' && etape.carteId !== undefined && /treachery|traîtrise/i.test(etape.typeCarte ?? '')) {
    return [etape.carteId]
  }
  return []
}

type Releve = { rect: DOMRect; src?: string }

export function DepartsDeLaBoite({ etape, boostsMontres, actif }: { etape: EtapeDeroule | undefined; boostsMontres: number; actif: boolean }) {
  const ids = actif ? cartesQuiPartent(etape, boostsMontres) : []
  const cle = etape?.cle
  type Ecran = { cle: string | undefined; cartes: Map<number, Releve> }
  const courant = useRef<Ecran>({ cle: undefined, cartes: new Map() })
  const quitte = useRef<Ecran | undefined>(undefined)

  // A chaque rendu : la place des cartes de l'écran dans la boîte. Un nouvel
  // écran met de côté les relevés de l'écran quitté, pris avant qu'il change.
  useLayoutEffect(() => {
    if (courant.current.cle !== cle) {
      quitte.current = courant.current
      courant.current = { cle, cartes: new Map() }
    }
    const boite = document.querySelector('.deroule-phase.est-essai .deroule-corps')
    for (const id of ids) {
      const el = boite?.querySelector<HTMLElement>(`[data-card-id="${id}"]`)
      const rect = el?.getBoundingClientRect()
      if (!el || !rect || rect.width === 0) continue
      courant.current.cartes.set(id, { rect, src: el.querySelector('img')?.getAttribute('src') ?? undefined })
    }
  })

  // Au clic : les cartes de l'écran quitté partent vers la défausse rencontre.
  useEffect(() => {
    const avant = quitte.current
    quitte.current = undefined
    if (!avant || avant.cle === undefined || avant.cartes.size === 0 || animationsCoupees()) return
    const pile = document.querySelector<HTMLElement>('.plateau-cadre [data-pile$="encounter-discard"]')?.getBoundingClientRect()
    if (!pile || pile.width === 0) return
    const vols: Animation[] = []
    for (const [id, { rect, src }] of avant.cartes) {
      if (carteDeLaTable(id)) continue
      const copie = copieVolante(src, rect)
      const animation = voler(copie, rect, pile, true)
      animation.onfinish = () => copie.remove()
      vols.push(animation)
    }
    return () => {
      // Un nouveau clic termine les vols d'un coup (décision 53).
      for (const a of vols) a.finish()
    }
  }, [cle])

  return null
}
