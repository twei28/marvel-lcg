// La phase du mechant, decoupee en ETAPES a valider une par une.
//
// Deux sources, et aucune n'est une relecture du monde :
//
// 1. `FaitMechant` : les activations que le moteur a deja resolues. Lui seul
//    connait la composition d'un coup (base, boost, defense) ; une deduction
//    verrait le resultat sans jamais pouvoir dire « 5 = 3 + 2 », et compterait
//    plusieurs fois ce que le moteur rend plusieurs fois autour d'une seule
//    resolution.
// 2. Les entrees du journal, pour ce que les faits ne couvrent pas : la menace
//    posee, les cartes revelees.
//
// Ce module est PUR : aucun DOM, aucune traduction. Il rend des cles de texte
// que le composant met en langue. C'est ce qui le rend testable sans navigateur
// et verifiable dans les deux langues.

import type { EntreeHistorique } from './HistoriquePartie'
import type { FaitMechant } from './world'

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
 * Phase du moteur -> temps de la carte de reference, pour les entrees dont le
 * temps ne depend pas de l'auteur (menace, distribution, revelation).
 *
 * « Enemy Activation » n'y figure PAS : le vilain et ses sbires s'activent
 * tous les deux pendant cette meme phase moteur, donc son temps ('mechant' ou
 * 'sbires') se decide sur l'AUTEUR du fait, pas sur son nom de phase. Voir
 * `etapesDeroule`.
 */
const TEMPS_PAR_PHASE: Record<string, TempsPhase> = {
  'Main Scheme Place Threat': 'menace',
  'Deal Encounter Cards': 'distribution',
  'Reveal Encounter Cards': 'revelation',
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
 * Sa propre forme, distincte de `consequences` : une consequence est un texte
 * deja redige, alors qu'une ligne de bilan porte des NOMBRES, que le bilan
 * additionne et que l'affichage met en langue au dernier moment.
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
  /** Son seuil, quand elle en a un (la menace maximale d'une manigance). */
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
  /** Cible de l'action, pour le trait de la livraison 2. */
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
  consequences: { cle: string; texte: string }[]
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
  return phase ? TEMPS_PAR_PHASE[phase] : undefined
}

/**
 * Les etapes de la phase, dans l'ordre de la carte de reference.
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
 *   aucun nom d'auteur.
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
  const duRound = [...entrees.filter((e) => e.round === round)].reverse()

  // Meme filtre que ci-dessus, mais sur les FAITS : sans lui, un fait du
  // round precedent restait affiche pendant le tour du joueur suivant, avant
  // de ressurgir a la vraie phase du mechant du round 2 (defaut constate en
  // partie reelle). Un fait SANS round_id (moteur ou sauvegarde anterieurs a
  // ce champ) est GARDE quel que soit le round demande : mieux vaut une etape
  // de trop qu'un deroule muet.
  const faitsDuRound = faits.filter((f) => f.round_id === undefined || f.round_id === round)

  const menace = duRound.filter(
    (e) => tempsDe(e.phase) === 'menace' && e.type === 'threat'
  )
  // Une etape PAR manigance touchee. Une seule etape suivie de la liste de ses
  // consequences disait deux fois la meme chose : « Menace sur la manigance
  // principale », puis « L'Effraction ! gagne 2 menaces ». Le fait tient en
  // une phrase, et chaque manigance a son propre compteur.
  for (const e of menace) {
    etapes.push({
      cle: `menace:${e.cle}`,
      temps: 'menace',
      titre: 'menace',
      regle: 'regle:menace',
      // Le nom NU de la carte, que l'entree porte deja a cote de sa phrase
      // (voir EntreeHistorique.nomCarte) : le decouper du titre traduit
      // marcherait dans une langue sur deux.
      cibleNom: e.nomCarte,
      // `valeur` est la variation SIGNEE du compteur : seule une POSE de
      // menace se met en phrase ici. Un retrait, qui n'a pas lieu a ce temps
      // de la phase, laisserait « gagne -1 menaces » ; sans montant, le titre
      // se replie sur sa formule generique.
      montant: e.valeur !== undefined && e.valeur > 0 ? e.valeur : undefined,
      restant: e.restant,
      plafond: e.plafond,
      boosts: [],
      consequences: [],
    })
  }

  faitsDuRound.forEach((fait, index) => {
    // Une phase deja connue (distribution, revelation) garde son temps
    // propre. Sinon, c'est une activation ordinaire : son temps depend de
    // l'AUTEUR du coup, pas de son nom de phase, puisque le vilain et ses
    // sbires s'activent tous deux pendant « Enemy Activation ».
    const temps = tempsDe(fait.phase) ?? (mechantIds.has(fait.auteur_id) ? 'mechant' : 'sbires')
    // `restant` vaut `null` quand la cible n'a pas de compteur : on le ramene a
    // l'absence, seul etat que l'affichage sait taire.
    const restant = fait.restant ?? undefined
    // Les deux accords exiges par `EtapeDeroule.defaite`, et rien de moins.
    const defaite = restant !== undefined && restant <= 0 && herosVaincusIds.has(fait.cible_id)
    etapes.push({
      cle: `fait:${index}:${fait.auteur_id}`,
      temps,
      titre: fait.genre === 'attaque' ? 'attaque' : 'manigance',
      regle: temps === 'mechant' || temps === 'sbires' ? 'regle:activations' : 'regle:revelation',
      carteId: fait.auteur_id,
      cibleId: fait.cible_id,
      // Nettoyage applique partout ailleurs sur les noms de heros (icones,
      // symboles) : sans lui, le deroule affichait des prefixes que personne
      // d'autre n'affiche.
      auteurNom: fait.auteur.replace(/^\W*/, ''),
      cibleNom: fait.cible.replace(/^\W*/, ''),
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
      consequences: [],
    })
  })

  // Les cartes revelees, que les faits du moteur ne couvrent pas : lui ne rend
  // que les activations resolues.
  //
  // Cote moteur, la carte quitte le paquet de rencontre AU MOMENT OU ELLE EST
  // DISTRIBUEE (`encounter_deck -> dealt_encounter_cards`), donc c'est LA que
  // le journal note « revelee », sous la phase 'Deal Encounter Cards' (temps
  // 'distribution'). Le passage suivant, de la main du joueur vers la zone
  // commune de revelation (`Reveal Encounter Cards`), ne change plus rien que
  // ce module puisse observer : les deux zones sont deja « en jeu ». Se
  // limiter au seul temps 'revelation' aurait donc laisse ce temps muet en
  // partie reelle (aucune carte n'y arrive jamais) : on accepte les DEUX
  // phases, et on les affiche toutes comme des revelations, ce qui
  // correspond a ce que le joueur voit vraiment (le nom de la carte, des
  // qu'elle quitte le paquet). Voir le rapport de la tache pour la mesure qui
  // etablit ce point.
  //
  // Les entrees de type `text` (narration technique du moteur, defausses,
  // fins d'activation, « DiscardPile<3> ») ne produisent PLUS d'etape ici :
  // constate en partie, 8 etapes de ce genre sur 12, en anglais et
  // illisibles, noyaient les quatre etapes utiles. Elles restent entieres
  // dans le journal a droite et dans le Log, qui les affichent deja.
  const cartesRevelees = duRound.filter(
    (e) =>
      e.type === 'card' &&
      (tempsDe(e.phase) === 'revelation' || tempsDe(e.phase) === 'distribution')
  )

  // Regle officielle : chaque joueur revele et resout sa carte DANS L'ORDRE
  // DU TOUR, en commencant par le premier joueur. `cartesRevelees` arrive
  // dans l'ordre chronologique du journal (voir `duRound` plus haut), pas
  // forcement celui du tour : on la retrie avant de construire les etapes,
  // et le tri final sur `ORDRE` (stable) preserve ensuite cet ordre relatif.
  for (const e of trierParOrdreDuTour(cartesRevelees, premierJoueurId, nomsHerosParJoueur.length)) {
    etapes.push({
      cle: `carte:${e.cle}`,
      temps: 'revelation',
      titre: 'revelation',
      regle: 'regle:revelation',
      carteId: e.cibleId,
      // Nettoyage identique a celui des faits plus haut : le moteur prefixe
      // les identites d'un marqueur decoratif que le plateau retire partout
      // ailleurs.
      auteurNom: nomHerosNettoye(nomsHerosParJoueur[e.joueur ?? -1]),
      // Le nom NU de la carte (voir `cibleNom` de l'etape de menace, meme
      // raison) : `titre` n'est plus une phrase toute faite, `titreEtape` la
      // construit a partir de `auteurNom` et `cibleNom`.
      cibleNom: e.nomCarte,
      boosts: [],
      consequences: [],
    })
  }

  return etapes.sort((a, b) => ORDRE.indexOf(a.temps) - ORDRE.indexOf(b.temps))
}

/**
 * Nettoyage du nom d'un heros, identique a celui applique aux faits du
 * mechant (`fait.auteur.replace(...)`) : le moteur prefixe les identites d'un
 * marqueur decoratif que le plateau retire partout ailleurs (icones,
 * symboles).
 */
function nomHerosNettoye(nom: string | undefined): string | undefined {
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
 */
export function lignesBilan(etapes: EtapeDeroule[]): LigneBilan[] {
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
export function avecBilan(etapes: EtapeDeroule[]): EtapeDeroule[] {
  if (etapes.length === 0) return etapes
  const bilan: EtapeDeroule = {
    cle: 'bilan',
    temps: 'bilan',
    titre: 'bilan',
    // Aucune regle a rappeler : le bilan n'est pas un point de la carte de
    // reference, c'est le compte de ce qui vient de se passer.
    regle: '',
    boosts: [],
    consequences: [],
    bilan: lignesBilan(etapes),
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
