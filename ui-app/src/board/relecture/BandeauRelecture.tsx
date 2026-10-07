// Le bandeau de la relecture : qui fait quoi, avec quoi il a paye, ce que ca
// a fait. Et, sur la table, la carte jouee en surbrillance, la fleche de
// l'attaque et le chiffre des degats qui s'envole au-dessus de la cible.
import { useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react'
import { createPortal } from 'react-dom'
import { t } from '../langue'
import { COULEURS_JOUEURS } from '../CoucheCurseurs'
import { actionsDe, degatsParRendu, type Action, type Degat } from './actions'
import type { Relecture } from './fichier'
import type { Lecteur } from './lecteur'

/** Combien de rendus le bandeau garde une action a l'ecran. */
const PERSISTANCE = 6
const DUREE_EFFET_MS = 1400

const couleur = (siege: number | undefined) =>
  siege === undefined ? '#e8edf2' : COULEURS_JOUEURS[siege % COULEURS_JOUEURS.length]

function nomHeros(relecture: Relecture, siege: number): string {
  return (
    relecture.entete.joueurs[siege]?.heros ||
    relecture.trames[0]?.monde.players?.[siege]?.area_hero?.[0]?.name?.replace(/^\W*/, '') ||
    ''
  )
}

export function phrasesDe(action: Action, relecture: Relecture): string[] {
  const lignes: string[] = []
  if (action.genre === 'joue' && action.carte) {
    const qui =
      action.siege === undefined
        ? t('Un joueur')
        : t('Joueur %1 (%2)').replace('%1', String(action.siege + 1)).replace('%2', nomHeros(relecture, action.siege))
    lignes.push(t('%1 joue %2').replace('%1', qui).replace('%2', action.carte.nom))
    if (action.paiement.length > 0) {
      const cartes = action.paiement
        .map((p) => (p.ressources.length > 0 ? `${p.nom} (${p.ressources.map((r) => t(r)).join(' + ')})` : p.nom))
        .join(', ')
      lignes.push(t('Payé avec : %1').replace('%1', cartes))
    }
  } else if (action.acteur && action.cible) {
    const modele =
      action.genre === 'attaque' ? '%1 attaque %2' : action.genre === 'contre' ? '%1 contre sur %2' : '%1 pose de la menace sur %2'
    lignes.push(t(modele).replace('%1', action.acteur.nom).replace('%2', action.cible.nom))
  }
  for (const degat of action.degats) {
    lignes.push(t('%1 dégâts à %2').replace('%1', String(degat.montant)).replace('%2', degat.nom))
  }
  return lignes
}

function centre(id: number): { x: number; y: number } | undefined {
  const carte = document.querySelector<HTMLElement>(`.scan-card[data-card-id="${id}"]`)
  const r = carte?.getBoundingClientRect()
  if (!r || r.width === 0) return undefined
  return { x: r.left + r.width / 2, y: r.top + r.height / 2 }
}

type Effet = { cle: number; fleche?: { de: { x: number; y: number }; a: { x: number; y: number }; genre: string }; degats: (Degat & { x: number; y: number })[] }

export function BandeauRelecture({ lecteur, relecture }: { lecteur: Lecteur; relecture: Relecture }) {
  const { index } = useSyncExternalStore(
    (rappel) => lecteur.ecouterControle(rappel),
    () => lecteur.lireControle()
  )
  const actions = useMemo(() => actionsDe(relecture), [relecture])
  const degats = useMemo(() => degatsParRendu(relecture), [relecture])
  const [effet, setEffet] = useState<Effet>()
  const [aAllumer, setAAllumer] = useState<{ id: number; cle: number }>()
  const indexPrecedent = useRef(index)

  let courante: Action | undefined
  for (const action of actions) {
    if (action.index > index) break
    if (index - action.index <= PERSISTANCE) courante = action
  }

  // Les effets sur la table ne se jouent qu'en avancant d'UN rendu : un saut
  // pose l'etat sans rejouer ce qui s'est passe entre-temps.
  useEffect(() => {
    const avance = index === indexPrecedent.current + 1
    indexPrecedent.current = index
    // Le nettoyage du rendu precedent a coupe son minuteur : sans cette remise a
    // zero, sa fleche restait a l'ecran pour de bon apres un saut.
    if (!avance) {
      setEffet(undefined)
      setAAllumer(undefined)
      return
    }
    const action = actions.find((a) => a.index === index)
    if (action?.carte) setAAllumer({ id: action.carte.id, cle: index })
    let fleche: Effet['fleche']
    if (action?.acteur && action.cible && action.acteur.id !== action.cible.id) {
      const de = centre(action.acteur.id)
      const a = centre(action.cible.id)
      if (de && a) fleche = { de, a, genre: action.genre }
    }
    const chiffres = (degats.get(index) ?? []).flatMap((d) => {
      const ou = centre(d.id)
      return ou ? [{ ...d, ...ou }] : []
    })
    setEffet(fleche || chiffres.length > 0 ? { cle: index, fleche, degats: chiffres } : undefined)
    const minuteur = window.setTimeout(() => setEffet((e) => (e?.cle === index ? undefined : e)), DUREE_EFFET_MS)
    return () => window.clearTimeout(minuteur)
  }, [index, actions, degats])

  // LA CARTE JOUEE S'ALLUME QUAND ELLE PARAIT. Au moment du coup elle est dans
  // la zone de resolution, que la table ne dessine pas : on l'attend (3 s au
  // plus), puis elle reste allumee le temps de l'effet, quels que soient les
  // rendus qui passent entre-temps.
  useEffect(() => {
    if (!aAllumer) return
    let allumee: Element | null = null
    let eteindre: number | undefined
    const debut = performance.now()
    const guetteur = window.setInterval(() => {
      allumee = document.querySelector(`.scan-card[data-card-id="${aAllumer.id}"]`)
      if (allumee) {
        window.clearInterval(guetteur)
        allumee.classList.add('relecture-surbrillance')
        eteindre = window.setTimeout(() => allumee?.classList.remove('relecture-surbrillance'), DUREE_EFFET_MS)
      } else if (performance.now() - debut > 3000) {
        window.clearInterval(guetteur)
      }
    }, 100)
    return () => {
      window.clearInterval(guetteur)
      window.clearTimeout(eteindre)
      allumee?.classList.remove('relecture-surbrillance')
    }
  }, [aAllumer])

  const lignes = courante ? phrasesDe(courante, relecture) : []
  return (
    <>
      {lignes.length > 0 ? (
        <div className="relecture-bandeau" role="status" style={{ borderColor: couleur(courante?.siege) }}>
          <strong style={{ color: couleur(courante?.siege) }}>{lignes[0]}</strong>
          {lignes.slice(1).map((ligne) => (
            <span key={ligne}>{ligne}</span>
          ))}
        </div>
      ) : null}
      {effet
        ? createPortal(
            <div className="relecture-effets" aria-hidden="true">
              {effet.fleche ? (
                <svg className={`relecture-fleche est-${effet.fleche.genre}`} width="100%" height="100%">
                  <defs>
                    <marker id="relecture-pointe" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">
                      <path d="M0,0 L10,5 L0,10 z" />
                    </marker>
                  </defs>
                  <line
                    x1={effet.fleche.de.x}
                    y1={effet.fleche.de.y}
                    x2={effet.fleche.a.x}
                    y2={effet.fleche.a.y}
                    markerEnd="url(#relecture-pointe)"
                  />
                </svg>
              ) : null}
              {effet.degats.map((d) => (
                <span key={d.id} className="relecture-degats" style={{ left: d.x, top: d.y }}>
                  -{d.montant}
                </span>
              ))}
            </div>,
            document.body
          )
        : null}
    </>
  )
}
