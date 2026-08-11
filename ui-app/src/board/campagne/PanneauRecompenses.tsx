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
import { scanUrl } from '../card-model'
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
  lireContexte,
  reinitialiserEnquete,
  type Campagne,
  type DefinitionCampagne,
  type ScenarioCampagne,
} from './contexte'
import { assainirCarnet, preRemplir } from './preremplissage'
import { verdictDeCampagne, type Verdict } from './defaite-campagne'
import { repriseDeCampagne, type Reprise } from './reprise-campagne'

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
    }

/** Nombre de héros de la campagne : les clés « Player N » en dépendent. */
const nbJoueurs = (campagne: Campagne, monde: World) =>
  Math.max(campagne.equipe?.length ?? 0, monde.players?.length ?? 0, 1)

export function PanneauRecompenses({
  monde,
  gagne,
  onTermine,
}: {
  monde: World | undefined
  gagne: boolean
  /** Appelé quand le joueur a validé : le plateau peut proposer la suite. */
  onTermine: (retourCampagne: boolean) => void
}) {
  const [etat, setEtat] = useState<Etat>({ phase: 'chargement' })
  const [valeurs, setValeurs] = useState<Record<string, string>>({})
  const [enregistrement, setEnregistrement] = useState(false)
  const [echec, setEchec] = useState('')

  useEffect(() => {
    const contexte = lireContexte()
    if (!contexte || !monde) {
      setEtat({ phase: 'absent' })
      return
    }
    let annule = false
    ;(async () => {
      try {
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
          if (!verdict.perdue && !reprise.applicable) {
            setEtat({ phase: 'absent' })
            return
          }
        }
        const champs = champsDuScenario(definition, scenario, campagne.difficulte)
        setEtat({
          phase: 'pret',
          campagne,
          definition,
          scenario,
          champs,
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
    })
  }, [etat, monde])

  useEffect(() => {
    setValeurs(preRemplissage)
  }, [preRemplissage])

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

  const visibles = champs.filter((c) => conditionRemplie(c, monde as World))
  const manquants = visibles.filter((champ) => {
    // Aucun champ n'est affiché à la défaite : en exiger un bloquerait le
    // bouton sur une case que personne ne peut voir ni remplir.
    if (!gagne) return false
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
        termines: gagne
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

      {visibles.length && gagne ? (
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
            />
          ))}
        </div>
      ) : gagne ? (
        <p className="camp-recomp-rien">
          {estFinal
            ? t('Hydra est vaincue. Rien de plus à reporter : tournez la page.')
            : t('Ce scénario ne rapporte rien à reporter dans le carnet.')}
        </p>
      ) : null}

      {echec ? <p className="camp-recomp-echec">{echec}</p> : null}

      <div className="camp-recomp-actions">
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
        {manquants.length ? (
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
}: {
  champ: ChampVictoire
  total: number
  monde: World
  valeurs: Record<string, string>
  poser: (cle: string, valeur: string) => void
  nomJoueur: (i: number) => string
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
        return (
          <div className="camp-champ-ligne" key={cle}>
            {champ.parJoueur ? (
              <span className="camp-champ-joueur">{nomJoueur(joueurId)}</span>
            ) : null}
            {elimine ? (
              <span className="camp-champ-elimine">
                {t('Héros vaincu : il ne participe pas aux récompenses de ce scénario.')}
              </span>
            ) : (
              <Controle champ={champ} cle={cle} valeurs={valeurs} poser={poser} />
            )}
          </div>
        )
      })}
    </div>
  )
}

function Controle({
  champ,
  cle,
  valeurs,
  poser,
}: {
  champ: ChampVictoire
  cle: string
  valeurs: Record<string, string>
  poser: (cle: string, valeur: string) => void
}) {
  const valeur = valeurs[cle] ?? ''

  // Un CHOIX du livret : on montre les cartes, pas une liste déroulante. C'est
  // une décision de jeu, elle mérite qu'on voie ce qu'on prend.
  if (champ.type === 'choix' && champ.options?.length) {
    return (
      <div className="camp-cartes">
        {champ.options.map((id) => (
          <button
            type="button"
            key={id}
            className={`camp-carte${valeur === id ? ' sel' : ''}`}
            aria-pressed={valeur === id}
            onClick={() => poser(cle, valeur === id ? '' : id)}
          >
            <img src={scanUrl(id)} alt={id} loading="lazy" />
          </button>
        ))}
      </div>
    )
  }

  if (champ.format === 'int') {
    return (
      <input
        className="camp-champ-int"
        type="number"
        min={0}
        value={valeur}
        onChange={(e) => poser(cle, e.target.value)}
      />
    )
  }

  // Liste avec options connues : des cases à cocher sur les cartes concernées.
  if (champ.options?.length) {
    const choisies = new Set(deListe(valeur))
    return (
      <div className="camp-cartes">
        {champ.options.map((id) => (
          <button
            type="button"
            key={id}
            className={`camp-carte${choisies.has(id) ? ' sel' : ''}`}
            aria-pressed={choisies.has(id)}
            onClick={() => {
              const suite = new Set(choisies)
              if (suite.has(id)) suite.delete(id)
              else suite.add(id)
              poser(cle, enListe(champ.options!.filter((x) => suite.has(x))))
            }}
          >
            <img src={scanUrl(id)} alt={id} loading="lazy" />
          </button>
        ))}
      </div>
    )
  }

  // Liste sans options connues (les héros engagés, par exemple) : le relevé du
  // moteur en clair, corrigeable à la main.
  return (
    <input
      className="camp-champ-texte"
      type="text"
      value={valeur}
      placeholder={t('rien')}
      onChange={(e) => poser(cle, e.target.value.trim())}
    />
  )
}
