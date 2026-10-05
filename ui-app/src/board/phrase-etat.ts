// phrase-etat.ts — la consigne et la phrase d'état de l'assistant (design essai).
//
// Le panneau dit trois choses, dans cet ordre : QUOI (la carte, en petit),
// CE QU'ON TE DEMANDE (la consigne, en gros : « Payer 1 pour jouer »), et OÙ
// ON EN EST (« Il manque 1 ressource »). Le compte payé / dû est porté par
// les pastilles, la phrase ne le répète pas. Aucun nom de carte : les cartes
// payables brillent déjà dans la main (retour de l'utilisateur, 11/09/2026).

import type { AssistantInteraction } from './interaction'
import { langueActuelle, t } from './langue'

/** Les lettres du moteur (game/element/resources.py), dites en français. */
const NOM_TYPE_FR: Record<string, string> = {
  R: 'physique',
  B: 'mentale',
  Y: 'énergie',
  G: 'joker',
  L: 'éclair',
}

/** La consigne, en gros : ce que le moteur attend du joueur. */
export function consigne(assistant: AssistantInteraction, nomAction: string): string {
  if (assistant.etape !== 'payment') return assistant.titre
  if (assistant.coutRequis === undefined || assistant.coutRequis <= 0) return t('Payer le coût')
  return `${t('Payer')} ${assistant.coutRequis} ${t('pour')} ${nomAction.toLocaleLowerCase()}`
}

/** La ligne sous la consigne : où on en est. */
export function phraseEtat(assistant: AssistantInteraction, prete: boolean): string {
  if (assistant.etape === 'payment') {
    const types = Object.entries(assistant.typesManquants ?? {})
    if (types.length > 0) {
      const liste = types
        .map(([type, nombre]) => `${nombre} ${t(NOM_TYPE_FR[type] ?? type)}`)
        .join(` ${t('et')} `)
      return `${t('Il manque')} ${liste}`
    }
    if (assistant.coutRequis !== undefined) {
      const manque = Math.max(0, assistant.coutRequis - assistant.coutPaye)
      if (manque === 0) return t('Coût couvert')
      return `${t('Il manque')} ${manque} ${manque > 1 ? t('ressources') : t('ressource')}`
    }
    return assistant.detail ?? ''
  }
  if (assistant.etape === 'confirm' && prete) return t('Tout est prêt')
  return assistant.detail ?? ''
}

/** La raison d'un ciblage « pas prêt », née en anglais dans `reponsePrete`, dite en français. */
export function raisonDite(raison: string): string {
  if (langueActuelle() === 'en') return raison
  const cibles = (n: number) => `${n} ${n > 1 ? 'cibles' : 'cible'}`
  const encore = /^Choose (\d+) more target\(s\)$/.exec(raison)
  if (encore) return `Choisis encore ${cibles(Number(encore[1]))}`
  const enTrop = /^Remove (\d+) target\(s\)$/.exec(raison)
  if (enTrop) return `Retire ${cibles(Number(enTrop[1]))}`
  return raison
}
