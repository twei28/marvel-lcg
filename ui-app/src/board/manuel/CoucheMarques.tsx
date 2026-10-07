// Ce que montrent les marques du mode manuel (marques.ts) : la carte ciblee
// porte un repere a la couleur du joueur qui la cible, la carte surlignee un
// cadre de couleur, et une fleche relie deux cartes.
//
// ⚠ DES ATTRIBUTS, PAS DES CLASSES. React reecrit le `className` d'une carte des
// que son etat change (constat du 07/10/2026 sur la surbrillance de la
// relecture) ; il ne touche pas aux attributs `data-` qu'il ne gere pas. Ils
// sont reposes a chaque lecture, au cas ou la carte a change de noeud.
import { useEffect, useState } from 'react'
import { COULEURS_JOUEURS } from '../CoucheCurseurs'
import type { Marques } from './marques'
import './marques.css'

const ATTR_CIBLE = 'data-ciblee'
const ATTR_SURLIGNAGE = 'data-surlignage'

function cartesDe(id: string): HTMLElement[] {
  return [...document.querySelectorAll<HTMLElement>(`.plateau-scene .scan-card[data-card-id="${CSS.escape(id)}"]`)]
}

export function poserLesMarques(marques: Marques): void {
  const ciblees = new Set<Element>()
  for (const [id, siege] of Object.entries(marques.cibles)) {
    for (const carte of cartesDe(id)) {
      carte.setAttribute(ATTR_CIBLE, String(siege))
      carte.style.setProperty('--couleur-cible', COULEURS_JOUEURS[siege % COULEURS_JOUEURS.length])
      ciblees.add(carte)
    }
  }
  for (const carte of document.querySelectorAll<HTMLElement>(`[${ATTR_CIBLE}]`)) {
    if (!ciblees.has(carte)) carte.removeAttribute(ATTR_CIBLE)
  }
  const surlignees = new Set<Element>()
  for (const [id, couleur] of Object.entries(marques.surlignages)) {
    for (const carte of cartesDe(id)) {
      carte.setAttribute(ATTR_SURLIGNAGE, couleur)
      surlignees.add(carte)
    }
  }
  for (const carte of document.querySelectorAll(`[${ATTR_SURLIGNAGE}]`)) {
    if (!surlignees.has(carte)) carte.removeAttribute(ATTR_SURLIGNAGE)
  }
}

type Trait = { cle: string; x1: number; y1: number; x2: number; y2: number; couleur: string }

function centre(id: number): { x: number; y: number } | undefined {
  const r = cartesDe(String(id))[0]?.getBoundingClientRect()
  return r && r.width > 0 ? { x: r.left + r.width / 2, y: r.top + r.height / 2 } : undefined
}

export function CoucheMarques({ marques }: { marques: Marques }) {
  const [traits, setTraits] = useState<Trait[]>([])

  useEffect(() => {
    poserLesMarques(marques)
  }, [marques])
  useEffect(() => () => poserLesMarques({ cibles: {}, fleches: [], surlignages: {} }), [])

  // Les fleches suivent leurs cartes : remesurees a chaque image tant qu'il y en a.
  useEffect(() => {
    if (marques.fleches.length === 0) {
      setTraits([])
      return
    }
    let image = 0
    let precedent = ''
    const mesurer = () => {
      const neufs: Trait[] = []
      for (const f of marques.fleches) {
        const de = centre(f.de)
        const a = centre(f.a)
        if (de && a) {
          neufs.push({ cle: `${f.de}-${f.a}`, x1: de.x, y1: de.y, x2: a.x, y2: a.y, couleur: COULEURS_JOUEURS[f.p % COULEURS_JOUEURS.length] })
        }
      }
      const empreinte = JSON.stringify(neufs)
      if (empreinte !== precedent) {
        precedent = empreinte
        setTraits(neufs)
      }
      image = window.requestAnimationFrame(mesurer)
    }
    mesurer()
    return () => window.cancelAnimationFrame(image)
  }, [marques.fleches])

  if (traits.length === 0) return null
  return (
    <svg className="couche-marques" aria-hidden="true" width="100%" height="100%">
      <defs>
        {traits.map((trait) => (
          <marker
            key={trait.cle}
            id={`marque-pointe-${trait.cle}`}
            viewBox="0 0 10 10"
            refX="8"
            refY="5"
            markerWidth="5"
            markerHeight="5"
            orient="auto"
          >
            <path d="M0,0 L10,5 L0,10 z" fill={trait.couleur} />
          </marker>
        ))}
      </defs>
      {traits.map((trait) => (
        <line
          key={trait.cle}
          x1={trait.x1}
          y1={trait.y1}
          x2={trait.x2}
          y2={trait.y2}
          stroke={trait.couleur}
          markerEnd={`url(#marque-pointe-${trait.cle})`}
        />
      ))}
    </svg>
  )
}
