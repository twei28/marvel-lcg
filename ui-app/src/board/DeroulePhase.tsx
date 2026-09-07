// Le cartouche du deroule detaille : une etape a la fois.
//
// FIXE sur le cote droit de la table, il ne bouge jamais d'une etape a
// l'autre : l'oeil sait ou lire et la main ou cliquer des le deuxieme tour. Un
// cartouche colle a la carte concernee aurait deplace le bouton a chaque clic.
// Sa place exacte est MESUREE sur la table (voir plus bas), jamais ecrite en
// dur.
//
// « Precedent » RELIT, il ne rejoue rien : le monde du moteur ne recule pas.
// C'est « Annuler la derniere action » qui fait cela, et il reste disponible.
//
// Quand le moteur pose une QUESTION au joueur (dans quel ordre activer deux
// sbires, defendre ou non), le cartouche s'efface : il se replie sur sa seule
// chronologie et dit que le moteur attend le joueur. Ce n'est pas la meme
// attente que « La suite arrive… », ou c'est le joueur qui attend le moteur.

import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import {
  arreterSurDefaite,
  avecBilan,
  rangDansLeTemps,
  type EtapeDeroule,
  type TempsPhase,
} from './deroule-phase'
import {
  compteurEtape,
  compteurLigneBilan,
  regleEtape,
  resultatEtape,
  texteActivationAnnulee,
  texteArretDefaite,
  texteBilanVide,
  texteDefaite,
  texteFenetreReponse,
  texteLigneBilan,
  titreEtape,
} from './deroule-textes'
import { t } from './langue'
import { DELAI_PAS_A_PAS_DEFAUT, ecrireRegleDepliee, lireRegleDepliee } from './moteur'
import { TraitCible } from './TraitCible'
import { useDerouleScene } from './useDerouleScene'

/** Le temps de lire un boost a capacite avant le suivant. */
const DELAI_BOOST_MS = 1500

/**
 * Le pas du defilement apres Echap (« Tout derouler ») : le temps de VOIR
 * passer une etape, pas de la lire. Assez court pour que la phase file, assez
 * long pour que chaque etape soit peinte une fois et que le journal, la mise
 * en scene et le moteur la voient passer dans l'ordre.
 */
export const DELAI_DEFILEMENT_MS = 120

/**
 * L'ancre du cartouche sur la table, posee sur le body en variables CSS que
 * `.deroule-phase` (board.css) lit comme ses proprietes `left`, `bottom` et
 * `width`. Sans elles, le CSS reprend son repli (en bas au centre, a 16 px du
 * bord), qui sert quand aucune table n'est mesurable (plateau mobile,
 * premiere frame).
 *
 * ECART_MAIN : le jour que le cartouche garde a droite de la main.
 * BAS_MINIMUM : le plancher de `bottom`, le meme que le repli du CSS.
 */
const VARIABLE_GAUCHE = '--deroule-gauche'
const VARIABLE_LARGEUR = '--deroule-largeur'
const VARIABLE_BAS = '--deroule-bas'
const VARIABLE_DECALAGE = '--deroule-decalage'
const ECART_MAIN = 10
const BAS_MINIMUM = 16

/**
 * Les cinq temps de la carte de reference, dans l'ordre.
 *
 * Le mechant et ses sbires sont deux moments distincts du tour (le vilain
 * s'active AVANT ses sbires) : les fondre dans un seul « Activations »
 * cachait ou l'on en etait. Arbitrage de l'utilisateur, qui a decrit la
 * phase exactement dans ces termes.
 */
const TEMPS: { cle: TempsPhase; libelle: string }[] = [
  { cle: 'menace', libelle: 'Menace' },
  { cle: 'mechant', libelle: 'Méchant' },
  { cle: 'sbires', libelle: 'Sbires' },
  { cle: 'distribution', libelle: 'Distribution' },
  { cle: 'revelation', libelle: 'Révélation' },
]

export function DeroulePhase({
  etapes,
  identitePhase,
  phaseMechantEnCours = false,
  partieFinie = false,
  questionAuJoueur = false,
  pvMaxParNom,
  trameRetenue,
  avanceAuto = false,
  delaiAvanceMs = DELAI_PAS_A_PAS_DEFAUT,
  onSuivant,
  onTerminer,
  onDefaiteVue,
}: {
  etapes: EtapeDeroule[]
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
   * « Avance toute seule » (reglage du panneau Options, board.tsx) : chaque
   * etape se valide d'elle-meme au bout de `delaiAvanceMs`, par la MEME
   * fonction que le clic « Suivant », donc par le meme accuse de reception.
   *
   * C'est le CARTOUCHE qui tient cette horloge, et lui seul. Elle a d'abord
   * ete tenue par le moteur (`attendre-delai`, un minuteur qui relachait la
   * trame de lui-meme) pendant que le cartouche, lui, attendait des clics :
   * deux horloges qui divergeaient a la premiere etape. Constate en partie
   * reelle : le joueur lisait la menace, le mechant et ses sbires avaient
   * deja frappe. Le moteur n'a plus aucune horloge propre.
   *
   * Ce que l'avance auto ne valide JAMAIS a la place du joueur : le bilan de
   * fin de phase (c'est la qu'il reprend la main, il doit le voir) et la
   * chute d'un heros (« Continuer »). Un « Precedent » la suspend jusqu'au
   * prochain « Suivant », sans quoi l'etape relue repartirait aussitot.
   */
  avanceAuto?: boolean
  /** Le temps de lire une etape avant qu'elle ne se valide seule (ms). */
  delaiAvanceMs?: number
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
  // Vrai apres Echap (« Tout derouler ») : les etapes defilent sans delai de
  // lecture, jusqu'au bilan, qui attend un vrai clic. C'est le CARTOUCHE qui
  // defile, par la meme fonction que « Suivant » : le moteur suit, une trame
  // a la fois, il ne precede jamais. Avant, Echap relachait le moteur pour
  // tout le reste de la phase (`passerToutLaPhase`, `phaseSautee`) et le
  // cartouche restait sur son etape pendant que le moteur filait : le joueur
  // n'avait plus aucune autorite sur le rythme. Un « Precedent » y met fin.
  const [defilement, setDefilement] = useState(false)
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
  const [validee, setValidee] = useState<{ cle: string; etat?: EtapeDeroule['etat'] }>()

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


  const cleDeLaPhase = phaseRacontee.current

  // Le dépliant de la règle sous l'étape : un choix qu'on ne fait qu'une
  // fois (voir lireRegleDepliee dans moteur.ts). Lu une seule fois a l'etat
  // initial, PAS reinitialise a chaque nouvelle phase (contrairement a
  // `index`, `termine`, etc. ci-dessous) : il doit rester replie sur toutes
  // les etapes et toutes les parties, jusqu'a ce que le joueur le replie.
  const [regleDepliee, setRegleDepliee] = useState(() => lireRegleDepliee())

  const basculerRegle = () => {
    setRegleDepliee((avant) => {
      const apres = !avant
      ecrireRegleDepliee(apres)
      return apres
    })
  }

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
    setDefilement(false)
    setValidee(undefined)
    derniereTrameAcquittee.current = undefined
    memoireEtapes.current = []
  }, [cleDeLaPhase])

  // Les etapes de la phase RACONTEE, memorisees.
  //
  // Le moteur quitte la phase du mechant et incremente le round dans la MEME
  // foulee : il ne retient aucune trame entre les deux, donc le plateau ne voit
  // jamais l'etat intermediaire « phase finie, round inchange ». Or les etapes
  // sont filtrees sur le round du monde (`etapesDeroule`, deroule-phase.ts) :
  // a la premiere trame d'apres, la liste retombe a zero. Sans cette memoire,
  // `avecBilan` n'a plus rien a compter et le bilan de fin de phase ne
  // s'affiche JAMAIS (constat 5 du rapport A3-fix, mesure en partie reelle).
  //
  // La memoire est ecrite pendant le rendu, comme `avancerRef` plus bas : elle
  // ne doit provoquer aucun rendu, elle suit celui qui a lieu.
  if (identitePhase === cleDeLaPhase && etapes.length > 0) memoireEtapes.current = etapes
  const etapesDeLaPhase =
    identitePhase === cleDeLaPhase && etapes.length > 0 ? etapes : memoireEtapes.current

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
  const etapesAffichees = arreterSurDefaite(
    phaseRaconteeEnCours ? etapesDeLaPhase : avecBilan(etapesDeLaPhase, pvMaxParNom)
  )

  // L'INDEX, retrouve a partir de la cle retenue, a chaque rendu.
  //
  // La cle est la seule chose que le cartouche garde d'un rendu a l'autre :
  // c'est ce qui le rend insensible a l'ordre de la liste. Une revelation de
  // plus pour un autre joueur retrie les etapes, une intention se complete en
  // place, un fait arrive en amont : rien de tout cela ne deplace le joueur.
  //
  // REPLI, quand la cle a disparu de la liste (le seul cas connu : une defaite
  // survenue plus tot vient de couper le deroule derriere elle) : la premiere
  // etape NON VALIDEE. Les etapes se valident dans l'ordre, donc c'est celle
  // qui suit la derniere validee, et la premiere de toutes quand rien ne l'a
  // encore ete. Jamais un retour a zero, qui ferait tout relire.
  const rangDeLaCle =
    cleCourante === undefined ? -1 : etapesAffichees.findIndex((e) => e.cle === cleCourante)
  const rangValidee =
    validee === undefined ? -1 : etapesAffichees.findIndex((e) => e.cle === validee.cle)
  const index =
    rangDeLaCle !== -1
      ? rangDeLaCle
      : rangValidee === -1
        ? 0
        : Math.min(rangValidee + 1, etapesAffichees.length - 1)

  const etape = etapesAffichees[index]

  // Adoption de la premiere cle. Tant que le cartouche n'en retient aucune, il
  // lit l'etape 0 : une etape qui s'insererait devant elle changerait alors ce
  // qu'il montre. Des que la liste existe, il retient donc la cle de ce qu'il
  // affiche. L'effet ne se declenche qu'une fois par phase (il se rendort
  // aussitot que la cle est posee) et la remise a zero ci-dessus le reveille.
  const premiereCle = etapesAffichees[0]?.cle
  useEffect(() => {
    if (cleCourante === undefined && premiereCle !== undefined) setCleCourante(premiereCle)
  }, [cleCourante, premiereCle])

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
  const etapeValidee =
    etape !== undefined &&
    validee !== undefined &&
    validee.cle === etape.cle &&
    validee.etat === etape.etat

  const avancer = () => {
    // Hors phase du mechant, etapes est vide et il n'y a rien a avancer : une
    // touche pressee ne doit alors rien declencher.
    if (!etape) return
    // Partie finie : le cartouche n'est plus a l'ecran, sa touche Entree ne
    // doit pas continuer a relacher le moteur derriere l'ecran de fin.
    if (partieFinie) return
    // Un « Suivant » (clic, clavier, ou le minuteur de l'avance auto lui-meme)
    // leve la suspension posee par « Precedent ».
    setSuspendu(false)
    // L'etape courante est validee, DANS L'ETAT OU ELLE EST AU MOMENT DU CLIC.
    // Une intention validee ici ne vaudra pas validation de la resolution qui
    // prendra sa place (voir `validee` et `cartoucheAJour`).
    setValidee({ cle: etape.cle, etat: etape.etat })
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
    if (etape.defaite) {
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

  const reculer = () => {
    // Relire, c'est renoncer a l'attente en cours : sans cela, la sortie
    // d'attente ci-dessous repousserait aussitot le joueur en avant et
    // « Precedent » n'aurait aucun effet visible. La suite reste atteignable
    // au bouton « Suivant », comme apres tout « Precedent ».
    setEnAttente(false)
    setSuspendu(true)
    setDefilement(false)
    // Relire, c'est n'etre plus a jour : le moteur doit attendre de nouveau
    // qu'on revienne au bout. Sans cet oubli, « Precedent » relachait le
    // moteur pendant que le joueur relisait.
    setValidee(undefined)
    setCleCourante(etapesAffichees[index - 1]?.cle)
  }

  // Echap : tout derouler. Une intention d'aller de l'avant, qui leve donc la
  // suspension d'un « Precedent » anterieur.
  const derouler = () => {
    setSuspendu(false)
    setDefilement(true)
  }

  // La version la plus recente de `avancer`, pour l'horloge du cartouche
  // (plus bas : avance auto et defilement d'Echap). `avancer` est recreee a
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
  }, [enAttente, index, etapesAffichees.length, etapeValidee, phaseRaconteeEnCours])

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
  // SAUF si le moteur pose une question : la, il ne rendra pas la main avant
  // qu'on lui reponde, l'annonce reste affichee tout le temps de la fenetre,
  // et c'est exactement le second temps que la decision 7 reclame.
  const etapeEstAnnonce = etape?.etat === 'annonce'
  const cartoucheAJour =
    termine ||
    partieFinie ||
    etapesAffichees.length === 0 ||
    (surLaDerniereEtape && (etapeValidee || (etapeEstAnnonce && !questionAuJoueur)))

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
      // Le cartouche est replie devant une question du moteur : il n'a plus de
      // bouton, il n'a donc plus de touche non plus. Entree appartient a la
      // question, et Echap ne doit pas demander de derouler une phase que le
      // moteur ne fait pas avancer tant qu'on ne lui a pas repondu.
      if (questionAuJoueur) return
      // On ecrit peut-etre ailleurs : le tchat est a portee de main pendant la
      // phase, et un espace tape dedans ne doit pas la faire avancer.
      const cible = evenement.target
      if (
        cible instanceof HTMLElement &&
        (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)
      ) {
        return
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
      if (evenement.key === 'Enter' || evenement.key === ' ') {
        evenement.preventDefault()
        avancer()
        return
      }
      if (evenement.key === 'Escape') {
        evenement.preventDefault()
        derouler()
      }
    }
    document.addEventListener('keydown', auClavier)
    return () => document.removeEventListener('keydown', auClavier)
  })

  // Combien de boosts sont deja retournes sur l'etape courante. Ils
  // s'enchainent SEULS : c'est l'etape qui attend la validation, pas chaque
  // carte. Une attaque a trois boosts couterait sinon quatre clics.
  const [boostsMontres, setBoostsMontres] = useState(0)

  useEffect(() => {
    setBoostsMontres(etape?.boosts.length ? 1 : 0)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `etape` est
    // reconstruit a chaque trame du moteur (meme piege que dans
    // useDerouleScene.ts et TraitCible.tsx) : en dependre remettrait
    // `boostsMontres` a 1 en boucle et aucun boost ne s'enchainerait jamais. `etape?.cle` identifie l'etape, et
    // `etape?.boosts.length` reagit si son compte de boosts change.
  }, [etape?.cle, etape?.boosts.length])

  useEffect(() => {
    const total = etape?.boosts.length ?? 0
    if (boostsMontres === 0 || boostsMontres >= total) return
    const minuteur = window.setTimeout(
      () => setBoostsMontres((n) => n + 1),
      DELAI_BOOST_MS
    )
    return () => window.clearTimeout(minuteur)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- meme raison :
    // `etape?.cle` et `etape?.boosts.length` suffisent a piloter le
    // minuteur, l'identite de `etape` ne doit pas le redeclencher.
  }, [boostsMontres, etape?.cle, etape?.boosts.length])

  // Le cartouche est-il a l'ecran ? Calcule ICI parce que les hooks ci-dessous
  // en dependent, et que la sortie `return null` qui l'applique vient bien plus
  // bas : un hook place apres elle ferait tomber tout le plateau.
  const visible = Boolean(etape) && !termine && !partieFinie

  // Les etapes qui attendent un VRAI clic, avance auto ou pas : le bilan de
  // fin de phase (le joueur reprend la main, il doit le voir) et la chute
  // d'un heros (le moment le plus important d'une partie ne defile pas). Le
  // bilan se reconnait a son temps : `avecBilan` est le seul a le produire.
  const etapeAttendUnClic = etape?.temps === 'bilan' || Boolean(etape?.defaite)

  // Le delai avant que l'etape courante ne se valide seule, ou `undefined`
  // quand elle attend un clic. Le defilement d'Echap l'emporte sur l'avance
  // auto : il ne lit pas, il fait voir passer.
  const delaiAvant = defilement ? DELAI_DEFILEMENT_MS : avanceAuto ? delaiAvanceMs : undefined

  // L'HORLOGE du cartouche, la seule de toute la phase. Elle sert a l'avance
  // auto (delai de lecture) comme au defilement d'Echap (pas de lecture).
  //
  // Un minuteur par etape affichee, nettoye au demontage et a chaque
  // changement d'etape (c'est `etape?.cle` dans les dependances qui le
  // re-arme, pas l'objet `etape`, reconstruit a chaque trame du moteur : en
  // dependre remettrait le minuteur a zero plus vite qu'il n'arrive a
  // echeance, et rien n'avancerait jamais). Sans ce nettoyage, deux minuteurs
  // se superposeraient et une etape serait sautee.
  //
  // Aucun minuteur :
  //  - sans avance auto ni defilement, evidemment ;
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

  // Mise en scene de l'etape courante. Appele ici, avec les autres hooks :
  // ce composant a un `return null` plus bas, et un hook place apres lui fait
  // tomber tout le plateau (React compte alors un hook de plus au rendu
  // suivant).
  useDerouleScene(etape, visible)

  // OU SE TIENT LE CARTOUCHE : a droite de la main, dans la colonne du
  // journal, le bas au bas du journal.
  //
  // Trois choses qu'il ne doit JAMAIS recouvrir, meme replie : la main du
  // joueur, le panneau central ou le moteur pose ses questions, et la carte
  // que la mise en scene agrandit. Mesures faites en partie (fenetre de
  // 1920 x 889, table a l'echelle 0,814 ; les rangees de la grille font alors
  // 183 px, voir board.css `.plateau-scene`) :
  //
  //  - la main (`.zone-main`, rangee du bas, colonne centrale) : 623 a 806 de
  //    haut, 133 a 1468 de large ;
  //  - le panneau central (`.demande-centrale`, 660 px de large, centre a 45 %
  //    de la hauteur) : 334 a 466 de haut, 630 a 1290 de large ;
  //  - la carte agrandie (x 2,36 sur place) : le vilain, rangee 1, deborde de
  //    0 a 320 ; un sbire, rangee 2, de 169 a 511 ; une manigance annexe
  //    revelee, calee en haut de la colonne de droite, de 202 a 445. Toutes
  //    s'arretent au-dessus de 583 ;
  //  - le journal (`.journal-heros`, rangee du bas, colonne de droite) : 623 a
  //    806 de haut, 1600 a 1912 de large. Il n'est pas une zone de cartes, et
  //    pendant la phase du mechant c'est le cartouche qui raconte ce qu'il
  //    ecrit.
  //
  // Un cartouche de 223 px de haut (sa hauteur courante) pose au bas du
  // journal occupe donc 583 a 806 de haut et 1478 a 1912 de large : a droite
  // de la main (1468 + 10 de jour), sous tout ce que la mise en scene
  // agrandit, loin du panneau central. La colonne centrale, elle, ne pouvait
  // pas tenir ces trois contraintes : entre le panneau (466) et la main (623)
  // il reste 157 px, et le cartouche en demande 223. C'est ce qui l'avait
  // pose SUR la question du moteur quand on l'a remonte au-dessus de la main.
  //
  // AU-DESSUS du journal (rangees 2-3 de la colonne de droite) aurait ete
  // pire : c'est la zone des manigances annexes, ou une carte revelee peut
  // etre agrandie par la mise en scene, sous le cartouche.
  //
  // On ne pose rien en dur : on lit la position REELLE de la main et du
  // journal. Ce sont deux cases de la grille de la scene, donc leurs boites ne
  // bougent ni avec le nombre de cartes (rognees a l'interieur) ni avec la
  // taille de l'ecran (la scene se met a l'echelle, et le rect suit). Le
  // cartouche prend toute la largeur entre le bord droit de la main et le bord
  // droit du journal : 434 px sur la mesure ci-dessus, et il retrecit avec la
  // table sur un ecran plus petit (sa chronologie passe alors a la ligne).
  // C'est la meme facon de lire le plateau que `useDerouleScene` et
  // `placement/boites`.
  //
  // Main ou journal introuvable (plateau mobile, plateau pas encore monte) :
  // on ne devine pas une geometrie absente, les variables sont retirees et le
  // CSS reprend son repli.
  useLayoutEffect(() => {
    const corps = document.body
    const oublier = () => {
      corps.style.removeProperty(VARIABLE_GAUCHE)
      corps.style.removeProperty(VARIABLE_LARGEUR)
      corps.style.removeProperty(VARIABLE_BAS)
      corps.style.removeProperty(VARIABLE_DECALAGE)
    }
    if (!visible) {
      oublier()
      return
    }
    const mesurer = () => {
      const main = document.querySelector('.plateau-scene .zone-main')
      const journal = document.querySelector('.plateau-scene .journal-heros')
      if (!main || !journal) {
        oublier()
        return
      }
      const boiteMain = main.getBoundingClientRect()
      const boiteJournal = journal.getBoundingClientRect()
      // Boite vide : la mise en page n'a pas encore eu lieu (ou l'on est dans
      // un environnement sans mise en page). Une mesure fausse serait pire que
      // pas de mesure du tout.
      if (boiteMain.height === 0 || boiteJournal.height === 0 || boiteJournal.width === 0) {
        oublier()
        return
      }
      const gauche = Math.round(boiteMain.right + ECART_MAIN)
      const largeur = Math.round(boiteJournal.right) - gauche
      const bas = Math.round(window.innerHeight - boiteJournal.bottom)
      if (largeur <= 0) {
        oublier()
        return
      }
      corps.style.setProperty(VARIABLE_GAUCHE, `${gauche}px`)
      corps.style.setProperty(VARIABLE_LARGEUR, `${largeur}px`)
      corps.style.setProperty(VARIABLE_BAS, `${Math.max(bas, BAS_MINIMUM)}px`)
      // Le repli du CSS centre le cartouche par une translation de -50 % : une
      // fois ancre par `left`, cette translation doit tomber.
      corps.style.setProperty(VARIABLE_DECALAGE, '0px')
    }
    mesurer()
    // La scene se remet a l'echelle a chaque redimensionnement : la main et le
    // journal changent alors de place, et le cartouche doit les suivre.
    window.addEventListener('resize', mesurer)
    return () => {
      window.removeEventListener('resize', mesurer)
      oublier()
    }
  }, [visible])

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
  if (!etape || termine || partieFinie) return null

  // Position du temps COURANT dans la chronologie : elle seule dit qui est
  // deja passe. Calculee une fois pour les cinq temps, pas a chaque `<li>`.
  //
  // Un temps absent de la chronologie (le bilan) compte comme place APRES tous
  // les autres : sur la derniere etape, les cinq temps s'affichent alors tous
  // valides, ce qui est exactement ce qui vient de se passer. Sans cela, le
  // `-1` rendu par findIndex n'en aurait marque aucun.
  const trouve = TEMPS.findIndex((item) => item.cle === etape.temps)
  const positionCourante = trouve === -1 ? TEMPS.length : trouve

  // « 1 sur 3 » : combien d'etapes ce temps compte, et ou l'on en est.
  // `undefined` quand il n'en compte qu'une, et rien ne s'affiche alors.
  const rang = rangDansLeTemps(etapesAffichees, index)
  const resultat = resultatEtape(etape)
  const compteur = compteurEtape(etape)
  const regle = regleEtape(etape)
  const annulee = texteActivationAnnulee(etape)

  // La chronologie des cinq temps : la seule chose que le cartouche garde
  // quand il se replie devant une question du moteur.
  const chronologie = (
    <ol className="deroule-temps">
      {TEMPS.map((temps, position) => {
        // Un temps se juge par rapport au temps COURANT, celui de l'etape
        // affichee, et par rapport a lui seul :
        //  - avant lui et sans etape : VIDE (barre, « aucun »). Il n'a coute
        //    aucun clic (etapesDeroule ne cree pas de placeholder pour lui),
        //    le joueur doit seulement voir qu'il a ete saute, et pourquoi ;
        //  - avant lui avec des etapes : passe, coche ;
        //  - lui : mis en avant ;
        //  - apres lui : A VENIR, jamais vide, quel que soit le nombre
        //    d'etapes connues. Constate en partie : le moteur demandait dans
        //    quel ordre activer DEUX sbires, dont les faits n'existaient donc
        //    pas encore, et la chronologie affichait « Sbires (aucun) »
        //    barre. La marque etait prematuree et disait le contraire de la
        //    verite.
        // Sur le bilan, tous les temps sont passes (`positionCourante` vaut
        // alors TEMPS.length) : ceux sans etape sont vides, c'est exact.
        const estCourant = temps.cle === etape.temps
        const estAvant = !estCourant && position < positionCourante
        const aDesEtapes = etapesAffichees.some((e) => e.temps === temps.cle)
        const estVide = estAvant && !aDesEtapes
        const estPasse = estAvant && aDesEtapes
        const classe = estVide ? 'est-vide' : estCourant ? 'est-courant' : estPasse ? 'est-passe' : ''
        return (
          <li key={temps.cle} className={classe}>
            {t(temps.libelle)}
            {/* Motif deja utilise pour « Fin du tour » (board.tsx) : un
                symbole colle au texte, pas une traduction a part. */}
            {estPasse ? ' ✓' : null}
            {estVide ? <span className="deroule-temps-vide-detail"> ({t('Aucun')})</span> : null}
          </li>
        )
      })}
    </ol>
  )

  // Le moteur pose une question au joueur : le cartouche s'efface devant
  // elle. Ni titre, ni bouton, ni « La suite arrive… » (ce serait un
  // mensonge : c'est le moteur qui attend). La chronologie reste, pour que le
  // joueur sache toujours ou il en est, et la mention dit qui attend qui.
  if (questionAuJoueur) {
    return (
      <>
        <TraitCible etape={etape} actif={!termine} />
        <section className="deroule-phase est-replie" role="dialog" aria-label={t('Phase du méchant')}>
          <div className="deroule-chrono">{chronologie}</div>
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
              <p className="deroule-titre">{titreEtape(etape)}</p>
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
        </section>
      </>
    )
  }

  return (
    <>
      <TraitCible etape={etape} actif={!termine} />
      <section className="deroule-phase" role="dialog" aria-label={t('Phase du méchant')}>
        <div className="deroule-chrono">
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

        {/* Le titre dit le fait, et le compteur de la cible se lit a sa
            droite. Un titre generique suivi de la meme chose en dessous
            faisait dire une seule chose a trois lignes. */}
        <div className="deroule-entete">
          {/* Le bilan porte le meme titre que les autres etapes, en capitales :
              il annonce la fin de la phase, pas un coup de plus. */}
          <p className={`deroule-titre${etape.temps === 'bilan' ? ' est-bilan' : ''}`}>
            {titreEtape(etape)}
          </p>
          {compteur ? <span className="deroule-compteur">{compteur}</span> : null}
        </div>
        {resultat ? <p className="deroule-resultat">{resultat}</p> : null}
        {/* L'activation annoncee qui n'a pas lieu. Sans cette ligne, l'etape
            resterait sur « Klaw va attaquer Colossus » et le joueur
            attendrait un coup qui ne vient pas. */}
        {annulee ? <p className="deroule-annulee">{annulee}</p> : null}
        {/* La chute du heros. Elle ne ressemble a aucune autre ligne du
            cartouche, et c'est voulu : c'est le moment le plus important d'une
            partie, il ne doit pas defiler comme les autres. Le crane est
            decoratif (aria-hidden) : la phrase dit deja tout, et un lecteur
            d'ecran n'a pas a epeler un symbole. */}
        {etape.defaite ? (
          <p className="deroule-defaite">
            <span aria-hidden="true">☠</span> {texteDefaite(etape)}
          </p>
        ) : null}
        {etape.boosts.length > 0 ? (
          <ul className="deroule-boosts">
            {etape.boosts.slice(0, boostsMontres).map((boost) => (
              <li key={boost.cle}>
                <b>{boost.nom}</b>
                <span>+{boost.apport}</span>
              </li>
            ))}
          </ul>
        ) : null}
        {/* Le bilan de fin de phase : ce que le joueur vient d'encaisser, en
            deux lignes, au moment ou il decide de son tour. Une liste VIDE
            n'est pas une absence : elle dit que la phase n'a rien coute, et le
            cartouche le dit plutot que de rester muet. */}
        {etape.bilan ? (
          <ul className="deroule-bilan">
            {etape.bilan.length === 0 ? (
              <li className="deroule-bilan-rien">{texteBilanVide()}</li>
            ) : (
              etape.bilan.map((ligne) => (
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
        {regle ? (
          <div className="deroule-regle">
            {/* Vrai bouton, pas un <span> cliquable : atteignable au Tab et a
                Entree/Espace nativement, et `aria-expanded` annonce l'etat au
                lecteur d'ecran. Meme motif que `.recap-mechant-repli`
                (RecapPhaseMechant.tsx), le seul autre dépliant du plateau. */}
            <button
              type="button"
              className="deroule-regle-bouton"
              aria-expanded={regleDepliee}
              onClick={basculerRegle}
            >
              <span aria-hidden="true">{regleDepliee ? '▾' : '▸'}</span> {t('la règle')}
            </button>
            {regleDepliee ? <p className="deroule-regle-texte">{regle}</p> : null}
          </div>
        ) : null}
        <div className="deroule-boutons">
          {/* Dire qu'on attend, sans rien bloquer : une mention grise a cote du
              bouton, qui reste cliquable. Ni modale ni bouton desactive, parce
              que l'attente dure une fraction de seconde en temps normal et
              qu'un bouton qui s'eteint puis se rallume attire l'oeil plus que
              l'etape elle-meme. Un reclic pendant l'attente est sans danger :
              il relache au plus une trame de plus.

              Elle ne parle que du MOTEUR qu'on attend. Quand c'est le joueur
              qu'on attend (`questionAuJoueur`), le cartouche est replie plus
              haut et cette ligne n'existe pas : « La suite arrive… » par-dessus
              une question du moteur etait exactement le mensonge constate en
              partie. Le test « ne dit pas La suite arrive… quand c est au
              joueur d agir » le verrouille. */}
          {enAttente ? (
            <span className="deroule-attente" aria-live="polite">
              {t('La suite arrive…')}
            </span>
          ) : null}
          {/* Dit pourquoi il n'y a plus rien apres, a la place meme ou l'on
              lit d'ordinaire « La suite arrive… ». Les deux ne se croisent
              jamais : une defaite ne fait plus attendre de suite. */}
          {etape.defaite ? <span className="deroule-arret">{texteArretDefaite()}</span> : null}
          {index > 0 ? (
            <button type="button" className="bh-bouton" onClick={reculer}>
              {t('Précédent')}
            </button>
          ) : null}
          {/* Sur le bilan, le bouton ne dit plus « Suivant » : il n'y a plus
              rien apres, et c'est lui qui rend la main au joueur. Sur une
              defaite, il dit « Continuer » : ce n'est pas une etape de plus
              qu'on demande, c'est le droit de reprendre la partie. */}
          <button type="button" className="bh-bouton deroule-suivant" onClick={avancer}>
            {etape.defaite
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
