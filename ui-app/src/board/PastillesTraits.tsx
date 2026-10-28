// Les pastilles de traits d'un heros : sur la carte du plateau (posees en bas, sur le scan) et sous la carte agrandie.
import type { ScanCardProps } from '../components/ScanCard'
import { langueActuelle, t } from './langue'
import { useModeTraits } from './reglages-affichage-cartes'
import { pastillesDeTraits, pastillesVisibles, type PastilleTrait } from './traits-heros'

/** Seul le heros (ou son alter ego) porte des pastilles : c'est SON etat que le joueur veut lire. */
export function porteDesPastilles(carte: Pick<ScanCardProps, 'kind'>): boolean {
  return carte.kind === 'hero' || carte.kind === 'alter-ego'
}

export function pastillesDeLaCarte(carte: ScanCardProps, mode: Parameters<typeof pastillesVisibles>[1]): PastilleTrait[] {
  if (!porteDesPastilles(carte)) return []
  return pastillesVisibles(pastillesDeTraits(carte.traits, carte.traitsActuels, langueActuelle()), mode)
}

function titreDe(p: PastilleTrait): string {
  if (p.etat === 'gagne') return `${t('Trait gagné')} : ${p.texte}`
  if (p.etat === 'perdu') return `${t('Trait perdu')} : ${p.texte}`
  return `${t('Trait imprimé')} : ${p.texte}`
}

/**
 * `posee` : en bas du scan, sur le plateau. `surGrande` : en bas de la grande carte ouverte (telephone). Sinon : une rangee sous la carte (apercu agrandi).
 * Ne rend rien quand le reglage est sur « Aucun » ou qu'il n'y a rien a montrer.
 */
export function PastillesTraits({ carte, posee = false, surGrande = false }: { carte: ScanCardProps; posee?: boolean; surGrande?: boolean }) {
  const mode = useModeTraits()
  const pastilles = pastillesDeLaCarte(carte, mode)
  if (pastilles.length === 0) return null
  return (
    <div className={`pastilles-traits${posee ? ' est-posee' : ''}${surGrande ? ' est-sur-grande' : ''}`} aria-label={t('Traits')}>
      {pastilles.map((p) => (
        <span key={p.cle} className={`pastille-trait est-${p.etat}`} title={titreDe(p)}>
          {p.etat === 'gagne' ? '+ ' : ''}
          {p.texte}
        </span>
      ))}
    </div>
  )
}
