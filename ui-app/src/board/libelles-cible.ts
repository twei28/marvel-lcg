// Les libellés de l'étape « choisir les cibles ».
//
// Isolés du hook d'interaction parce qu'ils portent une subtilité qui a déjà
// coûté un soin de 4 PV ramené à 1 : certaines actions se RÉPARTISSENT.
//
// Le moteur exprime cela par des DOUBLONS dans `all_legal_targets`. Exemple
// vérifié sur 43006 Regenerative Longevity (« Heal a total of 4 damage from
// your identity and Honey Badger »), X-23 à 5 dégâts et Honey Badger à 1 :
//
//     target_num_range : [1, 4]
//     all_legal_targets: [1, 1, 1, 1, 9]   → X-23 x4, Honey Badger x1
//
// Un clic = une attribution. Il faut donc cliquer QUATRE fois sur X-23 pour
// la soigner de 4. L'ancien libellé annonçait « 1/1 requise(s) · 2
// possible(s) » : il montrait le minimum, comptait les cartes distinctes, et
// « Confirmer » s'allumait dès le premier clic. Le geste naturel soignait 1 PV.

import { t } from './langue'

export type LibellesCible = {
  titre: string
  detail: string
  /** Ligne d'aide, seulement quand une même carte est cliquable plusieurs fois. */
  indice?: string
}

export type EtatCible = {
  /** Attributions déjà posées (doublons compris). */
  choisies: number
  minimum: number
  maximum: number
  /** Cartes DISTINCTES désignables. */
  cartesCiblables: number
  /** Vrai dès qu'une carte accepte plus d'une attribution. */
  repetable: boolean
  mulligan?: boolean
}

export function libellesCible(etat: EtatCible): LibellesCible {
  const { choisies, minimum, maximum, cartesCiblables, repetable } = etat

  // Le mulligan est le premier écran de la partie, et « mulligan » ne veut rien
  // dire pour un débutant : le détail dit ce que fait le bouton et rappelle
  // qu'on a le droit de ne rien défausser. Le mode Découverte s'appuie dessus
  // (première leçon, lecons.ts).
  if (etat.mulligan) {
    return {
      titre: t('Choisir les cartes du mulligan'),
      detail: `${choisies} ${t('à défausser puis repiocher · tu peux n’en choisir aucune')}`,
    }
  }

  const titre =
    maximum > 1
      ? `${t('Choisir jusqu’à')} ${maximum} ${t('cibles')}`
      : cartesCiblables === 1
        ? t('Choisir la seule cible')
        : t('Choisir la cible')

  // Trois cas, du plus permissif au plus contraint.
  const detail =
    minimum === 0
      ? `${choisies}/${maximum} ${t('sélectionnée(s) · nombre au choix')}`
      : maximum > minimum
        ? `${choisies}/${maximum} ${t('attribuée(s)')} · ${minimum} ${t('minimum')} · ` +
          `${cartesCiblables} ${t('carte(s) ciblable(s)')}`
        : `${choisies}/${minimum} ${t('requise(s)')} · ${cartesCiblables} ${t('possible(s)')}`

  const indice = repetable
    ? t(
        'Une même carte peut être choisie plusieurs fois (1 clic = 1 attribution, ou « +N » pour tout lui donner d’un coup)'
      )
    : undefined

  return { titre, detail, indice }
}
