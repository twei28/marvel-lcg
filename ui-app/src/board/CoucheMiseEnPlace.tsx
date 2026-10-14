// La mise en place montrée carte par carte (voir mise-en-place-pas-a-pas.ts).
//
// Chaque carte qui arrive en jeu s'affiche en grand au centre, plateau
// assombri, avec sa légende ; « Continuer » (ou Espace) la fait glisser à sa
// place, où un contour arrondi la repère brièvement, une seule fois.
//
// Tant qu'elle attend son tour, la table ne la montre pas : sa place est un
// contour en pointillés (13/10/2026, voir `attenteSurTable`). Pendant le vol,
// le voile s'efface pour qu'on la voie se poser.

import { useCallback, useEffect, useRef, useState } from 'react'
import './mise-en-place.css'
import { scanUrl } from './card-model'
import { t } from './langue'
import type { World } from './world'
import { TraductionSurCarte, typeDeBoite } from './traduction-carte'
import {
  etapesNouvelles,
  ordonnerRetournements,
  type EtapeMiseEnPlace,
  type MemoireMiseEnPlace,
  type Reglages,
} from './mise-en-place-pas-a-pas'

export type EtatMiseEnPlace = {
  /** La mise en place est en cours (round 0). */
  enCours: boolean
  /** Le voile d'ouverture couvre encore la table : on attend avant de compter. */
  voile: boolean
  /** Spectateur, relecture, mode manuel : personne à qui montrer pas à pas. */
  muet: boolean
}

/**
 * La file des étapes à montrer, et le geste qui passe à la suivante.
 *
 * Hors mise en place (ou en mode muet), la mémoire suit le monde sans rien
 * produire : une partie rechargée en cours de round ne rejoue pas sa table.
 */
export function useMiseEnPlacePasAPas(monde: World | undefined, etat: EtatMiseEnPlace) {
  const memoire = useRef<MemoireMiseEnPlace>(new Map())
  const dernier = useRef<number | undefined>(undefined)
  const [file, setFile] = useState<EtapeMiseEnPlace[]>([])

  useEffect(() => {
    if (!monde) return
    const rendu = monde.render_id
    if (rendu === dernier.current) return
    const resynchro = dernier.current !== undefined && rendu < dernier.current
    dernier.current = rendu
    const reglages: Reglages = {
      panneauPrincipale: monde.confirm_main_scheme === true,
      panneauAnnexe: monde.confirm_side_scheme === true,
    }
    if (etat.enCours && etat.voile && !etat.muet) {
      // On attend que la table se montre : la mémoire reste vide pour que
      // tout ce qui est déjà posé soit présenté au lever du voile.
      dernier.current = undefined
      return
    }
    const { etapes, memoire: suite } = etapesNouvelles(memoire.current, monde, reglages)
    memoire.current = suite
    if (resynchro) {
      setFile([])
      return
    }
    if (!etat.enCours || etat.muet || etapes.length === 0) return
    // Toute la file en attente se reordonne, tete comprise : une etape masquee
    // (choix de la tour de Tower Defense) n'a pas encore ete vue, et 2B y
    // attendait quand 1B est arrive.
    setFile((f) => ordonnerRetournements([...f, ...etapes], monde, 0))
  }, [monde, monde?.render_id, etat.enCours, etat.voile, etat.muet])

  // Plus de mise en place (partie lancée, ou finie avant d'y arriver) : ce qui
  // attendait encore n'a plus rien à montrer. Effet à part : la fin ne vient
  // pas forcément avec une trame neuve.
  useEffect(() => {
    if (!etat.enCours || etat.muet) setFile((f) => (f.length ? [] : f))
  }, [etat.enCours, etat.muet])

  // ⚠ LA TRAME OÙ UNE CARTE ARRIVE EST DESSINÉE AVANT L'EFFET CI-DESSUS : sans
  // cet aperçu, la carte s'affichait à sa place le temps d'une image avant de
  // passer en pointillés. La mémoire n'a pas encore vu la trame : on la compare
  // sans rien retenir. Pas de useMemo : une fois la trame retenue par l'effet,
  // l'aperçu doit tomber à vide, sinon la carte restait en pointillés.
  const apercu =
    !monde || !etat.enCours || etat.voile || etat.muet || monde.render_id === dernier.current
      ? []
      : etapesNouvelles(memoire.current, monde, {
          panneauPrincipale: monde.confirm_main_scheme === true,
          panneauAnnexe: monde.confirm_side_scheme === true,
        }).etapes

  const suivant = useCallback(() => setFile((f) => f.slice(1)), [])
  return {
    etape: file[0] as EtapeMiseEnPlace | undefined,
    restantes: file.length,
    suivant,
    /** Les étapes pas encore validées, celle affichée comprise. */
    enAttente: apercu.length > 0 ? [...file, ...apercu] : file,
  }
}

function marquer(carteId: number, animations: boolean) {
  const cible = document.querySelector<HTMLElement>(`.scan-card[data-card-id="${carteId}"]`)
  if (!cible) return
  cible.classList.add('mep-repere')
  if (animations) cible.classList.add('mep-repere-anime')
  window.setTimeout(() => cible.classList.remove('mep-repere', 'mep-repere-anime'), 1000)
}

export const DUREE_VOL = 400

/** Une copie de `depart` vole vers la carte de la table ; `fini` à l'arrivée (tout de suite si rien ne vole). */
export function glisser(depart: HTMLElement | null, carteId: number, fini?: () => void) {
  const cible = document.querySelector<HTMLElement>(`.scan-card[data-card-id="${carteId}"]`)
  const a = depart?.getBoundingClientRect()
  const b = cible?.getBoundingClientRect()
  if (!depart || !a || !b || typeof depart.animate !== 'function' || !a.width || !b.width) {
    fini?.()
    return
  }
  const fantome = depart.cloneNode(true) as HTMLElement
  fantome.className = `${depart.className} mep-fantome`
  Object.assign(fantome.style, {
    position: 'fixed',
    left: `${a.left}px`,
    top: `${a.top}px`,
    width: `${a.width}px`,
    height: `${a.height}px`,
    margin: '0',
  })
  document.body.appendChild(fantome)
  const dx = b.left + b.width / 2 - (a.left + a.width / 2)
  const dy = b.top + b.height / 2 - (a.top + a.height / 2)
  const echelle = Math.min(b.width / a.width, b.height / a.height)
  const anim = fantome.animate(
    [{ transform: 'none', opacity: 1 }, { transform: `translate(${dx}px, ${dy}px) scale(${echelle})`, opacity: 0.85 }],
    { duration: DUREE_VOL, easing: 'ease-in-out' }
  )
  // Un seul appel, même si l'animation et le filet arrivent tous les deux.
  let fait = false
  const finir = () => {
    fantome.remove()
    if (fait) return
    fait = true
    fini?.()
  }
  anim.onfinish = finir
  anim.oncancel = finir
  window.setTimeout(finir, DUREE_VOL + 300)
}

/**
 * Les places en attente : un contour en pointillés à la taille de la carte,
 * pour que rien ne bouge quand elle se pose (décision du 13/10/2026).
 */
export function PlacesEnAttente({ ids }: { ids: ReadonlySet<number> }) {
  if (ids.size === 0) return null
  const cartesVisees = [...ids].map((id) => `.scan-card[data-card-id="${id}"]:not(.mep-fantome)`)
  return (
    <style>
      {[
        `${cartesVisees.join(',\n')} { outline: 2px dashed rgba(240, 185, 95, 0.75); outline-offset: -2px; background: transparent !important; box-shadow: none !important; filter: none !important; animation: none !important; }`,
        `${cartesVisees.map((c) => `${c} > *`).join(',\n')} { visibility: hidden !important; }`,
        // Les stades à venir empilés derrière la carte, et leur loupe (Board.tsx,
        // `stagesArriere`) : à côté de la carte, pas dedans. Sur Tower Defense,
        // Proxima Midnight II et 2A restaient visibles au-dessus des pointillés.
        `${[...ids]
          .map((id) => `.plateau-unite:has(> .scan-card[data-card-id="${id}"]) > :is(.stage-arriere, .stages-bouton)`)
          .join(',\n')} { visibility: hidden !important; }`,
      ].join('\n')}
    </style>
  )
}

export function CoucheMiseEnPlace({
  etape,
  restantes,
  suivant,
  animations,
}: {
  etape: EtapeMiseEnPlace | undefined
  restantes: number
  suivant: () => void
  /** Animations permises (réglage du joueur, hors mode sobre). */
  animations: boolean
}) {
  const cadre = useRef<HTMLDivElement>(null)
  const [enVol, setEnVol] = useState(false)

  const continuer = useCallback(() => {
    if (!etape || enVol) return
    const poser = () => {
      setEnVol(false)
      // La place se remplit (pointillés retirés, jeton mis à jour), puis la suivante.
      suivant()
      marquer(etape.carteId, animations)
    }
    if (!animations) {
      poser()
      return
    }
    setEnVol(true)
    glisser(cadre.current, etape.carteId, poser)
  }, [etape, enVol, animations, suivant])

  useEffect(() => {
    if (!etape) return
    const touche = (ev: KeyboardEvent) => {
      if (ev.key !== ' ' && ev.key !== 'Enter') return
      if (ev.ctrlKey || ev.metaKey || ev.altKey) return
      ev.preventDefault()
      ev.stopImmediatePropagation()
      continuer()
    }
    window.addEventListener('keydown', touche, true)
    return () => window.removeEventListener('keydown', touche, true)
  }, [etape, continuer])

  if (!etape) return null
  const src = scanUrl(etape.picId)
  const detail = etape.detail
  let ligne: string | null = null
  if (detail?.cle === 'héros') ligne = `${t('Engagé avec')} ${detail.valeur}`
  else if (detail?.cle === 'dégâts') ligne = `${detail.valeur} ${t(Number(detail.valeur) > 1 ? 'dégâts' : 'dégât')}`
  else if (detail?.cle === 'menace') ligne = `+${detail.valeur} ${t('menace')}`
  else if (detail?.cle === 'menace de départ') ligne = `${t('Menace de départ')} : ${detail.valeur}`

  return (
    <div className={`mep-couche${animations ? ' est-anime' : ''}${enVol ? ' est-en-vol' : ''}`} role="dialog" aria-modal="true" aria-label={t('Mise en place')}>
      <div className="mep-contenu" key={etape.cle}>
        <p className="mep-titre">{t('Mise en place')}</p>
        <div ref={cadre} className={`mep-cadre${etape.paysage ? ' est-paysage' : ''}`}>
          <img src={src} alt={etape.legende} />
          <TraductionSurCarte
            codeCarte={etape.codeCarte}
            imageUrl={src}
            traits={etape.traits}
            type={typeDeBoite(etape.type)}
            paysage={etape.paysage}
          />
        </div>
        <p className="mep-legende">{t(etape.legende)}</p>
        {ligne ? <p className="mep-detail">{ligne}</p> : null}
        <button type="button" className="mep-continuer" onClick={continuer} autoFocus>
          {t('Continuer')}
          {restantes > 1 ? <span className="mep-reste"> · {restantes - 1}</span> : null}
        </button>
      </div>
    </div>
  )
}
