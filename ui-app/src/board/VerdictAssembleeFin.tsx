/**
 * Le VERDICT DE L'ASSEMBLEE sur l'ecran de fin de partie (Kingsfall multi-tables, 22/10/2026). Avant, seul l'onglet « Assemblee » le disait : un groupe
 * dont la table finit en premier ne savait pas ce que devenait l'assemblee. Rien ne s'affiche hors assemblee. Tant que d'autres groupes jouent,
 * l'ecran le dit et se met a jour tout seul (relecture de l'etat commun, `useAssembleeEnDirect`).
 */
import { t } from './langue'
import { groupesEnCours, verdictDeLAssemblee } from './assemblee-etat'
import { useAssembleeEnDirect } from './use-assemblee-en-direct'
import type { World } from './world'
import './VoletAssemblee.css'

export function VerdictAssembleeFin({ monde, siege }: { monde: World | undefined; siege: number }) {
  const assemblee = useAssembleeEnDirect(monde, siege)
  if (!assemblee) return null
  const verdict = verdictDeLAssemblee(assemblee)
  const enCours = groupesEnCours(assemblee)
  if (verdict === 'en_attente') {
    return (
      <p className="assemblee-attente" role="status">
        {t('Ta table a fini. L’assemblée attend les autres groupes.')}{' '}
        {enCours > 1 ? `${enCours} ${t('groupes jouent encore.')}` : enCours === 1 ? t('Un groupe joue encore.') : ''}
      </p>
    )
  }
  return (
    <p className={`assemblee-verdict est-${verdict}`} role="status">
      {verdict === 'gagnee' ? t('L’assemblée gagne !') : t('L’assemblée perd.')}
    </p>
  )
}
