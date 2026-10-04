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

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { catalogueVide, type Catalogue } from './catalogue'
import { scanUrl } from './card-model'
import { t } from './langue'
import { transformDecalage, useGlisserPanneau } from './placement/useGlisserPanneau'
import { CatalogueManuel } from './manuel/CatalogueManuel'
import {
  creerEtatTouches,
  interpreterTouche,
  type CibleClavier,
  type GesteClavier,
} from './manuel/clavier'
import { FinManuelle } from './manuel/FinManuelle'
import { leMoteurSeTait } from './manuel/mode'
import { estSpectateur } from './moteur'
import { MenuTable } from './manuel/MenuTable'
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

/** Les types de cartes qui se mesurent en menace plutôt qu'en points de vie. */
const MANIGANCES = new Set(['MainScheme', 'SideScheme', 'Scheme'])
/** Ce qui ne s'incline pas et n'a pas d'état : inutile de proposer ces entrées. */
const SANS_ETAT = new Set(['Event', 'Treachery', 'Obligation', 'Resource'])

/**
 * Le jeton qu'un chiffre pose « naturellement » sur cette carte, pour le
 * clavier (voir `manuel/clavier.ts`). MÊMES ENSEMBLES que le menu au clic
 * droit, juste au-dessus : une manigance se mesure en menace, une carte SANS
 * ÉTAT n'a rien à recevoir — mieux vaut ne rien poser qu'un jeton faux qu'on
 * ne relira pas.
 */
function jetonNaturelDe(carte: WorldCard): 'degats' | 'menace' | 'aucun' {
  if (MANIGANCES.has(carte.card_type)) return 'menace'
  if (SANS_ETAT.has(carte.card_type)) return 'aucun'
  return 'degats'
}

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
    if (dessus) piles.set(dessus.id, { titre, cartes, duJoueur, zone })
  }

  ajouter(joueur?.player_deck, t('Deck du héros'), true, 'PlayerDeck')
  ajouter(joueur?.player_discard_pile, t('Pile de défausse'), true, 'DiscardPile')
  ajouter(world.encounter_deck, t('Deck Rencontre'), false, 'EncounterDeck')
  ajouter(world.encounter_discard_pile, t('Défausse Rencontre'), false, 'EncounterDiscardPile')
  return piles
}

export function useTriche(
  world: World | undefined,
  joueurId: number,
  /** Verse l'intervention dans le journal de partie. */
  ajouterAuJournal?: (libelle: string) => void
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

  const index = useMemo(() => (actif ? indexer(world) : new Map()), [actif, world])
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

  // L'écoute vit au niveau du document : les cartes portent déjà
  // `data-card-id`, il suffit de remonter depuis la cible du clic.
  useEffect(() => {
    if (!actif) return
    const surClicDroit = (evenement: MouseEvent) => {
      const cible = evenement.target as HTMLElement | null
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
          evenement.preventDefault()
          setMenuTable({ x: evenement.clientX, y: evenement.clientY })
        }
        return
      }
      const id = Number(noeud.getAttribute('data-card-id'))
      if (!Number.isFinite(id)) return

      evenement.preventDefault()

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
          nom: carte.name || `${t('Carte')} ${id}`,
          estManigance: MANIGANCES.has(carte.card_type),
          estPersonnage: !SANS_ETAT.has(carte.card_type),
        },
        x: evenement.clientX,
        y: evenement.clientY,
      })
    }
    document.addEventListener('contextmenu', surClicDroit)
    return () => document.removeEventListener('contextmenu', surClicDroit)
  }, [actif, index, piles, manuel])

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
        case 'melanger': {
          const pileVisee = [...piles.values()].find((candidate) => candidate.zone === geste.zone)
          await emettreGeste(`${t('Mélanger')} — ${pileVisee?.titre ?? geste.zone}`, () =>
            triche.melanger(geste.zone)
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
              ? await triche.envoyerEnMain(carte.id)
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
          // « retirer » du clavier (Maj) passe par Puzzle.Heal, comme le menu.
          const libelle = geste.nombre >= 0 ? t('Infliger des dégâts') : t('Soigner')
          await emettreGeste(`${libelle} ${Math.abs(geste.nombre)} — ${nom}`, () =>
            geste.nombre >= 0
              ? triche.blesser(geste.id, geste.nombre)
              : triche.soigner(geste.id, -geste.nombre)
          )
        }
      }
    },
    [index, piles, emettreGeste, noter]
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
    }

    const cibleClavier = (id: number): CibleClavier | undefined => {
      const pileVisee = piles.get(id)
      if (pileVisee) return { genre: 'pile', zone: pileVisee.zone }
      const carte = index.get(id)
      if (!carte) return undefined
      return { genre: 'carte', id, jetonNaturel: jetonNaturelDe(carte) }
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
      // Ctrl/Cmd/Alt : ce sont des raccourcis du NAVIGATEUR (Ctrl+F cherche,
      // Ctrl+R recharge, Ctrl+1..9 change d'onglet), pas du jeu. Sans cette
      // garde, survoler une carte pendant Ctrl+F la retournait — un dos de
      // pile ou une carte face cachée révélée, et la remettre face cachée ne
      // fait pas oublier ce qu'on a lu : irréversible au sens fort. On sort
      // AVANT tout `preventDefault`, pour laisser le navigateur faire son
      // travail. Alt a en plus son propre rôle : il agrandit tout de suite la
      // carte survolée (`Board.tsx`), une raison de plus pour qu'il ne
      // déclenche jamais un geste de jeu ici. Seul Maj reste porteur de
      // sens : il inverse un chiffre (retirer au lieu d'ajouter).
      if (evenement.ctrlKey || evenement.metaKey || evenement.altKey) return
      // Une saisie de texte en cours : le chiffre tapé est un chiffre, pas un
      // geste de jeu.
      if (estZoneDeSaisie(document.activeElement)) return
      if (survole.current === undefined) return
      const cible = cibleClavier(survole.current)
      if (!cible) return
      const geste = interpreterTouche({ cle: evenement.key, majuscule: evenement.shiftKey }, cible)
      if (!geste) return
      evenement.preventDefault()
      void executerGeste(geste)
    }

    const surRelachement = (evenement: KeyboardEvent) => etatTouches.enregistrer(evenement)

    document.addEventListener('pointermove', surPointeur)
    document.addEventListener('keydown', surTouche)
    document.addEventListener('keyup', surRelachement)
    return () => {
      document.removeEventListener('pointermove', surPointeur)
      document.removeEventListener('keydown', surTouche)
      document.removeEventListener('keyup', surRelachement)
    }
  }, [manuel, index, piles, executerGeste, etatTouches, lancerAnnulation])

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
      avisRefus,
      annulationEnCours,
      menuTable,
      setMenuTable,
    },
    /** Pour la tâche 5 (glisser-déposer) : lire l'état sans poser d'écoute. */
    estToucheEnfoncee: etatTouches.estEnfoncee,
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
    avisRefus,
    annulationEnCours,
    menuTable,
    setMenuTable,
  } = couche
  // Le catalogue (tâche 6) : une carte qui n'était pas dans la partie. Mode
  // manuel uniquement, ouvert depuis le menu de la TABLE (clic droit hors de
  // toute carte — voir `MenuTable.tsx` et le menu plus bas).
  const [catalogueOuvert, setCatalogueOuvert] = useState(false)
  // Déclarer la fin (tâche 7) : même origine que le catalogue, le menu de la
  // TABLE. `FinManuelle` tient déjà sa propre confirmation ; `onDeclarer`
  // n'est donc appelé qu'une fois la décision prise, jamais au premier clic.
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
        ? triche.envoyerEnMain(carte.id)
        : mode === 'reveler'
          ? triche.reveler(carte.id)
          : triche.mettreEnJeu(carte.id)
    )
    setPile(undefined)
  }

  const melangerPile = async () => {
    if (!pile) return
    await emettreGeste(`${t('Mélanger')} — ${pile.titre}`, () => triche.melanger(pile.zone))
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
        />
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
