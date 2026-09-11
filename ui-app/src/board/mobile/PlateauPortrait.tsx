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
import { BarreBas } from './BarreBas'
import { BarreMenace } from './BarreMenace'
import { CarteAvecChiffres } from './CarteAvecChiffres'
import { CompteursPortrait } from './CompteursPortrait'
import { MainPortrait } from './MainPortrait'
import { repartirEnBlocs } from './blocs-portrait'
import './portrait.css'

/**
 * TOUS les chiffres d'un personnage (vilain, engage, heros, allie), dans la
 * forme qu'attend `CarteAvecChiffres`.
 *
 * CORRECTION post tache 6 : cette fonction ne lisait QUE `stats`
 * (statsAffichees dans card-model.ts), qui ne porte que les stats qui
 * different de la valeur imprimee sur le scan — vide la plupart du temps.
 * Resultat : quasiment aucun chiffre n'apparaissait a cote de la carte,
 * contrairement a la regle centrale du chantier (releve sur
 * play.marvelsimulator.com : le vilain montre "10/10" a cote, un heros
 * "3 REC"/"11 PV" a cote). Les PV, eux, ne passent jamais par `stats` : ils
 * vivent dans `jauge`/`allyHp` (voir card-model.ts), que `CarteAvecChiffres`
 * retire desormais AUSSI avant de les passer a ScanCard — sans quoi ils
 * restaient dessines sur l'illustration, le meme interdit que `stats`.
 *
 * PV d'abord (texte deja forme "X / Y" par jaugeAffichee(), ou a defaut
 * `allyHp` "X/Y" quand aucune jauge n'est calculable), puis les stats
 * modifiees.
 */
function chiffresDe(carte: ScanCardProps): Array<{ valeur: string; libelle: string }> {
  const chiffres: Array<{ valeur: string; libelle: string }> = []
  const pv = carte.jauge?.texte ?? carte.allyHp
  if (pv) chiffres.push({ valeur: pv, libelle: t('PV') })
  for (const stat of carte.stats ?? []) {
    chiffres.push({ valeur: String(stat.value), libelle: stat.label })
  }
  return chiffres
}

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
  const engages = blocs.find((bloc) => bloc.cle === 'engages')?.unites ?? []
  const heros = blocs.find((bloc) => bloc.cle === 'heros')?.unites ?? []
  const main = blocs.find((bloc) => bloc.cle === 'main')?.unites ?? []
  return (
    <main className="plateau-portrait">
      <BandeauPortrait monde={props.world} quiAgit={props.quiAgit} />
      <div className="portrait-table">
        {vilain.map((unite) => (
          <CarteAvecChiffres
            key={unite.cle}
            carte={unite.carte}
            nom={unite.carte.name}
            chiffres={chiffresDe(unite.carte)}
          />
        ))}
        {principal ? (
          <>
            {/* Aucun `chiffres` ici : la menace se lit deja sur BarreMenace,
                un second affichage a cote serait redondant. Une manigance
                n'est pas un personnage (isUnit false) : chiffresDe() n'y
                trouverait de toute facon ni PV ni stats. */}
            <CarteAvecChiffres key={principal.cle} carte={principal.carte} nom={principal.carte.name} chiffres={[]} />
            <BarreMenace {...menaceDe(principal.carte)} />
          </>
        ) : null}
        <CompteursPortrait compteurs={comptesRencontre(rencontre)} />

        <section className="portrait-bloc portrait-engages">
          <h2 className="portrait-bloc-titre">{t('Engagés')}</h2>
          {engages.length === 0 ? (
            <p className="portrait-vide">{t('Aucun ennemi engagé')}</p>
          ) : (
            engages.map((unite) => (
              <CarteAvecChiffres
                key={unite.cle}
                carte={unite.carte}
                nom={unite.carte.name}
                chiffres={chiffresDe(unite.carte)}
              />
            ))
          )}
        </section>

        <section className="portrait-bloc portrait-heros">
          <h2 className="portrait-bloc-titre">{t('Ton héros')}</h2>
          {heros.map((unite) => (
            <CarteAvecChiffres
              key={unite.cle}
              carte={unite.carte}
              nom={unite.carte.name}
              chiffres={chiffresDe(unite.carte)}
            />
          ))}
        </section>
      </div>
      {/* Troisieme rangee de la grille (auto) : la main, puis la barre du bas
          en dessous. Un seul conteneur pour que la grille garde exactement
          ses trois rangees (`auto 1fr auto`), pas une quatrieme implicite. */}
      <div className="portrait-bas">
        {/* Un tap ouvre la carte (apercu), il ne la joue pas : appui long et
            jouer viennent d'une tache suivante (decision du 11/09/2026, pour
            ne pas jouer une carte qu'on visait juste a regarder). */}
        <MainPortrait unites={main} onOuvrir={(unite) => props.onCardClick?.(unite.carte)} />
        {/*
          Reutilisee telle quelle : PlateauPaysage et PlateauMedaillons
          cablent deja `actionsPartie`/`outils` sur cette meme barre (Journal,
          Annuler, Fin du tour seul colore y vivent depuis board.tsx). Le
          brief demandait une barre locale si la signature ne convenait pas :
          elle convient, inventer une seconde barre aurait fait deux endroits
          a maintenir pour le meme chrome.
        */}
        <BarreBas demande={props.bas} outils={props.actionsPartie} onglets={props.outils} />
      </div>
    </main>
  )
}
