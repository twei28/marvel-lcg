// L'option « Ask » du moteur (player_setup.py, `register_ask_effect`, partie à
// 2 joueurs ou plus) : demander à un AUTRE joueur d'agir. Deux usages, un seul
// nom : pendant une attaque, défendre à la place du héros attaqué ; pendant ton
// tour, jouer une de ses Actions.
//
// ⚠ « Ask » N'EST PAS UN NOM DE CAPACITÉ. Traité comme tel, le bouton reprenait
// le nom imprimé sur la carte qui porte l'option, le héros attaqué : « I Can Do
// This All Day! » pour une demande de défense, et « Ne pas utiliser I Can Do
// This All Day! » pour le refus (capture du 21/10/2026, Captain America attaqué).
import type { Option } from './ask'
import { t } from './langue'

export const DEMANDER_A_UN_AUTRE = 'Ask'

export function estDemandeAUnAutre(option: Pick<Option, 'name'>): boolean {
  return option.name === DEMANDER_A_UN_AUTRE
}

function pendantUneAttaque(eventName: string | undefined): boolean {
  return /attack/i.test(eventName ?? '')
}

/** « Demander à Laura Kinney de défendre », ou « … d'agir » pendant son tour. */
export function libelleDemandeAUnAutre(
  option: Pick<Option, 'all_legal_targets'>,
  eventName: string | undefined,
  nomDe: (id: number) => string | undefined
): string {
  const aides = [...new Set(option.all_legal_targets ?? [])]
  const nom = aides.length === 1 ? nomDe(aides[0]!) : undefined
  if (pendantUneAttaque(eventName)) {
    return nom ? t('Demander à %1 de défendre').replace('%1', nom) : t('Demander à un autre joueur de défendre')
  }
  return nom ? t('Demander à %1 d’agir').replace('%1', nom) : t('Demander à un autre joueur d’agir')
}
