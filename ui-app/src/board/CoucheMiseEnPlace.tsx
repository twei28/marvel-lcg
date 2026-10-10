// La mise en place montrée carte par carte (voir mise-en-place-pas-a-pas.ts).
//
// Chaque carte qui arrive en jeu s'affiche en grand au centre, plateau
// assombri, avec sa légende ; « Continuer » (ou Espace) la fait glisser à sa
// place, où un contour arrondi la repère brièvement, une seule fois.

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

  const suivant = useCallback(() => setFile((f) => f.slice(1)), [])
  return { etape: file[0] as EtapeMiseEnPlace | undefined, restantes: file.length, suivant }
}

function marquer(carteId: number, animations: boolean) {
  const cible = document.querySelector<HTMLElement>(`.scan-card[data-card-id="${carteId}"]`)
  if (!cible) return
  cible.classList.add('mep-repere')
  if (animations) cible.classList.add('mep-repere-anime')
  window.setTimeout(() => cible.classList.remove('mep-repere', 'mep-repere-anime'), 1000)
}

function glisser(depart: HTMLElement | null, carteId: number) {
  const cible = document.querySelector<HTMLElement>(`.scan-card[data-card-id="${carteId}"]`)
  if (!depart || !cible || typeof depart.animate !== 'function') return
  const a = depart.getBoundingClientRect()
  const b = cible.getBoundingClientRect()
  if (!a.width || !b.width) return
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
    { duration: 320, easing: 'ease-in' }
  )
  anim.onfinish = () => fantome.remove()
  anim.oncancel = () => fantome.remove()
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

  const continuer = useCallback(() => {
    if (!etape) return
    if (animations) glisser(cadre.current, etape.carteId)
    marquer(etape.carteId, animations)
    suivant()
  }, [etape, animations, suivant])

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
    <div className={`mep-couche${animations ? ' est-anime' : ''}`} role="dialog" aria-modal="true" aria-label={t('Mise en place')}>
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
