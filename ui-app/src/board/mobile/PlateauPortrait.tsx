// Le plateau du telephone, en BANDES (spec du 12/09/2026,
// docs/superpowers/specs/2026-09-12-plateau-portrait-en-bandes-design.md).
//
// Un bandeau fixe en haut (phase, menu « … », Fin du tour), puis une table
// qui defile verticalement avec quatre bandes horizontales (mechant,
// manigances, engages, mon heros), chacune defilant du doigt, plus les
// soutiens et les ameliorations sur leur propre ligne quand il y en a. La main est
// cachee derriere l'encoche de droite, les piles derriere celle de gauche.
// Meme plateau en paysage, avec des bandes plus larges (portrait.css).
//
// Il accepte exactement les BoardProps du plateau PC : c'est ce qui permet a
// board.tsx de choisir sans rien adapter. Il ne decore rien lui-meme : les
// bandes passent par `Unite` (Board.tsx), qui appelle `avecInteraction`, la
// seule copie autorisee de cette logique.
import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from 'react'
import { ImagesParesseuses, type CardEffectDelta, type ScanCardProps } from '../../components/ScanCard'
import { PileRegardee, avecInteraction } from '../Board'
import type { BoardProps } from '../Board'
import type { EtatInteractif } from '../interaction'
import { t } from '../langue'
import type { GroupeDePile, UniteAffichee } from '../zones'
import { Bande } from './Bande'
import { BandeauAnnuler } from './BandeauAnnuler'
import { BandeauPortrait } from './BandeauPortrait'
import { CarteOuverte } from './CarteOuverte'
import { Encoche } from './Encoche'
import { MainPortrait } from './MainPortrait'
import { OngletsJoueurs } from './OngletsJoueurs'
import { TiroirPiles } from './TiroirPiles'
import { repartirEnBandes } from './bandes-portrait'
import { useHauteurDeQuestion } from './hauteur-de-question'
import { TableRonds } from './ronds/TableRonds'
import { MainSousLaTable } from './ronds/MainSousLaTable'
import { RoundEnGrand } from './ronds/RoundEnGrand'
import { ContexteGlisse, CoucheGlisseRonds, useGlisserAuDoigt } from './ronds/glisser-ronds'
import { useReglagesTelephone } from './reglages-telephone'
import { useDefilerVersLaCible } from './defiler-vers-la-cible'
import './portrait.css'
import './telephone.css'

const AUCUNE_INTERACTION: Map<number, EtatInteractif> = new Map()
const AUCUN_EFFET: Map<number, CardEffectDelta> = new Map()

/** Les roles qui font d'une carte en main l'objet d'une QUESTION. */
const ROLES_DE_QUESTION = new Set(['cible', 'ressource'])

/**
 * Une question du moteur porte sur la main quand au moins une carte en main
 * est une cible a choisir ou une ressource a depenser.
 *
 * ⚠ Pas le role `porteur` : pendant tout le tour du joueur, chaque carte
 * jouable de la main est un porteur (elle PEUT lancer une action). Le
 * compter ouvrirait la main en permanence, ce qui est exactement ce que
 * l'encoche existe pour eviter (mesure le 12/09/2026 : le voile de la main
 * bloquait le bandeau des la fin du mulligan). `mainVisibleForcee` (plateau
 * PC) est trop large dans l'autre sens : il s'allume pour toute etape de
 * ciblage, meme sans carte de main.
 */
export function questionSurLaMain(
  main: UniteAffichee[],
  interactifs: Map<number, EtatInteractif> | undefined
): boolean {
  if (!interactifs || interactifs.size === 0) return false
  const idsMain = new Set(main.map((unite) => Number(unite.carte.id)))
  for (const [id, etat] of interactifs) {
    if (idsMain.has(id) && ROLES_DE_QUESTION.has(etat.role)) return true
  }
  return false
}

/** La carte `id` telle que le plateau la porte maintenant : posee, attachee ou en main. */
function trouverCarte(
  plateau: BoardProps['plateau'],
  main: UniteAffichee[],
  id: string
): ScanCardProps | undefined {
  const unites = [...(plateau?.emplacements ?? []).flatMap((emplacement) => emplacement.groupes.flat()), ...main]
  for (const unite of unites) {
    if (unite.carte.id === id) return unite.carte
    const attachee = unite.attachees.find((carte) => carte.id === id)
    if (attachee) return attachee
  }
  return undefined
}

export function PlateauPortrait(props: BoardProps) {
  const bandes = useMemo(() => repartirEnBandes(props.plateau), [props.plateau])
  // La forme de la table : les cartes en bandes, ou les ronds (essai du 24/10/2026, choisi au debut de la partie).
  const { plateau: formeDeTable } = useReglagesTelephone()
  // Le glisser au doigt (ronds seulement) : memes regles que le plateau PC (`props.glisser`), geste adapte aux ronds.
  const glisserRonds = useGlisserAuDoigt(formeDeTable === 'ronds' ? props.glisser : undefined)
  const interactifs = props.interactifs ?? AUCUNE_INTERACTION
  const effets = props.effets ?? AUCUN_EFFET
  // Les bandes decorent leurs cartes via `Unite` ; la main, rendue a part,
  // recoit la sienne ici (jouable, cible, ressource a depenser).
  const main = useMemo(
    () => bandes.main.map((unite) => ({ ...unite, carte: avecInteraction(unite.carte, interactifs, effets) })),
    [bandes.main, interactifs, effets]
  )

  // La carte lue EN GRAND, au milieu de l'ecran. `props.onCardClick` ne sert
  // pas a lire une carte : il ouvre les ACTIONS du moteur. Lire est un etat
  // local, comme sur le portrait du 11/09.
  const [carteLue, setCarteLue] = useState<
    { carte: ScanCardProps; attachees: ScanCardProps[]; libelleAction?: string; deLaMain?: boolean } | undefined
  >()
  const ouvrirCarte = useCallback(
    (carte: ScanCardProps, attachees: ScanCardProps[] = [], libelleAction?: string, deLaMain?: boolean) =>
      setCarteLue({ carte, attachees, libelleAction, deLaMain }),
    []
  )
  // La carte ouverte SUIT la question en cours (06/10/2026) : son action est
  // relue a chaque rendu. Ouverte pendant le mulligan, elle portait l'action du
  // mulligan ; « Garder ma main » restait touchable au-dessus, et la mise en
  // place finie, elle restait ouverte avec un bouton vers une question close.
  // Une carte ouverte POUR une action se referme quand l'action disparait ;
  // une carte ouverte pour la lire reste ouverte.
  const carteLueActuelle = useMemo(() => {
    if (!carteLue) return undefined
    const brute = trouverCarte(props.plateau, bandes.main, carteLue.carte.id)
    return brute ? avecInteraction(brute, interactifs, effets) : undefined
  }, [carteLue, props.plateau, bandes.main, interactifs, effets])
  const actionPerdue = carteLue?.carte.onSelect !== undefined && carteLueActuelle?.onSelect === undefined
  useEffect(() => {
    if (actionPerdue) setCarteLue(undefined)
  }, [actionPerdue])
  // Les encoches s'effacent pendant le defilement de la table (elles se
  // posent sur la bande du heros).
  const [enDefilement, setEnDefilement] = useState(false)
  const finDeDefilement = useRef<number | undefined>(undefined)
  const surDefilement = useCallback(() => {
    setEnDefilement(true)
    if (finDeDefilement.current !== undefined) window.clearTimeout(finDeDefilement.current)
    finDeDefilement.current = window.setTimeout(() => setEnDefilement(false), 600)
  }, [])
  useEffect(() => () => {
    if (finDeDefilement.current !== undefined) window.clearTimeout(finDeDefilement.current)
  }, [])
  // Une cible allumee hors de l'ecran : la table defile jusqu'a elle.
  useDefilerVersLaCible(props.interactifs)
  const [pileRegardee, setPileRegardee] = useState<
    { titre: string; cartes: ScanCardProps[]; groupes?: GroupeDePile[] } | undefined
  >()
  const [tiroirOuvert, setTiroirOuvert] = useState(false)
  // En ronds, la main est posee SOUS les zones et ouverte d'office (24/10/2026) ; en bandes, elle reste cachee derriere son encoche.
  const [mainOuverte, setMainOuverte] = useState(formeDeTable === 'ronds')
  useEffect(() => {
    setMainOuverte(formeDeTable === 'ronds')
  }, [formeDeTable])
  // La feuille de question du bas (« x / Jouer », la question du moteur) :
  // la main ouverte se pose au-dessus d'elle, jamais dessous.
  const hauteurDeQuestion = useHauteurDeQuestion()

  // L'ouverture AUTOMATIQUE de la main : elle sort quand une question porte
  // sur elle, et se range quand la question est passee — mais seulement si
  // c'est la question qui l'avait ouverte, jamais si le joueur l'a sortie
  // lui-meme.
  //
  // ⚠ ET ELLE NE SE ROUVRE PLUS DANS LE DOS DU JOUEUR. Rapport joueur du
  // 13/09/2026 : « quand on doit payer des ressources avec des cartes sur la
  // table, c'est impossible ». Mesure : payer une carte POSEE demande de
  // refermer la main (son voile couvre tout l'ecran), puis d'ouvrir la fiche
  // de la carte et d'appuyer sur « Utiliser cette carte ». Or CHAQUE ressource
  // choisie fait repasser le plateau par un rendu SANS question, le temps que
  // le moteur reponde : `laQuestion` retombait a faux puis remontait, et la
  // main se rouvrait. Sur un cout a 3, il fallait la refermer trois fois.
  //
  // `refuseeParLeJoueur` retient le geste : une fois la main rangee a la main,
  // elle ne ressort que si le joueur la rappelle par son encoche, ou quand la
  // situation change vraiment (phase ou round). Le voile, lui, reste : c'est
  // par lui qu'on ferme d'un geste.
  const laQuestion = questionSurLaMain(bandes.main, props.interactifs)
  const ouvertePourLaQuestion = useRef(false)
  const refuseeParLeJoueur = useRef(false)
  const situation = `${props.world?.round_id ?? ''}/${props.world?.phase ?? ''}`
  useEffect(() => {
    refuseeParLeJoueur.current = false
  }, [situation])
  useEffect(() => {
    if (laQuestion) {
      if (refuseeParLeJoueur.current) return
      setMainOuverte((ouverte) => {
        if (!ouverte) ouvertePourLaQuestion.current = true
        return true
      })
    } else if (ouvertePourLaQuestion.current) {
      ouvertePourLaQuestion.current = false
      // En ronds, la main est posee sous les zones : elle ne se range pas toute seule (seul le joueur la replie).
      if (formeDeTable !== 'ronds') setMainOuverte(false)
    }
  }, [laQuestion, formeDeTable])

  const ouvrirPile = useCallback(
    (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) => setPileRegardee({ titre, cartes, groupes }),
    []
  )
  // Agir avec une carte : l'action DIRECTE posee par le moteur ; a defaut,
  // `onCardClick` ouvre le menu des actions de la carte (board.tsx).
  // En mode manuel, l'appui long ouvre le menu du clic droit (CoucheTriche,
  // lot 4) : le portrait n'agit pas en plus.
  const manuelAuDoigt = props.glisser?.auDoigt === true
  const agir = useCallback(
    (carte: ScanCardProps) => {
      if (manuelAuDoigt) return
      if (carte.onSelect) carte.onSelect()
      else props.onCardClick?.(carte)
    },
    [props.onCardClick, manuelAuDoigt]
  )
  // « Jouer » (zone 3) : une carte de la main que le moteur propose de JOUER
  // (role `porteur`), pas une ressource a depenser ni une cible a cocher.
  const jouable = useCallback(
    (unite: UniteAffichee) => !manuelAuDoigt && interactifs.get(Number(unite.carte.id))?.role === 'porteur',
    [interactifs, manuelAuDoigt]
  )
  // Une carte de la main ouverte en grand garde sa place dans la main : un
  // glisser du doigt passe a sa voisine (retour de Raven, 12/10/2026).
  const ouvrirDeLaMain = useCallback(
    (unite: UniteAffichee) => ouvrirCarte(unite.carte, [], jouable(unite) ? t('Jouer') : undefined, true),
    [ouvrirCarte, jouable]
  )
  const rangDansLaMain = carteLue?.deLaMain ? main.findIndex((u) => u.carte.id === carteLue.carte.id) : -1
  const voisines =
    rangDansLaMain < 0
      ? undefined
      : {
          position: rangDansLaMain + 1,
          total: main.length,
          precedente: rangDansLaMain > 0 ? () => ouvrirDeLaMain(main[rangDansLaMain - 1]) : undefined,
          suivante: rangDansLaMain < main.length - 1 ? () => ouvrirDeLaMain(main[rangDansLaMain + 1]) : undefined,
        }
  const decor = useMemo(
    () => ({
      interactifs,
      effets,
      heroActifId: props.heroActifId,
      ouvrirPile,
      ouvrirCarte,
      agir,
    }),
    [interactifs, effets, props.heroActifId, ouvrirPile, ouvrirCarte, agir]
  )

  // Les onglets ne trient PAS des cartes deja recues : ils rappellent
  // board.tsx (`choisirJoueurRegarde` = `setVueForcee`) pour qu'il
  // RECONSTRUISE `props.plateau` sur un autre joueur (`seulCeJoueur`).
  const onglets =
    props.joueursAffichables && props.choisirJoueurRegarde ? (
      <OngletsJoueurs
        joueurs={props.joueursAffichables}
        actif={props.joueurRegarde ?? props.playerId}
        choisir={props.choisirJoueurRegarde}
      />
    ) : undefined

  return (
    <ImagesParesseuses.Provider value={true}>
    <ContexteGlisse.Provider value={glisserRonds.valeur}>
    <main
      {...(formeDeTable === 'ronds' ? glisserRonds.gestes : {})}
      className={`plateau-portrait${enDefilement ? ' est-en-defilement' : ''}${formeDeTable === 'ronds' && mainOuverte ? ' avec-main-dock' : ''}`}
      style={{ '--question-h': `${hauteurDeQuestion}px` } as CSSProperties}
    >
      <BandeauPortrait
        monde={props.world}
        quiAgit={props.quiAgit}
        menu={props.actionsPartie}
        actionPrincipale={props.actionPrincipale}
        annuler={formeDeTable === 'ronds' ? props.annulerCoup : undefined}
      />
      <div className="portrait-table" onScroll={surDefilement}>
        {formeDeTable === 'ronds' ? (
          <TableRonds bandes={bandes} decor={decor} onglets={onglets} />
        ) : (
          <>
        <Bande cle="vilain" titre={t('Méchant')} texteVide={t('Aucun méchant')} decor={decor} {...bandes.vilain} />
        <Bande
          cle="manigances"
          titre={t('Manigances')}
          texteVide={t('Aucune manigance')}
          decor={decor}
          {...bandes.manigances}
        />
        <Bande cle="engages" titre={t('Engagés')} texteVide={t('Aucun ennemi engagé')} decor={decor} {...bandes.engages} />
        <Bande
          cle="heros"
          titre={t('Ton héros')}
          texteVide={t('Aucun héros')}
          onglets={onglets}
          decor={decor}
          {...bandes.heros}
        />
        {/* Une ligne par famille (retour de Raven, 12/10/2026) : vides, elles
            ne prennent pas de place. */}
        {bandes.soutiens.unites.length > 0 ? (
          <Bande cle="soutiens" titre={t('Soutiens')} texteVide="" decor={decor} {...bandes.soutiens} />
        ) : null}
        {bandes.ameliorations.unites.length > 0 ? (
          <Bande cle="ameliorations" titre={t('Améliorations')} texteVide="" decor={decor} {...bandes.ameliorations} />
        ) : null}
          </>
        )}
      </div>

      <Encoche cote="gauche" libelle={t('Piles')} onOuvrir={() => setTiroirOuvert(true)} />
      {/* En ronds, la main ouverte est posee sous les zones : la languette ne sert qu'a la rouvrir une fois repliee. */}
      {formeDeTable === 'ronds' && mainOuverte ? null : (
        <Encoche
          cote="droite"
          libelle={t('Main')}
          nombre={bandes.main.length}
          onOuvrir={() => {
            refuseeParLeJoueur.current = false
            setMainOuverte(true)
          }}
        />

      )}

      <TiroirPiles piles={bandes.piles} ouvert={tiroirOuvert} onFermer={() => setTiroirOuvert(false)} onOuvrirPile={ouvrirPile} />
      {/* Toucher une carte jouable = la choisir, puis « Jouer » ; toucher
          long = la jouer (MainPortrait.tsx). */}
      {formeDeTable === 'ronds' ? (
        mainOuverte ? (
          <MainSousLaTable
            unites={main}
            onOuvrir={ouvrirDeLaMain}
            onJouer={(unite) => agir(unite.carte)}
            jouable={jouable}
            onReplier={() => {
              ouvertePourLaQuestion.current = false
              refuseeParLeJoueur.current = true
              setMainOuverte(false)
            }}
          />
        ) : null
      ) : (
        <MainPortrait
          unites={main}
        ouverte={mainOuverte}
        onFermer={() => {
          ouvertePourLaQuestion.current = false
          refuseeParLeJoueur.current = true
          setMainOuverte(false)
        }}
        onOuvrir={ouvrirDeLaMain}
        onJouer={(unite) => agir(unite.carte)}
        jouable={jouable}
      />
      )}
      {carteLue && !actionPerdue ? (
        <CarteOuverte
          key={carteLue.carte.id}
          carte={carteLueActuelle ?? carteLue.carte}
          voisines={voisines}
          attachees={carteLue.attachees}
          onOuvrirAttachee={(carte) => ouvrirCarte(carte)}
          onFermer={() => setCarteLue(undefined)}
          libelleAction={carteLue.libelleAction}
        />
      ) : null}
      {pileRegardee ? (
        <PileRegardee
          titre={pileRegardee.titre}
          cartes={pileRegardee.cartes}
          groupes={pileRegardee.groupes}
          fermer={() => setPileRegardee(undefined)}
        />
      ) : null}
      {/* En ronds, l'annulation est la fleche ↶ permanente du bandeau (Q45) : plus de bandeau de 5 secondes. */}
      {formeDeTable === 'ronds' ? null : <BandeauAnnuler annuler={props.annulerCoup} />}
      {formeDeTable === 'ronds' ? <RoundEnGrand round={props.world?.round_id} /> : null}
      {formeDeTable === 'ronds' ? <CoucheGlisseRonds glisse={glisserRonds.glisse} refus={glisserRonds.refus} /> : null}
    </main>
    </ContexteGlisse.Provider>
    </ImagesParesseuses.Provider>
  )
}
