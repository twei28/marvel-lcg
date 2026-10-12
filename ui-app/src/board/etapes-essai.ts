// Les étapes que seule la refonte de la phase du méchant (essai) raconte à part.
//
// Décision 39 (.planning/todos/2026-10-12-phase-mechant-schema-et-questions.md) :
// la Riposte a SON écran, juste après l'attaque qu'elle suit, avec une flèche dans
// l'autre sens. Le moteur la publie sur le fait d'attaque (`riposte`, lot 5b) ;
// sans essai, rien ne change : cette fonction n'est appelée que par l'essai.
import type { EtapeDeroule } from './deroule-phase'

export function avecEtapesRiposte(etapes: EtapeDeroule[]): EtapeDeroule[] {
  if (!etapes.some((etape) => etape.riposte)) return etapes
  const suite: EtapeDeroule[] = []
  for (const etape of etapes) {
    suite.push(etape)
    const riposte = etape.riposte
    if (!riposte || etape.titre !== 'attaque' || etape.etat === 'annule') continue
    suite.push({
      cle: `${etape.cle}:riposte`,
      temps: etape.temps,
      titre: 'riposte',
      regle: 'regle:riposte',
      // La carte touchée riposte contre l'attaquant : les rôles s'inversent.
      carteId: etape.cibleId,
      cibleId: etape.carteId,
      auteurNom: etape.cibleNom,
      cibleNom: etape.auteurNom,
      montant: riposte.degats,
      restant: riposte.restant ?? undefined,
      etat: 'resolu',
      riposte,
      boosts: [],
      rangSbire: etape.rangSbire,
      totalSbires: etape.totalSbires,
    })
  }
  return suite
}
