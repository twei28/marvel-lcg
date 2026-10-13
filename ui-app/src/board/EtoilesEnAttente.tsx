// Les cartes qu'un boost ★ met en jeu arrivent sur la table AU CLIC (essai, 13/10/2026).
//
// Demande de l'utilisateur : « quand on révèle les boosts et que le boost est une
// étoile, tu la mets directement en jeu. J'aimerais qu'elle se mette en jeu à la
// fin de l'attaque du méchant ou de sa manigance. » Ses choix :
//  - au clic sur Continuer qui quitte l'écran de l'attaque (ou de la manigance),
//    sans écran en plus ;
//  - pendant l'écran, sa place sur la table reste vide, en pointillés, avec le
//    trait depuis la boîte (le bandeau « NOUVEAU SBIRE » reste dans la boîte) ;
//  - pour TOUT ce qu'un boost ★ met en jeu (sbire, manigance annexe,
//    attachement, environnement), pendant une attaque ou une manigance.
//
// ⚠ Seul l'affichage attend : le moteur a deja resolu le ★ au retournement,
// comme le veut la regle. La carte est donc dans le monde ; on la marque
// (`data-etoile-attente`), `TrajetsPhase` ne la fait pas voler a son apparition,
// et c'est ce composant qui la fait voler au clic.
import { useEffect, useLayoutEffect, useRef } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { animationsCoupees, copieVolante, voler } from './TrajetsPhase'

const ATTRIBUT = 'data-etoile-attente'
/** La place vide en pointilles, deja dessinee par trajets-phase.css. */
const CLASSE = 'trajet-arrivee'

/** Les cartes que les boosts ★ deja retournes de cet ecran ont mises en jeu. */
export function etoilesDeLEcran(etape: EtapeDeroule | undefined, boostsMontres: number): number[] {
  if (!etape || (etape.titre !== 'attaque' && etape.titre !== 'manigance')) return []
  if (etape.etat === 'annonce' || etape.etat === 'annule') return []
  return etape.boosts.slice(0, boostsMontres).filter((boost) => boost.etoile).map((boost) => boost.cibleId)
}

function carteDeLaTable(id: number): HTMLElement | undefined {
  for (const el of document.querySelectorAll<HTMLElement>(`.plateau-cadre .scan-card[data-card-id="${id}"]`)) {
    if (!el.closest('.deroule-phase') && !el.classList.contains('is-facedown')) return el
  }
  return undefined
}

export function EtoilesEnAttente({
  etape,
  boostsMontres,
  actif,
}: {
  etape: EtapeDeroule | undefined
  boostsMontres: number
  actif: boolean
}) {
  const ids = actif ? etoilesDeLEcran(etape, boostsMontres) : []
  const signature = ids.join(',')
  const cle = etape?.cle
  const enAttente = useRef<{ cle: string | undefined; ids: number[] }>({ cle: undefined, ids: [] })

  // Pendant l'ecran : la place reste vide. Le plateau se redessine souvent :
  // on repose la marque a chaque changement de la table.
  useLayoutEffect(() => {
    if (ids.length === 0 || typeof document === 'undefined') return
    const marquer = () => {
      for (const id of ids) {
        const el = carteDeLaTable(id)
        if (!el) continue
        if (!el.hasAttribute(ATTRIBUT)) el.setAttribute(ATTRIBUT, '')
        if (!el.classList.contains(CLASSE)) el.classList.add(CLASSE)
      }
    }
    marquer()
    const table = document.querySelector('.plateau-cadre')
    const observateur = typeof MutationObserver === 'undefined' ? undefined : new MutationObserver(marquer)
    if (table) observateur?.observe(table, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] })
    return () => observateur?.disconnect()
    // `ids` est recalcule a chaque rendu : sa signature suffit.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cle, signature])

  // Au clic (un nouvel ecran) : les cartes de l'ecran quitte volent de la boite a leur place.
  useEffect(() => {
    const avant = enAttente.current
    enAttente.current = { cle, ids }
    if (avant.cle === cle || avant.ids.length === 0) return
    const coupees = animationsCoupees()
    const boite = document.querySelector<HTMLElement>('.deroule-phase.est-essai .deroule-corps')
    const animations: Animation[] = []
    for (const id of avant.ids) {
      if (ids.includes(id)) continue
      const el = carteDeLaTable(id)
      if (!el) continue
      el.removeAttribute(ATTRIBUT)
      const arrivee = el.getBoundingClientRect()
      if (coupees || !boite || arrivee.width === 0) {
        el.classList.remove(CLASSE)
        continue
      }
      const depart = boite.getBoundingClientRect()
      const copie = copieVolante(el.querySelector('img')?.getAttribute('src') ?? undefined, depart)
      const animation = voler(copie, depart, arrivee, false)
      animation.onfinish = () => {
        copie.remove()
        el.classList.remove(CLASSE)
      }
      animations.push(animation)
    }
    return () => {
      // Un nouveau clic termine le vol d'un coup (decision 53).
      for (const a of animations) a.finish()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cle, signature])

  return null
}
