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

/**
 * LOT 5c (décision 42) : la distribution de l'étape 3 en UN tableau, une ligne par
 * joueur avec la raison de chaque carte, à la place des étapes « X reçoit N cartes ».
 */
export function avecTableauDistribution(etapes: EtapeDeroule[]): EtapeDeroule[] {
  const distributions = etapes.filter((etape) => etape.temps === 'distribution' && etape.titre === 'distribution')
  if (distributions.length === 0) return etapes
  const premiere = distributions[0]
  const tableau: EtapeDeroule = {
    cle: `${premiere.cle}:tableau`,
    temps: 'distribution',
    titre: 'distribution-tableau',
    regle: 'regle:distribution',
    boosts: [],
    montant: distributions.reduce((somme, etape) => somme + (etape.montant ?? 1), 0),
    lignesDistribution: distributions.map((etape) => ({
      joueur: etape.joueur,
      nom: etape.auteurNom,
      cartes: etape.montant ?? 1,
      raisons: etape.raisonsCartes ?? [],
    })),
  }
  // 13/10/2026 (encadré ⑪) : en solo, UNE carte sans raison particulière n'a
  // pas d'écran ; on passe directement à sa révélation.
  const lignes = tableau.lignesDistribution ?? []
  const seule =
    lignes.length === 1 &&
    lignes[0].cartes === 1 &&
    lignes[0].raisons.every((r) => r.raison === 'base' && !r.source)
  const suite: EtapeDeroule[] = []
  for (const etape of etapes) {
    if (etape === premiere) {
      if (!seule) suite.push(tableau)
    } else if (!(etape.temps === 'distribution' && etape.titre === 'distribution')) suite.push(etape)
  }
  return suite
}

/** Un effet ★ qui s'applique APRÈS le retournement (« si cette activation… », « après cette activation… »). */
export function effetEtoileDiffere(texte: string | undefined): boolean {
  if (!texte) return false
  return /\b(if|after) this (activation|attack)\b/i.test(texte) || /\b(si|après) cette (activation|attaque)\b/i.test(texte)
}

/**
 * LOT 5c (décision 38) : l'effet ★ différé d'un boost a son écran à part, au moment
 * où il s'applique, juste après l'attaque (et sa Riposte). `texteEtoile` donne le
 * texte ★ du boost ; seule l'essai appelle cette fonction.
 */
export function avecEtapesEtoileDifferee(
  etapes: EtapeDeroule[],
  texteEtoile: ((carteId: number) => string | undefined) | undefined
): EtapeDeroule[] {
  if (!texteEtoile) return etapes
  const suite: EtapeDeroule[] = []
  let attente: EtapeDeroule[] = []
  const vider = () => {
    suite.push(...attente)
    attente = []
  }
  for (const etape of etapes) {
    // Les étapes d'effet différé se placent après l'attaque ET sa Riposte.
    if (attente.length > 0 && etape.titre !== 'riposte') vider()
    if ((etape.titre !== 'attaque' && etape.titre !== 'manigance') || etape.etat !== 'resolu') {
      suite.push(etape)
      continue
    }
    // 13/10/2026 (encadré ⑥) : un ★ « si cette attaque inflige des dégâts » sur une
    // attaque qui n'a rien infligé n'a pas d'écran : une ligne sur le résultat.
    const sansEffet: string[] = []
    for (const boost of etape.boosts) {
      if (!boost.etoile) continue
      const texte = texteEtoile(boost.cibleId)
      if (!effetEtoileDiffere(texte)) continue
      if (etape.titre === 'attaque' && (etape.montant ?? 0) === 0 && conditionDegats(texte)) {
        sansEffet.push(boost.nom)
        continue
      }
      attente.push({
        cle: `${etape.cle}:etoile:${boost.cle}`,
        temps: etape.temps,
        titre: 'etoile-differe',
        regle: 'regle:boost',
        carteId: boost.cibleId,
        auteurNom: boost.nom,
        cibleId: etape.cibleId,
        cibleNom: etape.cibleNom,
        montant: etape.montant,
        defenseurId: etape.defenseurId,
        etat: 'resolu',
        boosts: [],
        rangSbire: etape.rangSbire,
        totalSbires: etape.totalSbires,
      })
    }
    suite.push(sansEffet.length > 0 ? { ...etape, etoilesSansEffet: sansEffet } : etape)
  }
  vider()
  return suite
}

/** Le ★ ne joue que si l'attaque a infligé des dégâts (FR et EN). */
function conditionDegats(texte: string | undefined): boolean {
  if (!texte) return false
  return (
    /\bif this (attack|activation) deals damage\b/i.test(texte) ||
    /\bsi cette (attaque|activation) (vous )?(inflige|cause) des dégâts/i.test(texte)
  )
}

/** LOT 5c (décision 45) : un héros mis à terre a son écran dédié, juste après le coup. */
export function avecEcranElimination(etapes: EtapeDeroule[]): EtapeDeroule[] {
  if (!etapes.some((etape) => etape.defaite)) return etapes
  const suite: EtapeDeroule[] = []
  for (const etape of etapes) {
    suite.push(etape)
    if (!etape.defaite) continue
    suite.push({
      cle: `${etape.cle}:elimination`,
      temps: etape.temps,
      titre: 'elimination',
      regle: 'regle:elimination',
      carteId: etape.cibleAnnonceeId ?? etape.cibleId,
      cibleId: etape.cibleAnnonceeId ?? etape.cibleId,
      cibleNom: etape.cibleNom,
      joueur: etape.joueur,
      etat: 'resolu',
      boosts: [],
    })
  }
  return suite
}
