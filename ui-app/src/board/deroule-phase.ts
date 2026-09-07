// La phase du mechant, decoupee en ETAPES a valider une par une.
//
// UNE SEULE SOURCE : `FaitMechant`, le journal que le MOTEUR tient du round en
// cours (`WorldStat.RecordFaitMechant`, cote Python). Il couvre les quatre
// points de la carte de reference — la menace, les activations, la
// distribution, les revelations — et il voyage avec le monde, donc il survit a
// un rechargement de page en pleine phase.
//
// Le journal local (`EntreeHistorique`, reconstruit dans le navigateur en
// comparant deux photos du monde) ne sert plus qu'au REPLI de compatibilite
// decrit dans `etapesDeroule`. C'etait la seconde source, et elle avait une
// autre duree de vie : au premier F5 le cartouche perdait sa menace et ses
// cartes revelees, definitivement (constat F4 de l'audit du 06/09/2026).
//
// Ce module est PUR : aucun DOM, aucune traduction. Il rend des cles de texte
// que le composant met en langue. C'est ce qui le rend testable sans navigateur
// et verifiable dans les deux langues.

import type { EntreeHistorique } from './HistoriquePartie'
import { PHASES_DU_MECHANT_ORDONNEES, type PhaseDuMechant } from './moteur'
import type {
  FaitActivation,
  FaitActivationResolue,
  FaitDistribution,
  FaitMechant,
  FaitMenace,
  FaitRevelation,
} from './world'

export type TempsPhase =
  | 'menace'
  | 'mechant'
  | 'sbires'
  | 'distribution'
  | 'revelation'
  | 'premier-joueur'
  | 'bilan'

/**
 * Ordre des cinq temps de la carte de reference, puis le bilan.
 *
 * `bilan` n'est PAS un temps de la carte de reference : c'est le point final
 * du cartouche, et il vient donc apres tout le reste, quel que soit l'ordre
 * d'arrivee des faits. La chronologie affichee ne le montre pas (elle s'en
 * tient aux cinq temps), elle les montre alors tous valides.
 */
const ORDRE: TempsPhase[] = [
  'menace',
  'mechant',
  'sbires',
  'distribution',
  'revelation',
  'premier-joueur',
  'bilan',
]

/**
 * Phase du moteur -> temps de la carte de reference, pour les faits dont le
 * temps ne depend pas de l'auteur.
 *
 * `undefined` sur « Enemy Activation », et c'est une reponse, pas un trou : le
 * vilain et ses sbires s'activent tous les deux pendant cette meme phase
 * moteur, donc le temps ('mechant' ou 'sbires') se decide sur l'AUTEUR du
 * fait. Voir `etapesDeroule`.
 *
 * Indexe par `PhaseDuMechant` (moteur.ts), donc EXHAUSTIF par construction :
 * une phase ajoutee a la liste unique force une decision ici, au lieu de
 * retomber en silence sur le repli. C'est ce que l'audit F6 reprochait a
 * l'ancienne table, qui n'en connaissait que trois sur quatre.
 */
const TEMPS_PAR_PHASE: Record<PhaseDuMechant, TempsPhase | undefined> = {
  'Main Scheme Place Threat': 'menace',
  'Enemy Activation': undefined,
  'Deal Encounter Cards': 'distribution',
  'Reveal Encounter Cards': 'revelation',
}

/** Les memes cles, pour reconnaitre une phase inconnue sans caster a l'aveugle. */
const PHASES_CONNUES: ReadonlySet<string> = new Set<string>(PHASES_DU_MECHANT_ORDONNEES)

// Gardes de type sur le genre d'un fait. `FaitMechant` est une union discriminee
// (voir world.ts) : sans elles, `fait.montant` ou `fait.carte` ne compilent pas,
// et c'est exactement ce qu'on veut — un genre oublie se voit a la compilation.
export function estActivation(fait: FaitMechant): fait is FaitActivation {
  return fait.genre === 'attaque' || fait.genre === 'manigance'
}
/**
 * Une activation RESOLUE : le coup a eu lieu et le moteur en connait le
 * resultat. Un fait sans `etat` en est une — c'est tout ce que le moteur
 * savait produire avant les deux temps, et c'est ce que les sauvegardes
 * anterieures portent.
 */
export function estResolue(fait: FaitActivation): fait is FaitActivationResolue {
  return fait.etat === undefined || fait.etat === 'resolu'
}
function estMenace(fait: FaitMechant): fait is FaitMenace {
  return fait.genre === 'menace'
}
function estDistribution(fait: FaitMechant): fait is FaitDistribution {
  return fait.genre === 'distribution'
}
function estRevelation(fait: FaitMechant): fait is FaitRevelation {
  return fait.genre === 'revelation'
}

/**
 * Un fait accompagne de son RANG dans `faits_mechant` du monde.
 *
 * Le rang voyage avec le fait d'un bout a l'autre de `etapesDeroule` parce
 * qu'il fait partie de l'IDENTITE de l'etape (voir `cleDuFait`) : il doit donc
 * survivre aux filtres par genre et aux tris par ordre du tour, qui changent
 * tous deux la position d'un fait sans changer le fait.
 */
type FaitRange<T extends FaitMechant = FaitMechant> = { fait: T; rang: number }

/**
 * L'IDENTITE d'une etape batie sur un fait du moteur : son round, son genre,
 * son rang dans `faits_mechant` du monde, et ce que l'etape vise (une cible,
 * un joueur, une carte).
 *
 * JAMAIS un rang dans un tableau filtre ou retrie, et c'est tout le sujet : le
 * cartouche retient la CLE de l'etape que le joueur lit, pas son numero. Une
 * revelation de plus pour un autre joueur (un Deferlement, par exemple)
 * reordonne la liste ; avec un rang de tableau, la cle de l'etape affichee
 * changeait, son minuteur d'avance repartait, et une etape qui s'inserait en
 * amont faisait reculer le joueur d'un cran (constat F3 de l'audit du
 * 06/09/2026, et Important 3 de la relecture d'A2).
 *
 * Le rang d'origine est stable pendant tout un round : le moteur AJOUTE ses
 * faits en fin de liste et REMPLACE une intention par sa resolution a la meme
 * place (`WorldStat.RecordFaitMechant`, cote Python). Il ne bougerait que sur
 * le garde-fou des 200 faits d'un meme round, qu'aucune partie n'atteint.
 *
 * Le round entre dans la cle parce que le moteur vide `faits_mechant` au
 * premier fait d'un round nouveau : sans lui, les rangs des deux rounds se
 * ressembleraient.
 */
function cleDuFait(genre: string, round: number, rang: number, vise: number | string): string {
  return `${genre}:${round}:${rang}:${vise}`
}

export type BoostDeroule = {
  cle: string
  nom: string
  cibleId: number
  apport: number
}

/**
 * Une ligne du bilan de fin de phase : ce qu'UNE cible a encaisse en tout.
 *
 * Elle porte des NOMBRES, jamais un texte deja redige : le bilan les
 * additionne, et l'affichage les met en langue au dernier moment.
 */
export type LigneBilan = {
  cle: string
  /** Ce que la cible a encaisse : des degats, ou de la menace. */
  genre: 'degats' | 'menaces'
  cibleNom: string
  /** Le total de la phase pour cette cible, toutes sources confondues. */
  total: number
  /** Le compteur de la cible apres le DERNIER coup connu, s'il y en a un. */
  restant?: number
  /**
   * Son seuil, quand il est connu : la menace maximale d'une manigance, qui
   * vient des etapes, ou les PV maximum d'un personnage, que l'appelant
   * fournit (voir `lignesBilan`). Absent des que le seuil n'est pas sur.
   */
  plafond?: number
}

export type EtapeDeroule = {
  /** Identifiant stable, pour la cle React et le « Precedent ». */
  cle: string
  temps: TempsPhase
  /**
   * Cle de texte ('attaque', 'manigance', 'menace') que le composant traduit
   * en phrase, ou titre deja redige repris tel quel du journal (cartes
   * revelees) quand la source n'est pas un fait du moteur.
   */
  titre: string
  /** Rappel de la regle appliquee. */
  regle: string
  /** Carte a mettre en avant sur le plateau. */
  carteId?: number
  /**
   * Cible de l'action, pour le trait de la livraison 2.
   *
   * Peut etre presente SANS `carteId` : l'etape de menace vise une manigance
   * sans avoir d'auteur (c'est une regle du jeu qui pose la menace). La mise en
   * scene met alors la cible elle-meme en avant, faute d'auteur (`sceneDe`).
   */
  cibleId?: number
  /**
   * Noms de l'auteur et de la cible, portes par l'ETAPE elle-meme, pas
   * resolus a l'affichage via l'index du monde courant.
   *
   * `FaitMechant` les porte deja en clair (`auteur`, `cible`) : le moteur les
   * connait au moment du coup. Une carte morte pendant la phase (ex. un
   * minion tue par sa propre cible) a disparu de l'index du monde au moment
   * ou l'etape s'affiche ; y chercher son nom affichait « Ultron attaque #88 »
   * a la place. Meme raison que RecapPhaseMechant, qui fait ce choix pour la
   * meme cause.
   *
   * Sur une etape de revelation, les deux changent de sens : `auteurNom` est
   * le HEROS qui revele (absent si le journal n'a pas pu le rattacher a un
   * joueur, ou si l'appelant n'a pas fourni les noms), `cibleNom` le nom NU
   * de la carte revelee.
   */
  auteurNom?: string
  cibleNom?: string
  /**
   * Le nombre du coup : les degats ou les menaces que la cible a encaisses,
   * les menaces posees pour l'etape de menace.
   *
   * Sur un fait, c'est `subi` et JAMAIS `inflige` : `inflige` est ce qui a ete
   * porte une fois la defense deduite, `subi` ce que la cible a reellement
   * encaisse. Une reduction de degats ou des derniers points de vie depasses
   * separent les deux, et le joueur lit ce qui s'est passe.
   */
  montant?: number
  /**
   * Compteur de la CIBLE apres le coup : ses points de vie restants, ou la
   * menace sur la manigance. Absent quand la source n'en donne pas (le moteur
   * laisse `restant` vide pour une cible qui n'a pas de compteur) : mieux vaut
   * n'afficher aucun compteur qu'un nombre invente.
   */
  restant?: number
  /**
   * Le seuil du compteur, quand la cible en a un : la menace maximale d'une
   * manigance. Les points de vie n'en ont pas, d'ou l'absence frequente.
   */
  plafond?: number
  boosts: BoostDeroule[]
  /**
   * Ou en est une etape d'ACTIVATION, et rien d'autre : les autres temps
   * (menace, distribution, revelation) n'ont qu'un seul etat et n'en portent
   * pas.
   *
   *  - `annonce` : le mechant VA frapper. C'est la fenetre ou le joueur peut
   *    encore defendre ou jouer une interruption. L'etape ne porte alors que
   *    ce qui est connu d'avance (`valeurAnnoncee`), jamais un resultat ;
   *  - `resolu` : le coup a eu lieu, l'etape porte son montant et ses boosts.
   *    La MEME etape, sous la meme cle : elle se complete sous les yeux du
   *    joueur au lieu de le faire reculer ;
   *  - `annule` : l'activation annoncee n'a pas eu lieu (un « ... instead »
   *    l'a remplacee, la cible a quitte la table). Sans cet etat, le cartouche
   *    resterait sur « va attaquer » jusqu'a la fin de la phase.
   */
  etat?: 'annonce' | 'resolu' | 'annule'
  /**
   * La valeur IMPRIMEE annoncee, avant boosts et avant defense. Portee par les
   * seules etapes d'activation annoncees ou annulees : sur une resolution,
   * c'est `montant` qui dit ce qui a ete encaisse, et afficher les deux
   * ferait lire deux nombres pour un seul coup.
   */
  valeurAnnoncee?: number
  /**
   * Ce coup a mis un HEROS a terre. Absent partout ailleurs, y compris sur
   * l'etape ordinaire qui l'a precede.
   *
   * La marque exige DEUX accords, et jamais un seul :
   *
   * 1. le monde dit ce heros elimine (`WorldPlayer.is_eliminated`, pose par
   *    `Player.Eliminate` cote moteur). C'est l'etat, il ne dit pas QUEL coup ;
   * 2. le fait dit `restant <= 0` (`cible.health` apres coup, cote moteur, et
   *    `IsDefeated()` s'y ramene : `health <= 0`). C'est le coup, il ne dit pas
   *    si la cible est un heros : un sbire abattu tombe lui aussi a zero.
   *
   * L'un sans l'autre marquerait a tort : tous les coups de la phase sur un
   * heros qui finira par tomber, ou chaque sbire mort. Annoncer une defaite qui
   * n'a pas eu lieu serait pire que de ne rien annoncer : c'est le faux positif
   * qui ferait douter le joueur de tout le reste du cartouche.
   */
  defaite?: boolean
  /**
   * Le bilan de la phase, porte par la seule etape de temps `bilan`. Une
   * liste VIDE est un etat legitime, et pas la meme chose qu'un champ absent :
   * elle dit « la phase n'a rien coute », que l'affichage annonce en toutes
   * lettres. Absent sur toutes les autres etapes.
   */
  bilan?: LigneBilan[]
}

function tempsDe(phase: string | undefined): TempsPhase | undefined {
  if (!phase || !PHASES_CONNUES.has(phase)) return undefined
  return TEMPS_PAR_PHASE[phase as PhaseDuMechant]
}

/**
 * Les etapes de la phase, dans l'ordre de la carte de reference.
 *
 * LES CINQ TEMPS VIENNENT DES FAITS DU MOTEUR, et d'eux seuls : la menace du
 * point 1, les activations du point 2, la distribution du point 3, les
 * revelations du point 4. `entrees` (le journal local) n'est plus lu que par le
 * REPLI de compatibilite, decrit dans le corps, et qui disparaitra.
 *
 * Un fait porte SA phase : un vilain qu'une carte revelee fait frapper une
 * seconde fois se range sous la revelation, pas sous mechant ou sbires, sans
 * quoi il paraissait attaquer deux fois sans raison.
 *
 * `mechantIds` distingue le vilain de ses sbires pour les activations
 * ordinaires : `etapesDeroule` ne voit pas le monde, seulement les faits et le
 * journal, donc c'est l'appelant (board.tsx, qui lit `cartesMondeParId`) qui
 * lui dit qui est le camp du vilain. Un auteur absent de l'ensemble (inconnu
 * ou deja hors table) se range sous sbires : c'est le cas le plus frequent, et
 * s'y tromper coute une pastille, pas une regle du jeu.
 *
 * `herosVaincusIds` suit la meme regle, pour la meme raison : ce module ne voit
 * pas le monde, donc c'est board.tsx qui lui donne les cartes d'identite des
 * heros que le monde declare ELIMINES. L'ensemble est optionnel et vide par
 * defaut : sans lui, aucune etape n'est marquee, ce qui est le bon repli (ne
 * rien annoncer plutot qu'annoncer a tort).
 *
 * `premierJoueurId` et `nomsHerosParJoueur` servent l'ordre du tour des
 * revelations (regle officielle : chaque joueur revele dans l'ordre du tour,
 * en commencant par le premier joueur). Meme motif que les deux ensembles
 * ci-dessus : ce module ne voit pas le monde, donc c'est l'appelant qui lui
 * donne ce qu'il faut.
 *
 * - `premierJoueurId` est l'indice de SIEGE (le meme que celui que porte
 *   `EntreeHistorique.joueur`, tous deux venant de `World.players`) du joueur
 *   qui a le jeton de premier joueur ce round. Le monde ne publie pas de
 *   champ dedie a l'ordre des joueurs : le jeton vit comme un COMPTEUR
 *   generique sur l'identite du joueur (`WorldCard.info['k_first_player_token']`,
 *   pose par le moteur des `SetActive()`, cote Python
 *   game/card/face/card_type/identity.py). Absent (aucun joueur ne le
 *   porte : ancien moteur, ou source muette) -> `undefined`, et les
 *   revelations gardent alors l'ordre du journal plutot que d'inventer un
 *   ordre.
 * - `nomsHerosParJoueur` est le nom de heros de chaque joueur, dans le MEME
 *   ordre que `World.players`, brut (prefixe decoratif compris : nettoye ICI,
 *   comme le reste du fichier le fait deja pour `auteurNom`/`cibleNom` des
 *   faits). Vide par defaut : sans lui, une etape de revelation ne porte
 *   aucun nom d'auteur — sauf si le fait en porte un lui-meme, ce qui est
 *   desormais le cas ordinaire (`joueur_nom`).
 */
export function etapesDeroule(
  faits: FaitMechant[],
  entrees: EntreeHistorique[],
  round: number,
  mechantIds: Set<number>,
  herosVaincusIds: Set<number> = new Set(),
  premierJoueurId?: number,
  nomsHerosParJoueur: (string | undefined)[] = []
): EtapeDeroule[] {
  const etapes: EtapeDeroule[] = []

  // `entrees` accumule TOUTE la partie, pas seulement la phase en cours : sans
  // ce filtre sur le round, la phase du round 4 faisait revoir les cartes
  // rencontre des rounds 1 a 3. Et l'historique empile la plus recente EN
  // TETE : sans le `.reverse()`, ces vieilles cartes s'affichaient en plus a
  // l'envers. Meme choix que RecapPhaseMechant.bilanDeLaPhase, qui a le meme
  // besoin.
  //
  // Le journal ne sert plus qu'au REPLI (voir plus bas) : la source ordinaire
  // du cartouche, ce sont les faits.
  const duRound = [...entrees.filter((e) => e.round === round)].reverse()

  // Meme filtre que ci-dessus, mais sur les FAITS : sans lui, un fait du
  // round precedent restait affiche pendant le tour du joueur suivant, avant
  // de ressurgir a la vraie phase du mechant du round 2 (defaut constate en
  // partie reelle). Un fait SANS round_id (moteur ou sauvegarde anterieurs a
  // ce champ) est GARDE quel que soit le round demande : mieux vaut une etape
  // de trop qu'un deroule muet.
  //
  // Chaque fait garde son RANG D'ORIGINE dans `faits_mechant` (voir
  // `cleDuFait`) : c'est de lui que vient l'identite des etapes, et il ne doit
  // donc jamais etre celui d'un tableau filtre ou retrie.
  const faitsDuRound = faits
    .map((fait, rang) => ({ fait, rang }))
    .filter(({ fait }) => fait.round_id === undefined || fait.round_id === round)

  const faitsMenace = faitsDuRound.filter(
    (porte): porte is FaitRange<FaitMenace> => estMenace(porte.fait)
  )
  const faitsDistribution = faitsDuRound.filter(
    (porte): porte is FaitRange<FaitDistribution> => estDistribution(porte.fait)
  )
  const faitsRevelation = faitsDuRound.filter(
    (porte): porte is FaitRange<FaitRevelation> => estRevelation(porte.fait)
  )

  // ------------------------------------------------------------------ REPLI
  //
  // Un moteur pas encore mis a jour, ou une sauvegarde plus ancienne, ne porte
  // AUCUN fait de ces trois genres : le cartouche se retrouverait sans menace,
  // sans distribution et sans revelation, c'est a dire quasiment vide. On
  // relit alors le journal local, exactement comme avant, et pour ce genre-la
  // seulement.
  //
  // Le critere est « aucun fait de ce genre POUR CE ROUND », et pas « le monde
  // vient d'un vieux moteur » : on ne sait pas distinguer les deux, et cette
  // formulation-ci se referme d'elle-meme des que le premier fait arrive. Une
  // phase qui n'a legitimement pose aucune menace (escalade nulle) lit donc le
  // journal, qui n'en trouve pas davantage : meme resultat, aucun etat faux.
  //
  // ⚠ CE REPLI EST TEMPORAIRE. Il disparaitra quand tous les moteurs en
  // service auront ces faits ; il ne reste que le temps de la transition, et
  // rien de neuf ne doit s'appuyer dessus.
  const repliMenace = faitsMenace.length === 0
  const repliCartes = faitsDistribution.length === 0 && faitsRevelation.length === 0

  // ---------------------------------------------------------- POINT 1 : menace
  //
  // Une etape PAR manigance touchee. Une seule etape suivie d'une liste disait
  // deux fois la meme chose : « Menace sur la manigance principale », puis
  // « L'Effraction ! gagne 2 menaces ». Le fait tient en une phrase, et chaque
  // manigance a son propre compteur.
  for (const { fait, rang } of faitsMenace) {
    etapes.push({
      cle: cleDuFait('menace', fait.round_id ?? round, rang, fait.cible_id),
      temps: 'menace',
      titre: 'menace',
      regle: 'regle:menace',
      // Pas de `carteId` : la menace est une REGLE du jeu, aucun personnage ne
      // l'inflige, donc il n'y a ni auteur a mettre en avant ni trait a
      // tracer. `cibleId` suffit a la mise en scene (`sceneDe`), qui agrandit
      // alors la manigance dont on parle.
      cibleId: fait.cible_id,
      cibleNom: nomNettoye(fait.cible),
      // Une pose de zero ne se met pas en phrase (« gagne 0 menaces ») : sans
      // montant, le titre se replie sur sa formule generique.
      montant: fait.montant > 0 ? fait.montant : undefined,
      restant: fait.restant ?? undefined,
      plafond: fait.plafond ?? undefined,
      boosts: [],
    })
  }

  if (repliMenace) {
    for (const e of duRound.filter((e) => tempsDe(e.phase) === 'menace' && e.type === 'threat')) {
      etapes.push({
        cle: `menace:${e.cle}`,
        temps: 'menace',
        titre: 'menace',
        regle: 'regle:menace',
        // Le nom NU de la carte, que l'entree porte deja a cote de sa phrase
        // (voir EntreeHistorique.nomCarte) : le decouper du titre traduit
        // marcherait dans une langue sur deux.
        cibleNom: e.nomCarte,
        cibleId: e.cibleId,
        // `valeur` est la variation SIGNEE du compteur : seule une POSE de
        // menace se met en phrase ici. Un retrait, qui n'a pas lieu a ce temps
        // de la phase, laisserait « gagne -1 menaces ».
        montant: e.valeur !== undefined && e.valeur > 0 ? e.valeur : undefined,
        restant: e.restant,
        plafond: e.plafond,
        boosts: [],
      })
    }
  }

  // --------------------------------------------------- POINT 2 : activations
  //
  // Le rang parcourt TOUS les faits du monde, genres nouveaux compris : la cle
  // d'une activation ne change donc pas selon ce que la phase a produit par
  // ailleurs.
  faitsDuRound.forEach(({ fait, rang }) => {
    if (!estActivation(fait)) return
    // Une phase deja connue (distribution, revelation) garde son temps
    // propre. Sinon, c'est une activation ordinaire : son temps depend de
    // l'AUTEUR du coup, pas de son nom de phase, puisque le vilain et ses
    // sbires s'activent tous deux pendant « Enemy Activation ».
    const temps = tempsDe(fait.phase) ?? (mechantIds.has(fait.auteur_id) ? 'mechant' : 'sbires')
    // L'IDENTITE de l'etape. Elle vient de l'identifiant d'activation quand le
    // moteur en donne un : c'est ce qui permet a l'intention et a sa
    // resolution d'etre LA MEME etape, qui se complete sous les yeux du
    // joueur. Sans identifiant (moteur ou sauvegarde anterieurs), on garde
    // l'ancienne identite pour ne rien casser de ce qui existe deja.
    const cle =
      fait.activation_id !== undefined
        ? `activation:${fait.activation_id}`
        : `fait:${rang}:${fait.auteur_id}`
    const commun = {
      cle,
      temps,
      titre: fait.genre === 'attaque' ? 'attaque' : 'manigance',
      regle: temps === 'mechant' || temps === 'sbires' ? 'regle:activations' : 'regle:revelation',
      carteId: fait.auteur_id,
      cibleId: fait.cible_id,
      // Nettoyage applique partout ailleurs sur les noms de heros (icones,
      // symboles) : sans lui, le deroule affichait des prefixes que personne
      // d'autre n'affiche.
      auteurNom: nomNettoye(fait.auteur),
      cibleNom: nomNettoye(fait.cible),
    }

    // L'INTENTION (ou son annulation) : le coup n'a pas eu lieu, et l'etape ne
    // doit donc porter AUCUN resultat. Pas de montant, pas de compteur, pas de
    // boost (les cartes ne sont meme pas retournees), et surtout pas de
    // defaite : rien n'a encore ete subi.
    if (!estResolue(fait)) {
      etapes.push({
        ...commun,
        etat: fait.etat,
        valeurAnnoncee: fait.base,
        boosts: [],
      })
      return
    }

    // `restant` vaut `null` quand la cible n'a pas de compteur : on le ramene a
    // l'absence, seul etat que l'affichage sait taire.
    const restant = fait.restant ?? undefined
    // Les deux accords exiges par `EtapeDeroule.defaite`, et rien de moins.
    const defaite = restant !== undefined && restant <= 0 && herosVaincusIds.has(fait.cible_id)
    etapes.push({
      ...commun,
      etat: 'resolu',
      // `subi` et non `inflige` : voir le commentaire de `montant`.
      montant: fait.subi,
      restant,
      // Absent, et non `false`, sur une etape ordinaire : le champ ne parait
      // que la ou il dit quelque chose.
      defaite: defaite ? true : undefined,
      boosts: fait.boosts.map((boost, rang) => ({
        cle: `boost:${rang}:${boost.id}`,
        nom: boost.nom,
        cibleId: boost.id,
        apport: boost.apport,
      })),
    })
  })

  // ---------------------------------------------------- POINT 3 : distribution
  //
  // Ce temps etait STRUCTURELLEMENT toujours vide (constat M3 de l'audit) :
  // rien ne le renseignait, et la chronologie affichait « DISTRIBUTION (Aucun) »
  // barre a presque toutes les phases de toutes les parties. Le joueur
  // apprenait a ignorer un cinquieme du fil de progression.
  //
  // Le moteur ordonne deja ses distributions par tour de table, mais le tri
  // s'applique quand meme : il est stable, il ne coute rien, et il tient si la
  // source change d'ordre.
  for (const { fait, rang } of trierParOrdreDuTour(
    faitsDistribution.map(({ fait, rang }) => ({ fait, rang, joueur: fait.joueur ?? undefined })),
    premierJoueurId,
    nomsHerosParJoueur.length
  )) {
    etapes.push({
      cle: cleDuFait('distribution', fait.round_id ?? round, rang, fait.joueur ?? -1),
      temps: 'distribution',
      titre: 'distribution',
      regle: 'regle:distribution',
      // Le heros qui recoit. Le nom du FAIT d'abord : il date du moment de la
      // distribution, donc il tient meme si le joueur a depuis change de forme
      // ou quitte la table. L'index du monde ne sert que de repli.
      auteurNom: nomNettoye(fait.joueur_nom ?? undefined)
        ?? nomNettoye(nomsHerosParJoueur[fait.joueur ?? -1]),
      // Pas de carte : elle est FACE CACHEE, et la nommer ici revelerait au
      // joueur ce que la regle lui cache jusqu'au point 4.
      boosts: [],
    })
  }

  // ----------------------------------------------------- POINT 4 : revelations
  //
  // Regle officielle : chaque joueur revele et resout sa carte DANS L'ORDRE
  // DU TOUR, en commencant par le premier joueur.
  for (const { fait, rang } of trierParOrdreDuTour(
    faitsRevelation.map(({ fait, rang }) => ({ fait, rang, joueur: fait.joueur ?? undefined })),
    premierJoueurId,
    nomsHerosParJoueur.length
  )) {
    etapes.push({
      cle: cleDuFait('revelation', fait.round_id ?? round, rang, fait.carte_id),
      temps: 'revelation',
      titre: 'revelation',
      regle: 'regle:revelation',
      carteId: fait.carte_id,
      auteurNom: nomNettoye(fait.joueur_nom ?? undefined)
        ?? nomNettoye(nomsHerosParJoueur[fait.joueur ?? -1]),
      cibleNom: fait.carte,
      boosts: [],
    })
  }

  if (repliCartes) {
    // Ancien chemin, garde le temps de la transition (voir le REPLI ci-dessus).
    //
    // Cote moteur, la carte quitte le paquet de rencontre AU MOMENT OU ELLE
    // EST DISTRIBUEE (`encounter_deck -> dealt_encounter_cards`), donc c'est LA
    // que le journal local note « revelee », sous la phase 'Deal Encounter
    // Cards' (temps 'distribution'). Le passage suivant, vers la zone commune
    // de revelation, ne change plus rien qu'il puisse observer : les deux
    // zones sont deja « en jeu ». Se limiter au seul temps 'revelation' aurait
    // donc laisse ce temps muet en partie reelle : on accepte les DEUX phases,
    // et on les affiche toutes comme des revelations.
    //
    // Les entrees de type `text` (narration technique du moteur, defausses,
    // « DiscardPile<3> ») ne produisent PAS d'etape : constate en partie,
    // 8 etapes de ce genre sur 12, en anglais et illisibles, noyaient les
    // quatre etapes utiles. Elles restent entieres dans le journal a droite.
    const cartesRevelees = duRound.filter(
      (e) =>
        e.type === 'card' &&
        (tempsDe(e.phase) === 'revelation' || tempsDe(e.phase) === 'distribution')
    )
    for (const e of trierParOrdreDuTour(cartesRevelees, premierJoueurId, nomsHerosParJoueur.length)) {
      etapes.push({
        cle: `carte:${e.cle}`,
        temps: 'revelation',
        titre: 'revelation',
        regle: 'regle:revelation',
        carteId: e.cibleId,
        auteurNom: nomNettoye(nomsHerosParJoueur[e.joueur ?? -1]),
        cibleNom: e.nomCarte,
        boosts: [],
      })
    }
  }

  return etapes.sort((a, b) => ORDRE.indexOf(a.temps) - ORDRE.indexOf(b.temps))
}

/**
 * Nettoyage du nom d'une carte : le moteur prefixe les identites d'un marqueur
 * decoratif (« * Doctor Doom ») que le plateau retire partout ailleurs (icones,
 * symboles).
 *
 * Exportee parce que le nom nettoye sert de CLE hors de ce module : le bilan de
 * fin de phase regroupe ses lignes sur lui, et board.tsx doit nettoyer de la
 * meme facon les noms qu'il releve sur le monde, sans quoi aucune cle ne se
 * retrouverait. Une seule regle, a un seul endroit.
 */
export function nomNettoye(nom: string | undefined): string | undefined {
  return nom ? nom.replace(/^\W*/, '') : undefined
}

/**
 * Trie une liste d'entrees rattachees a un joueur (`joueur`, un indice de
 * siege) dans l'ordre du tour a partir du premier joueur.
 *
 * Sans premier joueur connu, ou a moins de deux joueurs (solo, ou source
 * muette sur leur nombre), la liste ressort INCHANGEE : le solo ne doit rien
 * voir bouger, et un ordre invente serait pire que l'ordre du journal (voir
 * le rapport de la tache).
 *
 * Le tri est STABLE (`Array.prototype.sort`) : deux entrees du meme joueur,
 * ou toutes deux sans joueur connu, gardent leur ordre d'arrivee entre elles.
 */
function trierParOrdreDuTour<T extends { joueur?: number }>(
  entrees: T[],
  premierJoueurId: number | undefined,
  nbJoueurs: number
): T[] {
  if (premierJoueurId === undefined || nbJoueurs < 2) return entrees
  // Une entree sans joueur connu se range apres tout le monde plutot que de
  // fausser l'ordre des autres (rang hors plage, jamais atteint sinon).
  const rang = (joueur: number | undefined): number =>
    joueur === undefined ? nbJoueurs : (joueur - premierJoueurId + nbJoueurs) % nbJoueurs
  return [...entrees].sort((a, b) => rang(a.joueur) - rang(b.joueur))
}

/**
 * Rang de l'etape courante DANS SON TEMPS, et nombre d'etapes de ce temps.
 *
 * Rend `undefined` quand le temps n'en compte qu'une : « 1 sur 1 » n'apprend
 * rien et encombre un cartouche qui tient en quatre lignes. Le joueur doit
 * savoir combien il lui en reste dans ce temps, pas lire un compteur inutile.
 *
 * Le rang se compte par les etapes qui PRECEDENT l'index, pas par un
 * `indexOf` : deux etapes peuvent etre egales sans etre le meme objet.
 */
export function rangDansLeTemps(
  etapes: EtapeDeroule[],
  index: number
): { rang: number; total: number } | undefined {
  const etape = etapes[index]
  if (!etape) return undefined
  const total = etapes.filter((e) => e.temps === etape.temps).length
  if (total < 2) return undefined
  const rang = etapes.slice(0, index + 1).filter((e) => e.temps === etape.temps).length
  return { rang, total }
}

/**
 * Le genre de compteur qu'une etape fait bouger, d'apres sa cle de titre.
 * Un titre libre (carte revelee) n'y figure pas : il ne compte rien.
 */
const GENRE_PAR_TITRE: Record<string, 'degats' | 'menaces'> = {
  attaque: 'degats',
  manigance: 'menaces',
  menace: 'menaces',
}

/**
 * Le bilan de la phase : une ligne par cible touchee, avec son TOTAL.
 *
 * Les totaux se lisent sur les etapes, qui tiennent elles-memes leurs nombres
 * des faits du moteur et des entrees de menace (voir l'en-tete de ce
 * module) : jamais en comparant deux photos du monde. Une comparaison voit le
 * resultat sans sa composition, et compte plusieurs fois ce que le moteur rend
 * plusieurs fois autour d'une seule resolution. RecapPhaseMechant a tranche la
 * meme question dans le meme sens.
 *
 * GROUPE, et c'est tout l'interet : si le vilain et deux sbires frappent le
 * meme heros, cela fait UNE ligne « Colossus a pris 6 degats », pas trois. Le
 * regroupement se fait sur le NOM de la cible plutot que sur son identifiant,
 * parce que la menace posee au point 1 vient du journal (qui donne un nom, pas
 * d'identifiant) et qu'une manigance du meme temps vient d'un fait : sur
 * l'identifiant, la meme manigance ressortirait sur deux lignes. Deux cibles
 * distinctes ne partagent pas un nom sur une table.
 *
 * Le compteur retenu est celui du DERNIER coup connu pour cette cible : les
 * etapes arrivent dans l'ordre du jeu, c'est donc l'etat le plus recent.
 *
 * `pvMaxParNom` donne les PV MAXIMUM des personnages, par nom nettoye (voir
 * `nomNettoye`), pour que le bilan dise « 8/14 » et plus seulement « 8 ». Il
 * vient de l'appelant parce qu'il n'est nulle part dans les sources de ce
 * module : le moteur ne publie pas les PV maximum a cote de ses faits (voir
 * `FaitMechant`), seul le monde les connait. Absent, ou muet sur une cible : le
 * restant s'affiche seul, comme avant. Un plafond invente serait pire qu'un
 * chiffre nu.
 */
export function lignesBilan(
  etapes: EtapeDeroule[],
  pvMaxParNom?: Map<string, number>
): LigneBilan[] {
  const lignes = new Map<string, LigneBilan>()

  for (const etape of etapes) {
    if (etape.temps === 'bilan') continue
    const genre = GENRE_PAR_TITRE[etape.titre]
    if (!genre) continue
    // Sans montant, rien a additionner ; un montant negatif ou nul n'est pas
    // un coup encaisse (un retrait de menace n'a pas sa place dans un bilan
    // de ce que la phase a coute).
    if (etape.montant === undefined || etape.montant <= 0) continue
    const nom = etape.cibleNom ?? ''
    if (!nom) continue

    const cle = `${genre}:${nom}`
    const deja = lignes.get(cle)
    if (deja) {
      deja.total += etape.montant
      // On ne remplace un compteur deja connu que par un compteur connu : une
      // etape qui n'en porte pas ne doit pas effacer celui de la precedente.
      if (etape.restant !== undefined) deja.restant = etape.restant
      if (etape.plafond !== undefined) deja.plafond = etape.plafond
      continue
    }
    lignes.set(cle, {
      cle,
      genre,
      cibleNom: nom,
      total: etape.montant,
      restant: etape.restant,
      plafond: etape.plafond,
    })
  }

  // Les PV maximum en dernier, et seulement la ou les etapes n'ont rien dit :
  // une manigance porte deja son seuil (`plafond`, venu de son entree de
  // journal), et ce seuil-la fait foi puisqu'il date du coup lui-meme.
  for (const ligne of lignes.values()) {
    if (ligne.genre !== 'degats' || ligne.plafond !== undefined) continue
    const max = pvMaxParNom?.get(ligne.cibleNom)
    if (max !== undefined && max > 0) ligne.plafond = max
  }

  return [...lignes.values()]
}

/**
 * Les etapes suivies de leur bilan, TOUJOURS en dernier.
 *
 * Ce module ne sait pas si la phase est finie : il ne voit ni le monde ni la
 * phase du moteur. C'est l'appelant qui decide d'ajouter le bilan ou non
 * (DeroulePhase, sur `phaseMechantEnCours`), et c'est voulu : un bilan affiche
 * au milieu de la phase mentirait sur ce qu'elle a coute.
 *
 * Une liste vide reste vide : hors phase du mechant, le cartouche ne doit
 * annoncer la fin de rien du tout.
 */
export function avecBilan(
  etapes: EtapeDeroule[],
  pvMaxParNom?: Map<string, number>
): EtapeDeroule[] {
  if (etapes.length === 0) return etapes
  const bilan: EtapeDeroule = {
    cle: 'bilan',
    temps: 'bilan',
    titre: 'bilan',
    // Aucune regle a rappeler : le bilan n'est pas un point de la carte de
    // reference, c'est le compte de ce qui vient de se passer.
    regle: '',
    boosts: [],
    bilan: lignesBilan(etapes, pvMaxParNom),
  }
  // Le tri, plutot qu'un simple `push` : `bilan` est le dernier de ORDRE, donc
  // l'etape finit derniere quel que soit l'ordre d'arrivee des faits.
  return [...etapes, bilan].sort((a, b) => ORDRE.indexOf(a.temps) - ORDRE.indexOf(b.temps))
}

/**
 * Le deroule, coupe NET a l'etape ou un heros est tombe.
 *
 * L'etape qui l'a mis a terre reste affichee, marquee ; rien ne s'affiche
 * au-dela, meme si des faits plus tardifs existent (en multijoueur la phase
 * continue pour les autres, et le moteur produit encore des activations). Le
 * cartouche raconte une phase du mechant, et cette phase-la vient de basculer
 * dans autre chose.
 *
 * Cette coupe s'applique APRES `avecBilan`, et c'est ce qui tranche entre les
 * deux : la defaite l'emporte, le bilan de fin de phase ne s'affiche pas
 * derriere elle. Un « voici ce que la phase vous a coute » apres un heros a
 * terre serait un contresens.
 *
 * Rend la liste RECUE quand aucune etape n'est marquee : le cas ordinaire ne
 * doit rien recopier.
 */
export function arreterSurDefaite(etapes: EtapeDeroule[]): EtapeDeroule[] {
  const index = etapes.findIndex((etape) => etape.defaite)
  return index === -1 ? etapes : etapes.slice(0, index + 1)
}
