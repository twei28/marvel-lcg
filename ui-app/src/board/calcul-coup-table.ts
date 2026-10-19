import type { EtapeDeroule } from './deroule-phase'
import { t } from './langue'

/** Calcul connu à la résolution, sans transformer une prévention ou Tenace en fausse égalité. */
export function calculCoupTable(etape: EtapeDeroule): string | undefined {
  if (etape.etat !== 'resolu' || (etape.titre !== 'attaque' && etape.titre !== 'manigance') || etape.base === undefined || etape.montant === undefined) return undefined
  const attaque = etape.titre === 'attaque'
  const imprimee = etape.baseImprimee ?? etape.base
  const termes = [`${t(attaque ? 'ATQ' : 'MEN')} ${imprimee}`]
  const bonus = etape.base - imprimee
  // UNE LIGNE PAR SOURCE quand le jeu connait l'origine (19/10/2026) : « ATQ 2 + 2 Fusil Laser + Boost 3 = 7 ». Le moteur ne
  // nomme que les bonus d'EFFETS (les icones de boost ont leur terme « Boost »). Ce que les sources ne couvrent pas reste « Bonus ».
  const parSource = new Map<string, { nom: string; valeur: number }>()
  for (const b of etape.bonus ?? []) {
    const cle = `${b.source_id ?? ''}|${b.source}`
    const avant = parSource.get(cle)
    parSource.set(cle, { nom: b.source, valeur: (avant?.valeur ?? 0) + b.valeur })
  }
  let explique = 0
  for (const { nom, valeur } of parSource.values()) {
    if (!valeur) continue
    explique += valeur
    termes.push(`${valeur > 0 ? '+' : '−'} ${Math.abs(valeur)} ${nom}`)
  }
  const reste = bonus - explique
  if (reste) termes.push(`${reste > 0 ? '+' : '−'} ${Math.abs(reste)} ${t('Bonus')}`)
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
