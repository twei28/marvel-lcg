// Le plateau en PORTRAIT : une colonne, un seul ecran, aucun defilement.
//
// Spec : docs/superpowers/specs/2026-09-11-plateau-portrait-telephone-design.md
//
// Releve mesure sur play.marvelsimulator.com : leur page ne defile pas
// (scrollHeight == innerHeight), et cela ne tient que parce que la table n'est
// PAS faite de cartes jouables. Le vilain, le complot et les allies sont la
// vraie carte en petit, avec leurs chiffres en gros A COTE. Seule la main est
// en cartes qu'on lit a vue.
//
// Il accepte exactement les BoardProps du plateau PC, comme PlateauPaysage :
// c'est ce qui permet a board.tsx de choisir sans rien adapter.
import type { ScanCardProps } from '../../components/ScanCard'
import type { BoardProps } from '../Board'
import type { UniteAffichee } from '../zones'
import { t } from '../langue'
import { BandeauPortrait } from './BandeauPortrait'
import { BarreMenace } from './BarreMenace'
import { CarteAvecChiffres } from './CarteAvecChiffres'
import { CompteursPortrait } from './CompteursPortrait'
import { repartirEnBlocs } from './blocs-portrait'
import './portrait.css'

/**
 * La menace posee et son seuil d'une manigance.
 *
 * Pas dans `stats` : cette liste ne sert qu'aux PERSONNAGES (statsAffichees
 * dans card-model.ts se tait des qu'`isUnit(card)` est faux), donc une
 * manigance y arrive toujours vide. Le seul champ de ScanCardProps qui porte
 * encore les deux nombres est `schemeThreat`, deja forme par menaceAffichee()
 * en "pose/seuil" (ou juste "pose" quand aucun seuil imprime n'est connu,
 * cas des manigances annexes) : c'est de la qu'on les relit.
 */
function menaceDe(carte: ScanCardProps): { pose: number; total: number } {
  const [pose, total] = (carte.schemeThreat ?? '').split('/')
  return { pose: Number(pose) || 0, total: Number(total) || 0 }
}

/**
 * Le deck et la defausse de rencontre, en nombre de cartes.
 *
 * Reperes par leur CLE (posee par `piles('rencontre', ...)` dans zones.ts) et
 * non par leur nom affiche : le nom d'une pile est celui de sa carte du
 * dessus (« Rhino »...), jamais « Deck » ou « Défausse ».
 */
function comptesRencontre(unites: UniteAffichee[]): Array<{ valeur: number; libelle: string }> {
  const compte = (cle: string) => unites.find((unite) => unite.cle === cle)?.carte.pileCount ?? 0
  return [
    { valeur: compte('rencontre-encounter-deck'), libelle: t('Rencontre') },
    { valeur: compte('rencontre-encounter-discard'), libelle: t('Défausse') },
  ]
}

export function PlateauPortrait(props: BoardProps) {
  const blocs = repartirEnBlocs(props.plateau)
  const vilain = blocs.find((bloc) => bloc.cle === 'vilain')?.unites ?? []
  // Seule la manigance PRINCIPALE se joue ici (spec du 11/09/2026, §Decoupage) :
  // les annexes, elles, restent pour une tache suivante.
  const principal = blocs.find((bloc) => bloc.cle === 'complot')?.unites[0]
  const rencontre = blocs.find((bloc) => bloc.cle === 'rencontre')?.unites ?? []
  return (
    <main className="plateau-portrait">
      <BandeauPortrait monde={props.world} quiAgit={props.quiAgit} />
      <div className="portrait-table">
        {vilain.map((unite) => (
          <CarteAvecChiffres
            key={unite.cle}
            carte={unite.carte}
            nom={unite.carte.name}
            chiffres={(unite.carte.stats ?? []).map((stat) => ({
              valeur: String(stat.value),
              libelle: stat.label,
            }))}
          />
        ))}
        {principal ? (
          <>
            {/* Aucun `chiffres` ici : la menace se lit deja sur BarreMenace,
                un second affichage a cote serait redondant. */}
            <CarteAvecChiffres key={principal.cle} carte={principal.carte} nom={principal.carte.name} chiffres={[]} />
            <BarreMenace {...menaceDe(principal.carte)} />
          </>
        ) : null}
        <CompteursPortrait compteurs={comptesRencontre(rencontre)} />
      </div>
    </main>
  )
}
