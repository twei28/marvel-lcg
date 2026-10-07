// CoucheTriche.tsx — tout le mode Bac à sable, en une seule couche.
//
// Le plateau n'a que deux lignes à ajouter : appeler `useTriche(world)` et
// rendre `<CoucheTriche>`. Le clic droit est capté au niveau du DOCUMENT et
// résolu par `data-card-id`, que chaque carte porte déjà — aucune modification
// des composants de carte, aucun accessoire à faire descendre à travers le
// plateau.
//
// Ce regroupement est délibéré : le mode doit pouvoir être remanié ou retiré
// sans laisser de traces éparpillées dans un plateau de 2000 lignes.

import { envoyerMarque } from './manuel/marques'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { catalogueVide, type Catalogue } from './catalogue'
import { scanUrl } from './card-model'
import { t } from './langue'
import { transformDecalage, useGlisserPanneau } from './placement/useGlisserPanneau'
import { CatalogueManuel } from './manuel/CatalogueManuel'
import {
  creerEtatTouches,
  estInclinable,
  estManigance,
  estSansEtat,
  interpreterDoubleClic,
  interpreterTouche,
  natureDe,
  type CibleClavier,
  type GesteClavier,
} from './manuel/clavier'
import { statutsPortes } from './effets-statuts'
import { nomAffiche } from './noms-cartes-fr'
import { FinManuelle } from './manuel/FinManuelle'
import { ChoixCibleAmelioration, type ChoixCible } from './manuel/ChoixCibleAmelioration'
import { ChoixMulligan } from './manuel/ChoixMulligan'
import { gesteDePose } from './manuel/glisser-manuel'
import { carteDeLaTrame, contexteDePose, poserEnJeu, type CibleAmelioration } from './manuel/poser-en-jeu'
import { leMoteurSeTait } from './manuel/mode'
import { peutBouger, proprietaireDe, siegesControles } from './manuel/proprietaire'
import { appuiCompte, issueAppui, type AppuiEnCours } from './manuel/appui-tactile'
import { APPUI_LONG_MS } from './mobile/useAppuiLong'
import { estMultijoueur, estSpectateur } from './moteur'
import { MenuTable } from './manuel/MenuTable'
import { useConfirmation } from './ConfirmationJeu'
import { MenuTriche, type CibleTriche } from './MenuTriche'
import * as triche from './triche'
import type { World, WorldCard } from './world'

/** Une pile ouverte à la consultation. */
export type PileTriche = {
  titre: string
  cartes: WorldCard[]
  /**
   * Pile du joueur : la carte part en main. Sinon, c'est une pile du MONDE
   * (Rencontre...) : ce que devient la carte dépend du CHEMIN qui la prend —
   * voir `agirSurCarte` (clic sur une carte choisie dans la pile ouverte :
   * mise en jeu ou révélée) et `executerGeste`, cas `'piocher'` (chiffre au
   * clavier sur le dessus de la pile, à l'aveugle : zone de résolution,
   * `ProcessingArea`, jamais en jeu directement).
   */
  duJoueur: boolean
  /** Le nom moteur de la pile (`DeckType`), pour pouvoir la mélanger. */
  zone: string
  /** Pile d'un joueur : son siège, sans quoi elle viserait le joueur courant (lot 5). */
  siege?: number
}

type MenuOuvert = { cible: CibleTriche; x: number; y: number }

/**
 * Combien de temps l'avis de refus reste affiché à l'écran (tâche 4 ter).
 *
 * Discret et bref, comme le reste des interventions du mode manuel : ce
 * n'est pas une erreur de l'application, c'est une réponse à un geste — pas
 * de quoi retenir l'écran plus que le temps de le lire.
 */
const DUREE_AVIS_REFUS = 3500

/**
 * Un champ de saisie a le focus : le clavier du mode manuel ne doit pas le
 * mordre. Sans cette garde, taper « 3 » dans une case de recherche infligerait
 * 3 dégâts à la carte survolée par le pointeur.
 */
function estZoneDeSaisie(cible: Element | null): boolean {
  if (!(cible instanceof HTMLElement)) return false
  return cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable
}

/** Parcourt le monde et indexe chaque carte par son identifiant d'objet. */
function indexer(world: World | undefined): Map<number, WorldCard> {
  const index = new Map<number, WorldCard>()
  if (!world) return index
  const parcourir = (valeur: unknown) => {
    if (Array.isArray(valeur)) {
      for (const element of valeur) parcourir(element)
      return
    }
    if (typeof valeur !== 'object' || valeur === null) return
    const objet = valeur as Record<string, unknown>
    if (typeof objet.id === 'number' && typeof objet.card_type === 'string') {
      index.set(objet.id, objet as unknown as WorldCard)
    }
    for (const enfant of Object.values(objet)) parcourir(enfant)
  }
  parcourir(world)
  return index
}

/**
 * Les quatre piles consultables, repérées par la carte qui les REPRÉSENTE à
 * l'écran — c'est-à-dire leur dessus. Un clic droit sur ce dessus doit ouvrir
 * la pile, pas le menu de la carte : sans cette distinction, on ne pourrait
 * jamais atteindre le contenu d'un deck.
 */
function pilesParDessus(
  world: World | undefined,
  joueurId: number
): Map<number, PileTriche> {
  const piles = new Map<number, PileTriche>()
  if (!world) return piles
  const joueur = world.players?.[joueurId]

  const ajouter = (
    cartes: WorldCard[] | undefined,
    titre: string,
    duJoueur: boolean,
    zone: string
  ) => {
    if (!cartes || cartes.length === 0) return
    const dessus = cartes.at(-1)
    if (dessus) piles.set(dessus.id, { titre, cartes, duJoueur, zone, ...(duJoueur ? { siege: joueurId } : {}) })
  }

  ajouter(joueur?.player_deck, t('Deck du héros'), true, 'PlayerDeck')
  ajouter(joueur?.player_discard_pile, t('Pile de défausse'), true, 'DiscardPile')
  ajouter(world.encounter_deck, t('Deck Rencontre'), false, 'EncounterDeck')
  ajouter(world.encounter_discard_pile, t('Défausse Rencontre'), false, 'EncounterDiscardPile')
  return piles
}

/** Une main trop grande à la fin de la phase des héros (F12). */
type Excedent = { siege: number; nombre: number; main: { id: number; nom: string }[] }

export function useTriche(
  world: World | undefined,
  joueurId: number,
  /** Verse l'intervention dans le journal de partie. */
  ajouterAuJournal?: (libelle: string) => void,
  /**
   * Le siège de CET écran (lot 5 du 06/10/2026, question 14). En ligne, il ne
   * bouge que ses cartes ; à une même table, tous les sièges sont à lui.
   * `joueurId`, lui, est le héros AFFICHÉ.
   */
  monSiege: number = joueurId
) {
  // Le menu s'ouvre dans les DEUX modes : bac à sable (on truque une partie
  // qui se joue aux règles) et manuel (il n'y a plus que lui pour jouer).
  //
  // ⚠ `leMoteurSeTait`, PAS `estModeManuel` (tâche 8 bis) : ces gestes ne
  // doivent s'ouvrir qu'une fois la boucle manuelle entrée, jamais pendant la
  // mise en place — le moteur y attend encore de vraies réponses (le
  // mulligan compris), et un menu manuel ouvert par erreur à ce moment-là
  // n'aurait aucune commande légitime à recevoir.
  // ⚠ I2 (revue finale, 20/09/2026) : LE SPECTATEUR N'ARME RIEN. La couche
  // s'armait sur le seul `leMoteurSeTait`, sans aucune garde de siège : dès
  // qu'une table ORDINAIRE passait en pause, celui qui la REGARDE récupérait
  // le clic droit, le clavier et le glisser libre sur la partie des autres,
  // et `/sandbox_command` acceptait ses gestes. `BandeauPause` mis à part
  // (voir sa prop `lectureSeule`), rien ne le couvrait : la CSS du spectateur
  // ne masque que `.board-actions`.
  //
  // ⚠ CE N'EST QUE LA POLITESSE, PAS LA GARANTIE — un raccourci clavier, une
  // console ouverte ou un `curl` en feraient le tour. La garantie est dans le
  // moteur : `SpectateurPeutEcrire` (`web_server.py`) ferme toute route POST
  // à un spectateur, `/manuel_pause` et `/manuel_passer` exigent en plus un
  // siège. Même partage des rôles que `CoucheCurseurs` et `estSpectateur`.
  const regarde = estSpectateur()
  const manuel = !regarde && leMoteurSeTait(world)
  const actif = !regarde && (world?.mode_sandbox === true || manuel)
  const [menu, setMenu] = useState<MenuOuvert | undefined>(undefined)
  const [pile, setPile] = useState<PileTriche | undefined>(undefined)
  // Le menu de la TABLE (tâche 6, ronde de correction 1) : un clic droit hors
  // de toute carte, en mode manuel — c'est une action de table (« Faire
  // apparaître une carte »), pas une action liée à une carte précise. Voir
  // `MenuTable.tsx`.
  const [menuTable, setMenuTable] = useState<{ x: number; y: number } | undefined>(undefined)
  const [interventions, setInterventions] = useState<string[]>([])
  // Question 3 du 06/10/2026 : une amélioration posée sur la table, plusieurs
  // cartes peuvent la recevoir, le joueur choisit.
  const [choixCible, setChoixCible] = useState<ChoixCible | undefined>(undefined)
  const choisirCible = useCallback(
    (sourceId: number, nom: string, cibles: CibleAmelioration[]) => setChoixCible({ sourceId, nom, cibles }),
    []
  )
  const fermerChoixCible = useCallback(() => setChoixCible(undefined), [])

  const index = useMemo(() => (actif ? indexer(world) : new Map()), [actif, world])
  const controles = useMemo(() => siegesControles(world, monSiege, estMultijoueur()), [world, monSiege])
  const touchable = useCallback((id: number) => peutBouger(world, id, controles), [world, controles])
  /**
   * Piocher vers la main de SON propriétaire (lot 5) : en manuel par
   * `MoveTo(..., 'HandsArea', siege)`. `Gain` donne au joueur COURANT
   * (`puzzle.py`), donc chez le mauvais héros dès qu'on est deux. Le bac à
   * sable garde `Gain`, qui suit les règles.
   */
  const versLaMain = useCallback(
    (id: number) =>
      manuel ? triche.deplacerVers(id, 'HandsArea', 'Top', proprietaireDe(world, id) ?? joueurId) : triche.envoyerEnMain(id),
    [manuel, world, joueurId]
  )
  const statuts = useMemo(() => statutsPortes(index), [index])
  // Les cartes EN MAIN, tous joueurs : le double-clic d'OCTGN n'y fait rien
  // (lot 1 du 06/10/2026). Il les retournait en secret, ou inclinait un allié.
  const enMain = useMemo(
    () => new Set((world?.players ?? []).flatMap((joueur) => (joueur.hand_cards ?? []).map((carte) => carte.id))),
    [world]
  )
  const piles = useMemo(
    () => (actif ? pilesParDessus(world, joueurId) : new Map()),
    [actif, world, joueurId]
  )

  const noter = useCallback(
    (libelle: string) => {
      setInterventions((liste) => [...liste, libelle])
      ajouterAuJournal?.(libelle)
    },
    [ajouterAuJournal]
  )

  // Le menu « Random » d'OCTGN : un tirage ne touche pas au moteur, il
  // s'écrit seulement au journal.
  const tirerAuHasard = useCallback(
    (tirage: 'pile-ou-face' | 'nombre' | 'joueur') => {
      if (tirage === 'pile-ou-face') {
        noter(`${t('Pile ou face')} : ${Math.random() < 0.5 ? t('Pile') : t('Face')}`)
        return
      }
      if (tirage === 'nombre') {
        const reponse = window.prompt(t('Jusqu’à quel nombre ?'), '6')
        const maximum = Number(reponse)
        if (!reponse || !Number.isInteger(maximum) || maximum < 1) return
        noter(`${t('Nombre au hasard')} (1-${maximum}) : ${1 + Math.floor(Math.random() * maximum)}`)
        return
      }
      const nombre = Math.max(1, world?.players?.length ?? 1)
      noter(`${t('Joueur au hasard')} : ${t('Joueur')} ${1 + Math.floor(Math.random() * nombre)}`)
    },
    [noter, world]
  )

  // --- Un geste refusé doit se voir, SANS jamais dire l'inverse -------------
  //
  // ÉCART CORRIGÉ (revue, 19/09/2026, ronde 1 de la tâche 4 ter) : la
  // première version écrivait la ligne du geste tout de suite, sur le succès
  // du DÉPÔT HTTP (`reponse.ok`), et une ligne générique séparée
  // (« Geste refusé par la table ») quand le moteur refusait plus tard. Deux
  // lignes qui se contredisaient (l'une dit « fait », l'autre dit « refusé »,
  // sans dire LEQUEL des gestes elle vise), et la route répond « déposé »
  // avant toute exécution : presque aucun refus de RÈGLE ne fait plus échouer
  // le dépôt, donc le marqueur `(refusé)` d'origine ne se déclenchait plus
  // que sur une panne réseau. La marque promise par le brief (« comme les
  // gestes refusés le font déjà ») n'était donc plus fiable pour un vrai
  // refus moteur.
  //
  // Le correctif : ne plus juger sur le dépôt. Un geste déposé avec succès
  // part dans une file d'attente (`enAttenteRef`) et n'écrit sa ligne qu'au
  // PROCHAIN rendu, quand `world.manuel_refus` dit enfin ce qui s'est
  // réellement passé. Un dépôt qui échoue, lui, reste définitif tout de
  // suite : aucun rendu futur ne le concernera jamais.
  // ⚠ I3 (revue finale, 20/09/2026) : `libelles` AU PLURIEL, PAS `libelle`.
  // Un geste composé (le chiffre sur une pile du monde, qui dépose une
  // commande PAR CARTE) doit écrire AUTANT de lignes que de déplacements
  // réels — sinon un seul Ctrl+Z en défait N, et le journal ment sur ce
  // qu'il a fait. Un geste simple porte un tableau à UN élément : c'est le
  // même mécanisme de résolution différée pour les deux, la seule
  // différence est combien de lignes il écrit une fois l'issue connue.
  type GesteEnAttente = { libelles: string[] }
  const enAttenteRef = useRef<GesteEnAttente[]>([])

  const dernierRenduVu = useRef<number | undefined>(undefined)
  const [avisRefus, setAvisRefus] = useState<string | undefined>(undefined)
  const minuteurRefus = useRef<number | undefined>(undefined)

  const confirmer = useConfirmation()
  const afficherBrievement = useCallback((ligne: string) => {
    setAvisRefus(ligne)
    if (minuteurRefus.current !== undefined) window.clearTimeout(minuteurRefus.current)
    minuteurRefus.current = window.setTimeout(() => setAvisRefus(undefined), DUREE_AVIS_REFUS)
  }, [])

  /**
   * Dépose un geste sans écrire sa ligne : voir le commentaire ci-dessus.
   * Utilisé par `executerGeste` (clavier) ci-dessous, et exposé via `couche`
   * pour `MenuTriche` (clic droit) et les actions sur une pile ouverte.
   */
  const emettreGeste = useCallback(
    async (libelle: string, deposer: () => Promise<boolean>) => {
      const depose = await deposer()
      if (!depose) {
        noter(`${libelle} (${t('refusé')})`)
        return
      }
      enAttenteRef.current.push({ libelles: [libelle] })
    },
    [noter]
  )

  // Question 8 du 06/10/2026 : un double-clic sur une carte EN MAIN la pose
  // en jeu selon son type, exactement comme la lâcher sur la table
  // (`gesteDePose`, partagé avec le glisser). Une carte refusée (une
  // ressource...) le dit en bulle, sans rien envoyer.
  const poserDepuisLaMain = useCallback(
    (id: number) => {
      const carte = carteDeLaTrame(world, id)
      const nomDe = (autre: number) => {
        const trouvee = carteDeLaTrame(world, autre)
        return trouvee ? nomAffiche(trouvee) : t('carte')
      }
      const pose = poserEnJeu({ id, type: carte?.card_type ?? '' }, contexteDePose(world, proprietaireDe(world, id) ?? joueurId))
      const decision = gesteDePose(id, pose, { nomDe, emettreGeste, choisirCible })
      if (decision.genre === 'geste') decision.executer()
      else if (decision.genre === 'refus') afficherBrievement(decision.raison)
    },
    [world, joueurId, emettreGeste, choisirCible, afficherBrievement]
  )

  const attacherChoisie = useCallback(
    (cible: CibleAmelioration) => {
      if (!choixCible) return
      const { sourceId, nom } = choixCible
      setChoixCible(undefined)
      void emettreGeste(`${t('Poser en jeu')} : ${nom} (${t('sous')} ${cible.nom})`, () =>
        triche.attacher(sourceId, cible.id)
      )
    },
    [choixCible, emettreGeste]
  )

  // Le menu de la main d'OCTGN (lot 6 du 06/10/2026) : la main du héros
  // affiché, si cet écran a le droit d'y toucher (question 14).
  const mainAffichee = useMemo(
    () =>
      (world?.players?.[joueurId]?.hand_cards ?? [])
        .filter((carte) => touchable(carte.id))
        .map((carte) => ({ id: carte.id, nom: nomAffiche(carte) || `${t('Carte')} ${carte.id}` })),
    [world, joueurId, touchable]
  )
  const [mulliganOuvert, setMulliganOuvert] = useState(false)
  // F12 avec une main trop grande (`doEndHeroPhase` d'OCTGN, lot 6).
  const [excedent, setExcedent] = useState<Excedent | undefined>(undefined)
  const defausserExcedent = useCallback(
    (ids: number[]) => {
      setExcedent(undefined)
      if (ids.length === 0) return
      void emettreGeste(`${t('Défausser l’excédent')} ${ids.length}`, () => triche.defausserPlusieurs(ids))
    },
    [emettreGeste]
  )
  const defausserAuHasard = useCallback(() => {
    if (mainAffichee.length === 0) return
    const carte = mainAffichee[Math.min(mainAffichee.length - 1, Math.floor(Math.random() * mainAffichee.length))]
    void emettreGeste(`${t('Défausser au hasard')} — ${carte.nom}`, () =>
      triche.deplacerVers(carte.id, 'DiscardPile', 'Top', joueurId)
    )
  }, [mainAffichee, emettreGeste, joueurId])
  const confirmerMulligan = useCallback(
    (ids: number[]) => {
      setMulliganOuvert(false)
      if (ids.length === 0) return
      void emettreGeste(`${t('Mulligan')} ${ids.length}`, () => triche.mulligan(ids, joueurId))
    },
    [emettreGeste, joueurId]
  )
  const echangerAvecLeDessus = useCallback(
    (id: number) => {
      const nom = index.get(id)?.name ?? `${t('Carte')} ${id}`
      void emettreGeste(`${t('Échanger avec le dessus du deck')} — ${nom}`, () =>
        triche.echangerAvecLeDessusDuDeck(id, proprietaireDe(world, id) ?? joueurId)
      )
    },
    [index, emettreGeste, world, joueurId]
  )

  // Résout la file au rendu suivant. En manuel, `World.ManualLoop` redessine
  // même quand un geste échoue (voir engine/game/world/world.py), donc ce
  // rendu arrive toujours — pas besoin d'attente supplémentaire. En bac à
  // sable, c'est la partie ELLE-MÊME qui continue de tourner et de redessiner
  // normalement (questions, phases...) : le rendu arrive tout aussi sûrement,
  // juste par un chemin différent.
  //
  // ⚠ RÉGRESSION CORRIGÉE (revue, ronde 2) : cet effet ne tournait qu'en
  // mode manuel (`if (!manuel ...)`), hérité de l'ancien effet qui n'avait de
  // sens qu'à ce mode-là. Mais `emettreGeste` est devenu l'UNIQUE chemin
  // d'écriture au journal pour LES DEUX modes (le bac à sable partage le même
  // menu et les mêmes actions de pile). Résultat : en bac à sable, chaque
  // geste réussi partait dans la file et rien ne l'en sortait plus jamais —
  // un mensonge (l'ancien défaut) échangé contre un silence total (pire).
  // On dépend maintenant de `actif` (bac à sable OU manuel), pas de `manuel`
  // seul : la file se vide dès que cette couche est utilisable, quel que soit
  // le mode qui l'utilise.
  //
  // ⚠ ON DÉPEND DE `world`, PAS DE `world.render_id`/`world.manuel_refus` À
  // PART : ce sont deux champs du MÊME objet, qui change de référence à
  // chaque rendu du monde ; les lister en plus ne fait que répéter la même
  // condition (retour de revue, ronde 1).
  //
  // ⚠ LE MOTIF TECHNIQUE (« KeyError: 'zone inconnue : ...' ») N'EST JAMAIS
  // MONTRÉ TEL QUEL : il s'adresse à qui débogue, pas à qui joue, et il est
  // déjà dans le journal serveur (`Log.Print`, `DrainSandboxCommands`).
  //
  // ⚠ PLUS D'UN GESTE EN ATTENTE AU MÊME RENDU : ON NE DEVINE PAS. Un seul
  // drainage peut regrouper plusieurs commandes
  // (`DrainSandboxCommands`, engine/device/manager/base.py) : un seul rendu
  // peut donc clore plusieurs de nos gestes à la fois, sans dire lesquels ont
  // réussi. Mieux vaut une ligne honnête (« issue inconnue ») qu'une ligne
  // qui invente un succès ou un refus au hasard.
  useEffect(() => {
    if (!actif || !world) return
    if (world.render_id === dernierRenduVu.current) return
    dernierRenduVu.current = world.render_id

    const enAttente = enAttenteRef.current
    if (enAttente.length === 0) return

    if (enAttente.length > 1) {
      const enCours = enAttente.splice(0, enAttente.length)
      for (const { libelles } of enCours) {
        for (const libelle of libelles) noter(`${libelle} (${t('issue inconnue')})`)
      }
      return
    }

    const { libelles } = enAttente.shift() as GesteEnAttente
    // `manuel_refus` est publié sans condition de mode côté moteur (tâche
    // 4 ter) : le bac à sable en profite pareillement. S'il ne l'était un
    // jour QUE pour le manuel, un champ absent/vide ici écrirait quand même
    // la ligne SANS mention de refus plutôt que de ne rien écrire — c'est
    // déjà ce que fait `!!world.manuel_refus` sur un champ `undefined`.
    //
    // ⚠ I3 : LES N LIGNES D'UN MÊME GESTE PARTAGENT LA MÊME ISSUE. Un seul
    // drainage moteur (`DrainSandboxCommands`) exécute les N commandes d'UN
    // SEUL geste ensemble et rend UNE seule erreur pour tout le lot — ce
    // n'est pas l'ambiguïté « deux gestes en vol » ci-dessus (des gestes
    // INDÉPENDANTS, dont on ignore lequel a réussi), donc pas la même
    // réponse : on connaît l'issue, elle s'applique à chaque ligne.
    const refuse = !!world.manuel_refus
    for (const libelle of libelles) {
      const ligne = refuse ? `${libelle} (${t('refusé')})` : libelle
      noter(ligne)
    }
    if (refuse) afficherBrievement(`${libelles[0]}${libelles.length > 1 ? ` (+${libelles.length - 1})` : ''} (${t('refusé')})`)
  }, [actif, world, noter, afficherBrievement])

  useEffect(
    () => () => {
      if (minuteurRefus.current !== undefined) window.clearTimeout(minuteurRefus.current)
    },
    []
  )

  // Le menu d'UNE carte, à une position d'écran : clic droit, appui long,
  // F1, touche Menu, Maj+F10 (lot 6 du 06/10/2026).
  const ouvrirMenuCarte = useCallback(
    (id: number, x: number, y: number) => {
      // Question 14 : la carte d'un autre joueur, en ligne, n'a pas de menu.
      if (!touchable(id)) return
      const pileVisee = piles.get(id)
      if (pileVisee) {
        setPile(pileVisee)
        return
      }
      const carte = index.get(id)
      if (!carte) return
      setMenu({
        cible: {
          id,
          nom: nomAffiche(carte) || `${t('Carte')} ${id}`,
          estManigance: estManigance(carte.card_type),
          estPersonnage: !estSansEtat(carte.card_type),
          // Lot 5 : la pile de joueur visée est celle du propriétaire ; une
          // carte Rencontre va chez le héros affiché.
          siege: manuel ? (proprietaireDe(world, id) ?? joueurId) : undefined,
        },
        x,
        y,
      })
    },
    [touchable, piles, index, manuel, world, joueurId]
  )
  // Dernière position du pointeur : le menu ouvert au clavier s'y pose.
  const dernierPointeur = useRef({ x: 0, y: 0 })

  // L'écoute vit au niveau du document : les cartes portent déjà
  // `data-card-id`, il suffit de remonter depuis la cible du clic.
  useEffect(() => {
    if (!actif) return
    // Rend vrai si le geste a ouvert un menu (le clic droit coupe alors celui
    // du navigateur). Partagée par le clic droit et l'appui long au doigt.
    const ouvrirMenuSous = (cible: HTMLElement | null, x: number, y: number): boolean => {
      const noeud = cible?.closest?.('[data-card-id]') as HTMLElement | null
      if (!noeud) {
        // Clic droit dans le vide : c'est une action de TABLE (« Faire
        // apparaître une carte »), pas une action liée à une carte précise
        // (revue, ronde de correction 1 — le jour où l'on cherche une carte,
        // c'est justement parce qu'il en manque une, on ne doit pas avoir à en
        // viser une pour l'atteindre). Mode manuel uniquement : le bac à
        // sable a un moteur pour distribuer des cartes normalement, il n'a
        // pas besoin de cette échappatoire, et son clic droit dans le vide
        // doit garder son comportement d'avant (rien, menu du navigateur).
        if (manuel) {
          setMenuTable({ x, y })
          return true
        }
        return false
      }
      const id = Number(noeud.getAttribute('data-card-id'))
      if (!Number.isFinite(id)) return false
      ouvrirMenuCarte(id, x, y)
      return true
    }
    const surClicDroit = (evenement: MouseEvent) => {
      if (ouvrirMenuSous(evenement.target as HTMLElement | null, evenement.clientX, evenement.clientY)) {
        evenement.preventDefault()
      }
    }

    // Au doigt (lot 4, question 11) : iPad n'envoie aucun `contextmenu` à
    // l'appui long. Une minuterie tient lieu de clic droit ; un déplacement au
    // delà du seuil du glisser la coupe et laisse le glisser prendre la main.
    let appui: (AppuiEnCours & { cible: HTMLElement | null }) | undefined
    let minuteurAppui: number | undefined
    // Le menu s'ouvre SOUS le doigt : au lever, le navigateur envoie mousedown,
    // mouseup puis click au point de contact, qui déclenchaient l'entrée du menu
    // sous le doigt (« Défausser » : tenir une carte la défaussait, constat du
    // 06/10/2026). Le lever qui suit un menu ouvert par appui long est avalé.
    let leverAAvaler = false
    const oublierAppui = () => {
      if (minuteurAppui !== undefined) window.clearTimeout(minuteurAppui)
      minuteurAppui = undefined
      appui = undefined
    }
    const surAppui = (evenement: PointerEvent) => {
      oublierAppui()
      leverAAvaler = false
      if (!appuiCompte(evenement.pointerType)) return
      const tenu = { x: evenement.clientX, y: evenement.clientY, debut: Date.now(), cible: evenement.target as HTMLElement | null }
      appui = tenu
      minuteurAppui = window.setTimeout(() => {
        minuteurAppui = undefined
        if (appui === tenu && ouvrirMenuSous(tenu.cible, tenu.x, tenu.y)) leverAAvaler = true
        appui = undefined
      }, APPUI_LONG_MS)
    }
    const surDeplacementAppui = (evenement: PointerEvent) => {
      if (appui && issueAppui(appui, Date.now(), evenement.clientX, evenement.clientY) === 'glisser') oublierAppui()
    }

    const surFinDuToucher = (evenement: TouchEvent) => {
      if (leverAAvaler) evenement.preventDefault()
    }
    const surClicApresAppui = (evenement: MouseEvent) => {
      if (!leverAAvaler) return
      leverAAvaler = false
      evenement.preventDefault()
      evenement.stopPropagation()
    }

    document.addEventListener('contextmenu', surClicDroit)
    document.addEventListener('touchend', surFinDuToucher, { capture: true, passive: false })
    document.addEventListener('click', surClicApresAppui, true)
    document.addEventListener('pointerdown', surAppui)
    document.addEventListener('pointermove', surDeplacementAppui)
    document.addEventListener('pointerup', oublierAppui)
    document.addEventListener('pointercancel', oublierAppui)
    return () => {
      oublierAppui()
      document.removeEventListener('contextmenu', surClicDroit)
      document.removeEventListener('touchend', surFinDuToucher, { capture: true })
      document.removeEventListener('click', surClicApresAppui, true)
      document.removeEventListener('pointerdown', surAppui)
      document.removeEventListener('pointermove', surDeplacementAppui)
      document.removeEventListener('pointerup', oublierAppui)
      document.removeEventListener('pointercancel', oublierAppui)
    }
  }, [actif, manuel, ouvrirMenuCarte])

  // Un geste qui touche plusieurs cartes (Ctrl+Q, F12) : une commande par
  // carte, une ligne de journal par carte, un seul bloc en attente (même
  // issue pour toutes, voir plus haut).
  const emettreLot = useCallback(
    async (lignes: { libelle: string; deposer: () => Promise<boolean> }[]) => {
      const libelles: string[] = []
      for (const { libelle, deposer } of lignes) {
        if (await deposer()) libelles.push(libelle)
        else noter(`${libelle} (${t('refusé')})`)
      }
      if (libelles.length > 0) enAttenteRef.current.push({ libelles })
    },
    [noter]
  )

  // Traduit un geste du clavier en appel du canal `triche.ts`. La ligne
  // n'est pas écrite ici : `emettreGeste` la retarde jusqu'au rendu qui
  // connaît l'issue réelle (voir plus haut).
  const executerGeste = useCallback(
    async (geste: GesteClavier) => {
      switch (geste.geste) {
        case 'retourner': {
          const nom = index.get(geste.id)?.name ?? `${t('Carte')} ${geste.id}`
          await emettreGeste(`${t('Retourner')} — ${nom}`, () => triche.retourner(geste.id))
          return
        }
        case 'incliner': {
          const nom = index.get(geste.id)?.name ?? `${t('Carte')} ${geste.id}`
          await emettreGeste(`${t('Incliner')} — ${nom}`, () => triche.incliner(geste.id))
          return
        }
        case 'redresser': {
          const nom = index.get(geste.id)?.name ?? `${t('Carte')} ${geste.id}`
          await emettreGeste(`${t('Redresser')} — ${nom}`, () => triche.redresser(geste.id))
          return
        }
        case 'melanger': {
          const pileVisee = [...piles.values()].find((candidate) => candidate.zone === geste.zone)
          await emettreGeste(`${t('Mélanger')} — ${pileVisee?.titre ?? geste.zone}`, () =>
            triche.melanger(geste.zone, pileVisee?.siege)
          )
          return
        }
        case 'piocher': {
          const pileVisee = [...piles.values()].find((candidate) => candidate.zone === geste.zone)
          // On prend les `nombre` cartes du DESSUS (fin du tableau, voir
          // `pilesParDessus`), dans l'ordre où elles se présentent.
          const cartes = pileVisee ? pileVisee.cartes.slice(-geste.nombre).reverse() : []
          // ⚠ UNE CARTE RENCONTRE NE VA JAMAIS EN MAIN : elle se révèle et se
          // résout, elle ne se garde pas. Sur une pile du JOUEUR (son deck, sa
          // défausse), un chiffre pioche — la carte part en main
          // (`Puzzle.Gain`), c'est le geste normal. Sur une pile du MONDE
          // (deck Rencontre, défausse Rencontre...), la même touche sort les
          // cartes vers la zone de RÉSOLUTION (`ProcessingArea`), où le
          // plateau montre déjà la carte en cours de résolution : elles
          // atterrissent visibles, sur la table, et c'est le joueur qui
          // décide ensuite où les envoyer avec les gestes qu'il a déjà
          // (Déplacer vers, au clic droit). On ne devine pas la suite à sa
          // place.
          // ⚠ PAS DE REPLI SILENCIEUX : si la pile visée n'existe plus (son
          // identifiant a péri entre le survol et la frappe) ou est déjà
          // vide, la boucle ne tourne pas et rien n'a bougé — ce n'est PAS un
          // succès. Sans ce cas de départ, `toutDepose` restait vrai par
          // défaut et le journal affirmait avoir sorti des cartes qui n'ont
          // jamais bougé.
          //
          const libelle = pileVisee?.duJoueur ? t('Piocher') : t('Sortir en résolution')
          // Rien à faire : la pile visée a disparu ou est déjà vide. Ce n'est
          // PAS un succès qui écrirait une ligne mentant sur un déplacement
          // qui n'a jamais eu lieu.
          if (cartes.length === 0) {
            noter(`${libelle} ${geste.nombre} — ${pileVisee?.titre ?? geste.zone} (${t('refusé')})`)
            return
          }
          // ⚠ I3 (revue finale, 20/09/2026) : GESTE COMPOSÉ, N LIGNES DE
          // JOURNAL — UNE PAR CARTE. La version du 19/09/2026 déposait bien
          // une commande par carte, mais n'écrivait qu'une ligne agrégée
          // (« Piocher 3 — Deck Rencontre ») : un seul Ctrl+Z défaisait alors
          // les TROIS déplacements réels, alors que la spec promet
          // « Ctrl+Z, geste par geste ». Chaque carte a désormais sa propre
          // ligne, nommée par SON nom — un journal plus bavard sur un geste
          // rare est le prix accepté.
          //
          // Un dépôt HTTP qui échoue (réseau) reste immédiat pour SA carte
          // seule ; les autres cartes de ce même chiffre continuent leur
          // chemin normalement — voir `emettreGeste` pour ce même principe
          // sur un geste simple.
          const libelles: string[] = []
          for (const carte of cartes) {
            const nom = carte.name || `${t('Carte')} ${carte.id}`
            const description = `${libelle} — ${nom}`
            const depose = pileVisee?.duJoueur
              ? await versLaMain(carte.id)
              : await triche.deplacerVers(carte.id, 'ProcessingArea')
            if (depose) {
              libelles.push(description)
            } else {
              noter(`${description} (${t('refusé')})`)
            }
          }
          // Les cartes réellement déposées partagent UN SEUL bloc en attente
          // (voir plus haut, résolution différée) : un seul drainage moteur
          // les exécute ensemble, elles connaîtront donc la MÊME issue —
          // jamais l'ambiguïté « deux gestes en vol », qui vise des gestes
          // INDÉPENDANTS dont on ignore lequel a réussi.
          if (libelles.length > 0) enAttenteRef.current.push({ libelles })
          return
        }
        case 'statut': {
          const nom = index.get(geste.id)?.name ?? `${t('Carte')} ${geste.id}`
          // Le moteur BASCULE : `interpreterTouche` n'envoie ce geste que
          // quand il change vraiment l'état (pose si absent, retrait si présent).
          const action =
            geste.statut === 'stun' ? triche.assommer : geste.statut === 'confuse' ? triche.rendreConfus : triche.rendreCoriace
          const base =
            geste.statut === 'stun' ? t('Sonné') : geste.statut === 'confuse' ? t('Désorienté') : t('Tenace')
          const libelle = geste.pose ? base : `${base} ${t('retiré')}`
          await emettreGeste(`${libelle} — ${nom}`, () => action(geste.id))
          return
        }
        case 'victoire': {
          const nom = index.get(geste.id)?.name ?? `${t('Carte')} ${geste.id}`
          await emettreGeste(`${t('Pile de victoire')} — ${nom}`, () => triche.deplacerVers(geste.id, 'VictoryDisplay'))
          return
        }
        case 'surligner':
          await envoyerMarque(monSiege, { genre: 'surligner', id: geste.id, couleur: geste.couleur })
          return
        case 'boost': {
          // `villainBoost` d'OCTGN : la carte du dessus du deck Rencontre va
          // FACE CACHÉE à côté du méchant ; deck vidé, la défausse y est
          // remélangée.
          const deck = [...piles.values()].find((candidate) => candidate.zone === 'EncounterDeck')
          const dessus = deck?.cartes.at(-1)?.id
          if (dessus === undefined) {
            noter(`${t('Carte boost')} (${t('refusé')})`)
            afficherBrievement(t('Le deck Rencontre est vide.'))
            return
          }
          await emettreGeste(t('Carte boost'), () => triche.deplacerVers(dessus, 'BoostArea', 'Top', undefined, true))
          if (deck!.cartes.length === 1) {
            await emettreGeste(t('Remélanger la défausse Rencontre dans le deck'), () =>
              triche.remelangerDefausse('EncounterDiscardPile')
            )
          }
          return
        }
        case 'defausser': {
          const carte = index.get(geste.id)
          const nom = carte?.name ?? `${t('Carte')} ${geste.id}`
          const info = (carte?.info ?? {}) as Record<string, number | undefined>
          // `discard` d'OCTGN (actions.py:1013) : une carte Permanente ne se
          // défausse pas.
          if ((info.permanent ?? 0) > 0) {
            noter(`${t('Défausser')} — ${nom} (${t('refusé')})`)
            afficherBrievement(t('Cette carte est Permanente : elle ne se défausse pas.'))
            return
          }
          // Une carte « Victoire X » va à la pile de victoire. OCTGN ne demande
          // rien pour un sbire vaincu (des dégâts, ni menace ni marqueur) ;
          // sinon il demande (actions.py:1029).
          if ((info.victory ?? 0) > 0) {
            const blessee = (info.max_health ?? 0) - (info.health ?? info.max_health ?? 0) > 0
            const versVictoire =
              (blessee && (info.k_threat ?? 0) === 0) ||
              (await confirmer({
                titre: nom,
                texte: t('Cette carte a « Victoire » : la défausser, ou la mettre dans la pile de victoire ?'),
                confirmer: t('Pile de victoire'),
                annuler: t('Défausse'),
              }))
            if (versVictoire) {
              await emettreGeste(`${t('Pile de victoire')} — ${nom}`, () => triche.deplacerVers(geste.id, 'VictoryDisplay'))
              return
            }
          }
          await emettreGeste(`${t('Défausser')} — ${nom}`, () => triche.defausser(geste.id))
          return
        }
        case 'compteur': {
          if (enMain.has(geste.id)) {
            afficherBrievement(t('Une carte en main ne porte pas de compteurs : pose-la en jeu d’abord.'))
            return
          }
          const nom = index.get(geste.id)?.name ?? `${t('Carte')} ${geste.id}`
          const libelle = geste.nombre >= 0 ? t('Ajouter des compteurs') : t('Retirer des compteurs')
          await emettreGeste(`${libelle} ${Math.abs(geste.nombre)} — ${nom}`, () =>
            triche.poserCompteur(geste.id, 'counter', geste.nombre)
          )
          return
        }
        case 'jetons': {
          const nom = index.get(geste.id)?.name ?? `${t('Carte')} ${geste.id}`
          if (geste.nature === 'menace') {
            const libelle = geste.nombre >= 0 ? t('Poser de la menace') : t('Retirer de la menace')
            await emettreGeste(`${libelle} ${Math.abs(geste.nombre)} — ${nom}`, () =>
              triche.poserMenace(geste.id, geste.nombre)
            )
            return
          }
          // Puzzle.Damage ne sait pas soigner avec une valeur négative : le
          // « retirer » passe par Puzzle.Heal, comme le menu. Sur un héros ou
          // un méchant, OCTGN compte les points de vie RESTANTS : « plus »
          // soigne, « moins » blesse. Sur un sbire ou un allié, il compte
          // les dégâts : « plus » blesse.
          const soigne = geste.nature === 'pv' ? geste.nombre >= 0 : geste.nombre < 0
          const libelle = soigne ? t('Soigner') : t('Infliger des dégâts')
          const valeur = Math.abs(geste.nombre)
          await emettreGeste(`${libelle} ${valeur} — ${nom}`, () =>
            soigne ? triche.soigner(geste.id, valeur) : triche.blesser(geste.id, valeur)
          )
          return
        }
        case 'acceleration': {
          const nom = index.get(geste.id)?.name ?? `${t('Carte')} ${geste.id}`
          const libelle = geste.nombre >= 0 ? t('Ajouter de l’accélération') : t('Retirer de l’accélération')
          await emettreGeste(`${libelle} ${Math.abs(geste.nombre)} — ${nom}`, () =>
            triche.poserAcceleration(geste.id, geste.nombre)
          )
          return
        }
        case 'vaincreStade':
          await emettreGeste(t('Vaincre ce stade'), () => triche.avancerLeMechant())
          return
        case 'maniganceTerminee':
          await emettreGeste(t('Manigance terminée'), () => triche.avancerLaManigance())
          return
        // Lot 6 du 06/10/2026 : `drawUnrevealed` d'OCTGN. La carte du dessus
        // part FACE CACHÉE sur la table : à côté de son héros pour une pile de
        // joueur, en zone de résolution pour une pile Rencontre. Le journal ne
        // la nomme pas.
        case 'piocherCache': {
          const pileVisee = [...piles.values()].find((candidate) => candidate.zone === geste.zone)
          const cartes = pileVisee ? pileVisee.cartes.slice(-geste.nombre).reverse() : []
          const libelle = `${t('Piocher face cachée')} — ${pileVisee?.titre ?? geste.zone}`
          if (!pileVisee || cartes.length === 0) {
            noter(`${libelle} (${t('refusé')})`)
            return
          }
          await emettreLot(
            cartes.map((carte: WorldCard) => ({
              libelle,
              deposer: () =>
                pileVisee.duJoueur
                  ? triche.deplacerVers(carte.id, 'PlayerProcessingArea', 'Top', pileVisee.siege, true)
                  : triche.deplacerVers(carte.id, 'ProcessingArea', 'Top', undefined, true),
            }))
          )
          return
        }
        case 'piocherCachePlusieurs': {
          const reponse = window.prompt(t('Combien de cartes ?'), '3')
          const nombre = Number(reponse)
          if (reponse === null || !Number.isInteger(nombre) || nombre < 1) return
          await executerGeste({ geste: 'piocherCache', zone: geste.zone, nombre })
          return
        }
        case 'menuCarte': {
          ouvrirMenuCarte(geste.id, dernierPointeur.current.x, dernierPointeur.current.y)
          return
        }
        // Maj+F1 (`clearMarker` d'OCTGN) : le marqueur NATUREL de la carte
        // revient à zéro. La menace d'une manigance, les dégâts d'un
        // personnage, sinon les compteurs génériques.
        case 'effacerMarqueurs': {
          const carte = index.get(geste.id)
          if (!carte) return
          const nom = carte.name || `${t('Carte')} ${geste.id}`
          const valeur = (cle: string) => {
            const brut = carte.info?.[cle]
            return typeof brut === 'number' ? brut : 0
          }
          const nature = natureDe(carte.card_type)
          if (nature === 'menace') {
            if (valeur('k_threat') === 0) return noter(`${t('Aucun marqueur')} — ${nom}`)
            await emettreGeste(`${t('Effacer la menace')} — ${nom}`, () => triche.fixerMenace(geste.id, 0))
            return
          }
          if (nature === 'pv' || nature === 'degats') {
            const degats = valeur('k_damage')
            if (degats === 0) return noter(`${t('Aucun marqueur')} — ${nom}`)
            await emettreGeste(`${t('Effacer les dégâts')} — ${nom}`, () => triche.soigner(geste.id, degats))
            return
          }
          const compteurs = valeur('c_counter')
          if (compteurs === 0) return noter(`${t('Aucun marqueur')} — ${nom}`)
          await emettreGeste(`${t('Effacer les compteurs')} — ${nom}`, () =>
            triche.poserCompteur(geste.id, 'counter', -compteurs)
          )
          return
        }
        case 'piocherPlusieurs': {
          const reponse = window.prompt(t('Combien de cartes ?'), '3')
          const nombre = Number(reponse)
          if (reponse === null || !Number.isInteger(nombre) || nombre < 1) return
          await executerGeste({ geste: 'piocher', zone: geste.zone, nombre })
          return
        }
        case 'toutRedresser':
        case 'finPhaseHeros': {
          // `doEndHeroPhase` d'OCTGN décible tout le monde en fin de phase des héros.
          if (geste.geste === 'finPhaseHeros') void envoyerMarque(monSiege, { genre: 'decibler', tous: true })
          const lignes: { libelle: string; deposer: () => Promise<boolean> }[] = []
          const excedents: Excedent[] = []
          // Question 7 du 06/10/2026 : pour TOUS les héros de cet écran, comme
          // OCTGN (à une même table, tous ; en ligne, le sien seul).
          for (const siegeDuJoueur of controles) {
            const joueur = world?.players?.[siegeDuJoueur]
            if (!joueur || joueur.is_eliminated) continue
            // Les cartes du joueur seulement (`readyAll` d'OCTGN ignore tout ce
            // qui est Rencontre, méchant ou manigance principale).
            const inclinees = [...(joueur.area_hero ?? []), ...(joueur.allies ?? []), ...(joueur.supports ?? [])].filter(
              (carte) => !carte.is_ready && estInclinable(carte.card_type)
            )
            for (const carte of inclinees) {
              lignes.push({
                libelle: `${t('Redresser')} — ${carte.name || `${t('Carte')} ${carte.id}`}`,
                deposer: () => triche.redresser(carte.id),
              })
            }
            // Fin de la phase des héros : on repioche jusqu'à la taille de main
            // (`doEndHeroPhase`), dans la main de CE joueur (`MoveTo` par siège,
            // jamais `Gain`, qui donne au joueur courant).
            // Lot 6 du 06/10/2026, `doEndHeroPhase` complet : main trop grande,
            // on propose de défausser l'excédent ; sinon le moteur pioche
            // jusqu'à la taille de main en une commande, deck vide remélangé.
            if (geste.geste === 'finPhaseHeros') {
              const enMainJoueur = joueur.hand_cards ?? []
              const taille = joueur.hand_size ?? 0
              if (enMainJoueur.length > taille) {
                excedents.push({
                  siege: siegeDuJoueur,
                  nombre: enMainJoueur.length - taille,
                  main: enMainJoueur.map((carte) => ({ id: carte.id, nom: nomAffiche(carte) || `${t('Carte')} ${carte.id}` })),
                })
              } else if (enMainJoueur.length < taille) {
                lignes.push({
                  libelle: `${t('Piocher jusqu’à la taille de main')} — ${nomAffiche(joueur.area_hero?.[0] ?? ({ name: '' } as WorldCard)) || `${t('Joueur')} ${siegeDuJoueur + 1}`}`,
                  deposer: () => triche.piocherJusquALaMain(siegeDuJoueur),
                })
              }
            }
          }
          if (excedents.length > 0) setExcedent(excedents[0])
          if (lignes.length === 0) {
            if (excedents.length === 0) {
              noter(geste.geste === 'toutRedresser' ? t('Rien à redresser') : t('Rien à redresser ni à piocher'))
            }
            return
          }
          await emettreLot(lignes)
          return
        }
      }
    },
    [index, piles, emettreGeste, emettreLot, noter, world, controles, versLaMain, ouvrirMenuCarte, enMain, afficherBrievement, confirmer]
  )

  // --- Ctrl+Z : annule le dernier geste (tâche 6) ---------------------------
  //
  // La reconstruction moteur (mise en place puis rejeu de tous les gestes
  // moins le dernier) prend une à deux secondes : deux annulations lancées
  // coup sur coup se marcheraient dessus. `enVolRef` empêche tout départ
  // concurrent ; `annulationEnCours` (rendu) dit au joueur que quelque chose
  // se passe pendant l'attente.
  //
  // ⚠ ON IGNORE LA PRESSION SUIVANTE, ON NE LA MET PAS EN FILE — CHOIX
  // DÉLIBÉRÉ (revue, ronde de correction 1) : une file laisserait le joueur
  // empiler cinq Ctrl+Z et regarder sa partie se dérouler à l'envers sans
  // savoir où elle s'arrêtera. Ignorer pendant qu'une annulation est en vol,
  // avec un signe visible que quelque chose se passe (`annulationEnCours`),
  // est le comportement juste : une fois l'annulation en cours terminée, le
  // joueur VOIT le résultat et presse à nouveau s'il en veut une seconde, en
  // connaissance de cause. NE PAS « améliorer » ceci en file d'attente.
  const enVolRef = useRef(false)
  const [annulationEnCours, setAnnulationEnCours] = useState(false)

  const lancerAnnulation = useCallback(() => {
    if (enVolRef.current) return
    enVolRef.current = true
    setAnnulationEnCours(true)
    void triche.annulerDernierGeste().then((reussi) => {
      enVolRef.current = false
      setAnnulationEnCours(false)
      noter(reussi ? t('Dernier geste annulé') : t('Rien à annuler'))
    })
  }, [noter])

  // L'UNIQUE écoute clavier du mode manuel (voir `manuel/clavier.ts`) : ce
  // qu'on fait cent fois par partie doit se faire d'une touche. Un
  // `pointermove` au document retient ce qui est survolé ; `keydown` le
  // traduit en geste via `interpreterTouche`, PURE, puis l'envoie. La tâche 5
  // (glisser-déposer) lira `estToucheEnfoncee` plutôt que de poser sa propre
  // écoute : deux écoutes concurrentes sur les mêmes événements sont une
  // source de bugs d'ordonnancement.
  const survole = useRef<number | undefined>(undefined)
  const etatTouches = useRef(creerEtatTouches()).current

  useEffect(() => {
    if (!manuel) return

    const surPointeur = (evenement: PointerEvent) => {
      const cible = evenement.target as HTMLElement | null
      const noeud = cible?.closest?.('[data-card-id]') as HTMLElement | null
      const id = noeud ? Number(noeud.getAttribute('data-card-id')) : NaN
      survole.current = Number.isFinite(id) ? id : undefined
      dernierPointeur.current = { x: evenement.clientX, y: evenement.clientY }
    }

    const cibleClavier = (id: number): CibleClavier | undefined => {
      // Question 14 : ni touche ni double-clic sur la carte d'un autre joueur.
      if (!touchable(id)) return undefined
      const pileVisee = piles.get(id)
      if (pileVisee) return { genre: 'pile', zone: pileVisee.zone, dessus: id }
      const carte = index.get(id)
      if (!carte) return undefined
      const portes = statuts.get(id) ?? []
      return {
        genre: 'carte',
        id,
        type: carte.card_type,
        prete: carte.is_ready,
        faceVisible: carte.is_face_up,
        statuts: {
          stunned: portes.includes('stunned'),
          confused: portes.includes('confused'),
          tough: portes.includes('tough'),
        },
      }
    }

    const surTouche = (evenement: KeyboardEvent) => {
      etatTouches.enregistrer(evenement)
      // Ctrl+Z : AVANT la garde des modificateurs juste en dessous, sinon
      // elle l'avale comme n'importe quel autre Ctrl+lettre — et ON
      // `preventDefault` ici : on remplace volontairement l'annulation du
      // navigateur, qui n'a aucun sens sur un plateau de jeu. La garde du
      // FOCUS reste prioritaire : dans un champ de texte, Ctrl+Z est
      // l'annulation de SA saisie, pas la nôtre.
      if (
        evenement.ctrlKey &&
        !evenement.metaKey &&
        !evenement.altKey &&
        evenement.key.toLowerCase() === 'z' &&
        !estZoneDeSaisie(document.activeElement)
      ) {
        evenement.preventDefault()
        lancerAnnulation()
        return
      }
      // Ctrl/Cmd/Alt : raccourcis du NAVIGATEUR (Ctrl+R recharge, Ctrl+1..9
      // change d'onglet). Seules les combinaisons d'OCTGN passent, et le
      // navigateur ne perd la sienne (`preventDefault`) que si le geste
      // s'applique : sinon Ctrl+F ouvre bien la recherche.
      if (evenement.metaKey) return
      // Une saisie de texte en cours : le chiffre tapé est un chiffre, pas un
      // geste de jeu.
      if (estZoneDeSaisie(document.activeElement)) return
      // Les gestes de TABLE d'OCTGN (Alt+Entrée, Ctrl+Q, F12) n'ont besoin de
      // rien sous le pointeur.
      const cle = evenement.key.toLowerCase()
      // Échap : `clearTargets` d'OCTGN, mes cibles et mes flèches. Pas quand une
      // fenêtre ou un menu est ouvert : Échap le ferme d'abord (catalogue, fin).
      if (
        cle === 'escape' &&
        !evenement.ctrlKey &&
        !evenement.altKey &&
        // Les volets latéraux (aide, journal) restent ouverts en jouant : ce ne sont pas des fenêtres.
        !document.querySelector('[role="dialog"]:not(.volet-aide):not(.volet-journal), [role="menu"]')
      ) {
        void envoyerMarque(monSiege, { genre: 'decibler' })
        return
      }
      const geste_de_table =
        (evenement.altKey && !evenement.ctrlKey && cle === 'enter') ||
        (evenement.ctrlKey && !evenement.altKey && !evenement.shiftKey && cle === 'q') ||
        (!evenement.ctrlKey && !evenement.altKey && cle === 'f12')
      if (survole.current === undefined && !geste_de_table) return
      const cible = survole.current === undefined ? undefined : cibleClavier(survole.current)
      if (!cible && !geste_de_table) return
      const geste = interpreterTouche(
        { cle: evenement.key, majuscule: evenement.shiftKey, ctrl: evenement.ctrlKey, alt: evenement.altKey, code: evenement.code },
        cible ?? { genre: 'pile', zone: '' }
      )
      if (!geste) return
      evenement.preventDefault()
      void executerGeste(geste)
    }

    // Double-clic d'OCTGN (`defaultCardAction`) : une carte face cachée se
    // retourne ; sur le méchant, il sort la carte du dessus du deck Rencontre
    // (l'amplification) ; sur un héros, un allié, une amélioration ou un
    // soutien, il s'incline ou se redresse. Une pile ou une manigance : rien.
    const surDoubleClic = (evenement: MouseEvent) => {
      if (estZoneDeSaisie(document.activeElement)) return
      const noeud = (evenement.target as HTMLElement | null)?.closest?.('[data-card-id]')
      const id = noeud ? Number(noeud.getAttribute('data-card-id')) : NaN
      if (!Number.isFinite(id) || piles.has(id)) return
      if (!touchable(id)) return
      if (enMain.has(id)) {
        poserDepuisLaMain(id)
        return
      }
      const cible = cibleClavier(id)
      if (!cible || cible.genre !== 'carte') return
      const geste = interpreterDoubleClic(cible)
      if (geste) void executerGeste(geste)
    }

    const surRelachement = (evenement: KeyboardEvent) => etatTouches.enregistrer(evenement)

    document.addEventListener('pointermove', surPointeur)
    document.addEventListener('keydown', surTouche)
    document.addEventListener('keyup', surRelachement)
    document.addEventListener('dblclick', surDoubleClic)
    return () => {
      document.removeEventListener('dblclick', surDoubleClic)
      document.removeEventListener('pointermove', surPointeur)
      document.removeEventListener('keydown', surTouche)
      document.removeEventListener('keyup', surRelachement)
    }
  }, [manuel, index, piles, enMain, statuts, executerGeste, etatTouches, lancerAnnulation, poserDepuisLaMain, touchable])

  return {
    actif,
    manuel,
    interventions,
    couche: {
      menu,
      pile,
      setMenu,
      setPile,
      emettreGeste,
      executerGeste,
      tirerAuHasard,
      avisRefus,
      annulationEnCours,
      menuTable,
      setMenuTable,
      choixCible,
      choisirCible,
      attacherChoisie,
      fermerChoixCible,
      estEnMain: (id: number) => enMain.has(id),
      poserDepuisLaMain,
      versLaMain,
      mainAffichee,
      mulliganOuvert,
      setMulliganOuvert,
      excedent,
      setExcedent,
      defausserExcedent,
      defausserAuHasard,
      confirmerMulligan,
      echangerAvecLeDessus,
    },
    /** Pour la tâche 5 (glisser-déposer) : lire l'état sans poser d'écoute. */
    estToucheEnfoncee: etatTouches.estEnfoncee,
    /** Le Ctrl+Z du manuel, pour « ↶ Annuler » et U (lot 1, 06/10/2026). */
    annulerDernierGeste: lancerAnnulation,
  }
}

export type CoucheTricheProps = {
  actif: boolean
  /** Bac à sable ou manuel ? Décide seulement de l'affichage du bandeau. */
  manuel: boolean
  couche: ReturnType<typeof useTriche>['couche']
  /**
   * Optionnel : les appelants existants (tests) ne le fournissent pas
   * toujours. Sans lui, la recherche du catalogue (tâche 6) ne trouve
   * simplement jamais rien — rien ne casse.
   */
  catalogue?: Catalogue
}

export function CoucheTriche({ actif, manuel, couche, catalogue = catalogueVide }: CoucheTricheProps) {
  const {
    menu,
    pile,
    setMenu,
    setPile,
    emettreGeste,
    executerGeste,
    tirerAuHasard,
    avisRefus,
    annulationEnCours,
    menuTable,
    setMenuTable,
    choixCible,
    attacherChoisie,
    fermerChoixCible,
    estEnMain,
    poserDepuisLaMain,
    versLaMain,
    mainAffichee,
    mulliganOuvert,
    setMulliganOuvert,
    excedent,
    setExcedent,
    defausserExcedent,
    defausserAuHasard,
    confirmerMulligan,
    echangerAvecLeDessus,
  } = couche
  // Le catalogue (tâche 6) : une carte qui n'était pas dans la partie. Mode
  // manuel uniquement, ouvert depuis le menu de la TABLE (clic droit hors de
  // toute carte — voir `MenuTable.tsx` et le menu plus bas).
  // Déclarer la fin (tâche 7) : même origine que le catalogue, le menu de la
  // TABLE. `FinManuelle` tient déjà sa propre confirmation ; `onDeclarer`
  // n'est donc appelé qu'une fois la décision prise, jamais au premier clic.
  const [catalogueOuvert, setCatalogueOuvert] = useState(false)
  const [finOuverte, setFinOuverte] = useState(false)
  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »).
  const { decalage: decalageFin, gestes: gestesGlisserFin } = useGlisserPanneau(
    finOuverte ? 'fin-ouverte' : 'fin-fermee'
  )
  const { decalage: decalagePile, gestes: gestesGlisserPile } = useGlisserPanneau(pile?.titre ?? 'aucune-pile')

  // Échap ferme le catalogue et la fenêtre de fin de partie, comme les deux
  // menus le font déjà (`MenuTriche.tsx`, `MenuTable.tsx`) — défaut relevé
  // en revue finale (20/09/2026) : ces deux fenêtres ne se fermaient
  // qu'au clic sur « Fermer » ou en dehors du voile.
  useEffect(() => {
    if (!catalogueOuvert && !finOuverte) return
    const surEchap = (evenement: KeyboardEvent) => {
      if (evenement.key !== 'Escape') return
      setCatalogueOuvert(false)
      setFinOuverte(false)
    }
    document.addEventListener('keydown', surEchap)
    return () => document.removeEventListener('keydown', surEchap)
  }, [catalogueOuvert, finOuverte])

  // C : chercher une carte dans TOUT le catalogue (celle qu'on veut poser n'est
  // pas dans la partie). Indépendant de la carte survolée, d'où cet effet à
  // part de l'écoute des gestes. Ctrl/Cmd/Alt et les champs de texte restent
  // au navigateur.
  useEffect(() => {
    if (!manuel) return
    const surC = (evenement: KeyboardEvent) => {
      if (evenement.key.toLowerCase() !== 'c') return
      if (evenement.ctrlKey || evenement.metaKey || evenement.altKey || evenement.shiftKey) return
      if (estZoneDeSaisie(document.activeElement)) return
      evenement.preventDefault()
      setCatalogueOuvert(true)
    }
    document.addEventListener('keydown', surC)
    return () => document.removeEventListener('keydown', surC)
  }, [manuel])

  if (!actif) return null

  // Passe par `emettreGeste`, comme tout autre geste (revue de la tâche) : un
  // refus doit se voir exactement de la même façon, jamais un succès muet ni
  // inventé. La fermeture du panneau, elle, n'attend pas ce rendu — la partie
  // finie s'affiche par-dessus de toute façon (`EcranFinPartie`, `board.tsx`),
  // il n'y a plus rien à re-choisir derrière.
  const declarerFin = async (gagne: boolean) => {
    setFinOuverte(false)
    await emettreGeste(gagne ? t('Fin de partie — Victoire') : t('Fin de partie — Défaite'), () =>
      triche.declarerFin(gagne)
    )
  }

  // ⚠ LE NOM TRANSITE AVEC L'IDENTIFIANT (revue, ronde de correction 1) : le
  // journal existe pour qu'on relise une partie des jours après, souvent
  // quelqu'un d'autre — un card_id nu (« 45017 ») ne dit rien à personne.
  const faireApparaitre = async (cardId: string, nom: string) => {
    await emettreGeste(`${t('Faire apparaître')} — ${nom}`, () => triche.creerCarte(cardId))
    setCatalogueOuvert(false)
  }

  const agirSurCarte = async (carte: WorldCard, mode: 'defaut' | 'reveler') => {
    if (!pile) return
    const quoi = pile.duJoueur
      ? t('Ajoutée à la main')
      : mode === 'reveler'
        ? t('Révélée')
        : t('Mise en jeu')
    await emettreGeste(`${quoi} — ${carte.name}`, () =>
      pile.duJoueur
        ? versLaMain(carte.id)
        : mode === 'reveler'
          ? triche.reveler(carte.id)
          : triche.mettreEnJeu(carte.id)
    )
    setPile(undefined)
  }

  const melangerPile = async () => {
    if (!pile) return
    await emettreGeste(`${t('Mélanger')} — ${pile.titre}`, () => triche.melanger(pile.zone, pile.siege))
    setPile(undefined)
  }

  const estUneDefausse = pile?.zone === 'DiscardPile' || pile?.zone === 'EncounterDiscardPile'

  const remelangerLaDefausse = async () => {
    if (!pile || !estUneDefausse || pile.cartes.length === 0) return
    await emettreGeste(`${t('Remélanger dans le deck')} — ${pile.titre}`, () =>
      triche.remelangerDefausse(pile.zone, pile.siege)
    )
    setPile(undefined)
  }

  return (
    <>
      {/* Le bandeau ne s'affiche qu'en bac à sable : il dit qu'une partie
          normale a été truquée. En manuel, il n'y a rien à dénoncer, et la
          spec demande un plateau nu. */}
      {manuel ? null : (
        <div className="bandeau-triche" role="status">
          <span className="bandeau-triche-marque">{t('Bac à sable')}</span>
          <span className="bandeau-triche-aide">
            {t('Clic droit sur une carte ou une pile')}
          </span>
        </div>
      )}

      {/* Tâche 4 ter : un geste manuel refusé se voit, brièvement et sans
          alarmer — ce n'est pas une erreur de l'application, c'est une
          réponse à un geste. Discret comme le bandeau lui-même. */}
      {manuel ? (
        <button
          type="button"
          className="bouton-catalogue-manuel"
          onClick={() => setCatalogueOuvert(true)}
          title={t('Chercher une carte dans tout le catalogue pour la poser (raccourci : C)')}
        >
          {t('Chercher une carte')} <kbd>C</kbd>
        </button>
      ) : null}

      {manuel && choixCible ? (
        <ChoixCibleAmelioration choix={choixCible} onChoisir={attacherChoisie} onFermer={fermerChoixCible} />
      ) : null}

      {manuel && avisRefus ? (
        <div className="avis-refus-manuel" role="status">
          {avisRefus}
        </div>
      ) : null}

      {/* Tâche 6 : la reconstruction moteur d'une annulation prend une à deux
          secondes — le joueur doit voir que quelque chose se passe. Même
          famille visuelle que l'avis de refus, transitoire elle aussi. */}
      {manuel && annulationEnCours ? (
        <div className="avis-refus-manuel" role="status">
          {t('Annulation en cours…')}
        </div>
      ) : null}

      {menu ? (
        <MenuTriche
          cible={menu.cible}
          x={menu.x}
          y={menu.y}
          onFermer={() => setMenu(undefined)}
          emettreGeste={emettreGeste}
          manuel={manuel}
          enMain={estEnMain(menu.cible.id)}
          poserEnJeu={manuel && estEnMain(menu.cible.id) ? () => poserDepuisLaMain(menu.cible.id) : undefined}
          echangerAvecLeDessus={manuel && estEnMain(menu.cible.id) ? () => echangerAvecLeDessus(menu.cible.id) : undefined}
        />
      ) : null}

      {/* Le menu de la TABLE (tâche 6, ronde de correction 1) : un clic droit
          hors de toute carte, en mode manuel. « Faire apparaître une carte »
          est une action de table, pas une action liée à une carte précise —
          elle n'a donc plus sa place dans MenuTriche. */}
      {manuel && menuTable ? (
        <MenuTable
          x={menuTable.x}
          y={menuTable.y}
          onFermer={() => setMenuTable(undefined)}
          onFaireApparaitre={() => setCatalogueOuvert(true)}
          onTerminerPartie={() => setFinOuverte(true)}
          onVaincreStade={() => void emettreGeste(t('Vaincre ce stade'), () => triche.avancerLeMechant())}
          onManigancePrincipale={() =>
            void emettreGeste(t('Manigance terminée'), () => triche.avancerLaManigance())
          }
          onToutRedresser={() => void executerGeste({ geste: 'toutRedresser' })}
          onFinPhaseHeros={() => void executerGeste({ geste: 'finPhaseHeros' })}
          onBoost={() => void executerGeste({ geste: 'boost' })}
          onHasard={tirerAuHasard}
          onDefausseAuHasard={mainAffichee.length > 0 ? defausserAuHasard : undefined}
          onMulligan={mainAffichee.length > 0 ? () => setMulliganOuvert(true) : undefined}
          onFinDeRound={() => void emettreGeste(t('Fin du round'), () => triche.finDeRound())}
        />
      ) : null}

      {manuel && excedent ? (
        <ChoixMulligan
          key={excedent.siege}
          main={excedent.main}
          titre={t('Main trop grande')}
          consigne={`${t('Défausse')} ${excedent.nombre} ${t('carte(s)')}`}
          libelle={t('Défausser')}
          maximum={excedent.nombre}
          onConfirmer={defausserExcedent}
          onFermer={() => setExcedent(undefined)}
        />
      ) : null}

      {manuel && mulliganOuvert ? (
        <ChoixMulligan main={mainAffichee} onConfirmer={confirmerMulligan} onFermer={() => setMulliganOuvert(false)} />
      ) : null}

      {manuel && catalogueOuvert ? (
        <CatalogueManuel
          catalogue={catalogue}
          onFermer={() => setCatalogueOuvert(false)}
          onPoser={(cardId, nom) => void faireApparaitre(cardId, nom)}
        />
      ) : null}

      {/* Tâche 7 : même présentation que le catalogue juste au-dessus (voile
          plein écran, boîte de dialogue) — la fin de partie mérite la même
          attention qu'y faire apparaître une carte, pas moins. */}
      {manuel && finOuverte ? (
        <div className="pile-triche-voile" onPointerDown={() => setFinOuverte(false)}>
          <section
            className="pile-triche fin-manuelle"
            role="dialog"
            aria-label={t('Terminer la partie')}
            style={transformDecalage(decalageFin)}
            onPointerDown={(evenement) => evenement.stopPropagation()}
          >
            <header className="pile-triche-entete">
              <h2
                className="poignee-glisser"
                onPointerDown={gestesGlisserFin.onPointerDown}
                onPointerMove={gestesGlisserFin.onPointerMove}
                onPointerUp={gestesGlisserFin.onPointerUp}
                onPointerCancel={gestesGlisserFin.onPointerCancel}
              >
                {t('Terminer la partie')}
              </h2>
              <button type="button" onClick={() => setFinOuverte(false)}>{t('Fermer')}</button>
            </header>
            <FinManuelle onDeclarer={(gagne) => void declarerFin(gagne)} />
          </section>
        </div>
      ) : null}

      {pile ? (
        <div className="pile-triche-voile" onPointerDown={() => setPile(undefined)}>
          <section
            className="pile-triche"
            role="dialog"
            aria-label={pile.titre}
            style={transformDecalage(decalagePile)}
            onPointerDown={(evenement) => evenement.stopPropagation()}
          >
            <header className="pile-triche-entete">
              <h2
                className="poignee-glisser"
                onPointerDown={gestesGlisserPile.onPointerDown}
                onPointerMove={gestesGlisserPile.onPointerMove}
                onPointerUp={gestesGlisserPile.onPointerUp}
                onPointerCancel={gestesGlisserPile.onPointerCancel}
              >
                {pile.titre} <small>({pile.cartes.length})</small>
              </h2>
              <span className="pile-triche-aide">
                {pile.duJoueur
                  ? t('Choisis une carte pour l’ajouter à ta main')
                  : t('Choisis une carte pour la mettre en jeu')}
              </span>
              <button type="button" onClick={() => void melangerPile()}>{t('Mélanger')}</button>
              {estUneDefausse ? (
                <button type="button" onClick={() => void remelangerLaDefausse()}>
                  {t('Remélanger dans le deck')}
                </button>
              ) : null}
              <button type="button" onClick={() => setPile(undefined)}>{t('Fermer')}</button>
            </header>

            <div className="pile-triche-cartes">
              {pile.cartes.length === 0 ? (
                <p className="pile-triche-vide">{t('Cette pile est vide')}</p>
              ) : (
                pile.cartes.map((carte, rang) => (
                  <span className="pile-triche-carte" key={`${carte.id}-${rang}`}>
                    <img src={scanUrl(carte.pic_id)} alt={carte.name} loading="lazy" />
                    <span className="pile-triche-actions">
                      <button type="button" onClick={() => void agirSurCarte(carte, 'defaut')}>
                        {pile.duJoueur ? t('En main') : t('Mettre en jeu')}
                      </button>
                      {/* « Révéler » : la carte suit le cheminement normal
                          d'une carte Rencontre au lieu d'être posée
                          directement. C'est l'échappatoire prévue quand le
                          placement automatique ne convient pas. */}
                      {!pile.duJoueur ? (
                        <button type="button" onClick={() => void agirSurCarte(carte, 'reveler')}>
                          {t('Révéler')}
                        </button>
                      ) : null}
                    </span>
                  </span>
                ))
              )}
            </div>
          </section>
        </div>
      ) : null}
    </>
  )
}
