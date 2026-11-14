import type { WorldCard } from './world'

/** Ces améliorations commencent face cachée ; leur face connue n'est pas leur forme active. */
export function estFormeEnergieSpectrum(carte: Pick<WorldCard, 'card_id'>): boolean {
  return carte.card_id === '21002' || carte.card_id === '21003' || carte.card_id === '21004'
}
