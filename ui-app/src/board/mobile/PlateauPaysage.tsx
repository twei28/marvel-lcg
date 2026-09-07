// Le plateau en PAYSAGE : deux rangees de vraies cartes.
//
// Spec : docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md §4.
// Ce n'est ni le plateau PC en petit (65 px de carte a l'echelle, illisible),
// ni le modele a medaillons d'aout (des jetons ronds qui perdaient trop d'un
// terrain qui est grand). C'est la table, lue en deux lignes :
//
//   rangee ENNEMIE : mechant, manigances, sbires, environnement | piles rencontre
//   rangee HEROS   : identite(s), allies, soutiens, ameliorations | piles joueur
//   la MAIN en eventail, la BARRE du bas
//
// Une rangee qui deborde DEFILE. Rien n'est condense. En portrait, EcranPortrait
// couvre tout sans rien demonter. Il accepte exactement les BoardProps du
// plateau PC : c'est ce qui permet a board.tsx de choisir l'un ou l'autre.

import { useEffect, useMemo, useState } from 'react'
import { avecInteraction, phaseAffichee, type BoardProps } from '../Board'
import { t } from '../langue'
import type { CardEffectDelta, ScanCardProps } from '../../components/ScanCard'
import type { EtatInteractif } from '../interaction'
import type { EmplacementAffiche, UniteAffichee } from '../zones'
import { BarreBas } from './BarreBas'
import { CarteOuverte } from './CarteOuverte'
import { EcranPortrait } from './EcranPortrait'
import { MainEventail } from './MainEventail'
import { RangeeCartes, type GroupeRangee } from './RangeeCartes'
import { useCouches, useCouchesBoard } from './couches'
import { carteIdentite, groupesParJoueur, ordreDAffichage } from './joueurs'
import { doitMontrerEcranPortrait, usePleinEcranAuPremierGeste } from './plein-ecran'
import { mainDe, repartirEnRangees, unitesDe, type RangeeAffichee } from './rangees'
import { useOrientation } from './useOrientation'
import './medaillon.css'
import './paysage.css'

const AUCUNE_INTERACTION: Map<number, EtatInteractif> = new Map()
const AUCUN_EFFET: Map<number, CardEffectDelta> = new Map()

/** Les emplacements de la rangee heros qui ne sont pas l'aire des joueurs. */
const ANNEXES_HEROS = new Set<EmplacementAffiche['cle']>(['deck-special', 'reserve', 'nemesis'])

function decorerUnite(
  unite: UniteAffichee,
  decorer: (carte: ScanCardProps) => ScanCardProps
): UniteAffichee {
  return { ...unite, carte: decorer(unite.carte), attachees: unite.attachees.map(decorer) }
}

/**
 * La rangee heros, groupe par groupe : un groupe par joueur (le joueur actif
 * d'abord), puis les annexes (deck special, reserve, nemesis). En solo a un
 * heros, `proprietaires` est absent et tout revient au joueur 0 : un seul
 * groupe, comme avant.
 */
function groupesHeros(rangee: RangeeAffichee, joueurActif: number): GroupeRangee[] {
  const aire = rangee.defilants.find((emplacement) => emplacement.cle === 'terrain-soutien')
  const groupes: GroupeRangee[] = []
  if (aire) {
    const parJoueur = groupesParJoueur(aire)
    for (const joueur of ordreDAffichage([...parJoueur.keys()], joueurActif)) {
      groupes.push({
        cle: `joueur-${joueur}`,
        unites: (parJoueur.get(joueur) ?? []).flat(),
        actif: parJoueur.size > 1 && joueur === joueurActif,
      })
    }
  }
  const annexes = unitesDe(rangee.defilants.filter((emplacement) => ANNEXES_HEROS.has(emplacement.cle)))
  if (annexes.length > 0) groupes.push({ cle: 'annexes-heros', unites: annexes })
  return groupes
}

/** Le joueur dont l'identite porte `heroActifId`, sinon le joueur local. */
function joueurDeLIdentite(rangee: RangeeAffichee, heroActifId: number | undefined, defaut: number): number {
  if (heroActifId === undefined) return defaut
  const aire = rangee.defilants.find((emplacement) => emplacement.cle === 'terrain-soutien')
  if (!aire) return defaut
  for (const [joueur, groupes] of groupesParJoueur(aire)) {
    if (Number(carteIdentite(groupes)?.id) === heroActifId) return joueur
  }
  return defaut
}

export function PlateauPaysage({
  world,
  playerId,
  plateau,
  bas,
  outils,
  actionsPartie,
  interactifs = AUCUNE_INTERACTION,
  effets = AUCUN_EFFET,
  heroActifId,
  carteFocalisee,
  onFermerCarte,
  selecteurOuvert = false,
  onFermerSelecteur,
  onCardClick,
}: BoardProps) {
  const orientation = useOrientation()
  const couches = useCouches()
  useCouchesBoard(carteFocalisee, selecteurOuvert, couches, onFermerCarte, onFermerSelecteur)
  usePleinEcranAuPremierGeste(true)

  // Le cartouche du deroule (DeroulePhase, rendu par la page a cote du
  // plateau) s'adosse a la barre du bas quand cette classe est la : voir
  // paysage.css. Posee sur body parce que le cartouche n'est pas dans cet arbre.
  useEffect(() => {
    document.body.classList.add('mode-plateau-paysage')
    return () => document.body.classList.remove('mode-plateau-paysage')
  }, [])

  const [pileRegardee, setPileRegardee] = useState<{ titre: string; cartes: ScanCardProps[] } | undefined>()
  const [carteOuverte, setCarteOuverte] = useState<ScanCardProps | undefined>()

  // Les etats d'interaction sont poses sur chaque carte AVANT le decoupage ; le
  // badge « Active » suit heroActifId, comme sur le plateau PC.
  const rangees = useMemo(() => {
    const decorer = (carte: ScanCardProps) => {
      const decoree = avecInteraction(carte, interactifs, effets)
      return heroActifId !== undefined && Number(carte.id) === heroActifId ? { ...decoree, estActif: true } : decoree
    }
    const decorerEmplacement = (emplacement: EmplacementAffiche): EmplacementAffiche => ({
      ...emplacement,
      groupes: emplacement.groupes.map((groupe) => groupe.map((unite) => decorerUnite(unite, decorer))),
    })
    return repartirEnRangees(plateau).map((rangee) => ({
      ...rangee,
      defilants: rangee.defilants.map(decorerEmplacement),
      epingles: rangee.epingles.map(decorerEmplacement),
    }))
  }, [plateau, interactifs, effets, heroActifId])

  const [ennemie, heros] = rangees
  const joueurActif = joueurDeLIdentite(heros, heroActifId, playerId)

  // Memorises : sans quoi RangeeCartes recevrait un nouveau tableau de
  // groupes a chaque rendu du parent, et son ResizeObserver se deconnecterait
  // et se reconnecterait a chaque fois (son effet depend de `groupes`).
  const groupesEnnemie = useMemo(
    () => [{ cle: 'ennemie', unites: unitesDe(ennemie.defilants) }],
    [ennemie]
  )
  const groupesDeHeros = useMemo(() => groupesHeros(heros, joueurActif), [heros, joueurActif])

  const ciblesDe = (rangee: RangeeAffichee): number =>
    unitesDe(rangee.defilants).filter((unite) => {
      const etat = interactifs.get(Number(unite.carte.id))
      return etat?.role === 'cible' || etat?.role === 'cible-preview'
    }).length
  const ciblesEnnemie = ciblesDe(ennemie)
  const ciblesHeros = ciblesDe(heros)
  const enCiblage = ciblesEnnemie + ciblesHeros > 0

  // Un PAIEMENT est en cours des qu'une carte porte le role « ressource ». Tant
  // qu'on n'a pas touche « Payer », le plateau reste normal : on peut reculer.
  const paiementDemande = useMemo(
    () => [...interactifs.values()].some((etat) => etat.role === 'ressource'),
    [interactifs]
  )
  const [paiementAccepte, setPaiementAccepte] = useState(false)
  useEffect(() => {
    if (!paiementDemande) setPaiementAccepte(false)
  }, [paiementDemande])
  const enPaiement = paiementDemande && paiementAccepte

  const main = useMemo(
    () => mainDe(plateau).map((unite) => avecInteraction(unite.carte, interactifs, effets)),
    [plateau, interactifs, effets]
  )

  // Depuis la MAIN (appui long) ou la carte ouverte : on agit directement.
  const jouerCarte = (carte: ScanCardProps) => {
    if (carte.onSelect) carte.onSelect()
    else onCardClick?.(carte)
  }
  const ouvrirPile = (titre: string, cartes: ScanCardProps[]) => setPileRegardee({ titre, cartes })

  return (
    <div
      className={
        `plateau-mobile plateau-paysage est-${orientation}` +
        (enCiblage || enPaiement ? ' est-en-ciblage' : '') +
        (enPaiement ? ' est-en-paiement' : '')
      }
    >
      <div className="pp-rangees">
        <RangeeCartes
          cle="ennemie"
          titre={ennemie.titre}
          groupes={groupesEnnemie}
          piles={unitesDe(ennemie.epingles)}
          cibles={ciblesEnnemie || undefined}
          effets={effets}
          onOuvrirCarte={setCarteOuverte}
          onOuvrirPile={ouvrirPile}
        />
        <RangeeCartes
          cle="heros"
          titre={`${heros.titre} · ${phaseAffichee(world.phase)}`}
          groupes={groupesDeHeros}
          piles={unitesDe(heros.epingles)}
          cibles={ciblesHeros || undefined}
          effets={effets}
          onOuvrirCarte={setCarteOuverte}
          onOuvrirPile={ouvrirPile}
        />
      </div>

      <MainEventail cartes={main} modePaiement={enPaiement} onJouer={jouerCarte} />

      {paiementDemande && !paiementAccepte ? (
        <div className="pm-barre pm-barre-demande">
          <button type="button" className="pm-payer" onClick={() => setPaiementAccepte(true)}>
            {t('Payer')}
          </button>
          {bas}
        </div>
      ) : (
        <BarreBas demande={bas} outils={actionsPartie} onglets={outils} />
      )}

      {carteOuverte ? (
        <CarteOuverte carte={carteOuverte} onFermer={() => setCarteOuverte(undefined)} />
      ) : null}

      {pileRegardee ? (
        <div className="focus-voile" onPointerDown={() => setPileRegardee(undefined)}>
          <section
            className="focus"
            role="dialog"
            aria-label={pileRegardee.titre}
            onPointerDown={(evenement) => evenement.stopPropagation()}
          >
            <header className="focus-entete">
              <h2>{pileRegardee.titre}</h2>
              <button type="button" className="focus-fermer" onClick={() => setPileRegardee(undefined)}>
                {t('Fermer')}
              </button>
            </header>
            <div className="focus-corps">
              <div className="focus-cartes">
                {pileRegardee.cartes.map((carte) => (
                  <span key={carte.id}>
                    <img className="pile-carte" src={carte.imageUrl} alt={carte.name} />
                  </span>
                ))}
              </div>
            </div>
          </section>
        </div>
      ) : null}

      {doitMontrerEcranPortrait(orientation) ? <EcranPortrait /> : null}
    </div>
  )
}
