// Les cartes POSÉES SOUS une autre (une pile) ne sont pas des améliorations.
//
// State of Flow (Shang-Chi) : « After you play an ATTACK event, place it faceup on top here, forming a pile ». Corsair et Havok
// glissent aussi des cartes dessous. Pour le moteur, ces cartes sont rattachées à leur porteuse (`bind_object_id`) comme une
// amélioration, et le plateau les dessinait pareil : le joueur croyait que son événement était resté en jeu (rapport du
// 26/10/2026, partie réelle sur téléphone). Un événement ou une ressource ne s'attache jamais pour de vrai : s'il pend à une carte,
// c'est qu'il est empilé dessous.
import type { ScanCardProps } from '../components/ScanCard'
import { t } from './langue'

/** Une carte attachée qui est en réalité posée sous son porteur : un événement ou une ressource. */
export function estEmpilee(attachee: Pick<ScanCardProps, 'kind'>): boolean {
  return attachee.kind === 'event' || attachee.kind === 'resource'
}

export function compterEmpilees(attachees: readonly Pick<ScanCardProps, 'kind'>[]): number {
  return attachees.filter(estEmpilee).length
}

/** Texte de la pastille et de son aria-label : « Pile de cartes : 3 ». */
export function libelleEmpilees(nombre: number): string {
  return `${t('Pile de cartes')} : ${nombre}`
}
