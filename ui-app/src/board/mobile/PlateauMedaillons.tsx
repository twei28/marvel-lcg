// ⚠ ANCIEN MODELE (medaillons, portrait). Conserve derriere `?medaillons` pour
// comparer sur le telephone, jusqu'a sa suppression au sous-projet 3 de
// docs/superpowers/specs/2026-09-07-parcours-solo-mobile-design.md (§4.9).
// Le rendu par defaut est PlateauPortrait.tsx.
//
// Le mini-plateau : la partie sur un telephone.
//
// Ce n'est pas le plateau PC en petit, ni une liste de zones. C'est une TABLE
// composee : chaque carte posee devient un medaillon, les rangees sont centrees,
// et l'ensemble tient a l'ecran sans defilement global.
//
// Deux versions ont echoue avant celle-ci, pour des raisons opposees. La
// premiere condensait chaque carte en une tuile de 140x96 portant une vignette
// de 34x47 : illisible, et en paysage la degradation repliait les six bandes en
// lignes de titre, laissant un ecran vide. La seconde rendait de VRAIES cartes
// empilees verticalement : lisible, mais « tout l'un en dessous de l'autre »,
// une liste et non un jeu.
//
// L'etat de l'art (Hearthstone, MTG Arena, Gwent) dit la meme chose : une carte
// POSEE change de forme, le plateau reste spatial, et la main est fanee en bas.
// C'est ce que ce fichier applique.
//
// Il accepte exactement les BoardProps du plateau PC : c'est ce qui permet a
// board.tsx de choisir l'un ou l'autre sans rien adapter.

import { useEffect, useMemo, useState } from 'react'
import { avecInteraction, phaseAffichee, type BoardProps } from '../Board'
import { t } from '../langue'
import type { CardEffectDelta, ScanCardProps } from '../../components/ScanCard'
import type { EtatInteractif } from '../interaction'
import type { UniteAffichee } from '../zones'
import { repartir, BANDES_PLATEAU, type BandeAffichee, type CleBande } from './bandes'
import { useCouches, useCouchesBoard } from './couches'
import { MainEventail } from './MainEventail'
import { RangeeMedaillons } from './RangeeMedaillons'
import { BarreBas } from './BarreBas'
import { CarteOuverte } from './CarteOuverte'
import { TiroirPiles, type PileAffichee } from './TiroirPiles'
import { useOrientation } from './useOrientation'
import { ZoneFocus } from './ZoneFocus'
import './mobile.css'
import './medaillon.css'

const AUCUNE_INTERACTION: Map<number, EtatInteractif> = new Map()
const AUCUN_EFFET: Map<number, CardEffectDelta> = new Map()

/** Toutes les unites d'une bande, tous emplacements confondus. */
function unitesDe(bande: BandeAffichee | undefined): UniteAffichee[] {
  if (!bande) return []
  return bande.emplacements.flatMap((emplacement) => emplacement.groupes.flat())
}

export function PlateauMedaillons({
  world,
  playerId,
  plateau,
  bas,
  outils,
  actionsPartie,
  interactifs = AUCUNE_INTERACTION,
  effets = AUCUN_EFFET,
  carteFocalisee,
  onFermerCarte,
  selecteurOuvert = false,
  onFermerSelecteur,
  onCardClick,
}: BoardProps) {
  const orientation = useOrientation()
  const couches = useCouches()
  const { pile, ouvrir, fermer } = couches
  useCouchesBoard(carteFocalisee, selecteurOuvert, couches, onFermerCarte, onFermerSelecteur)
  const [pileRegardee, setPileRegardee] = useState<
    { titre: string; cartes: ScanCardProps[] } | undefined
  >(undefined)
  /** La carte qu'on lit en grand. Un medaillon ne porte ni nom ni regles. */
  const [carteOuverte, setCarteOuverte] = useState<ScanCardProps | undefined>(undefined)

  // Les etats d'interaction sont poses sur chaque carte AVANT le decoupage :
  // le medaillon lit `state` pour savoir s'il est une cible legale.
  const bandes = useMemo(() => {
    const decorer = (carte: ScanCardProps) => avecInteraction(carte, interactifs, effets)
    return repartir(plateau).map((bande) => ({
      ...bande,
      emplacements: bande.emplacements.map((emplacement) => ({
        ...emplacement,
        groupes: emplacement.groupes.map((groupe) =>
          groupe.map((unite) => ({
            ...unite,
            carte: decorer(unite.carte),
            attachees: unite.attachees.map(decorer),
          }))
        ),
      })),
    }))
  }, [plateau, interactifs, effets])

  const parCle = useMemo(() => {
    const index = new Map<CleBande, BandeAffichee>()
    for (const bande of bandes) index.set(bande.cle, bande)
    return index
  }, [bandes])

  // Combien de cibles legales chaque rangee porte, pour l'afficher sur son titre.
  const ciblesParBande = useMemo(() => {
    const compte = new Map<CleBande, number>()
    for (const bande of bandes) {
      const n = unitesDe(bande).filter((unite) => {
        const etat = interactifs.get(Number(unite.carte.id))
        return etat?.role === 'cible' || etat?.role === 'cible-preview'
      }).length
      if (n > 0) compte.set(bande.cle, n)
    }
    return compte
  }, [bandes, interactifs])

  // Un ciblage est en cours : tout ce qui n'est pas visable s'eteint.
  const enCiblage = ciblesParBande.size > 0

  // Un PAIEMENT est en cours des qu'une carte porte le role « ressource ».
  // On reutilise exactement le traitement du ciblage : tout s'eteint sauf ce
  // qui peut payer — cartes de la main ET generateurs deja en jeu, que le
  // moteur marque du meme role. Le compte « 2/4 » vit dans la barre du bas,
  // rendue par le plateau PC (voir BarreAction).
  const paiementDemande = useMemo(
    () => [...interactifs.values()].some((etat) => etat.role === 'ressource'),
    [interactifs]
  )

  // Le moteur peut DEMANDER un paiement sans qu'on soit pret a s'engager.
  // Tant qu'on n'a pas touche « Payer », le plateau reste normal : c'est ce qui
  // laisse reculer avant de depenser quoi que ce soit.
  const [paiementAccepte, setPaiementAccepte] = useState(false)
  useEffect(() => {
    if (!paiementDemande) setPaiementAccepte(false)
  }, [paiementDemande])
  const enPaiement = paiementDemande && paiementAccepte

  const piles: PileAffichee[] = useMemo(
    () =>
      unitesDe(parCle.get('piles')).map((unite) => ({
        cle: unite.cle,
        titre: unite.pileTitre ?? unite.carte.name,
        unite,
      })),
    [parCle]
  )

  // Depuis la MAIN (appui long) ou le mode focus : on agit directement.
  const jouerCarte = (carte: ScanCardProps) => {
    if (carte.onSelect) carte.onSelect()
    else onCardClick?.(carte)
  }

  // Depuis un MEDAILLON : on ouvre d'abord, parce qu'un medaillon ne porte ni
  // nom ni texte de regles. L'action se declenche depuis le panneau ouvert.
  const ouvrirCarte = (carte: ScanCardProps) => setCarteOuverte(carte)

  const coucheFocus = [...pile].reverse().find((couche) => couche.sorte === 'focus')
  const bandeEnFocus = coucheFocus
    ? bandes.find((bande) => bande.cle === coucheFocus.bande)
    : undefined

  const main = unitesDe(parCle.get('main')).map((unite) => unite.carte)

  return (
    <div
      className={
        `plateau-mobile est-${orientation}` +
        (enCiblage || enPaiement ? ' est-en-ciblage' : '') +
        (enPaiement ? ' est-en-paiement' : '')
      }
    >
      {/* En PAYSAGE la largeur permet une colonne de piles visible, comme sur le
          plateau PC : le tiroir n'aurait plus de raison d'être. En portrait il
          reste le seul moyen de les atteindre. */}
      {orientation === 'portrait' ? (
        <TiroirPiles
          piles={piles}
          onOuvrirPile={(titre, cartes) => setPileRegardee({ titre, cartes })}
        />
      ) : (
        <aside className="pm-colonne-piles" aria-label={t('Piles')}>
          <ul className="tiroir-liste">
            {piles.map((pile) => {
              const contenu = pile.unite.pileContenu
              const consultable = contenu !== undefined && contenu.length > 0
              return (
                <li key={pile.cle}>
                  <button
                    type="button"
                    className="tiroir-pile"
                    disabled={!consultable}
                    onClick={() => {
                      if (consultable) {
                        setPileRegardee({ titre: pile.unite.pileTitre ?? pile.titre, cartes: contenu })
                      }
                    }}
                  >
                    <span className="tiroir-pile-nom">{pile.titre}</span>
                    <span className="tiroir-pile-compte">{contenu?.length ?? 0}</span>
                  </button>
                </li>
              )
            })}
          </ul>
        </aside>
      )}

      <div className="pm-rangees">
        {BANDES_PLATEAU.map((cle) => {
          const bande = parCle.get(cle)
          if (!bande) return null
          return (
            <RangeeMedaillons
              key={cle}
              titre={
                cle === 'heros'
                  ? `${bande.titre} · ${phaseAffichee(world.phase)}`
                  : bande.titre
              }
              unites={unitesDe(bande)}
              // La manigance principale decide de la defaite : meme vocabulaire,
              // taille superieure.
              taille={cle === 'complots' ? 'grand' : 'normal'}
              cibles={ciblesParBande.get(cle)}
              effets={effets}
              onOuvrirCarte={ouvrirCarte}
            />
          )
        })}
      </div>

      {/* Plus de largeur a transmettre : les cartes ne se resserrent plus, la
          main se balaie quand elle deborde. */}
      <MainEventail cartes={main} modePaiement={enPaiement} onJouer={jouerCarte} />

      {paiementDemande && !paiementAccepte ? (
        <div className="pm-barre pm-barre-demande">
          <button
            type="button"
            className="pm-payer"
            onClick={() => setPaiementAccepte(true)}
          >
            {t('Payer')}
          </button>
          {bas}
        </div>
      ) : (
        <BarreBas demande={bas} outils={actionsPartie} onglets={outils} />
      )}

      {bandeEnFocus ? (
        <ZoneFocus
          bande={bandeEnFocus}
          playerId={playerId}
          onFermer={fermer}
          onOuvrirCarte={jouerCarte}
        />
      ) : null}

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

      {/* `ouvrir` reste utilise par ZoneFocus via la pile de couches. */}
      <span hidden aria-hidden="true" onClick={() => ouvrir({ sorte: 'focus', bande: 'terrain' })} />
    </div>
  )
}
