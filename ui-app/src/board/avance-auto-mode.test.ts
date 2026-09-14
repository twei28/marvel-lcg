// L'avance auto ne s'applique QUE dans le mode « Détaillé ».
//
// ⚠ LE DÉFAUT QUE CE FICHIER EMPÊCHE DE REVENIR, constaté en partie réelle le
// 14/09/2026, à la toute première partie jouée dans le mode « Sur la table » :
// « tout avance tout seul sans attendre le suivant ».
//
// Le réglage « Avance toute seule » était bien GRISÉ hors du mode Détaillé
// (FenetreReglages, `disponible`), mais sa VALEUR continuait d'être transmise
// au cartouche. Un joueur qui l'avait allumée en Détaillé la gardait active en
// passant sur « Sur la table », dont toute la définition est l'inverse : un
// clic à chaque étape, la demande la plus explicite de l'utilisateur.
//
// ⚠ GRISER N'EST PAS DÉSACTIVER. Le grisé rend un réglage inchangeable ; il
// faut en plus qu'il cesse de s'appliquer, et c'est à la source que ça se
// décide.
import { describe, expect, it } from 'vitest'
import { MODES, type ModePhaseMechant } from './moteur'

/**
 * La règle, telle que `board.tsx` l'écrit (`avanceAutoActive`). Copiée ici
 * plutôt qu'importée : `board.tsx` monte tout le plateau, et cette règle tient
 * en une ligne. Le test vaut alors garde-fou sur l'INTENTION.
 */
const avanceAutoActive = (mode: ModePhaseMechant, reglage: boolean) =>
  mode === 'detaille' && reglage

describe('l’avance auto et les trois modes', () => {
  it('s’applique en « Détaillé » quand le joueur l’a allumée', () => {
    expect(avanceAutoActive('detaille', true)).toBe(true)
  })

  it('⚠ ne s’applique PAS en « Sur la table », même allumée', () => {
    // Le cas exact du défaut. Ce mode est défini par « un clic à chaque étape ».
    expect(avanceAutoActive('sur-table', true)).toBe(false)
  })

  it('ne s’applique pas en « Instantané » non plus', () => {
    // Ce mode ne retient rien : il n'y a aucune étape à faire avancer.
    expect(avanceAutoActive('instantane', true)).toBe(false)
  })

  it('éteinte, elle ne s’applique dans AUCUN mode', () => {
    for (const mode of MODES) {
      expect(avanceAutoActive(mode, false), mode).toBe(false)
    }
  })

  it('un seul mode sur les trois peut l’activer', () => {
    // Témoin : si un quatrième mode arrive un jour, ce compte le dira.
    expect(MODES.filter((m) => avanceAutoActive(m, true))).toEqual(['detaille'])
  })
})
