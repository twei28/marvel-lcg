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
import { paysageSelonTypePapier, scanUrl } from '../card-model'
import { CarteApercu } from '../Board'
import { useApercuSurvol } from '../apercu-survol'
import { catalogueVide, chargerCatalogue, type Catalogue } from '../catalogue'
import type { ScanCardProps } from '../../components/ScanCard'
import type { World } from '../world'
import {
  cleCarnet,
  conditionRemplie,
  deListe,
  enListe,
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
  type DroitCarnet,
} from './droits-carnet'
import { assainirCarnet, preRemplir } from './preremplissage'
import { verdictDeCampagne, type Verdict } from './defaite-campagne'
import { repriseDeCampagne, type Reprise } from './reprise-campagne'
import { estModeManuel } from '../manuel/mode'

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

export function PanneauRecompenses({
  monde,
  gagne,
  siege,
  onTermine,
}: {
  monde: World | undefined
  gagne: boolean
  /**
   * Siège de CE navigateur, tel que l'URL le donne (`?p=`). Le 0 est l'hôte.
   * Il décide qui saisit quoi : voir `droits-carnet.ts`.
   */
  siege: number
  /** Appelé quand le joueur a validé : le plateau peut proposer la suite. */
  onTermine: (retourCampagne: boolean) => void
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

  async function valider() {
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
        onTermine(true)
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
        ...(verdict.perdue ? { perdue: true } : {}),
      }
      await enregistrerCampagne(suivante)
      effacerContexte()
      onTermine(true)
    } catch (e) {
      setEchec((e as Error).message)
      setEnregistrement(false)
    }
  }

  const estFinal = Boolean(scenario.final)
  const epilogue = scenario.pages?.epilogue ?? []

  return (
    <section className="camp-recomp" aria-label={t('Récompenses de campagne')}>
      <header className="camp-recomp-tete">
        <span className="camp-recomp-eyebrow">
          {campagne.nom} · {t('Scénario')} {scenario.numero} / {definition.scenarios.length}
        </span>
        <strong className="camp-recomp-titre">
          {verdict.perdue
            ? t('La campagne est perdue')
            : reprise.applicable
              ? reprise.titre || t('Ce scénario est à re-préparer')
              : estFinal
                ? t('La campagne est gagnée !')
                : t('Ce que vous gagnez')}
        </strong>
      </header>

      {verdict.perdue ? (
        <p className="camp-recomp-defaite">
          {verdict.texte}{' '}
          {gagne
            ? t('Le scénario est gagné, mais la campagne s’arrête ici.')
            : t('Ce scénario ne se rejoue pas : la campagne s’arrête ici.')}
        </p>
      ) : null}

      {reprise.applicable ? (
        <div className="camp-recomp-reprise">
          <p>{reprise.texte}</p>
          <p className="camp-recomp-reprise-compte">
            {preuvesRendues > 0
              ? `${preuvesRendues} ${
                  preuvesRendues > 1 ? t('preuves vous seront rendues') : t('preuve vous sera rendue')
                }`
              : t('Aucune preuve ne vous sera rendue : le Conseil n’a jamais fini vidé de ses secrets.')}
          </p>
        </div>
      ) : null}

      {epilogue.length && gagne ? (
        <div className="camp-recomp-bd">
          {epilogue.map((fichier) => (
            <img
              key={fichier}
              src={`/public/stories/${definition.code}/${fichier}`}
              alt=""
              loading="lazy"
            />
          ))}
        </div>
      ) : null}

      {/* Tâche 7 : en mode manuel, le moteur ne surveille plus la table — les
          cases marquées « relevé par le jeu » (voir `ChampRecompense`
          ci-dessous) ne se rempliront donc plus toutes seules. Elles restent
          déjà CORRIGEABLES dans tous les modes (décision antérieure : un
          détecteur peut se tromper, voir l'en-tête du fichier) ; ce qui
          manquait, c'est de le DIRE — sans cette ligne, un joueur qui trouve
          ces cases vides croirait à un bug plutôt qu'au mode qu'il a choisi. */}
      {continueSurDefaite ? (
        <p className="camp-recomp-defaite">
          {t('Scénario perdu : la campagne continue avec les gains de la défaite.')}
        </p>
      ) : null}

      {champsVisibles && estModeManuel(monde) && visibles.some((c) => c.type === 'auto') ? (
        <p className="camp-recomp-aide-manuel">
          {t(
            'Mode manuel : le moteur ne surveille plus la table, les cases « relevé par le jeu » restent à remplir à la main.'
          )}
        </p>
      ) : null}

      {visibles.length && champsVisibles ? (
        <div className="camp-recomp-champs">
          {visibles.map((champ) => (
            <ChampRecompense
              key={champ.cle + (champ.condition ?? '')}
              champ={champ}
              total={total}
              monde={monde as World}
              valeurs={valeurs}
              poser={poser}
              nomJoueur={nomJoueur}
              siege={siege}
            />
          ))}
        </div>
      ) : champsVisibles ? (
        <p className="camp-recomp-rien">
          {estFinal
            ? t('Hydra est vaincue. Rien de plus à reporter : tournez la page.')
            : t('Ce scénario ne rapporte rien à reporter dans le carnet.')}
        </p>
      ) : null}

      {echec ? <p className="camp-recomp-echec">{echec}</p> : null}

      <div className="camp-recomp-actions">
        {peutValider(siege) ? (
          <button
            type="button"
            className="camp-recomp-valider"
            disabled={Boolean(manquants.length) || enregistrement}
            onClick={valider}
          >
            {enregistrement
              ? t('Enregistrement…')
              : verdict.perdue
                ? t('Consigner la fin de la campagne')
                : reprise.applicable
                  ? t('Re-préparer les preuves')
                  : estFinal
                    ? t('Voir la conclusion')
                    : t('Valider et continuer la campagne')}
          </button>
        ) : (
          <>
            <button
              type="button"
              className="camp-recomp-valider"
              disabled={enregistrement}
              onClick={envoyerMesChamps}
            >
              {enregistrement
                ? t('Envoi…')
                : envoye
                  ? t('Renvoyer mes champs')
                  : t('Envoyer mes champs')}
            </button>
            <span className="camp-recomp-attente-hote">
              {envoye
                ? t("Envoyé. L'hôte valide les récompenses pour la table.")
                : t("L'hôte valide les récompenses pour la table.")}
            </span>
          </>
        )}
        {/* Réservé à qui valide. Chez un siège distant, cette liste nommait des
            cases appartenant à d'AUTRES joueurs : elle lui demandait de remplir
            ce qu'il n'a pas le droit d'écrire. Relevé par campagne-multi. */}
        {peutValider(siege) && manquants.length ? (
          <span className="camp-recomp-bloque">
            {t('À choisir avant de continuer :')} {manquants.map((c) => t(c.libelle)).join(', ')}
          </span>
        ) : null}
      </div>
    </section>
  )
}

function ChampRecompense({
  champ,
  total,
  monde,
  valeurs,
  poser,
  nomJoueur,
  siege,
}: {
  champ: ChampVictoire
  total: number
  monde: World
  valeurs: Record<string, string>
  poser: (cle: string, valeur: string) => void
  nomJoueur: (i: number) => string
  siege: number
}) {
  const joueurs = champ.parJoueur ? [...Array(total).keys()] : [0]
  const auto = champ.type === 'auto'

  return (
    <div className={`camp-champ ${auto ? 'est-auto' : 'est-choix'}`}>
      <div className="camp-champ-tete">
        <span className="camp-champ-libelle">{t(champ.libelle)}</span>
        {auto ? <span className="camp-champ-marque">{t('relevé par le jeu')}</span> : null}
      </div>
      {champ.aide ? <p className="camp-champ-aide">{t(champ.aide)}</p> : null}
      {joueurs.map((joueurId) => {
        const elimine = champ.parJoueur && joueurElimine(monde, joueurId)
        const cle = cleCarnet(champ, joueurId)
        // À plusieurs, une case n'appartient qu'à un siège. Les autres la
        // voient, pour suivre le carnet se remplir, mais ne peuvent pas
        // l'écrire : sinon le dernier à cliquer gagne, en silence.
        const droit = droitSurChamp(champ, joueurId, siege, peutValider(siege))
        return (
          <div className={`camp-champ-ligne${droit === 'lecture' ? ' est-lecture' : ''}`} key={cle}>
            {champ.parJoueur ? (
              <span className="camp-champ-joueur">{nomJoueur(joueurId)}</span>
            ) : null}
            {elimine ? (
              <span className="camp-champ-elimine">
                {t('Héros vaincu : il ne participe pas aux récompenses de ce scénario.')}
              </span>
            ) : (
              <Controle champ={champ} cle={cle} valeurs={valeurs} poser={poser} droit={droit} />
            )}
            {droit === 'lecture' && !elimine && champ.parJoueur ? (
              <small className="camp-champ-proprietaire">
                {t('à remplir par')} {nomJoueur(joueurId)}
              </small>
            ) : null}
          </div>
        )
      })}
    </div>
  )
}

/**
 * Des cartes cliquables, avec l'agrandissement au survol de la table (même
 * `CarteApercu`, même règle `useApercuSurvol` : un seul écouteur sur le
 * conteneur). L'écran de fin de partie est à 600 : l'aperçu passe au-dessus.
 */
function ListeCartes({
  ids,
  choisie,
  inerte,
  basculer,
}: {
  ids: readonly string[]
  choisie: (id: string) => boolean
  inerte: boolean
  basculer: (id: string) => void
}) {
  const [catalogue, setCatalogue] = useState<Catalogue>(catalogueVide)
  useEffect(() => {
    let annule = false
    void chargerCatalogue().then((c) => {
      if (!annule) setCatalogue(c)
    })
    return () => {
      annule = true
    }
  }, [])

  const cartes = useMemo<ScanCardProps[]>(
    () =>
      ids.map((id) => ({
        id,
        name: id,
        kind: 'unknown',
        imageUrl: scanUrl(id),
        isLandscape: paysageSelonTypePapier(catalogue.type(id)),
        keywords: catalogue.motsCles(id),
        codeCarte: id,
      })),
    [ids, catalogue]
  )
  const { regardee, survol, quitter } = useApercuSurvol(cartes)

  return (
    <div className="camp-cartes" onMouseOver={survol} onMouseLeave={quitter}>
      {ids.map((id) => (
        // Le survol se lit sur l'enveloppe : un bouton désactivé (carnet d'un
        // autre siège) n'émet plus d'évènement souris, et l'aperçu doit
        // pourtant s'ouvrir pour lire la carte.
        <span key={id} data-card-id={id} className="camp-carte-enveloppe">
          <button
            type="button"
            className={`camp-carte${choisie(id) ? ' sel' : ''}`}
            aria-pressed={choisie(id)}
            disabled={inerte}
            onClick={() => basculer(id)}
          >
            <img src={scanUrl(id)} alt={id} loading="lazy" />
          </button>
        </span>
      ))}
      {regardee ? <CarteApercu carte={regardee} classe="au-dessus-de-la-fin" /> : null}
    </div>
  )
}

function Controle({
  champ,
  cle,
  valeurs,
  poser,
  droit,
}: {
  champ: ChampVictoire
  cle: string
  valeurs: Record<string, string>
  poser: (cle: string, valeur: string) => void
  /** `lecture` rend le contrôle inerte : la case est à quelqu'un d'autre. */
  droit: DroitCarnet
}) {
  const valeur = valeurs[cle] ?? ''
  const inerte = droit === 'lecture'

  // Un CHOIX du livret : on montre les cartes, pas une liste déroulante. C'est
  // une décision de jeu, elle mérite qu'on voie ce qu'on prend.
  if (champ.type === 'choix' && champ.options?.length) {
    return (
      <ListeCartes
        ids={champ.options}
        choisie={(id) => valeur === id}
        inerte={inerte}
        basculer={(id) => poser(cle, valeur === id ? '' : id)}
      />
    )
  }

  if (champ.format === 'int') {
    return (
      <input
        className="camp-champ-int"
        type="number"
        min={0}
        disabled={inerte}
        value={valeur}
        onChange={(e) => poser(cle, e.target.value)}
      />
    )
  }

  // Liste avec options connues : des cases à cocher sur les cartes concernées.
  if (champ.options?.length) {
    const choisies = new Set(deListe(valeur))
    return (
      <ListeCartes
        ids={champ.options}
        choisie={(id) => choisies.has(id)}
        inerte={inerte}
        basculer={(id) => {
          const suite = new Set(choisies)
          if (suite.has(id)) suite.delete(id)
          else suite.add(id)
          poser(cle, enListe(champ.options!.filter((x) => suite.has(x))))
        }}
      />
    )
  }

  // Liste sans options connues (les héros engagés, par exemple) : le relevé du
  // moteur en clair, corrigeable à la main.
  return (
    <input
      className="camp-champ-texte"
      type="text"
      disabled={inerte}
      value={valeur}
      placeholder={t('rien')}
      onChange={(e) => poser(cle, e.target.value.trim())}
    />
  )
}
