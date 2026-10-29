// Page du nouveau plateau.
//
//   /app/board.html                -> la partie en cours, JOUABLE
//   /app/board.html?etat=<fichier> -> un etat de partie enregistre, lecture seule
//   /app/board.html?p=1            -> le plateau vu par le joueur 1
//
// Le plateau est AJOUTE a cote de l'ancien, il ne le remplace pas : la barre du
// haut ramene a l'ancienne interface a tout moment. Aucun fichier du jeu n'est
// modifie.
//
// Attention : en mode partie en cours, cette page ouvre le socket du moteur et
// devient donc un vrai client de jeu. Elle DOIT accuser reception des rendus,
// sinon la partie se figerait (voir moteur.ts).
// ⚠ EN PREMIER : dans le cadre du spectateur et de la relecture, ce module
// remplace localStorage avant que quiconque ne le lise (cadre-joueur.ts).
import { estCadre, poserSurvolsDuJoueur, recouvrir, reglagesDuJoueur, stockageDuCadre } from './board/cadre-joueur'
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
  type FocusEvent as ReactFocusEvent,
  type MouseEvent as ReactMouseEvent,
} from 'react'
import { createRoot, type Root } from 'react-dom/client'
import '../styles/tokens.css'
import '../styles/palette.css'
import '../styles/affichage-sobre.css'
import '../styles/affichage-epure.css'
import '../styles/teinte.css'
import { PlusieursJoueurs, ScanCard, type CardEffectDelta, type ScanCardProps } from './components/ScanCard'
import { AssistantAction } from './board/AssistantAction'
import { consigne, phraseEtat } from './board/phrase-etat'
import { CartesDuJournal, type AccesCartesJournal } from './board/NomsDeCartes'
import { estModeManuel, leMoteurSeTait } from './board/manuel/mode'
import { SelecteurHeros } from './board/manuel/SelecteurHeros'
import { InterrupteurFacon } from './board/manuel/InterrupteurFacon'
import { aideSOuvreSeule, VoletAideManuel } from './board/manuel/VoletAideManuel'
import { VoletAideAuto } from './board/VoletAideAuto'
import { reglagesGlisserManuel } from './board/manuel/glisser-manuel'
import { carteDeLaTrame, contexteDePose, estCacheePourLeJoueur, origineDe } from './board/manuel/poser-en-jeu'
import { peutBouger, proprietaireDe, siegesControles } from './board/manuel/proprietaire'
// ⚠ IMPORT NOMME, PAS `import * as triche` : `PagePartie` a deja un
// identifiant local `triche` (`useTriche(...)`, le bac a sable) -- un import
// namespace du meme nom serait ombrage silencieusement par lui a l'usage.
import { basculerPause, reprendreEnAuto } from './board/triche'
import { BarreAction } from './board/BarreAction'
import { Board, CarteApercu, type ReglagesGlisser } from './board/Board'
import type { CibleSurvolee } from './board/glisser/useGlisser'
import { envoyerMarque, useMarques } from './board/manuel/marques'
import { CoucheMarques } from './board/manuel/CoucheMarques'
import { CoucheSelection } from './board/manuel/CoucheSelection'
import { cartesDuGeste, selection } from './board/manuel/selection'
import {
  ciblesDeLaSource,
  estSourceGlissable,
  optionJouer,
  optionsDuDepot,
  optionsSansCible,
  raisonDuRefus,
  refusJouer,
  zonesDeLaSource,
  zonesSansCible,
} from './board/glisser/cibles'
import { PlateauMobile } from './board/mobile/PlateauMobile'
import { useModeMobile, type ReglageMode } from './board/mobile/useModeMobile'
import { useEcranAllume, useEstTelephone, useVerrouPortrait, useVibrationsDePartie } from './board/mobile/telephone'
import { useReglagesTelephone } from './board/mobile/reglages-telephone'
import { EcranTourne } from './board/mobile/EcranTourne'
import { ciblesDeLaFeuille } from './board/mobile/cibles-feuille'
import { cibleAEchanger } from './board/mobile/echange-cible'
import { cartesPayantes } from './board/mobile/paiement-feuille'
import { useEstTablette, useMarqueTablette, useTabletteDebout } from './board/tablette/tablette'
import { CoucheAnimations } from './board/CoucheAnimations'
import { CoucheCharge } from './board/CoucheCharge'
import { CoucheRevelation } from './board/CoucheRevelation'
import { StatsPartie } from './board/StatsPartie'
import { CoucheMiseEnPlace, PlacesEnAttente, glisser, useMiseEnPlacePasAPas } from './board/CoucheMiseEnPlace'
import { attenteSurTable, avecFacesDAvant, mechantAttendLaQuestion, panneauAvantLaFile } from './board/mise-en-place-pas-a-pas'
import { CoucheTriche, useTriche } from './board/CoucheTriche'
import { installerSurvol, SELECTEUR_SURVOL_PLATEAU, useSons } from './board/sons'
import { useHaloStatut } from './board/halo-statut'
import { catalogueVide, chargerCatalogue, type Catalogue } from './board/catalogue'
import { extraireBoost, extraireCapacite, extraireEffetRevele } from './board/texte-capacite'
import type { InfoRevelee } from './board/vue-cartouche'
import { fusionnerDistribution, retenirCartesDistribuees, type DistribueesRetenues } from './board/frise-phase'
import { avecTableauDistribution } from './board/etapes-essai'
import { quitterPleinEcran } from './board/mobile/plein-ecran'
import {
  atterrir,
  fermerLaTable,
  laTablePeutAvoirEteFermee,
  lienAccueil,
  lireLeSite,
  natureDuDepart,
  type Site,
} from './board/quitter-la-table'
import { adresseApresPartie, estInviteDeTable, useRetourAuSalon } from './board/retour-salon'
import { estFenetreDeReaction } from './board/DemandeCentrale'
import {
  narrationAuCentre,
  questionDansLaScene,
  questionDansLePanneau,
  type EtatDeLaQuestion,
} from './board/ou-va-la-question'
import { mainVisibleForcee } from './board/main-visible'
import { TEXTES_FR } from './board/textes-fr'
import { TEXTES_FR_FANMADE } from './board/textes-fr-fanmade'
import { animationsDuPlateau, estResynchronisation } from './board/animations-en-scene'
import { autresFacesDe, kindOf, pvMaximum, scanUrl, toScanCard, type ContexteCarte } from './board/card-model'
import { cartesDuLotParOption, carteDeCampagneParOption, carteDuSchemaCampagneParOption, carteNommeeParOption, indexerCartesMondeParNom } from './board/option-carte'
import {
  DemandeCentrale,
  EvenementCentrale,
  demandeDoitApparaitreAuCentre,
  moteurAttendUneReponse,
} from './board/DemandeCentrale'
import { useHistoriquePartie } from './board/HistoriquePartie'
import { peutSuivre } from './board/suivi-vue'
import { deltasStatuts } from './board/effets-statuts'
import { phraseDeLEffet } from './board/phrases-effets'
import { ToastsEffetsCartes, type ToastEffet } from './board/ToastEffetCarte'
import { traduireMoteur } from './board/vocabulaire-moteur'
import {
  afficherFinDePartie,
  coupFatalLocal,
  DELAI_FILET_FIN_PARTIE_MS,
  finDePartie,
  herosLocaux,
} from './board/fin-partie'
import { installerCollecteErreurs } from './board/erreurs-console'
import { MessageRapport, useRapportBug } from './board/RapportBug'
import { PanneauBug } from './board/PanneauBug'
import { AttenteTable } from './board/AttenteTable'
import {
  joueurAttendu,
  joueurEnRetard,
  tablePartagee,
  useTableSilencieuse,
} from './board/attente-table'
import { BandeauAbsent } from './board/BandeauAbsent'
import { BandeauAnnonce } from './board/BandeauAnnonce'
import { BandeauMiseAJour } from './board/BandeauMiseAJour'
import { BilanObjectifs, PanneauObjectifs } from './board/PanneauObjectifs'
import { PanneauEnonce } from './board/PanneauEnonce'
import { CreateurPuzzle } from './board/CreateurPuzzle'
import { BoutonVoirLaTable } from './board/BoutonVoirLaTable'
import { useMiseAJour } from './board/maj'
import { cheminEmplacement, dossierSauvegardes } from './board/sauvegardes'
import { useAnnonce, usePassage } from './board/annonce'
import { JournalHeros } from './board/JournalHeros'
import { RecapPhaseMechant } from './board/RecapPhaseMechant'
import { CiblesScene } from './board/CiblesScene'
import { DeroulePhase } from './board/DeroulePhase'
import { BandeauPhase } from './board/BandeauPhase'
import { entreesPourRepli, etapesDeroule, etapesHorsPhase, nomNettoye, tempsDeLaQuestion } from './board/deroule-phase'
import { titreEtape } from './board/deroule-textes'
import { etapeEnLangue } from './board/etape-en-langue'
import { CoupHorsPhase, CoupHorsPhaseSurTable, DansLeCadre, EspaceDeLaQuestion } from './board/CoupHorsPhase'
import { CartoucheHorsPhase, RelectureJournal } from './board/CartouchePhase'
import type { QuestionDuMoteur } from './board/sous-cadre'
import './board/fin-partie-bd.css'
import './board/action-annulee.css'
import { useActionAnnulee } from './board/action-annulee'
import { choixEnAttente as choixAttend, groupeDeLaPile, ouvertureDePile, pileAOuvrirSeule, pilesToutesALaFois, type SorteDePile } from './board/pile-auto'
import './board/choix-en-attente.css'
import { RevuePhase } from './board/RevuePhase'
import { EditeurTable } from './board/EditeurTable'
import { DISPOSITION_DE_DEPART, DISPOSITION_ORIGINE, type Disposition } from './board/table-briques'
import { enregistrerDisposition, useDispositionTable } from './board/table-perso'
import { detailAttaqueComplet, ligneAttaqueConnue } from './board/ligne-attaque'
import { useCoupsEnVol } from './board/JetonsCoups'
import { avecCompteursFiges } from './board/coups-sur-table'
import { avecEcranStadeRevele, avecEtapesRiposte } from './board/etapes-essai'
import { avecFacesRencontreDuRecit, questionDuRecit, cartesAVenir, majInstantanes, mondeAvantEtape, mondeDeLaTable, sansCartesAVenir, type Instantanes } from './board/table-calee'
import {
  appliquerTeinte,
  chercherTeinteDuCompte,
  ecrireTeinte,
  envoyerTeinteAuCompte,
  lireTeinteDuNavigateur,
  type Teinte,
} from './board/teinte'
import { texteTempsParDecision } from './board/deroule-textes'
import { SplashTour } from './board/SplashTour'
import {
  CLE_AUTO_CIBLE,
  CLE_VALIDATION_COURTE,
  lireAutoCible,
  lireValidationCourte,
  useInteraction,
  type EtatInteractif,
  type SelectionPartagee,
} from './board/interaction'
import { publierVu, publierVuLimite, useVuDuJoueur } from './board/vu-partage'
import { poserVitre } from './board/vitre-spectateur'
import { CadreJoueur } from './board/CadreJoueur'
import { suivreDefilements, useDefilementsDuJoueur } from './board/defilement-partage'
import { phraseDuRefus } from './board/raisons-refus'
import { CoucheRefusEffets } from './board/refus-effets'
import { CoucheChoixUniques } from './board/choix-uniques'
import { MenuActionsCarte } from './board/MenuActionsCarte'
import { CiblageSurTable } from './board/TableSansModale'
import { FournisseurConfirmation, useConfirmation } from './board/ConfirmationJeu'
import { basculerLangue, langueActuelle, synchroniserLangueServeur, t } from './board/langue'
import { CLE_TEXTES_CDB, codeMarvelcdb, lireTextesCdb, texteMarvelcdb } from './board/marvelcdb'
import { nomAffiche } from './board/noms-cartes-fr'
import { libellePhase, libelleQuiAgit, libelleRound, nomDuHerosDuTour } from './board/etat-partie'
import { CLE_DESIGN_ESSAI, lireDesignEssai } from './board/design-essai'
import {
  NOM_OPTION_MANIGANCE,
  demandeHorsPanneauManigance,
  ouvertureEncoreVoilee,
  priseDuPanneauManigance,
  questionDeLaManigance,
} from './board/manigance-face-a'
import { PanneauManigance } from './board/PanneauManigance'
import { CLE_SCANS_FR, scansFrActifs } from './board/scans-fr'
import { ecrireDosCartes, lireDosCartes, type DosCartes } from './board/dos-cartes'
import {
  CoucheMeteo,
  CLE_METEO,
  EFFETS_DELAVANTS,
  effetsAffiches,
  type ApercuMeteo,
  lireMeteoActive,
  basculerAmbiance,
  ReglagesApercuAmbiance,
} from './board/CoucheMeteo'
import { ModaleAmbiance } from './board/ModaleAmbiance'
import { CoucheCurseurs, CLE_CURSEURS, lireCurseursActifs } from './board/CoucheCurseurs'
import { publierEtape, useSuiviDuJoueur } from './board/etape-partagee'
import { appliquerEtiquettesTable, lireEtiquettesTable } from './board/etiquettes-table'
import { BarreAvantage } from './board/BarreAvantage'
import { lecteurActif, estRelecture, type Lecteur } from './board/relecture/lecteur'
import { PageRelecture } from './board/relecture/PageRelecture'
import { PanneauRecompenses } from './board/campagne/PanneauRecompenses'
import { CLE_MUSIQUE, lireMusiqueActive, useMusique } from './board/musique'
import {
  Moteur,
  PHASES_DU_MECHANT,
  estMultijoueur,
  evenementNarreImportant,
  ecrireFinTourAuto,
  ecrireModePhaseMechant,
  ecrireReponseAmbiance,
  ecrireSauvegardeAuto,
  estSpectateur,
  libelleModePhase,
  lireFinTourAuto,
  lireModePhaseMechant,
  lireReponseAmbiance,
  lireSauvegardeAuto,
  migrerReglagesPhase,
  type EtatMoteur,
  type ModeActions,
  type ModePhaseMechant,
  type ModeRevelation,
  type ReponseAmbiance,
} from './board/moteur'
import { BarreSpectateur } from './board/BarreSpectateur'
import { FenetreReglages } from './board/FenetreReglages'
import { essaiPhaseMechant, essaisOuverts } from './board/essais'
import { PHASE_BIS_POUR_TOUS, lirePresentationPhase, phaseTrisUtilisable, suivrePresentationPhase } from './board/phase-presentation'
import { cadresDesJoueurs, joueurDeLaCarte } from './board/couleur-joueur'
import { VoletJournal } from './board/VoletJournal'
import { VoletVille } from './board/VoletVille'
import { VoletAssemblee } from './board/VoletAssemblee'
import { useAssembleeEnDirect } from './board/use-assemblee-en-direct'
import { VerdictAssembleeFin } from './board/VerdictAssembleeFin'
import { optionSeDeplacer, villeDuMonde } from './board/ville-etat'
import { JournalConsole } from './board/JournalConsole'
import {
  appliquerAffichage,
  chercherAffichageDuCompte,
  CLE_AFFICHAGE,
  ecrireAffichage,
  lireAffichage,
  retenirEpurePermis,
  type Affichage,
} from './board/affichage'
import { fondDe, identiteAffichee, identitesMechants, marqueDe, marqueMechantDe, palettes, type Couleur } from './board/halo-heros'
// CouchePasAPas et usePasAPas : DEBRANCHES a la demande de l'utilisateur, voir
// les commentaires a leurs points d'appel plus bas pour les rallumer.
import { SelecteurCibles } from './board/SelecteurCibles'
import { transformDecalage, useGlisserPanneau } from './board/placement/useGlisserPanneau'
import { installerGlisserPartout } from './board/placement/glisserPartout'
import { cibleDeLaTouche, SELECTEURS_BLOQUANTS } from './board/clavier-cartouche'
import { nomLisible, nomLisibleParlant } from './board/BarreAction'
import { construirePlateau, type Plateau } from './board/zones'
import type { Demande, Option, Reponse } from './board/ask'
import {
  chargerEtat,
} from './board/sources'
import { estRegardeePar, isScheme, isUnit, isVisibleFor, type World, type WorldCard } from './board/world'

/** Ce qui, ouvert par-dessus le plateau, garde Echap pour se fermer. */
const OUVERT_PAR_DESSUS = `${SELECTEURS_BLOQUANTS}, .plateau-regardees-voile, .menu-triche, .pile-triche, .pile-triche-voile, .volet-aide, .editeur-table-barre, .modale-menu, .reglages-fond`

// Migration EXPLICITE des anciens reglages de la phase du mechant (voir
// moteur.ts, `migrerReglagesPhase`), faite UNE FOIS, ici, a l'evaluation du
// module. C'est le plus tot possible : avant meme le montage du composant,
// donc forcement avant les `useState(lireModePhaseMechant)` /
// `useState(lireAvanceAuto)` plus bas, qui n'appellent leur lecteur qu'a
// l'initialisation du premier rendu. Un appel loge dans le corps du composant
// aurait couru un risque inutile (React StrictMode invoque deux fois le corps
// du composant en developpement), alors qu'ici l'evaluation du module n'a
// lieu qu'une fois par chargement de page - et la fonction est de toute facon
// sans effet des la deuxieme fois (elle ne fait rien si la cle porte deja une
// valeur du nouveau schema).
migrerReglagesPhase()

/** L'ancien plateau. Le serveur sert marvel.html des que l'adresse a une query. */

/** Table pas encore decoupee : aucune carte dessinee. */
const AUCUN_ID: Set<number> = new Set()
const CLE_MODE_ACTIONS = 'marvel-board-action-mode'
const CLE_ANIMATIONS = 'marvel-board-animations'

// `ModeActions` et `ModeRevelation` vivent dans board/moteur.ts (14/09/2026) :
// la fenetre des reglages en a besoin et ne peut pas importer ce fichier.

function lireModeActions(): ModeActions {
  try {
    return window.localStorage.getItem(CLE_MODE_ACTIONS) === 'detailed' ? 'detailed' : 'simple'
  } catch {
    return 'simple'
  }
}

/** Animations de deplacement activees ? Par defaut oui, sauf choix contraire. */
function lireAnimations(): boolean {
  try {
    return window.localStorage.getItem(CLE_ANIMATIONS) !== 'off'
  } catch {
    return true
  }
}

const CLE_SONS = 'marvel-board-sons'
const CLE_REVELATION = 'marvel-board-revelation'

/** Sons du moteur actifs ? Par defaut oui, comme le client d'origine. */
function lireSons(): boolean {
  try {
    return window.localStorage.getItem(CLE_SONS) !== 'off'
  } catch {
    return true
  }
}

const DUREES_REVELATION: Record<ModeRevelation, number> = { off: 0, court: 2600, long: 5000 }

function lireRevelation(): ModeRevelation {
  try {
    const valeur = window.localStorage.getItem(CLE_REVELATION)
    return valeur === 'off' || valeur === 'long' ? valeur : 'court'
  } catch {
    return 'court'
  }
}

function parametres() {
  const url = new URLSearchParams(window.location.search)
  const joueur = Number(url.get('p') ?? '0')
  return {
    etat: url.get('etat'),
    playerId: Number.isInteger(joueur) && joueur >= 0 ? joueur : 0,
    /** On REGARDE cette partie sans y jouer. Voir `estSpectateur` (moteur.ts). */
    spectateur: url.has('spectateur'),
  }
}

function messageDErreur(cause: unknown): string {
  return cause instanceof Error ? cause.message : String(cause)
}

/** Nom d'une carte du monde, par identifiant d'objet. Pour situer une action. */
function nomDeCarte(world: World | undefined, id: number): string | undefined {
  if (!world || id === 0) return undefined
  let trouve: string | undefined
  const parcourir = (valeur: unknown) => {
    if (trouve !== undefined) return
    if (Array.isArray(valeur)) {
      for (const element of valeur) parcourir(element)
      return
    }
    if (typeof valeur !== 'object' || valeur === null) return
    const objet = valeur as Record<string, unknown>
    if (objet.id === id && typeof objet.name === 'string') {
      trouve = objet.name
      return
    }
    for (const enfant of Object.values(objet)) parcourir(enfant)
  }
  parcourir(world)
  return trouve
}

function indexerCartesMonde(world: World | undefined): Map<number, WorldCard> {
  const index = new Map<number, WorldCard>()
  if (!world) return index

  const parcourir = (valeur: unknown) => {
    if (Array.isArray(valeur)) {
      for (const element of valeur) parcourir(element)
      return
    }
    if (typeof valeur !== 'object' || valeur === null) return
    const objet = valeur as Partial<WorldCard>
    if (typeof objet.id === 'number' && typeof objet.card_type === 'string') {
      index.set(objet.id, objet as WorldCard)
    }
    for (const enfant of Object.values(objet)) parcourir(enfant)
  }

  parcourir(world)
  return index
}

function valeurCompteur(carte: WorldCard, cle: 'health' | 'k_threat'): number | undefined {
  const valeur = carte.info[cle]
  return typeof valeur === 'number' && Number.isFinite(valeur) ? valeur : undefined
}

/**
 * Le premier compteur nomme (`c_rage`, `k_acceleration_token`) dont la valeur a
 * change d'un rendu a l'autre. Un compteur qui apparait part de zero.
 */
function changementDeJeton(avant: WorldCard, apres: WorldCard): { cle: string; variation: number } | undefined {
  const lire = (carte: WorldCard, champ: string) => {
    const v = carte.info[champ]
    return typeof v === 'number' && Number.isFinite(v) ? v : 0
  }
  const champs = new Set([...Object.keys(avant.info), ...Object.keys(apres.info)])
  for (const champ of champs) {
    const nomme = champ.startsWith('c_') && !champ.endsWith('_printed')
    if (!nomme && champ !== 'k_acceleration_token') continue
    const variation = lire(apres, champ) - lire(avant, champ)
    if (variation !== 0) return { cle: champ === 'k_acceleration_token' ? 'acceleration' : champ.slice(2), variation }
  }
  return undefined
}

/** Capture les variations de compteurs entre deux rendus du moteur. */
function useEffetsCartes(monde: World | undefined): Map<number, CardEffectDelta> {
  const [effets, setEffets] = useState<Map<number, CardEffectDelta>>(() => new Map())
  const precedent = useRef<World | undefined>(undefined)
  const minuteurs = useRef(new Map<number, number>())

  useEffect(() => {
    if (!monde) return
    const avant = precedent.current
    if (avant) {
      const precedentes = indexerCartesMonde(avant)
      const courantes = indexerCartesMonde(monde)
      const changements: Array<[number, CardEffectDelta]> = []

      for (const [id, carte] of courantes) {
        const ancienne = precedentes.get(id)
        if (!ancienne) continue
        const vieAvant = valeurCompteur(ancienne, 'health')
        const vieApres = valeurCompteur(carte, 'health')
        if (vieAvant !== undefined && vieApres !== undefined && vieAvant !== vieApres) {
          changements.push([id, { value: vieApres - vieAvant, kind: vieApres < vieAvant ? 'damage' : 'heal' }])
          continue
        }
        const menaceAvant = valeurCompteur(ancienne, 'k_threat')
        const menaceApres = valeurCompteur(carte, 'k_threat')
        if (menaceAvant !== undefined && menaceApres !== undefined && menaceAvant !== menaceApres) {
          changements.push([id, { value: menaceApres - menaceAvant, kind: 'threat' }])
          continue
        }
        // Des JETONS nommes (rage, toile...) poses ou retires : le toast dit
        // « X gagne 1 jeton Rage », pas « gagne 1 menace ».
        const jeton = changementDeJeton(ancienne, carte)
        if (jeton) changements.push([id, { kind: 'token', jeton: jeton.cle, value: jeton.variation }])
      }

      // Statuts poses ou retires (Sonne / Desoriente / Tenace). Un porteur
      // n'a qu'un badge a la fois : si sa vie ou sa menace a bouge dans le
      // meme rendu, ce chiffre garde la place, le statut se lit sur la
      // mini-carte. Voir effets-statuts.ts.
      const dejaSignales = new Set(changements.map(([id]) => id))
      for (const [id, delta] of deltasStatuts(precedentes, courantes)) {
        if (!dejaSignales.has(id)) changements.push([id, delta])
      }

      if (changements.length > 0) {
        setEffets((courants) => {
          const suivants = new Map(courants)
          for (const [id, effet] of changements) {
            const ancienMinuteur = minuteurs.current.get(id)
            if (ancienMinuteur !== undefined) window.clearTimeout(ancienMinuteur)
            suivants.set(id, effet)
            const minuteur = window.setTimeout(() => {
              setEffets((actuels) => {
                if (actuels.get(id) !== effet) return actuels
                const sans = new Map(actuels)
                sans.delete(id)
                return sans
              })
              minuteurs.current.delete(id)
            }, 1700)
            minuteurs.current.set(id, minuteur)
          }
          return suivants
        })
      }
    }
    precedent.current = monde
  }, [monde, monde?.render_id])

  useEffect(
    () => () => {
      for (const minuteur of minuteurs.current.values()) window.clearTimeout(minuteur)
    },
    []
  )

  return effets
}

function indexerCartesAffichees(plateau: Plateau | undefined): Map<number, ScanCardProps> {
  const index = new Map<number, ScanCardProps>()
  if (!plateau) return index
  for (const emplacement of plateau.emplacements) {
    for (const groupe of emplacement.groupes) {
      for (const unite of groupe) {
        index.set(Number(unite.carte.id), unite.carte)
        for (const attachee of unite.attachees) index.set(Number(attachee.id), attachee)
      }
    }
  }
  return index
}

function optionAvecCibles(option: Option | undefined): option is Option {
  return option !== undefined && option.target_num_range[1] > 0 && option.all_legal_targets.length > 0
}

function idsPulsePourOption(
  option: Option | undefined,
  plateau: Plateau | undefined,
  cibleVerrouillee?: number
): Set<number> {
  const ids = new Set<number>()
  if (!optionAvecCibles(option) || !plateau) return ids
  if (option.bind_id !== 0 && plateau.idsAffiches.has(option.bind_id)) ids.add(option.bind_id)
  if (cibleVerrouillee !== undefined) {
    if (plateau.idsAffiches.has(cibleVerrouillee)) {
      ids.add(cibleVerrouillee)
      return ids
    }
    const representant = plateau.representantsDePile.get(cibleVerrouillee)
    if (representant !== undefined) ids.add(representant)
    return ids
  }
  for (const cible of new Set(option.all_legal_targets)) {
    if (plateau.idsAffiches.has(cible)) {
      ids.add(cible)
      continue
    }
    const representant = plateau.representantsDePile.get(cible)
    if (representant !== undefined) ids.add(representant)
  }
  return ids
}

/**
 * Pendant l'activation ennemie, le moteur laisse les cartes impliquees dans
 * le prompt sous la forme [(id, card_id) Nom]. On les met toutes en evidence
 * pour que la relation source/cible reste lisible sans ouvrir une action.
 */
function idsPulsePourDemandeEnnemie(
  monde: World | undefined,
  demande: Demande | undefined,
  plateau: Plateau | undefined
): Set<number> {
  const ids = new Set<number>()
  if (!monde || !plateau || monde.phase !== 'Enemy Activation') return ids

  const texte = [monde.prompt, monde.prompt_last_text, demande?.prompt_text]
    .filter((valeur): valeur is string => typeof valeur === 'string')
    .join(' ')
  const references = [...texte.matchAll(/\[\(\s*(\d+)\s*,/g)]
    .map((correspondance) => Number(correspondance[1]))
    .filter((id) => Number.isFinite(id))

  // Les prompts d'activation contiennent normalement toutes les cartes liees.
  // Le repli couvre les demandes techniques dont le texte ne porte pas de
  // references, en reutilisant les porteurs et leurs cibles legales.
  const candidats = references.length > 0
    ? references
    : demande?.options.flatMap((option) => [option.bind_id, ...option.all_legal_targets]) ?? []

  for (const id of new Set(candidats)) {
    if (id <= 0) continue
    if (plateau.idsAffiches.has(id)) {
      ids.add(id)
      continue
    }
    const representant = plateau.representantsDePile.get(id)
    if (representant !== undefined) ids.add(representant)
  }
  return ids
}

/** Ce qu'on fait dans la pile qui tient cette carte, dit sur la pile elle-même. */
function libelleDeLaPile(id: number, monde: World | undefined): string {
  const dans = (cartes: readonly WorldCard[] | undefined) => cartes?.some((c) => c.id === id) ?? false
  if (dans(monde?.encounter_discard_pile)) return t('Chercher dans la défausse rencontre')
  if (dans(monde?.encounter_deck)) return t('Chercher dans le paquet rencontre')
  for (const joueur of monde?.players ?? []) {
    if (dans(joueur.player_discard_pile) || dans(joueur.additional_discard_pile)) return t('Prendre dans la défausse')
    if (dans(joueur.player_deck) || dans(joueur.additional_deck)) return t('Chercher dans le deck')
  }
  return t('Ouvrir la pile')
}

/** La nature de la pile qui tient cette carte (deck, defausse, paquet ou defausse rencontre), pour l'intitule d'un groupe. */
function sorteDePile(id: number, monde: World | undefined): SorteDePile {
  const dans = (cartes: readonly WorldCard[] | undefined) => cartes?.some((c) => c.id === id) ?? false
  if (dans(monde?.encounter_discard_pile)) return 'defausse-rencontre'
  if (dans(monde?.encounter_deck)) return 'rencontre'
  for (const joueur of monde?.players ?? []) {
    if (dans(joueur.player_discard_pile) || dans(joueur.additional_discard_pile)) return 'defausse'
    if (dans(joueur.player_deck) || dans(joueur.additional_deck)) return 'deck'
  }
  return 'autre'
}

function ciblesHorsTablePourOption(
  option: Option,
  cartesParId: Map<number, WorldCard>,
  plateau: Plateau,
  playerId: number,
  catalogue: Catalogue
): ScanCardProps[] {
  const cartes: ScanCardProps[] = []
  for (const id of new Set(option.all_legal_targets)) {
    if (plateau.idsAffiches.has(id)) continue
    const carte = cartesParId.get(id)
    if (!carte) continue
    const visible = isVisibleFor(carte, playerId) || option.is_search
    cartes.push(
      toScanCard(
        visible ? { ...carte, visible_for_players: [playerId], is_face_up: true } : carte,
        { playerId, actives: new Set(), catalogue }
      )
    )
  }
  return cartes
}

function optionDisponible(option: Option): boolean {
  return option.failure_reason === ''
}

function optionsDisponiblesVersCible(options: Option[], cible: number): Option[] {
  return options.filter(
    (option) =>
      optionDisponible(option) &&
      option.target_num_range[1] > 0 &&
      option.all_legal_targets.includes(cible)
  )
}

function estCibleExpliquee(carte: WorldCard | undefined): boolean {
  if (!carte) return false
  return isScheme(carte) || carte.card_type === 'EncounterVillain' || carte.card_type === 'Minion'
}

function ajouterPulse(
  interactifs: Map<number, EtatInteractif>,
  ids: Set<number>
): Map<number, EtatInteractif> {
  if (ids.size === 0) return interactifs
  const resultat = new Map(interactifs)
  for (const id of ids) {
    const courant = resultat.get(id)
    if (courant) {
      resultat.set(id, { ...courant, pulse: true })
      continue
    }
    resultat.set(id, { role: 'cible-preview', choisie: false, pulse: true })
  }
  return resultat
}

type GroupeCartesRegardees = {
  cle: string
  titre: string
  cartes: ScanCardProps[]
}

function cartesRegardeesDansPile(
  cle: string,
  titre: string,
  pile: readonly WorldCard[] | undefined,
  contexte: ContexteCarte
): GroupeCartesRegardees | undefined {
  if (!Array.isArray(pile)) return undefined

  // REGARDEES, pas seulement connues (rapport Yarro n85) : voir `estRegardeePar`.
  const visibles = pile.filter(
    (carte) => estRegardeePar(carte, contexte.playerId) && !carte.is_face_up
  )
  if (visibles.length <= 1) return undefined

  return {
    cle,
    titre,
    cartes: visibles.map((carte) => toScanCard(carte, contexte)),
  }
}

function cartesRegardees(
  world: World,
  playerId: number,
  catalogue: Catalogue
): GroupeCartesRegardees[] {
  const contexte: ContexteCarte = {
    playerId,
    actives: new Set(world.active_card_ids ?? []),
    catalogue,
  }
  const groupes: Array<GroupeCartesRegardees | undefined> = [
    cartesRegardeesDansPile('rencontre', 'Encounter deck', world.encounter_deck, contexte),
    cartesRegardeesDansPile('vilain', 'Villain deck', world.villain_deck, contexte),
    cartesRegardeesDansPile('complot', 'Main scheme deck', world.main_schemes_deck, contexte),
  ]

  for (const [index, joueur] of (world.players ?? []).entries()) {
    groupes.push(
      cartesRegardeesDansPile(
        `joueur-${index}`,
        index === playerId ? 'Your deck' : `Player ${index + 1} deck`,
        joueur.player_deck,
        contexte
      )
    )
    // PAS le deck supplementaire. Cette fenetre annonce une revelation
    // PASSAGERE — « tu regardes les 2 premieres cartes ». Or un deck
    // supplementaire est une zone PERMANENTE dont le proprietaire connait le
    // contenu : les ecureuils de Squirrel Girl sont visibles pour elle tout en
    // restant face cachee, ce qui remplissait la condition en permanence. La
    // fenetre etait donc perpetuellement due, et se rouvrait des qu'un ecureuil
    // etait depense ou rendu, puisqu'elle ne retient que le lot exact qu'on
    // vient de fermer. On consulte ce deck en cliquant la pile, comme les
    // autres.
    groupes.push(
      cartesRegardeesDansPile(
        `joueur-${index}-mise-de-cote`,
        index === playerId ? 'Your set-aside deck' : `Player ${index + 1} set-aside deck`,
        joueur.set_aside_deck,
        contexte
      )
    )
  }

  for (const [index, deck] of (world.additional_decks ?? []).entries()) {
    groupes.push(
      cartesRegardeesDansPile(`deck-supplementaire-${index}`, `Additional deck ${index + 1}`, deck, contexte)
    )
  }

  return groupes.filter((groupe): groupe is GroupeCartesRegardees => groupe !== undefined)
}

function signatureCartesRegardees(groupes: GroupeCartesRegardees[]): string {
  return groupes
    .map((groupe) => `${groupe.cle}:${groupe.cartes.map((carte) => carte.id).join(',')}`)
    .join('|')
}

function ModaleCartesRegardees({ groupes }: { groupes: GroupeCartesRegardees[] }) {
  const signature = useMemo(() => signatureCartesRegardees(groupes), [groupes])
  const [signatureFermee, setSignatureFermee] = useState<string | undefined>(undefined)
  const [apercuId, setApercuId] = useState<string | null>(null)

  const cartesParId = useMemo(() => {
    const index = new Map<string, ScanCardProps>()
    for (const groupe of groupes) {
      for (const carte of groupe.cartes) index.set(carte.id, carte)
    }
    return index
  }, [groupes])

  const pointerCarte = useCallback((cible: EventTarget | null) => {
    if (!(cible instanceof HTMLElement)) {
      setApercuId(null)
      return
    }
    const carte = cible.closest<HTMLElement>('.scan-card')
    setApercuId(carte?.dataset.cardId ?? null)
  }, [])

  const survoler = useCallback(
    (evenement: ReactMouseEvent<HTMLElement>) => pointerCarte(evenement.target),
    [pointerCarte]
  )

  const focaliser = useCallback(
    (evenement: ReactFocusEvent<HTMLElement>) => pointerCarte(evenement.target),
    [pointerCarte]
  )

  const perdreFocus = useCallback((evenement: ReactFocusEvent<HTMLElement>) => {
    const prochaine = evenement.relatedTarget
    if (prochaine instanceof Node && evenement.currentTarget.contains(prochaine)) return
    setApercuId(null)
  }, [])

  useEffect(() => {
    if (!signature) setSignatureFermee(undefined)
  }, [signature])

  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »). Les hooks se declarent AVANT
  // le retour anticipe ci-dessous.
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(signature)

  if (!signature || signatureFermee === signature) return null

  const total = groupes.reduce((somme, groupe) => somme + groupe.cartes.length, 0)
  const carteApercu = apercuId ? cartesParId.get(apercuId) : undefined

  return (
    <div className="plateau-regardees-voile">
      <section
        className="plateau-regardees"
        role="dialog"
        aria-label={t('Cartes regardées')}
        style={transformDecalage(decalage)}
        onMouseOver={survoler}
        onMouseLeave={() => setApercuId(null)}
        onFocus={focaliser}
        onBlur={perdreFocus}
      >
        <header className="plateau-regardees-entete">
          <div
            className="poignee-glisser"
            onPointerDown={gestesGlisser.onPointerDown}
            onPointerMove={gestesGlisser.onPointerMove}
            onPointerUp={gestesGlisser.onPointerUp}
            onPointerCancel={gestesGlisser.onPointerCancel}
          >
            <span className="plateau-eyebrow">{t('Cartes regardées')}</span>
            <strong>
              {total} card{total > 1 ? 's' : ''}
            </strong>
          </div>
          <button type="button" onClick={() => setSignatureFermee(signature)}>
            {t('Fermer')}
          </button>
        </header>

        <div className="plateau-regardees-corps">
          {groupes.map((groupe) => (
            <section className="plateau-regardees-groupe" key={groupe.cle}>
              <h2>
                {groupe.titre} · {groupe.cartes.length}
              </h2>
              <div className="plateau-regardees-cartes">
                {groupe.cartes.map((carte) => (
                  <ScanCard {...carte} key={carte.id} />
                ))}
              </div>
            </section>
          ))}
        </div>
      </section>
      {carteApercu ? <CarteApercu carte={carteApercu} /> : null}
    </div>
  )
}

function ModaleCiblesMenu({
  titre,
  cartes,
  fermer,
}: {
  titre: string
  cartes: ScanCardProps[]
  fermer: () => void
}) {
  const [apercuId, setApercuId] = useState<string | null>(null)

  const cartesParId = useMemo(() => {
    const index = new Map<string, ScanCardProps>()
    for (const carte of cartes) index.set(carte.id, carte)
    return index
  }, [cartes])

  const pointerCarte = useCallback((cible: EventTarget | null) => {
    if (!(cible instanceof HTMLElement)) {
      setApercuId(null)
      return
    }
    const carte = cible.closest<HTMLElement>('.scan-card')
    setApercuId(carte?.dataset.cardId ?? null)
  }, [])

  const survoler = useCallback(
    (evenement: ReactMouseEvent<HTMLElement>) => pointerCarte(evenement.target),
    [pointerCarte]
  )

  const focaliser = useCallback(
    (evenement: ReactFocusEvent<HTMLElement>) => pointerCarte(evenement.target),
    [pointerCarte]
  )

  const perdreFocus = useCallback((evenement: ReactFocusEvent<HTMLElement>) => {
    const prochaine = evenement.relatedTarget
    if (prochaine instanceof Node && evenement.currentTarget.contains(prochaine)) return
    setApercuId(null)
  }, [])

  useEffect(() => {
    const fermerClavier = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') fermer()
    }
    document.addEventListener('keydown', fermerClavier)
    return () => document.removeEventListener('keydown', fermerClavier)
  }, [fermer])

  const carteApercu = apercuId ? cartesParId.get(apercuId) : undefined
  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »).
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(`${titre}|${cartes.map((c) => c.id).join(',')}`)

  return (
    <div className="plateau-regardees-voile plateau-cibles-menu-voile" onPointerDown={fermer}>
      <section
        className="plateau-regardees plateau-cibles-menu"
        role="dialog"
        aria-label="Possible off-table targets"
        style={transformDecalage(decalage)}
        onPointerDown={(evenement) => evenement.stopPropagation()}
        onMouseOver={survoler}
        onMouseLeave={() => setApercuId(null)}
        onFocus={focaliser}
        onBlur={perdreFocus}
      >
        <header className="plateau-regardees-entete">
          <div
            className="poignee-glisser"
            onPointerDown={gestesGlisser.onPointerDown}
            onPointerMove={gestesGlisser.onPointerMove}
            onPointerUp={gestesGlisser.onPointerUp}
            onPointerCancel={gestesGlisser.onPointerCancel}
          >
            <span className="plateau-eyebrow">{t('Cibles possibles')}</span>
            <strong>
              {titre} - {cartes.length} card{cartes.length > 1 ? 's' : ''}
            </strong>
          </div>
          <button type="button" onClick={fermer}>
            {t('Fermer')}
          </button>
        </header>
        {/* Cette fenetre MONTRE les cartes que l'action pourrait viser ; elle n'en choisit aucune (rapport du 26/10/2026 :
            on y cliquait un sbire en croyant le choisir). */}
        <p className="plateau-cibles-menu-note">
          {t('Aperçu seulement : pour choisir une carte, lance l’action puis clique sur la pile.')}
        </p>
        <div className="plateau-regardees-corps">
          <div className="plateau-regardees-cartes">
            {cartes.map((carte) => (
              <ScanCard {...carte} key={carte.id} />
            ))}
          </div>
        </div>
      </section>
      {carteApercu ? <CarteApercu carte={carteApercu} /> : null}
    </div>
  )
}

/**
 * Outils de la barre du haut : le mode d'affichage des actions, et rien de plus.
 *
 * Trois autres commandes y vivaient et en sont parties : le selecteur d'etats
 * enregistres, le champ « joueur affiche » et le lien vers l'ancien plateau.
 * Toutes occupaient une place permanente en haut de l'ecran — celle qui manque
 * a la table — pour des usages rares ou deja couverts ailleurs.
 *
 * AUCUNE FONCTION N'A DISPARU, seulement les raccourcis :
 *  - un etat enregistre se charge par `?etat=<fichier>` ;
 *  - le siege regarde se choisit par `?p=<joueur>`, et en hot-seat la vue suit
 *    de toute facon le joueur que le moteur interroge ;
 *  - l'ancien plateau reste servi a la racine, `/?p=<joueur>`.
 * Les trois passent par parametres(), qui lit l'adresse et n'a pas bouge.
 */
function Outils({
  modeActions,
  changerModeActions,
}: {
  modeActions: ModeActions
  changerModeActions: (mode: ModeActions) => void
}) {
  return <ModeActionsBoutons modeActions={modeActions} changerModeActions={changerModeActions} />
}

/**
 * Le choix Simple / Detaille.
 *
 * Compose a part parce qu'il se pose a DEUX endroits selon la vue : dans le
 * groupe des reglages de la barre en partie, et seul dans la barre de la vue
 * « etat enregistre », qui n'a pas d'actions de partie. Une seule definition,
 * deux placements.
 */
function ModeActionsBoutons({
  modeActions,
  changerModeActions,
}: {
  modeActions: ModeActions
  changerModeActions: (mode: ModeActions) => void
}) {
  return (
    <div className="mode-actions" role="group" aria-label={t('Mode d’affichage des actions')}>
      <button
        type="button"
        className={modeActions === 'simple' ? 'est-actif' : ''}
        onClick={() => changerModeActions('simple')}
      >
        Simple
      </button>
      <button
        type="button"
        className={modeActions === 'detailed' ? 'est-actif' : ''}
        onClick={() => changerModeActions('detailed')}
      >
        {t('Détaillé')}
      </button>
    </div>
  )
}

/** Un etat enregistre : chargement unique, aucune interaction. */
function useEtatEnregistre(fichier: string) {
  const [monde, setMonde] = useState<World | undefined>(undefined)
  const [erreur, setErreur] = useState<string | undefined>(undefined)

  useEffect(() => {
    let vivant = true
    setMonde(undefined)
    setErreur(undefined)
    chargerEtat(fichier)
      .then((nouveau) => {
        if (vivant) setMonde(nouveau)
      })
      .catch((cause: unknown) => {
        if (vivant) setErreur(messageDErreur(cause))
      })
    return () => {
      vivant = false
    }
  }, [fichier])

  return { monde, erreur }
}

/** La partie en cours : socket, accuse de reception, demandes du moteur. */
function usePartieEnCours(playerId: number) {
  // En relecture, le lecteur tient la place du moteur (relecture/lecteur.ts).
  const [moteur] = useState<Moteur | Lecteur>(() => lecteurActif() ?? new Moteur(playerId))
  const [etat, setEtat] = useState<EtatMoteur>({
    hautsFaits: [],
    siegesAbsents: [],
    // Zero, c'est-a-dire « sans limite » : c'est le defaut du moteur, et la
    // seule valeur qui ne raconte rien de faux avant la premiere trame.
    maxTimeout: 0,
    aNous: false,
    connecte: false,
    validationRequise: false,
    tentatives: 0,
  })

  useEffect(() => {
    const arreter = moteur.ecouter(setEtat)
    moteur.demarrer()
    return () => {
      arreter()
      moteur.arreter()
    }
  }, [moteur])

  const repondre = useCallback(
    // Rend `true` quand la reponse EST PARTIE (voir `Moteur.repondre`) : le
    // panneau de la manigance rouvre son bouton sur ce fait quand l'envoi
    // echoue. Les autres appelants ignorent ce retour, comme avant.
    (reponse: Reponse | null, bindPlayerId: number) => moteur.repondre(reponse, bindPlayerId),
    [moteur]
  )

  // STABLES d'un rendu a l'autre, et ce n'est pas un detail de style : le
  // plateau se redessine a chaque trame du moteur, et `reglerModePhase` est
  // la dependance d'un effet (plus bas) qui redit le mode au moteur. Recreee a
  // chaque rendu, elle relancait cet effet a chaque trame — et
  // `setModePhaseMechant` relachait alors la trame retenue. Mesure en partie
  // reelle le 07/09/2026 : la phase du mechant entiere defilait sans un clic.
  const continuer = useCallback(() => moteur.continuer(), [moteur])
  const reconnecter = useCallback(() => moteur.reconnecterMaintenant(), [moteur])
  const reglerModePhase = useCallback(
    (mode: ModePhaseMechant) => moteur.setModePhaseMechant(mode),
    [moteur]
  )
  const avancerPasAPas = useCallback(() => moteur.avancerMaintenant(), [moteur])
  // Le joueur a agi sur le cartouche, meme quand cela ne relache aucune trame :
  // le filet anti-blocage, qui mesure une INACTIVITE, doit repartir de zero.
  const signalerActivite = useCallback(() => moteur.signalerActiviteDuJoueur(), [moteur])

  return {
    etat,
    repondre,
    continuer,
    reconnecter,
    reglerModePhase,
    // Branche sur le cartouche du deroule detaille (DeroulePhase, plus bas) :
    // c'est lui qui relache le moteur, etape par etape, et lui seul. L'avance
    // auto est retiree (pas a pas strict) : le moteur n'a plus d'horloge.
    avancerPasAPas,
    signalerActivite,
  }
}

/** Metadonnees d'un emplacement de sauvegarde, via /get_replay_json. */
type MetaSauvegarde = { villain?: string; step?: number; time?: string }

async function lireMetaSauvegarde(nom: string): Promise<MetaSauvegarde | undefined> {
  try {
    const reponse = await fetch(`/get_replay_json?${nom}`, { cache: 'no-store' })
    if (!reponse.ok) return undefined
    const brut = (await reponse.json()) as MetaSauvegarde
    return typeof brut === 'object' && brut !== null ? brut : undefined
  } catch {
    return undefined
  }
}

/**
 * Popover de sauvegardes : 3 emplacements nommes (save_1..3.json, comme le
 * client original), chacun avec Save / Load, plus l'export en fichier.
 * Les fichiers vivent dans replays/ (hors .game : ils survivent aux rebuilds).
 *
 * ⚠ LE DOSSIER VIENT DU MOTEUR, ET JAMAIS D'ICI (correctif du 13/09/2026).
 * Ce fichier ecrivait « ../replays/save_1.json » en dur : le dossier COMMUN,
 * le meme pour tout le monde. Sur un serveur a vingt places, les trois
 * emplacements etaient donc PARTAGES entre tous les comptes — chacun ecrasait
 * la sauvegarde du voisin et chargeait des parties qu'il n'avait jamais
 * jouees. La configuration disait pourtant la verite depuis toujours
 * (`replay_folders`, separe par place) ; c'est le client qui inventait un
 * chemin au lieu de la lire. Il la demande maintenant a
 * `/get_dossier_sauvegardes`.
 */

/**
 * ⌂ Menu (24/09/2026) : FUSION de deux boutons distincts (« Menu » et
 * « Déconnexion complète »), demande de l'utilisateur apres avoir vu les deux
 * actions confondues sur le meme ecran (capture a l'appui). Un choix, pas un
 * clic direct -- `retourMenu` (navigation douce, sans consequence) et
 * `retourMenuPrincipal` (ferme la table, avec SA PROPRE confirmation
 * detaillee juste apres, cf. commentaire au-dessus de sa definition) restent
 * INTACTS : cette modale ne fait que choisir lequel appeler, elle n'ajoute
 * pas une seconde confirmation devant celle qui existe deja.
 */
function ModaleMenu({
  ouvert,
  fermer,
  retourMenu,
  retourMenuPrincipal,
}: {
  ouvert: boolean
  fermer: () => void
  retourMenu: () => void
  retourMenuPrincipal: () => void
}) {
  useEffect(() => {
    if (!ouvert) return
    const surTouche = (e: KeyboardEvent) => {
      if (e.key === 'Escape') fermer()
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [ouvert, fermer])
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(ouvert ? 'menu-ouvert' : 'menu-ferme')
  if (!ouvert) return null
  return (
    <div
      className="reglages-fond"
      role="presentation"
      onClick={(e) => {
        if (e.target === e.currentTarget) fermer()
      }}
    >
      <div
        className="reglages-fenetre sans-onglets modale-menu"
        role="dialog"
        aria-modal="true"
        aria-label={t('Menu')}
        style={transformDecalage(decalage)}
      >
        <header className="reglages-tete">
          <h2
            className="poignee-glisser"
            onPointerDown={gestesGlisser.onPointerDown}
            onPointerMove={gestesGlisser.onPointerMove}
            onPointerUp={gestesGlisser.onPointerUp}
            onPointerCancel={gestesGlisser.onPointerCancel}
          >
            {t('Menu')}
          </h2>
          <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
            ×
          </button>
        </header>
        <div className="reglages-contenu modale-menu-choix">
          <button
            type="button"
            className="bh-bouton bh-menu"
            onClick={() => {
              fermer()
              retourMenu()
            }}
            title={t('Revenir au menu principal')}
          >
            <span aria-hidden="true">⌂</span> {t('Retour au menu')}
          </button>
          <button
            type="button"
            className="bh-bouton bh-fermer-table"
            onClick={() => {
              fermer()
              retourMenuPrincipal()
            }}
            title={t('Fermer et déconnecter la table (surtout pour le multijoueur en ligne)')}
          >
            <span aria-hidden="true">⏻</span>{' '}
            {t('Déconnexion complète (surtout multijoueur en ligne)')}
          </button>
        </div>
      </div>
    </div>
  )
}

function PopoverSauvegardes() {
  const confirmer = useConfirmation()
  // Les fenetres se glissent de partout, hors boutons, cartes et champs (voir placement/glisserPartout.ts).
  useEffect(() => installerGlisserPartout(), [])
  const [ouvert, setOuvert] = useState(false)
  const [metas, setMetas] = useState<Record<number, MetaSauvegarde | undefined>>({})
  const [occupe, setOccupe] = useState<string | undefined>(undefined)

  const rafraichir = useCallback(() => {
    for (const slot of [1, 2, 3]) {
      void cheminEmplacement(slot)
        .then((chemin) => lireMetaSauvegarde(chemin))
        .then((meta) => setMetas((m) => ({ ...m, [slot]: meta })))
    }
  }, [])

  const basculer = useCallback(() => {
    setOuvert((o) => {
      if (!o) rafraichir()
      return !o
    })
  }, [rafraichir])

  const sauverSlot = useCallback(
    (slot: number) => {
      setOccupe(`save-${slot}`)
      // Chemin EXPLICITE (la commande /save ecrirait sinon dans le repertoire
      // courant, detruit a chaque reconstruction), mais DEMANDE AU MOTEUR :
      // c'est lui qui sait quel dossier appartient a cette table.
      void cheminEmplacement(slot)
        .then((chemin) => fetch(`/debug?/save ${chemin}`))
        .then(() => window.setTimeout(rafraichir, 600))
        .catch(() => undefined)
        .finally(() => setOccupe(undefined))
    },
    [rafraichir]
  )

  const chargerSlot = useCallback(async (slot: number) => {
    const accepte = await confirmer({
      titre: `${t('Charger la sauvegarde')} ${slot} ?`,
      texte: t('La partie en cours sera remplacée.'),
      confirmer: t('Charger'),
      ton: 'danger',
    })
    if (!accepte) return
    setOccupe(`load-${slot}`)
    // `:-1` = reprendre au DERNIER pas enregistre (semantique du client original).
    void cheminEmplacement(slot)
      .then((chemin) => fetch(`/debug?/load ${chemin}:-1`))
      .then(() => {
        window.location.href = '/app/board.html?p=0'
      })
      .catch(() => setOccupe(undefined))
  }, [confirmer])

  const exporter = useCallback(() => {
    setOccupe('export')
    fetch('/save_replay_data')
      .then((r) => r.json())
      .then((data) => {
        const blob = new Blob([JSON.stringify(data)], { type: 'application/json' })
        const lien = document.createElement('a')
        lien.href = URL.createObjectURL(blob)
        const date = new Date().toISOString().slice(0, 16).replace(/[T:]/g, '-')
        lien.download = `marvel-partie-${date}.json`
        lien.click()
        URL.revokeObjectURL(lien.href)
      })
      .catch(() => undefined)
      .finally(() => setOccupe(undefined))
  }, [])

  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »).
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(ouvert ? 'sauvegardes-ouvert' : 'sauvegardes-ferme')

  return (
    <span className="popover-sauvegardes-ancre">
      <button
        type="button"
        className={`bh-bouton bh-save${ouvert ? ' est-actif' : ''}`}
        onClick={basculer}
        aria-expanded={ouvert}
        title={t('Emplacements de sauvegarde, chargement, export')}
      >
        <span className="ico ico-sauver" aria-hidden="true">💾</span> {t('Sauver')}
      </button>
      {ouvert ? (
        <div className="popover-sauvegardes" role="menu" style={transformDecalage(decalage)}>
          <span
            className="popover-sauvegardes-titre poignee-glisser"
            onPointerDown={gestesGlisser.onPointerDown}
            onPointerMove={gestesGlisser.onPointerMove}
            onPointerUp={gestesGlisser.onPointerUp}
            onPointerCancel={gestesGlisser.onPointerCancel}
          >
            {t('Sauvegardes')}
          </span>
          {[1, 2, 3].map((slot) => {
            const meta = metas[slot]
            return (
              <div className="ligne-sauvegarde" key={slot}>
                <span className="slot-titre">
                  <b>Slot {slot}</b>
                  <small>
                    {meta?.villain
                      ? `${meta.villain} · step ${meta.step ?? '?'}${meta.time ? ` · ${meta.time}` : ''}`
                      : t('Vide')}
                  </small>
                </span>
                <button type="button" onClick={() => sauverSlot(slot)} disabled={occupe !== undefined}>
                  {occupe === `save-${slot}` ? '...' : t('Sauver')}
                </button>
                <button
                  type="button"
                  onClick={() => chargerSlot(slot)}
                  disabled={occupe !== undefined || !meta?.villain}
                >
                  {occupe === `load-${slot}` ? '...' : t('Charger')}
                </button>
              </div>
            )
          })}
          <div className="ligne-sauvegarde">
            <span className="slot-titre">
              <b>{t('Fichier')}</b>
              <small>{t('Télécharger cette partie en .json')}</small>
            </span>
            <button type="button" onClick={exporter} disabled={occupe !== undefined}>
              {occupe === 'export' ? '...' : t('Exporter')}
            </button>
          </div>
        </div>
      ) : null}
    </span>
  )
}

/**
 * Barre de relecture (ouverte via « Watch replay » du wizard : ?revoir=1&pas=N).
 * Navigue dans la partie rejouee via les commandes serveur /goto et /step.
 */
function BarreRevoir({ pasTotal }: { pasTotal: number }) {
  const [position, setPosition] = useState(0)

  const aller = useCallback((pas: number) => {
    setPosition(pas)
    void fetch(`/debug?/goto ${pas}`).catch(() => undefined)
  }, [])

  const avancer = useCallback(() => {
    setPosition((p) => Math.min(p + 1, pasTotal))
    void fetch('/debug?/step 1').catch(() => undefined)
  }, [pasTotal])

  return (
    <div className="barre-revoir" role="toolbar" aria-label={t('Contrôles de relecture')}>
      <span className="revoir-titre">▶ {t('Relecture')}</span>
      <button type="button" onClick={() => aller(0)} title={t('Retour au début')}>
        ⏮
      </button>
      <input
        type="range"
        min={0}
        max={pasTotal}
        value={position}
        onChange={(e) => aller(Number(e.currentTarget.value))}
      />
      <button type="button" onClick={avancer} title={t('Pas suivant')}>
        ▶
      </button>
      <button type="button" onClick={() => aller(pasTotal)} title={t('Aller à la fin')}>
        ⏭
      </button>
      <span className="revoir-position">
        {position}/{pasTotal}
      </span>
    </div>
  )
}

/**
 * Au-dela de ce nombre d'essais, on cesse de parler de « connexion perdue ».
 *
 * Les delais de reconnexion sont 2, 4, 8, 15 puis 30 secondes (`moteur.ts`) :
 * cinq essais valent donc environ une minute. Passe ce cap, une coupure
 * passagere serait revenue. Ce qui reste, c'est une table fermee — par un
 * deploiement, par le faucheur d'inactivite, ou parce qu'on l'a eteinte.
 */
const ESSAIS_AVANT_TABLE_FERMEE = 5

/**
 * À partir de ce nombre d'essais, on NOMME la cause la plus probable.
 *
 * ⚠ AJOUTÉ LE 21/09/2026, PARCE QUE FERMER UNE TABLE EST DEVENU UN CLIC. Les
 * délais sont 2, 4, 8, 15 puis 30 s : l'invité dont l'hôte vient de quitter
 * voyait donc « Connexion perdue » pendant VINGT-NEUF secondes avant
 * d'apprendre que sa table n'existait plus. C'était déjà long quand seul un
 * déploiement pouvait fermer une table ; ça ne l'est plus quand l'hôte le
 * fait d'un bouton, en cours de soirée.
 *
 * Trois essais valent environ six secondes : assez pour qu'un hoquet de
 * réseau soit déjà revenu, assez peu pour laisser quelqu'un attendre devant
 * une table morte.
 *
 * ⚠ ET CE SEUIL NE DÉPLACE QUE LA PHRASE, JAMAIS LA SORTIE. « Revenir à
 * l'accueil » reste à `ESSAIS_AVANT_TABLE_FERMEE` : à six secondes la partie
 * est presque sûrement récupérable, et offrir la porte à cet instant ferait
 * quitter sa partie à un invité impatient pendant un hoquet de wifi — lequel
 * est arrivé par un lien de siège dont la clé est dans l'adresse, si bien que
 * l'accueil ne l'y ramène pas. Dire, oui ; pousser dehors, non.
 */
const ESSAIS_AVANT_DOUTE = 3

/**
 * Bandeau de reconnexion : visible des que le socket tombe pendant une partie,
 * avec compte a rebours de la prochaine tentative et bouton immediat.
 *
 * ⚠ ET IL FINIT PAR DIRE LA VERITE (17/09/2026). Il repetait « nouvel essai
 * dans Xs » indefiniment : un joueur dont la table avait ete fermee voyait un
 * decompte qui ne menait nulle part, sans jamais apprendre qu'il n'y avait
 * plus rien a rejoindre. Constate en direct sur le plateau d'un joueur : 19
 * tentatives de socket en dix minutes, toutes en 502.
 */
function BandeauConnexion({
  etat,
  reconnecter,
  peutAvoirEteFermee,
}: {
  etat: EtatMoteur
  reconnecter: () => void
  /**
   * ⚠ CE BANDEAU NE SAIT RIEN DE QUI LE REGARDE, et il nommait pourtant une
   * cause. Il ne reçoit qu'un état de socket : ni siège, ni spectateur, ni
   * « cette table vient du site ». Résultat, l'HÔTE lui-même lisait « l'hôte
   * a peut-être fermé la table » pendant une simple coupure, et une partie
   * LOCALE l'affichait alors qu'il n'y a ni hôte ni table. On le lui dit donc
   * (`laTablePeutAvoirEteFermee`), et il se tait quand la phrase n'a pas de
   * sens.
   */
  peutAvoirEteFermee: boolean
}) {
  const [, forcer] = useState(0)
  useEffect(() => {
    if (etat.connecte) return
    const t = window.setInterval(() => forcer((n) => n + 1), 500)
    return () => window.clearInterval(t)
  }, [etat.connecte])

  if (etat.connecte || !etat.monde) return null
  const restant = etat.prochaineTentative
    ? Math.max(0, Math.ceil((etat.prochaineTentative - Date.now()) / 1000))
    : undefined
  const fermee = etat.tentatives >= ESSAIS_AVANT_TABLE_FERMEE
  const doute = etat.tentatives >= ESSAIS_AVANT_DOUTE
  return (
    <div className="bandeau-connexion" role="alert">
      <span aria-hidden="true">⚠</span>
      {fermee ? (
        <span>
          {t('Cette table a été fermée.')} {t('Ta partie n’est plus en cours.')}
        </span>
      ) : (
        <span>
          {t('Connexion perdue')}
          {restant !== undefined
            ? ` — ${t('nouvel essai dans')} ${restant}s`
            : ` — ${t('reconnexion...')}`}
          {etat.tentatives > 1 ? ` (${t('essai')} ${etat.tentatives})` : ''}
          {/* ⚠ UNE POSSIBILITÉ, PAS UNE DÉCLARATION. Affirmer la fermeture
              ici serait faux une fois sur deux (une vraie coupure met le même
              temps à revenir) ; se taire jusqu'à la trentième seconde, c'était
              laisser quelqu'un attendre devant une table morte. */}
          {doute && peutAvoirEteFermee ? ` — ${t('l’hôte a peut-être fermé la table')}` : ''}
        </span>
      )}
      {/* ⚠ LA SORTIE RESTE A `ESSAIS_AVANT_TABLE_FERMEE`, pas au palier du
          doute : voir la docstring d'`ESSAIS_AVANT_DOUTE`. Nommer une cause
          et pousser quelqu'un dehors ne se décident pas au même moment. */}
      {fermee ? (
        <button type="button" onClick={() => atterrir(lienAccueil())}>
          {t('Revenir à l’accueil')}
        </button>
      ) : null}
      <button type="button" onClick={reconnecter}>
        {t('Reconnecter maintenant')}
      </button>
    </div>
  )
}

/** Le SITE, pas la table : c'est le domaine parent qui sait rouvrir une place. */
// `lienAccueil` vit desormais dans `board/quitter-la-table.ts` : c'est la
// meme question (« ou aller quand le moteur n'est plus la ? »), et le depart
// volontaire en a besoin comme dernier recours.

function PageEtat({
  fichier,
  playerId,
  catalogue,
  outils,
}: {
  fichier: string
  playerId: number
  catalogue: Catalogue
  outils: React.ReactNode
}) {
  const { monde, erreur } = useEtatEnregistre(fichier)
  const plateau = useMemo(
    () => (monde ? construirePlateau(monde, { playerId, catalogue }) : undefined),
    [monde, playerId, catalogue]
  )
  const { mode } = useModeMobile()
  /**
   * LE CARTOUCHE DE LA PHASE DU MECHANT, SUR UN ETAT ENREGISTRE (14/09/2026).
   *
   * ⚠ POURQUOI CE BLOC EXISTE. `tools/autoplay.py` sait capturer une vraie
   * phase du mechant (`AUTOPLAY_CAPTURE`), et deux fixtures en portent une avec
   * son journal `faits_mechant`. Mais cette page-ci ne montait QUE la table :
   * on voyait les cartes de la phase, jamais le cartouche qui la raconte. Le
   * seul moyen de le regarder restait donc de jouer une partie a la main, ce
   * que l'outillage etait precisement cense eviter. Mesure faite : la fixture
   * `rhino__spider_man__phase-mechant-complet.js` produit six etapes, et aucune
   * n'etait affichee.
   *
   * ⚠ AUCUN MOTEUR DERRIERE. « Suivant » ne relache rien (il n'y a pas de trame
   * retenue) : il fait seulement avancer le cartouche, qui tient son propre
   * index. C'est exactement ce qu'on veut regarder.
   */
  const etapesEnregistrees = useMemo(() => {
    if (!monde) return []
    const mechantIds = new Set<number>()
    for (const carte of indexerCartesMonde(monde).values()) {
      if (kindOf(carte) === 'villain') mechantIds.add(carte.id)
    }
    return etapesDeroule(
      monde.faits_mechant ?? [],
      [],
      monde.round_id ?? 0,
      mechantIds,
      new Set(),
      undefined,
      (monde.players ?? []).map((joueur) => (joueur.area_hero ?? [])[0]?.name)
    )
  }, [monde])
  const modePhaseEnregistre = lireModePhaseMechant()
  // La scene du PC dessine le cartouche du bas, distribution fondue (D15),
  // comme la partie elle-meme ; le telephone garde le rendu d'avant (D36).
  const cartoucheDuBas =
    modePhaseEnregistre === 'detaille' && mode !== 'mobile'
  const pourLeCartouche = useMemo(
    () =>
      cartoucheDuBas
        ? fusionnerDistribution(etapesEnregistrees)
        : { etapes: etapesEnregistrees, cartesDistribuees: 0 },
    [cartoucheDuBas, etapesEnregistrees]
  )
  const [bandeauFini, setBandeauFini] = useState(false)
  // Le mode manuel : tout ce qui parlait au nom du moteur disparait, meme sur
  // un etat enregistre (un capture de partie manuelle reste muette).
  //
  // ⚠ `leMoteurSeTait`, PAS `estModeManuel` (tache 8 bis) : ce masquage ne
  // doit prendre effet qu'une fois la boucle manuelle entree, jamais pendant
  // la mise en place — le moteur y raconte encore normalement (BandeauPhase
  // et DeroulePhase compris).
  const manuel = leMoteurSeTait(monde)

  if (!monde || !plateau) {
    return (
      <p className="plateau-message" role={erreur ? 'alert' : undefined}>
        {erreur ?? t('Chargement...')}
      </p>
    )
  }

  const Rendu = mode === 'mobile' ? PlateauMobile : Board
  return (
    <>
    {/* ⚠ LE BANDEAU AUSSI, sinon la sequence « il joue seul, puis la phase
        commence » ne s'observe nulle part hors d'une vraie partie - et c'est
        exactement le manque qui avait laisse passer un cartouche invisible le
        14/09/2026. */}
    {manuel ? null : modePhaseEnregistre !== 'instantane' && etapesEnregistrees.length > 0 ? (
      <BandeauPhase
        round={monde.round_id ?? 1}
        actif
        onFini={() => setBandeauFini(true)}
      />
    ) : null}
    {manuel ? null : modePhaseEnregistre !== 'instantane' && etapesEnregistrees.length > 0 ? (
      <DeroulePhase
        attendreBandeau={!bandeauFini}
        presentation={modePhaseEnregistre === 'detaille' ? 'scene' : 'table'}
        telephone={mode === 'mobile'}
        etapes={pourLeCartouche.etapes}
        cartesDistribuees={pourLeCartouche.cartesDistribuees}
        infoCarte={(id) => indexerCartesMonde(monde).get(id)?.info}
        accelerationEnJeu={[...(monde.area_schemes_main ?? []), ...(monde.area_schemes_side ?? [])].reduce((n, c) => n + (c.info?.acceleration_icon ?? 0), 0)}
        identitePhase={monde.round_id ?? 0}
        identitePartie={fichier}
        phaseMechantEnCours={PHASES_DU_MECHANT.has(monde.phase ?? '')}
        // ⚠ SANS `carteScene`, LES DEUX GESTES DU PAQUET NE MONTRENT RIEN. Les
        // cartes boost sont deja parties a la defausse quand l'etape s'affiche,
        // et la carte revelee est encore face cachee dans le monde retenu : ni
        // l'une ni l'autre ne se lit sur la table. C'est cet acces a l'index du
        // monde qui les sort et les retourne. Oubli constate a l'ecran : zero
        // boost, zero carte revelee, sur une etape qui en portait.
        carteScene={(id, faceVisible) => {
          const carte = indexerCartesMonde(monde).get(id)
          if (!carte) return undefined
          return toScanCard(
            faceVisible
              ? { ...carte, visible_for_players: [playerId], is_face_up: true }
              : carte,
            { playerId, actives: new Set(), catalogue }
          )
        }}
        dosRencontre={{
          id: 'dos-rencontre',
          name: t('Carte rencontre'),
          kind: 'unknown',
          imageUrl: scanUrl('encounter'),
          facedown: true,
        }}
        // ⚠ SANS `nomFr`, LES NOMS RESTENT EN ANGLAIS. Les faits du moteur
        // portent le nom anglais en clair (« The Break-In! ») ; c'est ce
        // rappel-la qui rend le nom francais de la carte. Le plateau d'une
        // vraie partie le fournit depuis toujours ; cette page-ci ne le
        // fournissait pas, et toutes les captures que j'en tirais montraient du
        // francais mele d'anglais. Constate par l'utilisateur sur mes propres
        // captures : « pourquoi il y a marque The Break-In ? ».
        nomFr={(id) => {
          const carte = indexerCartesMonde(monde).get(id)
          return carte ? nomAffiche(carte) : undefined
        }}
        onSuivant={() => {}}
        onTerminer={() => {}}
      />
    ) : null}
    <Rendu
      world={monde}
      playerId={playerId}
      plateau={plateau}
      outils={outils}
      bandeManigances={mode !== 'mobile'}
      bas={
        <footer className="plateau-action plateau-action-attente" role="status">
          <strong>Saved state.</strong>
          <span>
            {t('Aucune partie derrière cette vue : rien à jouer. Retire « ?etat= » de l’adresse pour revenir à la partie.')}
          </span>
        </footer>
      }
    />
    </>
  )
}

/** Ligne interrupteur du panneau d'options. */
function LigneOption({
  libelle,
  detail,
  actif,
  onBascule,
}: {
  libelle: string
  detail?: string
  actif: boolean
  onBascule: () => void
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={actif}
      className={`ligne-option${actif ? ' est-actif' : ''}`}
      onClick={onBascule}
      title={detail}
    >
      <span className="ligne-option-libelle">{libelle}</span>
      <span className="ligne-option-etat" aria-hidden="true">
        {actif ? t('Oui') : t('Non')}
      </span>
    </button>
  )
}

/** Panneau d'options du plateau : tous les reglages regroupes derriere ⚙. */
/* `PanneauOptions` a ete SUPPRIME le 14/09/2026, remplace par
   `board/FenetreReglages.tsx`. C'etait un popover de 18 reglages a plat,
   ouvert depuis un autre popover : « il y a une colonne et puis quand j'ouvre
   les options, il y a encore la colonne des options ». Rien n'a ete perdu au
   passage, chaque reglage se retrouve dans l'un des quatre onglets. */

/** Ecran de fin de partie : victoire ou defaite, avec retour au menu. */
function EcranFinPartie({
  gagne,
  raison,
  bataille,
  monde,
  siege,
  retourSalon = false,
  onMenu,
  onDeconnexion,
}: {
  gagne: boolean
  raison?: string
  /**
   * Mode Bataille : la partie se gagne PAR UN CAMP, et le meme ecran sert aux
   * deux tables. `gagne` dit alors si c'est NOTRE camp, et `nul` si personne
   * n'a gagne (les deux camps perdus, ou egalite parfaite).
   */
  bataille?: { nul: boolean }
  monde?: World
  /**
   * Siège de CE navigateur (`?p=`), et non la vue affichée : regarder la table
   * d'un autre ne fait pas de nous ce joueur. Le panneau de récompenses s'en
   * sert pour savoir quelles cases nous appartiennent.
   */
  siege: number
  /** Invité d'une table répartie : « Retour » mène à son salon (retour-salon.ts). */
  retourSalon?: boolean
  onMenu: () => void
  onDeconnexion: () => void
}) {
  const heros = (monde?.players ?? [])
    .map((joueur) => joueur.area_hero?.[0]?.name?.replace(/^\W*/, ''))
    .filter((nom): nom is string => Boolean(nom))
  const eyebrow = bataille
    ? bataille.nul
      ? t('Match nul')
      : gagne
        ? t('Victoire')
        : t('Défaite')
    : gagne
      ? t('Victoire')
      : t('Défaite')
  const titre = bataille
    ? bataille.nul
      ? t('Aucun camp ne l\u2019emporte')
      : gagne
        ? t('Ton camp l\u2019emporte !')
        : t('Le camp adverse l\u2019emporte')
    : gagne
      ? t('Les héros l\u2019emportent !')
      : t('Les héros sont vaincus')
  const rounds = monde?.round_id
  const mechants = (monde?.area_villain ?? []).map((carte) => nomAffiche(carte)).filter(Boolean)
  const [onglet, setOnglet] = useState<'resultat' | 'stats'>('resultat')
  // Le lien Buy Me a Coffee (25/10/2026, choix de l'utilisateur) : discret, une
  // victoire sur deux au hasard, jamais en defaite ni en relecture. Tire une
  // seule fois a l'ouverture de l'ecran, pour ne pas clignoter d'un rendu a l'autre.
  const [cafeTire] = useState(() => Math.random() < 0.5)
  const avecCafe = gagne && cafeTire && !estRelecture()
  return (
    <div
      className={`fin-partie ${gagne ? 'est-victoire' : 'est-defaite'}${bataille?.nul ? ' est-nul' : ''}${langueActuelle() === 'en' ? ' avec-image-en' : ''}`}
      role="dialog"
      aria-modal="true"
      aria-label={eyebrow}
    >
      {gagne ? (
        <div className="fin-partie-confettis" aria-hidden="true">
          {Array.from({ length: 24 }, (_, i) => (
            <span key={i} style={{ '--i': i } as React.CSSProperties} />
          ))}
        </div>
      ) : null}
      {/* L'ONOMATOPEE BD (04/10/2026, choix de l'utilisateur) : un eclat a
          pointes derriere le mot, qui arrive avec un petit choc (coupe sans
          animations, en sobre et en mouvement reduit : fin-partie-bd.css). */}
      <div className="fin-partie-eclat" aria-hidden="true">
        {bataille?.nul ? t('MATCH NUL !') : gagne ? t('VICTOIRE !') : t('DÉFAITE !')}
      </div>
      <div className={`fin-partie-carte${onglet === 'stats' ? ' est-stats' : ''}`}>
        <div className="fin-partie-onglets" role="tablist">
          <button
            type="button"
            role="tab"
            aria-selected={onglet === 'resultat'}
            className={`fin-partie-onglet${onglet === 'resultat' ? ' est-actif' : ''}`}
            onClick={() => setOnglet('resultat')}
          >
            {t('Résultat')}
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={onglet === 'stats'}
            className={`fin-partie-onglet${onglet === 'stats' ? ' est-actif' : ''}`}
            onClick={() => setOnglet('stats')}
          >
            {t('Stats')}
          </button>
        </div>
        {onglet === 'stats' ? <StatsPartie stats={monde?.stats_partie} gagne={gagne} /> : null}
        {/* Resultat reste MONTE pendant les Stats : les recompenses de campagne
            deja cochees ne doivent pas se perdre en changeant d'onglet. */}
        <div className="fin-partie-resultat" style={{ display: onglet === 'stats' ? 'none' : 'contents' }}>
        <span className="fin-partie-eyebrow">{eyebrow}</span>
        <strong className="fin-partie-titre">{titre}</strong>
        {raison ? (
          <span className="fin-partie-raison">{traduireMoteur(raison)}</span>
        ) : null}
        <VerdictAssembleeFin monde={monde} siege={siege} />
        <BilanObjectifs objectifs={monde?.puzzle_objectives} />
        {heros.length || mechants.length ? (
          <span className="fin-partie-detail">
            {heros.join(', ')}
            {mechants.length ? ` ${t('contre')} ${[...new Set(mechants)].join(', ')}` : ''}
            {rounds ? ` · ${rounds} ${t('round(s)')}` : ''}
          </span>
        ) : null}
        {/* Liste des hauts faits debloques : DEBRANCHEE, comme la banniere.
            Le style .fin-partie-hauts-faits reste dans board.css. */}
        {/* Campagne : ce que le scenario vient de rapporter. Ne s'affiche qu'a
            la VICTOIRE d'une partie lancee depuis l'ecran des campagnes — le
            livret veut qu'une defaite se rejoue sans rien reporter. */}
        <PanneauRecompenses
          monde={monde}
          gagne={gagne}
          siege={siege}
          resume={{
            heros: (monde?.players ?? [])
              .map((joueur) => ({
                nom: joueur.area_hero?.[0]?.name?.replace(/^\W*/, '') ?? '',
                pic: joueur.area_hero?.[0]?.pic_id,
              }))
              .filter((h) => h.nom),
            vilains: (monde?.area_villain ?? [])
              .map((carte) => ({ nom: nomAffiche(carte), pic: carte.pic_id }))
              .filter((v) => v.nom),
            rounds,
          }}
          onTermine={(retourCampagne, suite) => {
            if (retourCampagne) {
              const demande = new URLSearchParams()
              if (suite?.campagne) demande.set('campagne', suite.campagne)
              if (suite?.lancer) demande.set('lancer', suite.lancer)
              const requete = demande.toString()
              window.location.href = requete ? `/campagne.html?${requete}` : '/campagne.html'
            } else onMenu()
          }}
        />
        {/* Dans le cadre, l'ecran de fin est celui que le joueur a vu (ses boutons, inertes). */}
        {estRelecture() && !estCadre() ? (
          <div className="fin-partie-choix-sortie">
            <button type="button" className="fin-partie-menu" onClick={() => lecteurActif()?.aller(0)}>
              {t('Revoir depuis le début')}
            </button>
          </div>
        ) : (
          <div className="fin-partie-choix-sortie">
            <button type="button" className="fin-partie-menu" onClick={onMenu}>
              {retourSalon ? t('Retour au salon') : t('Retour au choix du héros')}
            </button>
            <a className="fin-partie-menu" href="/get_enregistrement" download="partie.marvelreplay">
              {t('Télécharger la partie')}
            </a>
            <button type="button" className="fin-partie-menu fin-partie-deconnexion" onClick={onDeconnexion}>
              {t('Fermer et déconnecter la table (surtout pour le multijoueur en ligne)')}
            </button>
          </div>
        )}
        {avecCafe ? (
          <p className="fin-partie-cafe">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M4 8h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z" />
              <path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17" />
              <path d="M8 2.5v2.5M12 2.5v2.5" />
            </svg>
            <span>
              {t('Si vous voulez aider à garder le site en vie (serveurs, outils…),')}{' '}
              <a href="https://buymeacoffee.com/narwhalchampions" target="_blank" rel="noopener noreferrer">
                {t('c’est par ici')}
              </a>
              . {t('Aucune obligation, évidemment.')}
            </span>
          </p>
        ) : null}
        </div>
      </div>
    </div>
  )
}

/**
 * Ce qu'un passage de main doit durer pour meriter un changement de vue.
 * Mesure sur le cas signale : les allers-retours du moteur durent environ une
 * demi-seconde.
 */
const DELAI_SUIVI_VUE = 800

/**
 * L'ecran de jeu. Exporte UNIQUEMENT pour que les tests puissent le monter
 * (voir PagePartie.test.tsx) : rien d'autre ne l'importe, la page le rend
 * elle-meme plus bas.
 */
export function PagePartie({
  playerId,
  catalogue,
  modeActions: modeActionsChoisi,
  changerModeActions,
}: {
  playerId: number
  catalogue: Catalogue
  modeActions: ModeActions
  changerModeActions: (mode: ModeActions) => void
}) {
  const confirmer = useConfirmation()
  // ⚠ ON REGARDE, ON NE JOUE PAS. Lu une fois : l'adresse ne change pas sous
  // nos pieds, et la valeur sert a une dizaine d'endroits. Ce que ce drapeau
  // fait, et ce qu'il ne fait pas, est dit dans `estSpectateur` (moteur.ts).
  const spectateur = estSpectateur()
  // LE TELEPHONE PENDANT LA PARTIE (zone 3, 10/10/2026, board/mobile/telephone.ts) :
  // ecran allume, vibrations, verrou portrait. Rien de tout cela sur un PC.
  const telephone = useEstTelephone()
  const reglagesTelephone = useReglagesTelephone()
  useEcranAllume(telephone)
  const { tourner: tournerLeTelephone } = useVerrouPortrait(telephone, reglagesTelephone.verrouPortrait)
  // LA TABLETTE (24/10/2026, board/tablette/) : le plateau PC au doigt, en paysage.
  const tablette = useEstTablette() && !telephone
  useMarqueTablette(tablette)
  const tabletteDebout = useTabletteDebout(tablette)
  // Au doigt, les actions d'une carte sont des boutons sous son apercu (decision 3) :
  // la presentation simple, sans action unique jouee d'un toucher.
  const modeActions: ModeActions = tablette ? 'simple' : modeActionsChoisi
  // ⚠ LUE UNE FOIS, AU MONTAGE, ET JAMAIS AU CLIC. L'adresse du site ne change
  // pas de la vie d'une page, et la lire au moment où l'on quitte la mettait
  // dans le chemin d'un clic : fenêtre qui ne s'ouvre pas si le moteur traîne,
  // et — bien pire — hôte pris pour un joueur local si la lecture échoue, donc
  // table laissée debout sans que personne ne le sache. `connu` reste faux
  // tant qu'on n'a pas de réponse : ce n'est PAS « aucun site ».
  const [site, setSite] = useState<Site>({ connu: false, url: '' })
  useEffect(() => {
    let vivant = true
    lireLeSite().then((lu) => {
      if (vivant) setSite(lu)
    })
    return () => {
      vivant = false
    }
  }, [])
  const {
    etat,
    repondre,
    continuer,
    reconnecter,
    reglerModePhase,
    avancerPasAPas,
    signalerActivite,
  } = usePartieEnCours(playerId)
  // Le preavis du site (mise a jour imminente, coupure). Interroge le moteur,
  // qui relaie le site : en partie locale il n'y a personne derriere, et le
  // bandeau ne s'affiche jamais.
  const annonce = useAnnonce()
  // Un onglet laisse ouvert garde son JavaScript apres un deploiement : c'est
  // le seul moyen de le lui dire (voir board/maj.ts).
  const majDisponible = useMiseAJour()
  // Il PASSE, il ne s'installe pas : deux secondes toutes les trente. Entre
  // deux passages l'ecran de jeu est entierement libre.
  const annonceVisible = usePassage(annonce !== null)
  // Fin de tour SUGGEREE : le moteur nous interroge, mais aucune option n'est
  // reellement jouable (toutes portent une failure_reason). Le bouton End Turn
  // devient vert et pulse — jamais d'auto-pass, le joueur garde la main.
  const finDeTourSuggeree = useMemo(() => {
    const options = etat.demande?.options
    if (!etat.aNous || !options || options.length === 0) return false
    return options.every((option) => option.failure_reason !== '')
  }, [etat.aNous, etat.demande])

  // Mode « revoir » (lecteur de replay) : ouvert par le wizard avec
  // ?revoir=1&pas=<nombre de pas enregistres>.
  const modeRevoir = useMemo(() => {
    const url = new URLSearchParams(window.location.search)
    if (url.get('revoir') !== '1') return undefined
    const pas = Number(url.get('pas') ?? '0')
    return { pas: Number.isFinite(pas) && pas > 0 ? pas : 0 }
  }, [])
  // HOT-SEAT : un seul ecran joue tous les heros. La vue (main affichee,
  // visibilite, interactions) suit le joueur que le moteur interroge...
  // ...sauf si le joueur FORCE la vue sur un heros precis (regarder la main de
  // l'autre). Auto = null.
  const [vueForcee, setVueForcee] = useState<number | null>(null)

  // La vue ne suit pas TOUS les passages de main.
  //
  // Entre deux cartes jouees, le moteur interroge brievement l'autre joueur —
  // fenetre de reponse ou d'interruption ou il n'a rien de jouable — puis
  // revient. La vue basculait a chaque fois : « entre chaque carte jouee il me
  // remet une demi-seconde sur l'autre perso », signale en jeu a deux heros.
  //
  // Regle : on suit TOUT DE SUITE si le joueur interroge a au moins une option
  // reellement jouable (c'est son tour, il attend la table). Sinon on attend
  // DELAI_SUIVI_VUE : si le moteur repart avant, la bascule n'aura jamais eu
  // lieu. Rien de jouable n'est retarde — la REPONSE part toujours pour le
  // joueur du moteur (`option.bind_player_id`), independamment de la vue.
  // Une vue FORCEE sur un joueur qui vient d'etre elimine ne mene plus nulle
  // part : sa table a disparu. On repasse en Auto plutot que de laisser
  // l'ecran vide avec un bouton qui n'existe plus dans la barre.
  useEffect(() => {
    if (vueForcee === null) return
    if (etat.monde?.players?.[vueForcee]?.is_eliminated) setVueForcee(null)
  }, [vueForcee, etat.monde])

  const [joueurSuivi, setJoueurSuivi] = useState<number | undefined>(undefined)
  const demandeJouable = etat.demande?.options.some((o) => o.failure_reason === '') ?? false

  useEffect(() => {
    const cible = etat.joueurDemande
    if (cible === undefined || cible === joueurSuivi) return
    // On ne suit pas un joueur dont on ne verrait RIEN. Pendant les mulligans,
    // le moteur interroge chaque siege a son tour : la vue partait chez le
    // voisin, dont la main nous est cachee, et l'ecran sans main passait pour
    // une partie bloquee. Voir suivi-vue.ts.
    if (!peutSuivre(etat.monde, cible, playerId, estMultijoueur())) return
    if (joueurSuivi === undefined || demandeJouable) {
      setJoueurSuivi(cible)
      return
    }
    const attente = window.setTimeout(() => setJoueurSuivi(cible), DELAI_SUIVI_VUE)
    return () => window.clearTimeout(attente)
  }, [etat.joueurDemande, joueurSuivi, demandeJouable, etat.monde, playerId])

  const joueurActif = vueForcee ?? joueurSuivi ?? etat.joueurDemande ?? playerId

  // Les onglets du multijoueur en portrait (tache 10) : la MEME liste que les
  // boutons « Vue » ci-dessous (elimines exclus), pour que taper un onglet
  // fasse exactement setVueForcee(id), sans etat parallele qui pourrait
  // diverger du suivi automatique du hot-seat.
  const joueursAffichables = useMemo(
    () =>
      (etat.monde?.players ?? [])
        .map((joueur, i) => ({ id: i, nom: joueur.area_hero?.[0]?.name?.replace(/^\W*/, '') ?? `J${i}`, elimine: joueur.is_eliminated }))
        .filter((joueur) => !joueur.elimine)
        .map(({ id, nom }) => ({ id, nom })),
    [etat.monde]
  )
  const effets = useEffetsCartes(etat.monde)
  // Declare AVANT le useMemo de `plateau` : il en est une dependance, pour
  // que decocher l'option en pleine partie rafraichisse l'affichage sans
  // attendre le prochain evenement du moteur.
  const [scansFr, setScansFr] = useState(scansFrActifs)
  // Le choix des dos de cartes : une dependance du plateau, comme les scans FR.
  const [dosCartes, setDosCartes] = useState<DosCartes>(lireDosCartes)
  const changerDosCartes = useCallback((choix: DosCartes) => {
    ecrireDosCartes(choix)
    setDosCartes(choix)
  }, [])

  // La table est decoupee AVANT l'interaction : celle-ci a besoin de savoir
  // quelles cartes sont reellement dessinees pour ne rendre cliquable que ce qui
  // se voit, et renvoyer le reste au selecteur.
  const {
    mode: modePlateau,
    reglage: reglageMode,
    surAppareilMobile,
    changer: changerReglageMode,
  } = useModeMobile()
  // Remonte ici (et non plus 200 lignes plus bas) parce que la construction du
  // plateau en a besoin : voir `seulCeJoueur` juste en dessous.
  // LE LISERÉ DE L'IDENTITÉ (18/10/2026) : le dégradé des trois couleurs du héros vient des palettes, chargées une
  // seule fois ; les cartes se redessinent dès qu'elles sont là (`couleursDeHeros`, lu par `toScanCard`).
  const [palettesPretes, setPalettesPretes] = useState(false)
  useEffect(() => {
    let vivant = true
    void palettes().then(() => {
      if (vivant) setPalettesPretes(true)
    })
    return () => {
      vivant = false
    }
  }, [])
  const plateau = useMemo(
    () =>
      etat.monde
        ? construirePlateau(etat.monde, {
            playerId: joueurActif,
            // Le siege qui regarde l'ecran, distinct de `playerId` des que la
            // vue Auto suit un AUTRE joueur (`joueurActif` ci-dessus) : sans
            // lui, la zone « Heros et soutiens » du viewer local partait a
            // droite le temps que ce suivi dure. Voir zones.ts, `Options.viewerId`.
            viewerId: playerId,
            catalogue,
            // Vue braquee sur un joueur PAR UN CLIC : on ne pose que sa table.
            // En « Auto » (vueForcee === null), la vue suit celui qui doit agir
            // et la table montre tout le monde, comme une vraie partie a
            // plusieurs.
            //
            // SAUF sur telephone : le portrait ne deplie qu'un joueur a la
            // fois, ses onglets servent justement a changer de joueur. En
            // « Auto », « Ton héros » listait les heros et allies de TOUTE la
            // table et « Engagés » les ennemis de tout le monde : le titre
            // mentait, et la hauteur des blocs devenait imprevisible
            // (revue finale du 11/09/2026).
            seulCeJoueur: vueForcee !== null || modePlateau === 'mobile',
          })
        : undefined,
    [etat.monde, joueurActif, catalogue, scansFr, dosCartes, vueForcee, palettesPretes]
  )
  // ⚠ LA TABLE NE VOIT PAS LA QUESTION DE LA MANIGANCE. Son panneau la tient
  // (voir `demandeHorsPanneauManigance`) : le halo, le menu d'une carte et le
  // clic direct du mode Detaille se construisent tous sur CETTE demande-ci,
  // jamais sur `etat.demande`. La reference est la meme pour toute autre
  // question : rien d'autre ne change.
  const demandeOrdinaire = demandeHorsPanneauManigance(etat.demande, etat.monde)
  // Le siège qui compose la réponse : celui que le moteur interroge. C'est sa
  // sélection que le spectateur et la relecture montrent (vu-partage.ts).
  const siegeQuiCompose = etat.joueurDemande ?? joueurActif
  const selectionDuJoueur = useVuDuJoueur<SelectionPartagee | null>('sel', spectateur ? siegeQuiCompose : undefined)
  // Une reponse partie au moteur n'est PAS une action abandonnee : `useActionAnnulee` (plus bas) le sait par ce suivi.
  const noterReponseRef = useRef<() => void>(() => {})
  const repondreSuivi = useCallback(
    (reponse: Reponse | null, bindPlayerId: number) => {
      noterReponseRef.current()
      return repondre(reponse, bindPlayerId)
    },
    [repondre]
  )
  const interaction = useInteraction(
    etat.monde,
    demandeOrdinaire,
    repondreSuivi,
    plateau?.idsAffiches ?? AUCUN_ID,
    joueurActif,
    catalogue,
    modeActions,
    plateau?.representantsDePile,
    spectateur ? (selectionDuJoueur ?? null) : undefined
  )
  useEffect(() => {
    if (spectateur || !interaction.selectionPartagee) return
    publierVu(siegeQuiCompose, 'sel', interaction.selectionPartagee)
  }, [spectateur, siegeQuiCompose, interaction.selectionPartagee])
  const groupesRegardes = useMemo(
    () => (etat.monde ? cartesRegardees(etat.monde, joueurActif, catalogue) : []),
    [etat.monde, joueurActif, catalogue]
  )
  const cartesMondeParId = useMemo(() => indexerCartesMonde(etat.monde), [etat.monde])
  const cartesAfficheesParId = useMemo(() => indexerCartesAffichees(plateau), [plateau])
  const cartesMondeParNom = useMemo(
    () => indexerCartesMondeParNom(cartesMondeParId),
    [cartesMondeParId]
  )
  // Un choix textuel (« quelle chanson ? ») montre le SCAN de la carte nommee.
  // A defaut, une option « Put "X" into play » (mise en place de campagne) nomme
  // une manigance pas encore posee : on la construit depuis son identifiant,
  // sinon le survol retomberait sur la manigance principale porteuse.
  const carteDeLOption = useCallback(
    (option: Option) =>
      carteNommeeParOption(option, cartesMondeParNom, joueurActif, catalogue)
      ?? carteDuSchemaCampagneParOption(option, joueurActif, catalogue)
      ?? carteDeCampagneParOption(option, cartesMondeParNom, joueurActif, catalogue),
    [cartesMondeParNom, joueurActif, catalogue]
  )
  // Un choix de LOT (« Role: Brawler ») montre les cartes du lot, pas la carte porteuse.
  const cartesDuLot = useCallback(
    (option: Option) => cartesDuLotParOption(option, joueurActif, catalogue),
    [joueurActif, catalogue]
  )
  // Au SURVOL d'un bouton de decision : la carte nommee si l'option en nomme
  // une, sinon la carte qui PORTE l'option (« Spider-Sense » sur une
  // interruption). Face visible forcee : c'est notre carte, on doit la lire.
  const carteAuSurvol = useCallback(
    (option: Option) => {
      const nommee = carteDeLOption(option)
      if (nommee) return nommee
      const porteuse = option.bind_id !== 0 ? cartesMondeParId.get(option.bind_id) : undefined
      if (!porteuse) return undefined
      return toScanCard(
        { ...porteuse, visible_for_players: [joueurActif], is_face_up: true },
        { playerId: joueurActif, actives: new Set(), catalogue }
      )
    },
    [carteDeLOption, cartesMondeParId, joueurActif, catalogue]
  )
  // Le TEXTE de la capacite qu'une option declenche, pour les fenetres de
  // reaction (« I Object! » de Jennifer Walters avant la menace) : le francais
  // quand le plateau l'a (cartes sans scan FR, fan-made), l'anglais de
  // cards.json sinon. Decision utilisateur du 12/09/2026 : mieux vaut le texte
  // en anglais qu'un nom de capacite muet.
  // Le francais de TOUTES les cartes (textes-fr-complets.ts, 700 Ko) arrive par
  // un import dynamique, une fois, des qu'une fenetre de reaction s'ouvre :
  // « pourquoi j'ai encore et toujours du texte en anglais quand je joue en
  // FR » (12/09/2026). Tant qu'il n'est pas la, l'anglais de cards.json fait
  // l'interim, et le panneau se redessine a l'arrivee du dictionnaire.
  const [textesFrComplets, setTextesFrComplets] = useState<Readonly<Record<string, string | undefined>>>()
  const fenetreDeReactionOuverte = etat.demande !== undefined && estFenetreDeReaction(etat.demande)
  // Le cartouche de la phase du Mechant lit aussi ce dictionnaire : la carte
  // revelee dont le moteur ne publie aucun resume se lit par son texte imprime.
  const francaisCompletUtile = fenetreDeReactionOuverte || PHASES_DU_MECHANT.has(etat.monde?.phase ?? '')
  useEffect(() => {
    if (!francaisCompletUtile || textesFrComplets || !scansFrActifs()) return
    let vivant = true
    import('./board/textes-fr-complets')
      .then((module) => {
        if (vivant) setTextesFrComplets(module.TEXTES_FR_COMPLETS)
      })
      .catch(() => undefined)
    return () => {
      vivant = false
    }
  }, [francaisCompletUtile, textesFrComplets])
  const texteCapaciteDeLOption = useCallback(
    (option: Option): string | undefined => {
      const porteuse = option.bind_id !== 0 ? cartesMondeParId.get(option.bind_id) : undefined
      if (!porteuse) return undefined
      const cardId = porteuse.card_id
      const francais = scansFrActifs()
        ? (TEXTES_FR[cardId] ?? TEXTES_FR_FANMADE[cardId] ?? textesFrComplets?.[cardId])
        : undefined
      return extraireCapacite(francais ?? catalogue.texte(cardId), option.name, etat.demande?.ability_type)
    },
    [cartesMondeParId, catalogue, etat.demande?.ability_type, textesFrComplets]
  )
  // Le texte imprime d'une carte (francais quand le plateau l'a, anglais de cards.json sinon) et le nom d'une OPTION qui s'en sert : une carte qui
  // offre deux actions du meme type les nomme par leur paragraphe (demande du 22/10/2026 : jamais « Action » / « Action 1 »).
  const texteImprimeDeLaCarte = useCallback(
    (cardId: string | undefined): string | undefined => {
      if (!cardId) return undefined
      const francais = scansFrActifs()
        ? (TEXTES_FR[cardId] ?? TEXTES_FR_FANMADE[cardId] ?? textesFrComplets?.[cardId])
        : undefined
      return francais ?? catalogue.texte(cardId)
    },
    [catalogue, textesFrComplets]
  )
  const nomActionDe = useCallback(
    (option: Option): string => {
      const porteuse = option.bind_id !== 0 ? cartesMondeParId.get(option.bind_id) : undefined
      return nomLisibleParlant(option, texteImprimeDeLaCarte(porteuse?.card_id))
    },
    [cartesMondeParId, texteImprimeDeLaCarte]
  )
  // Fermer ou abandonner une action avant de la valider ne disait rien (26/10/2026) : le message le dit, quelques secondes.
  const { message: actionAnnulee, noterReponse } = useActionAnnulee(
    interaction.option ? nomActionDe(interaction.option) : undefined,
    etat.demande
  )
  useEffect(() => {
    noterReponseRef.current = noterReponse
  }, [noterReponse])
  // L'onglet « Ville » (campagne MC×DC 2026) : l'etat exporte par le moteur, ouvert ou non, et le nom de chaque joueur (son heros).
  const [villeOuverte, setVilleOuverte] = useState(false)
  // L'onglet « Assemblée » (Kingsfall multi-tables) : l'etat commun relu par le moteur a chaque rendu.
  const [assembleeOuverte, setAssembleeOuverte] = useState(false)
  const assembleeExportee = useAssembleeEnDirect(etat.monde, joueurActif)
  const villeExportee = useMemo(() => villeDuMonde(etat.monde), [etat.monde])
  const nomsJoueursVille = useMemo(() => {
    const noms: Record<number, string> = {}
    ;(etat.monde?.players ?? []).forEach((p, i) => {
      noms[i] = p?.area_hero?.[0]?.name?.replace(/^\W*/, '') || `${t('Joueur')} ${i + 1}`
    })
    return noms
  }, [etat.monde])
  // L'EFFET BOOST ★ d'une carte rencontre, en une phrase (D10) : la ligne
  // « ★ Sweeping Swoop : … » sous la rangee du cartouche du bas. Meme source
  // que le texte d'une capacite : le francais quand le plateau l'a, l'anglais
  // de cards.json sinon. Muet sans paragraphe « Boost » : la vue dit alors
  // seulement que l'effet s'applique.
  const texteBoostEtoile = useCallback(
    (carteId: number): string | undefined => {
      const carte = cartesMondeParId.get(carteId)
      if (!carte) return undefined
      const cardId = carte.card_id
      const francais = scansFrActifs()
        ? (TEXTES_FR[cardId] ?? TEXTES_FR_FANMADE[cardId] ?? textesFrComplets?.[cardId])
        : undefined
      return extraireBoost(francais) ?? extraireBoost(catalogue.texte(cardId))
    },
    [cartesMondeParId, catalogue, textesFrComplets]
  )
  // Une carte rencontre revelee : son Renfort (le mot-cle du catalogue, dans la
  // langue de l'interface) et son texte imprime, francais quand le plateau
  // l'a, anglais de cards.json sinon (meme source que le Boost ★).
  const infoRevelee = useCallback(
    (carteId: number): InfoRevelee | undefined => {
      const carte = cartesMondeParId.get(carteId)
      if (!carte) return undefined
      const cardId = carte.card_id
      const francais = scansFrActifs()
        ? (TEXTES_FR[cardId] ?? TEXTES_FR_FANMADE[cardId] ?? textesFrComplets?.[cardId])
        : undefined
      return {
        renfort: catalogue.motsCles(cardId).some((mot) => mot.nom === t('Renfort')),
        texteImprime: extraireEffetRevele(francais ?? catalogue.texte(cardId)),
      }
    },
    [cartesMondeParId, catalogue, textesFrComplets]
  )
  // Les nombres que le monde publie sur une carte (`info` : stade imprime,
  // seuil de menace), pour le titre court et les jauges du cartouche du bas.
  const infoCarte = useCallback(
    (id: number): Partial<Record<string, number>> | undefined => cartesMondeParId.get(id)?.info,
    [cartesMondeParId]
  )
  // Le bouton de refus d'une reaction dit « Ne pas jouer » pour une carte EN
  // MAIN et « Ne pas utiliser » pour une capacite en jeu (04/10/2026).
  const idsEnMain = useMemo(
    () => new Set((etat.monde?.players ?? []).flatMap((joueur) => joueur.hand_cards.map((carte) => carte.id))),
    [etat.monde]
  )
  const estEnMain = useCallback((bindId: number) => idsEnMain.has(bindId), [idsEnMain])
  // Les cartes de la scene du deroule detaille : lues dans l'index du MONDE,
  // jamais sur la table. Face visible sur demande : la carte revelee et les
  // boosts sont encore face cachee dans le monde de la trame retenue (le fait
  // est journalise avant le retournement, player_action.py) et le joueur doit
  // pourtant les lire. Meme forcage que `ciblesHorsTable` (interaction.ts).
  const carteScene = useCallback(
    (id: number, faceVisible: boolean): ScanCardProps | undefined => {
      const carte = cartesMondeParId.get(id)
      if (!carte) return undefined
      return toScanCard(
        faceVisible ? { ...carte, visible_for_players: [joueurActif], is_face_up: true } : carte,
        { playerId: joueurActif, actives: new Set(), catalogue }
      )
    },
    [cartesMondeParId, joueurActif, catalogue]
  )
  const cartesDuPlateau = useMemo<AccesCartesJournal>(
    () => ({ existe: (id) => cartesMondeParId.has(id), voir: carteScene, classe: 'au-dessus-du-deroule' }),
    [cartesMondeParId, carteScene]
  )
  const cartesDuVolet = useMemo<AccesCartesJournal>(
    () => ({ ...cartesDuPlateau, classe: 'depuis-le-journal', borneDroite: ['.volet-journal'] }),
    [cartesDuPlateau]
  )
  const dosRencontre = useMemo<ScanCardProps>(
    () => ({
      id: 'dos-rencontre',
      name: t('Carte rencontre'),
      kind: 'unknown',
      imageUrl: scanUrl('encounter'),
      facedown: true,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [dosCartes]
  )
  const [optionSurvolee, setOptionSurvolee] = useState<Option | undefined>(undefined)
  const [pulseTemporaire, setPulseTemporaire] = useState<Set<number>>(() => new Set())
  const [ciblesMenu, setCiblesMenu] = useState<{ titre: string; cartes: ScanCardProps[] } | undefined>(
    undefined
  )
  const minuteurPulse = useRef<number | undefined>(undefined)

  useEffect(
    () => () => {
      window.clearTimeout(minuteurPulse.current)
    },
    []
  )

  const ciblesPulseesSurvol = useMemo(
    () => idsPulsePourOption(optionSurvolee, plateau, interaction.cibleFocus),
    [optionSurvolee, plateau, interaction.cibleFocus]
  )
  const ciblesPulseesPhaseEnnemie = useMemo(
    () => idsPulsePourDemandeEnnemie(etat.monde, etat.demande, plateau),
    [etat.monde, etat.demande, plateau]
  )
  const ciblesPulsees = useMemo(() => {
    const ids = new Set(ciblesPulseesSurvol)
    for (const id of ciblesPulseesPhaseEnnemie) ids.add(id)
    for (const id of pulseTemporaire) ids.add(id)
    return ids
  }, [ciblesPulseesSurvol, ciblesPulseesPhaseEnnemie, pulseTemporaire])
  // En manuel, la question garée du moteur ne doit plus être atteignable par
  // la table : une carte surlignée cliquée y répondrait (lot 1, 06/10/2026).
  const moteurMuet = leMoteurSeTait(etat.monde)
  const interactifsAvecPulse = useMemo(
    () => (moteurMuet ? new Map<number, EtatInteractif>() : ajouterPulse(interaction.cartes, ciblesPulsees)),
    [moteurMuet, interaction.cartes, ciblesPulsees]
  )

  /**
   * Le code brut rendu par `glisser/cibles.raisonDuRefus`, mis en francais.
   *
   * ⚠ Le glisser AFFICHAIT DEJA le motif du moteur tel quel, donc du jargon
   * anglais (« check_can_pay ») en pleine partie francaise, avec « Pas ici »
   * pour tout repli. Constate le 10/09/2026 en cablant l'agrandissement : les
   * deux chemins passent desormais par la MEME table.
   *
   * Un code sans phrase rend `undefined`, et l'appelant retombe sur son propre
   * repli. Ce silence est un defaut, pas un cas tolere : la gate le refuse.
   */
  const traduireRefusGlisser = useCallback((code: string | undefined) => {
    if (!code) return undefined
    return phraseDuRefus(code)
  }, [])

  // POURQUOI TELLE CARTE EST INJOUABLE, par carte, deja en francais.
  //
  // Le moteur joint ses refus dans un canal a part (`demande.refus`), avec un
  // CODE et non une phrase ; `phraseDuRefus` ecrit la phrase. Une carte peut
  // porter plusieurs actions refusees pour des raisons differentes : on garde
  // une ligne par raison, sans doublon, dans l'ordre ou le moteur les donne.
  //
  // ⚠ UN CODE INCONNU EST ECARTE ICI, ET C'EST VOULU : mieux vaut ne rien
  // afficher qu'un jargon anglais. Ce silence n'est pas un repli tolere, c'est
  // un defaut : `tools/verifier_raisons_refus.py` echoue des qu'un code
  // atteint le plateau sans phrase.
  const raisonsRefus = useMemo(() => {
    const parCarte = new Map<number, string[]>()
    for (const refus of etat.demande?.refus ?? []) {
      if (!refus.bind_id) continue
      const phrase = phraseDuRefus(refus.failure_reason)
      if (phrase === undefined) continue
      const deja = parCarte.get(refus.bind_id) ?? []
      if (!deja.includes(phrase)) deja.push(phrase)
      parCarte.set(refus.bind_id, deja)
    }
    return parCarte
  }, [etat.demande])
  const representantsPulseHorsTable = useMemo(() => {
    const representants = new Set<number>()
    if (!optionAvecCibles(optionSurvolee) || !plateau || interaction.cibleFocus !== undefined) {
      return representants
    }
    for (const cible of new Set(optionSurvolee.all_legal_targets)) {
      if (plateau.idsAffiches.has(cible)) continue
      const representant = plateau.representantsDePile.get(cible)
      if (representant !== undefined) representants.add(representant)
    }
    return representants
  }, [optionSurvolee, plateau, interaction.cibleFocus])

  const choisirOptionDepuisMenu = useCallback(
    (option: Option, ciblesInitiales?: number[], parGeste = false) => {
      const ids = idsPulsePourOption(option, plateau, ciblesInitiales?.[0])
      setPulseTemporaire(ids)
      setOptionSurvolee(undefined)
      window.clearTimeout(minuteurPulse.current)
      minuteurPulse.current = window.setTimeout(() => setPulseTemporaire(new Set()), 1000)
      interaction.choisirOption(option, ciblesInitiales, parGeste)
    },
    [interaction, plateau]
  )

  const ouvrirCiblesHorsTable = useCallback(
    (option: Option | undefined) => {
      if (!option || !plateau) return false
      const cartes = ciblesHorsTablePourOption(option, cartesMondeParId, plateau, joueurActif, catalogue)
      if (cartes.length === 0) return false
      setCiblesMenu({ titre: nomActionDe(option), cartes })
      return true
    },
    [cartesMondeParId, catalogue, plateau, joueurActif]
  )

  const [apercuSelecteur, setApercuSelecteur] = useState<ScanCardProps | undefined>(undefined)

  // Le selecteur se demonte des qu'une cible est choisie. React n'emet aucun
  // onMouseLeave sur un composant demonte : sans ce nettoyage, l'apercu resterait
  // fige sur la derniere carte survolee, par-dessus la table et sans plus jamais
  // se mettre a jour.
  const selecteurOuvert = interaction.ciblesHorsTable.length > 0
  useEffect(() => {
    if (!selecteurOuvert) setApercuSelecteur(undefined)
  }, [selecteurOuvert])

  // Deux etats seulement : automatique, ou forcer le plateau PC. Forcer le mode
  // MOBILE a disparu du cycle — c'est ce choix-la qui enfermait, puisqu'il
  // rendait ensuite l'option elle-meme inatteignable (voir modeEffectif).
  const cyclerReglageMode = useCallback(() => {
    changerReglageMode(reglageMode === 'pc' ? 'auto' : 'pc')
  }, [reglageMode, changerReglageMode])

  const [animations, setAnimations] = useState(lireAnimations)
  // L'affichage sobre coupe les animations sans toucher au reglage du joueur :
  // revenir en normal lui rend ce qu'il avait choisi.
  const [affichage, setAffichage] = useState<Affichage>(lireAffichage)
  // L'épuré garde les animations (16/10/2026) : seul le sobre les coupe.
  const animationsActives = animations && affichage !== 'sobre'
  useEffect(() => {
    appliquerAffichage(affichage)
  }, [affichage])
  // L'épuré n'est permis qu'à l'administrateur (16/10/2026) : une fois le serveur
  // entendu, la réponse est retenue et le choix rangé relu.
  useEffect(() => {
    let vivant = true
    void essaisOuverts().then((ouverts) => {
      retenirEpurePermis(ouverts)
      if (vivant) setAffichage(lireAffichage())
    })
    return () => {
      vivant = false
    }
  }, [])
  // Le compte fait foi quand il a deja un choix (meme contrat que la
  // preparation) : un plateau rejoint directement suit l'autre appareil.
  useEffect(() => {
    let vivant = true
    void chercherAffichageDuCompte().then((duCompte) => {
      if (!vivant || duCompte === undefined) return
      try {
        window.localStorage.setItem(CLE_AFFICHAGE, duCompte)
      } catch {
        /* stockage indisponible */
      }
      setAffichage(duCompte)
    })
    return () => {
      vivant = false
    }
  }, [])
  const changerAffichage = useCallback((choisi: Affichage) => {
    ecrireAffichage(choisi)
    setAffichage(choisi)
  }, [])
  // LA TEINTE DU FOND (04/10/2026, teinte.ts). Rendu en direct pendant qu'on
  // tourne la roue ; le compte n'est prevenu qu'au repos (600 ms), pas a
  // chaque mouvement du pointeur.
  const [teinte, setTeinte] = useState<Teinte | undefined>(lireTeinteDuNavigateur)
  useEffect(() => {
    appliquerTeinte(teinte)
  }, [teinte])
  useEffect(() => {
    let vivant = true
    void chercherTeinteDuCompte().then((duCompte) => {
      if (!vivant || duCompte === undefined) return
      ecrireTeinte(duCompte ?? undefined, false)
      setTeinte(duCompte ?? undefined)
    })
    return () => {
      vivant = false
    }
  }, [])
  const envoiTeinte = useRef<number | undefined>(undefined)
  const retenirTeinte = useCallback((choisie: Teinte | undefined) => {
    ecrireTeinte(choisie, false)
    setTeinte(choisie)
    window.clearTimeout(envoiTeinte.current)
    envoiTeinte.current = window.setTimeout(() => envoyerTeinteAuCompte(choisie), 600)
  }, [])
  const changerTeinte = useCallback((choisie: Teinte) => retenirTeinte(choisie), [retenirTeinte])
  const reinitialiserTeinte = useCallback(() => retenirTeinte(undefined), [retenirTeinte])
  const basculerAnimations = useCallback(() => {
    setAnimations((a) => {
      const nouveau = !a
      try {
        window.localStorage.setItem(CLE_ANIMATIONS, nouveau ? 'on' : 'off')
      } catch {
        /* localStorage indisponible : le choix ne survivra pas au rechargement. */
      }
      return nouveau
    })
  }, [])
  const historique = useHistoriquePartie(etat.monde, etat.demande, etat.partieId)

  // Les etapes du deroule detaille : `etapesDeroule` parcourt tous les faits
  // et toutes les entrees du journal, donc on ne la relance pas a chaque
  // rendu (meme motif que `cartesMondeParId` plus haut).
  //
  // `etapesDeroule` ne voit pas le monde, seulement les faits et le journal :
  // c'est ici qu'on lui dit qui est le vilain, pour distinguer ses coups de
  // ceux de ses sbires. `cartesMondeParId` porte deja le `card_type` de
  // chaque carte ; `kindOf()` le traduit en famille visuelle, et 'villain'
  // (EncounterVillain) distingue le vilain lui-meme d'un sbire ('minion',
  // Minion). Ajouter `cartesMondeParId` aux dependances ne change rien au
  // rythme de recalcul : `etat.monde` se re-parse en JSON a chaque trame du
  // moteur (meme piege que dans DeroulePhase.tsx), donc `faits_mechant`
  // change deja d'identite a chaque trame et relancait deja ce useMemo aussi
  // souvent.
  // L'etape que montre le cartouche : la table se cale dessus (table-calee.ts).
  const [cleEtapeAffichee, setCleEtapeAffichee] = useState<string>()
  const [modePhaseChoisi, setModePhase] = useState<ModePhaseMechant>(lireModePhaseMechant)
  // LE SPECTATEUR VOIT LA PHASE DANS LE MODE DU JOUEUR REGARDE (08/10/2026),
  // publie avec son etape (etape-partagee.ts) ; son propre reglage ne change pas.
  const modeDuJoueurSuivi = useSuiviDuJoueur(spectateur).mode
  const modePhase = spectateur && modeDuJoueurSuivi ? modeDuJoueurSuivi : modePhaseChoisi

  const etapesPhaseMechant = useMemo(() => {
    const mechantIds = new Set<number>()
    for (const carte of cartesMondeParId.values()) {
      if (kindOf(carte) === 'villain') mechantIds.add(carte.id)
    }
    // Les heros que le MONDE declare tombes. C'est l'etat que le moteur pose
    // lui-meme (`Player.Eliminate` -> `is_eliminated`), pas une deduction :
    // l'identite d'un joueur elimine reste dans `area_hero` (le moteur exclut
    // le type Identity de la defausse, voir joueur-elimine.test.ts), donc on la
    // retrouve, PV a zero.
    //
    // Il ne dit pas QUEL coup a mis le heros a terre : c'est `etapesDeroule`
    // qui croise cet ensemble avec le `restant` du fait. Les deux ensemble, et
    // jamais l'un sans l'autre.
    const herosVaincusIds = new Set<number>()
    for (const joueur of etat.monde?.players ?? []) {
      if (!joueur.is_eliminated) continue
      for (const carte of joueur.area_hero ?? []) {
        // Les DEUX faces : un heros peut tomber en alter ego (une obligation,
        // une manigance qui frappe). `area_hero` porte aussi ses ameliorations,
        // qui ne sont ni l'une ni l'autre.
        const famille = kindOf(carte)
        if (famille === 'hero' || famille === 'alter-ego') herosVaincusIds.add(carte.id)
      }
    }
    // Le premier joueur du round, pour l'ordre du tour des revelations
    // (regle officielle : chaque joueur revele en commencant par lui).
    //
    // Le monde ne publie pas de champ dedie a l'ordre des joueurs : le jeton
    // de premier joueur vit comme un COMPTEUR generique sur l'identite de son
    // detenteur (`k_first_player_token`, meme convention que `k_threat` sur
    // une manigance), pose par le moteur des `SetActive()`
    // (game/card/face/card_type/identity.py). `findIndex` rend -1 si personne
    // ne le porte (ancien moteur sans le jeton) : on rend alors `undefined`,
    // et `etapesDeroule` garde l'ordre du journal plutot que d'en inventer un.
    const premierJoueurId = (etat.monde?.players ?? []).findIndex(
      (joueur) => ((joueur.area_hero ?? [])[0]?.info['k_first_player_token'] ?? 0) > 0
    )
    // Le heros de chaque joueur, dans le MEME ordre que `World.players` :
    // c'est l'indice que porte deja `EntreeHistorique.joueur`. Brut, prefixe
    // decoratif compris : `etapesDeroule` le nettoie elle-meme, comme elle le
    // fait deja pour les faits du mechant.
    const nomsHerosParJoueur = (etat.monde?.players ?? []).map(
      (joueur) => (joueur.area_hero ?? [])[0]?.name
    )
    // T17 : les allies du monde, en jeu ou deja en defausse (ils ont quitte la table quand l'etape se lit).
    const alliesIds = new Set<number>()
    for (const carte of cartesMondeParId.values()) {
      if (kindOf(carte) === 'ally') alliesIds.add(carte.id)
    }
    return etapesDeroule(
      etat.monde?.faits_mechant ?? [],
      entreesPourRepli(historique.entrees, PHASES_DU_MECHANT.has(etat.monde?.phase ?? ''), etat.monde?.render_id),
      etat.monde?.round_id ?? 0,
      mechantIds,
      herosVaincusIds,
      premierJoueurId === -1 ? undefined : premierJoueurId,
      nomsHerosParJoueur,
      'phase',
      alliesIds
    )
  }, [
    cartesMondeParId,
    etat.monde?.faits_mechant,
    etat.monde?.players,
    historique.entrees,
    etat.monde?.phase,
    etat.monde?.round_id,
  ])
  // LES COUPS DU MECHANT HORS DE SA PHASE (03/10/2026) : leur propre cartouche,
  // un coup a la fois (CoupHorsPhase).
  const coupsHorsPhase = useMemo(() => {
    const mechantIds = new Set<number>()
    for (const carte of cartesMondeParId.values()) {
      if (kindOf(carte) === 'villain') mechantIds.add(carte.id)
    }
    return etapesHorsPhase(etat.monde?.faits_mechant ?? [], etat.monde?.round_id ?? 0, mechantIds)
  }, [cartesMondeParId, etat.monde?.faits_mechant, etat.monde?.round_id])
  // Les memes, cartes revelees comprises, pour le cartouche « Pendant ton
  // tour » de la scene PC (D26, lot 5 de la refonte du 04/10/2026). Le
  // cartouche de la table ne montre que des coups, comme avant.
  const coupsPendantTonTour = useMemo(() => {
    const mechantIds = new Set<number>()
    for (const carte of cartesMondeParId.values()) {
      if (kindOf(carte) === 'villain') mechantIds.add(carte.id)
    }
    return etapesHorsPhase(etat.monde?.faits_mechant ?? [], etat.monde?.round_id ?? 0, mechantIds, {
      avecRevelations: true,
    })
  }, [cartesMondeParId, etat.monde?.faits_mechant, etat.monde?.round_id])
  // « REVOIR LA PHASE DU MECHANT » (03/10/2026), dans le volet du journal : la
  // phase du round PRECEDENT. Le moteur garde ses faits jusqu'au premier fait
  // du round suivant ; on ne la propose donc qu'hors de la phase du mechant.
  const etapesPhasePrecedente = useMemo(() => {
    if (PHASES_DU_MECHANT.has(etat.monde?.phase ?? '')) return []
    const mechantIds = new Set<number>()
    for (const carte of cartesMondeParId.values()) {
      if (kindOf(carte) === 'villain') mechantIds.add(carte.id)
    }
    const round = (etat.monde?.round_id ?? 0) - 1
    if (round < 1) return []
    return etapesDeroule(etat.monde?.faits_mechant ?? [], [], round, mechantIds)
  }, [cartesMondeParId, etat.monde?.faits_mechant, etat.monde?.round_id, etat.monde?.phase])
  // LA TABLE CALEE SUR LE RECIT (04/10/2026, table-calee.ts). Pendant la
  // phase, la table dessine le monde de l'etape AFFICHEE par le cartouche, pas
  // le plus recent : sinon le boost ou la carte rencontre se retournaient sur
  // la table avant le « Suivant ». Une question au joueur rend le monde reel.
  // L'essai « Nouvelle phase du méchant » (10/10/2026), coché par compte dans
  // /admin : faux tant que le serveur n'a pas répondu, comme plus bas (essais ouverts).
  const [essaiPhaseCompte, setEssaiPhaseCompte] = useState(false)
  useEffect(() => {
    let vivant = true
    void essaiPhaseMechant().then((actif) => {
      if (vivant) setEssaiPhaseCompte(actif)
    })
    return () => {
      vivant = false
    }
  }, [])
  // « Étape par étape bis » (16/10/2026) : le compte qui a l'essai choisit, dans les
  // Réglages, entre trois présentations (board/phase-presentation.ts).
  const [presentationPhase, setPresentationPhase] = useState(lirePresentationPhase)
  useEffect(() => suivrePresentationPhase(setPresentationPhase), [])
  const phaseTris = presentationPhase === 'tris' && phaseTrisUtilisable()
  // Depuis le 19/10/2026 « bis » est pour tout le monde : l'essai de compte ne compte plus (PHASE_BIS_POUR_TOUS).
  const phaseEssai = (PHASE_BIS_POUR_TOUS || essaiPhaseCompte) && presentationPhase !== 'etape' && (presentationPhase !== 'tris' || phaseTris)
  // « Phase dynamique » (16/10/2026) : le cartouche détaillé, posé en panneau à droite.
  const phaseDynamique = phaseEssai && presentationPhase === 'dynamique'
  const instantanesRef = useRef<Instantanes>(new Map())
  const instantanes = useMemo(() => {
    const suivants = majInstantanes(
      instantanesRef.current,
      etapesPhaseMechant,
      etat.monde,
      PHASES_DU_MECHANT.has(etat.monde?.phase ?? ''),
      phaseEssai
    )
    instantanesRef.current = suivants
    return suivants
  }, [etapesPhaseMechant, etat.monde, phaseEssai])
  // REFONTE, LOT 4 (essai, decisions 49 et 51) : tant que l'attaque retourne
  // ses boosts, la table garde le monde d'AVANT l'etape (PV, menace) ; et une
  // carte qu'une etape suivante fera entrer en jeu n'y est pas encore.
  const [avantResultat, setAvantResultat] = useState(false)
  // La Riposte a son ecran dans l'essai (DeroulePhase) : ses coups doivent s'y retrouver.
  const etapesDesCoups = useMemo(
    () => (phaseEssai ? avecEcranStadeRevele(avecEtapesRiposte(etapesPhaseMechant)) : etapesPhaseMechant),
    [phaseEssai, etapesPhaseMechant]
  )
  // La dernière étape connue vient d'être validée sans qu'une suivante n'arrive (la riposte avant la
  // question d'ordre des sbires) : ses jetons volent quand même, la clé « validée » les libère.
  const [validationEtape, setValidationEtape] = useState<string | undefined>(undefined)
  const etatEtapeAffichee = etapesDesCoups.find((e) => e.cle === cleEtapeAffichee)?.etat
  const etapeSurTable = etapesDesCoups.find((e) => e.cle === cleEtapeAffichee)
  const questionVisible = questionDuRecit(Boolean(etat.aNous && etat.demande), etapeSurTable,
    validationEtape === `${cleEtapeAffichee}|${etatEtapeAffichee}`, modePhase === 'sur-table', avantResultat && Boolean(etapeSurTable?.boosts.length))
  const instantaneRecit = mondeDeLaTable(instantanes, cleEtapeAffichee, false)
  const mondeCale = useMemo(() => {
    const base = questionVisible ? etat.monde : instantaneRecit
    if (!base || modePhase !== 'sur-table' || !instantaneRecit) return base
    return avecFacesRencontreDuRecit(base, instantaneRecit, etapeSurTable?.etat === 'annonce')
  }, [questionVisible, etat.monde, instantaneRecit, modePhase, etapeSurTable?.etat])
  const cleDesCoups =
    cleEtapeAffichee !== undefined && validationEtape === `${cleEtapeAffichee}|${etatEtapeAffichee}`
      ? `${cleEtapeAffichee}#valide`
      : cleEtapeAffichee
  const compteursFiges = useCoupsEnVol(etapesDesCoups, cleDesCoups, phaseEssai, !avantResultat)
  const mondeTable = useMemo(() => {
    if (!phaseEssai || !mondeCale) return mondeCale
    const base = (avantResultat ? mondeAvantEtape(instantanes, etapesPhaseMechant, cleEtapeAffichee) : undefined) ?? mondeCale
    // Les compteurs peuvent garder leur valeur précédente sans recacher une carte déjà lue.
    const facesStables = modePhase === 'sur-table' ? avecFacesRencontreDuRecit(base, mondeCale, etapeSurTable?.etat === 'annonce') : base
    const monde = sansCartesAVenir(facesStables, cartesAVenir(etapesPhaseMechant, cleEtapeAffichee))
    // Essai, 13/10/2026 : les cartes que l'ecran touche (menace, PV) gardent
    // leur valeur d'AVANT ; le jeton qui vole au clic les met a jour en arrivant.
    return avecCompteursFiges(monde, compteursFiges)
  }, [phaseEssai, mondeCale, avantResultat, instantanes, etapesPhaseMechant, cleEtapeAffichee, compteursFiges, modePhase, etapeSurTable?.etat])
  const plateauTable = useMemo(
    () =>
      mondeTable
        ? construirePlateau(mondeTable, {
            playerId: joueurActif,
            viewerId: playerId,
            catalogue,
            seulCeJoueur: vueForcee !== null || modePlateau === 'mobile',
          })
        : undefined,
    [mondeTable, joueurActif, playerId, catalogue, vueForcee, modePlateau]
  )

  // Les PV MAXIMUM des personnages, par nom, pour le bilan de fin de phase du
  // mechant : sans eux il dit « 8 » la ou il pourrait dire « 8/14 ».
  //
  // Par NOM, parce que c'est la cle du bilan : ses lignes regroupent ce qu'UNE
  // cible a encaisse, et le regroupement se fait sur le nom (voir lignesBilan).
  // Le nom passe par `nomNettoye`, la meme fonction que le deroule applique aux
  // noms venus des faits : sans cela, « * Colossus » ne retrouverait jamais
  // « Colossus ».
  //
  // Le plafond vient de `pvMaximum`, exactement comme la pastille de PV des
  // cartes : `info.max_health` du moteur, ameliorations comprises, et le PV
  // imprime du catalogue en secours. Deux regles differentes pour un meme
  // chiffre se contrediraient a l'ecran.
  //
  // Une carte sans maximum sur (PV variables selon le nombre de joueurs, PV
  // infinis, carte hors catalogue) n'entre PAS dans la table : le bilan montre
  // alors le restant seul. Un plafond faux serait pire qu'un chiffre nu.
  const pvMaxParNom = useMemo(() => {
    const parNom = new Map<string, number>()
    for (const carte of cartesMondeParId.values()) {
      if (!isUnit(carte)) continue
      const max = pvMaximum(carte, catalogue)
      if (max === undefined || max <= 0) continue
      const nom = nomNettoye(carte.name)
      if (nom) parNom.set(nom, max)
    }
    return parNom
  }, [cartesMondeParId, catalogue])

  // Le rapport de bug. Il ne capture qu'AU CLIC : il lit le monde et la demande
  // du moment, et le journal ci-dessus pour le passé. Aucun tampon d'états n'est
  // gardé, donc une partie qui ne signale rien n'en porte aucun coût.
  const rapport = useRapportBug(etat.monde, etat.demande, historique.entrees, etat.joueurDemande)

  // Mode Bac à sable. Inerte hors de ce mode : le crochet n'installe aucune
  // écoute et la couche ne rend rien, donc une partie normale n'en porte
  // aucune trace. Déclaré APRÈS l'historique, dont il consomme la porte
  // d'entrée pour y inscrire chaque intervention.
  const triche = useTriche(etat.monde, joueurActif, historique.ajouterTriche)

  // Le mode manuel : tout ce qui parlait au nom du moteur disparait. Une garde
  // par endroit, greppable et retirable d'un bloc.
  //
  // ⚠ `leMoteurSeTait`, PAS `estModeManuel` (tache 8 bis) : la REGLE est vraie
  // des la creation de la partie (mise en place comprise), mais le moteur n'y
  // est tu qu'une fois la boucle manuelle entree. Se regler sur la regle
  // masquerait la demande centrale ET l'assistant d'action qui portent le
  // mulligan PENDANT la mise en place — la partie resterait bloquee pour
  // toujours, sans rien a cliquer sur la premiere main.
  const manuel = leMoteurSeTait(etat.monde)

  // Fin de tour automatique (24/09/2026, inspiré de MTG Arena) : quand le
  // bouton « Fin du tour » est déjà suggéré (plus rien de jouable), on
  // déclenche `interaction.annuler()` tout seul au lieu d'attendre le clic.
  // La toute première fois que ça arriverait, une modale demande au joueur
  // s'il veut ce comportement ; sa réponse est mémorisée et ne redemande
  // plus jamais — modifiable ensuite dans Réglages (`bascluerFinTourAuto`).
  const [finTourAutoChoix, setFinTourAutoChoix] = useState(lireFinTourAuto)
  const basculerFinTourAuto = useCallback(() => {
    setFinTourAutoChoix((c) => {
      const nouveau = c === 'on' ? 'off' : 'on'
      ecrireFinTourAuto(nouveau)
      return nouveau
    })
  }, [])
  // Empreinte de LA suggestion en cours : sert a ne declencher qu'UNE FOIS
  // par nouvelle demande suggeree, meme si `finDeTourSuggeree` (un booleen)
  // reste egal a lui-meme d'un rendu a l'autre pendant que le moteur
  // enchaine plusieurs demandes toutes aussi peu jouables les unes que les
  // autres (meme principe que `empreinte` dans interaction.ts).
  const empreinteFinTourSuggeree = useMemo(() => {
    if (!finDeTourSuggeree) return undefined
    const options = etat.demande?.options ?? []
    return `${etat.demande?.event_name ?? ''}|${options.map((o) => o.id).join(',')}`
  }, [finDeTourSuggeree, etat.demande])
  const derniereFinTourAutoPassee = useRef<string | undefined>(undefined)
  useEffect(() => {
    if (manuel || !empreinteFinTourSuggeree) return
    if (derniereFinTourAutoPassee.current === empreinteFinTourSuggeree) return
    derniereFinTourAutoPassee.current = empreinteFinTourSuggeree
    // ⚠ CHEMIN SYNCHRONE QUAND LE CHOIX EST DEJA TRANCHE (meme piege corrige
    // le jour meme dans interaction.ts pour l'ecart de heros et le paiement
    // automatique) : une Promise systematique decalerait `annuler()` d'un
    // tick sans raison des que le reglage est deja 'on'/'off'.
    if (finTourAutoChoix === 'on') {
      interaction.annuler()
      return
    }
    if (finTourAutoChoix === 'off') return
    void confirmer({
      titre: t('Terminer ton tour automatiquement ?'),
      texte: t(
        'Quand il ne reste plus rien à jouer, le jeu peut passer directement au joueur suivant, sans attendre un clic sur Fin du tour. Ce choix se change à tout moment dans Réglages.'
      ),
      confirmer: t('Oui, automatiquement'),
      annuler: t('Non, je clique moi-même'),
    }).then((accepte) => {
      ecrireFinTourAuto(accepte ? 'on' : 'off')
      setFinTourAutoChoix(accepte ? 'on' : 'off')
      if (accepte) interaction.annuler()
    })
  }, [empreinteFinTourSuggeree, manuel, confirmer, finTourAutoChoix, interaction.annuler])

  // ⚠ `estModeManuel`, PAS `manuel` (tâche 3, arbitrage du plan). Deux
  // exceptions au partage règle/état ci-dessus, et pour une raison sérieuse :
  // `mainVisibleForcee` et `SelecteurHeros` restent réservés au mode manuel
  // DÉCLARÉ, jamais à une simple PAUSE d'une partie ordinaire. En pause sur
  // une table EN LIGNE, chaque joueur a son propre écran ; ouvrir les mains
  // (ou proposer de regarder celle d'un autre) montrerait le jeu de tout le
  // monde à tout le monde. Une pause sert à corriger un bug, pas à dévoiler
  // les mains -- voir `manuel/mode.ts`, `estEnPause`.
  const modeManuelDeclare = estModeManuel(etat.monde)

  const [sons, setSons] = useState(lireSons)
  const basculerSons = useCallback(() => {
    setSons((s) => {
      const nouveau = !s
      try {
        window.localStorage.setItem(CLE_SONS, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [meteo, setMeteo] = useState(lireMeteoActive)
  // Couper « Ambiance » remet l'apercu sur Auto (voir basculerAmbiance) : sinon
  // un apercu fige (pose un jour pour essayer un effet) continue de forcer cet
  // effet a l'ecran malgre l'interrupteur general coupe, sans que rien ne le
  // signale au joueur (voir la ligne « Aperçu d’ambiance », grisee dans ce cas).
  const basculerMeteo = useCallback(() => {
    setMeteo((m) => {
      const { meteo: nouveau, reinitialiserApercu } = basculerAmbiance(m)
      try {
        window.localStorage.setItem(CLE_METEO, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      if (reinitialiserApercu) setApercuMeteo(undefined)
      return nouveau
    })
  }, [])

  // Apercu meteo : force un effet a l'ecran sans partie ni carte. Sert a
  // concevoir de nouveaux effets sans monter une situation de jeu a chaque
  // essai. Volontairement NON persiste : c'est un outil, pas une preference,
  // et le retrouver actif au lancement suivant serait deroutant.
  const [apercuMeteo, setApercuMeteo] = useState<ApercuMeteo>(undefined)
  const reglerApercuMeteo = useCallback((valeur: ApercuMeteo) => setApercuMeteo(valeur), [])

  // La reponse figee a la question « une ambiance s'allume, on la garde ? ».
  // Elle DOIT rester revocable : une case « ne plus me montrer ca » cochee par
  // erreur, sans ligne pour la remettre en marche, serait un piege definitif.
  const [reponseAmbiance, setReponseAmbiance] = useState<ReponseAmbiance>(lireReponseAmbiance)
  const cyclerReponseAmbiance = useCallback(() => {
    setReponseAmbiance((r) => {
      const suivant: ReponseAmbiance =
        r === 'demander' ? 'toujours' : r === 'toujours' ? 'jamais' : 'demander'
      ecrireReponseAmbiance(suivant)
      return suivant
    })
  }, [])


  const [textesCdb, setTextesCdb] = useState(lireTextesCdb)

  // Noms FRANÇAIS des cartes que la barre d'action propose (« Jouer Acier
  // Organique » et non « Organic Steel »). Le monde du moteur ne porte que
  // l'anglais : les cartes de la table paraissent françaises parce que leurs
  // SCANS le sont. La seule source d'un nom français est fr.marvelcdb.com, via
  // le proxy du serveur, un code à la fois et mis en cache. Hors ligne, la
  // requête échoue une fois par code et le nom anglais reste.
  const [nomsFr, setNomsFr] = useState<ReadonlyMap<string, string>>(() => new Map())
  useEffect(() => {
    // Sans question en cours (toute la phase du mechant), il reste les cartes
    // de la scene a nommer : le monde suffit.
    if (langueActuelle() !== 'fr' || !etat.monde) return
    const index = indexerCartesMonde(etat.monde)
    const codes = new Set<string>()
    for (const option of etat.demande?.options ?? []) {
      const carte = index.get(option.bind_id)
      const code = codeMarvelcdb(carte?.card_id)
      if (code && !nomsFr.has(code)) codes.add(code)
    }
    // Les cartes de la phase du mechant (scene du deroule) : auteur, cible,
    // boosts et carte revelee de chaque etape, pour que la scene les nomme
    // en francais comme les scans qu'elle montre.
    for (const etape of etapesPhaseMechant) {
      const ids = [etape.carteId, etape.cibleId, ...etape.boosts.map((boost) => boost.cibleId)]
      for (const id of ids) {
        if (id === undefined) continue
        const code = codeMarvelcdb(index.get(id)?.card_id)
        if (code && !nomsFr.has(code)) codes.add(code)
      }
    }
    if (codes.size === 0) return
    let vivant = true
    void Promise.all(
      [...codes].map(async (code) => [code, (await texteMarvelcdb(code))?.name] as const)
    ).then((paires) => {
      if (!vivant) return
      setNomsFr((avant) => {
        const suivant = new Map(avant)
        for (const [code, nom] of paires) suivant.set(code, nom ?? '')
        return suivant
      })
    })
    return () => {
      vivant = false
    }
    // Seules les options en cours comptent : le monde change à chaque rendu.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [etat.demande, etat.monde?.render_id, etapesPhaseMechant.length])

  const nomPorteurFr = useCallback(
    (bindId: number): string | undefined => {
      const carte = indexerCartesMonde(etat.monde).get(bindId)
      // Le dictionnaire LOCAL d'abord (noms-fr.ts, genere depuis
      // fr.marvelcdb.com) : complet, hors ligne, disponible des le premier
      // rendu. `nomsFr` juste en dessous ne disparait pas pour autant, il
      // complete : il vit du proxy reseau, COUPE par defaut et qui n'arrive
      // qu'apres coup. S'appuyer sur lui seul est ce qui laissait « Backflip »
      // sous le bouton « Jouer » en pleine partie francaise.
      const local = carte ? nomAffiche(carte) : undefined
      if (local && local !== carte?.name) return local
      const code = codeMarvelcdb(carte?.card_id)
      const nom = code ? nomsFr.get(code) : undefined
      return nom || nomDeCarte(etat.monde, bindId)
    },
    [etat.monde, nomsFr]
  )
  // Sous « Ne pas défendre » : CE QUI EST CONNU au moment de choisir, jamais un
  // total. Rules Reference v1.8, « Attack (Enemy Activation) » : la carte boost
  // est donnee face cachee AVANT la declaration du defenseur et retournee
  // APRES. L'utilisateur, 04/10/2026 : « le joueur ne sait pas le nombre de
  // dégâts final avant de défendre ». D'ou « ATQ 3 + 1 carte boost » : l'ATQ
  // actuelle de l'attaquant (la cible de l'option « Defense ») et le nombre de
  // cartes face cachee qui lui sont attachees (`boostable`, publie par
  // `ToDescriptor.Card` a la suite de l'ennemi). Un sbire sans Villainous n'en
  // a aucune : la ligne dit alors seulement « ATQ 2 ».
  const idsDecksSupplementaires = useMemo(
    () => new Set((etat.monde?.additional_decks ?? []).flat().map((carte) => carte.id)),
    [etat.monde]
  )
  const ligneSansDefense = useMemo(
    () => ligneAttaqueConnue(etat.demande?.options ?? [], cartesMondeParId, nomPorteurFr, idsDecksSupplementaires),
    [etat.demande, cartesMondeParId, nomPorteurFr, idsDecksSupplementaires]
  )
  // Le meme detail sans abreger : l'infobulle de « Ne pas défendre ».
  const survolSansDefense = useMemo(
    () => detailAttaqueComplet(etat.demande?.options ?? [], cartesMondeParId, nomPorteurFr, idsDecksSupplementaires),
    [etat.demande, cartesMondeParId, nomPorteurFr, idsDecksSupplementaires]
  )
  /* ---- Le glisser-deposer : les REGLES (8 septembre 2026) -----------------
     Le plateau tient le geste et le dessin ; ici vivent les regles, parce que
     seule cette page connait les options du moteur. Rien n'est devine : tout
     sort de `all_legal_targets` et de `failure_reason`.

     ⚠ LE GESTE NE S'OFFRE QUE QUAND LE CLIC L'EST DEJA : notre tour, connecte,
     et aucune action deja engagee. Pendant un ciblage ou un paiement, la table
     appartient a l'action en cours, et le clic y suffit. */
  const idIdentiteGlisser = etat.monde?.players?.[joueurActif]?.area_hero?.[0]?.id
  const optionsCourantes = useMemo(() => etat.demande?.options ?? [], [etat.demande])
  const reglagesGlisser = useMemo<ReglagesGlisser | undefined>(() => {
    // Mode manuel (tâche 5) : plus de moteur pour conduire la partie, donc
    // plus d'options ni de tour à soi — les gardes ci-dessous (`aNous`,
    // `connecte`, `interaction.option`) n'ont plus de sens et resteraient
    // parfois vraies par accident. Le glisser manuel ne dépend que du
    // plateau, comme le clic droit et le clavier du même mode.
    if (manuel) {
      // Un spectateur ne soulève rien : le serveur refuserait le geste (403).
      if (!plateau || spectateur) return undefined
      // Lot 2 du 06/10/2026 : la carte se pose chez le héros affiché, selon
      // son type (`poser-en-jeu.ts`). `joueurActif` est un rang dans
      // `world.players`, donc un SIÈGE (`to_descriptor.py`).
      const monde = etat.monde
      const base = reglagesGlisserManuel(triche.couche.emettreGeste, () => triche.estToucheEnfoncee('Shift'), {
        carte: (id) => {
          const carte = carteDeLaTrame(monde, id)
          return carte
            ? { type: carte.card_type, nom: nomPorteurFr(id) ?? carte.name, faceCachee: estCacheePourLeJoueur(monde, id) }
            : undefined
        },
        origine: (id) => origineDe(monde, id),
        // Lot 5 (question 6) : chez le héros du groupe visé, sinon l'affiché.
        contexte: (siege) => contexteDePose(monde, siege ?? joueurActif),
        proprietaire: (id) => proprietaireDe(monde, id),
        // Question 14 : en ligne, chacun ne bouge que ses cartes (Rencontre à tous).
        peutBouger: (id) => peutBouger(monde, id, siegesControles(monde, playerId, estMultijoueur())),
        dejaEngage: (id) => (monde?.players?.[joueurActif]?.engaged_enemies ?? []).some((c) => Number(c.id) === id),
        choisirCible: triche.couche.choisirCible,
      })
      // Lot 3 du 07/10/2026 : Maj+glisser d'une carte EN JEU vers une autre carte
      // en jeu trace une flèche (OCTGN) ; depuis la main, Maj pose toujours
      // face cachée. Maj+clic cible.
      const estFleche = (sourceId: number, cible: CibleSurvolee) =>
        triche.estToucheEnfoncee('Shift') &&
        origineDe(monde, sourceId) === 'jeu' &&
        cible.carteId !== undefined &&
        cible.carteId !== sourceId &&
        origineDe(monde, cible.carteId) === 'jeu'
      return {
        ...base,
        fleche: (sourceId, cible) => {
          if (!estFleche(sourceId, cible)) return false
          void envoyerMarque(joueurActif, { genre: 'fleche', de: sourceId, a: cible.carteId! })
          return true
        },
        majClic: (id) => void envoyerMarque(joueurActif, { genre: 'cibler', id }),
        ctrlClic: (id) => selection.basculer(id),
        // Lot 5 : glisser une carte SELECTIONNEE emmene toute la selection (OCTGN),
        // en une seule commande. Le refus ne vaut que pour la carte tenue.
        onDepot: (sourceId, cible) => {
          const ids = cartesDuGeste(sourceId)
          if (ids.length < 2 || estFleche(sourceId, cible)) return base.onDepot(sourceId, cible)
          const raison = base.accepte?.(sourceId, cible) === false ? base.onDepot(sourceId, cible) : undefined
          if (raison) return raison
          void triche.couche.capturerEnLot(() => {
            for (const id of ids) base.onDepot(id, cible)
          })
          return undefined
        },
        accepte: (sourceId, cible) => estFleche(sourceId, cible) || (base.accepte?.(sourceId, cible) ?? true),
        libelle: (sourceId, cible) =>
          estFleche(sourceId, cible)
            ? `${t('Flèche vers')} ${nomPorteurFr(cible.carteId!) ?? ''}`.trim()
            : base.libelle(sourceId, cible),
      }
    }
    if (!etat.aNous || !etat.connecte || interaction.option !== undefined || !plateau) {
      return undefined
    }
    // Ou vit chaque carte DESSINEE. Une zone vide n'existe pas dans le DOM
    // (`emplacement()` la supprime), elle n'apparait donc pas ici non plus.
    const zoneDeLaCarte = new Map<number, string>()
    for (const emplacement of plateau.emplacements) {
      for (const groupe of emplacement.groupes) {
        for (const unite of groupe) {
          zoneDeLaCarte.set(Number(unite.carte.id), emplacement.cle)
          for (const attachee of unite.attachees) {
            zoneDeLaCarte.set(Number(attachee.id), emplacement.cle)
          }
        }
      }
    }
    const zonesPourSource = (sourceId: number) =>
      zonesDeLaSource(
        optionsCourantes,
        sourceId,
        (id) => zoneDeLaCarte.get(id),
        idIdentiteGlisser
      )
    const regles: ReglagesGlisser = {
      estSource: (id) => estSourceGlissable(optionsCourantes, id, idIdentiteGlisser),
      ciblesLegales: (sourceId) =>
        ciblesDeLaSource(optionsCourantes, sourceId, plateau.idsAffiches, idIdentiteGlisser),
      zonesLegales: (sourceId) =>
        new Set([
          ...zonesPourSource(sourceId).keys(),
          // Une carte qui ne vise RIEN se lache sur le terrain : sans cette
          // union, le plateau repondait « Pas ici » partout et il fallait
          // passer par le menu. Demande de l'utilisateur, 15/09/2026.
          ...zonesSansCible(optionsCourantes, sourceId, idIdentiteGlisser),
        ]),
      libelle: (sourceId, cible) => {
        if (cible.carteId !== undefined) {
          const actions = optionsDuDepot(optionsCourantes, sourceId, cible.carteId, idIdentiteGlisser)
          const nomCible = nomPorteurFr(cible.carteId) ?? ''
          if (actions.length === 1) return `${nomActionDe(actions[0]!)} · ${nomCible}`
          if (actions.length > 1) return `${actions.length} ${t('actions possibles')} · ${nomCible}`
          // ⚠ Le code brut du moteur ne se montre JAMAIS au joueur : il passe
          // par la meme table que l'agrandissement (`phraseDuRefus`), sinon on
          // lui affichait « check_can_pay » en pleine partie francaise.
          return (
            traduireRefusGlisser(
              raisonDuRefus(optionsCourantes, sourceId, cible.carteId, idIdentiteGlisser)
            ) ?? t('Pas ici')
          )
        }
        // Lache dans une zone : elle vaut la cible qu'elle contient, on annonce
        // donc exactement ce qu'un lacher sur cette carte annoncerait.
        const parZone = cible.zone ? zonesPourSource(sourceId).get(cible.zone) : undefined
        if (parZone !== undefined) {
          const actions = optionsDuDepot(optionsCourantes, sourceId, parZone, idIdentiteGlisser)
          const nomCible = nomPorteurFr(parZone) ?? ''
          if (actions[0] && actions.length === 1) return `${nomActionDe(actions[0])} · ${nomCible}`
          if (actions.length > 1) return `${actions.length} ${t('actions possibles')} · ${nomCible}`
        }
        // La carte ne vise rien : c'est le TERRAIN qui l'accueille, et on
        // annonce l'action elle-meme, sans nom de cible puisqu'il n'y en a pas.
        if (cible.zone && zonesSansCible(optionsCourantes, sourceId, idIdentiteGlisser).has(cible.zone)) {
          const sansCible = optionsSansCible(optionsCourantes, sourceId, idIdentiteGlisser)
          if (sansCible[0] && sansCible.length === 1) return nomActionDe(sansCible[0])
          if (sansCible.length > 1) return `${sansCible.length} ${t('actions possibles')}`
        }
        return cible.zone ? t('Pas ici') : undefined
      },
      onDepot: (sourceId, cible) => {
        if (cible.carteId !== undefined) {
          const actions = optionsDuDepot(optionsCourantes, sourceId, cible.carteId, idIdentiteGlisser)
          if (actions[0] && actions.length === 1) {
            choisirOptionDepuisMenu(actions[0], [cible.carteId], true)
            return undefined
          }
          if (actions.length > 1) {
            // Plusieurs actions visent cette carte : on ouvre le menu de
            // ciblage, celui-la meme qu'un clic sur la cible aurait ouvert. Il
            // s'ancre sur la carte lachee, donc a l'endroit du geste.
            //
            // ⚠ AVEC SA SOURCE, sinon le menu recalcule les actions SANS elle
            // et ramene tout ce qui vise la cible. Defaut signale en jeu le
            // 15/09/2026 : lacher son heros sur le mechant proposait l'attaque
            // de l'ALLIE.
            interaction.focaliserCible(cible.carteId, sourceId)
            return undefined
          }
          return (
            traduireRefusGlisser(
              raisonDuRefus(optionsCourantes, sourceId, cible.carteId, idIdentiteGlisser)
            ) || t('Cette carte ne peut pas viser celle-ci.')
          )
        }
        if (cible.zone) {
          // Une zone vaut la cible qu'elle contient : lacher dedans, c'est
          // lacher sur cette carte. C'est ainsi qu'on jette un allie dans
          // l'aire de son heros sans avoir a viser l'identite au pixel pres.
          const parZone = zonesPourSource(sourceId).get(cible.zone)
          if (parZone !== undefined) {
            const actions = optionsDuDepot(optionsCourantes, sourceId, parZone, idIdentiteGlisser)
            if (actions[0] && actions.length === 1) {
              choisirOptionDepuisMenu(actions[0], [parZone], true)
              return undefined
            }
            if (actions.length > 1) {
              // Meme regle que ci-dessus : la zone vaut la cible, la source
              // reste la carte lachee.
              interaction.focaliserCible(parZone, sourceId)
              return undefined
            }
          }
          // Rien a viser dans cette zone : reste le cas de la carte qui ne
          // vise RIEN. Elle se joue telle quelle, sans cible.
          if (zonesSansCible(optionsCourantes, sourceId, idIdentiteGlisser).has(cible.zone)) {
            const sansCible = optionsSansCible(optionsCourantes, sourceId, idIdentiteGlisser)
            if (sansCible[0] && sansCible.length === 1) {
              choisirOptionDepuisMenu(sansCible[0], [], true)
              return undefined
            }
            if (sansCible.length > 1) {
              // Plusieurs actions sans cible sur la meme carte : c'est a elle
              // qu'il faut demander, pas a la zone.
              interaction.focaliserCarte(sourceId)
              return undefined
            }
          }
          return t('Cette carte ne se pose pas ici.')
        }
        // Lache dans le vide : il n'y avait pas de cible, il n'y a rien a
        // expliquer. La carte revient a sa place, sans un mot.
        return undefined
      },
    }
    // UNE CARTE QUI SE JOUE SE LACHE N'IMPORTE OU SUR LA TABLE (08/10/2026,
    // .planning/todos/2026-10-08-glisser-evenements-mode-normal.md). Sur une
    // cible possible, les regles ci-dessus la visent ; partout ailleurs sur la
    // table, elle se joue comme au bouton « Jouer » et la cible se choisit
    // ensuite. Injouable maintenant : elle se souleve quand meme, et le lacher
    // dit pourquoi.
    const refusDuMoteur = etat.demande?.refus ?? []
    const enMain = new Set((etat.monde?.players?.[joueurActif]?.hand_cards ?? []).map((carte) => Number(carte.id)))
    const jouer = (sourceId: number) => (enMain.has(sourceId) ? optionJouer(optionsCourantes, sourceId) : undefined)
    const refusPourJouer = (sourceId: number) =>
      enMain.has(sourceId) && !estSourceGlissable(optionsCourantes, sourceId, idIdentiteGlisser)
        ? refusJouer(refusDuMoteur, sourceId)
        : undefined
    const viseUneCible = (sourceId: number, cible: CibleSurvolee) =>
      cible.carteId !== undefined &&
      optionsDuDepot(optionsCourantes, sourceId, cible.carteId, idIdentiteGlisser).length > 0
    // La main n'est pas la table : relacher la carte dans la main ne la joue pas.
    const surLaTable = (cible: CibleSurvolee) =>
      cible.zone !== 'main' && (cible.surLaTable === true || cible.zone !== undefined)
    return {
      ...regles,
      estSource: (id) => regles.estSource(id) || refusPourJouer(id) !== undefined,
      accueilleLaTable: (sourceId) => jouer(sourceId) !== undefined,
      accepte: (sourceId, cible) => {
        if (refusPourJouer(sourceId) !== undefined) return false
        if (jouer(sourceId) && surLaTable(cible)) return true
        return regles.accepte ? regles.accepte(sourceId, cible) : true
      },
      libelle: (sourceId, cible) => {
        const refus = refusPourJouer(sourceId)
        if (refus !== undefined) return traduireRefusGlisser(refus) ?? t('Pas maintenant')
        const option = jouer(sourceId)
        if (option && surLaTable(cible) && !viseUneCible(sourceId, cible)) return nomActionDe(option)
        return regles.libelle(sourceId, cible)
      },
      onDepot: (sourceId, cible) => {
        const refus = refusPourJouer(sourceId)
        if (refus !== undefined) return traduireRefusGlisser(refus) ?? t('Cette carte ne peut pas être jouée maintenant.')
        const option = jouer(sourceId)
        if (option && surLaTable(cible) && !viseUneCible(sourceId, cible)) {
          choisirOptionDepuisMenu(option, [], true)
          return undefined
        }
        return regles.onDepot(sourceId, cible)
      },
    }
  }, [
    manuel,
    spectateur,
    triche.couche.emettreGeste,
    triche.estToucheEnfoncee,
    etat.aNous,
    etat.connecte,
    interaction,
    plateau,
    optionsCourantes,
    idIdentiteGlisser,
    cartesMondeParId,
    nomPorteurFr,
    choisirOptionDepuisMenu,
    etat.monde,
    etat.demande,
    joueurActif,
    triche.couche.choisirCible,
    traduireRefusGlisser,
  ])

  const basculerTextesCdb = useCallback(() => {
    setTextesCdb((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_TEXTES_CDB, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])
  // LE JOURNAL « SUR LA TABLE » (v3, Q45) : une ligne par etape de la phase du
  // mechant, round par round, a la place du detail du moteur.
  const etapesDuMechantParRound = useMemo(() => {
    const mechantIds = new Set<number>()
    for (const carte of cartesMondeParId.values()) {
      if (kindOf(carte) === 'villain') mechantIds.add(carte.id)
    }
    const cache = new Map<number, string[]>()
    return (round: number): string[] => {
      const connu = cache.get(round)
      if (connu) return connu
      const phrases = etapesDeroule(etat.monde?.faits_mechant ?? [], [], round, mechantIds)
        .filter((etape) => etape.titre !== 'vide')
        .map((etape) => titreEtape(etapeEnLangue(etape, nomPorteurFr)))
      cache.set(round, phrases)
      return phrases
    }
  }, [cartesMondeParId, etat.monde?.faits_mechant, nomPorteurFr])

  const basculerScansFr = useCallback(() => {
    setScansFr((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_SCANS_FR, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [curseurs, setCurseurs] = useState(lireCurseursActifs)
  const basculerCurseurs = useCallback(() => {
    setCurseurs((c) => {
      const nouveau = !c
      try {
        window.localStorage.setItem(CLE_CURSEURS, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [autoCible, setAutoCible] = useState(lireAutoCible)
  const basculerAutoCible = useCallback(() => {
    setAutoCible((a) => {
      const nouveau = !a
      try {
        window.localStorage.setItem(CLE_AUTO_CIBLE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  // Le nouveau design (barre, bandeau, assistant) : voir board/design-essai.ts.
  // Il est le DEFAUT depuis le 11/09/2026 ; c'est l'ancien plateau qui se
  // demande, par ?design=classique dans l'URL ou par la ligne dans Options.
  const [designEssai, setDesignEssai] = useState(() => {
    try {
      return lireDesignEssai(window.location.search, window.localStorage)
    } catch {
      return false
    }
  })
  const basculerDesignEssai = useCallback(() => {
    setDesignEssai((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_DESIGN_ESSAI, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [validationCourte, setValidationCourte] = useState(lireValidationCourte)
  const basculerValidationCourte = useCallback(() => {
    setValidationCourte((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_VALIDATION_COURTE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  // Le spectateur affiche la meme etape que le joueur, dans son mode (etape-partagee.ts).
  useEffect(() => {
    if (spectateur) return
    publierEtape(playerId, cleEtapeAffichee, modePhaseChoisi)
  }, [cleEtapeAffichee, playerId, spectateur, modePhaseChoisi])
  /**
   * DEUX INTENTIONS DIFFERENTES, QUE LE SEUL NOM « detaille » CONFONDAIT.
   *
   *  - `sceneCentrale` : le cartouche central joue la phase par-dessus la
   *    table (cartes rejouees dedans, question et ciblage dedans, revelation
   *    laissee au cartouche). C'est le mode « Detaille », et lui seul.
   *  - `unCartouche`   : une etape a la fois, un clic pour passer a la
   *    suivante. VRAI POUR « detaille » ET POUR « sur-table ».
   *
   * ⚠ La distinction n'est pas cosmetique : le moteur RETIENT ses trames dans
   * les deux modes (`decisionAccuse`), et seul le cartouche les relache. Un
   * mode qui retiendrait sans afficher de cartouche bloquerait la partie
   * jusqu'au filet anti-blocage de 90 secondes.
   */
  const sceneCentrale = modePhase === 'detaille'
  const unCartouche = modePhase !== 'instantane'
  /**
   * LE CARTOUCHE DU BAS (refonte du 04/10/2026) : la scene du mode « Étape par
   * étape », sur PC seulement. Le telephone garde le rendu d'avant (D36).
   */
  const nouvelleScenePC = sceneCentrale && modePlateau !== 'mobile'
  // LA DISTRIBUTION NE COUTE PLUS AUCUN CLIC (D15) : ses etapes sont retirees
  // AVANT le cartouche, et leur compte s'ecrit en tete de la pastille
  // « Cartes rencontre ». Rien ne change pour le rythme : `fusionnerDistribution`
  // retire des etapes, n'en fabrique aucune (piege 44). Place ICI, et non a
  // cote de `etapesPhaseMechant` : `nouvelleScenePC` n'existe qu'a partir
  // d'ici.
  const etapesPourLeCartouche = useMemo(
    () =>
      // Lot 5c (essai, decision 42) : la distribution devient UN tableau par joueur.
      phaseEssai
        ? {
            etapes: avecTableauDistribution(etapesPhaseMechant),
            cartesDistribuees: fusionnerDistribution(etapesPhaseMechant).cartesDistribuees,
          }
        : nouvelleScenePC
          ? fusionnerDistribution(etapesPhaseMechant)
          : { etapes: etapesPhaseMechant, cartesDistribuees: 0 },
    [phaseEssai, nouvelleScenePC, etapesPhaseMechant]
  )
  // Le compte des cartes distribuees, retenu pour la PHASE : le bilan le lit
  // apres que le round a tourne (voir `retenirCartesDistribuees`). Un `ref`
  // ecrit pendant le rendu, comme la memoire d'etapes de DeroulePhase : le
  // retenir ne doit provoquer aucun rendu.
  const distribueesRetenues = useRef<DistribueesRetenues>({ round: undefined, compte: 0 })
  distribueesRetenues.current = retenirCartesDistribuees(distribueesRetenues.current, {
    round: etat.monde?.round_id,
    compte: etapesPourLeCartouche.cartesDistribuees,
    enPhase: PHASES_DU_MECHANT.has(etat.monde?.phase ?? ''),
  })
  const cartesDistribuees = distribueesRetenues.current.compte
  const choisirModePhase = useCallback((mode: ModePhaseMechant) => {
    setModePhase(mode)
    ecrireModePhaseMechant(mode)
  }, [])

  /**
   * LE BANDEAU D'OUVERTURE JOUE SEUL, ET LA PHASE ATTEND QU'IL SOIT PARTI.
   *
   * Demande de l'utilisateur, 14/09/2026 : « d'abord le bandeau, puis apres on
   * montre la manigance. On attend que le bandeau soit parti. » Les deux se
   * superposaient : la premiere etape s'affichait pendant que le bandeau
   * passait encore par-dessus.
   *
   * ⚠ REMIS A « pas encore passe » A CHAQUE NOUVELLE PHASE, sur le round : il y
   * a une phase du mechant par round, et le bandeau rejoue a chacune. Sans cette
   * remise a zero, il ne serait attendu qu'a la toute premiere.
   */
  const [bandeauPasse, setBandeauPasse] = useState(false)
  const roundDuBandeau = useRef<number | undefined>(undefined)
  const roundCourant = etat.monde?.round_id ?? 0
  if (roundDuBandeau.current !== roundCourant) {
    roundDuBandeau.current = roundCourant
    if (bandeauPasse) setBandeauPasse(false)
  }

  // Le mode vit dans le composant, mais c'est le Moteur qui retient (ou non)
  // l'accuse de reception : il faut le lui redire a chaque changement. Avance
  // auto et vitesse, eux, ne le regardent pas : ils vont au cartouche.
  useEffect(() => {
    reglerModePhase(modePhase)
  }, [modePhase, reglerModePhase])

  // LE COUP FATAL SE VOIT AVANT L'ECRAN DE FIN.
  //
  // « Defaite en pleine phase : le coup fatal s'affiche normalement et c'est
  // APRES validation que vient l'ecran de fin. On comprend ce qui nous a
  // tues. » Le code faisait l'inverse : le cartouche et l'ecran de fin
  // basculaient sur la MEME trame (`monde.game_over`), et l'etape qui avait tue
  // n'etait jamais lue (constat M5 de l'audit du 06/09/2026).
  //
  // La retenue ne vaut QUE pour le siege dont le heros est tombe, et qu'en
  // mode Detaille : la table des autres joueurs n'attend rien, et le mode
  // Instantane n'a pas d'etape a montrer. La decision elle-meme est pure
  // (`afficherFinDePartie`, board/fin-partie.ts), avec son filet de temps.

  // QUI L'ON ATTEND, quand le plateau ne bouge plus (constat F5).
  //
  // Le moteur n'avance qu'une fois TOUS les clients a jour (`WaitSync`) et
  // n'interroge qu'un joueur a la fois. Trois facons de le savoir, une seule
  // mention a l'ecran. Les regles sont pures et testees dans
  // `board/attente-table.ts` ; ici, on ne fait que les alimenter.
  const phaseMechantEnCours = PHASES_DU_MECHANT.has(etat.monde?.phase ?? '')
  // Meme repere que `libelleRound` (board/etat-partie.ts) : la partie n'a pas
  // encore commence tant que `round_id` n'est pas un nombre strictement
  // positif (mise en place, mulligans).
  const enMiseEnPlace = typeof etat.monde?.round_id !== 'number' || etat.monde.round_id <= 0

  // Sauvegarde automatique a chaque debut de phase (24/09/2026, demande de
  // l'utilisateur). Filet de securite EN PLUS des trois emplacements manuels
  // (board/sauvegardes.ts), jamais a leur place : fichier DEDIE
  // (`save_auto.json`), construit avec le meme `dossierSauvegardes()` que
  // `sauverSlot`. Fire-and-forget : une sauvegarde manquee ne doit jamais se
  // voir ni gener la partie. Le premier rendu ne compte pas comme « nouvelle
  // phase » (`dernierePhaseSauvee.current === undefined`), sinon chaque
  // arrivee sur l'ecran (montage, reconnexion) declencherait une ecriture
  // pour rien.
  const [sauvegardeAuto, setSauvegardeAuto] = useState(lireSauvegardeAuto)
  const basculerSauvegardeAuto = useCallback(() => {
    setSauvegardeAuto((a) => {
      const nouveau = !a
      ecrireSauvegardeAuto(nouveau)
      return nouveau
    })
  }, [])
  const dernierePhaseSauvee = useRef<string | undefined>(undefined)
  useEffect(() => {
    const phase = etat.monde?.phase
    if (!phase || !sauvegardeAuto) return
    if (dernierePhaseSauvee.current === undefined) {
      dernierePhaseSauvee.current = phase
      return
    }
    if (dernierePhaseSauvee.current === phase) return
    dernierePhaseSauvee.current = phase
    void dossierSauvegardes()
      .then((dossier) => fetch(`/debug?/save ${dossier}save_auto.json`))
      .catch(() => undefined)
  }, [etat.monde?.phase, sauvegardeAuto])

  const nomsHerosParJoueur = useMemo(
    () =>
      (etat.monde?.players ?? []).map((joueur) =>
        joueur.area_hero?.[0]?.name?.replace(/^\W*/, '')
      ),
    [etat.monde?.players]
  )
  // Y A-T-IL SEULEMENT QUELQU'UN D'AUTRE ? Le drapeau `?multi=1` dit d'ou
  // vient la table, pas combien de joueurs y sont assis : le salon lance tres
  // bien une table a UN siege, et ce joueur-la lisait « En attente d'un autre
  // joueur » des que le plateau restait muet deux secondes et demie. On compte
  // donc les sieges (regle pure et testee, `tablePartagee`).
  const tableAPlusieurs = tablePartagee({
    multijoueur: estMultijoueur(),
    nombreDeSieges: etat.monde?.players?.length ?? 0,
  })
  // Cas 1 : le moteur interroge un AUTRE siege. La seule attente dont il dise
  // le nom (`ask_players[0]`, pousse a tous les clients).
  const autreJoueurInterroge = joueurAttendu({
    joueurDemande: etat.joueurDemande,
    playerId,
    multijoueur: tableAPlusieurs,
    nomsHerosParJoueur,
  })
  // Cas 2 : un autre siege n'a pas encore accuse reception de la trame
  // retenue (`sieges_non_acquittes`). Sur un moteur qui le publie, on nomme
  // le retardataire sans attendre le silence ci-dessous.
  const autreJoueurEnRetard = joueurEnRetard({
    siegesNonAcquittes: etat.siegesNonAcquittes,
    playerId,
    multijoueur: tableAPlusieurs,
    nomsHerosParJoueur,
  })
  // Cas 3 : plus rien n'arrive, et le moteur ne dit pas encore qui est en
  // retard (`siegesNonAcquittes` absent, moteur ancien). C'est alors tout ce
  // qu'un client peut savoir du retard d'un autre. On ne guette QUE lorsqu'on
  // n'a plus rien a faire de notre cote : trame relachee, aucune question en
  // cours, et aucune des deux reponses precedentes.
  const tableSilencieuse = useTableSilencieuse(
    etat.monde?.render_id,
    tableAPlusieurs &&
      etat.connecte &&
      phaseMechantEnCours &&
      etat.trameRetenue === undefined &&
      etat.demande === undefined &&
      autreJoueurInterroge === undefined &&
      etat.siegesNonAcquittes === undefined
  )
  const attendUnAutreJoueur =
    autreJoueurInterroge !== undefined || autreJoueurEnRetard !== undefined || tableSilencieuse

  // Les deux faces des heros de CE NAVIGATEUR, et non de la vue affichee :
  // regarder la table d'un autre ne fait pas de nous ce joueur.
  //
  // Hors multijoueur, ce navigateur tient TOUS les sieges (meme regle que
  // `joueurAttendu` ci-dessus) : ne lire que `?p=` faisait manquer le coup
  // fatal des qu'une partie a deux heros sur un ecran se terminait sur la
  // chute de l'autre. La regle est pure et testee (`herosLocaux`,
  // board/fin-partie.ts) ; ici, on ne fait que l'alimenter.
  const herosLocauxIds = useMemo(
    () =>
      herosLocaux({
        joueurs: etat.monde?.players,
        playerId,
        multijoueur: estMultijoueur(),
      }),
    [etat.monde?.players, playerId]
  )

  /**
   * LES IDENTITES DES AUTRES JOUEURS, pour savoir quelles etapes ne sont pas
   * les miennes.
   *
   * ⚠ ON NE PEUT PAS LE DEDUIRE DE `herosLocauxIds` SEUL. « Une cible qui n'est
   * pas mon heros » designe aussi la manigance principale, un sbire, un allie :
   * declencher l'avance automatique la-dessus ferait defiler toute la phase.
   * Il faut la liste des IDENTITES, et rien qu'elle.
   *
   * ⚠ VIDE EN SOLO ET EN HOT-SEAT, ou tous les heros sont locaux. La regle qui
   * s'en sert ne joue donc qu'en vrai multijoueur, et ne peut rien casser
   * ailleurs.
   */
  const herosDesAutresIds = useMemo(() => {
    const autres = new Set<number>()
    for (const joueur of etat.monde?.players ?? []) {
      for (const carte of joueur.area_hero ?? []) {
        const famille = kindOf(carte)
        if (famille !== 'hero' && famille !== 'alter-ego') continue
        if (!herosLocauxIds.has(carte.id)) autres.add(carte.id)
      }
    }
    return autres
  }, [etat.monde?.players, herosLocauxIds])

  const partieFinieMoteur = Boolean(etat.monde?.game_over)
  const coupFatalAMontrer =
    unCartouche && coupFatalLocal(etapesPhaseMechant, herosLocauxIds)
  // Le joueur a valide l'etape du coup fatal (« Continuer »), et le filet de
  // temps qui laisse paraitre l'ecran de fin quoi qu'il arrive.
  //
  // Les deux se remettent a faux a chaque NOUVELLE PARTIE, et il a fallu le
  // dire : « une nouvelle partie remonte tout le plateau » etait faux.
  // `PagePartie` n'est monte qu'une fois par chargement de page, sans `key`
  // (voir la fin de ce fichier) ; « Rejouer » enchaine donc une seconde partie
  // sur le meme etat. `coupFatalVu` restait vrai, `afficherFinDePartie` rendait
  // vrai des la trame de `game_over`, et le coup fatal n'etait plus jamais
  // montre a partir de la deuxieme partie (relecture A4). Meme motif et meme
  // source que la remise a zero du cartouche : `etat.partieId`.
  const [coupFatalVu, setCoupFatalVu] = useState(false)
  const [filetFinEcoule, setFiletFinEcoule] = useState(false)
  useEffect(() => {
    setCoupFatalVu(false)
    setFiletFinEcoule(false)
  }, [etat.partieId])
  const finPartieAffichee = afficherFinDePartie({
    partieFinie: partieFinieMoteur,
    coupFatalAMontrer,
    coupFatalVu,
    filetEcoule: filetFinEcoule,
  })

  useEffect(() => {
    if (!partieFinieMoteur || !coupFatalAMontrer || coupFatalVu || filetFinEcoule) return
    const minuteur = window.setTimeout(() => setFiletFinEcoule(true), DELAI_FILET_FIN_PARTIE_MS)
    return () => window.clearTimeout(minuteur)
  }, [partieFinieMoteur, coupFatalAMontrer, coupFatalVu, filetFinEcoule])

  // usePasAPas (halo teinte + chiffre flottant sur la carte de l'etape en
  // cours) : DEBRANCHEE a la demande de l'utilisateur - double emploi avec le
  // cartouche du deroule (MENACE / ACTIVATIONS / DISTRIBUTION / RÉVÉLATION),
  // exactement le defaut corrige entre le bandeau et le splash. pas-a-pas.ts
  // reste en place : il suffit de reimporter `usePasAPas` depuis
  // './board/pas-a-pas' et de remettre la ligne suivante pour la rallumer,
  // avec pour second argument « une trame est retenue »
  // (etat.trameRetenue !== undefined).
  // usePasAPas(historique.entrees, etat.trameRetenue !== undefined)

  // Espace n'a plus de role ici : la pause du moteur a disparu avec son
  // minuteur de lecture (le cartouche tient la seule horloge de la phase), et
  // c'est DeroulePhase qui prend Espace pour avancer d'une etape.

  // Le recap de fin de phase ne sert QU'EN INSTANTANE (voir son montage plus
  // bas). En detaille, c'est le cartouche du deroule qui raconte la phase et
  // qui la clot par son propre bilan.

  const [musique, setMusique] = useState(lireMusiqueActive)
  const basculerMusique = useCallback(() => {
    setMusique((m) => {
      const nouveau = !m
      try {
        window.localStorage.setItem(CLE_MUSIQUE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [revelation, setRevelation] = useState<ModeRevelation>(lireRevelation)
  // La fenetre des reglages (board/FenetreReglages.tsx). ⚠ Volontairement PAS
  // retenue entre deux parties : on ne veut pas rouvrir un ecran de reglages
  // par-dessus le plateau au chargement.
  const [reglagesOuvertsLocal, setReglagesOuverts] = useState(false)
  // LA TABLE PERSONNALISABLE (04/10/2026) : une disposition par nombre de
  // joueurs (table-perso.ts), et celle qu'on edite (`origine` : « Disposition
  // d'origine » a ete choisie, « Terminer » efface alors le choix).
  const nombreDeJoueurs = Math.max(1, etat.monde?.players?.length ?? 1)
  const dispositionTable = useDispositionTable(nombreDeJoueurs)
  const [editionTable, setEditionTable] = useState<{ d: Disposition; origine: boolean }>()
  // Refonte du header (24/09/2026) : trois nouvelles modales, meme famille que
  // `reglagesOuverts` (jamais retenues entre deux parties, memes raisons).
  //
  // ⌂ Menu (fusion « Menu » + « Deconnexion complete ») : un choix, pas un
  // clic direct -- demande de l'utilisateur, capture a l'appui, apres avoir
  // vu ces deux actions confondues sur le meme ecran.
  const [menuOuvertLocal, setMenuOuvert] = useState(false)
  // ▶ Partie (ex-PopoverPartie) : promue en fenetre centree comme
  // `FenetreReglages`, au lieu d'un popover ancre a son bouton -- son
  // declencheur vit maintenant DANS la modale « Plus d'options » ci-dessus,
  // qui se ferme avant de l'ouvrir (« lanceurs simples », pas de menu
  // imbrique dans un menu -- exactement le defaut deja corrige le 14/09/2026
  // sur ce meme bouton, voir le commentaire de PopoverPartie plus bas).
  const [partieOuverteLocale, setPartieOuverte] = useState(false)
  const ouvrirVolet = useCallback(() => setPartieOuverte(true), [])
  const fermerVolet = useCallback(() => setPartieOuverte(false), [])
  // L'aide du mode manuel s'ouvre toute seule a chaque passage en manuel, SUR
  // PC seulement (tablette et telephone : elle couvrait la main, 06/10/2026) ;
  // la main la ferme, et la languette la rouvre tant qu'on est en manuel.
  const [aideManuelOuverteLocale, setAideManuelOuverte] = useState(false)
  // Lots 3 et 4 du 07/10/2026 : cibles, flèches et surlignages du manuel, vus de tous (spectateur compris).
  const marquesManuel = useMarques(manuel)
  const [aideAutoOuverteLocale, setAideAutoOuverte] = useState(false)
  // SES MENUS (08/10/2026) : Reglages, Menu, journal, volets d'aide, ouverts
  // chez le spectateur et en relecture comme chez lui (genre « menu »).
  const menusDuJoueur = useVuDuJoueur<MenusOuverts | null>('menu', spectateur ? joueurActif : undefined)
  // Celui qui regarde peut ouvrir les reglages DU JOUEUR, en lecture seule
  // (message du bouton de la barre du spectateur ou de la relecture).
  const [reglagesVus, setReglagesVus] = useState(false)
  useEffect(() => {
    if (!spectateur) return
    const recevoir = (message: MessageEvent) => {
      if (message.origin === window.location.origin && message.data?.type === 'reglages-du-joueur') setReglagesVus(true)
    }
    window.addEventListener('message', recevoir)
    return () => window.removeEventListener('message', recevoir)
  }, [spectateur])
  const reglagesOuverts = spectateur ? menusDuJoueur?.r === true || reglagesVus : reglagesOuvertsLocal
  const menuOuvert = spectateur ? menusDuJoueur?.m === true : menuOuvertLocal
  const partieOuverte = spectateur ? menusDuJoueur?.j === true : partieOuverteLocale
  const aideManuelOuverte = spectateur ? menusDuJoueur?.am === true : aideManuelOuverteLocale
  const aideAutoOuverte = spectateur ? menusDuJoueur?.aa === true : aideAutoOuverteLocale
  useEffect(() => {
    if (spectateur) return
    const menus: MenusOuverts = {
      r: reglagesOuvertsLocal,
      m: menuOuvertLocal,
      j: partieOuverteLocale,
      am: aideManuelOuverteLocale,
      aa: aideAutoOuverteLocale,
    }
    publierVu(joueurActif, 'menu', menus)
  }, [spectateur, joueurActif, reglagesOuvertsLocal, menuOuvertLocal, partieOuverteLocale, aideManuelOuverteLocale, aideAutoOuverteLocale])
  // Ses defilements (main, journal, piles...) : defilement-partage.ts.
  useEffect(() => (spectateur ? undefined : suivreDefilements(joueurActif)), [spectateur, joueurActif])
  useDefilementsDuJoueur(spectateur ? joueurActif : undefined)
  const ouvrirAideAuto = useCallback(() => setAideAutoOuverte(true), [])
  const fermerAideAuto = useCallback(() => setAideAutoOuverte(false), [])
  const ouvrirAideManuel = useCallback(() => setAideManuelOuverte(true), [])
  const fermerAideManuel = useCallback(() => setAideManuelOuverte(false), [])
  useEffect(() => {
    setAideManuelOuverte(manuel && aideSOuvreSeule())
  }, [manuel])
  // « REVOIR LA PHASE DU MÉCHANT » EN SCENE PC (D38) : le journal rouvre le
  // cartouche du bas en relecture. Elle se referme d'elle-meme quand la phase
  // du mechant reprend, ou quand un coup du mechant arrive pendant le tour :
  // le cartouche « Pendant ton tour » (et sa question de defense) passe avant.
  const [relectureJournal, setRelectureJournal] = useState(false)
  // « Pendant ton tour » montre un coup : la narration du centre se tait.
  const [horsPhaseAffiche, setHorsPhaseAffiche] = useState(false)
  useEffect(() => {
    if (phaseMechantEnCours) setRelectureJournal(false)
  }, [phaseMechantEnCours])
  const nombreDeCoupsPendantTonTour = coupsPendantTonTour.length
  useEffect(() => {
    setRelectureJournal(false)
  }, [nombreDeCoupsPendantTonTour])
  // Les essais reserves a un seul compte (board/essais.ts). ⚠ Faux tant que le
  // serveur n'a pas repondu : on n'ouvre jamais un essai « par defaut », le
  // temps d'un aller-retour reseau.
  const [essais, setEssais] = useState(false)
  useEffect(() => {
    let vivant = true
    void essaisOuverts().then((ouverts) => {
      if (vivant) setEssais(ouverts)
    })
    return () => {
      vivant = false
    }
  }, [])
  // La racine porte l'essai : sa feuille de style y coupe toute animation en
  // boucle (cartouche-essai.css).
  useEffect(() => {
    document.documentElement.classList.toggle('essai-phase-mechant', phaseEssai)
    document.documentElement.classList.toggle('phase-dynamique', phaseDynamique)
    document.documentElement.classList.toggle('phase-tris', phaseTris)
    return () => document.documentElement.classList.remove('essai-phase-mechant', 'phase-dynamique', 'phase-tris')
  }, [phaseEssai, phaseDynamique, phaseTris])
  // Refonte du 12/10/2026 (essai) : la couleur de chaque joueur, tiree de
  // l'aspect de son deck, et le joueur a qui appartient une carte de la table.
  const cadresJoueurs = useMemo(() => cadresDesJoueurs(etat.monde, catalogue), [etat.monde, catalogue])
  const joueurDeCarteMonde = useCallback((id: number | undefined) => joueurDeLaCarte(etat.monde, id), [etat.monde])
  // Refonte, lot 6 (multi) : le premier joueur du round, pour les moments communs
  // (« le joueur concerne, sinon le premier joueur »).
  const premierJoueurMonde = useMemo(() => {
    const rang = (etat.monde?.players ?? []).findIndex(
      (joueur) => ((joueur.area_hero ?? [])[0]?.info['k_first_player_token'] ?? 0) > 0
    )
    return rang === -1 ? undefined : rang
  }, [etat.monde])
  const nomsJoueursMonde = useMemo(
    () => (etat.monde?.players ?? []).map((joueur) => String((joueur.area_hero ?? [])[0]?.name ?? '').replace(/^[*✱\s]+/, '')),
    [etat.monde]
  )
  /**
   * LE FOND PREND LA COULEUR DU HEROS AFFICHE.
   *
   * ⚠ IL SUIT `joueurActif`, PAS LA PARTIE. En multijoueur, changer de vue
   * change la teinte : « quand on change de heros, la couleur doit changer »
   * (utilisateur, 14/09/2026). C'est aussi pour cela que la carte d'identite
   * est relue a chaque rendu : elle change de face quand on se transforme, et
   * les deux faces portent la meme palette.
   *
   * ⚠ RESERVE AUX ESSAIS tant que l'utilisateur ne l'a pas valide a l'usage :
   * sans le drapeau, la classe n'est pas posee et la CSS garde le fond uni.
   */
  const identite = identiteAffichee(etat.monde, joueurActif)
  // Le méchant en jeu : ses cartes (toutes les phases partagent la même palette), jointes en une
  // clé simple pour ne repartir que quand le méchant change.
  const clesMechant = identitesMechants(etat.monde).join(',')
  useEffect(() => {
    const racine = document.documentElement
    const corps = document.body
    let vivant = true
    if (!essais || !identite || affichage === 'sobre') {
      corps.classList.remove('a-halo-heros', 'a-marque-heros', 'a-marque-mechant')
      return
    }
    void palettes().then((catalogue) => {
      if (!vivant) return
      const couleurs: Couleur[] | undefined = catalogue[identite]
      // Le méchant : la première de ses cartes en jeu qui porte une palette (deux couleurs).
      const cleMechant = clesMechant.split(',').find((id) => id && (catalogue[id]?.length ?? 0) > 0)
      const couleursMechant: Couleur[] | undefined = cleMechant ? catalogue[cleMechant] : undefined
      if (!couleurs || couleurs.length === 0) {
        corps.classList.remove('a-halo-heros', 'a-marque-heros', 'a-marque-mechant')
        return
      }
      // EPURE : trois bandes plates au coin, jamais le halo (affichage-epure.css).
      if (affichage === 'epure') {
        racine.style.setProperty('--marque-heros', marqueDe(couleurs) ?? 'none')
        racine.style.setProperty('--marque-mechant', marqueMechantDe(couleursMechant) ?? 'none')
        corps.classList.toggle('a-marque-mechant', Boolean(couleursMechant))
        // Les deux premieres couleurs du heros, en accent (16/10/2026, « epure mais pas mort ») :
        // le liseré sous les bandeaux (affichage-epure.css, §15).
        const [c1, c2] = [couleurs[0], couleurs[1] ?? couleurs[0]]
        racine.style.setProperty('--ep-heros-1', `rgb(${c1[0]},${c1[1]},${c1[2]})`)
        racine.style.setProperty('--ep-heros-2', `rgb(${c2[0]},${c2[1]},${c2[2]})`)
        corps.classList.remove('a-halo-heros')
        corps.classList.add('a-marque-heros')
        return
      }
      corps.classList.remove('a-marque-heros', 'a-marque-mechant')
      racine.style.setProperty(
        '--fond-plateau',
        fondDe(
          couleurs,
          'var(--fond-halo-base, linear-gradient(180deg, rgba(14,18,24,0.96), rgba(6,6,8,0.98)))',
          couleursMechant
        )
      )
      corps.classList.add('a-halo-heros')
    })
    return () => {
      vivant = false
    }
  }, [essais, identite, clesMechant, affichage])
  const cyclerRevelation = useCallback(() => {
    setRevelation((r) => {
      const suivant: ModeRevelation = r === 'off' ? 'court' : r === 'court' ? 'long' : 'off'
      try {
        window.localStorage.setItem(CLE_REVELATION, suivant)
      } catch {
        /* preference non critique */
      }
      return suivant
    })
  }, [])

  // Resynchronisation massive (Undo, reconnexion, remelange...) : le moteur
  // repart d'un `render_id` plus bas que le dernier vu (`GameSession.Undo`
  // relance toute la partie et rejoue l'historique depuis zero, cote
  // Fusion/marvel-lcg-src/src/game/game_run/game_session.py). Le plateau
  // recoit alors un etat entierement neuf, indiscernable pour lui d'une
  // vraie nouveaute : tout semblait « reclaquer » d'un coup (demande de
  // l'utilisateur, 28/09/2026). On le detecte par la seule baisse du
  // render_id — une hausse, meme un grand saut, reste un rendu normal (voir
  // CoucheAnimations.tsx) — et on coupe brievement les memes animations
  // d'entree que le reglage « sans animations », le temps qu'un rendu
  // s'affiche sans jouer ses entrees.
  const dernierRenderId = useRef<number | undefined>(undefined)
  const [resynchronisation, setResynchronisation] = useState(false)
  useEffect(() => {
    const actuel = etat.monde?.render_id
    if (actuel === undefined) return
    const precedent = dernierRenderId.current
    dernierRenderId.current = actuel
    // Un saut dans la relecture se pose sans rejouer ses entrees, comme une resynchronisation.
    if (!estResynchronisation(actuel, precedent) && etat.saut !== true) return
    setResynchronisation(true)
    // 1000ms : couvre la plus longue animation d'entree gardee par
    // `plateau-sans-animations` (statut-arrive, 900ms) avec une marge.
    const t = window.setTimeout(() => setResynchronisation(false), 1000)
    return () => window.clearTimeout(t)
  }, [etat.monde?.render_id, etat.saut])

  // Les effets CSS transitoires (secousse d'impact, halo de statut) sont
  // debrayes par une classe sur <body> : ils vivent dans des feuilles de style,
  // pas dans des composants qu'on peut couper par prop.
  useEffect(() => {
    document.body.classList.toggle('plateau-sans-animations', !animationsActives || resynchronisation)
    return () => document.body.classList.remove('plateau-sans-animations')
  }, [animationsActives, resynchronisation])

  // Le plateau descend sous la barre du spectateur, et les feuilles de style
  // ont besoin de le savoir : meme motif que ci-dessus.
  useEffect(() => {
    // Dans le cadre, la barre du spectateur est DEHORS (PageSpectateur) : le
    // plateau garde la place exacte qu'il avait chez le joueur.
    document.body.classList.toggle('est-spectateur', spectateur && !estCadre())
    document.body.classList.toggle('est-cadre', estCadre())
    const retirerVitre = spectateur ? poserVitre() : undefined
    return () => {
      document.body.classList.remove('est-spectateur')
      document.body.classList.remove('est-cadre')
      retirerVitre?.()
    }
  }, [spectateur])

  // Dans le cadre du direct : la barre du spectateur, dehors, a besoin du
  // nombre de sieges et de la fin de partie.
  const siegesDuMonde = etat.monde?.players?.length ?? 1
  const termineePourLaBarre = partieFinieMoteur || (!etat.connecte && etat.monde !== undefined)
  const raisonPourLaBarre = partieFinieMoteur
    ? etat.monde?.game_over_reason || undefined
    : !etat.connecte
      ? t('La table s’est éteinte')
      : undefined
  useEffect(() => {
    if (!spectateur || !estCadre() || window.parent === window) return
    window.parent.postMessage(
      { type: 'etat-spectateur', sieges: siegesDuMonde, terminee: termineePourLaBarre, raison: raisonPourLaBarre },
      window.location.origin
    )
  }, [spectateur, siegesDuMonde, termineePourLaBarre, raisonPourLaBarre])

  // CE QUE LE JOUEUR VOIT (vu-partage.ts) : la taille de son ecran et ses
  // reglages, pour que le cadre du spectateur et de la relecture les reprenne.
  useEffect(() => {
    if (spectateur) return
    const publierEcran = () => publierVuLimite(joueurActif, 'ecran', { w: window.innerWidth, h: window.innerHeight }, 300)
    const publierReglages = () => publierVu(joueurActif, 'regl', reglagesDuJoueur())
    publierEcran()
    publierReglages()
    window.addEventListener('resize', publierEcran)
    const minuteur = window.setInterval(publierReglages, 2000)
    return () => {
      window.removeEventListener('resize', publierEcran)
      window.clearInterval(minuteur)
    }
  }, [spectateur, joueurActif])


  // Le voile d'ouverture : on ne montre pas la table en train de se monter.
  // Levé une fois pour toutes dès que la question de la manigance arrive.
  //
  // ⚠ TANT QUE `etat.monde` N'EST PAS ENCORE ARRIVE, ON NE DECIDE RIEN. Avant
  // la premiere trame du moteur, `confirm_main_scheme` est forcement absent :
  // le lire comme un « non » figerait le voile a leve des la toute premiere
  // image (avant meme de savoir si une question est attendue), et il ne se
  // relevrait plus jamais une fois le monde charge. Le garde-fou `!etat.monde`
  // de la ligne suivante affiche deja le meme message de connexion : ne pas
  // toucher au verrou tant qu'on n'a pas encore de reponse du moteur ne change
  // rien a l'affichage de cette phase-la, et evite ce verrouillage premature.
  const voileLeve = useRef(false)
  // ⚠ UNE SEULE CONDITION, DES DEUX COTES. `priseDuPanneauManigance` dit A LA
  // FOIS que le panneau revendique la question et quelle carte il montre : la
  // revendication et le montage ne peuvent plus diverger. Quand la carte est
  // introuvable, le panneau rend la main aux panneaux ORDINAIRES au lieu de
  // laisser le joueur devant une question sans un seul bouton.
  //
  // La carte a montrer est celle que la QUESTION designe par son `bind_id`, pas
  // la premiere de la zone : le mode Bataille en met deux en jeu, et le moteur
  // pose une question par manigance (voir maniganceAMontrer).
  const priseManigance = priseDuPanneauManigance(etat.demande, etat.monde)
  const voile = etat.monde
    ? ouvertureEncoreVoilee({
        confirmAttendue: etat.monde.confirm_main_scheme === true,
        round: etat.monde.round_id ?? 0,
        // Le VOILE se leve des que la question arrive, prise par le panneau ou
        // non : si elle reste aux panneaux ordinaires, il faut d'autant plus
        // voir la table pour y repondre.
        questionArrivee: questionDeLaManigance(etat.demande) !== undefined,
        dejaLevee: voileLeve.current,
        demandePresente: etat.demande !== undefined,
        // Une partie finie leve le voile : sans cette porte, une partie
        // terminee pendant la mise en place restait sur « Connexion a la
        // partie… », le retour anticipe du voile passant AVANT l'ecran de fin.
        partieFinie: partieFinieMoteur,
      })
    : false
  if (etat.monde && !voile) voileLeve.current = true

  // La mise en place carte par carte (10/10/2026) : chaque carte qui arrive en
  // jeu se montre en grand, dans l'ordre, et attend « Continuer ». Le panneau
  // de la manigance attend que la file soit vide pour parler a son tour.
  // Seulement dans le mode « Étape par étape » (l'ancien Bis, 10/10/2026).
  const miseEnPlaceMuette = !sceneCentrale || spectateur || estRelecture() || modeManuelDeclare
  const miseEnPlace = useMiseEnPlacePasAPas(etat.monde, {
    // Une partie finie pendant la mise en place ne la montre plus : l'écran de
    // fin passait SOUS la carte en attente (vu en essai à deux, 13/10/2026).
    enCours: enMiseEnPlace && !partieFinieMoteur,
    voile,
    muet: miseEnPlaceMuette,
  })
  // La table ne montre que ce qui a eu son « Continuer » (13/10/2026) : places
  // en pointilles, jetons et face de manigance d'avant. La manigance que le
  // panneau presente attend aussi.
  const panneauEnAttente = enMiseEnPlace && !miseEnPlaceMuette && !voile ? priseManigance?.carte.id : undefined
  const attenteMep = useMemo(
    () => attenteSurTable(miseEnPlace.enAttente, panneauEnAttente),
    [miseEnPlace.enAttente, panneauEnAttente]
  )
  const mondeAffiche = mondeTable ?? etat.monde
  const mondeSurTable = useMemo(
    () => (mondeAffiche ? avecFacesDAvant(avecCompteursFiges(mondeAffiche, attenteMep.figes), attenteMep.faces) : undefined),
    [mondeAffiche, attenteMep]
  )
  const plateauSurTable = useMemo(
    () =>
      mondeSurTable && mondeSurTable !== mondeAffiche
        ? construirePlateau(mondeSurTable, {
            playerId: joueurActif,
            viewerId: playerId,
            catalogue,
            seulCeJoueur: vueForcee !== null || modePlateau === 'mobile',
          })
        : undefined,
    [mondeSurTable, mondeAffiche, joueurActif, playerId, catalogue, vueForcee, modePlateau]
  )
  // 1A et 2A avant les mechants (livret, etape 10 ; decision du 10/10/2026) :
  // le panneau de la manigance principale passe devant un mechant en file.
  const panneauPrioritaire = panneauAvantLaFile(miseEnPlace.etape, priseManigance?.carte)
  const mechantRetenu = mechantAttendLaQuestion(miseEnPlace.etape, {
    enMiseEnPlace,
    confirmPrincipale: etat.monde?.confirm_main_scheme === true,
    demandePresente: etat.demande !== undefined,
  })

  // ⚠ LE SILENCE DE L'OUVERTURE VAUT AUSSI POUR LES SONS. Ce hook est appele
  // AVANT le retour anticipe du voile — les hooks ne se sautent pas — et
  // chaque trame de mise en place portant un `sound_name` etait jouee derriere
  // le voile. C'est la seule raison pour laquelle le bloc du voile est calcule
  // ici, au-dessus, et pas juste avant le retour anticipe qui s'en sert.
  useSons(
    etat.monde,
    sons,
    etat.demande !== undefined,
    voile || etat.saut === true || (lecteurActif()?.lireControle().muet ?? false),
    phaseMechantEnCours && !sceneCentrale ? 0.6 : 1
  )
  // Survol des boutons du Menu et des Réglages (refonte des sons, 07/10/2026).
  useEffect(() => installerSurvol(document, SELECTEUR_SURVOL_PLATEAU), [])
  useMusique(etat.monde, musique)

  // Raccourcis clavier : E = fin du tour (quand le bouton simple est visible),
  // Espace = fin du tour (des que le bouton complet est cliquable, meme hors
  // mode simple -- demande de l'utilisateur, 24/09/2026, inspire de MTG
  // Arena), U = annuler la derniere action. Ignorés pendant une saisie ou
  // avec un modificateur. HOOKS DECLARES ICI, avant le retour anticipe
  // « monde pas charge » : sinon le nombre de hooks change entre deux rendus
  // (React #310). La cible reelle des raccourcis E et Espace est assignee
  // plus bas, une fois `afficherFinTourSimple`/`finDeTourDisponible` connus,
  // via ces refs.
  const finTourClavier = useRef<() => void>(() => {})
  const finTourClavierEspace = useRef<() => void>(() => {})
  // Même mécanique pour B : l'écoute est installée une fois, sa cible change à
  // chaque monde reçu. Sans le ref, l'effet se réinstallerait à chaque rendu.
  const rapportClavier = useRef<() => void>(() => {})
  const annulerClavier = useRef<() => void>(() => {})
  const echapClavier = useRef<() => void>(() => {})
  // Echap ecoute en CAPTURE sur la fenetre : il passe avant les fenetres qui
  // se ferment a Echap, et laisse la touche a celle qui est ouverte
  // par-dessus. L'annulation ne vient qu'au Echap suivant.
  useEffect(() => {
    const surEchap = (evenement: KeyboardEvent) => {
      if (evenement.key !== 'Escape' || evenement.ctrlKey || evenement.metaKey || evenement.altKey) return
      const cible = evenement.target as HTMLElement | null
      if (cible && (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)) return
      if (document.querySelector(OUVERT_PAR_DESSUS)) return
      // Le cartouche du mechant a deja son Echap : le refus (decision D37).
      if (cibleDeLaTouche('Escape', document.querySelector('.deroule-phase.est-scene'))) return
      echapClavier.current()
    }
    window.addEventListener('keydown', surEchap, true)
    return () => window.removeEventListener('keydown', surEchap, true)
  }, [])
  useEffect(() => {
    const surTouche = (evenement: KeyboardEvent) => {
      if (evenement.ctrlKey || evenement.metaKey || evenement.altKey) return
      const cible = evenement.target as HTMLElement | null
      if (cible && (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)) return
      const touche = evenement.key.toLowerCase()
      if (touche === 'e') {
        finTourClavier.current()
      } else if (touche === ' ') {
        // Empeche a la fois le defilement de page (comportement natif de la
        // barre espace) et un second declenchement si le focus se trouve deja
        // sur le bouton Fin du tour (qui s'active lui-meme a l'espace).
        evenement.preventDefault()
        finTourClavierEspace.current()
      } else if (touche === 'u') {
        annulerClavier.current()
      } else if (touche === 'b') {
        // « B » comme bug : copie les 20 dernières entrées SANS ouvrir le
        // panneau, parce que le symptôme peut disparaître au rendu suivant.
        rapportClavier.current()
      }
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [])
  rapportClavier.current = () => void rapport.copier('recent')

  // Installée une fois pour la vie de la page : une erreur de rendu survenue
  // AVANT l'ouverture du panneau doit quand même figurer au rapport.
  useEffect(() => installerCollecteErreurs(), [])

  useHaloStatut(etat.monde, animations)

  const annulerGesteManuel = triche.annulerDernierGeste
  const annulerCoup = useCallback(() => {
    // En manuel, on défait le dernier GESTE, comme Ctrl+Z (lot 1, 06/10/2026) :
    // « /undo auto » rejouerait la partie jusqu'au dernier coup du moteur.
    if (manuel) {
      annulerGesteManuel()
      return
    }
    // « /undo auto » remonte au dernier point de decision, comme le bouton Undo
    // du client d'origine. L'espace est encode par fetch, le '/' est conserve.
    fetch('/debug?/undo auto').catch(() => undefined)
  }, [manuel, annulerGesteManuel])
  annulerClavier.current = annulerCoup

  // ANNULER L'ACTION EN COURS (croix de la boite de question, touche Echap).
  // `/undo action` remonte a la question du tour ou la carte a ete choisie,
  // quel que soit le nombre de sous-questions deja repondues ; U, lui, ne
  // remonte que d'une decision.
  const annulerAction = useCallback(() => {
    fetch('/debug?/undo action').catch(() => undefined)
  }, [])
  echapClavier.current = () => {
    if (manuel || spectateur || telephone) return
    // Une action encore en composition (cible, paiement) n'a rien envoye au
    // moteur : on l'abandonne cote plateau, sans rien rejouer.
    if (interaction.option) {
      interaction.abandonnerOption()
      return
    }
    if (etat.aNous && etat.demande?.annuler_action) annulerAction()
  }
  // Ton tour, attaque subie, action validee : trois vibrations (zone 3).
  useVibrationsDePartie(etat.monde, playerId, telephone && !spectateur)

  // Sortir du plein ecran AVANT de naviguer (spec mobile §6.3) : sinon
  // l'assistant s'ouvre encore en plein ecran, sans barre d'adresse.
  // L'invité d'une table répartie retourne à SON salon, pas à l'assistant de
  // l'hôte (13/10/2026, board/retour-salon.ts).
  const navigateurTable = { siege: playerId, multi: estMultijoueur(), spectateur }
  const inviteDeTable = estInviteDeTable(navigateurTable)
  const adresseRetour = adresseApresPartie(navigateurTable)
  const retourMenu = useCallback(() => {
    quitterPleinEcran()
    atterrir(adresseRetour)
  }, [adresseRetour])
  // Resté sur l'écran de fin, l'invité rejoint son salon dès que l'hôte prépare la suivante.
  useRetourAuSalon(Boolean(finPartieAffichee) && inviteDeTable, playerId)

  // ⌂ QUITTER, C'EST FERMER LA TABLE (21/09/2026), et non plus seulement
  // changer d'écran. Le pourquoi — le salon qui expédiait les invités sur
  // l'ANCIENNE partie tant que la table en portait une — est écrit en tête de
  // `board/quitter-la-table.ts`. Ce même bouton sert sur mobile :
  // `BandeauPortrait` rend le `.board-actions` du plateau tel quel, donc ce
  // `onClick`-ci.
  const retourMenuPrincipal = useCallback(async () => {
    // ⚠ L'ADRESSE EST DÉJÀ LÀ, LUE AU MONTAGE. La lire ICI la mettait dans le
    // chemin du clic : un moteur qui traîne laissait la fenêtre ne jamais
    // s'ouvrir, et un `fetch` en échec faisait passer l'hôte pour un joueur
    // local — donc repartir sans rien fermer, défaut d'origine rétabli en
    // silence.
    const nature = natureDuDepart({ siege: playerId, spectateur, site })
    // ⚠ ON ANNONCE CE QUI VA VRAIMENT SE PASSER. « La partie en cours sera
    // perdue » ne dit rien d'une table qui disparaît avec ses invités dedans.
    // Et quand on ne SAIT pas, on le dit aussi : c'est la troisième réponse.
    const accepte = await confirmer({
      titre:
        nature === 'fermeture'
          ? t('Fermer la table ?')
          : nature === 'incertain'
            ? t('Quitter la partie ?')
            : t('Revenir au menu principal ?'),
      texte:
        nature === 'fermeture'
          ? t(
              'La table va disparaître : les autres joueurs sont déconnectés, et il faudra en rouvrir une depuis le site pour rejouer. La partie en cours est mise de côté — le site te la proposera sous « Reprendre ».'
            )
          : nature === 'incertain'
            ? t(
                'Si cette table vient du site, elle va se fermer : les autres joueurs seront déconnectés et il faudra en rouvrir une pour rejouer. Le plateau n’a pas pu le vérifier.'
              )
            : t('La partie en cours sera perdue si tu ne l’as pas sauvegardée.'),
      confirmer: t('Quitter'),
      ton: 'danger',
    })
    if (!accepte) return
    if (nature === 'simple') {
      quitterPleinEcran()
      atterrir('/prepare.html')
      return
    }
    const depart = await fermerLaTable()
    if (depart.issue === 'fermee') {
      // Sortir du plein écran AVANT de naviguer (spec mobile §6.3), et surtout
      // vers le SITE : le moteur qui servait cette page n'existe déjà plus.
      quitterPleinEcran()
      atterrir(depart.url)
      return
    }
    if (depart.issue === 'sans-site') {
      // Il n'y avait rien à fermer : le moteur est toujours là, et son écran
      // des héros avec lui.
      quitterPleinEcran()
      atterrir('/prepare.html')
      return
    }
    if (depart.issue === 'refusee') {
      // ⚠ LA SEULE ISSUE OÙ L'ON PEUT AFFIRMER QUE RIEN N'A BOUGÉ : le moteur
      // a refusé avant d'appeler qui que ce soit.
      const quandMeme = await confirmer({
        titre: t('Cette table n’est pas la tienne à fermer.'),
        texte: t('Seul l’hôte peut la fermer. Rien n’a été touché.'),
        confirmer: t('Revenir au menu quand même'),
        annuler: t('Rester sur la partie'),
      })
      if (!quandMeme) return
      quitterPleinEcran()
      atterrir('/prepare.html')
      return
    }
    // ⚠ ISSUE INCONNUE, ET ON N'AFFIRME RIEN. Le site révoque le mot de passe
    // et lance l'extinction AVANT de répondre : son silence ne veut pas dire
    // qu'il n'a rien fait, c'est même le contraire qui est probable. Dire
    // « rien n'a été détruit » serait un mensonge, et proposer de rester sur
    // la partie, une impasse sur un moteur condamné. On donne l'adresse du
    // site, seul endroit où la réponse existe.
    const allerVoir = await confirmer({
      titre: t('La table est peut-être en train de se fermer.'),
      texte: t(
        'Le site n’a pas répondu à temps. Impossible de dire d’ici si la table est fermée ou non : le site, lui, le sait.'
      ),
      confirmer: t('Ouvrir le site'),
      annuler: t('Rester ici'),
    })
    if (!allerVoir) return
    quitterPleinEcran()
    // Trois sources, de la mieux informée à la dernière chance : ce que le
    // moteur vient de dire, ce qu'il avait dit au montage, et à défaut
    // l'adresse déduite de la nôtre. ⚠ Un 502 ne porte aucun corps : c'est
    // précisément le cas où `depart.url` est vide alors qu'on connaît le site
    // depuis le début.
    atterrir(depart.url || site.url || lienAccueil())
  }, [confirmer, playerId, site, spectateur])

  // Ce que le toast dit de chaque carte touchee : voir `phrases-effets.ts` (un statut n'est pas de la menace).
  const toastsEffets = useMemo(() => {
    const toasts: ToastEffet[] = []
    for (const [id, effet] of effets) {
      const carte = cartesMondeParId.get(id)
      if (!carte) continue
      // Narration ecrite ici, pas envoyee par le moteur : elle doit donc suivre
      // la langue du client comme le reste du plateau.
      const texte = phraseDeLEffet(nomAffiche(carte), effet)
      if (texte) toasts.push({ id, texte })
    }
    return toasts
  }, [effets, cartesMondeParId])

  const ciblageSurTable =
    !sceneCentrale &&
    phaseMechantEnCours &&
    interaction.option !== undefined &&
    (interaction.assistant.etape === 'target' || interaction.assistant.etape === 'confirm')

  // La règle de la pile vaut PARTOUT (18/10/2026, « ta règle partout ») : mise en place, tour du joueur,
  // phase du méchant. `rechercheEnCours` : une action attend ses cibles ou sa confirmation.
  const rechercheEnCours =
    interaction.option !== undefined &&
    (interaction.assistant.etape === 'target' || interaction.assistant.etape === 'confirm')

  // UNE RECHERCHE S'OUVRE PAR SA PILE (17/10/2026) : sur la table, pendant la phase, la fenêtre de
  // choix ne surgit plus seule. Le deck ou la défausse où sont les cartes cherchées brille, avec ce
  // qu'on y fait (« Chercher dans le deck »), et c'est le clic sur la pile qui ouvre la fenêtre, avec
  // les seules cartes de cette pile. Changer d'action referme la pile.
  const [pileFouillee, setPileFouillee] = useState<number | undefined>()
  // TELEPHONE, recherche sur PLUSIEURS piles (Suit Up : deck + defausse, 26/10/2026) : toutes les cartes s'ouvrent d'un coup.
  const [toutesLesPiles, setToutesLesPiles] = useState(false)
  // FENETRE REDUITE SANS ANNULER (26/10/2026) : croix, Echap ou tap sur le voile. L'action reste en attente ; sur telephone
  // l'onglet « Piles » clignote et un bandeau propose de rouvrir ; sur PC la porte de la pile se rallume.
  const [selecteurReduit, setSelecteurReduit] = useState(false)
  useEffect(() => {
    setPileFouillee(undefined)
    setToutesLesPiles(false)
    setSelecteurReduit(false)
  }, [interaction.option])
  const pilesARechercher = useMemo(() => {
    const piles = new Map<number, string>()
    if (!(ciblageSurTable || rechercheEnCours) || !plateau) return piles
    for (const cible of interaction.ciblesHorsTable) {
      const id = Number(cible.props.id)
      const representant = plateau.representantsDePile.get(id)
      if (representant === undefined || piles.has(representant)) continue
      piles.set(representant, libelleDeLaPile(id, etat.monde))
    }
    return piles
  }, [ciblageSurTable, rechercheEnCours, plateau, interaction.ciblesHorsTable, etat.monde])
  // Sur TELEPHONE le deck n'est pas a l'ecran, donc sa porte non plus : la pile seule s'ouvre d'office (pile-auto.ts).
  const pileOuverteDOffice = pileAOuvrirSeule({
    telephone: modePlateau === 'mobile',
    rechercheEnCours: rechercheEnCours && !selecteurReduit,
    piles: pilesARechercher,
    pileOuverte: pileFouillee,
  })
  useEffect(() => {
    if (pileOuverteDOffice !== undefined) setPileFouillee(pileOuverteDOffice)
  }, [pileOuverteDOffice])
  const toutesLesPilesDOffice = pilesToutesALaFois({
    telephone: modePlateau === 'mobile',
    rechercheEnCours: rechercheEnCours && !selecteurReduit,
    piles: pilesARechercher,
    pileOuverte: pileFouillee,
  })
  useEffect(() => {
    if (toutesLesPilesDOffice) setToutesLesPiles(true)
  }, [toutesLesPilesDOffice])
  const toutesOuvertes = toutesLesPiles && pilesARechercher.size > 1
  const porteDePileFermee =
    pilesARechercher.size > 0 && !toutesOuvertes && (pileFouillee === undefined || !pilesARechercher.has(pileFouillee))
  const ciblesHorsTableVisibles = selecteurReduit || porteDePileFermee
    ? []
    : pilesARechercher.size > 1 && !toutesOuvertes
      ? interaction.ciblesHorsTable.filter((c) => plateau?.representantsDePile.get(Number(c.props.id)) === pileFouillee)
      : interaction.ciblesHorsTable
  // Cliquer une pile (sa porte sur la table, ou sa ligne du tiroir) : avec PLUSIEURS piles a chercher, la MEME fenetre s'ouvre,
  // deck et defausse cote a cote ; avec une seule, c'est cette pile (demande de l'utilisateur, 26/10/2026).
  const ouvrirPile = (clic: number) => {
    const ouverture = ouvertureDePile(pilesARechercher, clic)
    setSelecteurReduit(false)
    if (ouverture.toutes) setToutesLesPiles(true)
    else setPileFouillee(ouverture.pile)
  }
  const reduireLeSelecteur = () => {
    setPileFouillee(undefined)
    setToutesLesPiles(false)
    setSelecteurReduit(true)
  }
  // Le choix attend : recherche en cours et fenetre fermee sans annuler.
  const choixAttend_ = choixAttend({ rechercheEnCours, reduit: selecteurReduit })
  const pilesAChoisir = useMemo(() => {
    const comptes = new Map<number, number>()
    if (!plateau) return comptes
    for (const cible of interaction.ciblesHorsTable) {
      const representant = plateau.representantsDePile.get(Number(cible.props.id))
      if (representant !== undefined) comptes.set(representant, (comptes.get(representant) ?? 0) + 1)
    }
    return comptes
  }, [plateau, interaction.ciblesHorsTable])
  // L'intitule de chaque groupe, quand les cartes de plusieurs piles sont montrees ensemble : d'abord le deck, puis la defausse.
  const ciblesParPile = useMemo(() => {
    if (!toutesOuvertes) return { cibles: ciblesHorsTableVisibles, groupes: undefined }
    const rang: Record<SorteDePile, number> = { deck: 0, defausse: 1, rencontre: 2, 'defausse-rencontre': 3, autre: 4 }
    const sorte = (c: (typeof ciblesHorsTableVisibles)[number]) => sorteDePile(Number(c.props.id), etat.monde)
    const triees = [...ciblesHorsTableVisibles].sort((a, b) => rang[sorte(a)] - rang[sorte(b)])
    return {
      cibles: triees,
      groupes: new Map(triees.map((c) => [Number(c.props.id), groupeDeLaPile(sorte(c))] as const)),
    }
  }, [toutesOuvertes, ciblesHorsTableVisibles, etat.monde])

  // ⚠ AVANT le retour anticipe ci-dessous : un hook place apres lui change le nombre de hooks quand la partie apparait (erreur React 310).
  // TELEPHONE (26/10/2026, maquette approuvee) : la question « choisis la cible » se pose dans une FEUILLE qu'on glisse au doigt, avec
  // DEDANS les ronds des cibles de la table (PV, statuts) ; un toucher choisit, comme sur la table. Cibles dans une pile : le selecteur
  // a deux colonnes s'en charge, la feuille n'en montre pas (liste vide : l'assistant garde sa forme d'avant).
  // Toucher une AUTRE cible legale quand le moteur n'en veut qu'une l'echange : la choisie est retiree, puis la nouvelle prise des que
  // l'interaction l'a rendue choisissable (un cycle de rendu plus tard).
  const echangeEnAttente = useRef<number | undefined>(undefined)
  useEffect(() => {
    const id = echangeEnAttente.current
    if (id === undefined) return
    const etatCarte = interaction.cartes.get(id)
    if (etatCarte?.role === 'cible' && !etatCarte.choisie && etatCarte.agir) {
      echangeEnAttente.current = undefined
      etatCarte.agir()
    }
  }, [interaction.cartes])
  const feuilleCibles = useMemo(() => {
    const etapeCible =
      interaction.assistant.etape === 'target' || (interaction.assistant.etape === 'confirm' && interaction.cibles.length > 0)
    if (!plateau || modePlateau !== 'mobile' || !etapeCible) return undefined
    const unites = ciblesDeLaFeuille(plateau, interaction.cartes, interaction.option?.all_legal_targets)
    if (unites.length === 0) return undefined
    return {
      unites,
      decor: {
        interactifs: interaction.cartes,
        effets: new Map<number, CardEffectDelta>(),
        ouvrirPile: () => undefined,
        // Une cible legale qu'on ne peut plus ajouter (maximum atteint) : la toucher ECHANGE (voir `cibleAEchanger`).
        ouvrirCarte: (carte: ScanCardProps) => {
          const id = Number(carte.id)
          const retirer = cibleAEchanger({
            id,
            maximum: interaction.option?.target_num_range[1] ?? 0,
            legales: interaction.option?.all_legal_targets ?? [],
            interactifs: interaction.cartes,
          })
          if (retirer === undefined) return
          echangeEnAttente.current = id
          interaction.cartes.get(retirer)?.agir?.()
        },
        agir: (carte: ScanCardProps) => carte.onSelect?.(),
      },
    }
  }, [modePlateau, interaction.assistant.etape, interaction.cibles.length, interaction.cartes, interaction.option, plateau])
  // TELEPHONE (26/10/2026) : « PAY 2 TO PLAY » cachait la main, on ne pouvait plus toucher les cartes a depenser. A l'etape du
  // paiement, la feuille porte la rangee des cartes qui peuvent payer (main, puis table). Meme regle que ci-dessus : AVANT le retour
  // anticipe, jamais apres (erreur React 310).
  const feuillePaiement = useMemo(() => {
    if (!plateau || modePlateau !== 'mobile' || interaction.assistant.etape !== 'payment') return undefined
    const cartes = cartesPayantes(plateau, interaction.cartes, effets)
    return cartes.length > 0 ? { cartes } : undefined
  }, [modePlateau, interaction.assistant.etape, interaction.cartes, plateau, effets])

  if (!etat.monde || !plateau || voile) {
    return (
      <p className="plateau-message" role={etat.erreur ? 'alert' : undefined}>
        {etat.erreur ?? t('Connexion à la partie…')}
      </p>
    )
  }

  const idMenu = interaction.carteFocus ?? interaction.cibleFocus
  const carteMenu = idMenu !== undefined ? cartesAfficheesParId.get(idMenu) : undefined
  const modeMenu = interaction.cibleFocus !== undefined ? 'target' : 'source'
  const identiteJoueurId = etat.monde.players?.[joueurActif]?.area_hero?.[0]?.id
  // Badge « Active » : identite du joueur que le moteur interroge. Sans objet en
  // solo (un seul heros, toujours actif).
  const heroActifId =
    (etat.monde.players?.length ?? 0) > 1 && etat.joueurDemande !== undefined
      ? etat.monde.players?.[etat.joueurDemande]?.area_hero?.[0]?.id
      : undefined
  const menuIdentiteJoueur =
    modeMenu === 'source' &&
    carteMenu !== undefined &&
    identiteJoueurId !== undefined &&
    Number(carteMenu.id) === identiteJoueurId
  // Deux libelles ecrits en dur en ANGLAIS, au milieu d'une interface
  // francaise. Ils datent du portage et personne ne les avait vus : ce bouton
  // n'apparait que sur le menu d'une carte, jamais dans la barre.
  const libelleAnnulationMenu =
    etat.demande?.event_name === 'WhenPlayerInTurn' && etat.demande.ability_type === 'Normal'
      ? t('Fin du tour')
      : t('Passer')
  // Le moteur attend une reponse du joueur LOCAL. Etat du MOTEUR, sans un mot
  // sur la facon dont on repond : c'est ce que le cartouche du deroule doit
  // savoir (voir moteurAttendUneReponse).
  const moteurAttendLeJoueur = moteurAttendUneReponse(etat)
  // ⚠ OU VA LA QUESTION : la regle vit dans `ou-va-la-question.ts`, avec sa
  // gate. Elle est invisible comme celle du rythme — quand elle se trompe, le
  // moteur attend et RIEN a l'ecran ne dit ou repondre. Sortie d'ici le
  // 14/09/2026, apres le defaut mesure en partie : « en mode detaille il
  // n'indique meme plus quand on peut defendre ».
  // T16 : « Qui defend ? » hors de la phase du mechant, « Sur la table » : le bandeau lateral de la table la porte.
  const defenseHorsPhaseSurTable =
    modePhase === 'sur-table' &&
    !manuel &&
    !phaseMechantEnCours &&
    !enMiseEnPlace &&
    moteurAttendLeJoueur &&
    interaction.option === undefined &&
    carteMenu === undefined &&
    Boolean(etat.demande?.options.some((option) => option.name === 'Defense'))
  const etatQuestion: EtatDeLaQuestion = {
    moteurAttendLeJoueur,
    demandePresente: etat.demande !== undefined,
    effetEnCours: effets.size > 0,
    ciblage: interaction.option !== undefined,
    menuCarte: carteMenu !== undefined,
    sceneCentrale,
    phaseMechantEnCours,
    // La face A de la manigance a son propre panneau : ni le panneau central,
    // ni la scene, ni la barre du bas ne la proposent en double.
    questionDeLaManigance: priseManigance !== undefined,
    // Seul « Sur la table » a une bulle : en « D'un coup », la question restait
    // muette et la phase bloquee (12/10/2026).
    bulleSurTable: modePhase === 'sur-table',
    // Le cartouche du bas raconte deja chaque etape : la narration centrale se
    // tait pendant la phase (« plus aucun panneau hors du cartouche »).
    cartoucheEnBas: nouvelleScenePC,
    // HORS PHASE, la defense d'une attaque annoncee pendant le tour se joue
    // dans le cartouche « Pendant ton tour » (D26) ; rien d'autre n'y va.
    coupHorsPhaseEnScene:
      nouvelleScenePC &&
      !phaseMechantEnCours &&
      coupsPendantTonTour.some((coup) => coup.etat === 'annonce') &&
      Boolean(etat.demande?.options.some((option) => option.name === 'Defense')),
    // Un cartouche du bas a l'ecran hors phase (ce coup, ou la relecture du
    // journal) : la narration centrale se tait, il raconte seul.
    cartoucheHorsPhaseAffiche:
      nouvelleScenePC &&
      !phaseMechantEnCours &&
      (horsPhaseAffiche || (relectureJournal && etapesPhasePrecedente.length > 0)),
    questionSurTableHorsPhase: defenseHorsPhaseSurTable,
  }
  // Le PANNEAU central cede la place a toutes les autres facons de repondre a
  // cette meme question : un ciblage sur la table, le menu d'une carte, une
  // animation d'effet en cours.
  const afficherDemandeCentrale = questionDansLePanneau(etatQuestion)
  // Pendant la phase du mechant en Detaille, la question du moteur se joue
  // DANS la scene du deroule (livraison C de la spec du 7 septembre 2026) :
  // « Defendre ? » se decide en voyant l'attaque. Le panneau central se tait
  // alors, et DeroulePhase recoit la meme question par sa prop `question`.
  // Un ciblage (`interaction.option`) n'est pas concerne : le panneau cede
  // deja la place a la table, et la scene se replie pour la laisser cliquable.
  const questionEnScene = questionDansLaScene(etatQuestion)
  // Un CIBLAGE pendant la phase du mechant en Detaille (livraison D) : les
  // candidats se montrent aussi dans la scene, en cartes cliquables, avec la
  // validation. Ceux de la table gardent leur halo et restent cliquables
  // derriere le voile : les deux chemins menent au meme `agir`.
  const ciblageEnScene = sceneCentrale && phaseMechantEnCours && interaction.option !== undefined

  // Hors phase du méchant (mise en place, tour du joueur), la porte de la pile est le bandeau des piles :
  // le deck ou la défausse brille avec son libellé, la fenêtre de choix et l'assistant attendent le clic.
  const porteHorsPhase =
    rechercheEnCours && !ciblageSurTable && !(ciblageEnScene && nouvelleScenePC) && porteDePileFermee
  // « Sur la table », sans fenêtre (16/10/2026) : choisir des cibles, dans l'ordre s'il le faut, se fait
  // sur les cartes elles-mêmes. Le paiement garde le panneau d'action.
  // Rapport n76 (Yarro, 10/10/2026) : quand TOUTES les cibles sont hors table,
  // le selecteur devient une fenetre avec Annuler / Valider, et le panneau
  // central (qui le recouvrait) se retire. Des cibles aussi sur la table : la
  // table doit rester cliquable, on garde l'ancien couple.
  const fenetreChoix =
    ciblesHorsTableVisibles.length > 0 &&
    !(ciblageEnScene && nouvelleScenePC) &&
    interaction.ciblesHorsTable.length >= interaction.assistant.ciblePossibles
  // LE BANDEAU COLLE (fiche du 07/10/2026) : des cibles aussi sur la table, donc pas de fenetre modale. Le panneau
  // d'action ne flotte plus a cote du selecteur hors table, il en devient le haut, et les deux se deplacent ensemble.
  // Le paiement, lui, garde le panneau d'action (le selecteur n'est la que pour choisir).
  const bandeauColleActif =
    !fenetreChoix &&
    ciblesHorsTableVisibles.length > 0 &&
    !(ciblageEnScene && nouvelleScenePC) &&
    interaction.option !== undefined &&
    interaction.assistant.etape === 'target' &&
    etat.connecte &&
    etat.aNous &&
    etat.demande !== undefined &&
    !manuel &&
    !porteHorsPhase &&
    !ciblageSurTable &&
    !(nouvelleScenePC && phaseMechantEnCours)
  const bandeauColle = (() => {
    if (!bandeauColleActif || !interaction.option) return undefined
    const option = interaction.option
    const nomAction = nomActionDe(option)
    const porteur = cartesMondeParId.get(option.bind_id)
    const porteurEstIdentite = porteur?.card_type === 'Hero' || porteur?.card_type === 'AlterEgo'
    const nomDuPorteur =
      designEssai && option.bind_id !== 0 && !porteurEstIdentite
        ? (nomPorteurFr(option.bind_id) ?? (porteur ? nomAffiche(porteur) : undefined))
        : undefined
    return {
      surtitre: nomDuPorteur ?? nomAction,
      consigne: consigne(interaction.assistant, nomAction),
      phrase: phraseEtat(interaction.assistant, interaction.prete) || undefined,
      libelleValider: (nomDuPorteur ? `${nomAction} ${nomDuPorteur}` : nomAction) || t('Confirmer'),
      prete: interaction.prete,
      valider: interaction.valider,
      annuler: interaction.annuler,
    }
  })()
  // LA QUESTION STRUCTUREE du cartouche du bas (scene PC, lots 4 et 5) : la
  // defense et le choix d'une carte revelee dans sa rangee, le reste dans son
  // sous-cadre. Pendant la phase, c'est DeroulePhase qui la porte ; hors
  // phase, le cartouche « Pendant ton tour » (sa defense seulement, voir
  // `coupHorsPhaseEnScene`). Les gestionnaires restent ici ; le cartouche
  // n'appelle que `choisirOption`, `valider`, `annuler` et `agir`.
  const questionDuMoteurPC: QuestionDuMoteur | undefined =
    nouvelleScenePC && etat.demande && (questionEnScene || ciblageEnScene)
      ? {
          demande: etat.demande,
          interaction,
          cartesParId: cartesMondeParId,
          choisirOption: choisirOptionDepuisMenu,
          survolerOption: setOptionSurvolee,
          carteDeLOption,
          carteAuSurvol,
          nomPorteur: nomPorteurFr,
          texteCapacite: texteCapaciteDeLOption,
          estEnMain,
          ligneSansDefense,
          survolSansDefense,
          carteScene,
        }
      : undefined
  // etat.validationRequise n'entre pas dans la condition ci-dessous : c'est
  // desormais le cartouche du deroule detaille (DeroulePhase) qui garde la
  // validation, ce panneau-la ne fait plus que narrer. Ses deux raisons
  // d'apparaitre (un effet en cours, ou un evenement narre important pendant
  // l'activation ennemie) doivent continuer de marcher telles quelles.
  // ⚠ ET ELLE SE TAIT AUSSI DEVANT LA QUESTION LOGEE DANS LA SCENE. Sans
  // cette garde, la narration se posait AU CENTRE, par-dessus la scene qui
  // porte desormais les boutons « Defendre / Passer » pendant une animation.
  const afficherEvenementCentrale =
    narrationAuCentre(etatQuestion, {
      connecte: etat.connecte,
      evenementImportant:
        etat.monde.phase === 'Enemy Activation' && evenementNarreImportant(etat.monde),
    }) &&
    // ⚠ LE BILAN AUSSI. Le moteur sort de la phase (et tourne le round) avant
    // que le joueur ait valide le bilan : `cartoucheEnBas` ne joue plus, et la
    // narration du tour suivant se posait au centre pendant que le cartouche
    // du bas montrait encore son bilan (planche du lot 3). Tant qu'il montre
    // une etape, il est le seul panneau.
    !(nouvelleScenePC && cleEtapeAffichee !== undefined) &&
    // SANS MODALE (16/10/2026) : « Sur la table », la flèche, la pastille et la ligne du
    // haut racontent déjà l'événement. Ce panneau le redisait dans une fenêtre.
    !(modePhase === 'sur-table' && (phaseMechantEnCours || cleEtapeAffichee !== undefined))

  // Mode simple : la barre du bas disparait. Il reste juste un bouton flottant
  // « End Turn » quand on est en phase libre (sinon plus aucun moyen visible de
  // finir son tour ; le clic-sur-heros le permet aussi, mais c'est moins evident).
  // La fin de tour est-elle possible MAINTENANT ? Phase libre, rien d'engage.
  const finDeTourDisponible =
    etat.aNous &&
    etat.connecte &&
    etat.demande !== undefined &&
    etat.demande.show_cancel &&
    !demandeDoitApparaitreAuCentre(etat.demande) &&
    !interaction.option &&
    !carteMenu
  // Absent en manuel : il répondrait à la question garée du moteur (lot 1).
  const afficherFinTourSimple = modeActions === 'simple' && finDeTourDisponible && !manuel
  // Le troisieme segment du bandeau, « qui agit ». Calcule inconditionnellement :
  // le portrait (RenduPartie) en a besoin meme quand la barre PC (design essai)
  // ne l'affiche pas encore ailleurs.
  const quiAgit = libelleQuiAgit(etat.monde, etat)

  // Le cartouche « Pendant ton tour » recouvre le bouton de fin de tour : ses
  // raccourcis se taisent avec lui. Espace
  // tournait les pages de ce meme cartouche toute la phase, et le reflexe
  // finissait le tour du joueur venu fermer le coup du mechant (verification
  // du lot 5 de la refonte).
  const finDeTourCachee = nouvelleScenePC && horsPhaseAffiche
  finTourClavier.current = () => {
    if (afficherFinTourSimple && !finDeTourCachee) interaction.annuler()
  }
  // Meme garde que le bouton complet lui-meme : `disabled={!finDeTourDisponible}`
  // et absent en mode manuel (`{manuel ? null : (<button ...>)}`, plus bas).
  finTourClavierEspace.current = () => {
    if (finDeTourDisponible && !manuel && !finDeTourCachee) interaction.annuler()
  }

  const RenduPartie = modePlateau === 'mobile' ? PlateauMobile : Board

  return (
    <CartesDuJournal.Provider value={cartesDuPlateau}>
      <PlusieursJoueurs.Provider value={(etat.monde?.players?.length ?? 1) > 1}>
      {/* ⚠ LA BARRE DU SPECTATEUR PASSE AVANT TOUT LE RESTE. Un plateau sans
          boutons ressemble a un plateau CASSE : elle dit, en permanence, qu'on
          regarde. Voir BarreSpectateur.tsx. */}
      {spectateur && !estCadre() ? (
        <BarreSpectateur
          siege={playerId}
          sieges={etat.monde?.players?.length ?? 1}
          terminee={partieFinieMoteur || (!etat.connecte && etat.monde !== undefined)}
          raison={
            partieFinieMoteur
              ? etat.monde?.game_over_reason || undefined
              : !etat.connecte
                ? t('La table s’est éteinte')
                : undefined
          }
        />
      ) : null}

      {etat.erreur ? (
        <p className="plateau-message" role="alert">
          {etat.erreur}
        </p>
      ) : null}
      {actionAnnulee ? (
        <p className="plateau-annulation" role="status">
          {actionAnnulee}
        </p>
      ) : null}


      {/* En mode detaille, BandeauPhase (plus bas) annonce deja la phase du
          mechant, plus fort : ce splash-ci ne doit pas la doubler. */}
      <SplashTour monde={etat.monde} annonceMechantAilleurs={unCartouche} saut={etat.saut === true} />
      <BarreAvantage monde={etat.monde} />


      {/* Le cartouche du bas (scene PC, lot 4) montre les cibles hors table
          dans son sous-cadre : le selecteur les montrerait une seconde fois,
          hors du cartouche (piege 29). */}
      {ciblageEnScene && nouvelleScenePC ? null : (
        <SelecteurCibles
          cibles={ciblesParPile.cibles}
          groupes={ciblesParPile.groupes}
          titre={interaction.option ? nomActionDe(interaction.option) : ''}
          survoler={setApercuSelecteur}
          bandeau={bandeauColle}
          fenetre={
            fenetreChoix
              ? {
                  choisies: interaction.assistant.cibleNombre,
                  minimum: interaction.assistant.cibleMinimum,
                  maximum: interaction.assistant.cibleMaximum,
                  valider: interaction.valider,
                  annuler: interaction.annuler,
                  // Fermer sans annuler : TELEPHONE seulement (bandeau « Rouvrir », onglet « Piles » qui clignote, tiroir). Sur PC, la
                  // reouverture par la porte de la pile apres Echap n'est pas verifiee (26/10/2026) : la fenetre garde son Annuler.
                  reduire: modePlateau === 'mobile' ? reduireLeSelecteur : undefined,
                }
              : undefined
          }
        />
      )}
      {porteHorsPhase && interaction.option ? (
        // Dans le cadre du plateau : les cadres verts se placent dans SON repere (la barre du haut
        // le decale de 42 px du haut de la page), sinon ils flottent au-dessus des piles.
        <DansLeCadre>
          <CiblageSurTable
            titre={nomActionDe(interaction.option)}
            choisies={interaction.cibles.length}
            maximum={interaction.option.target_num_range[1]}
            cibles={[...pilesARechercher].map(([id, libelle]) => ({
              id,
              choisie: false,
              etiquette: libelle,
              agir: () => ouvrirPile(id),
            }))}
            prete={interaction.prete}
            raison={interaction.raison}
            valider={interaction.valider}
            annuler={interaction.annuler}
          />
        </DansLeCadre>
      ) : null}
      {apercuSelecteur ? (
        <CarteApercu carte={apercuSelecteur} classe={fenetreChoix ? 'au-dessus-de-la-fenetre' : undefined} />
      ) : null}
      {interaction.ciblesHorsTable.length === 0 && !interaction.option ? (
        <ModaleCartesRegardees groupes={groupesRegardes} />
      ) : null}

      {ciblesMenu ? (
        <ModaleCiblesMenu
          titre={ciblesMenu.titre}
          cartes={ciblesMenu.cartes}
          fermer={() => setCiblesMenu(undefined)}
        />
      ) : null}

      {defenseHorsPhaseSurTable && etat.demande ? (
        <DansLeCadre>
          <EspaceDeLaQuestion />
          <DemandeCentrale
            demande={etat.demande}
            options={interaction.options}
            cartesParId={cartesMondeParId}
            choisirOption={choisirOptionDepuisMenu}
            annuler={interaction.annuler}
            survolerOption={setOptionSurvolee}
            carteDeLOption={carteDeLOption}
            carteAuSurvol={carteAuSurvol}
            cartesDuLot={cartesDuLot}
            nomPorteur={nomPorteurFr}
            texteCapacite={texteCapaciteDeLOption}
            estEnMain={estEnMain}
            ligneSansDefense={ligneSansDefense}
            survolSansDefense={survolSansDefense}
            enScene
            surLaTable
            annulerAction={annulerAction}
          />
        </DansLeCadre>
      ) : null}

      {manuel ? null : afficherDemandeCentrale && etat.demande && !questionEnScene ? (
        <DemandeCentrale
          demande={etat.demande}
          options={interaction.options}
          cartesParId={cartesMondeParId}
          choisirOption={choisirOptionDepuisMenu}
          annuler={interaction.annuler}
          survolerOption={setOptionSurvolee}
          carteDeLOption={carteDeLOption}
          carteAuSurvol={carteAuSurvol}
          cartesDuLot={cartesDuLot}
          nomPorteur={nomPorteurFr}
          texteCapacite={texteCapaciteDeLOption}
          estEnMain={estEnMain}
          ligneSansDefense={ligneSansDefense}
          survolSansDefense={survolSansDefense}
          annulerAction={annulerAction}
        />
      ) : null}

      {/* Un changement sur une carte (statut, jeton, menace, PV) : une phrase posee SUR cette carte (T15). */}
      {afficherEvenementCentrale ? <ToastsEffetsCartes toasts={toastsEffets} /> : null}

      {afficherEvenementCentrale && (toastsEffets.length === 0 || (!unCartouche && etat.validationRequise)) ? (
        <EvenementCentrale
          prompt={etat.monde.prompt}
          eventName={etat.monde.event_name}
          // En mode Détaillé, la validation appartient au cartouche
          // (DeroulePhase) : ce panneau ne doit plus jamais montrer de bouton
          // « Continuer », quelle que soit la valeur de etat.validationRequise.
          validationRequise={unCartouche ? false : etat.validationRequise}
          continuer={continuer}
          // Les cartes citees par l'evenement en cours : le bandeau raconte ce
          // qui leur arrive, il ne doit surtout pas les cacher.
          cartes={etat.monde.active_card_ids}
        />
      ) : null}

      {/* ⚠ PAS DE MENU DE CARTE EN SPECTATEUR. Il ne propose que des actions,
          toutes refusees par le moteur : l'ouvrir serait promettre ce qu'on ne
          peut pas tenir. L'agrandissement au survol, lui, reste : c'est
          precisement ce qu'on vient faire. */}
      {/* Tablette en manuel : les gestes manuels prennent seuls la place sous l'apercu. */}
      {carteMenu && !interaction.option && !(tablette && manuel) ? (
        <MenuActionsCarte
          texteDeCarte={texteImprimeDeLaCarte}
          carte={carteMenu}
          carteMonde={cartesMondeParId.get(Number(carteMenu.id))}
          options={interaction.options}
          toutesOptions={etat.demande?.options ?? []}
          cartesParId={cartesMondeParId}
          catalogue={catalogue}
          choisirOption={choisirOptionDepuisMenu}
          annulerDemande={
            menuIdentiteJoueur && etat.demande?.show_cancel ? interaction.annuler : undefined
          }
          libelleAnnulation={libelleAnnulationMenu}
          fermer={interaction.defocaliser}
          playerId={joueurActif}
          survolerOption={setOptionSurvolee}
          idsAffiches={plateau.idsAffiches}
          ouvrirCiblesHorsTable={ouvrirCiblesHorsTable}
          mode={modeMenu}
          ciblePreselectionnee={interaction.cibleFocus}
          affichage={modeActions}
          dansApercu={tablette && modePlateau !== 'mobile'}
        />
      ) : null}

      {manuel || fenetreChoix || porteHorsPhase || bandeauColleActif ? null : (
        <AssistantAction
          demande={etat.demande}
          interaction={interaction}
          aNous={etat.aNous}
          connecte={etat.connecte}
          cartesParId={cartesMondeParId}
          affichage={modeActions}
          designEssai={designEssai}
          nomPorteur={nomPorteurFr}
          tailleMain={etat.monde?.players[etat.joueurDemande ?? playerId]?.hand_size}
          choixDansLaScene={ciblageEnScene}
          // Le sous-cadre du cartouche du bas porte tout, paiement compris (D6).
          sousCadre={(nouvelleScenePC && phaseMechantEnCours && interaction.option !== undefined) || ciblageSurTable}
          feuilleCibles={feuilleCibles}
          feuillePaiement={feuillePaiement}
        />
      )}

      <CoucheMeteo world={etat.monde} active={meteo} apercu={apercuMeteo} />
      {/* Explique l'ambiance qui s'allume, au lieu de la subir sans un mot.
          Reglage PERSONNEL : elle ne change rien pour les autres joueurs et
          ne retient pas le moteur, la partie continue derriere. */}
      <ModaleAmbiance
        // Change de cle quand le joueur touche au reglage : le composant se
        // remonte, et une question remise en marche depuis les Options se
        // repose des la partie EN COURS, sans attendre la suivante.
        key={reponseAmbiance}
        monde={etat.monde}
        ambianceActive={meteo}
        apercu={apercuMeteo}
        reglerApercu={reglerApercuMeteo}
        onReponseFigee={setReponseAmbiance}
      />
      {/* Le preavis du site (mise a jour, coupure). Il barre le dixieme
          superieur de l'ecran, deux secondes toutes les trente, et laisse
          passer les clics : voir BandeauAnnonce. */}
      {annonce && annonceVisible ? (
        <BandeauAnnonce texte={annonce.texte} secondes={annonce.secondes} />
      ) : null}
      {/* ⚠ HORS de la condition ci-dessus, et ce n'est pas la meme chose :
          l'annonce previent d'une coupure a venir, celle-ci constate qu'on
          tourne sur du vieux code. Les deux peuvent se produire ensemble. */}
      <BandeauMiseAJour visible={majDisponible} />
      <CreateurPuzzle
        actif={etat.monde?.mode_createur_puzzle === true}
        pret={etat.monde?.manuel_actif === true}
        nomsDesJoueurs={(etat.monde?.players ?? []).map((j, i) => j?.area_hero?.[0]?.name?.replace(/^\W*/, '') || `${t('Joueur')} ${i + 1}`)}
      />
      <PanneauObjectifs objectifs={etat.monde?.puzzle_objectives} />
      <PanneauEnonce info={etat.monde?.puzzle_info} objectifs={etat.monde?.puzzle_objectives} termine={Boolean(etat.monde?.game_over)} />
      {etat.joueurDemande !== undefined &&
      etat.siegesAbsents.includes(etat.joueurDemande) ? (
        <BandeauAbsent
          numero={etat.joueurDemande + 1}
          nom={etat.monde?.players?.[etat.joueurDemande]?.area_hero?.[0]?.name?.replace(/^\W*/, '')}
          // Le siege est deja ouvert cote serveur (voir allowed_seats) : il
          // suffit de regarder ce joueur pour repondre a sa place.
          onReprendre={() => setVueForcee(etat.joueurDemande ?? null)}
        />
      ) : null}

      {/* CouchePasAPas (barre « où on en est » + Tout passer) : DEBRANCHEE a
          la demande de l'utilisateur - double emploi avec le cartouche du
          deroule juste en dessous, qui porte deja MENACE / ACTIVATIONS /
          DISTRIBUTION / RÉVÉLATION : exactement le defaut corrige entre le
          bandeau et le splash. Le « Tout passer » qu'elle portait est repris
          par DeroulePhase (touche Echap, qui fait defiler le cartouche).
          CouchePasAPas.tsx reste en place, mais deux de ses props n'ont PLUS
          de contrepartie dans le moteur : la pause (`enPause`,
          `onBasculerPause`) et le « Tout passer » moteur (`onToutPasser`) ont
          disparu avec le minuteur de lecture du moteur, le cartouche tenant
          desormais la seule horloge de la phase. La rallumer demanderait de
          lui retirer ces deux commandes ; `actif` vaudrait
          `etat.trameRetenue !== undefined` et `onAvancer` = avancerPasAPas
          (deja destructure plus haut, utilise par DeroulePhase ci-dessous). */}
      {/* Banniere des hauts faits : DEBRANCHEE a la demande de l'utilisateur.
          Moteur.enregistrerHautsFaits() continue de les accumuler dans
          etat.hautsFaits, et CoucheHautsFaits.tsx reste en place : il suffit de
          remettre <CoucheHautsFaits hautsFaits={etat.hautsFaits} /> ici pour la
          rallumer. */}
      {/* Deroule detaille : une etape a la fois, validee avant la suivante.
          Le recap ci-dessous garde son role de bilan de fin, pour les modes
          rapides ou l'on n'a rien vu passer. */}
      {/* Le joueur SANS cartouche (mode Instantane) : une ligne discrete, pas
          un plateau fige et muet. Le reglage est personnel, mais le rythme est
          celui de la table — c'est exactement ce que F5 reprochait. */}
      {!unCartouche && attendUnAutreJoueur && phaseMechantEnCours ? (
        (<AttenteTable nom={autreJoueurInterroge?.nom} />)
      ) : null}
      {/* Hors phase, un coup du mechant : le cartouche d'un seul coup a la
          table et au telephone ; en scene PC, le cartouche du bas « Pendant
          ton tour » (D26), defense et carte revelee comprises. */}
      {manuel || !unCartouche || phaseMechantEnCours || nouvelleScenePC ? null : modePhase === 'sur-table' ? (
        <CoupHorsPhaseSurTable etapes={coupsHorsPhase} ignorerLesPremiers />
      ) : (
        <CoupHorsPhase etapes={coupsHorsPhase} ignorerLesPremiers />
      )}
      {!manuel && nouvelleScenePC && !phaseMechantEnCours ? (
        <CartoucheHorsPhase
          coups={coupsPendantTonTour}
          nomConcerne={nomDuHerosDuTour(etat.monde)}
          dynamique={phaseDynamique}
            tris={phaseTris}
          questionAuJoueur={moteurAttendLeJoueur && autreJoueurInterroge === undefined}
          questionDuMoteur={questionDuMoteurPC}
          masque={relectureJournal}
          onAffiche={setHorsPhaseAffiche}
          pvMaxParNom={pvMaxParNom}
          carteScene={carteScene}
          nomFr={nomPorteurFr}
          texteEtoile={texteBoostEtoile}
          infoCarte={infoCarte}
          infoRevelee={infoRevelee}
        />
      ) : null}
      {!manuel && nouvelleScenePC && !phaseMechantEnCours && relectureJournal && etapesPhasePrecedente.length > 0 ? (
        <RelectureJournal
          etapes={etapesPhasePrecedente}
          pvMaxParNom={pvMaxParNom}
          carteScene={carteScene}
          nomFr={nomPorteurFr}
          texteEtoile={texteBoostEtoile}
          infoCarte={infoCarte}
          infoRevelee={infoRevelee}
          onFermer={() => setRelectureJournal(false)}
        />
      ) : null}
      {manuel ? null : unCartouche ? (
        <>
          <BandeauPhase
            round={etat.monde?.round_id ?? 1}
            actif={etapesPhaseMechant.length > 0}
            onFini={() => setBandeauPasse(true)}
          />
          <DeroulePhase
            // Meme mecanique, deux endroits : le cartouche central du mode
            // « Detaille », ou le cartouche pose A COTE DE L'ACTION du mode
            // « Sur la table ».
            presentation={sceneCentrale ? 'scene' : 'table'}
            essai={phaseEssai}
            dynamique={phaseDynamique}
            tris={phaseTris}
            cadresJoueurs={cadresJoueurs}
            joueurDeCarte={joueurDeCarteMonde}
            siegeLocal={playerId}
            premierJoueur={premierJoueurMonde}
            nomsJoueurs={nomsJoueursMonde}
            attendreBandeau={!bandeauPasse}
            // Distribution retiree en scene PC (D15), liste brute ailleurs.
            etapes={etapesPourLeCartouche.etapes}
            telephone={modePlateau === 'mobile'}
            cartesDistribuees={cartesDistribuees}
            texteEtoile={texteBoostEtoile}
            infoCarte={infoCarte}
            accelerationEnJeu={[...(etat.monde?.area_schemes_main ?? []), ...(etat.monde?.area_schemes_side ?? [])].reduce((n, c) => n + (c.info?.acceleration_icon ?? 0), 0)}
            infoRevelee={infoRevelee}
            // L'identite de la phase en cours, seule chose qui remet le
            // cartouche a zero. Il y a une phase du mechant par round, donc le
            // round suffit a distinguer deux phases ; la liste d'etapes, elle,
            // s'allonge PENDANT la phase (chaque validation relache une trame
            // qui produit l'etape suivante) et ne peut donc pas jouer ce role.
            identitePhase={etat.monde?.round_id ?? 0}
            // La partie, que le moteur renumerote a chaque nouvelle partie :
            // une partie neuve peut commencer SANS rechargement de page, et le
            // round retombe alors a 1 sans que rien d'autre ne le dise au
            // cartouche.
            identitePartie={etat.partieId}
            // Tant que le moteur est dans une des quatre phases du mechant, la
            // liste d'etapes peut encore s'allonger : arriver au bout de
            // celles qu'on connait ne veut pas dire que la phase est finie.
            phaseMechantEnCours={phaseMechantEnCours}
            // La partie est finie ET l'ecran de fin est a l'ecran : le
            // cartouche s'efface. Meme valeur que cet ecran (`EcranFinPartie`,
            // plus bas), pas une seconde inventee pour l'occasion. Constate en
            // partie : l'ecran de defaite etait la et le cartouche annonçait
            // encore « La suite arrive… ». Tant que le coup fatal n'a pas ete
            // valide, `finPartieAffichee` reste faux et le cartouche montre
            // l'etape qui a tue (voir `afficherFinDePartie`).
            partieFinie={finPartieAffichee}
            // Le moteur pose une question au joueur local : le cartouche
            // s'efface devant elle. On lit l'etat du MOTEUR, pas la visibilite
            // du panneau central : pendant un ciblage (choisir les deux sbires
            // a activer), le panneau cede la place au selecteur de cibles et le
            // cartouche se redeployait pour annoncer « La suite arrive… » alors
            // que le moteur attendait le joueur.
            // ...et SEULEMENT quand c'est nous. Sans mot de passe de siege, le
            // serveur laisse ce navigateur lire la question d'un autre joueur
            // (`allowed_seats` rend `None`) : replier le cartouche sur « Le
            // moteur attend ta reponse » serait alors faux. C'est la mention
            // d'attente ci-dessous qui prend le relais dans ce cas.
            questionAuJoueur={moteurAttendLeJoueur && autreJoueurInterroge === undefined}
            // L'onglet de la question : la phase du moteur, et pendant les
            // activations, l'attaquant (la cible de l'option « Defense »).
            tempsQuestion={tempsDeLaQuestion(
              etat.monde?.phase,
              (() => {
                // L'ordre d'activation des sbires se demande en 2B (16/10/2026).
                if ((etat.demande?.options ?? []).some((o) => /minion.*order/i.test(o.name))) return false
                if (interaction.option && /minion.*order/i.test(interaction.option.name)) return false
                const defense = etat.demande?.options?.find((o) => o.name === 'Defense')
                const attaquant = defense?.all_legal_targets?.[0]
                if (attaquant === undefined) return undefined
                const carte = cartesMondeParId.get(attaquant)
                return carte ? kindOf(carte) === 'villain' : undefined
              })()
            )}
            // Les cartes de la scene, et le dos d'une carte rencontre pour
            // l'etape de distribution (voir `carteScene` plus haut).
            carteScene={carteScene}
            dosRencontre={dosRencontre}
            nomFr={nomPorteurFr}
            // LA QUESTION STRUCTUREE du cartouche du bas, pendant la phase
            // (voir `questionDuMoteurPC`).
            questionDuMoteur={phaseMechantEnCours ? questionDuMoteurPC : undefined}
            // La question d'un AUTRE siege, en lecture seule (D28) : des noms,
            // aucun gestionnaire. Sans demande lisible (siege protege), la
            // rangee dit quand meme qui choisit, sans ses cartes.
            questionDUnAutre={
              nouvelleScenePC && phaseMechantEnCours && autreJoueurInterroge !== undefined
                ? {
                    options: (etat.demande?.options ?? []).map((option) => ({
                      id: option.id,
                      bindId: option.bind_id,
                      nom: nomPorteurFr(option.bind_id) ?? nomActionDe(option),
                    })),
                  }
                : undefined
            }
            // La question rendue par le plateau, logee dans la scene (voir
            // `questionEnScene`) : la table et le telephone seulement, le
            // cartouche du bas a la sienne.
            question={
              nouvelleScenePC ? undefined : ciblageEnScene && interaction.option ? (
                <CiblesScene
                  titre={nomActionDe(interaction.option)}
                  cibles={[
                    ...[...interaction.cartes.entries()]
                      .filter(([, e]) => e.role === 'cible')
                      .map(([id, e]) => ({
                        props: carteScene(id, true) ?? {
                          id: String(id),
                          name: cartesMondeParId.get(id)?.name ?? '',
                          kind: 'unknown' as const,
                          imageUrl: '',
                        },
                        choisie: e.choisie,
                        fois: e.fois,
                        ordre: e.ordre,
                        ordreReculer: e.ordreReculer,
                        ordreAvancer: e.ordreAvancer,
                        permuterAvec: e.permuterAvec,
                        assignerReste: e.assignerReste,
                        assignerResteQuantite: e.assignerResteQuantite,
                        agir: e.agir,
                      })),
                    ...interaction.ciblesHorsTable,
                  ]}
                  choisies={interaction.cibles.length}
                  minimum={interaction.option.target_num_range[0]}
                  maximum={interaction.option.target_num_range[1]}
                  prete={interaction.prete}
                  raison={interaction.raison}
                  valider={interaction.valider}
                  annuler={interaction.annuler}
                />
              ) : ciblageSurTable ? (
                <CiblageSurTable
                  titre={nomActionDe(interaction.option!)}
                  choisies={interaction.cibles.length}
                  maximum={interaction.option!.target_num_range[1]}
                  cibles={[
                    ...[...interaction.cartes.entries()]
                      .filter(([id, e]) => e.role === 'cible' && e.agir !== undefined && !pilesARechercher.has(id))
                      .map(([id, e]) => ({ id, choisie: e.choisie, ordre: e.ordre, fois: e.fois, agir: e.agir! })),
                    ...(porteDePileFermee
                      ? [...pilesARechercher].map(([id, libelle]) => ({
                          id,
                          choisie: false,
                          etiquette: libelle,
                          agir: () => ouvrirPile(id),
                        }))
                      : []),
                  ]}
                  prete={interaction.prete}
                  raison={interaction.raison}
                  valider={interaction.valider}
                  annuler={interaction.annuler}
                  ordreDeLaTable={interaction.option?.name === 'Minion_Activates_Order' || interaction.option?.name === 'Players_Activation_Order'}
                />
              ) : questionEnScene && etat.demande ? (
                <DemandeCentrale
                  demande={etat.demande}
                  options={interaction.options}
                  cartesParId={cartesMondeParId}
                  choisirOption={choisirOptionDepuisMenu}
                  annuler={interaction.annuler}
                  survolerOption={setOptionSurvolee}
                  carteDeLOption={carteDeLOption}
                  carteAuSurvol={carteAuSurvol}
                  cartesDuLot={cartesDuLot}
                  nomPorteur={nomPorteurFr}
                  texteCapacite={texteCapaciteDeLOption}
                  estEnMain={estEnMain}
                  ligneSansDefense={ligneSansDefense}
                  survolSansDefense={survolSansDefense}
                  enScene
                  surLaTable={!sceneCentrale}
                  annulerAction={manuel ? undefined : annulerAction}
                />
              ) : undefined
            }
            // Les deux faces de NOTRE heros : la chute d'un autre joueur ne
            // coupe plus le deroule de ce siege-ci, elle y reste une etape
            // marquee et la phase continue (constat F5).
            herosLocauxIds={herosLocauxIds}
            herosDesAutresIds={herosDesAutresIds}
            // La table attend quelqu'un d'AUTRE : le cartouche le dit a la
            // place de « La suite arrive… », qui parle du moteur. Le nom est
            // connu quand le moteur interroge ce siege-la OU quand il publie
            // le retard de son accuse de reception ; sinon la mention reste
            // vraie mais vague (voir board/attente-table.ts).
            attendUnAutreJoueur={attendUnAutreJoueur}
            nomJoueurAttendu={autreJoueurInterroge?.nom ?? autreJoueurEnRetard?.nom}
            // Les PV maximum, que seul le monde connait : le bilan de fin de
            // phase dit alors « 8/14 » plutot que « 8 » tout seul.
            pvMaxParNom={pvMaxParNom}
            // L'identite de la trame que le moteur retient. Elle donne au
            // cartouche de quoi n'acquitter qu'UNE fois par trame, plutot que
            // de se fier a un booleen qui se recalcule sans cesse.
            trameRetenue={etat.trameRetenue}
            // L'echeance du filet anti-blocage : 90 s d'INACTIVITE pendant une
            // trame retenue, remise a zero par chaque accuse du joueur. Le
            // cartouche n'en montre que les quinze dernieres secondes : la
            // phase qui repart toute seule ne doit pas ressembler a un bug.
            echeanceFilet={etat.echeanceFilet}
            // « Temps par decision » regle a la preparation : le moteur expire
            // ses attentes et poursuit sans nous, ce que le mode Detaille
            // suppose pourtant impossible. Le cartouche le DIT, il ne corrige
            // rien.
            tempsParDecision={etat.maxTimeout}
            // PAS A PAS, TOUJOURS (choix de l'utilisateur, 03/10/2026, apres le
            // rapport Yarro n°46 : « tout est alle a 2000 a l'heure »). Chaque
            // etape attend le clic « Suivant » ; le reglage « Avance toute
            // seule » et sa vitesse ont ete retires.
            // L'accuse de reception. Il ne part plus a chaque « Suivant » : le
            // cartouche le declenche quand il n'a plus rien a montrer, donc
            // quand le joueur a valide tout ce qu'il sait deja. onTerminer
            // rappelle la meme fonction pour ne jamais laisser le moteur
            // bloque une fois la derniere etape validee (elle ne fait rien
            // sans trame en attente, moteur.ts, avancerMaintenant).
            onSuivant={avancerPasAPas}
            // Le joueur a bouge dans le cartouche, sans forcement acquitter :
            // une seule trame retenue peut porter deux etapes. Le filet mesure
            // une inactivite, il doit donc voir ces clics-la aussi.
            onActivite={signalerActivite}
            onTerminer={avancerPasAPas}
            onEtapeAffichee={setCleEtapeAffichee}
            onEtapeValidee={(cle, etatValide) => setValidationEtape(`${cle}|${etatValide}`)}
            onAvantResultat={setAvantResultat}
            // Le coup fatal est vu : l'ecran de fin de partie peut paraitre.
            onDefaiteVue={() => setCoupFatalVu(true)}
          />
        </>
      ) : null}
      {/* ⚠ JAMAIS `{manuel ? null : (...)}` ICI (correctif tache 4, plan de
          pause) -- CONTRAIREMENT A TOUTES LES AUTRES COUCHES DU MOTEUR
          ci-dessus. `RecapPhaseMechant` construit son bilan sur la DUREE (un
          `useState` qui ne se remplit qu'a la SORTIE de la phase, voir le
          composant) : le demonter pendant la pause detruit ce bilan, et le
          remonter a la reprise repart d'un etat vierge qui ne recalcule RIEN
          tant qu'aucune NOUVELLE transition de phase ne se reproduit -- le
          recap ne revenait donc jamais, meme quand il avait deja quelque
          chose a montrer avant la pause (constate en ecrivant le test de la
          tache 4). Le composant reste donc TOUJOURS monte ; c'est la prop
          `actif`, qu'il sait deja lire pour se taire (`if (!bilan || !actif)
          return null`), qui porte desormais aussi le silence du mode manuel. */}
      <RecapPhaseMechant
        entrees={historique.entrees}
        monde={etat.monde}
        // EN INSTANTANE SEULEMENT, ET JAMAIS PENDANT QUE LE MOTEUR SE TAIT.
        // En detaille, le cartouche du deroule (DeroulePhase, juste au-dessus)
        // raconte la phase etape par etape et la termine par son propre
        // bilan, valide au clic : le recap disait ensuite la meme chose une
        // seconde plus tard, calculee par un autre chemin. Deux bilans qui se
        // suivent, et qui pouvaient diverger (constat M7 de l'audit du
        // 06/09/2026).
        //
        // Il avait ete remis en detaille « par securite » (c27bb07) a un moment
        // ou le cartouche ne tenait pas le rythme et s'effaçait avant la fin de
        // la phase. Ce n'est plus le cas : la cause racine est corrigee
        // (86d8bd34) et le bilan du cartouche s'affiche vraiment (09e4bfa1).
        actif={!manuel && !unCartouche}
        // La MEME definition de « la phase du mechant » que le cartouche, et la
        // meme valeur deja calculee : le recap avait son propre detecteur de
        // transition, sur sa propre photo de `monde.phase` (constat F6).
        phaseMechantEnCours={phaseMechantEnCours}
        // De quoi montrer la carte au survol d'une ligne : le même index et le
        // même catalogue que la table, donc le même agrandissement qu'elle.
        cartesMonde={cartesMondeParId}
        catalogue={catalogue}
        playerId={joueurActif}
      />
      <CoucheCurseurs
        // ⚠ TOUJOURS, MEME EN SOLO. Le seuil « plus d'un joueur » privait le
        // spectateur de la seule chose qu'il vienne voir sur les parties solo,
        // les plus nombreuses : le joueur seul n'envoyait jamais sa souris (mesure
        // du 07/10/2026). Et une partie enregistree n'avait aucun curseur a relire.
        actif={curseurs}
        monJoueur={playerId}
        nomsJoueurs={(etat.monde?.players ?? []).map(
          (joueur, i) => joueur.area_hero?.[0]?.name?.replace(/^\W*/, '') ?? `J${i}`
        )}
      />

      {tournerLeTelephone ? <EcranTourne /> : null}
      {tabletteDebout ? <EcranTourne tablette /> : null}

      {/* 13/10/2026 (encadré ⑧) : ton héros est éliminé, les autres jouent encore.
          Tu regardes la suite ; tu gagnes ou tu perds avec ton équipe (Rules
          Reference, PLAYER ELIMINATION). Ta zone a déjà quitté la table. */}
      {estMultijoueur() && !spectateur && etat.monde?.players?.[playerId]?.is_eliminated && !etat.monde?.game_over ? (
        <div className="bandeau-spectateur" role="status">
          <span>{t('Tu es éliminé : tu regardes la suite. Tu gagnes ou tu perds avec ton équipe.')}</span>
          <button type="button" className="bandeau-spectateur-quitter" onClick={() => void retourMenuPrincipal()}>
            {t('Quitter la partie')}
          </button>
        </div>
      ) : null}

      <RenduPartie
        world={mondeSurTable ?? mondeTable ?? etat.monde}
        playerId={joueurActif}
        // Le bandeau « Annuler » du telephone (zone 3) appelle la MEME
        // annulation que le bouton « ↶ Annuler » de la barre.
        annulerCoup={spectateur ? undefined : annulerCoup}
        tablette={tablette && modePlateau !== 'mobile'}
        bandeManigances={modePlateau !== 'mobile'}
        disposition={editionTable?.d ?? dispositionTable}
        identitePartie={etat.partieId}
        superposition={
          editionTable && modePlateau !== 'mobile' ? (
            <EditeurTable
              disposition={editionTable.d}
              changer={(d) => setEditionTable({ d, origine: false })}
              origine={() => setEditionTable({ d: DISPOSITION_DE_DEPART, origine: true })}
              annuler={() => setEditionTable(undefined)}
              terminer={() => {
                enregistrerDisposition(nombreDeJoueurs, editionTable.origine ? undefined : editionTable.d)
                setEditionTable(undefined)
              }}
            />
          ) : undefined
        }
        plateau={plateauSurTable ?? plateauTable ?? plateau}
        effets={effets}
        heroActifId={heroActifId}
        // Le bandeau portrait n'a pas de quoi recalculer « qui agit » (il ne
        // connait ni aNous, ni connecte, ni demande) : on le lui passe deja fait.
        quiAgit={quiAgit}
        // Le bouton Fin du tour du telephone vit dans le bandeau portrait
        // (spec du 12/09/2026) : le flottant `.bouton-fin-tour` n'y est plus
        // rendu (voir plus bas).
        actionPrincipale={
          afficherFinTourSimple
            ? { libelle: t('Fin du tour'), suggere: finDeTourSuggeree, agir: interaction.annuler }
            : undefined
        }
        // Onglets du multijoueur (tache 10) : ignores par le plateau PC
        // (props optionnelles), lus par PlateauPortrait pour proposer la
        // bascule que la barre PC offre deja plus bas via `vueForcee`.
        joueursAffichables={joueursAffichables}
        joueurRegarde={joueurActif}
        choisirJoueurRegarde={setVueForcee}
        // Fenetre de choix fermee sans annuler : l'onglet « Piles » clignote (PlateauPortrait).
        choixEnAttente={
          choixAttend_
            ? { titre: interaction.option ? nomActionDe(interaction.option) : '', piles: pilesAChoisir, rouvrir: () => setSelecteurReduit(false) }
            : undefined
        }
        // Meme condition que le rendu de MenuActionsCarte ci-dessus : le rendu
        // mobile empile une couche tant que ce menu est affiche, pour que le
        // Retour d'Android le ferme au lieu de sortir de la partie.
        carteFocalisee={carteMenu && !interaction.option ? idMenu : undefined}
        onFermerCarte={interaction.defocaliser}
        // Meme condition que le rendu de SelecteurCibles ci-dessus (il ne
        // dessine rien sans cible). Le Retour abandonne l'option en cours de
        // composition : le menu de la carte revient, on n'a pas quitte la
        // partie au milieu d'un ciblage.
        selecteurOuvert={interaction.ciblesHorsTable.length > 0}
        onFermerSelecteur={interaction.abandonnerOption}
        // Le journal du heros ne vit plus sur la table : la colonne de droite
        // est aux manigances (demande de l'utilisateur, 7 septembre 2026).
        // Il se lit dans le volet du journal (VoletJournal, menu « ⋯ »).
        actionsPartie={
          /* ORDRE : par intention, et il se lit comme une phrase —
              ce que je FAIS, ce que je REGARDE, comment c'est REGLE, je PARS.

              Avant, les reglages etaient eclates en trois endroits : le panneau
              Options, la paire Musique/Langue, et le mode d'affichage exile a
              l'autre bout de la barre. Options, lui, s'etait intercale entre les
              deux actions de partie et les deux boutons de consultation.

              Musique et Langue restent HORS du panneau Options, deliberement :
              couper le son ou changer de langue doit se faire d'un geste (voir
              le commentaire du bouton musique). */
          <div
            className={`board-actions${designEssai ? ' design-essai' : ''}${spectateur && !estCadre() ? ' est-spectateur' : ''}`}
          >
            {/* OÙ ON EN EST. La barre n'avait que des boutons : le round et
                la phase n'étaient écrits nulle part une fois le cartouche
                refermé. Deux lignes, à gauche, avant tout le reste. */}
            {/* Design essai : le bandeau vit aussi avant le premier round
                (mulligan), ou il dit « Mise en place · Mulligans · A toi de
                jouer » ; sans le drapeau, rien ne change. */}
            {libelleRound(etat.monde) || (designEssai && quiAgit) ? (
              <div className="bh-etat" role="status">
                <strong>{libelleRound(etat.monde) || t('Mise en place')}</strong>
                <span>{libellePhase(etat.monde)}</span>
                {designEssai && quiAgit ? <em>{quiAgit}</em> : null}
              </div>
            ) : null}
            {/* ⌂ MENU : DANS LA BARRE, PAS DANS « Partie » (14/09/2026).
                Demande de l'utilisateur : « le bouton home devrait etre sur le
                header, et pas dans le bouton Partie ». Il etait au fond d'un
                menu deroulant, derriere deux clics, alors que quitter une
                partie est une action qu'on cherche directement. Les autres
                entrees de « Partie » se CONSULTENT en jouant (historique, log,
                journal) ; celle-ci fait SORTIR, et n'a rien a faire avec elles.

                En tete de barre : c'est le geste qui ramene en arriere, il se
                lit avant tout le reste, comme dans un navigateur.

                ⚠ FUSIONNE AVEC « Déconnexion complète » LE 24/09/2026 (demande
                de l'utilisateur, capture a l'appui : les deux actions cote a
                cote pretaient a confusion). Un clic ouvre `ModaleMenu`, qui
                choisit laquelle appeler -- voir sa definition plus haut. */}
            <button
              type="button"
              className="bh-bouton bh-menu"
              onClick={() => setMenuOuvert(true)}
              title={t('Revenir au menu principal')}
            >
              <span className="ico ico-menu" aria-hidden="true">⌂</span> {t('Menu')}
            </button>
            <BoutonVoirLaTable />
            <button
              type="button"
              className="bh-bouton bh-undo"
              onClick={annulerCoup}
              title={t('Annuler la dernière action')}
            >
              {/* « Annuler » se traduit ici « Undo » (le dictionnaire réserve
                  « Annuler » -> « Cancel » pour l'assistant d'action). */}
              <span className="ico ico-annuler" aria-hidden="true">↶</span> {langueActuelle() === 'fr' ? 'Annuler' : 'Undo'}
            </button>
            <PopoverSauvegardes />
            {/* Signaler un bug : le journal de toute la partie part avec la
                description et la capture. Ne s'affiche que si un site ecoute. */}
            <PanneauBug outils={rapport} />

            {/* ⚠ LA VUE RESTE DANS LA BARRE, ET C'EST UNE DECISION ECRITE.
                La fiche des onglets du 14/09/2026 le dit mot pour mot : « la
                Vue reste dans la barre (elle change a chaque tour en
                multijoueur) ». La refonte l'avait pourtant rangee DANS le
                bouton « Partie », donc derriere deux clics, et l'utilisateur
                l'a signale en partie a plusieurs le 15/09/2026 : « j'ai plus le
                bouton dans le header pour choisir de voir tous les heros ou
                que celui que je selectionne ». Elle est revenue ici.

                Elle ne s'affiche qu'a PLUSIEURS : en solo il n'y a qu'une vue
                possible, un bouton n'y proposerait rien.

                MANUEL DECLARE (tache 7 bis, 19/09/2026 ; `modeManuelDeclare`,
                PAS `manuel`, depuis la ronde de correction 1 de la tache 3) :
                ce bandeau-ci suppose un moteur qui interroge quelqu'un
                (« Auto » = suivre celui qui doit agir). En manuel DECLARE le
                moteur ne demande plus jamais rien, « Auto » n'y elirait donc
                jamais personne — deux selecteurs affichant des choses
                differentes sur le meme ecran serait la pire des confusions.
                `SelecteurHeros`, plus bas, le remplace : meme etat
                (`vueForcee`), sans le concept d'Auto qui n'a pas de sens ici.

                ⚠ NE PAS SE REGLER SUR `manuel` (l'ETAT, `leMoteurSeTait`) :
                il vaut aussi vrai pendant une simple PAUSE d'une partie
                ORDINAIRE (tache 3), qui doit au contraire GARDER ce
                selecteur — la contrainte la plus lourde de ce plan est que
                le mode ordinaire ne perde rien, et une pause en est un
                moment. `SelecteurHeros` ne prend pas le relais en pause
                (arbitrage n°2, delibere : voir mode.ts), donc sans ce
                correctif une table a plusieurs heros mise en pause perdait
                TOUT selecteur de vue. */}
            {!modeManuelDeclare && (etat.monde?.players?.length ?? 0) > 1 ? (
              <span className="bh-vue" title={t('Quel héros est affiché (plateau et main)')}>
                <span className="bh-vue-label">{t('Vue')}</span>
                <button
                  type="button"
                  className={`bh-bouton${vueForcee === null ? ' est-actif' : ''}`}
                  title={t('Suivre celui qui doit agir')}
                  onClick={() => setVueForcee(null)}
                >
                  Auto
                </button>
                {/* Un joueur elimine n'est plus une vue possible : sa table a
                    disparu (voir zones.ts), il n'y aurait rien a regarder. */}
                {/* ⚠ TOUR TERMINE, ONGLET GRISE (24/09/2026, inspire
                    d'Arkham Horror LCG qui grise la carte d'un investigateur
                    dont le tour est fini). Purement visuel -- le bouton reste
                    cliquable, on peut toujours aller regarder la main d'un
                    heros qui a deja joue. */}
                {etat.monde!.players.map((joueur, i) =>
                  joueur.is_eliminated ? null : (
                    <button
                      type="button"
                      key={i}
                      className={`bh-bouton${vueForcee === i ? ' est-actif' : ''}${joueurActif === i ? ' est-joueur-actif' : ''}${joueur.has_finished_turn_this_round ? ' est-tour-fini' : ''}`}
                      title={`${joueur.area_hero?.[0]?.name ?? `${t('Joueur')} ${i}`}${joueur.has_finished_turn_this_round ? ` — ${t('tour terminé')}` : ''}`}
                      onClick={() => setVueForcee(i)}
                    >
                      {joueur.area_hero?.[0]?.name?.replace(/^\W*/, '').split(' ')[0] ?? `P${i}`}
                    </button>
                  )
                )}
              </span>
            ) : null}
            {/* Le sélecteur de héros du mode manuel (tâche 7 bis) : une main
                à l'écran, ce bouton pour passer de l'une à l'autre. Branché
                sur `vueForcee`, le même état que la vue automatique utilise
                déjà pour calculer `joueurActif` — pas de second chemin de
                vue. `SelecteurHeros` se tait déjà tout seul à un seul héros ;
                `joueursAffichables` (mémoisé plus haut) est la même liste que
                l'ancien bandeau utilisait, éliminés exclus. */}
            {modeManuelDeclare ? (
              <SelecteurHeros joueurs={joueursAffichables} regarde={joueurActif} onRegarder={setVueForcee} />
            ) : null}
            {/* PLUS DE FENETRE « Plus d'options » (04/10/2026, choix de
                l'utilisateur, questions une a une) : elle coutait un clic de
                plus. La pause a son bouton (visible quand elle est possible),
                la langue aussi, ⚙ ouvre directement les Reglages, et le
                journal reste sur sa languette. */}
            <InterrupteurFacon
              manuel={manuel}
              commenceEnManuel={modeManuelDeclare}
              lectureSeule={spectateur}
              questionOuverte={moteurAttendLeJoueur}
              onManuel={() => basculerPause(true)}
              onReprendre={() => basculerPause(false)}
              onReprendreA={reprendreEnAuto}
            />
            <button
              type="button"
              className="bh-bouton bh-langue"
              onClick={() => {
                void basculerLangue()
              }}
              title={
                langueActuelle() === 'fr'
                  ? 'Interface et narration en français : cliquer pour passer en anglais'
                  : 'Interface and narration in English: click to switch to French'
              }
            >
              {langueActuelle() === 'fr' ? 'FR' : 'EN'}
            </button>
            <button
              type="button"
              className={`bh-bouton bh-plus${reglagesOuverts ? ' est-actif' : ''}`}
              onClick={() => setReglagesOuverts(true)}
              aria-haspopup="dialog"
              aria-label={t('Réglages')}
              title={t('Réglages')}
            >
              <span className="ico ico-reglages" aria-hidden="true">{'\u2699\ufe0f'}</span>
            </button>

            {/* Fin du tour : le seul bouton colore, toujours a droite.
                MASQUE EN MODE MANUEL (tache 8 bis) : il n'y a plus de tour
                a finir une fois la boucle manuelle entree, le moteur ne
                conduit plus rien. Signale par la tache 8 sans etre teste ;
                couvert par plateau-muet.test.tsx desormais. */}
            {manuel ? null : (
            <button
                type="button"
                className={`bh-bouton bh-fin-tour${finDeTourSuggeree ? ' est-suggere' : ''}`}
                disabled={!finDeTourDisponible}
                onClick={interaction.annuler}
                title={
                  finDeTourSuggeree
                    ? t('Plus rien n\u2019est jouable — termine ton tour')
                    : finDeTourDisponible
                      ? t('Terminer ton tour')
                      : t('Fin du tour possible quand le moteur te rend la main')
                }
              >
                <span className="ico ico-fin-du-tour" aria-hidden="true">▷</span> {t('Fin du tour')}
                {finDeTourSuggeree ? ' ✓' : ''}
            </button>
            )}
          </div>
        }
        interactifs={interactifsAvecPulse}
        raisonsRefus={raisonsRefus}
        glisser={reglagesGlisser}
        bloquerActionsPassives={interaction.option !== undefined}
        mainVisibleForcee={mainVisibleForcee({
          // Manuel DÉCLARÉ seulement (tâche 3, `modeManuelDeclare`, pas
          // `manuel`) : une PAUSE ne doit PAS forcer cet affichage (voir le
          // commentaire de `modeManuelDeclare` plus haut).
          modeManuelDeclare,
          ciblageEnCours: interaction.option !== undefined,
          etapeAssistant: interaction.assistant.etape,
          carreDeLaPhase: nouvelleScenePC && (phaseMechantEnCours || etatQuestion.coupHorsPhaseEnScene === true),
          questionAuJoueur: moteurAttendLeJoueur && autreJoueurInterroge === undefined,
        })}
        delave={effetsAffiches(etat.monde, meteo, apercuMeteo).some((e) => EFFETS_DELAVANTS.includes(e))}
        onCardClick={
          etat.aNous && etat.connecte && !interaction.option
            ? (carte) => {
                const id = Number(carte.id)
                if (representantsPulseHorsTable.has(id) && ouvrirCiblesHorsTable(optionSurvolee)) {
                  return
                }
                if (modeActions === 'simple') {
                  const optionsSource =
                    demandeOrdinaire?.options.filter((option) => option.bind_id === id) ?? []
                  const identiteId = etat.monde?.players?.[joueurActif]?.area_hero?.[0]?.id
                  const aActionsGenerales =
                    id === identiteId &&
                    (demandeOrdinaire?.options.some((option) => option.bind_id === 0) ?? false)
                  const peutFinirTour =
                    id === identiteId && demandeOrdinaire?.show_cancel === true
                  if (optionsSource.length > 0 || aActionsGenerales || peutFinirTour) {
                    interaction.focaliserCarte(id)
                  }
                  return
                }
                const carteMonde = cartesMondeParId.get(id)
                const actionsVersCible = optionsDisponiblesVersCible(
                  demandeOrdinaire?.options ?? [],
                  id
                )
                if (actionsVersCible.length === 1 && !tablette) {
                  choisirOptionDepuisMenu(actionsVersCible[0]!, [id])
                  return
                }
                if (actionsVersCible.length > 1 || estCibleExpliquee(carteMonde)) {
                  interaction.focaliserCible(id)
                  return
                }
                interaction.focaliserCarte(id)
              }
            : undefined
        }
        bas={
          !manuel && modeActions === 'detailed' ? (
            <BarreAction
              demande={etat.demande}
              interaction={interaction}
              aNous={etat.aNous}
              connecte={etat.connecte}
              nomPorteur={nomPorteurFr}
              questionPriseParLePanneau={priseManigance !== undefined}
            />
          ) : undefined
        }
      />

      {afficherFinTourSimple && modePlateau !== 'mobile' ? (
        <button
          type="button"
          className={`bouton-fin-tour${finDeTourSuggeree ? ' est-suggere' : ''}`}
          onClick={interaction.annuler}
          title={
            finDeTourSuggeree
              ? t('Plus rien n\u2019est jouable — termine ton tour')
              : t('Terminer ton tour')
          }
        >
          {t('Fin du tour')}{finDeTourSuggeree ? ' ✓' : ''}
        </button>
      ) : null}

      {/* La fenetre des reglages. ⚠ RENDUE HORS DE LA BARRE, au meme niveau
          que les autres couches : ancree dans la barre, elle aurait herite de
          son `overflow` et de son empilement, c'est-a-dire exactement le
          travers qu'on corrige. */}
      <FenetreReglages
        ouvert={reglagesOuverts}
        fermer={() => {
          setReglagesOuverts(false)
          setReglagesVus(false)
        }}
        lectureSeule={spectateur}
        affichage={affichage}
        changerAffichage={changerAffichage}
        teinte={teinte}
        changerTeinte={changerTeinte}
        reinitialiserTeinte={reinitialiserTeinte}
        // « Modifier la table » : plateau PC seulement (telephone inchange).
        modifierLaTable={
          modePlateau !== 'mobile'
            ? () => {
                setReglagesOuverts(false)
                setEditionTable({
                  d: dispositionTable === DISPOSITION_ORIGINE ? DISPOSITION_DE_DEPART : dispositionTable,
                  origine: false,
                })
              }
            : undefined
        }
        animations={animations}
        basculerAnimations={basculerAnimations}
        sons={sons}
        basculerSons={basculerSons}
        musique={musique}
        basculerMusique={basculerMusique}
        scansFr={scansFr}
        dosCartes={dosCartes}
        changerDosCartes={changerDosCartes}
        basculerScansFr={basculerScansFr}
        textesCdb={textesCdb}
        basculerTextesCdb={basculerTextesCdb}
        basculerLangue={basculerLangue}
        modePhase={modePhaseChoisi}
        changerModePhase={choisirModePhase}
        avancePhaseHote={phaseEssai && !spectateur && playerId === 0 && herosDesAutresIds.size > 0}
        libelleModePhase={libelleModePhase}
        tempsParDecision={etat.maxTimeout}
        texteTempsParDecision={texteTempsParDecision}
        validationCourte={validationCourte}
        basculerValidationCourte={basculerValidationCourte}
        autoCible={autoCible}
        basculerAutoCible={basculerAutoCible}
        finTourAuto={finTourAutoChoix === 'on'}
        basculerFinTourAuto={basculerFinTourAuto}
        paiementAuto={interaction.paiementAutoChoix === 'on'}
        basculerPaiementAuto={interaction.basculerPaiementAuto}
        sauvegardeAuto={sauvegardeAuto}
        basculerSauvegardeAuto={basculerSauvegardeAuto}
        revelation={revelation}
        cyclerRevelation={cyclerRevelation}
        meteo={meteo}
        basculerMeteo={basculerMeteo}
        apercuMeteo={apercuMeteo}
        reglerApercuMeteo={reglerApercuMeteo}
        reponseAmbiance={reponseAmbiance}
        cyclerReponseAmbiance={cyclerReponseAmbiance}
        designEssai={designEssai}
        basculerDesignEssai={basculerDesignEssai}
        modeActions={modeActionsChoisi}
        changerModeActions={changerModeActions}
        curseurs={curseurs}
        basculerCurseurs={basculerCurseurs}
        montrerDisposition={surAppareilMobile}
        reglageMode={reglageMode}
        cyclerReglageMode={cyclerReglageMode}
        telephone={telephone}
        tablette={tablette}
      />
      {/* Les trois modales de la refonte du header (24/09/2026), HORS DE LA
          BARRE pour la meme raison que `FenetreReglages` juste au-dessus :
          ancrees dans la barre, elles heriteraient de son `overflow` et de
          son empilement. */}
      <ModaleMenu
        ouvert={menuOuvert}
        fermer={() => setMenuOuvert(false)}
        retourMenu={retourMenu}
        retourMenuPrincipal={() => { void retourMenuPrincipal() }}
      />
      {manuel ? (
        <>
          <VoletAideManuel ouvert={aideManuelOuverte} ouvrir={ouvrirAideManuel} fermer={fermerAideManuel} />
          <CoucheMarques marques={marquesManuel} />
          <CoucheSelection />
        </>
      ) : (
        <VoletAideAuto
          ouvert={aideAutoOuverte}
          ouvrir={ouvrirAideAuto}
          fermer={fermerAideAuto}
          telephone={modePlateau === 'mobile'}
        />
      )}
      {assembleeExportee ? (
        <VoletAssemblee
          assemblee={assembleeExportee}
          ouvert={assembleeOuverte}
          ouvrir={() => setAssembleeOuverte(true)}
          fermer={() => setAssembleeOuverte(false)}
        />
      ) : null}
      {villeExportee ? (
        <VoletVille
          ville={villeExportee}
          moi={joueurActif}
          nomsJoueurs={nomsJoueursVille}
          optionDeplacement={optionSeDeplacer(etat.demande?.options)}
          seDeplacer={(option, objetLieu) => choisirOptionDepuisMenu(option, [objetLieu], true)}
          catalogue={catalogue}
          ouvert={villeOuverte}
          ouvrir={() => setVilleOuverte(true)}
          fermer={() => setVilleOuverte(false)}
        />
      ) : null}
      <VoletJournal ouvert={partieOuverte} ouvrir={ouvrirVolet} fermer={fermerVolet}>
        <CartesDuJournal.Provider value={cartesDuVolet}>
        <MessageRapport message={rapport.message} />
        <JournalConsole
          entrees={historique.entrees}
          effacer={historique.effacer}
          rapport={rapport}
          telechargerLog={() => rapport.telecharger('partie', 'txt')}
          etapesDuMechant={sceneCentrale ? undefined : etapesDuMechantParRound}
          // En scene PC, la phase precedente se relit dans le cartouche du bas
          // (D38) ; la table et le telephone gardent la revue du volet.
          revuePhase={
            etapesPhasePrecedente.length > 0 && !nouvelleScenePC ? (
              <RevuePhase etapes={etapesPhasePrecedente} pvMaxParNom={pvMaxParNom} nomFr={nomPorteurFr} />
            ) : undefined
          }
          onRevoirPhase={
            etapesPhasePrecedente.length > 0 && nouvelleScenePC
              ? () => {
                  // Le volet se referme : il passerait par-dessus le cartouche.
                  fermerVolet()
                  setRelectureJournal(true)
                }
              : undefined
          }
          journalHeros={
            <JournalHeros
              entrees={historique.entrees}
              monde={etat.monde}
              joueur={joueurActif}
              nomHeros={etat.monde.players?.[joueurActif]?.area_hero?.[0]?.name?.replace(/^\W*/, '')}
              toujoursVisible
            />
          }
        />
        </CartesDuJournal.Provider>
      </VoletJournal>
      <BandeauConnexion
        etat={etat}
        reconnecter={reconnecter}
        peutAvoirEteFermee={laTablePeutAvoirEteFermee({ siege: playerId, spectateur, site })}
      />
      {modeRevoir ? <BarreRevoir pasTotal={modeRevoir.pas} /> : null}
      {/* ⚠ LA TABLE SE TAIT PENDANT QUE LA SCENE RACONTE (15/09/2026).
          Voir `animations-en-scene.ts` : en mode Detaille, la fenetre montrait
          l'etape pendant que le plateau rejouait le meme evenement en
          mouvement, derriere elle. Deux recits en meme temps. */}
      <CoucheAnimations
        renderId={etat.monde.render_id}
        actif={animationsDuPlateau({
          reglage: animationsActives,
          sceneCentrale,
          phaseMechantEnCours,
          enMiseEnPlace,
        })}
      />
      <CoucheRefusEffets refus={etat.monde.refus_effets} />
      <CoucheChoixUniques choix={etat.monde.choix_uniques} />
      <CoucheTriche
        actif={triche.actif}
        manuel={triche.manuel}
        couche={triche.couche}
        catalogue={catalogue}
        siege={joueurActif}
        cartesParId={cartesMondeParId}
      />
      {/* En Detaille, pendant la phase du mechant, la scene montre deja la
          carte revelee face visible, avec ce qu'elle a fait : la couche a
          duree la remontrait en grand par-dessus, une seconde fois. Constate
          par l'utilisateur : « il montre quand meme encore la derniere carte
          en grand, en dehors de la modale ». Hors de cette phase (une carte
          revelee par un effet pendant le tour du heros), elle garde son role. */}
      {/* ⚠ ET PAS PENDANT QUE LE PANNEAU TIENT LA QUESTION (15/09/2026). Une
          manigance ANNEXE entre en jeu en passant par `Reveal` (trace :
          `01116a.py` -> `SetupCards.Reveal` -> `Reveal` -> `PutIntoPlay`) :
          cette couche la montrerait donc en grand au centre, en meme temps que
          le panneau qui la montre deja. Deux presentations de la meme carte,
          l'une par-dessus l'autre, exactement le defaut n°2 du 14/09. */}
      {/* ⚠ ET PLUS DU TOUT EN SCENE PC (D42, lot 5 de la refonte) : le
          cartouche du bas montre la carte revelee, pendant la phase comme
          pendant le tour (« Pendant ton tour »). Seule la mise en place garde
          la manigance principale en grand : elle n'a pas de cartouche. */}
      {(unCartouche && phaseMechantEnCours) || priseManigance || (nouvelleScenePC && !enMiseEnPlace) ? null : (
        <CoucheRevelation
          monde={etat.monde}
          duree={DUREES_REVELATION[revelation]}
          joueurId={joueurActif}
          seulementManigance={enMiseEnPlace}
        />
      )}
      <CoucheCharge
        renderId={etat.monde.render_id}
        eventName={etat.monde.event_name ?? ''}
        activeIds={etat.monde.active_card_ids ?? []}
        actif={animationsDuPlateau({
          reglage: animationsActives,
          sceneCentrale,
          phaseMechantEnCours,
          enMiseEnPlace,
        })}
      />

      {/* Le seul mouvement de toute l'ouverture : la face A de la manigance
          principale, montree en grand pendant que le moteur attend la
          confirmation avant de la retourner (World.ConfirmMainSchemeReveal).
          Le voile ci-dessus garantit que la table est deja montee derriere. */}
      <PlacesEnAttente ids={attenteMep.cachees} />
      <CoucheMiseEnPlace
        etape={panneauPrioritaire || mechantRetenu ? undefined : miseEnPlace.etape}
        paire={miseEnPlace.paire}
        restantes={miseEnPlace.restantes}
        suivant={miseEnPlace.suivant}
        animations={animationsActives}
      />
      {priseManigance && (!miseEnPlace.etape || panneauPrioritaire) ? (
        <PanneauManigance
          carte={priseManigance.carte}
          /* Seule la manigance PRINCIPALE se retourne : elle a deux faces
             imprimees et le moteur la retourne. Une annexe n'en a qu'une, elle
             vient simplement d'entrer en jeu. Pendant la mise en place, la
             face A se montre AVANT ses capacites et le moteur ne la retourne
             qu'a l'etape 12b : c'est la mise en place pas a pas qui montre
             alors la face B (10/10/2026). */
          retournement={priseManigance.question.name === NOM_OPTION_MANIGANCE && !(enMiseEnPlace && etat.monde.confirm_scheme_setup_order === true)}
          versoUrl={autresFacesDe(priseManigance.carte, catalogue)[0]?.url}
          versoCode={autresFacesDe(priseManigance.carte, catalogue)[0]?.code}
          versoType={autresFacesDe(priseManigance.carte, catalogue)[0]?.type}
          voleVers={animationsActives ? panneauEnAttente : undefined}
          onValider={() =>
            repondre(
              { id: priseManigance.question.id, targets: [], resources: [] },
              priseManigance.question.bind_player_id
            )
          }
        />
      ) : null}

      {/* L'ecran de fin attend que le coup fatal ait ete vu (mode Detaille,
          heros de ce siege), avec un filet de 20 s : voir
          `afficherFinDePartie`. Hors de ce cas, il parait sur la trame meme ou
          le moteur declare la partie finie, comme avant. */}
      {finPartieAffichee && etat.monde ? (
        <EcranFinPartie
          {...finDePartie(etat.monde, playerId)}
          raison={etat.monde.game_over_reason}
          monde={etat.monde}
          siege={playerId}
          retourSalon={inviteDeTable}
          onMenu={retourMenu}
          onDeconnexion={retourMenuPrincipal}
        />
      ) : null}
      </PlusieursJoueurs.Provider>
    </CartesDuJournal.Provider>
  )
}

/**
 * L'INTERIEUR DU CADRE (spectateur et relecture, 08/10/2026) : le plateau seul,
 * au siege regarde, avec les reglages du joueur (genre « regl »). Voir
 * cadre-joueur.ts et CadreJoueur.tsx.
 */
/** Les menus ouverts du joueur (genre « menu ») : Reglages, Menu, journal, aide manuel, aide auto. */
type MenusOuverts = { r: boolean; m: boolean; j: boolean; am: boolean; aa: boolean }

function PageCadre() {
  const lecteur = lecteurActif()
  const siegeLu = useSyncExternalStore(
    (rappel) => lecteur?.ecouterControle(rappel) ?? (() => undefined),
    () => lecteur?.lireControle().pointDeVue ?? 0
  )
  const siege = lecteur ? siegeLu : parametres().playerId
  const [catalogue, setCatalogue] = useState<Catalogue>(catalogueVide)
  useEffect(() => {
    chargerCatalogue().then(setCatalogue).catch(() => undefined)
  }, [])
  useEffect(() => {
    // Les feuilles du plateau sont chargees au plus tard a `load`.
    if (document.readyState === 'complete') poserSurvolsDuJoueur()
    else window.addEventListener('load', () => poserSurvolsDuJoueur(), { once: true })
  }, [])
  const reglages = useVuDuJoueur<Record<string, string>>('regl', siege)
  const [version, setVersion] = useState(0)
  useEffect(() => {
    const copie = stockageDuCadre()
    if (!copie || !reglages) return
    recouvrir(copie, reglages)
    appliquerAffichage(lireAffichage())
    appliquerEtiquettesTable(lireEtiquettesTable())
    setVersion((v) => v + 1)
  }, [reglages])
  const modeActions = useMemo(() => lireModeActions(), [version])
  return (
    <FournisseurConfirmation>
      <PagePartie
        key={`${siege}-${version}`}
        playerId={siege}
        catalogue={catalogue}
        modeActions={modeActions}
        changerModeActions={() => undefined}
      />
    </FournisseurConfirmation>
  )
}

/** Celui qui regarde en direct : sa barre, et le cadre du joueur. */
function PageSpectateur() {
  const { playerId } = parametres()
  const [infos, setInfos] = useState<{ sieges: number; terminee?: boolean; raison?: string }>({ sieges: 1 })
  useEffect(() => {
    const recevoir = (message: MessageEvent) => {
      if (message.origin !== window.location.origin) return
      const donnees = message.data as { type?: string; sieges?: number; terminee?: boolean; raison?: string }
      if (donnees?.type !== 'etat-spectateur') return
      setInfos({ sieges: Number(donnees.sieges) || 1, terminee: donnees.terminee, raison: donnees.raison })
    }
    window.addEventListener('message', recevoir)
    return () => window.removeEventListener('message', recevoir)
  }, [])
  const src = `${window.location.pathname}${window.location.search}${window.location.search ? '&' : '?'}cadre`
  return (
    <>
      <BarreSpectateur siege={playerId} sieges={infos.sieges} terminee={infos.terminee} raison={infos.raison} />
      <CadreJoueur src={src} siege={playerId} haut={32} />
    </>
  )
}

function Page() {
  const { etat, playerId } = parametres()
  // Le catalogue ne fait que completer les pastilles PV (« 1/3 » au lieu de
  // « 1 ») : le plateau ne l'attend pas pour s'afficher.
  const [catalogue, setCatalogue] = useState<Catalogue>(catalogueVide)
  const [modeActions, setModeActions] = useState<ModeActions>(() => lireModeActions())

  useEffect(() => {
    chargerCatalogue().then(setCatalogue).catch(() => undefined)
  }, [])

  const changerModeActions = useCallback((mode: ModeActions) => {
    setModeActions(mode)
    try {
      window.localStorage.setItem(CLE_MODE_ACTIONS, mode)
    } catch {
      // Preference non critique : si le navigateur refuse localStorage, le mode
      // simple par defaut reste utilisable.
    }
  }, [])

  const outils = (
    <Outils modeActions={modeActions} changerModeActions={changerModeActions} />
  )

  // Le fournisseur enveloppe TOUT : les deux ecrans posent des questions
  // bloquantes, et le dialogue doit exister avant qu'on la pose.
  if (estCadre()) return <PageCadre />
  return (
    <FournisseurConfirmation>
      {estRelecture() ? (
        <PageRelecture />
      ) : parametres().spectateur ? (
        <PageSpectateur />
      ) : etat ? (
        <PageEtat fichier={etat} playerId={playerId} catalogue={catalogue} outils={outils} />
      ) : (
        <PagePartie
          playerId={playerId}
          catalogue={catalogue}
          modeActions={modeActions}
          changerModeActions={changerModeActions}
        />
      )}
    </FournisseurConfirmation>
  )
}

// Le serveur de developpement peut reexecuter ce module sans recharger la page
// (reoptimisation des dependances, mise a jour a chaud). Un second createRoot sur
// le meme noeud casse le rendu : « container that has already been passed to
// createRoot », puis un removeChild qui vide la page. On garde donc la racine.
declare global {
  interface Window {
    racinePlateau?: Root
  }
}

// Sous vitest, ce module est importe pour ses COMPOSANTS, pas pour monter la
// page : le point d'entree ne doit alors rien faire. En dehors, le `throw` est
// maintenu — une page sans son noeud de montage est une page cassee, elle doit
// le dire tout de suite.
if (!import.meta.env.VITEST) {
  const cible = document.getElementById('plateau')
  if (!cible) throw new Error('Element #plateau not found in board.html')
  synchroniserLangueServeur()
  // Avant le premier rendu, et pour TOUTES les pages (etat enregistre, revoir,
  // salon) : le plateau en partie le reapplique ensuite a chaque changement.
  appliquerAffichage(lireAffichage())
  appliquerEtiquettesTable(lireEtiquettesTable())
  appliquerTeinte(lireTeinteDuNavigateur())
  window.racinePlateau ??= createRoot(cible)
  window.racinePlateau.render(<Page />)
}
