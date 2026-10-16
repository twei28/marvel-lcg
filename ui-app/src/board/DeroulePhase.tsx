// La scene centrale du deroule detaille : une etape a la fois.
//
// FIXE au centre de l'ecran, elle ne bouge jamais d'une etape a l'autre :
// l'oeil sait ou lire et la main ou cliquer des le deuxieme tour. Elle montre
// les cartes de l'etape (auteur, boosts, cible, carte revelee) toutes a la
// MEME taille, face visible, tirees de l'index du monde et jamais de la table
// : la table derriere est assombrie et n'est plus a lire pendant la phase,
// elle peut etre en avance sur le recit (spec du 7 septembre 2026,
// docs/superpowers/specs/2026-09-07-scene-phase-mechant-design.md).
//
// « Precedent » RELIT, il ne rejoue rien : le monde du moteur ne recule pas.
// C'est « Annuler la derniere action » qui fait cela, et il reste disponible.
//
// Quand le moteur pose une QUESTION au joueur (dans quel ordre activer deux
// sbires, defendre ou non), le cartouche s'efface : il se replie sur sa seule
// chronologie et dit que le moteur attend le joueur. Ce n'est pas la meme
// attente que « La suite arrive… », ou c'est le joueur qui attend le moteur.

import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type PointerEvent as ReactPointerEvent,
  type ReactNode,
} from 'react'
import { createPortal } from 'react-dom'
import { estSpectateur } from './moteur'
import { indexSpectateur, publierExtrasEtape, useSuiviDuJoueur } from './etape-partagee'
import {
  choisirPolitique,
  lectureASuivre,
  peutAvancer,
  siegeMeneur,
  siegesPrets,
  tousPrets,
  useAvanceMulti,
  type PolitiqueAvance,
} from './avance-multi'
import type { ScanCardProps } from '../components/ScanCard'
import { ScanCardTraduite } from './traduction-carte'
import {
  arreterSurDefaite,
  avecBilan,
  estDefaiteLocale,
  rangDansLeTemps,
  type EtapeDeroule,
  type TempsPhase,
} from './deroule-phase'
import {
  compteurLigneBilan,
  detailEtape,
  evolutionEtape,
  texteActivationAnnulee,
  texteCauseActivation,
  texteArretDefaite,
  texteAttente,
  texteFiletProche,
  texteBilanVide,
  texteDefaite,
  texteEffet,
  texteConsequence,
  texteFenetreReponse,
  texteLigneBilan,
  texteTempsParDecision,
  titreEtape,
  decouperPhrase,
  resultatEtape,
  surtitreEtape,
  texteSuiteRenfort,
  lignesEtoileBoost,
} from './deroule-textes'
import { t } from './langue'
import { CarteApercu } from './Board'
import { useApercuSurvol } from './apercu-survol'
import { sceneDe, type CarteDeScene } from './deroule-scene'
import { useDerouleScene } from './useDerouleScene'
import { useAncrageSurTable } from './useAncrageSurTable'
import { cartesConcernees, useSurbrillanceEtape } from './surbrillance-etape'
import './deroule-onglets.css'
import { ONGLETS, avecTempsVides, resumeOnglet, type CleOnglet } from './frise-phase'
import { DetailCoup, ListeDesCoups } from './DetailCoup'
import { etapeEnLangue } from './etape-en-langue'
import { useGlisserPanneau } from './placement/useGlisserPanneau'
import { cadreDeLEtape, styleDuCadre, type CadreJoueur } from './couleur-joueur'
import { CoucheTraitPhase, EffetsSurTable } from './CoucheTraitPhase'
import { FlechesPhase } from './FlechesPhase'
import { TrajetsPhase } from './TrajetsPhase'
import { EtoilesEnAttente } from './EtoilesEnAttente'
import { NumerosSbires } from './NumerosSbires'
import { DepartsDeLaBoite } from './DepartsDeLaBoite'
import { cartoucheEstAJour } from './cartouche-a-jour'
import { CoucheRencontreSurTable } from './CoucheRencontreSurTable'
import { JetonMenaceVolant } from './JetonMenaceVolant'
import { alerteMenace, contenuDuTrait } from './trait-phase'
import './boutons-bd.css'
// ⚠ APRES boutons-bd.css : CartouchePhase importe sa feuille, qui doit passer
// la DERNIERE (cartouche-phase.css, hors couche).
import { CartouchePhase, PictoBoost, PictoStat, type CartouchePhaseProps, type PiedMulti } from './CartouchePhase'
import { boutonPageSuivante, cibleDeLaTouche, clavierBloque } from './clavier-cartouche'
import type { QuestionDuMoteur } from './sous-cadre'
import {
  calculMenace,
  pastilleDuTemps,
  sortiesDeLEtape,
  texteDeLaChaine,
  type ClePastille,
  type InfoRevelee,
} from './vue-cartouche'
import './cartouche-essai-tel.css'
import { avecEcranElimination, avecEcranStadeRevele, avecEtapesEtoileDifferee, avecEtapesRiposte } from './etapes-essai'

/**
 * Le temps de VOIR une etape qui vise un autre joueur, avant qu'elle passe.
 *
 * Assez long pour suivre le coup des yeux, assez court pour ne pas faire
 * attendre celui qui ne peut rien y faire. C'est son joueur a lui qui donne le
 * vrai rythme : le moteur attend SON accuse de reception, pas le notre.
 */
const DELAI_ETAPE_D_UN_AUTRE_MS = 2200

/** Le temps de lire un boost a capacite avant le suivant. */
const DELAI_BOOST_MS = 1500

/** L'aide de la bulle « Sur la table » a deja ete lue (v3, Q47). */
const CLE_AIDE_TABLE = 'mc_aide_bulle_table'

// ⚠ PLUS DE « TOUT DEROULER » (Echap) : pas a pas strict, decision de
// l'utilisateur du 03/10/2026. Le defilement et son delai sont retires.

/**
 * A partir de quand le cartouche annonce le filet anti-blocage.
 *
 * Le filet relache la phase au bout de `DELAI_FILET_ANTI_BLOCAGE_CLIC_MS`
 * (moteur.ts) pour qu'un onglet fantome ne gele pas la table entiere. Sans un
 * mot, le joueur voit la phase repartir toute seule et n'a aucun moyen de
 * comprendre pourquoi. Quinze secondes : le temps de finir de lire l'etape et
 * de cliquer, jamais assez pour devenir un compte a rebours anxiogene affiche
 * pendant une minute et demie.
 */
export const DELAI_ALERTE_FILET_MS = 15_000

// LES SIX ONGLETS (intitules officiels numerotes, puis le Bilan) : voir
// `ONGLETS`, frise-phase.ts.

/**
 * Le nom d'un onglet, son NUMERO a part (« 1. » puis « Placer les menaces ») :
 * sur telephone, seul le numero reste, en pastille (decision du 03/10/2026).
 */
function nomDOnglet(libelle: string): ReactNode {
  const morceaux = /^(\d+[ab]?\.)(.*)$/.exec(libelle)
  if (!morceaux) return <span className="deroule-onglet-libelle">{libelle}</span>
  return (
    <>
      <span className="deroule-onglet-numero">{morceaux[1]}</span>
      <span className="deroule-onglet-libelle">{morceaux[2]}</span>
    </>
  )
}

/** Repli stable (une nouvelle fonction a chaque rendu relancerait la mesure des fleches). */
const joueurInconnu = (): number | undefined => undefined

export function DeroulePhase({
  etapes: etapesRecues,
  presentation = 'scene',
  essai = false,
  dynamique = false,
  attendreBandeau = false,
  identitePhase,
  identitePartie,
  phaseMechantEnCours = false,
  partieFinie = false,
  questionAuJoueur = false,
  tempsQuestion,
  carteScene,
  dosRencontre,
  nomFr,
  question,
  herosLocauxIds,
  herosDesAutresIds,
  attendUnAutreJoueur = false,
  nomJoueurAttendu,
  pvMaxParNom,
  trameRetenue,
  echeanceFilet,
  tempsParDecision = 0,
  telephone = false,
  cadresJoueurs,
  joueurDeCarte,
  siegeLocal,
  premierJoueur,
  nomsJoueurs,
  cartesDistribuees = 0,
  texteEtoile,
  infoCarte,
  infoRevelee,
  questionDuMoteur,
  questionDUnAutre,
  onSuivant,
  onActivite,
  onTerminer,
  onDefaiteVue,
  onEtapeAffichee,
  onAvantResultat,
}: {
  etapes: EtapeDeroule[]
  /**
   * L'essai « Nouvelle phase du méchant » (10/10/2026, coché par compte dans
   * /admin) : le cartouche du bas prend le nouveau rendu, et les boosts se
   * retournent UN PAR UN au clic au lieu de s'enchainer seuls. Faux : rien ne
   * change.
   */
  essai?: boolean
  /** « Phase dynamique » (16/10/2026) : le cartouche posé en panneau à droite de la table. Suppose `essai`. */
  dynamique?: boolean
  /**
   * OU l'etape est racontee. Deux presentations, UNE SEULE mecanique.
   *
   *  - « scene » : le cartouche central, par-dessus la table, avec les cartes
   *                de l'etape rejouees dedans. Le mode « Detaille », inchange.
   *  - « table » : le cartouche se pose A COTE DE LA CARTE qui vient d'agir,
   *                sur la table elle-meme, et ne rejoue aucune carte : ce sont
   *                les vraies cartes qu'on regarde. Le mode « Sur la table ».
   *
   * ⚠ LA MECANIQUE N'EST PAS DUPLIQUEE, ET C'EST LE POINT. Remise a zero entre
   * deux phases, bilan de fin, coup fatal,
   * filet anti-blocage : tout cela a ete mesure et corrige en partie reelle a
   * de multiples reprises (voir les commentaires de ce fichier). Un second
   * composant qui refarait « la meme chose en plus joli » aurait refait les
   * memes bugs. Seul le RENDU change.
   */
  presentation?: 'scene' | 'table'
  /**
   * Le bandeau d'ouverture de la phase joue encore : ne rien montrer.
   *
   * ⚠ N'AGIT QUE DANS LA PRESENTATION « table ». Demande de l'utilisateur,
   * 14/09/2026 : « d'abord le bandeau, puis apres on montre la manigance. On
   * attend que le bandeau soit parti. » Les deux se superposaient. Le mode
   * « Detaille » n'est pas touche : sa scene centrale coexiste avec le bandeau
   * depuis toujours, et personne ne s'en est plaint.
   *
   * ⚠ ON RETOURNE `null` APRES TOUS LES HOOKS, jamais avant. Le composant garde
   * son index, ses minuteurs et sa memoire d'etapes pendant ces deux secondes :
   * s'effacer n'est pas se demonter.
   */
  attendreBandeau?: boolean
  /**
   * L'identite de la phase en cours. board.tsx y passe `etat.monde.round_id` :
   * il y a une phase du mechant par round, donc le round suffit a distinguer
   * deux phases. La longueur de la liste ne peut PAS jouer ce role, puisqu'elle
   * grossit legitimement pendant la phase (chaque validation relache une trame
   * du moteur, qui produit l'etape suivante).
   *
   * Elle ne remet PAS le cartouche a zero a elle seule : le moteur incremente
   * le round au moment meme ou il quitte la phase du mechant, et le cartouche a
   * encore son bilan a montrer. C'est `phaseRacontee` (dans le corps du
   * composant) qui filtre, et c'est lui le declencheur de la remise a zero.
   */
  identitePhase?: number
  /**
   * La PARTIE en cours (board.tsx : `etat.partieId`, que le moteur renumerote
   * a chaque nouvelle partie mais PAS sur un « Annuler »).
   *
   * Elle existe parce qu'une nouvelle partie peut commencer SANS rechargement
   * de page (« Rejouer », retour au menu puis autre partie) : le monde revient
   * alors au round 1 en plein tour du joueur, et aucune des deux portes de
   * `phaseRacontee` ne s'ouvre. Voir le corps du composant.
   */
  identitePartie?: string
  /**
   * Vrai tant que le moteur est encore dans la phase du mechant (board.tsx :
   * `PHASES_DU_MECHANT.has(etat.monde.phase)`). Arriver au bout des etapes
   * CONNUES ne veut pas dire que la phase est finie : tant que celle-ci court,
   * le cartouche attend la suite au lieu de se masquer.
   */
  phaseMechantEnCours?: boolean
  /**
   * La partie est finie (board.tsx : `etat.monde.game_over`, la SEULE source
   * de cet etat, celle-la meme dont l'ecran de fin de partie se sert).
   *
   * Constate en partie : la manigance principale etait allee au bout, l'ecran
   * de defaite etait affiche, et le cartouche restait par-dessus le plateau a
   * annoncer « La suite arrive… » indefiniment. Il n'y a plus de suite : la
   * partie est finie, le cartouche s'efface.
   */
  partieFinie?: boolean
  /**
   * Le moteur pose une question au joueur LOCAL, dans son panneau central
   * (board.tsx : `afficherDemandeCentrale`, la condition meme qui affiche ce
   * panneau ; on la recoit, on ne la recalcule pas).
   *
   * Constate en partie (Bruce Banner contre Ultron) : le moteur demandait dans
   * quel ordre activer deux sbires, et le cartouche disait « La suite
   * arrive… » par-dessus la question, bouton compris. Le joueur attendait le
   * moteur, qui l'attendait. Tant que c'est vrai, le cartouche se replie sur
   * sa chronologie, sans titre ni bouton, et dit que le moteur attend la
   * reponse. Il ne disparait pas : le joueur doit encore savoir ou il en est.
   * Une fois la question resolue, il se redeploie la ou il en etait.
   *
   * A ne JAMAIS confondre avec `enAttente` (voir plus bas) : la, c'est le
   * joueur qui attend le moteur.
   */
  questionAuJoueur?: boolean
  /**
   * Le temps de la question en cours, d'apres la phase du moteur
   * (`tempsDeLaQuestion`) : la frise s'y cale quand l'etape correspondante
   * n'existe pas encore (l'attaque qu'on te demande de defendre).
   */
  tempsQuestion?: TempsPhase
  /**
   * LES CARTES DE LA SCENE (board.tsx : `carteScene`).
   *
   * Donne le scan d'une carte du monde par son identifiant, face visible
   * quand on le demande : la carte revelee et les boosts sont encore face
   * cachee dans le monde de la trame retenue (le fait est journalise AVANT
   * le retournement, player_action.py), et le joueur doit pourtant les lire.
   * Lue dans l'index du monde, jamais sur la table : une carte partie a la
   * defausse (un boost) se montre quand meme. Absente, ou muette sur une
   * carte : la scene montre le nom seul.
   */
  carteScene?: (id: number, faceVisible: boolean) => ScanCardProps | undefined
  /** Le dos d'une carte rencontre, pour l'etape de distribution. */
  dosRencontre?: ScanCardProps
  /**
   * LE NOM FRANCAIS d'une carte du monde, par son identifiant (board.tsx :
   * `nomPorteurFr`, qui lit fr.marvelcdb par le proxy du serveur). Les faits
   * du moteur portent les noms ANGLAIS ; sans lui, la scene disait
   * « Thunderball complote contre Thunderstruck » sous des scans qui disent
   * « Le Boulet » et « Envoyer Bouler ». Absent, ou muet : le nom du fait.
   */
  nomFr?: (id: number) => string | undefined
  /**
   * LA QUESTION DU MOTEUR, RENDUE PAR LE PLATEAU (board.tsx : le panneau
   * `DemandeCentrale` en mode scene). Quand elle est donnee, la scene reste
   * entiere (chronologie, cartes, intention) et la loge a la place de ses
   * boutons : « Defendre ? » se decide en voyant l'attaque. Sans elle, la
   * scene se replie comme avant, parce que la question se joue sur la table
   * (un ciblage) et que la table doit rester cliquable.
   */
  question?: ReactNode
  /**
   * LES DEUX FACES DU HEROS DE CE SIEGE (board.tsx : `herosLocauxIds`, lu sur
   * `?p=` et non sur la vue affichee).
   *
   * Elles ne servent qu'a une chose : savoir si la chute d'un heros est LA
   * NOTRE. La coupe du deroule (`arreterSurDefaite`) portait sur la liste
   * entiere, donc sur tous les clients : le cartouche d'un joueur s'arretait
   * quand le heros d'un AUTRE tombait, et ce joueur ne voyait jamais l'attaque
   * qu'il subissait ensuite (constat F5). Chez les autres, la chute reste une
   * etape marquee et la phase continue.
   *
   * Absentes ou vides (solo, previsualisation, monde pas encore lu) : toute
   * defaite compte comme la notre, c'est-a-dire le comportement d'avant.
   */
  herosLocauxIds?: ReadonlySet<number>
  /**
   * Les identites des AUTRES joueurs (board.tsx : `herosDesAutresIds`).
   *
   * ⚠ VIDE EN SOLO ET EN HOT-SEAT : la regle qui s'en sert ne joue qu'en vrai
   * multijoueur. Choix de l'utilisateur (14/09/2026) : « tout se joue sous tes
   * yeux, mais tu ne cliques que pour tes etapes ». Un coup porte a un autre
   * heros se montre, puis passe tout seul ; c'est SON joueur qui donne le
   * rythme, et le moteur l'attend de toute facon.
   */
  herosDesAutresIds?: ReadonlySet<number>
  /**
   * LA TABLE ATTEND QUELQU'UN D'AUTRE (board.tsx : `joueurAttendu`,
   * `joueurEnRetard` et `useTableSilencieuse`, dans `attente-table.ts`).
   *
   * Trois causes, une seule consequence a l'ecran : le moteur interroge un
   * autre siege, ou il retient sa trame parce qu'un autre client n'a pas
   * encore acquitte (`WaitSync`, cote Python), et ce retard est nomme sur un
   * moteur a jour, devine au silence sur un moteur ancien. Dans tous les cas
   * le plateau local n'a plus rien a faire, et « La suite arrive… » parlait
   * du MOTEUR : la decision 12 (« on attend tout le monde ») etait tenue par
   * le moteur et jamais dite a l'ecran (constat F5 de l'audit du 06/09/2026).
   */
  attendUnAutreJoueur?: boolean
  /**
   * Le NOM du joueur attendu, quand le moteur le donne.
   *
   * Deux cas le donnent : celui qu'il interroge (`ask_players[0]`) et celui
   * qui n'a pas encore accuse reception de la trame retenue
   * (`sieges_non_acquittes`, moteur a jour). Absent (moteur ancien qui ne
   * publie pas encore ce second champ), la mention reste vraie mais vague
   * (« En attente d'un autre joueur »). Voir l'en-tete de `attente-table.ts`.
   */
  nomJoueurAttendu?: string
  /**
   * Les PV maximum des personnages, par nom (board.tsx, qui lit le monde) :
   * sans eux le bilan de fin de phase dit « 8 » au lieu de « 8/14 ». Ils ne
   * peuvent pas venir des etapes, le moteur ne les publie pas a cote de ses
   * faits. Absents, ou muets sur une cible : le bilan montre le restant seul.
   */
  pvMaxParNom?: Map<string, number>
  /**
   * L'identite (`render_id`) de la trame que le moteur retient en ce moment,
   * ou `undefined` quand il n'en retient aucune (board.tsx :
   * `etat.trameRetenue`).
   *
   * Le cartouche s'en sert pour n'envoyer QU'UN accuse de reception par trame.
   * Un booleen (« le moteur attend ») ne suffirait pas : l'etat du cartouche
   * se recalcule plusieurs fois pour une meme trame, et l'accuse partirait
   * alors en rafale.
   */
  trameRetenue?: number
  /**
   * L'ECHEANCE du filet anti-blocage de la phase (board.tsx :
   * `etat.echeanceFilet`, un horodatage en ms), ou `undefined` quand aucun
   * filet n'est arme.
   *
   * Une seule par phase, cote moteur. Le cartouche n'en montre que les
   * dernieres secondes (`DELAI_ALERTE_FILET_MS`) : le joueur doit comprendre
   * que la phase va repartir sans lui, pas regarder un compte a rebours
   * pendant une minute et demie.
   */
  echeanceFilet?: number
  /**
   * « TEMPS PAR DECISION » regle a la preparation de mission, en secondes
   * (board.tsx : `etat.maxTimeout`, lu sur `max_timeout` dans la trame). Zero,
   * la valeur par defaut, veut dire « sans limite ».
   *
   * Il n'est la que pour etre DIT. Le mode Detaille repose sur une hypothese :
   * le moteur ne produit rien tant qu'on ne lui a pas repondu, donc le
   * cartouche donne le rythme. Non nul, cette hypothese tombe (`DoWaitSync` et
   * `DoGetInput` expirent, engine/device/manager/base.py) et le moteur poursuit
   * seul. Le cartouche ne change rien a son rythme pour autant : il le mentionne,
   * et c'est tout.
   */
  tempsParDecision?: number
  /**
   * LE PLATEAU EST CELUI DU TELEPHONE (board.tsx : `modePlateau === 'mobile'`).
   *
   * La scene du PC se dessine dans le cartouche du bas (`CartouchePhase`,
   * refonte du 04/10/2026) ; le telephone garde le rendu d'avant, inchange
   * pour ce chantier (D36). La table (`presentation="table"`) aussi.
   */
  telephone?: boolean
  /**
   * Refonte du 12/10/2026 (essai seulement) : le cadre de chaque joueur
   * (couleur de son aspect, `couleur-joueur.ts`) et le joueur a qui appartient
   * une carte de la table. Le bord de la boite prend la couleur du joueur
   * concerne par l'etape affichee.
   */
  cadresJoueurs?: CadreJoueur[]
  joueurDeCarte?: (id: number | undefined) => number | undefined
  /** Refonte, lot 6 (multi) : le siege de ce joueur et celui du premier joueur du round. */
  siegeLocal?: number
  premierJoueur?: number
  /** Le nom du heros de chaque siege, pour « J1 (Spider-Man) regarde… ». */
  nomsJoueurs?: string[]
  /**
   * Les cartes rencontre DISTRIBUEES pendant la phase, dont les etapes ont ete
   * retirees de la liste avant d'arriver ici (board.tsx, `fusionnerDistribution`,
   * D15) : leur compte s'ecrit en tete de la pastille « Cartes rencontre ».
   * Zero, le defaut, pour la table et le telephone, qui gardent ces etapes.
   */
  cartesDistribuees?: number
  /** Le texte de l'effet Boost ★ d'une carte, par son identifiant (D10). */
  texteEtoile?: (carteId: number) => string | undefined
  /** Les nombres que le monde publie sur une carte (`info` : stade, seuil). */
  infoCarte?: (id: number) => Partial<Record<string, number>> | undefined
  /** Ce que le catalogue sait d'une carte revelee : son Renfort, son texte imprime. */
  infoRevelee?: (carteId: number) => InfoRevelee | undefined
  /**
   * La question du moteur, STRUCTUREE, pour le cartouche du bas (scene PC,
   * lot 4 de la refonte) : la defense et le choix d'une carte revelee dans la
   * rangee, le reste dans le sous-cadre. La table et le telephone l'ignorent
   * et gardent `question`, rendue par le plateau.
   */
  questionDuMoteur?: QuestionDuMoteur
  /**
   * La question d'un AUTRE siege, en lecture seule (D28) : le cartouche du
   * bas montre ses cartes grisees et « X choisit… », sans un bouton.
   */
  questionDUnAutre?: CartouchePhaseProps['questionDUnAutre']
  /**
   * L'accuse de reception : il autorise le moteur a poursuivre son rendu
   * (board.tsx le branche sur `avancerMaintenant`).
   *
   * Il ne part PLUS a chaque etape validee. Il part quand le cartouche n'a
   * plus rien a montrer, c'est-a-dire quand le joueur a valide tout ce que le
   * cartouche sait deja (voir `cartoucheAJour` plus bas). Optionnel pour ne pas
   * casser les appelants qui ne pilotent pas le moteur (tests,
   * previsualisation).
   */
  onSuivant?: () => void
  /**
   * LE JOUEUR VIENT D'AGIR SUR LE CARTOUCHE (board.tsx :
   * `signalerActiviteDuJoueur`, moteur.ts), meme quand cela ne relache aucune
   * trame.
   *
   * Distinct de `onSuivant`, et il a fallu le separer : une seule trame retenue
   * peut porter DEUX etapes, le joueur clique alors « Suivant » pour passer de
   * l'une a l'autre, et ce clic-la n'acquitte rien puisque le cartouche n'est
   * pas encore a jour. Le filet anti-blocage, qui mesure une inactivite, ne
   * voyait donc rien de ces clics et doublait un joueur qui venait pourtant
   * d'agir (mesure en jeu, 07/09/2026 : clics a 60 s et 120 s, filet joue a
   * 151 s).
   *
   * Appele aussi par le minuteur qui passe seule, sur la table, l'etape d'un
   * autre joueur : il passe par la meme fonction. C'est sans consequence : il
   * acquitte des que le cartouche est a jour, donc le filet se desarme
   * aussitot apres.
   */
  onActivite?: () => void
  /**
   * L'etape que le cartouche montre (sa `cle`), pour que la table se cale sur
   * le recit (`table-calee.ts`, 04/10/2026). `undefined` quand il n'en montre
   * aucune.
   */
  onEtapeAffichee?: (cle: string | undefined) => void
  /**
   * REFONTE, LOT 4 (essai, decision 51) : vrai tant que l'etape affichee
   * retourne encore ses boosts, avant l'ecran du resultat. La table garde
   * alors le monde d'avant l'etape (PV et menace pas encore changes).
   */
  onAvantResultat?: (avant: boolean) => void
  /** Appele une fois la derniere etape validee. */
  onTerminer: () => void
  /**
   * Le joueur vient de valider l'etape qui porte la chute d'un heros
   * (« Continuer »). Il l'a donc VUE, et board.tsx peut enfin laisser paraitre
   * l'ecran de fin de partie, qui l'attendait (voir `afficherFinDePartie`).
   *
   * Distinct de `onTerminer`, qui part a la fin de CHAQUE phase du mechant :
   * s'en servir aurait declare le coup fatal vu des la premiere phase de la
   * partie, donc bien avant qu'il existe.
   */
  onDefaiteVue?: () => void
}) {
  // Refonte, lot 5b (essai) : la Riposte devient une étape à part (décision 39).
  // Lot 5c (essai) : l'effet ★ differe (decision 38) et l'elimination (45) ont aussi leur ecran.
  const etapes = useMemo(
    () =>
      essai
        ? avecEcranStadeRevele(avecEcranElimination(avecEtapesEtoileDifferee(avecEtapesRiposte(etapesRecues), texteEtoile)))
        : etapesRecues,
    [essai, etapesRecues, texteEtoile]
  )
  // LA CLE de l'etape que le joueur lit, jamais son numero. L'index se
  // retrouve a partir d'elle a chaque rendu (voir plus bas) : une etape qui
  // s'insere en amont ne fait donc plus reculer le joueur d'un cran, et
  // l'etape affichee ne change pas d'identite sous ses yeux (constat F3 de
  // l'audit du 06/09/2026).
  //
  // `undefined` veut dire « la premiere etape » : le cartouche n'a pas encore
  // d'etape a retenir tant que la liste est vide. Un effet plus bas adopte la
  // cle de la premiere etape des qu'elle existe, sans quoi une etape qui
  // s'insererait AVANT elle (une menace journalisee apres une activation)
  // changerait ce que le joueur lit.
  // Deux presentations, une seule mecanique (voir la prop `presentation`).
  // La scene du PC se dessine dans le cartouche du bas (CartouchePhase) ; la
  // scene du telephone garde le rendu d'avant (D36), SAUF pendant l'essai de la
  // « Nouvelle phase du méchant », qui y prend sa feuille basse
  // (cartouche-essai-tel.css). Declaree ICI, avant tout hook qui la lit
  // (`useGlisserPanneau`, plus bas).
  const nouvelleScene = presentation !== 'table' && (!telephone || essai)
  const surTable = presentation === 'table'
  const [cleCourante, setCleCourante] = useState<string>()
  // Vrai une fois la derniere etape validee : le cartouche doit alors
  // disparaitre de lui-meme. `onTerminer` relache desormais vraiment le
  // moteur (board.tsx), mais cela ne le fait pas disparaitre de l'ecran pour
  // autant : c'est toujours au composant de se masquer, plutot que de rester
  // affiche indefiniment sur la derniere etape, y compris pendant le tour du
  // joueur suivant.
  const [termine, setTermine] = useState(false)
  // Vrai quand le joueur a valide la derniere etape CONNUE alors que la phase
  // du mechant court encore : le moteur, relache par cette validation, est en
  // train de calculer la suite. Le cartouche reste alors affiche sur place et
  // n'annonce surtout pas la fin de la phase.
  const [enAttente, setEnAttente] = useState(false)
  // Vrai juste apres un « Precedent » : suspend l'avance auto jusqu'au
  // prochain « Suivant ». Sans cela, revenir en arriere ferait repartir
  // l'etape relue en avant aussitot, et le bouton serait inutilisable. Ce
  // motif a deja vecu dans ce fichier (enchainement des etapes techniques,
  // retire avec elles) : il revient pour la meme raison.
  const [suspendu, setSuspendu] = useState(false)
  // La derniere etape que le joueur a VALIDEE, et l'ETAT dans lequel il l'a
  // validee. Les deux comptent, et c'est tout le sujet de la reprise : une
  // activation s'annonce d'abord (`etat: 'annonce'`) puis se resout, et le
  // fait resolu REMPLACE l'intention sous la meme cle, sans allonger la liste.
  // Une etape validee en `annonce` n'est donc PAS validee en `resolu` : c'est
  // le meme numero d'etape, mais ce n'est plus la meme chose a lire.
  //
  // Mesure en partie reelle (Bishop contre Ultron, mode Detaille) : sans
  // l'etat, un clic donne pendant la fenetre d'annonce laissait le cartouche
  // « a jour » pour toutes les trames suivantes, et le journal a saute de 192 a
  // 262 en deux secondes — deux activations de sbires, la distribution et la
  // revelation resolues sans qu'aucune etape n'ait ete validee.
  const [validee, setValidee] = useState<{
    cle: string
    etat?: EtapeDeroule['etat']
    temps?: EtapeDeroule['temps']
    titre?: EtapeDeroule['titre']
    cibleId?: number
  }>()
  // LA RELECTURE d'un onglet passe (decision du 03/10/2026) : lecture seule,
  // « Revenir à l'étape en cours ». `cle` designe le coup dont on lit le
  // detail quand l'onglet en compte plusieurs. Rien ne part au moteur.
  const [relecture, setRelecture] = useState<{ temps: CleOnglet; cle?: string }>()

  // La derniere trame pour laquelle un accuse de reception est parti. C'est LA
  // garde contre la rafale d'accuses : l'etat du cartouche se recalcule
  // plusieurs fois pour une meme trame (chaque publication du moteur redessine
  // le plateau), et sans cette memoire l'effet ci-dessous relacherait le moteur
  // autant de fois. Un `ref` et non un `useState` : le retenir ne doit
  // provoquer aucun rendu, sans quoi la garde se declencherait elle-meme.
  const derniereTrameAcquittee = useRef<number | undefined>(undefined)

  // LA PHASE QUE LE CARTOUCHE RACONTE, et le seul declencheur de sa remise a
  // zero. Ce n'est pas `identitePhase` telle qu'elle arrive : board.tsx y passe
  // le round du monde, et le moteur incremente ce round au moment MEME ou il
  // quitte la phase du mechant. Suivre `identitePhase` sans filtre effacerait
  // donc le cartouche a la seconde ou il a enfin son bilan a montrer.
  //
  // Elle ne change que dans deux cas : une NOUVELLE phase du mechant s'ouvre
  // (une autre identite arrive alors que la phase du mechant court), ou le
  // cartouche a deja rendu la main (`termine`) et n'a donc plus rien a
  // raconter. Entre les deux, il finit de raconter la sienne, bilan compris.
  //
  // Un `ref` et non un `useState` : la remise a zero doit avoir lieu dans le
  // MEME passage d'effets que le rendu qui l'a decidee. Un etat aurait ajoute
  // un rendu, et l'accuse de reception (plus bas, sur ses propres dependances)
  // serait passe entre les deux sans repartir.
  const phaseRacontee = useRef(identitePhase)
  if (identitePhase !== phaseRacontee.current && (phaseMechantEnCours || termine)) {
    phaseRacontee.current = identitePhase
  }

  // Les dernieres etapes connues de la phase racontee. Voir plus bas pour la
  // raison : les faits du round disparaissent avant que le bilan ait pu etre
  // calcule.
  const memoireEtapes = useRef<EtapeDeroule[]>([])

  // UNE NOUVELLE PARTIE, elle, efface tout, sans condition.
  //
  // Les deux portes ci-dessus ne s'ouvrent ni l'une ni l'autre quand une
  // partie neuve commence sans rechargement de page (« Rejouer », ou un retour
  // au menu suivi d'une autre partie) : le monde revient au round 1 en plein
  // tour du joueur, donc `phaseMechantEnCours` est faux, et le cartouche n'a
  // jamais eu l'occasion de se dire `termine` puisque la partie finie l'avait
  // masque (`partieFinie`). `phaseRacontee` restait alors collee sur le round
  // de la partie morte et `memoireEtapes` gardait ses etapes : le cartouche
  // reapparaissait avec le bilan perime (« Colossus a pris 6 degats »)
  // par-dessus la partie neuve, le temps d'un tour.
  //
  // La memoire est videe ICI, et pas seulement l'identite : deux parties
  // peuvent s'arreter et repartir au MEME round, et la remise a zero par
  // `cleDeLaPhase` ne jouerait alors pas.
  const partieRacontee = useRef(identitePartie)
  // LE MONDE ARRIVE APRES L'ETIQUETTE DE PARTIE, et cette garde vient de la
  // mesure en jeu : `partieId` est publie des la reception de la trame (le
  // socket, `oublierSiNouvellePartie`), le monde a la fin de la lecture qui
  // suit. Il y a donc au moins un rendu ou la partie est NEUVE et le monde
  // encore celui d'avant. Sans cela, la memoire se remplissait a nouveau des
  // etapes de la partie morte juste apres avoir ete videe, et le cartouche les
  // affichait par-dessus la partie neuve : « The Break-In! gagne 1 menace 3/7 »
  // avec son bouton « Suivant », en plein tour du joueur d'une autre partie.
  //
  // On attend donc que le monde ait RATTRAPE l'etiquette, ce qui se reconnait
  // a une liste d'etapes vide : une partie neuve commence a sa mise en place,
  // sans aucun fait de phase du mechant.
  //
  // GARDE-FOU : cette attente ne se repose pas deux fois de suite. Tant qu'elle
  // court, le cartouche est MUET (`etapesDeCettePartie` est vide, plus bas), et
  // rien ne la releve qu'une liste d'etapes vide. Si cette liste ne venait
  // jamais, une deuxieme partie neuve la reposerait et le cartouche resterait
  // muet pour le reste de la session. On la laisse donc tomber a la deuxieme
  // bascule : une partie entiere a passe, le monde d'avant est loin.
  //
  // L'autre relachement possible (« une phase du mechant s'ouvre ») a ete
  // ECARTE : le monde perime peut lui-meme etre dans une phase du mechant, une
  // partie se terminant souvent sur le coup fatal, et la garde tomberait alors
  // au premier rendu, c'est-a-dire sans rien garder du tout.
  const mondeDeLaPartiePrecedente = useRef(false)
  if (identitePartie !== partieRacontee.current) {
    partieRacontee.current = identitePartie
    phaseRacontee.current = identitePhase
    memoireEtapes.current = []
    mondeDeLaPartiePrecedente.current = !mondeDeLaPartiePrecedente.current
  }
  if (mondeDeLaPartiePrecedente.current && etapes.length === 0) {
    mondeDeLaPartiePrecedente.current = false
  }

  const etapesDeCettePartie = mondeDeLaPartiePrecedente.current ? [] : etapes

  // UN UNDO, lui, ramene le monde EN ARRIERE : un round plus bas, ou le meme
  // round mais sans plus aucun fait a raconter et hors phase du mechant. La
  // fin ORDINAIRE d'une phase, elle, a toujours un round de plus (le moteur
  // l'incremente dans la meme foulee). Sans cette garde, la memoire gardait la
  // phase annulee et le bilan la remontrait en plein tour du joueur
  // (signalement 42). La sentinelle -1 force la remise a zero plus bas ; la
  // phase suivante rouvre normalement, puisqu'elle differe de toute identite.
  if (
    memoireEtapes.current.length > 0 &&
    ((identitePhase !== undefined &&
      phaseRacontee.current !== undefined &&
      identitePhase < phaseRacontee.current) ||
      (identitePhase === phaseRacontee.current && !phaseMechantEnCours && etapesDeCettePartie.length === 0))
  ) {
    memoireEtapes.current = []
    phaseRacontee.current = -1
  }

  const cleDeLaPhase = phaseRacontee.current

  // Une nouvelle phase repart de sa premiere etape, et RIEN D'AUTRE ne remet
  // le cartouche a zero. La remise a zero suivait auparavant le contenu de la
  // liste d'etapes : depuis que chaque validation relache une trame du moteur,
  // cette liste s'allonge PENDANT la phase, et le cartouche repartait donc de
  // la premiere etape a chaque nouvelle activation. Le joueur relisait en
  // boucle des etapes deja validees.
  //
  // `termine` doit se reinitialiser ICI, pas seulement `index` : sinon le
  // cartouche ne reapparaitrait plus jamais a la phase du mechant suivante, ce
  // qui est le piege symetrique et pire que le defaut d'origine.
  //
  // La derniere trame acquittee est oubliee ICI aussi : les `render_id` du
  // moteur repartent de zero avec une nouvelle partie, et un numero deja vu
  // ferait sauter l'accuse de la trame homonyme, donc gelerait la phase
  // jusqu'au filet anti-blocage.
  //
  // `suspendu` aussi : un « Precedent » sur la phase precedente le met a vrai,
  // et si elle se termine autrement qu'en revalidant jusqu'au bout, rien
  // d'autre ne le redescend. La premiere etape de la phase suivante
  // n'avancerait alors plus toute seule.
  useEffect(() => {
    setCleCourante(undefined)
    setTermine(false)
    setEnAttente(false)
    setSuspendu(false)
    setValidee(undefined)
    setRelecture(undefined)
    derniereTrameAcquittee.current = undefined
    memoireEtapes.current = []
    // `identitePartie` autant que la phase : deux parties peuvent s'arreter et
    // repartir au meme round, et le cartouche doit repartir de zero dans les
    // deux cas.
  }, [cleDeLaPhase, identitePartie])

  // Les etapes de la phase RACONTEE, memorisees.
  //
  // (Depuis le 07/10/2026 le moteur RETIENT la trame « End Phase » : le Bilan
  // la lit, round inchange, jusqu'a « Terminer » (moteur.ts, `decisionAccuse`).
  // Cette memoire reste le filet des cas ou cette trame ne vient pas : mode
  // « d'un coup », rechargement de page, filet des 90 s.)
  //
  // Le moteur quitte la phase du mechant et incremente le round dans la MEME
  // foulee : il ne retenait aucune trame entre les deux, donc le plateau ne
  // voyait jamais l'etat intermediaire « phase finie, round inchange ». Or les etapes
  // sont filtrees sur le round du monde (`etapesDeroule`, deroule-phase.ts) :
  // a la premiere trame d'apres, la liste retombe a zero. Sans cette memoire,
  // `avecBilan` n'a plus rien a compter et le bilan de fin de phase ne
  // s'affiche JAMAIS (constat 5 du rapport A3-fix, mesure en partie reelle).
  //
  // La memoire est ecrite pendant le rendu, comme `avancerRef` plus bas : elle
  // ne doit provoquer aucun rendu, elle suit celui qui a lieu.
  if (identitePhase === cleDeLaPhase && etapesDeCettePartie.length > 0) {
    memoireEtapes.current = etapesDeCettePartie
  }
  const etapesDeLaPhase =
    identitePhase === cleDeLaPhase && etapesDeCettePartie.length > 0
      ? etapesDeCettePartie
      : memoireEtapes.current

  // La phase RACONTEE court-elle encore ? `phaseMechantEnCours` seul ne suffit
  // plus : la phase du mechant du round suivant peut s'ouvrir avant que le
  // joueur ait valide le bilan de la precedente, et le cartouche raconte
  // encore celle-la jusqu'a ce que la remise a zero ci-dessus ait joue.
  const phaseRaconteeEnCours = phaseMechantEnCours && identitePhase === cleDeLaPhase

  // Les etapes REELLEMENT parcourues : celles du moteur, plus le bilan de fin
  // de phase quand la phase est finie.
  //
  // `phaseRaconteeEnCours` est la seule chose qui distingue proprement une
  // phase en cours d'une phase terminee (board.tsx calcule `phaseMechantEnCours`
  // sur `monde.phase`) : arriver au bout des etapes CONNUES ne dit rien,
  // puisque la liste s'allonge pendant la phase. Le bilan n'existe donc que
  // quand la phase est finie, et c'est ce qui en fait le terminateur naturel du
  // cartouche : il est toujours la derniere etape, et le valider, c'est finir.
  //
  // `arreterSurDefaite` vient EN DERNIER, et l'ordre tranche la question : un
  // heros tombe coupe le deroule a son etape, bilan compris. Le bilan de fin de
  // phase ne s'affiche donc jamais derriere une defaite.
  // Les TEMPS VIDES ont leur etape courte (« Aucune menace posée »), avec son
  // « Suivant » (decision du 03/10/2026) : `avecTempsVides`, frise-phase.ts.
  const etapesConnues = phaseRaconteeEnCours
    ? avecTempsVides(etapesDeLaPhase, false)
    : avecBilan(avecTempsVides(etapesDeLaPhase, true), pvMaxParNom)
  const etapesAffichees = arreterSurDefaite(etapesConnues, herosLocauxIds)
  // La coupe a-t-elle vraiment emporte quelque chose ? C'est ce qui distingue
  // « la liste a change d'ordre » de « un heros vient de tomber », et le repli
  // ci-dessous n'est pas le meme dans les deux cas.
  const coupeParDefaite = etapesAffichees.length < etapesConnues.length

  // L'INDEX, retrouve a partir de la cle retenue, a chaque rendu.
  //
  // La cle est la seule chose que le cartouche garde d'un rendu a l'autre :
  // c'est ce qui le rend insensible a l'ordre de la liste. Une revelation de
  // plus pour un autre joueur retrie les etapes, une intention se complete en
  // place, un fait arrive en amont : rien de tout cela ne deplace le joueur.
  //
  // REPLI, quand la cle a disparu de la liste : la premiere etape NON VALIDEE.
  // Les etapes se valident dans l'ordre, donc c'est celle qui suit la derniere
  // validee.
  //
  // ET QUAND MEME LA VALIDEE A DISPARU, apres une coupe de defaite : la
  // DERNIERE etape, c'est-a-dire celle qui porte le coup fatal. C'est le seul
  // endroit du cartouche ou l'on saute en avant, et c'est voulu.
  // `arreterSurDefaite` coupe sur l'ORDRE DES TEMPS et non sur l'ordre
  // d'arrivee des faits : une activation journalisee sous « Reveal Encounter
  // Cards » (une attaque declenchee par la carte que l'on vient de reveler)
  // garde le temps `revelation` et reste DEVANT les etapes de revelation apres
  // le tri stable. La coupe emporte alors l'etape lue ET l'etape validee, et
  // un repli sur zero renvoyait le joueur a la MENACE, sans jamais lui montrer
  // le coup qui l'a tue, pendant que le filet de 20 s de l'ecran de fin
  // courait (relecture A4).
  //
  // Corriger l'ordre de la coupe elle-meme (couper sur le rang du fait dans
  // `faits_mechant` plutot que sur le temps) demanderait de faire voyager ce
  // rang jusqu'a l'etape, alors qu'il ne sert aujourd'hui qu'a fabriquer sa
  // cle. Le repli, lui, se lit et se teste ici, et il rend au joueur ce qu'il
  // doit voir : l'etape de la defaite.
  const spectateur = estSpectateur()
  const suiviDuJoueur = useSuiviDuJoueur(spectateur)
  const cleSuivie = suiviDuJoueur.cle
  const rangDeLaCle =
    cleCourante === undefined ? -1 : etapesAffichees.findIndex((e) => e.cle === cleCourante)
  const rangValidee =
    validee === undefined ? -1 : etapesAffichees.findIndex((e) => e.cle === validee.cle)
  // Un spectateur ne clique jamais : il montre l'etape que le joueur lit.
  const index =
    spectateur
      ? indexSpectateur(etapesAffichees.map((e) => e.cle), cleSuivie)
      : rangDeLaCle !== -1
      ? rangDeLaCle
      : rangValidee !== -1
        ? Math.min(rangValidee + 1, etapesAffichees.length - 1)
        : coupeParDefaite
          ? etapesAffichees.length - 1
          : 0

  const etape = etapesAffichees[index]
  const cleAffichee = etape?.cle
  // Referme (bilan valide), le cartouche publie une etape VIDE : c'est ce que
  // le spectateur et la relecture lisent pour le refermer au meme moment.
  useEffect(() => {
    onEtapeAffichee?.(termine ? undefined : cleAffichee)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- board.tsx passe un
    // setter d'etat, stable ; seule la cle decide.
  }, [cleAffichee, termine])

  // EST-CE NOTRE HEROS QUI EST TOMBE ? La chute d'un autre joueur se DIT (le
  // crane et « X est vaincu » restent), mais elle n'arrete rien ici : pas de
  // « La phase s'arrete ici. », pas de bouton « Continuer », pas d'ecran de fin
  // retenu. La phase continue, et ce joueur-ci a encore des coups a lire.
  const defaiteLocale = etape !== undefined && estDefaiteLocale(etape, herosLocauxIds)
  // LOT 5c (essai, decision 44) : une carte a Péril revelee par UN AUTRE joueur grise
  // nos cartes : on ne joue rien et on ne conseille pas pendant sa resolution.
  const perilDUnAutre = Boolean(
    essai &&
      etape?.titre === 'revelation' &&
      etape.joueur !== undefined &&
      etape.carteId !== undefined &&
      (infoRevelee?.(etape.carteId)?.texteImprime ?? []).some((ligne) => /\bp[ée]ril\b/i.test(ligne)) &&
      ![...(herosLocauxIds ?? [])].some((id) => (joueurDeCarte ?? joueurInconnu)(id) === etape.joueur)
  )
  useEffect(() => {
    document.documentElement.classList.toggle('essai-peril-autre', perilDUnAutre)
    return () => document.documentElement.classList.remove('essai-peril-autre')
  }, [perilDUnAutre])
  /**
   * LE COUP FATAL SE VOIT SUR LA TABLE AVANT SON PANNEAU.
   *
   * Choix de l'utilisateur parmi trois (14/09/2026) : « le panneau, mais apres
   * avoir vu le coup ». Le coup se joue d'abord comme n'importe quelle etape -
   * le trait, le nombre, les points de vie a zero - et le panneau n'arrive
   * qu'au clic suivant. On voit ce qui nous a tues.
   *
   * ⚠ SEULEMENT DANS LA PRESENTATION « table ». Le mode « Detaille » montre le
   * coup DANS son panneau, avec les cartes rejouees : il n'a rien a attendre.
   *
   * ⚠ REMIS A ZERO A CHAQUE ETAPE, sinon un second coup fatal (un autre heros,
   * une autre partie) sauterait directement au panneau.
   */
  const [coupFatalVuSurTable, setCoupFatalVuSurTable] = useState(false)
  const cleDuCoupFatal = useRef<string | undefined>(undefined)
  if (cleDuCoupFatal.current !== etape?.cle) {
    cleDuCoupFatal.current = etape?.cle
    if (coupFatalVuSurTable) setCoupFatalVuSurTable(false)
  }
  /**
   * CETTE ETAPE VISE-T-ELLE UN AUTRE JOUEUR ?
   *
   * Choix de l'utilisateur (14/09/2026) : « tout se joue sous tes yeux, mais tu
   * ne cliques que pour tes etapes ». Un coup porte a un autre heros se montre,
   * puis passe tout seul apres un temps de lecture ; c'est SON joueur qui donne
   * le rythme, et le moteur attend son accuse de reception de toute facon.
   *
   * ⚠ SEULEMENT SUR UNE IDENTITE D'UN AUTRE JOUEUR, jamais sur « une cible qui
   * n'est pas la mienne ». La manigance principale, un sbire, un allie ne sont
   * les heros de personne : les compter ici ferait defiler toute la phase.
   *
   * ⚠ ET L'ENSEMBLE EST VIDE EN SOLO ET EN HOT-SEAT. Cette regle ne peut donc
   * rien changer hors d'une vraie table a plusieurs machines.
   */
  const viseUnAutreJoueur =
    etape?.cibleId !== undefined && (herosDesAutresIds?.has(etape.cibleId) ?? false)

  /** Le coup fatal est joue sur la table, son panneau attend un clic. */
  const fatalAMontrerSurTable = surTable && defaiteLocale && !coupFatalVuSurTable

  // Adoption de la premiere cle. Tant que le cartouche n'en retient aucune, il
  // lit l'etape 0 : une etape qui s'insererait devant elle changerait alors ce
  // qu'il montre. Des que la liste existe, il retient donc la cle de ce qu'il
  // affiche. L'effet ne se declenche qu'une fois par phase (il se rendort
  // aussitot que la cle est posee) et la remise a zero ci-dessus le reveille.
  const premiereCle = etapesAffichees[0]?.cle
  useEffect(() => {
    if (cleCourante === undefined && premiereCle !== undefined) setCleCourante(premiereCle)
  }, [cleCourante, premiereCle])

  // La cle lue a disparu (une etape du journal remplacee par le fait du moteur,
  // sous une autre cle) : le cartouche reprend celle de ce qu'il affiche. Sans
  // cela il lisait toute la suite par repli, et le repli, combine a la sortie
  // d'attente, sautait une etape (capture du 07/10/2026, Rhino / Assaut).
  useEffect(() => {
    if (spectateur || cleCourante === undefined || rangDeLaCle !== -1 || cleAffichee === undefined) return
    setCleCourante(cleAffichee)
  }, [spectateur, cleCourante, rangDeLaCle, cleAffichee])

  // LES DEUX MESURES DU « PLUS RIEN A MONTRER », calculees ici parce que la
  // sortie d'attente comme l'accuse de reception s'y appuient.
  //
  //  - `surLaDerniereEtape` : rien de NEUF n'est arrive depuis. C'est une
  //    garde de fraicheur, et elle porte sur la liste entiere, pas sur l'etat
  //    de l'etape courante. Le fait resolu n'est journalise qu'a la toute fin
  //    de l'activation (cote moteur : apres les degats, les defaites, la
  //    riposte) : entre l'intention et lui, le moteur rend plusieurs trames,
  //    dont certaines fabriquent des etapes neuves (l'accomplissement de la
  //    manigance principale, par exemple). La premiere d'entre elles doit
  //    remettre le cartouche en retard ;
  //  - `etapeValidee` : le joueur a valide CETTE etape DANS CET ETAT. Une
  //    intention validee ne vaut pas validation de la resolution qui prend sa
  //    place sous la meme cle.
  const surLaDerniereEtape = etapesAffichees.length > 0 && index === etapesAffichees.length - 1
  // La MEME etape sous une autre cle compte aussi : la menace tiree du journal
  // est remplacee par le fait du moteur, et sans cela le joueur la validait
  // deux fois (capture du 07/10/2026).
  const memeEtapeRecle =
    etape !== undefined &&
    validee !== undefined &&
    rangValidee === -1 &&
    validee.temps === etape.temps &&
    validee.titre === etape.titre &&
    validee.cibleId === etape.cibleId
  const etapeValidee =
    etape !== undefined &&
    validee !== undefined &&
    (validee.cle === etape.cle || memeEtapeRecle) &&
    validee.etat === etape.etat

  /**
   * LE JETON DE MENACE PART AU CLIC, PAS A L'AFFICHAGE DE L'ETAPE.
   *
   * ⚠ DEMANDE EXPLICITE DE L'UTILISATEUR, 14/09/2026 : « j'ai envie que la
   * menace sur le trafic clandestin SE METTE QUAND JE FAIS SUIVANT ». Le jeton
   * partait dès que l'étape s'affichait, donc avant tout clic : le joueur
   * lisait la phrase pendant que le jeton avait déjà volé.
   *
   * Il est retenu ICI, et non lu sur l'étape courante, parce que le clic fait
   * aussitôt passer à l'étape suivante : lire `etape` au moment du vol
   * donnerait la suivante, ou rien du tout.
   */
  const [volMenace, setVolMenace] = useState<
    { cle: string; cibleId: number | undefined; montant: number | undefined } | undefined
  >(undefined)

  // LOT 6 (essai, multi) : un joueur qui ne donne pas le rythme ne valide rien
  // lui-meme ; son cartouche suit celui qui le donne (`suivreLeMeneur`, plus bas).
  const avanceBloqueeRef = useRef(false)
  const avanceSuivieRef = useRef(false)
  const avancer = () => {
    if (avanceBloqueeRef.current && !avanceSuivieRef.current) return
    // Hors phase du mechant, etapes est vide et il n'y a rien a avancer : une
    // touche pressee ne doit alors rien declencher.
    if (!etape) return
    // Partie finie : le cartouche n'est plus a l'ecran, sa touche Entree ne
    // doit pas continuer a relacher le moteur derriere l'ecran de fin.
    if (partieFinie) return
    // Le joueur est vivant, et le filet anti-blocage doit le savoir meme quand
    // ce clic n'acquitte rien (voir `onActivite`).
    onActivite?.()
    // Un « Suivant » (clic, clavier, ou le minuteur de l'avance auto lui-meme)
    // leve la suspension posee par « Precedent ».
    setSuspendu(false)
    // L'etape courante est validee, DANS L'ETAT OU ELLE EST AU MOMENT DU CLIC.
    // Une intention validee ici ne vaudra pas validation de la resolution qui
    // prendra sa place (voir `validee` et `cartoucheAJour`).
    setValidee({ cle: etape.cle, etat: etape.etat, temps: etape.temps, titre: etape.titre, cibleId: etape.cibleId })
    // Le jeton de menace s'envole MAINTENANT, sur l'étape que le joueur vient
    // de valider (voir `volMenace`). Les autres étapes n'en posent pas.
    if (etape.titre === 'menace' || etape.titre === 'manigance') {
      setVolMenace({ cle: etape.cle, cibleId: etape.cibleId, montant: etape.montant })
    }
    // Aucun accuse de reception ici, et c'est tout le sujet de cette reprise :
    // valider l'etape 1 sur 4 relachait le moteur, qui repartait produire la
    // suite pendant que le joueur lisait. L'accuse ne part que lorsque le
    // cartouche n'a plus rien a montrer (voir `cartoucheAJour` plus bas), ce
    // que le clic ci-dessous provoque en entrant en attente.
    //
    // Un heros est tombe : le deroule s'arrete la, et « Continuer » rend la
    // main tout de suite. Sans ce court-circuit, la validation aurait bascule
    // le cartouche en « La suite arrive… » tant que la phase du mechant court
    // encore (elle continue pour les autres joueurs), sur une suite que
    // `arreterSurDefaite` ne lui donnera jamais.
    if (defaiteLocale) {
      setTermine(true)
      // Dit AVANT de rendre la main : c'est ce clic-ci qui autorise l'ecran de
      // fin de partie a paraitre, et le joueur vient de voir le coup.
      onDefaiteVue?.()
      onTerminer()
      return
    }
    // Une etape suivante est deja connue : on y va.
    if (index + 1 < etapesAffichees.length) {
      setEnAttente(false)
      setCleCourante(etapesAffichees[index + 1].cle)
      return
    }
    // Bout des etapes CONNUES, mais la phase du mechant court encore : le
    // moteur vient d'etre relache et va produire la suite. On reste sur place
    // en attente, sans appeler `onTerminer` et sans masquer le cartouche.
    if (phaseRaconteeEnCours) {
      setEnAttente(true)
      return
    }
    // Bout des etapes ET phase terminee : la, c'est vraiment fini.
    setTermine(true)
    onTerminer()
  }

  // SUR LA TABLE, Suivant retourne d'abord le boost suivant (v3, Q11), puis
  // valide l'etape une fois tous ses boosts montres.
  const avancerSurTable = () => {
    if (etape && boostsMontres < etape.boosts.length) {
      onActivite?.()
      setBoostsMontres((n) => n + 1)
      return
    }
    avancer()
  }

  // « TOUT PASSER » SUR LA TABLE (v3, Q32) : Echap, puis confirmation dans la
  // bulle. Les etapes defilent seules jusqu'a la fin de la phase ; une question
  // du moteur arrete le defilement le temps d'y repondre.
  const [confirmerPasser, setConfirmerPasser] = useState(false)
  const [passerTout, setPasserTout] = useState(false)

  const reculer = () => {
    // Relire est un geste de joueur comme un autre : le filet anti-blocage
    // repart de zero (voir `onActivite`).
    onActivite?.()
    // Relire, c'est renoncer a l'attente en cours : sans cela, la sortie
    // d'attente ci-dessous repousserait aussitot le joueur en avant et
    // « Precedent » n'aurait aucun effet visible. La suite reste atteignable
    // au bouton « Suivant », comme apres tout « Precedent ».
    setEnAttente(false)
    setSuspendu(true)
    // Relire, c'est n'etre plus a jour : le moteur doit attendre de nouveau
    // qu'on revienne au bout. Sans cet oubli, « Precedent » relachait le
    // moteur pendant que le joueur relisait.
    setValidee(undefined)
    setCleCourante(etapesAffichees[index - 1]?.cle)
  }


  // La version la plus recente de `avancer`, pour l'horloge du cartouche
  // (plus bas : avance auto). `avancer` est recreee a
  // chaque rendu et lit `index`,
  // `etapesAffichees` et `phaseRaconteeEnCours` du rendu courant : un minuteur
  // qui la capturerait a l'armement jouerait, a l'echeance, sur un etat vieux
  // de tout le delai de lecture (une etape arrivee entre-temps, par exemple).
  // La ref donne au minuteur la fonction du DERNIER rendu, sans que l'identite
  // de `avancer` ait a figurer dans les dependances de l'effet, ce qui le
  // relancerait a chaque trame.
  const avancerRef = useRef(avancer)
  avancerRef.current = avancer

  // Sortie d'attente. Trois issues, et trois seulement :
  //  - une etape de plus arrive : on avance dessus TOUT SEUL. Le joueur a deja
  //    clique pour l'obtenir, il ne doit pas avoir a recliquer ;
  //  - l'etape sur laquelle on attend CHANGE sous les yeux du joueur : une
  //    intention qui se resout ne fait pas grandir la liste (le fait resolu
  //    remplace le fait d'intention sous la meme cle), donc la premiere issue
  //    ne se declenche jamais. Sans celle-ci, un clic donne sur l'intention
  //    laissait le joueur sur « La suite arrive… » par-dessus une resolution
  //    qu'il ne voyait pas, et il ne reprenait pied qu'a l'etape suivante ;
  //  - la phase du mechant se termine sans rien produire de plus : le
  //    cartouche ne doit pas rester affiche par-dessus le plateau pendant tout
  //    le tour du joueur.
  //
  // En pratique, la fin de la phase fait apparaitre le bilan, donc c'est la
  // PREMIERE issue qui joue : le joueur atterrit sur le bilan et le valide.
  // La seconde reste un filet, pour le cas ou la phase se terminerait sans
  // qu'aucune etape n'ait ete produite.
  useEffect(() => {
    if (!enAttente) return
    // Deja au-dela de l'etape validee (le repli y a conduit) : on y reste.
    if (rangValidee !== -1 && rangValidee < index) {
      setEnAttente(false)
      return
    }
    if (index + 1 < etapesAffichees.length) {
      setEnAttente(false)
      setCleCourante(etapesAffichees[index + 1].cle)
      return
    }
    // L'etape validee n'est plus celle qu'on avait validee : elle s'est
    // completee sur place. On sort de l'attente SANS bouger d'index, et le
    // joueur lit la resolution la ou il lisait l'intention.
    if (!etapeValidee) {
      setEnAttente(false)
      return
    }
    if (!phaseRaconteeEnCours) {
      setEnAttente(false)
      setTermine(true)
      onTerminer()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `onTerminer` est
    // recree a chaque rendu par board.tsx : en dependre relancerait cet effet
    // a chaque trame du moteur, donc appellerait `onTerminer` en boucle. Les
    // cinq dependances ci-dessous sont des primitifs et decrivent a elles
    // seules la sortie d'attente.
  }, [enAttente, index, rangValidee, etapesAffichees.length, etapeValidee, phaseRaconteeEnCours])

  // LE RYTHME DE LA PHASE, en une ligne : le cartouche est-il a jour ?
  //
  // « A jour » ne veut pas dire « le cartouche affiche sa derniere etape ». Il
  // veut dire « le joueur a valide tout ce que le cartouche sait deja ». Sans
  // cette nuance, le moteur repartirait pendant que le joueur lit.
  //
  // Les facons de n'avoir plus rien a montrer :
  //  - `termine` : le cartouche a rendu la main (bilan valide, ou heros tombe
  //    alors que la phase court encore pour les autres). Il ne montrera plus
  //    rien de cette phase, donc il ne doit plus retenir le moteur ;
  //  - `partieFinie` : il n'y a plus de suite du tout, et le cartouche s'est
  //    efface derriere l'ecran de fin. Le laisser retenir figerait la table ;
  //  - aucune etape : la trame n'a rien fabrique a lire, elle file ;
  //  - pose sur la DERNIERE etape connue (rien de neuf n'est arrive depuis) et
  //    cette etape est validee DANS SON ETAT COURANT ;
  //  - pose sur la derniere etape connue et c'est une ANNONCE sur laquelle le
  //    joueur ne peut rien : voir juste dessous.
  //
  // Les deux dernieres portent la meme garde de fraicheur, et c'est elle qui
  // manquait : `surLaDerniereEtape` redevient faux des qu'une etape NEUVE
  // arrive, y compris pendant la fenetre d'annonce, ou le moteur rend
  // plusieurs trames avant de journaliser sa resolution.
  //
  // DEUX TEMPS SEULEMENT QUAND ON PEUT VRAIMENT AGIR (decision 7 de la spec).
  // Une etape d'intention n'est pas une etape a valider : c'est la meme etape
  // que sa resolution, montree avant qu'elle se complete. Si on la faisait
  // acquitter comme les autres, le joueur cliquerait DEUX fois par activation
  // — une fois pour laisser le mechant frapper, une fois pour lire le
  // resultat — ce que la decision refuse expressement.
  //
  // On acquitte donc tout de suite : le moteur resout, le fait resolu remplace
  // le fait d'intention sous la meme cle, et l'etape se complete sur place
  // sans que le joueur ait rien a faire. Il n'aura qu'un clic a donner, sur
  // l'etape complete.
  //
  // MAIS L'ETAPE COMPLETE, ELLE, SE VALIDE. C'est la nuance qui manquait : une
  // etape validee en `annonce` ne compte pas comme validee en `resolu`, sans
  // quoi le premier clic donne pendant la fenetre d'annonce rendait le
  // cartouche a jour pour tout ce qui suivait.
  //
  // ET UNE QUESTION DU MOTEUR EST UNE RAISON D'ACQUITTER, jamais de retenir.
  //
  // C'est la SORTIE DU PIEGE nomme par la revue du correctif A3, et elle se
  // conçoit avant de se coder. Le signal « le moteur attend le joueur » couvre
  // desormais les questions posees pendant qu'une trame est retenue (la barre
  // du bas : « Defendre / Passer »). Deux choses arrivent alors ensemble : le
  // cartouche se REPLIE devant la question, donc il n'a plus de bouton
  // « Suivant », et l'ancien terme `!questionAuJoueur` — mort jusqu'ici parce
  // que `validationRequise` et `trameRetenue` etaient poses ensemble — aurait
  // repris vie et rendu `cartoucheAJour` faux. Plus personne n'aurait relache
  // la trame : blocage jusqu'au filet.
  //
  // Retenir pendant une question ne protege d'ailleurs RIEN. Ce n'est pas
  // l'accuse de reception qui garde l'annonce a l'ecran pendant la fenetre de
  // reponse, c'est le moteur : il ne produit rien de plus tant qu'on ne lui a
  // pas repondu (cote Python, `Render` puis `WaitSync` puis `GetInput`, a la
  // suite sur le meme fil ; c'est meme notre accuse qui lui permet d'ARRIVER a
  // sa question). Acquitter pendant une question ne coute donc aucun rythme, et
  // ferme le blocage par construction : cartouche replie implique cartouche a
  // jour, donc trame relachee.
  //
  // L'annonce, elle, garde sa raison d'acquitter toute seule (decision 7 : pas
  // de clic sur « va attaquer »), sans plus avoir a s'inquieter des questions.
  const etapeEstAnnonce = etape?.etat === 'annonce'
  // ⚠ LA REGLE VIT DANS `cartouche-a-jour.ts`, avec sa gate. C'est la seule qui
  // decide du rythme de toute la phase, et une erreur dedans ne se voit pas :
  // la phase defile toute seule, ou elle se fige. Elle est sortie d'ici le
  // 14/09/2026 apres que le defaut est revenu TROIS FOIS.
  const cartoucheAJour = cartoucheEstAJour({
    termine,
    partieFinie,
    sansEtape: etapesAffichees.length === 0,
    questionAuJoueur,
    surLaDerniereEtape,
    etapeValidee,
    etapeEstAnnonce,
    surTable,
  })

  // L'accuse de reception, seul endroit d'ou il part.
  //
  // Deux chemins y menent, et les deux sont necessaires :
  //  - le clic qui epuise les etapes connues : il met `enAttente`, donc rend le
  //    cartouche a jour, donc relance cet effet ;
  //  - l'arrivee d'une trame qui ne fabrique AUCUNE etape alors que le
  //    cartouche etait deja a jour : `trameRetenue` change, l'effet repart.
  //    Sans ce second chemin, la phase se figerait sur le premier
  //    micro-evenement muet.
  //
  // La garde contre la rafale est l'IDENTITE de la trame, pas un booleen : une
  // trame deja acquittee ne peut pas l'etre une seconde fois, quel que soit le
  // nombre de fois ou l'etat se recalcule pendant qu'elle est retenue.
  useEffect(() => {
    if (trameRetenue === undefined) return
    if (!cartoucheAJour) return
    if (derniereTrameAcquittee.current === trameRetenue) return
    derniereTrameAcquittee.current = trameRetenue
    onSuivant?.()
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `onSuivant` est
    // recree a chaque rendu par board.tsx : en dependre relancerait cet effet
    // a chaque trame du moteur. Les deux dependances ci-dessous sont des
    // primitifs et decrivent a elles seules la decision d'acquitter.
  }, [trameRetenue, cartoucheAJour])

  useEffect(() => {
    const auClavier = (evenement: KeyboardEvent) => {
      // On ecrit peut-etre ailleurs : le tchat est a portee de main pendant la
      // phase, et un espace tape dedans ne doit pas la faire avancer.
      const cible = evenement.target
      if (
        cible instanceof HTMLElement &&
        (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)
      ) {
        return
      }
      // TAB SUR LA TABLE (v3, Q48) : d'une carte allumee (cliquable) a la
      // suivante, pour choisir un defenseur ou une reponse sans souris.
      if (surTable && questionAuJoueur && evenement.key === 'Tab') {
        const allumees = [
          ...document.querySelectorAll<HTMLElement>('.plateau-cadre .scan-card.est-agissante'),
        ]
        if (allumees.length > 0) {
          evenement.preventDefault()
          const ici = allumees.indexOf(document.activeElement as HTMLElement)
          const pas = evenement.shiftKey ? -1 : 1
          allumees[(ici + pas + allumees.length) % allumees.length]?.focus()
          return
        }
      }
      // On ne confisque pas Entree/Espace a un bouton du PLATEAU : seul un
      // element interactif EXTERIEUR au cartouche doit garder son activation
      // au clavier normale. Un bouton du cartouche lui-meme (Suivant,
      // Precedent) reste pris en charge ici, comme avant.
      if (
        cible instanceof HTMLElement &&
        cible.closest('button, a, select, [role="button"]') &&
        !cible.closest('.deroule-phase')
      ) {
        return
      }
      // Une question du moteur est posee : Entree et Espace lui appartiennent
      // et ne valident rien ici. Dans le cartouche du bas (scene PC, D37), les
      // chiffres 1 a 9 cliquent le choix qui porte ce numero et Echap le refus,
      // sauf si une fenetre ouverte par-dessus garde la touche (volet du
      // journal, reglages, confirmation, menu d'une carte). Les deux gardes
      // ci-dessus passent AVANT : elles valent aussi pour ces touches.
      if (questionAuJoueur) {
        if (nouvelleScene && !clavierBloque(document)) {
          const vise = cibleDeLaTouche(evenement.key, document.querySelector('.deroule-phase.est-scene'))
          if (vise) {
            evenement.preventDefault()
            vise.click()
          }
        }
        return
      }
      if (evenement.key === 'Enter' || evenement.key === ' ') {
        evenement.preventDefault()
        // En relecture, Entree ramene a l'etape en cours, et ne valide RIEN :
        // l'etape en cours n'est meme pas a l'ecran.
        if (relecture) {
          setRelecture(undefined)
          return
        }
        // Le cartouche du bas a encore une page a montrer pour cette etape
        // (D41) : la touche la tourne, comme son bouton, sans rien valider.
        const page = nouvelleScene ? boutonPageSuivante(document.querySelector('.deroule-phase.est-scene')) : undefined
        if (page) {
          page.click()
          return
        }
        if (surTable) avancerSurTable()
        else avancer()
        return
      }
      if (surTable && evenement.key === 'ArrowLeft' && !relecture && index > 0) {
        evenement.preventDefault()
        reculer()
        return
      }
      if (surTable && evenement.key === 'Escape' && !clavierBloque(document)) {
        evenement.preventDefault()
        setConfirmerPasser((ouvert) => !ouvert)
      }
    }
    document.addEventListener('keydown', auClavier)
    return () => document.removeEventListener('keydown', auClavier)
  })

  useEffect(() => {
    setPasserTout(false)
    setConfirmerPasser(false)
  }, [cleDeLaPhase])
  useEffect(() => {
    if (!passerTout || !surTable || !etape || questionAuJoueur || enAttente || termine) return
    const minuteur = window.setTimeout(() => {
      setBoostsMontres(etape.boosts.length)
      avancer()
    }, 0)
    return () => window.clearTimeout(minuteur)
    // `avancer` change a chaque rendu : la cle de l'etape pilote le defilement.
  }, [passerTout, surTable, etape?.cle, questionAuJoueur, enAttente, termine])

  // Combien de boosts sont deja retournes sur l'etape courante. Ils
  // s'enchainent SEULS : c'est l'etape qui attend la validation, pas chaque
  // carte. Une attaque a trois boosts couterait sinon quatre clics.
  const [boostsMontres, setBoostsMontres] = useState(0)
  // 13/10/2026 (encadré ⑫) : les cartes révélées déjà retournées, par clé d'étape.
  const [cartesRetournees, setCartesRetournees] = useState<ReadonlySet<string>>(() => new Set())
  // 13/10/2026 (encadré ①) : les pastilles des joueurs dans le calcul de menace.
  const couleursDesJoueurs = useMemo(() => (essai && cadresJoueurs ? cadresJoueurs.map((c) => c.couleurs[0]) : undefined), [essai, cadresJoueurs])
  const avantResultat = Boolean(essai && etape && etape.boosts.length > 0 && boostsMontres < etape.boosts.length)
  useEffect(() => {
    onAvantResultat?.(avantResultat)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- setter d'etat stable
  }, [avantResultat])

  // LA LOUPE : la carte de la scene survolee, ouverte en grand a cote avec
  // son texte, comme une carte de la table (CarteApercu). Decide avec
  // l'utilisateur : « pour lire vraiment une carte rencontre ».
  //
  // ⚠ ELLE RESTAIT OUVERTE SUR UNE CARTE DISPARUE (capture de l'utilisateur,
  // le 10 septembre 2026 : un sbire d'une etape precedente montre en grand
  // par-dessus le bouton « Suivant », curseur loin de toute carte). Le survol
  // etait pose sur CHAQUE `figure`, et `mouseleave` n'est jamais emis quand
  // l'element disparait sous le pointeur. Une remise a zero sur `etape.cle` ne
  // suffisait pas : les boosts s'ajoutent A L'INTERIEUR d'une meme etape
  // (`boostsMontres`), la scene change donc sans changer de cle.
  //
  // La regle commune est dans `apercu-survol.ts` : un seul ecouteur sur le
  // conteneur, et la carte RETROUVEE a chaque rendu dans la liste visible.
  // `cartesVisibles` reproduit le filtre du rendu (`gauche` et `droite` plus
  // bas) : un boost pas encore montre n'est pas survolable, il ne doit donc
  // pas non plus etre agrandissable.
  // Le meme calcul sert au rendu ET a la loupe : elle doit montrer EXACTEMENT
  // la carte dessinee, face forcee comprise. C'est aussi lui qui donne
  // l'identifiant que `ScanCard` pose en `data-card-id` : une carte de scene
  // porte un id NUMERIQUE du moteur, pas celui de la carte dessinee, et le role
  // « dos » n'en a aucun.
  const propsDe = (carte: CarteDeScene) =>
    carte.role === 'dos'
      ? dosRencontre
      : carteScene?.(carte.id, carte.role === 'revelee' || carte.role === 'boost')

  const cartesVisibles = useMemo(() => {
    if (!etape) return []
    const montres = new Set(etape.boosts.slice(0, boostsMontres).map((boost) => boost.cibleId))
    return sceneDe(etape).cartes.filter(
      (carte) => carte.role !== 'boost' || montres.has(carte.id)
    )
  }, [etape, boostsMontres])
  const {
    regardee: carteDeSceneRegardee,
    survol: survolerScene,
    quitter: quitterScene,
    viser: viserScene,
  } = useApercuSurvol(cartesVisibles, (carte) => propsDe(carte)?.id)

  useEffect(() => {
    // Essai (13/10/2026, demande de l'utilisateur) : les boosts arrivent TOUS face
    // cachee, et un seul clic les retourne ensemble (« comme pour Klaw, j'aimerais
    // que les deux s'affichent en même temps »).
    setBoostsMontres(etape?.boosts.length ? (essai && nouvelleScene ? 0 : 1) : 0)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `etape` est
    // reconstruit a chaque trame du moteur (meme piege que dans
    // useDerouleScene.ts et TraitCible.tsx) : en dependre remettrait
    // `boostsMontres` a 1 en boucle et aucun boost ne s'enchainerait jamais. `etape?.cle` identifie l'etape, et
    // `etape?.boosts.length` reagit si son compte de boosts change.
  }, [etape?.cle, etape?.boosts.length])

  useEffect(() => {
    const total = etape?.boosts.length ?? 0
    if (boostsMontres === 0 || boostsMontres >= total) return
    // L'essai les retourne au clic (« Continuer »), un par un ; la table aussi
    // (v3, Q11 : « retourner un boost par clic »).
    if ((essai && nouvelleScene) || surTable) return
    const minuteur = window.setTimeout(
      () => setBoostsMontres((n) => n + 1),
      DELAI_BOOST_MS
    )
    return () => window.clearTimeout(minuteur)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- meme raison :
    // `etape?.cle` et `etape?.boosts.length` suffisent a piloter le
    // minuteur, l'identite de `etape` ne doit pas le redeclencher.
  }, [boostsMontres, etape?.cle, etape?.boosts.length, essai, nouvelleScene, surTable])

  // LOT 6 (essai, MULTI, decisions 10, 32, 33). Seulement a une vraie table a
  // plusieurs machines (`herosDesAutresIds` est vide en solo et en hot-seat) :
  // le solo et le hot-seat ne changent pas.
  const multi = Boolean(essai && !spectateur && (herosDesAutresIds?.size ?? 0) > 0)
  const avanceMulti = useAvanceMulti(multi)
  const politique: PolitiqueAvance | undefined = multi ? avanceMulti.politique : undefined
  const cadreMulti = multi && cadresJoueurs && etape ? cadreDeLEtape(etape, cadresJoueurs, joueurDeCarte ?? joueurInconnu) : undefined
  const siegeConcerne = cadreMulti?.genre === 'joueur' ? cadreMulti.joueur : undefined
  const meneur = siegeMeneur(siegeConcerne, premierJoueur)
  const siegesTable = (cadresJoueurs ?? []).map((_, rang) => rang)
  // Avant le choix de l'hote, personne n'avance ; en « tous », on se dit pret
  // au lieu d'avancer ; en « concerne », seul le meneur avance.
  const avanceBloquee =
    multi && (!avanceMulti.charge || politique === undefined || politique === 'tous' || !peutAvancer(politique, siegeLocal, siegeConcerne, premierJoueur))
  avanceBloqueeRef.current = avanceBloquee
  const suivreLeMeneur = () => {
    avanceSuivieRef.current = true
    try {
      avancerRef.current()
    } finally {
      avanceSuivieRef.current = false
    }
  }
  // Ce que nous lisons, publie pour les autres : les boosts deja retournes.
  useEffect(() => {
    if (multi) publierExtrasEtape({ boosts: boostsMontres })
  }, [multi, boostsMontres, etape?.cle])
  // Et l'etape que nous venons de valider : celui qui nous suit la valide aussi,
  // sans quoi le moteur attendrait son accuse de reception a jamais.
  useEffect(() => {
    if (multi) publierExtrasEtape({ valide: validee?.cle ?? '' })
  }, [multi, validee?.cle])
  // On suit le meneur (« concerne ») ou le dernier qui a clique (« quiconque ») :
  // une etape d'avance, un clic simule a la fois ; ses boosts ; la fermeture du bilan.
  const lectureSuivie = multi ? lectureASuivre(politique, avanceMulti.etapes, siegeLocal, meneur) : undefined
  const rangSuivi = lectureSuivie?.cle ? etapesAffichees.findIndex((e) => e.cle === lectureSuivie.cle) : -1
  useEffect(() => {
    if (!multi || !lectureSuivie || questionAuJoueur || termine || !etape) return
    if (rangSuivi > index) {
      suivreLeMeneur()
      return
    }
    if (rangSuivi === index && lectureSuivie.boosts > boostsMontres) {
      setBoostsMontres(Math.min(lectureSuivie.boosts, etape.boosts.length))
      return
    }
    // Le meneur a valide l'etape que nous montrons : nous la validons aussi
    // (nous passons en attente de la suite, et notre accuse part).
    if (rangSuivi === index && lectureSuivie.valide === etape.cle && validee?.cle !== etape.cle) {
      suivreLeMeneur()
      return
    }
    if (lectureSuivie.cle === '' && etape.temps === 'bilan') suivreLeMeneur()
    // eslint-disable-next-line react-hooks/exhaustive-deps -- la lecture suivie (cle, boosts, heure) pilote
  }, [multi, lectureSuivie?.cle, lectureSuivie?.boosts, lectureSuivie?.valide, lectureSuivie?.t, rangSuivi, index, boostsMontres, questionAuJoueur, termine, etape?.cle, validee?.cle])
  // « Tout le monde valide » : on avance ensemble quand chaque siege est pret.
  const prets = multi && politique === 'tous' ? siegesPrets(avanceMulti.etapes, etape?.cle, siegesTable) : []
  const tousSontPrets = multi && politique === 'tous' && tousPrets(avanceMulti.etapes, etape?.cle, siegesTable)
  useEffect(() => {
    if (!tousSontPrets || questionAuJoueur || termine) return
    suivreLeMeneur()
    // eslint-disable-next-line react-hooks/exhaustive-deps -- la cle de l'etape et l'accord pilotent
  }, [tousSontPrets, etape?.cle, questionAuJoueur, termine])
  const nomDuSiege = (siege: number | undefined): string =>
    siege === undefined
      ? '?'
      : nomsJoueurs?.[siege]
        ? `J${siege + 1} (${nomsJoueurs[siege]})`
        : `J${siege + 1}`
  const piedMulti: PiedMulti | undefined = !multi
    ? undefined
    : !avanceMulti.charge
      ? { genre: 'attente-choix' }
      : politique === undefined
        ? siegeLocal === 0
          ? { genre: 'choix-hote', choisir: (choix) => void choisirPolitique(0, choix) }
          : { genre: 'attente-choix' }
        : politique === 'tous'
          ? {
              genre: 'pret',
              pret: siegeLocal !== undefined && prets.includes(siegeLocal),
              pastilles: siegesTable.map((siege) => ({
                nom: nomDuSiege(siege),
                couleur: cadresJoueurs?.[siege]?.couleurs[0],
                pret: prets.includes(siege),
              })),
              marquer: () => {
                if (etape) publierExtrasEtape({ pret: etape.cle })
              },
            }
          : avanceBloquee
            ? { genre: 'regarde', nom: nomDuSiege(meneur) }
            : undefined

  // Le cartouche est-il a l'ecran ? Calcule ICI parce que les hooks ci-dessous
  // en dependent, et que la sortie `return null` qui l'applique vient bien plus
  // bas : un hook place apres elle ferait tomber tout le plateau.
  const visible = Boolean(etape) && !termine && !partieFinie

  // Les etapes qui attendent un VRAI clic, meme celles d'un autre joueur : le bilan de
  // fin de phase (le joueur reprend la main, il doit le voir) et la chute
  // d'un heros (le moment le plus important d'une partie ne defile pas). Le
  // bilan se reconnait a son temps : `avecBilan` est le seul a le produire.
  const etapeAttendUnClic = etape?.temps === 'bilan' || Boolean(etape?.defaite)

  // Le delai avant que l'etape courante ne se valide seule, ou `undefined`
  // quand elle attend un clic.
  // ⚠ UNE ETAPE QUI VISE UN AUTRE JOUEUR PASSE TOUTE SEULE, le temps de la
  // lire. Voir `viseUnAutreJoueur` : elle se montre, mais elle ne demande pas
  // NOTRE clic, le temps de voir le coup.
  // L'avance auto est retiree (pas a pas strict, 03/10/2026) : ce minuteur ne
  // sert plus qu'a cela.
  const delaiAvant = surTable && viseUnAutreJoueur ? DELAI_ETAPE_D_UN_AUTRE_MS : undefined

  // L'HORLOGE du cartouche, la seule de toute la phase. Elle passe seule, sur
  // la table, l'etape qui vise un autre joueur (delai de lecture).
  //
  // Un minuteur par etape affichee, nettoye au demontage et a chaque
  // changement d'etape (c'est `etape?.cle` dans les dependances qui le
  // re-arme, pas l'objet `etape`, reconstruit a chaque trame du moteur : en
  // dependre remettrait le minuteur a zero plus vite qu'il n'arrive a
  // echeance, et rien n'avancerait jamais). Sans ce nettoyage, deux minuteurs
  // se superposeraient et une etape serait sautee.
  //
  // Aucun minuteur :
  //  - sur une etape qui ne vise pas un autre joueur, evidemment ;
  //  - hors ecran (`visible`) : rien a avancer ;
  //  - `suspendu` : le joueur relit, apres un « Precedent » ;
  //  - `enAttente` : le cartouche est au bout de ce qu'il sait et attend que
  //    le moteur produise la suite. Il n'y a rien a avancer, et la sortie
  //    d'attente affichera d'elle-meme l'etape qui arrive, ce qui re-armera
  //    le minuteur dessus ;
  //  - `questionAuJoueur` : le cartouche est replie devant la question du
  //    moteur, il n'a plus de bouton, donc plus d'horloge non plus ;
  //  - `etapeEstAnnonce` : l'etape n'a pas fini de se completer. La depasser
  //    ferait manquer au joueur le seul moment ou elle dit quelque chose,
  //    c'est-a-dire sa resolution. Elle se completera sur place (l'accuse est
  //    deja parti, voir `cartoucheAJour`) et le minuteur repartira alors ;
  //  - `etapeAttendUnClic` : voir ci-dessus.
  useEffect(() => {
    if (delaiAvant === undefined) return
    if (!visible || suspendu || enAttente || questionAuJoueur || etapeEstAnnonce) return
    if (etapeAttendUnClic) return
    const minuteur = window.setTimeout(() => avancerRef.current(), delaiAvant)
    return () => window.clearTimeout(minuteur)
  }, [
    delaiAvant,
    etape?.cle,
    etape?.etat,
    visible,
    suspendu,
    enAttente,
    questionAuJoueur,
    etapeEstAnnonce,
    etapeAttendUnClic,
  ])

  // LE COMPTE A REBOURS DU FILET, en secondes, ou `undefined` tant que
  // l'echeance est loin (ou qu'aucun filet n'est arme).
  //
  // Un battement par seconde, et seulement pendant que le cartouche est a
  // l'ecran : rien a compter derriere un ecran de fin de partie. La dependance
  // est l'echeance elle-meme, un NOMBRE : elle ne change qu'au (re)armement du
  // filet, donc le battement n'est pas remis a zero a chaque trame.
  const [secondesFilet, setSecondesFilet] = useState<number>()
  useEffect(() => {
    if (echeanceFilet === undefined || !visible) {
      setSecondesFilet(undefined)
      return
    }
    const calculer = () => {
      const reste = echeanceFilet - Date.now()
      if (reste > DELAI_ALERTE_FILET_MS) {
        setSecondesFilet(undefined)
        return
      }
      setSecondesFilet(Math.max(0, Math.ceil(reste / 1000)))
    }
    calculer()
    const battement = window.setInterval(calculer, 1000)
    return () => window.clearInterval(battement)
  }, [echeanceFilet, visible])

  // Mise en scene de l'etape courante. Appele ici, avec les autres hooks :
  // ce composant a un `return null` plus bas, et un hook place apres lui fait
  // tomber tout le plateau (React compte alors un hook de plus au rendu
  // suivant).
  // ⚠ AUCUN VOILE SUR LA TABLE. Le voile assombrit la table pendant qu'une
  // etape est a l'ecran : c'est juste, quand la scene CENTRALE rejoue les
  // cartes par-dessus (spec du 07/09/2026, « la table n'est plus a lire »).
  // Dans le mode « Sur la table », c'est exactement l'inverse : la table EST
  // le recit, et l'assombrir reviendrait a eteindre ce qu'on demande de
  // regarder. Constate a l'ecran des la premiere capture.
  // ⚠ LE CARTOUCHE DU BAS NON PLUS (refonte du 04/10/2026) : il ne rejoue
  // aucune carte par-dessus la table, il la laisse lisible au-dessus de lui.
  // Seul le telephone garde le voile.
  useDerouleScene(etape, visible && !surTable && telephone)
  // Les cartes en cause s'allument sur la table, sans mouvement (rapport
  // Yarro n46) : le recit est dans le cartouche, le regard trouve ses cartes.
  useSurbrillanceEtape(visible ? cartesConcernees(etape) : [])

  // ⚠ PLUS DE `body.deroule-question` (refonte du 04/10/2026). Il sortait la
  // main du voile pendant une question ; la scene du PC laisse desormais la
  // main visible pendant la phase, sans voile (revirement du 05/10/2026,
  // `main-visible.ts`) ; sa regle est partie de board.css (halo-main.test.ts).

  // Le `return null` vient APRES tous les hooks, jamais avant : React exige
  // le meme nombre de hooks, dans le meme ordre, a chaque rendu. Ce composant
  // est monte des que le mode "detaille" est actif, donc hors phase du
  // mechant avec `etapes` vide, puis se remplit sans etre demonte quand la
  // phase commence. Un `return null` place plus haut sauterait le second
  // useEffect a un rendu et le rajouterait au suivant, ce que React refuse.
  // `termine` fait disparaitre le cartouche une fois la phase VRAIMENT finie
  // (bout des etapes connues et phase du mechant terminee) ; il est remis a
  // false des que l'identite de phase change (voir le useEffect ci-dessus),
  // donc le deroule reapparait bien a la phase du mechant suivante.
  // `partieFinie` le fait disparaitre pour de bon : plus rien n'arrive apres.
  /* ================= LA PRESENTATION « SUR LA TABLE » =======================
     Le cartouche quitte le centre et vient se poser a cote de la carte qui
     vient d'agir. Choix de l'utilisateur du 14/09/2026 parmi trois
     emplacements : « l'oeil est deja la ».

     ⚠ RIEN DE LA MECANIQUE N'EST TOUCHE ICI. Tout ce qui suit est du placement. */
  const [elCartouche, setElCartouche] = useState<HTMLElement | null>(null)

  // ⚠ `etape`, PAS `etapeLue` : ce bloc doit vivre AVANT le premier `return`,
  // celui de la question posee avant toute etape (12/09/2026), qui rend lui
  // aussi un cartouche a placer. `etapeLue` n'est construite que plus bas.
  // ⚠ L'AUTEUR D'ABORD, LA CIBLE A DEFAUT. L'etape de menace n'a pas d'auteur :
  // c'est une regle du jeu qui pose la menace, et sa seule carte est la
  // manigance visee. Sans ce repli, le cartouche se posait au milieu du
  // plateau, par-dessus la main, loin de la carte dont il parlait. C'est le
  // meme choix que la scene centrale, qui « met alors la cible elle-meme en
  // avant, faute d'auteur » (deroule-phase.ts, `cibleId`).
  const place = useAncrageSurTable(
    etape?.carteId ?? etape?.cibleId,
    etape?.carteId === undefined ? undefined : etape?.cibleId,
    etape?.cle ?? 'sans-etape',
    surTable,
    elCartouche,
    // ⚠ LE BOUTON NE SUIT PLUS LA CARTE. Il se posait a cote de celle qui agit,
    // donc il CHANGEAIT DE PLACE a chaque etape : on ne le cherchait pas une
    // fois mais a chaque clic. « Il faut que le joueur puisse se retrouver
    // facilement » (utilisateur, 14/09/2026). Les panneaux qui restent (bilan,
    // coup fatal, question) parlent d'une carte precise et gardent leur ancrage.
    'centre'
  )
  const classeCartouche = (extra: string) =>
    `deroule-phase${extra ? ' ' + extra : ''}${surTable ? ' est-sur-table' : ''}`
  // ⚠ TANT QUE LA PLACE N'EST PAS CONNUE, LE CARTOUCHE RESTE INVISIBLE mais
  // MONTE : il faut qu'il soit dans le DOM pour etre mesure, et il ne faut pas
  // qu'il paraisse un instant en haut a gauche avant de sauter a sa place.
  const styleCartouche: CSSProperties | undefined = surTable
    ? place
      ? { left: `${place.x}px`, top: `${place.y}px` }
      : { visibility: 'hidden' }
    : undefined

  // Deplacement a la poignee du bandeau rouge, sur le cartouche de QUESTION
  // seulement (signalement Yarro, 30/09/2026 : la fenetre principale ne
  // bougeait pas, seule celle des cibles hors table). `translate` et non
  // `transform` : `.deroule-phase` se centre deja par `transform:
  // translateX(-50%)`, que la propriete `translate` compose sans l'ecraser.
  // Le cartouche des ETAPES garde sa place d'une etape a la suivante (signalement
  // Yarro, 01/10/2026 : « toujours pas moyen de bouger la fenetre des etapes
  // du mechant ») ; seule la question se repose a chaque etape.
  // ⚠ LE CARTOUCHE DU BAS revient en bas a la PHASE suivante, jamais d'une
  // etape a l'autre (D2) : sa signature est la phase racontee.
  // La boite de l'essai sur PC (12/10/2026, decision 28) : sa place choisie a
  // la main est retenue d'une phase et d'une partie a l'autre.
  const boiteEssai = essai && nouvelleScene && !telephone
  const { decalage: decalageQuestion, gestes: gestesQuestion } = useGlisserPanneau(
    boiteEssai
      ? 'scene-essai'
      : nouvelleScene
        ? `scene|${cleDeLaPhase}`
        : questionAuJoueur
          ? `question|${etape?.cle ?? 'sans-etape'}`
          : 'etapes',
    boiteEssai ? 'marvel-boite-phase-mechant' : undefined
  )
  const styleDeplace: CSSProperties | undefined =
    decalageQuestion.dx !== 0 || decalageQuestion.dy !== 0
      ? { ...styleCartouche, translate: `${decalageQuestion.dx}px ${decalageQuestion.dy}px` }
      : styleCartouche
  const gestesDeplacer = {
    onPointerDown: gestesQuestion.onPointerDown,
    onPointerMove: gestesQuestion.onPointerMove,
    onPointerUp: gestesQuestion.onPointerUp,
    onPointerCancel: gestesQuestion.onPointerCancel,
  }

  // LA BULLE « SUR LA TABLE » (v3, 10/10/2026) : fixe mais deplacable par sa
  // bande d'onglets. Signature constante : la place choisie tient d'une etape
  // et d'une phase a l'autre.
  const { decalage: decalageBulle, gestes: gestesBulle } = useGlisserPanneau('bulle-table')
  const styleBulle: CSSProperties | undefined =
    decalageBulle.dx !== 0 || decalageBulle.dy !== 0
      ? { ...styleCartouche, translate: `${decalageBulle.dx}px ${decalageBulle.dy}px` }
      : styleCartouche
  // LA FEUILLE DU TELEPHONE (v3, Q37 et Q38) : la bulle se colle en bas de
  // l'ecran ; un glissement vertical sur ses onglets passe de reduite a
  // normale a depliee, et retour.
  const [feuille, setFeuille] = useState<'reduite' | 'normale' | 'depliee'>('normale')
  const departFeuille = useRef<number | undefined>(undefined)
  const ORDRE_FEUILLE = ['reduite', 'normale', 'depliee'] as const
  const gestesFeuille = {
    onPointerDown: (e: ReactPointerEvent) => {
      departFeuille.current = e.clientY
    },
    onPointerMove: () => {},
    onPointerUp: (e: ReactPointerEvent) => {
      const depart = departFeuille.current
      departFeuille.current = undefined
      if (depart === undefined || Math.abs(e.clientY - depart) < 30) return
      const sens = e.clientY < depart ? 1 : -1
      setFeuille((h) => ORDRE_FEUILLE[Math.min(2, Math.max(0, ORDRE_FEUILLE.indexOf(h) + sens))])
    },
    onPointerCancel: () => {
      departFeuille.current = undefined
    },
  }
  const poignee = telephone ? gestesFeuille : gestesBulle
  const classeTelephone = telephone ? ` est-telephone est-${feuille}` : ''

  // L'AIDE (v3, Q47) : ouverte d'office la premiere fois, puis au bouton « ? ».
  const [aideTable, setAideTable] = useState(() => {
    try {
      return globalThis.localStorage?.getItem(CLE_AIDE_TABLE) !== 'vue'
    } catch {
      return false
    }
  })
  const fermerAideTable = () => {
    setAideTable(false)
    try {
      globalThis.localStorage?.setItem(CLE_AIDE_TABLE, 'vue')
    } catch {
      // Stockage indisponible : l'aide reviendra, sans autre gene.
    }
  }
  // Fantome au survol d'une carte de la table : elle ne cache plus ce qu'on
  // regarde, et les clics passent a travers jusqu'a la souris sortie des cartes.
  const [bulleFantome, setBulleFantome] = useState(false)
  useEffect(() => {
    if (!surTable) return
    const survol = (e: PointerEvent) => {
      const cible = e.target instanceof Element ? e.target : null
      setBulleFantome(Boolean(cible?.closest('.scan-card')) && !cible?.closest('.deroule-bulle-table'))
    }
    document.addEventListener('pointerover', survol)
    return () => {
      document.removeEventListener('pointerover', survol)
      setBulleFantome(false)
    }
  }, [surTable])

  /**
   * ⚠ SUR LA TABLE, LE CARTOUCHE VA DANS LE CADRE DU PLATEAU, par un portail.
   *
   * Les coordonnées calculées sont celles du CADRE (`.plateau-cadre`), mais ce
   * composant est monté ailleurs dans l'arbre : posées telles quelles, elles
   * décalaient tout de la hauteur de la barre d'outils. Mesuré à l'écran :
   * le cartouche se posait 48 px trop haut, au-dessus de la carte au lieu d'être
   * à côté d'elle.
   *
   * Un PORTAIL plutôt qu'un recalcul en coordonnées de page : l'état du
   * composant reste où il est (index de l’étape, minuteurs), seul
   * le nœud DOM déménage. Et le trait, qui couvre tout le cadre, a besoin du
   * même repère.
   */
  const enveloppe = (contenu: ReactNode): ReactNode => {
    if (!surTable) return contenu
    const cadre = document.querySelector<HTMLElement>('.plateau-cadre')
    // Pas de cadre (premier rendu, jsdom) : on rend sur place. Le cartouche est
    // alors mal placé mais PRÉSENT, donc mesurable, et la mesure suivante le
    // remet où il faut. Le faire disparaître le rendrait impossible à mesurer.
    if (!cadre) return contenu
    return createPortal(
      <>
        {/* ⚠ LA LIGNE DES TEMPS MONTE DANS LA BARRE DU HAUT. Choix de
            l'utilisateur parmi trois (14/09/2026) : « oui, dans la barre du
            haut ». Elle vivait dans le panneau, qui a disparu ; la laisser au
            centre aurait remis un bloc de texte par-dessus la table.

            Un temps VIDE y est barre et marque « (Aucun) » : c'est deja le
            comportement de `chronologie`, et c'est exactement sa decision
            « on la saute, mais on le dit ». Il ne coute aucun clic, puisque
            `etapesDeroule` ne fabrique pas d'etape pour lui. */}
        <CoucheTraitPhase etape={etape} actif />
        <EffetsSurTable
          etape={etape}
          actif={!questionAuJoueur}
          pvMax={etape?.cibleNom ? pvMaxParNom?.get(etape.cibleNom) : undefined}
        />
        {/* Les cartes qui sortent du paquet rencontre : les boosts a cote du
            deck, puis la carte revelee en grand. Meme portail, meme repere. */}
        {/* Le jeton de menace, sur les etapes qui en posent (point 1, et une
            manigance du mechant). Ailleurs il ne rend rien. */}
        <JetonMenaceVolant
          cibleId={volMenace?.cibleId}
          montant={volMenace?.montant}
          cle={volMenace?.cle}
          actif={volMenace !== undefined}
        />
        <CoucheRencontreSurTable
          etape={etape}
          boostsMontres={boostsMontres}
          carteScene={carteScene}
          dosRencontre={dosRencontre}
          actif
        />
        {contenu}
      </>,
      cadre
    )
  }

  // LE CARTOUCHE DU BAS (scene PC, refonte du 04/10/2026). Tout ce qui precede
  // est la mecanique, commune aux trois rendus ; a partir d'ici, la scene du PC
  // dessine dans `CartouchePhase`, et la table comme le telephone gardent le
  // rendu qui suit, inchange. Le composant rend lui-meme `null` quand il n'a
  // rien a montrer (ni etape, ni question avant la premiere etape).
  // LE SPECTATEUR NE VALIDE RIEN, il suit le joueur : le bilan d'une phase
  // finie disparait quand le joueur l'a referme (`ferme`, etape-partagee.ts).
  if (spectateur && !phaseRaconteeEnCours && suiviDuJoueur.ferme) return null

  if (nouvelleScene) {
    // LA RELECTURE PAR LES PASTILLES (D22, D23). Le controleur la retient en
    // onglets (six temps, `relecture`) ; le cartouche du bas parle en
    // pastilles (cinq) : ④ « Cartes rencontre » se relit par ses revelations,
    // la distribution n'etant plus une etape (D15).
    const ongletDeLaPastille: Record<ClePastille, CleOnglet> = {
      menace: 'menace',
      mechant: 'mechant',
      sbires: 'sbires',
      'cartes-rencontre': 'revelation',
      bilan: 'bilan',
    }
    const pastilleRelue = relecture ? pastilleDuTemps(relecture.temps) : undefined
    return (
      <>
      {/* LOT 3 (essai, decisions 21 a 25) : les fleches source -> cible, dans
          la couleur du joueur vise. Seulement quand la boite est affichee. */}
      {essai && cadresJoueurs ? (
        <FlechesPhase
          etape={etape}
          actif={!termine && !partieFinie && etape !== undefined && !relecture}
          cadres={cadresJoueurs}
          joueurDeCarte={joueurDeCarte ?? joueurInconnu}
          boostsMontres={boostsMontres}
        />
      ) : null}
      {/* LOT 4 (essai, decisions 49 a 53) : les cartes volent vers la table et vers leur pile. */}
      {essai ? <TrajetsPhase actif={!termine && !partieFinie && etape !== undefined && !relecture} /> : null}
      {/* Essai, 13/10/2026 (encadrés ④ ⑫) : boosts et traîtrises vers la défausse rencontre au clic. */}
      {essai ? <DepartsDeLaBoite etape={etape} boostsMontres={boostsMontres} actif={!termine && !partieFinie && !relecture} /> : null}
      {/* Essai, 13/10/2026 (encadré ⑩) : le numéro d'ordre de chaque sbire, sur la table. */}
      {essai ? <NumerosSbires etapes={etapes} cle={etape?.cle} actif={!termine && !partieFinie && !relecture} /> : null}
      {/* Essai, 13/10/2026 : ce qu'un boost ★ met en jeu n'arrive sur la table qu'au clic. */}
      {essai ? (
        <EtoilesEnAttente etape={etape} boostsMontres={boostsMontres} actif={!termine && !partieFinie && !relecture} />
      ) : null}
      <CartouchePhase
        refCartouche={setElCartouche}
        style={
          essai && cadresJoueurs
            ? {
                ...styleDeplace,
                ...(styleDuCadre(cadreDeLEtape(etape, cadresJoueurs, joueurDeCarte ?? (() => undefined))) as CSSProperties),
              }
            : styleDeplace
        }
        cadre={essai && cadresJoueurs ? cadreDeLEtape(etape, cadresJoueurs, joueurDeCarte ?? (() => undefined)) : undefined}
        gestes={gestesDeplacer}
        etape={etape}
        etapes={etapesAffichees}
        index={index}
        efface={termine || partieFinie}
        questionAuJoueur={questionAuJoueur}
        question={question}
        questionDuMoteur={questionDuMoteur}
        questionDUnAutre={questionDUnAutre}
        tempsQuestion={tempsQuestion}
        avancer={avancer}
        multi={piedMulti}
        enAttente={enAttente}
        attendUnAutreJoueur={attendUnAutreJoueur}
        nomJoueurAttendu={nomJoueurAttendu}
        secondesFilet={secondesFilet}
        defaiteLocale={defaiteLocale}
        boostsMontres={boostsMontres}
        essai={essai}
        dynamique={dynamique && presentation === 'scene'}
        // L'ancien « Bis » est LA presentation du cartouche central depuis le
        // 10/10/2026 ; le cartouche pose sur la table garde la sienne.
        bis={presentation === 'scene'}
        montrerBoostSuivant={essai ? () => setBoostsMontres(etape?.boosts.length ?? 0) : undefined}
        carteCachee={essai && nouvelleScene && etape?.titre === 'revelation' && !cartesRetournees.has(etape.cle)}
        retournerCarte={() => etape && setCartesRetournees((deja) => new Set(deja).add(etape.cle))}
        couleursJoueurs={couleursDesJoueurs}
        couleurDeCarte={
          essai && cadresJoueurs
            ? (id: number) => {
                const siege = (joueurDeCarte ?? joueurInconnu)(id)
                return siege === undefined ? undefined : cadresJoueurs[siege]?.couleurs[0]
              }
            : undefined
        }
        tempsParDecision={tempsParDecision}
        pvMaxParNom={pvMaxParNom}
        carteScene={carteScene}
        nomFr={nomFr}
        texteEtoile={texteEtoile}
        infoCarte={infoCarte}
        infoRevelee={infoRevelee}
        cartesDistribuees={cartesDistribuees}
        herosLocauxIds={herosLocauxIds}
        herosDesAutresIds={herosDesAutresIds}
        relecture={pastilleRelue ? { temps: pastilleRelue } : undefined}
        setRelecture={(r) => setRelecture(r ? { temps: ongletDeLaPastille[r.temps] } : undefined)}
      />
      </>
    )
  }

  // LA QUESTION AVANT LA PREMIERE ETAPE (12/09/2026). Le moteur peut ouvrir
  // une fenetre d'interruption avant tout fait de la phase : « la menace va
  // etre placee, veux-tu jouer De Grandes Responsabilites ? » (point 1, avant
  // le fait `menace`). board.tsx lui a deja retire le panneau central
  // (`questionEnScene`), et ce composant rendait `null` faute d'etape : plus
  // aucun bouton nulle part, « Fin du tour » desactive, le joueur bloque, le
  // moteur attendant sans limite. Vu en jeu contre Ultron, capture a l'appui.
  // Sans etape, il n'y a ni chronologie ni scene a montrer : le bandeau
  // « A toi de jouer » et la question suffisent.
  if (!etape && !termine && !partieFinie && questionAuJoueur && question !== undefined) {
    return enveloppe(
      <section
        ref={setElCartouche}
        className={classeCartouche('est-question')}
        style={styleDeplace}
        role="dialog"
        aria-label={t('Phase du méchant')}
      >
        <div className="deroule-poignee poignee-glisser" {...gestesDeplacer} aria-hidden="true" />
        <div className="deroule-question-scene">{question}</div>
      </section>
    )
  }

  // L'ATTENTE D'UN AUTRE JOUEUR AVANT LA PREMIERE ETAPE (multi, 11/10/2026) :
  // l'hote est interroge, les autres ne voyaient rien sur le telephone et sur
  // la table. Ils voient qui on attend, sans un bouton.
  if (!etape && !termine && !partieFinie && !questionAuJoueur && attendUnAutreJoueur && phaseMechantEnCours && !spectateur) {
    return enveloppe(
      <section
        ref={setElCartouche}
        className={classeCartouche('est-attente')}
        style={styleDeplace}
        role="status"
        aria-label={t('Phase du méchant')}
      >
        <div className="deroule-poignee poignee-glisser" {...gestesDeplacer} aria-hidden="true" />
        <span className="deroule-rond-mention" aria-live="polite">
          {texteAttente({ autreJoueur: true, nom: nomJoueurAttendu })}
        </span>
      </section>
    )
  }

  if (!etape || termine || partieFinie) return null

  // L'etape TELLE QU'ON LA LIT : noms francais quand le plateau les connait.
  // `etape` reste la source pour ce qui se cherche par nom anglais (les PV
  // maximum, indexes par le nom du monde).
  const enLangue = (e: EtapeDeroule): EtapeDeroule => etapeEnLangue(e, nomFr)
  const etapeLue = enLangue(etape)

  // Position du temps COURANT dans la chronologie : elle seule dit qui est
  // deja passe. Calculee une fois pour les cinq temps, pas a chaque `<li>`.
  //
  // Un temps absent de la chronologie (le bilan) compte comme place APRES tous
  // les autres : sur la derniere etape, les cinq temps s'affichent alors tous
  // valides, ce qui est exactement ce qui vient de se passer. Sans cela, le
  // `-1` rendu par findIndex n'en aurait marque aucun.
  // Pendant une question, la frise suit la phase REELLE du moteur quand elle a
  // pris de l'avance sur la derniere etape connue (voir `tempsDeLaQuestion`).
  const positionDe = (cle: TempsPhase | undefined) => ONGLETS.findIndex((item) => item.cle === cle)
  const tempsAffiche =
    questionAuJoueur && tempsQuestion !== undefined && positionDe(tempsQuestion) > positionDe(etape.temps)
      ? tempsQuestion
      : etape.temps
  const trouve = positionDe(tempsAffiche)
  const positionCourante = trouve === -1 ? ONGLETS.length : trouve

  // « 1 sur 3 » : combien d'etapes ce temps compte, et ou l'on en est.
  // `undefined` quand il n'en compte qu'une, et rien ne s'affiche alors.
  const rang = rangDansLeTemps(etapesAffichees, index)
  // Le detail du coup suit les boosts deja retournes (`boostsMontres`) : la
  // ligne s'allonge d'un terme quand une carte de boost parait.
  const resultat = detailEtape({ ...etapeLue, boosts: etapeLue.boosts.slice(0, boostsMontres) })
  // Avant → apres. Le maximum de PV vient du monde, par le nom de la cible.
  // Le seuil d'une manigance vient de l'etape de MENACE qui la vise (le fait
  // d'activation ne le porte pas) : « 7 → 9 / 12 » plutot que « 7 → 9 ».
  const plafondConnu =
    etape.plafond ??
    etapesAffichees.find(
      (autre) =>
        autre.plafond !== undefined && autre.cibleId !== undefined && autre.cibleId === etape.cibleId
    )?.plafond
  const compteur = evolutionEtape(
    { ...etapeLue, plafond: plafondConnu },
    etape.cibleNom ? pvMaxParNom?.get(etape.cibleNom) : undefined
  )
  const annulee = texteActivationAnnulee(etapeLue)
  const cause = texteCauseActivation(etapeLue)
  // La chaine Renfort / annulation / remplacement et la sortie de la carte qui
  // a annule (rapport Yarro n72), en texte sur ce rendu (telephone, table).
  const chaineTexte = texteDeLaChaine(
    etapesAffichees,
    etape.cle,
    (e) => (e.carteId !== undefined ? nomFr?.(e.carteId) : undefined) ?? e.cibleNom
  )
  const sorties = sortiesDeLEtape(etapesAffichees, etapeLue)

  // LA FRISE DES SIX ONGLETS (decisions du 03/10/2026) : la seule chose que le
  // cartouche garde quand il se replie devant une question du moteur.
  //
  // Un onglet se juge par rapport au temps COURANT, celui de l'etape affichee :
  //  - avant lui : PASSE, rouge, avec son resultat court (« 3 dégâts · +1
  //    menace », « aucun ») ; « vide » quand il n'a eu que son etape vide ;
  //  - lui : en cours, rouge souligne ;
  //  - apres lui : A VENIR, gris, jamais vide (constat en partie : « Sbires
  //    (aucun) » affiche pendant que le moteur demandait dans quel ordre
  //    activer deux sbires).
  // Sur le bilan, c'est l'onglet Bilan qui est en cours, et tous les autres
  // sont passes.
  const chronologie = (
    <ol className="deroule-temps">
      {ONGLETS.map((onglet, position) => {
        const estCourant = onglet.cle === tempsAffiche
        const estAvant = !estCourant && position < positionCourante
        const aDesEtapes = etapesAffichees.some((e) => e.temps === onglet.cle && e.titre !== 'vide')
        const estVide = estAvant && !aDesEtapes
        const estPasse = estAvant && aDesEtapes
        const classe = estVide ? 'est-vide' : estCourant ? 'est-courant' : estPasse ? 'est-passe' : ''
        return (
          <li
            key={onglet.cle}
            className={`${classe}${relecture?.temps === onglet.cle ? ' est-relu' : ''}`}
          >
            {/* Un onglet PASSE se relit d'un clic (pas pendant une question :
                elle doit rester sous les yeux). */}
            {estAvant && !questionAuJoueur ? (
              <button
                type="button"
                className="deroule-onglet-bouton"
                onClick={() => setRelecture({ temps: onglet.cle })}
              >
                <span className="deroule-onglet-nom">{nomDOnglet(t(onglet.libelle))}</span>
                <small className="deroule-onglet-resume">{resumeOnglet(etapesAffichees, onglet.cle)}</small>
              </button>
            ) : (
              <>
                <span className="deroule-onglet-nom">{nomDOnglet(t(onglet.libelle))}</span>
                {estAvant ? (
                  <small className="deroule-onglet-resume">{resumeOnglet(etapesAffichees, onglet.cle)}</small>
                ) : null}
              </>
            )}
          </li>
        )
      })}
    </ol>
  )

  // L'HYPOTHESE DU MODE DETAILLE, DITE QUAND ELLE NE TIENT PLUS.
  //
  // Le mode repose sur ceci : le moteur ne produit rien tant qu'on ne lui a pas
  // repondu, donc le cartouche donne le rythme. Un « Temps par decision » regle
  // a la preparation (`max_timeout`) fait expirer `DoWaitSync` et `DoGetInput`,
  // et le moteur poursuit sans notre accuse ni notre reponse. Le cartouche ne
  // change RIEN a son rythme pour autant : il le mentionne, sobrement, dans ses
  // deux etats, pour que la partie qui avance seule ne ressemble pas a un
  // defaut. Pas d'`aria-live` : cette mention ne survient pas, elle est vraie
  // pour toute la partie.
  const mentionTempsParDecision =
    tempsParDecision > 0 ? (
      <p className="deroule-timeout">{texteTempsParDecision()}</p>
    ) : null

  // LES CARTES DE LA SCENE. Toutes a la meme taille (board.css,
  // `.deroule-cartes` fixe `--card-w`), face visible, lues dans l'index du
  // monde par `carteScene` : la carte revelee et les boosts sont encore face
  // cachee dans le monde de cette trame, on force leur face. Une carte
  // introuvable (fait degrade, index pas encore lu) laisse sa place a son nom
  // seul, jamais a un trou muet.
  const scene = sceneDe(etape)
  const nomDe = (carte: CarteDeScene): string => {
    if (carte.role === 'dos') return t('Carte rencontre')
    if (carte.role === 'auteur') return etapeLue.auteurNom ?? ''
    if (carte.role === 'boost') return etapeLue.boosts.find((b) => b.cibleId === carte.id)?.nom ?? ''
    return etapeLue.cibleNom ?? ''
  }
  // ⚠ LA PHRASE DE L'ETAPE, ET SES NOMS DE CARTES SURVOLABLES (15/09/2026).
  // C'est CE QUI REMPLACE les cartes de l'etape : « il n'y a pas besoin de
  // montrer les cartes ; par contre, tu peux mettre le nom, et quand on hover
  // sur le nom, on voit la carte en question ».
  //
  // Le nom porte le meme `data-card-id` qu'une carte de la table :
  // `useApercuSurvol` ne fait aucune difference entre les deux, et c'est tout
  // ce qu'il a fallu. Le decoupage se fait sur les noms que l'ETAPE porte,
  // jamais sur le texte redige : chercher un nom dans une phrase traduite
  // casserait a la premiere langue.
  //
  // ⚠ UN NOM DONT LA CARTE EST INCONNUE RESTE UN SIMPLE GRAS, sans souligne ni
  // curseur main (« il reste du texte ordinaire », meme jour) : on ne promet
  // que ce qu'on peut tenir, et un nom qui s'annonce survolable sans rien
  // montrer est pire que pas de souligne du tout.
  //
  // ⚠ ET « CONNUE » VEUT DIRE MONTRABLE, PAS NOMMEE. L'etape porte toujours
  // l'identifiant moteur de sa cible ; l'INDEX DES SCANS, lui, peut ne pas
  // l'avoir (carte hors table, index pas encore lu). Se fier a l'identifiant
  // seul souligne un nom qui n'ouvrira rien — exactement ce qui a ete ecarte.
  // On ne souligne donc que ce que la loupe saura montrer, et c'est la MEME
  // liste qu'elle interroge (`cartesVisibles`, `propsDe`).
  const idsMontrables = new Set(
    cartesVisibles.flatMap((carte) =>
      carte.role === 'dos' || !propsDe(carte) ? [] : [carte.id]
    )
  )
  const idSiMontrable = (id: number | undefined) =>
    id !== undefined && idsMontrables.has(id) ? id : undefined

  const phraseSurvolable = (phrase: string): ReactNode =>
    decouperPhrase(
      phrase,
      [etapeLue.auteurNom, etapeLue.cibleNom],
      [idSiMontrable(etapeLue.carteId), idSiMontrable(etapeLue.cibleId)]
    ).map((morceau, rang) =>
      morceau.gras ? (
        morceau.carteId !== undefined ? (
          <b
            key={rang}
            className="deroule-nom"
            data-card-id={morceau.carteId}
            tabIndex={0}
            // Au doigt : un appui ouvre la carte, un appui ailleurs la referme
            // (decision du 15/09/2026, « un appui sur le nom ouvre la carte »).
            onClick={() => viserScene(String(morceau.carteId))}
            onFocus={() => viserScene(String(morceau.carteId))}
            onBlur={() => viserScene(undefined)}
          >
            {morceau.texte}
          </b>
        ) : (
          <b key={rang}>{morceau.texte}</b>
        )
      ) : (
        <span key={rang}>{morceau.texte}</span>
      )
    )

  /**
   * Le titre du cartouche : la meme phrase, survolable, quel que soit l'etat.
   *
   * ⚠ L'ECOUTE DU SURVOL EST SUR LE TITRE, pas sur chaque nom. C'est la regle
   * de `apercu-survol.ts`, et elle est la pour une raison mesuree : un
   * `mouseleave` pose sur un nom n'est jamais emis quand ce nom disparait sous
   * le pointeur (l'etape avance), et l'agrandissement reste ouvert pour
   * toujours.
   */
  const titreSurvolable = (classe: string) => (
    <p className={classe} onMouseOver={survolerScene} onMouseLeave={quitterScene}>
      {phraseSurvolable(titreEtape(etapeLue))}
    </p>
  )

  // LE GESTE PHYSIQUE (decide avec l'utilisateur le 7 septembre 2026) : un
  // boost qui arrive dos visible et se retourne, la carte revelee qui se
  // retourne sur place. Les animations sont dans board.css, coupees avec les
  // autres (`body.plateau-sans-animations`). Les cles portent la cle de
  // l'ETAPE : React remonte l'element a chaque etape, et l'animation rejoue.
  //
  // ⚠ LE JETON QUI TOMBAIT SUR LA CIBLE EST PARTI AVEC ELLE (15/09/2026). Il
  // se posait sur la carte visee ; cette carte n'est plus dessinee, et un jeton
  // n'a pas de sens pose sur rien. Ce qu'il disait n'est pas perdu : la phrase
  // le porte deja (« Hunting Down Heroes gagne 2 menaces ») et le compteur a sa
  // droite donne l'avant et l'apres (« 5 → 7 / 12 »).


  const rendreCarte = (carte: CarteDeScene, position: number) => {
    const props = propsDe(carte)
    const apport =
      carte.role === 'boost' ? etape.boosts.find((b) => b.cibleId === carte.id)?.apport : undefined
    const scan = props ? (
      // Rien de ce que le monde COURANT dit de la carte : ni compteur, ni
      // PV, ni pastille de type. La table peut etre en avance sur le
      // recit ; c'est la scene qui donne les chiffres de l'etape, et un
      // « 9/12 » sur la carte contredisait le « 7/12 » de l'etape.
      <ScanCardTraduite
        {...props}
        state={undefined}
        exhausted={false}
        counters={undefined}
        schemeThreat={undefined}
        allyHp={undefined}
        stats={undefined}
        labelType={undefined}
        camp={undefined}
        // Carte NUE (decide avec l'utilisateur) : ni barre ni jeton, le
        // chiffre de l'etape est a droite et le jeton qui tombe est le geste.
        jauge={undefined}
        jetonMenace={undefined}
        jetonDegats={undefined}
        masquerType
      />
    ) : (
      <div className="deroule-carte-absente">{nomDe(carte)}</div>
    )
    // Le boost et la carte revelee se RETOURNENT : dos de carte rencontre
    // derriere, la face devant, une rotation a l'arrivee.
    const seRetourne = (carte.role === 'boost' || carte.role === 'revelee') && dosRencontre !== undefined
    return enveloppe(
      <figure
        key={`${carte.role}-${position}`}
        className={`deroule-carte est-${carte.role}`}
      >
        {seRetourne ? (
          <div className="deroule-retourne" key={`${etape.cle}-${carte.role}-${position}`}>
            <div className="deroule-retourne-dos" aria-hidden="true">
              <img src={dosRencontre?.imageUrl} alt="" />
            </div>
            <div className="deroule-retourne-face">{scan}</div>
          </div>
        ) : (
          scan
        )}
        {apport !== undefined ? (
          <figcaption className="deroule-carte-legende">
            {t('Boost')} +{apport}
          </figcaption>
        ) : null}
      </figure>
    )
  }
  // A gauche l'auteur et ses boosts (ou la carte seule), a droite la cible.
  // Les boosts se retournent UN PAR UN (`boostsMontres`, plus haut), comme
  // leurs lignes dans le texte : la carte parait quand sa ligne parait.
  const boostsVisibles = new Set(etape.boosts.slice(0, boostsMontres).map((b) => b.cibleId))
  const gauche = scene.cartes.filter(
    (carte) => carte.role !== 'cible' && (carte.role !== 'boost' || boostsVisibles.has(carte.id))
  )
  const droite = scene.cartes.filter((carte) => carte.role === 'cible')
  // L'apercu est monte dans <body> (portail) : `au-dessus-du-deroule` le
  // fait passer devant la scene (540), comme `au-dessus-du-bilan` pour le
  // recap. Le dos de la distribution n'a rien a montrer en grand.
  //
  // ⚠ IL SE REND A COTE DU TEXTE, PAS DANS LA RANGEE DE CARTES. Depuis que le
  // survol d'un NOM l'ouvre, la rangee n'existe plus sur la plupart des etapes,
  // et le mode « Sur la table » ne l'a jamais dessinee : le laisser dedans,
  // c'etait un survol de nom qui n'ouvrait rien. Il est monte dans <body> de
  // toute facon, sa place dans l'arbre ne change rien a l'ecran.
  const carteRegardee = carteDeSceneRegardee ? propsDe(carteDeSceneRegardee) : undefined
  const loupe =
    carteRegardee && !carteRegardee.facedown ? (
      <CarteApercu carte={carteRegardee} classe="au-dessus-du-deroule" />
    ) : null
  // ⚠ L'AUTEUR ET SA CIBLE NE SE DESSINENT PLUS (15/09/2026). « Il n'y a pas
  // besoin de montrer les cartes ; par contre, quand on hover sur le nom, on
  // voit la carte en question. » Elles restent dans `scene.cartes`, car c'est
  // la que le survol d'un nom va CHERCHER la carte a montrer : on cesse de les
  // dessiner, on ne les oublie pas.
  //
  // ⚠ CEUX-LA RESTENT MONTRES, et la question posee ce jour-la le disait mot
  // pour mot : parmi « toutes sans exception », « toutes sauf la carte
  // revelee » et « seulement celles de l'etape », c'est la DERNIERE qui a ete
  // choisie — « l'attaquant et sa cible partent, remplaces par leurs noms ».
  //
  //  - le BOOST : « elles restent montrees », decision du meme jour. Une carte
  //    de boost est retournee sous les yeux du joueur et change le resultat de
  //    l'attaque. C'est un moment du jeu, pas une information de plus.
  //  - la carte REVELEE et le DOS de la distribution : une carte que le joueur
  //    n'a jamais vue, « un nom seul ne dirait rien ».
  const cartesDessinees = (liste: typeof gauche) =>
    liste.filter((c) => c.role !== 'auteur' && c.role !== 'cible')
  const gaucheDessinee = cartesDessinees(gauche)
  const droiteDessinee = cartesDessinees(droite)
  // ⚠ LA RANGEE NE PARAIT QUE S'IL RESTE QUELQUE CHOSE A DESSINER. Une etape
  // qui n'a plus qu'un auteur et une cible (la plupart) ne laisse plus rien :
  // un conteneur vide y aurait garde sa marge, et le cartouche un trou.
  const cartesScene =
    gaucheDessinee.length + droiteDessinee.length > 0 ? (
      <div className="deroule-cartes" onMouseOver={survolerScene} onMouseLeave={quitterScene}>
        {gaucheDessinee.length > 0 ? (
          <div className="deroule-groupe">{gaucheDessinee.map(rendreCarte)}</div>
        ) : null}
        {/* ⚠ PLUS DE FLECHE : elle reliait les deux cartes de l'etape, qui ne
            sont plus dessinees. « Non, la phrase suffit » (15/09/2026) : « Klaw
            va attaquer Wolverine » dit deja qui attaque qui, dans l'ordre. */}
        {droiteDessinee.length > 0 ? (
          <div className="deroule-groupe">
            {droiteDessinee.map((carte) => rendreCarte(carte, gaucheDessinee.length))}
          </div>
        ) : null}
      </div>
    ) : null

  // ⚠ LES CARTES DE LA SCENE DISPARAISSENT SUR LA TABLE. Les rejouer dans le
  // cartouche alors qu'il est POSE SUR LA TABLE les montrerait deux fois, a
  // dix centimetres l'une de l'autre. Ce sont les vraies cartes qu'on regarde,
  // c'est tout l'interet du mode.
  const cartesMontrees = surTable ? null : cartesScene

  // Le moteur pose une question au joueur : le cartouche s'efface devant
  // elle. Ni titre, ni bouton, ni « La suite arrive… » (ce serait un
  // mensonge : c'est le moteur qui attend). La chronologie reste, pour que le
  // joueur sache toujours ou il en est, et la mention dit qui attend qui.
  if (questionAuJoueur && question) {
    return enveloppe(
      <section
        ref={setElCartouche}
        className={classeCartouche('est-question')}
        style={styleDeplace}
        role="dialog"
        aria-label={t('Phase du méchant')}
      >
        {/* Plus de bandeau « À toi de jouer » (retire le 03/10/2026, demande de
            l'utilisateur) : la frise sert de poignee pour deplacer la fenetre. */}
        <div className="deroule-chrono poignee-glisser" {...gestesDeplacer}>
          {chronologie}
        </div>
        {loupe}
        {cartesMontrees}
        {/* L'intention reste dite au-dessus de la question : « Ultron va
            attaquer Shuri », et le joueur decide en voyant le coup. Sur toute
            autre etape (l'ordre des sbires se demande avant tout fait), la
            scene garde ses cartes et se tait : la question dit tout. */}
        {etapeEstAnnonce ? (
          <div className="deroule-entete">
            {titreSurvolable('deroule-titre')}
          </div>
        ) : null}
        {etapeEstAnnonce && resultat ? <p className="deroule-resultat">{resultat}</p> : null}
        <div className="deroule-question-scene">{question}</div>
        {mentionTempsParDecision}
      </section>
    )
  }

  // ⚠ SUR LA TABLE, LE CARTOUCHE SE TAIT DEVANT LA QUESTION DU MOTEUR.
  //
  // Le panneau du moteur (« Choisir la cible », « Defendre / Passer ») s'ouvre
  // au centre, et le cartouche s'y repliait AU MEME ENDROIT pour dire « le
  // moteur attend ta reponse ». Depuis que tout est centre, les deux se
  // superposaient - avec le selecteur de cibles par-dessus, cela faisait TROIS
  // panneaux empiles. Capture a l'appui de l'utilisateur, 14/09/2026 : « c'est
  // quoi cette merde qui se superpose ».
  //
  // Il n'a rien a ajouter : le panneau du moteur dit deja qu'il attend, et il
  // porte les boutons. `enveloppe(null)` garde le reste du recit (le trait, les
  // cartes sorties du paquet, la ligne des temps dans la barre) : seul le
  // panneau redondant disparait.
  if (surTable && questionAuJoueur && question === undefined) {
    return enveloppe(null)
  }

  // LA QUESTION DANS LA BULLE (v3, Q17) : sur la table, la bulle remplace le
  // panneau central. Les cartes possibles restent allumees et cliquables sur
  // la table ; la bulle dit l'intention et porte les boutons (« Ne pas
  // defendre »...).
  if (surTable && questionAuJoueur) {
    return enveloppe(
      <div
        ref={setElCartouche}
        className={`deroule-rond-place deroule-bulle-table est-question${classeTelephone}${bulleFantome ? ' est-fantome' : ''}`}
        style={styleBulle}
        role="dialog"
        aria-label={t('Phase du méchant')}
      >
        {loupe}
        <div
          className="deroule-bulle-onglets poignee-glisser"
          onPointerDown={poignee.onPointerDown}
          onPointerMove={poignee.onPointerMove}
          onPointerUp={poignee.onPointerUp}
          onPointerCancel={poignee.onPointerCancel}
        >
          {chronologie}
        </div>
        {etapeEstAnnonce ? <span className="deroule-recit">{phraseSurvolable(titreEtape(etapeLue))}</span> : null}
        <div className="deroule-bulle-question">{question}</div>
      </div>
    )
  }

  if (questionAuJoueur) {
    return enveloppe(
      <>
        <section
          ref={setElCartouche}
          className={classeCartouche('est-replie')}
          style={styleDeplace}
          role="dialog"
          aria-label={t('Phase du méchant')}
        >
          {loupe}
          <div className="deroule-chrono poignee-glisser" {...gestesDeplacer}>
            {chronologie}
          </div>
          {/* L'INTENTION, et elle seule, reste dite pendant la question. C'est
              le second temps de la decision 7 : « Klaw va attaquer Colossus,
              tu peux defendre ou repondre ». Sur toute autre etape, le
              cartouche se tait — le moteur attend le joueur, et rien de ce que
              le cartouche pourrait ajouter n'aiderait a repondre.

              La mention de la fenetre ne parait QUE la : c'est la seule
              condition qui prouve que le moteur pose vraiment une question au
              joueur local. L'ecrire sur une annonce muette inviterait a
              chercher une reponse qui n'existe pas. */}
          {etapeEstAnnonce ? (
            <>
              {titreSurvolable('deroule-titre')}
              {resultat ? <p className="deroule-resultat">{resultat}</p> : null}
              <p className="deroule-fenetre" aria-live="polite">
                {texteFenetreReponse()}
              </p>
            </>
          ) : (
            <p className="deroule-question" aria-live="polite">
              {t('Le moteur attend ta réponse')}
            </p>
          )}
          {mentionTempsParDecision}
        </section>
      </>
    )
  }

  /* ================= SUR LA TABLE : RIEN QU'UN BOUTON =======================
     ⚠ LE PANNEAU ENTIER DISPARAIT ICI, et c'est le coeur de la demande.
     L'utilisateur, le 14/09/2026, apres avoir vu la premiere version :
     « ce que tu n'as pas compris, c'est que je ne voulais plus ces grosses
     fenetres ». Le mode s'appelle « Sur la table » et je lui avais remis le
     panneau du mode Detaille, juste deplace a cote de la carte : meme titre
     geant, meme chronologie, meme regle depliable, memes deux boutons.

     Quatre remplacements lui ont ete montres sur le vrai plateau ; il a retenu
     le plus radical : un bouton rond contre la carte qui agit, RIEN D'AUTRE.
     Ce qui raconte l'etape est deja sur la table : le trait porte qui frappe
     qui, son nombre et sa couleur, les boosts sont sortis du paquet, la carte
     rencontre s'affiche a cote de son deck.

     ⚠ DEUX ETAPES GARDENT LEUR PANNEAU, et ce ne sont pas des exceptions de
     confort : le BILAN de fin de phase est un recapitulatif, il n'a aucune
     carte sur la table a montrer ; le COUP FATAL demande au joueur le droit de
     reprendre la partie, pas de passer a la suite. Les reduire a un rond
     perdrait ce qu'ils ont a dire.

     ⚠ ET LA QUESTION DU MOTEUR AUSSI : ses branches sont plus haut dans ce
     fichier et ne passent pas par ici. C'est la qu'on choisit de defendre ; il
     faut voir les boutons. */
  // Le nombre de l'etape, dans son unite, EXACTEMENT comme le trait le dit.
  const contenu = contenuDuTrait(etapeLue)
  const phraseEtape = titreEtape(etapeLue)
  const nombreEnClair =
    contenu.montant !== undefined
      ? `${contenu.montant}${contenu.unite ? ' ' + t(contenu.unite) : ''}`
      : contenu.unite
        ? t(contenu.unite)
        : ''
  const recit = {
    ton: contenu.ton,
    // ⚠ PAS DEUX FOIS LE MEME NOMBRE. Certaines phrases le portent deja :
    // « The Break-In! gagne 1 menace » suivi d'un « 1 menace » en jaune disait
    // la meme chose a dix pixels d'ecart. Constate a l'ecran. On ne rajoute le
    // nombre que quand la phrase ne le dit pas.
    texte: nombreEnClair && phraseEtape.includes(nombreEnClair) ? '' : nombreEnClair,
  }

  // LE CALCUL EN PASTILLES de la bulle (v3, Q10 et Q15) : [ATQ 2] + [+1 BOOST]
  // − [DÉF 3] sur une activation, « 1 par joueur + 1 accélération = 2 » sur la
  // menace du point 1. Rien quand l'etape ne porte pas ses chiffres.
  const boostsVus = etape.boosts.slice(0, boostsMontres)
  const activation = etape.titre === 'attaque' || etape.titre === 'manigance'
  const baseCalcul = etape.base ?? etape.valeurAnnoncee
  const termesMenace = etape.titre === 'menace' ? calculMenace(etapeLue)?.split(' = ') : undefined
  const calculBulle =
    activation && baseCalcul !== undefined && (boostsVus.length > 0 || (etape.defense ?? 0) > 0) ? (
      <span className="deroule-bulle-calcul" aria-label={detailEtape({ ...etapeLue, boosts: boostsVus })}>
        <PictoStat genre={etape.titre === 'attaque' ? 'atq' : 'men'} valeur={baseCalcul} />
        {boostsVus.map((boost) => (
          <span key={boost.cle} className="deroule-bulle-terme">
            <span className="deroule-bulle-operateur">+</span>
            <PictoBoost nombre={boost.apport} etoile={boost.etoile} />
          </span>
        ))}
        {(etape.defense ?? 0) > 0 ? (
          <span className="deroule-bulle-terme">
            <span className="deroule-bulle-operateur">−</span>
            <PictoStat genre="def" valeur={etape.defense} />
          </span>
        ) : null}
      </span>
    ) : termesMenace && termesMenace.length === 2 ? (
      <span className="deroule-bulle-calcul est-menace">
        {termesMenace[0].split(' + ').map((terme, rang) => (
          <span key={terme} className="deroule-bulle-terme">
            {rang > 0 ? <span className="deroule-bulle-operateur">+</span> : null}
            <span className="deroule-bulle-pastille">{terme}</span>
          </span>
        ))}
        <span className="deroule-bulle-operateur">=</span>
        <b className="deroule-bulle-total">{termesMenace[1]}</b>
      </span>
    ) : null
  const alerte = alerteMenace({ ...etape, plafond: plafondConnu })

  // Le bandeau d'ouverture joue encore : la table se tait. Voir la prop.
  if (surTable && attendreBandeau) return null

  // LA RELECTURE D'UN ONGLET PASSE, en lecture seule (03/10/2026).
  if (relecture) {
    const duTemps = etapesAffichees.filter((e) => e.temps === relecture.temps)
    const choisie =
      (relecture.cle !== undefined ? duTemps.find((e) => e.cle === relecture.cle) : undefined) ??
      (duTemps.length === 1 ? duTemps[0] : undefined)
    const lue = choisie ? enLangue(choisie) : undefined
    return enveloppe(
      <section
        ref={setElCartouche}
        className={classeCartouche('est-relecture')}
        style={styleDeplace}
        role="dialog"
        aria-label={t('Phase du méchant')}
      >
        <div className="deroule-chrono poignee-glisser" {...gestesDeplacer}>
          {chronologie}
        </div>
        <p className="deroule-relecture-mention">{t('Relecture')}</p>
        {lue ? (
          <DetailCoup etape={lue} />
        ) : (
          <ListeDesCoups
            coups={duTemps.map(enLangue)}
            choisir={(cle) => setRelecture({ temps: relecture.temps, cle })}
          />
        )}
        <div className="deroule-boutons">
          {lue && duTemps.length > 1 ? (
            <button type="button" className="bh-bouton" onClick={() => setRelecture({ temps: relecture.temps })}>
              {t('Tous les coups')}
            </button>
          ) : null}
          <button type="button" className="bh-bouton deroule-suivant" onClick={() => setRelecture(undefined)}>
            {t('Revenir à l’étape en cours')}
          </button>
        </div>
      </section>
    )
  }

  // LA DEFAITE SUR LA TABLE (v3, Q44) : le coup fatal a ete joue sur la table,
  // une bulle en fait le constat avant l'ecran de fin de partie.
  if (surTable && defaiteLocale && !fatalAMontrerSurTable) {
    return enveloppe(
      <div
        ref={setElCartouche}
        className={`deroule-rond-place deroule-bulle-table est-defaite${classeTelephone}`}
        style={styleBulle}
      >
        <div
          className="deroule-bulle-onglets poignee-glisser"
          onPointerDown={poignee.onPointerDown}
          onPointerMove={poignee.onPointerMove}
          onPointerUp={poignee.onPointerUp}
          onPointerCancel={poignee.onPointerCancel}
        >
          {chronologie}
        </div>
        <span className="deroule-recit">{phraseSurvolable(phraseEtape)}</span>
        <span className="deroule-bulle-defaite">
          <span aria-hidden="true">☠</span> {texteDefaite(etapeLue)}
        </span>
        <span className="deroule-bulle-compteur">{texteArretDefaite()}</span>
        {estSpectateur() ? null : (
          <span className="deroule-rond-rangee">
            <button type="button" className="deroule-rond" onClick={avancer}>
              {t('Continuer')}
              <kbd className="deroule-rond-touche">{t('Espace')}</kbd>
            </button>
          </span>
        )}
      </div>
    )
  }

  // LE BILAN SUR LA TABLE (v3, Q26 et Q29) : dans la bulle, menaces posees a
  // gauche, degats subis (et statuts) a droite ; « Terminer la phase » rend la
  // main, et l'annonce du tour du heros (SplashTour) prend le relais.
  if (surTable && etape.temps === 'bilan' && !defaiteLocale && etapeLue.bilan) {
    const menaces = etapeLue.bilan.filter((ligne) => ligne.genre === 'menaces')
    const coups = etapeLue.bilan.filter((ligne) => ligne.genre !== 'menaces')
    const colonne = (titre: string, lignes: typeof coups) => (
      <div className="deroule-bulle-colonne">
        <b className="deroule-bulle-colonne-titre">{titre}</b>
        {lignes.length === 0 ? (
          <span className="deroule-bulle-colonne-rien">{t('Aucune')}</span>
        ) : (
          lignes.map((ligne) => (
            <span key={ligne.cle} className="deroule-bulle-ligne">
              {texteLigneBilan(ligne)}
              {compteurLigneBilan(ligne) ? <small> {compteurLigneBilan(ligne)}</small> : null}
            </span>
          ))
        )}
      </div>
    )
    return enveloppe(
      <div
        ref={setElCartouche}
        className={`deroule-rond-place deroule-bulle-table est-bilan${classeTelephone}${bulleFantome ? ' est-fantome' : ''}`}
        style={styleBulle}
      >
        <div
          className="deroule-bulle-onglets poignee-glisser"
          onPointerDown={poignee.onPointerDown}
          onPointerMove={poignee.onPointerMove}
          onPointerUp={poignee.onPointerUp}
          onPointerCancel={poignee.onPointerCancel}
        >
          {chronologie}
        </div>
        <span className="deroule-recit">{titreEtape(etapeLue)}</span>
        {etapeLue.bilan.length === 0 ? (
          <span className="deroule-bulle-compteur">{texteBilanVide()}</span>
        ) : (
          <div className="deroule-bulle-colonnes">
            {colonne(t('Menaces posées'), menaces)}
            {colonne(t('Dégâts subis'), coups)}
          </div>
        )}
        {estSpectateur() ? null : (
          <span className="deroule-rond-rangee">
            {index > 0 ? (
              <button
                type="button"
                className="deroule-rond-retour"
                onClick={reculer}
                aria-label={t('Précédent')}
                title={t('Précédent')}
              >
                <span aria-hidden="true">‹</span>
              </button>
            ) : null}
            <button type="button" className="deroule-rond" onClick={avancer}>
              {t('Terminer la phase')}
              <kbd className="deroule-rond-touche">{t('Espace')}</kbd>
            </button>
          </span>
        )}
        {enAttente ? (
          <span className="deroule-rond-mention" aria-live="polite">
            {texteAttente({ autreJoueur: attendUnAutreJoueur, nom: nomJoueurAttendu })}
          </span>
        ) : null}
      </div>
    )
  }

  if (surTable && etape.temps !== 'bilan' && (!defaiteLocale || fatalAMontrerSurTable)) {
    return enveloppe(
      <div
        ref={setElCartouche}
        className={`deroule-rond-place deroule-bulle-table${classeTelephone}${bulleFantome ? ' est-fantome' : ''}`}
        style={styleBulle}
      >
        {loupe}
        {/* La frise en onglets biseautes, et la poignee pour deplacer la bulle. */}
        <div
          className="deroule-bulle-onglets poignee-glisser"
          onPointerDown={poignee.onPointerDown}
          onPointerMove={poignee.onPointerMove}
          onPointerUp={poignee.onPointerUp}
          onPointerCancel={poignee.onPointerCancel}
        >
          {chronologie}
        </div>
        <button
          type="button"
          className="deroule-bulle-aide-bouton"
          onClick={() => (aideTable ? fermerAideTable() : setAideTable(true))}
          aria-label={t('Aide')}
          aria-expanded={aideTable}
          title={t('Aide')}
        >
          ?
        </button>
        {aideTable ? (
          <span className="deroule-bulle-aide" role="note">
            <span>{t('Déplace la bulle en tirant ses onglets.')}</span>
            <span>{t('Survole une carte : la bulle s’efface pour la laisser voir.')}</span>
            <span>{t('Suivant ou Espace avance, ← revient, Échap passe toute la phase.')}</span>
            <button type="button" className="bh-bouton" onClick={fermerAideTable}>
              {t('Compris')}
            </button>
          </span>
        ) : null}
        {/* ⚠ CE QUI VIENT DE SE PASSER, EN UNE LIGNE. L'utilisateur, apres avoir
            vu le bouton seul : « est-ce que c'est possible de mettre ce qu'il
            s'est passe ? Je ne sais pas exactement si tu vois bien ce que je
            veux dire. » Quatre formes lui ont ete montrees sur le vrai plateau
            plutot que decrites ; il a retenu celle-ci, la plus sobre : la
            phrase et son nombre, juste au-dessus du bouton, sans encadre ni
            fond. On lit et on clique au meme endroit.

            ⚠ ET C'EST LE MEME NOMBRE QUE LE TRAIT, par construction : les deux
            passent par `contenuDuTrait`. Deux calculs auraient fini par se
            contredire, et le joueur verrait « 4 degats » sur le trait et
            « 1 degat » sous la phrase. */}
        <span
          className={`deroule-recit est-${recit.ton}`}
          onMouseOver={survolerScene}
          onMouseLeave={quitterScene}
        >
          {/* ⚠ LES NOMS DE CARTES EN GRAS, le reste en texte normal. Choix de
              l'utilisateur parmi trois formes (14/09/2026) : « moitie-moitie,
              les noms en gras ». On repere qui fait quoi a qui d'un coup d'oeil
              sans que la phrase crie comme un titre. Le decoupage se fait sur
              les noms que l'ETAPE porte, jamais sur le texte redige : chercher
              un nom dans une phrase traduite casserait a la premiere langue. */}
          {/* ⚠ LES NOMS SONT SURVOLABLES DEPUIS LE 15/09/2026, et c'est ce qui
              remplace les cartes de l'etape. « Arrete de montrer les cartes ;
              par contre, quand on hover sur le nom, on voit la carte en
              question. » Le nom porte le meme `data-card-id` qu'une carte :
              `useApercuSurvol` ne fait pas la difference.

              Un nom dont la carte est inconnue reste un simple gras, sans
              souligne ni curseur main : on ne promet que ce qu'on peut tenir. */}
          {phraseSurvolable(phraseEtape)}
          {recit.texte ? <b className="deroule-recit-nombre">{recit.texte}</b> : null}
        </span>
        {/* v3 (10/10/2026) : le detail sous la phrase. Compteur des sbires,
            fil d'Ariane, calcul en pastilles (Q10, Q15), avant → apres,
            effets ★ et alerte de menace (Q16). */}
        {rang ? (
          <span className="deroule-bulle-rang">
            {(etape.temps === 'sbires' ? t('Sbire %1 / %2') : t('%1 sur %2'))
              .replace('%1', String(rang.rang))
              .replace('%2', String(rang.total))}
          </span>
        ) : null}
        {chaineTexte || surtitreEtape(etapeLue) ? (
          <span className="deroule-bulle-ariane">{chaineTexte || surtitreEtape(etapeLue)}</span>
        ) : null}
        {calculBulle}
        {compteur ? <span className="deroule-bulle-compteur">{compteur}</span> : null}
        {lignesEtoileBoost({ ...etapeLue, boosts: etapeLue.boosts.slice(0, boostsMontres) }).map((ligne) => (
          <span key={ligne} className="deroule-bulle-etoile">{ligne}</span>
        ))}
        {alerte ? (
          <span className="deroule-bulle-alerte" role="status">
            {t('Attention : %1 / %2 menaces').replace('%1', String(alerte.restant)).replace('%2', String(alerte.plafond))}
          </span>
        ) : null}
        {/* ⚠ PAS DE BOUTON SUR L'ETAPE D'UN AUTRE JOUEUR : elle passe toute
            seule. En montrer un laisserait croire qu'on tient le rythme, alors
            que le moteur attend l'autre siege. */}
        {viseUnAutreJoueur || estSpectateur() ? null : (
        <span className="deroule-rond-rangee">
          {/* ⚠ LA FLECHE RETOUR, choisie par l'utilisateur (14/09/2026) : « oui,
              une petite fleche a cote ». A COTE, donc, et pas au-dessus : elle
              partage la rangee du bouton. Elle ne parait qu'a partir de la
              deuxieme etape - sur la premiere, il n'y a rien derriere. */}
          {index > 0 ? (
            <button
              type="button"
              className="deroule-rond-retour"
              onClick={reculer}
              aria-label={t('Précédent')}
              title={t('Précédent')}
            >
              <span aria-hidden="true">‹</span>
            </button>
          ) : null}
          <button
            type="button"
            // SPECTATEUR (08/10/2026) : le bouton reste, grise et inactif, pour
            // voir l'ecran du joueur ; la cle suit l'etape, il s'allume donc
            // brievement (CSS) a chaque fois que le joueur passe a la suivante.
            key={estSpectateur() ? `suivant-${etapeLue?.cle ?? ''}` : 'suivant'}
            className={`deroule-rond${estSpectateur() ? ' suivant-spectateur' : ''}`}
            disabled={estSpectateur()}
            // ⚠ SUR UN COUP FATAL, CE BOUTON N'AVANCE PAS : il fait paraitre le
            // panneau, qui demandera ensuite le droit de reprendre la partie.
            // Avancer ici sauterait la fin de la partie du joueur.
            onClick={fatalAMontrerSurTable ? () => setCoupFatalVuSurTable(true) : avancerSurTable}
            // Le texte de l'etape n'est PAS perdu : il devient le nom accessible
            // du bouton et son infobulle. Un lecteur d'ecran l'annonce, et le
            // survol le rend a qui le cherche.
            aria-label={`${titreEtape(etapeLue)} — ${t('Suivant')}`}
            title={titreEtape(etapeLue)}
          >
            {t('Suivant')}
            <kbd className="deroule-rond-touche">{t('Espace')}</kbd>
          </button>
        </span>
        )}
        {confirmerPasser && !passerTout ? (
          <span className="deroule-bulle-confirmer" role="alertdialog" aria-label={t('Passer toute la phase ?')}>
            {t('Passer toute la phase ?')}
            <button
              type="button"
              className="bh-bouton"
              onClick={() => {
                setConfirmerPasser(false)
                setPasserTout(true)
              }}
            >
              {t('Tout passer')}
            </button>
            <button type="button" className="bh-bouton" onClick={() => setConfirmerPasser(false)}>
              {t('Annuler')}
            </button>
          </span>
        ) : null}
        {/* Les deux seules mentions qui survivent : « la suite arrive » quand on
            attend le moteur ou un autre joueur, et le filet anti-blocage qui va
            jouer. Toutes deux disent pourquoi RIEN NE SE PASSE ; sans elles, le
            plateau parait fige. */}
        {enAttente ? (
          <span className="deroule-rond-mention" aria-live="polite">
            {texteAttente({ autreJoueur: attendUnAutreJoueur, nom: nomJoueurAttendu })}
          </span>
        ) : null}
        {secondesFilet !== undefined ? (
          <span className="deroule-rond-mention" aria-live="polite">
            {texteFiletProche(secondesFilet)}
          </span>
        ) : null}
      </div>
    )
  }

  return enveloppe(
    <>
      <section
        ref={setElCartouche}
        className={classeCartouche('')}
        style={styleDeplace}
        role="dialog"
        aria-label={t('Phase du méchant')}
      >
        <div className="deroule-chrono poignee-glisser" {...gestesDeplacer}>
          {chronologie}
          {rang ? (
            <span className="deroule-rang">
              {/* Cle a trous plutot qu'une concatenation : « sur » se traduit
                  deja par « on » ailleurs dans le dictionnaire, et « 1 on 3 »
                  ne veut rien dire. */}
              {t('%1 sur %2').replace('%1', String(rang.rang)).replace('%2', String(rang.total))}
            </span>
          ) : null}
        </div>

        {loupe}
        {cartesMontrees}

        {/* Le titre dit le fait, et le compteur de la cible se lit a sa
            droite. Un titre generique suivi de la meme chose en dessous
            faisait dire une seule chose a trois lignes. */}
        {/* « Renfort de X » (03/10/2026) : cette carte en est une AUTRE. */}
        {surtitreEtape(etapeLue) ? <p className="deroule-surtitre">{surtitreEtape(etapeLue)}</p> : null}
        <div className="deroule-entete">
          {/* Le bilan porte le meme titre que les autres etapes, en capitales :
              il annonce la fin de la phase, pas un coup de plus. */}
          {titreSurvolable(
            `deroule-titre${etape.temps === 'bilan' ? ' est-bilan' : ''}`
          )}
          {/* Il s'ecrivait 450 ms apres le jeton qui tombait sur la cible
              (`est-apres-jeton`). Le jeton est parti avec la carte : plus rien
              a attendre, le compteur parait avec sa ligne. */}
          {compteur ? (
            <span key={etape.cle} className="deroule-compteur">
              {compteur}
            </span>
          ) : null}
        </div>
        {resultat ? <p className="deroule-resultat">{resultat}</p> : null}
        {/* L'effet ★ des boosts DEJA retournes, une ligne chacun (03/10/2026). */}
        {lignesEtoileBoost({ ...etapeLue, boosts: etapeLue.boosts.slice(0, boostsMontres) }).map((ligne) => (
          <p key={ligne} className="deroule-etoile">{ligne}</p>
        ))}
        {/* L'activation annoncee qui n'a pas lieu. Sans cette ligne, l'etape
            resterait sur « Klaw va attaquer Colossus » et le joueur
            attendrait un coup qui ne vient pas. */}
        {annulee ? <p className="deroule-annulee">{annulee}</p> : null}
        {sorties.map((sortie) => (
          <p key={sortie} className="deroule-annulee">{sortie}</p>
        ))}
        {chaineTexte ? <p className="deroule-chaine-texte">{chaineTexte}</p> : null}
        {/* D'ou vient cette activation. Le moteur ne le dit que pour celles
            qui ne viennent PAS de la regle du jeu : la seconde attaque du
            vilain, declenchee par une carte revelee. */}
        {cause ? <p className="deroule-cause">{cause}</p> : null}
        {/* Ce que la carte revelee a fait, mesure par le moteur. Sans lui, la
            scene ne dit rien de plus : le joueur voit la table au clic suivant. */}
        {etapeLue.effets && etapeLue.effets.length > 0 ? (
          <ul className="deroule-effets">
            {etapeLue.effets.map((effet, rang) => (
              <li key={rang}>{texteEffet(effet)}</li>
            ))}
          </ul>
        ) : null}
        {/* Ce que l'effet de la carte a declenche (le vilain manigance...),
            range ici plutot qu'en etapes a part (rapport Yarro n46). */}
        {etapeLue.consequences && etapeLue.consequences.length > 0 ? (
          <ul className="deroule-effets deroule-consequences">
            {etapeLue.consequences.map((consequence) => (
              <li key={consequence.cle}>{texteConsequence(consequence)}</li>
            ))}
          </ul>
        ) : null}
        {/* Un Renfort suit cette carte : la suite est une AUTRE carte. */}
        {texteSuiteRenfort(etapeLue) ? <p className="deroule-suite-renfort">{texteSuiteRenfort(etapeLue)}</p> : null}
        {/* La chute du heros. Elle ne ressemble a aucune autre ligne du
            cartouche, et c'est voulu : c'est le moment le plus important d'une
            partie, il ne doit pas defiler comme les autres. Le crane est
            decoratif (aria-hidden) : la phrase dit deja tout, et un lecteur
            d'ecran n'a pas a epeler un symbole. */}
        {etape.defaite ? (
          <p className="deroule-defaite">
            <span aria-hidden="true">☠</span> {texteDefaite(etapeLue)}
          </p>
        ) : null}
        {/* Le bilan de fin de phase : ce que le joueur vient d'encaisser, en
            deux lignes, au moment ou il decide de son tour. Une liste VIDE
            n'est pas une absence : elle dit que la phase n'a rien coute, et le
            cartouche le dit plutot que de rester muet. */}
        {etapeLue.bilan ? (
          <ul className="deroule-bilan">
            {etapeLue.bilan.length === 0 ? (
              <li className="deroule-bilan-rien">{texteBilanVide()}</li>
            ) : (
              etapeLue.bilan.map((ligne) => (
                <li key={ligne.cle}>
                  <span className="deroule-bilan-fait">{texteLigneBilan(ligne)}</span>
                  {compteurLigneBilan(ligne) ? (
                    <span className="deroule-bilan-compteur">{compteurLigneBilan(ligne)}</span>
                  ) : null}
                </li>
              ))
            )}
          </ul>
        ) : null}
        {mentionTempsParDecision}
        <div className="deroule-boutons">
          {/* Dire qu'on attend, sans rien bloquer : une mention grise a cote du
              bouton, qui reste cliquable. Ni modale ni bouton desactive, parce
              que l'attente dure une fraction de seconde en temps normal et
              qu'un bouton qui s'eteint puis se rallume attire l'oeil plus que
              l'etape elle-meme. Un reclic pendant l'attente est sans danger :
              il relache au plus une trame de plus.

              Elle ne parle du MOTEUR que lorsqu'on attend vraiment le moteur.
              Quand c'est le joueur LOCAL qu'on attend (`questionAuJoueur`), le
              cartouche est replie plus haut et cette ligne n'existe pas : « La
              suite arrive… » par-dessus une question du moteur etait exactement
              le mensonge constate en partie. Et quand c'est un AUTRE joueur que
              la table attend, elle le dit et le nomme quand elle le peut
              (`texteAttente`, constat F5). */}
          {enAttente ? (
            <span className="deroule-attente" aria-live="polite">
              {texteAttente({ autreJoueur: attendUnAutreJoueur, nom: nomJoueurAttendu })}
            </span>
          ) : null}
          {/* Le filet va jouer. On le dit AVANT, pour que la phase qui repart
              toute seule ne ressemble pas a un bug. Meme discretion que la
              mention d'attente, a la meme place. */}
          {secondesFilet !== undefined ? (
            <span className="deroule-filet" aria-live="polite">
              {texteFiletProche(secondesFilet)}
            </span>
          ) : null}
          {/* Dit pourquoi il n'y a plus rien apres, a la place meme ou l'on
              lit d'ordinaire « La suite arrive… ». Les deux ne se croisent
              jamais : une defaite ne fait plus attendre de suite. */}
          {defaiteLocale ? <span className="deroule-arret">{texteArretDefaite()}</span> : null}
          {index > 0 ? (
            <button type="button" className="bh-bouton" onClick={reculer}>
              {t('Précédent')}
            </button>
          ) : null}
          {/* Sur le bilan, le bouton ne dit plus « Suivant » : il n'y a plus
              rien apres, et c'est lui qui rend la main au joueur. Sur une
              defaite, il dit « Continuer » : ce n'est pas une etape de plus
              qu'on demande, c'est le droit de reprendre la partie. */}
          <button
            type="button"
            key={estSpectateur() ? `suivant-${etape.cle}` : 'suivant'}
            className={`bh-bouton deroule-suivant${estSpectateur() ? ' suivant-spectateur' : ''}`}
            disabled={estSpectateur()}
            onClick={avancer}
          >
            {defaiteLocale
              ? t('Continuer')
              : etape.temps === 'bilan'
                ? t('À toi de jouer')
                : t('Suivant')}
          </button>
        </div>
      </section>
    </>
  )
}
