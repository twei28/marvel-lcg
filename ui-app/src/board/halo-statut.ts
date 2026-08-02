// Halo de statut : quand une carte gagne (ou perd) solide/etourdi/confus, un
// halo colore pulse brievement sur elle.
//
// Transposition de animation_gain_status du client original : les evenements
// AfterUnitGainStatus / AfterUnitLostStatus citent la carte concernee dans
// active_card_ids[1]. L'original ne savait pas QUEL statut etait gagne (halo
// generique) ; ici on lit le prompt du rendu, qui nomme la carte de statut,
// pour colorer le halo (or = tough, orange = stunned, violet = confused,
// memes teintes que card-effects.css).
//
// Application imperative de classes CSS, comme CoucheAnimations masque les
// vraies cartes : transitoire, sans toucher au rendu React.

import { useEffect } from 'react'
import type { World } from './world'

const DUREE = 1000

let dernierRender = -1

function couleurDepuisPrompt(prompt: string): string {
  const p = prompt.toLowerCase()
  if (p.includes('tough')) return 'tough'
  if (p.includes('stun')) return 'stun'
  if (p.includes('confus')) return 'confuse'
  return 'generique'
}

export function useHaloStatut(monde: World | undefined, actif: boolean) {
  useEffect(() => {
    if (!monde || monde.render_id === dernierRender) return
    dernierRender = monde.render_id

    if (!actif) return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const evenement = monde.event_name ?? ''
    if (evenement !== 'AfterUnitGainStatus' && evenement !== 'AfterUnitLostStatus') return

    const ids = monde.active_card_ids ?? []
    // [0] = la carte de statut, [1] = l'unite qui la gagne/perd.
    const uniteId = ids[1]
    if (uniteId === undefined) return
    const el = document.querySelector<HTMLElement>(
      `.plateau-scene .scan-card[data-card-id="${uniteId}"]`
    )
    if (!el) return

    const perte = evenement === 'AfterUnitLostStatus'
    const teinte = perte ? 'perte' : couleurDepuisPrompt(`${monde.prompt ?? ''} ${monde.prompt_last_text ?? ''}`)
    const classes = ['halo-statut', `halo-${teinte}`]
    el.classList.add(...classes)
    window.setTimeout(() => {
      el.classList.remove(...classes)
    }, DUREE)
  }, [monde, monde?.render_id, actif])
}
