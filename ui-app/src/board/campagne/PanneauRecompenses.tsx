// PanneauRecompenses — ce que le scénario de campagne vient de rapporter.
//
// S'ouvre sur l'écran de fin de partie, à la victoire, et à la défaite dans le
// seul cas où elle compte : celle du dernier scénario, qui peut perdre la
// campagne (voir defaite-campagne.ts). Une défaite ailleurs se rejoue sans
// pénalité, donc sans rien reporter non plus.
//
// Le principe : tout ce que le moteur sait, le panneau l'a déjà rempli et le
// présente comme un constat (« voici ce que la partie a produit »). Il ne reste
// au joueur que les vrais CHOIX du livret — quelle amélioration prendre. Chaque
// valeur détectée reste corrigeable, parce qu'un détecteur peut se tromper et
// qu'on préfère une case modifiable à une campagne faussée.
import { useEffect, useMemo, useState } from 'react'
import { t } from '../langue'
import type { World } from '../world'
import {
  cleCarnet,
  conditionRemplie,
  joueurElimine,
  type ChampVictoire,
} from './detecteurs'
import {
  champsDuScenario,
  chargerCampagne,
  chargerCarnetSuggere,
  chargerDefinition,
  effacerContexte,
  enregistrerCampagne,
  enregistrerCarnetPartiel,
  reinitialiserEnquete,
  resoudreContexte,
  type Campagne,
  type DefinitionCampagne,
  type ScenarioCampagne,
} from './contexte'
import { scenarioSuivantLance } from './attente-scenario'
import {
  cleDUnAutreSiege,
  droitSurChamp,
  peutValider,
} from './droits-carnet'
import { assainirCarnet, preRemplir } from './preremplissage'
import { verdictDeCampagne, type Verdict } from './defaite-campagne'
import { repriseDeCampagne, type Reprise } from './reprise-campagne'
import { estModeManuel } from '../manuel/mode'
import { ParcoursFinScenario, type ResumeFinScenario, type SuiteDemandee } from './ParcoursFinScenario'

type Etat =
  | { phase: 'chargement' }
  | { phase: 'absent' }
  | { phase: 'erreur'; message: string }
  | {
      phase: 'pret'
      campagne: Campagne
      definition: DefinitionCampagne
      scenario: ScenarioCampagne
      champs: ChampVictoire[]
      suggestions: Record<string, string>
      /** Scénario qui a produit `suggestions` côté moteur — voir preremplissage.ts. */
      scenarioSuggestions: string | null
      /** Le hasard des champs à tirage, figé à l'ouverture du panneau. */
      ordresDeTirage: Record<string, readonly string[]>
    }

/**
 * Mélange les options des champs à TIRAGE, une fois pour toutes.
 *
 * Le livret fait tirer certaines pénalités au hasard (« Choose one Osborn Tech
 * attachment at random »). Le hasard est donc légitime, mais il doit être tiré
 * UNE fois : `preRemplir` tourne dans un `useMemo` qui dépend du monde, et un
 * `Math.random()` à l'intérieur ferait changer les cartes à chaque trame du moteur,
 * sous les yeux du joueur.
 */
function melangerLesTirages(champs: ChampVictoire[]): Record<string, readonly string[]> {
  const ordres: Record<string, readonly string[]> = {}
  for (const champ of champs) {
    if (!champ.tirage) continue
    const options = [...(champ.options ?? [])]
    for (let i = options.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[options[i], options[j]] = [options[j]!, options[i]!]
    }
    ordres[champ.cle] = options
  }
  return ordres
}

/** Nombre de héros de la campagne : les clés « Player N » en dépendent. */
const nbJoueurs = (campagne: Campagne, monde: World) =>
  Math.max(campagne.equipe?.length ?? 0, monde.players?.length ?? 0, 1)

const RESUME_VIDE: ResumeFinScenario = { heros: [], vilains: [] }

export function PanneauRecompenses({
  monde,
  gagne,
  siege,
  resume = RESUME_VIDE,
  onTermine,
}: {
  monde: World | undefined
  gagne: boolean
  /**
   * Siège de CE navigateur, tel que l'URL le donne (`?p=`). Le 0 est l'hôte.
   * Il décide qui saisit quoi : voir `droits-carnet.ts`.
   */
  siege: number
  /** Héros, vilain et rounds de la partie qui vient de finir (page « Victoire » du parcours). */
  resume?: ResumeFinScenario
  /** Appelé quand le joueur a validé : le plateau peut proposer la suite. */
  onTermine: (retourCampagne: boolean, suite?: SuiteDemandee) => void
}) {
  const [etat, setEtat] = useState<Etat>({ phase: 'chargement' })
  const [valeurs, setValeurs] = useState<Record<string, string>>({})
  const [enregistrement, setEnregistrement] = useState(false)
  const [echec, setEchec] = useState('')
  // Un distant n'a pas de « Valider » : sans retour, il ne saurait pas si son
  // envoi a pris.
  const [envoye, setEnvoye] = useState(false)

  useEffect(() => {
    let annule = false
    ;(async () => {
      try {
        // Une partie ORDINAIRE n'a pas de campagne, quoi que disent la clé du
        // navigateur ou le `partieEnCours` du serveur : ce sont des états
        // durables qu'elle n'efface pas (ils servent à reprendre un scénario),
        // et c'est ainsi qu'une victoire hors campagne validait un scénario
        // sans rapport (07/10/2026). Le critère est la RÈGLE du moteur, la même
        // pour tous les sièges. Aucun appel réseau avant.
        if (monde?.mode_campaign !== true) {
          setEtat({ phase: 'absent' })
          return
        }
        // Le contexte vient du localStorage chez l'hôte, du serveur chez tous
        // les autres. La garde est DANS la fonction : dehors, elle rendrait
        // « absent » aux sièges distants avant même d'avoir demandé.
        const contexte = await resoudreContexte()
        if (annule) return
        if (!contexte || !monde) {
          setEtat({ phase: 'absent' })
          return
        }
        const campagne = await chargerCampagne(contexte.id)
        const definition = await chargerDefinition(campagne.code)
        const carnetSuggere = await chargerCarnetSuggere()
        const scenario = definition.scenarios.find((s) => s.id === contexte.scenario)
        if (!scenario) throw new Error(`scénario inconnu : ${contexte.scenario}`)
        if (annule) return
        // Une défaite n'ouvre le panneau que si elle perd la campagne, OU si
        // le scénario demande de re-préparer quelque chose avant d'être
        // rejoué. Sinon rien ne se reporte, et le joueur rejoue tel quel.
        if (!gagne) {
          const verdict = verdictDeCampagne({
            final: Boolean(scenario.final),
            regle: scenario.defaite,
            gagne: false,
            expert: campagne.difficulte === 'expert',
            carnet: campagne.carnet ?? {},
          })
          const reprise = repriseDeCampagne({
            final: Boolean(scenario.final),
            regle: scenario.reprise,
            gagne: false,
            expert: campagne.difficulte === 'expert',
            perdue: verdict.perdue,
          })
          if (!verdict.perdue && !reprise.applicable && !scenario.defaite_continue) {
            setEtat({ phase: 'absent' })
            return
          }
        }
        const champs = champsDuScenario(definition, scenario, campagne.difficulte)
        // Le hasard des champs à tirage est tiré ICI, une seule fois, et gardé :
        // `preRemplir` tourne dans un `useMemo` qui dépend du monde, donc un
        // `Math.random()` à l'intérieur changerait de cartes à chaque trame du
        // moteur. Le tirage doit être fait une fois pour toutes, comme on tire une
        // carte d'un paquet.
        const ordresDeTirage = melangerLesTirages(champs)
        setEtat({
          phase: 'pret',
          campagne,
          definition,
          scenario,
          champs,
          ordresDeTirage,
          suggestions: carnetSuggere.suggestions,
          scenarioSuggestions: carnetSuggere.scenario,
        })
      } catch (e) {
        if (!annule) setEtat({ phase: 'erreur', message: (e as Error).message })
      }
    })()
    return () => {
      annule = true
    }
  }, [monde, gagne])

  // Pré-remplissage : une seule fois, à l'ouverture. Le joueur reste maître de
  // ses corrections — un nouveau rendu du monde ne doit pas les écraser.
  const preRemplissage = useMemo(() => {
    if (etat.phase !== 'pret' || !monde) return {}
    return preRemplir({
      champs: etat.champs,
      monde,
      carnet: etat.campagne.carnet,
      suggestions: etat.suggestions,
      scenarioSuggestions: etat.scenarioSuggestions,
      scenarioActuel: etat.scenario.id,
      total: nbJoueurs(etat.campagne, monde),
      ordresDeTirage: etat.ordresDeTirage,
    })
  }, [etat, monde])

  useEffect(() => {
    setValeurs(preRemplissage)
  }, [preRemplissage])

  // L'hôte attend les champs des autres sièges. Trois secondes suffisent : on
  // regarde quelqu'un remplir un formulaire, pas une animation. Le poll
  // n'existe pas chez les distants, qui n'attendent personne, et s'arrête dès
  // que le panneau se ferme.
  //
  // Il ne reprend QUE les cases des autres. Sans ce filtre, une case à l'hôte
  // qu'il vient d'effacer réapparaîtrait toutes les trois secondes.
  const idCampagne = etat.phase === 'pret' ? etat.campagne.id : undefined
  useEffect(() => {
    if (!peutValider(siege) || !idCampagne) return
    const minuteur = window.setInterval(() => {
      void chargerCampagne(idCampagne)
        .then((fraiche) => {
          const desAutres = Object.fromEntries(
            Object.entries(fraiche.carnet ?? {}).filter(([cle]) => cleDUnAutreSiege(cle, siege))
          )
          setValeurs((courantes) => ({ ...courantes, ...desAutres }))
        })
        .catch(() => undefined)
    }, 3000)
    return () => window.clearInterval(minuteur)
  }, [siege, idCampagne])

  // Les distants suivent l'hôte. Lui n'attend personne : c'est lui qui relance
  // depuis l'écran des campagnes, et il y navigue tout seul.
  //
  // Quatre secondes : on attend que quelqu'un lise un épilogue et relance, pas
  // un clic. Recharger la page est brutal mais juste : une nouvelle partie a
  // démarré, tout ce que le plateau tenait en mémoire est périmé.
  const scenarioCourant = etat.phase === 'pret' ? etat.scenario.id : ''
  useEffect(() => {
    if (peutValider(siege) || !scenarioCourant) return
    const minuteur = window.setInterval(() => {
      void fetch('/get_campagne_en_cours', { cache: 'no-store' })
        .then((r) => (r.ok ? r.json() : null))
        .then((lu) => {
          if (scenarioSuivantLance(scenarioCourant, lu)) window.location.reload()
        })
        .catch(() => undefined)
    }, 4000)
    return () => window.clearInterval(minuteur)
  }, [siege, scenarioCourant])

  if (etat.phase === 'absent') return null
  if (etat.phase === 'chargement') {
    return (
      <section className="camp-recomp">
        <p className="camp-recomp-attente">{t('Chargement de la campagne…')}</p>
      </section>
    )
  }
  if (etat.phase === 'erreur') {
    return (
      <section className="camp-recomp">
        <p className="camp-recomp-echec">
          {t('La campagne n’a pas pu être lue :')} {etat.message}
        </p>
      </section>
    )
  }

  const { campagne, definition, scenario, champs } = etat
  // Les propositions du moteur (`optionsSuggerees`) ne valent que pour la partie qui vient de finir : même garde
  // d'estampille que `preRemplir`.
  const suggestionsDuMoteur = etat.scenarioSuggestions === scenario.id ? etat.suggestions : undefined
  const total = nbJoueurs(campagne, monde as World)
  const nomJoueur = (i: number) =>
    campagne.equipe?.[i]?.nomHeros ?? `${t('Joueur')} ${i + 1}`

  const poser = (cle: string, valeur: string) =>
    setValeurs((v) => {
      const suite = { ...v }
      if (valeur === '') delete suite[cle]
      else suite[cle] = valeur
      return suite
    })

  // Une défaite qui fait continuer la campagne (`defaite_continue`) a ses
  // propres gains : ses champs se montrent et se valident comme une victoire.
  const continueSurDefaite = !gagne && Boolean(scenario.defaite_continue) && !scenario.final
  const champsVisibles = gagne || continueSurDefaite
  const visibles = champs.filter((c) => conditionRemplie(c, monde as World))
  const manquants = visibles.filter((champ) => {
    // Aucun champ n'est affiché à la défaite (sauf `defaite_continue`) : en
    // exiger un bloquerait le bouton sur une case que personne ne peut voir.
    if (!champsVisibles) return false
    if (champ.type !== 'choix' || !champ.obligatoire) return false
    const joueurs = champ.parJoueur ? [...Array(total).keys()] : [0]
    return joueurs.some(
      (i) =>
        !(champ.parJoueur && joueurElimine(monde as World, i)) && !valeurs[cleCarnet(champ, i)]
    )
  })

  // Le verdict se calcule sur le carnet TEL QU'IL SERA ENREGISTRE, corrections
  // du joueur comprises : pour AoA, cocher « Professeur X sauvé » à la main
  // doit sauver la campagne, exactement comme si le moteur l'avait relevé.
  const carnetApres = { ...(campagne.carnet ?? {}), ...assainirCarnet(champs, valeurs, total) }
  const verdict: Verdict = verdictDeCampagne({
    final: Boolean(scenario.final),
    regle: scenario.defaite,
    gagne,
    expert: campagne.difficulte === 'expert',
    carnet: carnetApres,
  })

  const reprise: Reprise = repriseDeCampagne({
    final: Boolean(scenario.final),
    regle: scenario.reprise,
    gagne,
    expert: campagne.difficulte === 'expert',
    perdue: verdict.perdue,
  })
  // Combien de preuves la reprise va rendre. Le compte vient du carnet ; le
  // CHOIX des preuves, lui, se fait côté serveur et n'arrive jamais ici.
  const preuvesRendues = Math.min(
    6,
    Number((reprise.applicable && scenario.reprise?.cle_compte
      ? campagne.carnet?.[scenario.reprise.cle_compte]
      : '0') ?? '0') || 0
  )

  /**
   * Un siège distant envoie SES champs, et rien d'autre.
   *
   * On n'envoie que ce qui nous appartient : le serveur fusionne, donc envoyer
   * le carnet entier écraserait les champs des autres avec la copie qu'on en a
   * lue, qui peut déjà être périmée.
   */
  async function envoyerMesChamps() {
    if (enregistrement) return
    setEnregistrement(true)
    setEchec('')
    try {
      const miens: Record<string, string> = {}
      for (const champ of visibles) {
        const joueurs = champ.parJoueur ? [...Array(total).keys()] : [0]
        for (const joueurId of joueurs) {
          if (droitSurChamp(champ, joueurId, siege, peutValider(siege)) !== 'saisie') continue
          const cle = cleCarnet(champ, joueurId)
          const valeur = valeurs[cle]
          if (valeur !== undefined) miens[cle] = valeur
        }
      }
      await enregistrerCarnetPartiel(campagne.id, miens)
      setEnvoye(true)
    } catch (e) {
      setEchec((e as Error).message)
    } finally {
      setEnregistrement(false)
    }
  }

  async function valider(suite?: SuiteDemandee) {
    if (manquants.length || enregistrement) return
    setEnregistrement(true)
    setEchec('')
    try {
      // Reprise : c'est le SERVEUR qui réécrit la campagne, parce qu'il est le
      // seul à pouvoir retirer la taupe sans la montrer. Rien à enregistrer
      // ici derrière, sous peine d'écraser le carnet qu'il vient de poser.
      if (reprise.applicable) {
        await reinitialiserEnquete(campagne.id)
        effacerContexte()
        onTermine(true, { campagne: campagne.id })
        return
      }
      const suivante: Campagne = {
        ...campagne,
        carnet: carnetApres,
        // Une défaite ne termine rien : le scénario reste à jouer. Ce qui se
        // termine, c'est la campagne, et c'est `perdue` qui le dit.
        termines: gagne || continueSurDefaite
          ? [...new Set([...(campagne.termines ?? []), scenario.id])]
          : (campagne.termines ?? []),
        partieEnCours: null,
        // La colonne de ce scénario dans le carnet imprimé : ce qu'il vient de
        // noter. Rien ne la relit pour jouer ; l'écran de campagne la montre.
        ...(gagne || continueSurDefaite
          ? {
              historique: {
                ...(campagne.historique ?? {}),
                [scenario.id]: assainirCarnet(champs, valeurs, total),
              },
            }
          : {}),
        ...(verdict.perdue ? { perdue: true } : {}),
      }
      await enregistrerCampagne(suivante)
      effacerContexte()
      onTermine(true, { campagne: campagne.id, lancer: suite?.lancer })
    } catch (e) {
      setEchec((e as Error).message)
      setEnregistrement(false)
    }
  }

  return (
    <ParcoursFinScenario
      monde={monde as World}
      gagne={gagne}
      siege={siege}
      campagne={campagne}
      definition={definition}
      scenario={scenario}
      visibles={visibles}
      champsVisibles={champsVisibles}
      continueSurDefaite={continueSurDefaite}
      verdict={verdict}
      reprise={reprise}
      preuvesRendues={preuvesRendues}
      valeurs={valeurs}
      poser={poser}
      total={total}
      nomJoueur={nomJoueur}
      suggestions={suggestionsDuMoteur}
      manquants={manquants}
      enregistrement={enregistrement}
      echec={echec}
      envoye={envoye}
      modeManuel={estModeManuel(monde)}
      resume={resume}
      onValider={(suite) => void valider(suite)}
      onEnvoyer={envoyerMesChamps}
    />
  )
}
