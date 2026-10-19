import type { EtapeDeroule } from './deroule-phase'
import { t } from './langue'

/** Calcul connu à la résolution, sans transformer une prévention ou Tenace en fausse égalité. */
export function calculCoupTable(etape: EtapeDeroule): string | undefined {
  if (etape.etat !== 'resolu' || (etape.titre !== 'attaque' && etape.titre !== 'manigance') || etape.base === undefined || etape.montant === undefined) return undefined
  const attaque = etape.titre === 'attaque'
  const imprimee = etape.baseImprimee ?? etape.base
  const termes = [`${t(attaque ? 'ATQ' : 'MEN')} ${imprimee}`]
  const bonus = etape.base - imprimee
  if (bonus) termes.push(`${bonus > 0 ? '+' : '−'} ${Math.abs(bonus)} ${t('Bonus')}`)
  const boost = etape.boosts.reduce((s, b) => s + b.apport, 0)
  if (etape.boosts.length) termes.push(`+ ${t('Boost')} ${boost}${etape.boosts.some((b) => b.etoile) ? ' ★' : ''}`)
  const defense = attaque ? etape.defense ?? 0 : 0
  if (defense > 0) termes.push(`− ${t('DÉF')} ${defense}`)
  let reduit = 0
  for (const reduction of etape.reductions ?? []) {
    reduit += reduction.valeur
    termes.push(`− ${reduction.valeur} ${reduction.source}`)
  }
  const attendu = Math.max(0, etape.base + boost - defense - reduit)
  const unite = attaque ? t(etape.montant === 1 ? 'dégât' : 'dégâts') : t(etape.montant === 1 ? 'menace' : 'menaces')
  return attendu === etape.montant
    ? `${termes.join(' ')} = ${etape.montant} ${unite}`
    : `${termes.join(' ')} = ${attendu} → ${etape.montant} ${unite}`
}
