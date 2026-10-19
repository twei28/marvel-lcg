// LES REGLES CACHEES (19/10/2026, T11) : une petite ligne discrete sous la phrase du bandeau quand une regle joue sans que rien
// ne la montre. Elle disparait avec le bandeau. Texte francais, dico-en pour l'anglais.
import type { EtapeDeroule } from './deroule-phase'
import { t } from './langue'

export function reglesCachees(etape: EtapeDeroule, contexte: { accelerationEnJeu?: number } = {}): string[] {
  const lignes: string[] = []
  // Le fait du moteur donne l'acceleration ; avant qu'il n'arrive (l'etape vient du journal), on la lit sur les icones des
  // manigances en jeu.
  const acceleration = etape.acceleration ?? contexte.accelerationEnJeu ?? 0
  if (etape.titre === 'menace' && acceleration > 0) {
    const n = acceleration
    lignes.push(t(n > 1 ? 'Accélération : +%1 menaces' : 'Accélération : +%1 menace').replace('%1', String(n)))
  }
  const activation = etape.titre === 'attaque' || etape.titre === 'manigance'
  if (activation && etape.etat === 'resolu') {
    // Le ★ d'un boost : l'effet de la carte s'applique en plus des icones.
    for (const boost of etape.boosts) if (boost.etoile) lignes.push(t('★ %1 : effet de la carte').replace('%1', boost.nom))
    if (etape.motsCles?.percant) lignes.push(t('Perforant : le Tenace est retiré'))
    else if (etape.motsCles?.robuste) lignes.push(t('Tenace : défaussé à la place des dégâts'))
  }
  if (etape.titre === 'attaque' && etape.desoriente && (etape.etat === 'annonce' || etape.etat === 'resolu')) {
    lignes.push(t('Désorienté : n’empêche pas d’attaquer'))
  }
  return lignes
}
