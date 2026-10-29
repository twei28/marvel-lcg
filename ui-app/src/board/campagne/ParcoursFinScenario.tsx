// ParcoursFinScenario — ce qui se passe quand un scénario de campagne se termine.
//
// Quatre pages, une par « Continuer » (demande de l'utilisateur, 29/10/2026 : tout
// était empilé sur le splash de fin, illisible) :
//   1. Victoire   : le grand mot, le vilain vaincu, les rounds et les héros ;
//   2. Bilan      : ce que le jeu a relevé, et les vrais choix du livret ;
//   3. Carnet     : valeurs corrigeables, journal, état des héros, histoire ;
//   4. Suite      : le scénario suivant (ou la fin de la campagne).
//
// Tout l'état (valeurs, droits, enregistrement) reste dans PanneauRecompenses :
// ce composant ne fait que le présenter, page par page.
import { useEffect, useMemo, useState } from 'react'
import { createPortal } from 'react-dom'
import { t } from '../langue'
import { scanUrl } from '../card-model'
import type { World } from '../world'
import { ChampRecompense } from './ChampRecompense'
import {
  cleCarnet,
  deListe,
  joueurElimine,
  type ChampVictoire,
} from './detecteurs'
import { peutValider } from './droits-carnet'
import type { Campagne, DefinitionCampagne, ScenarioCampagne } from './contexte'
import type { Verdict } from './defaite-campagne'
import type { Reprise } from './reprise-campagne'
import './parcours-fin.css'

export type ResumeFinScenario = {
  heros: Array<{ nom: string; pic?: string }>
  vilains: Array<{ nom: string; pic?: string }>
  rounds?: number
}

type PageId = 'victoire' | 'bilan' | 'carnet' | 'suite'
const PAGES: PageId[] = ['victoire', 'bilan', 'carnet', 'suite']
const NOMS_PAGES: Record<PageId, string> = {
  victoire: 'Victoire',
  bilan: 'Bilan',
  carnet: 'Carnet',
  suite: 'Suite',
}

type OngletCarnet = 'valeurs' | 'journal' | 'heros' | 'histoire'

/** Où atterrir sur l'écran des campagnes : la campagne à ouvrir, et le scénario à lancer d'office. */
export type SuiteDemandee = { campagne?: string; lancer?: string }

export type ParcoursProps = {
  monde: World
  gagne: boolean
  siege: number
  campagne: Campagne
  definition: DefinitionCampagne
  scenario: ScenarioCampagne
  visibles: ChampVictoire[]
  champsVisibles: boolean
  continueSurDefaite: boolean
  verdict: Verdict
  reprise: Reprise
  preuvesRendues: number
  valeurs: Record<string, string>
  poser: (cle: string, valeur: string) => void
  total: number
  nomJoueur: (i: number) => string
  suggestions?: Readonly<Record<string, string>>
  manquants: ChampVictoire[]
  enregistrement: boolean
  echec: string
  envoye: boolean
  modeManuel: boolean
  resume: ResumeFinScenario
  onValider: (suite?: SuiteDemandee) => void
  onEnvoyer: () => Promise<void>
}

/** Le scénario que la campagne propose ensuite, ou rien (dernier scénario, ordre libre). */
export function prochainScenario(
  definition: DefinitionCampagne,
  campagne: Campagne,
  scenario: ScenarioCampagne,
  termine: boolean
): ScenarioCampagne | undefined {
  if (scenario.final || definition.ordre_libre) return undefined
  const finis = new Set([...(campagne.termines ?? []), ...(termine ? [scenario.id] : [])])
  return [...definition.scenarios]
    .sort((a, b) => a.numero - b.numero)
    .find((s) => !finis.has(s.id))
}

type FicheScenario = { villain?: string; sets: string[] }

function joli(id: string): string {
  const mots = id.replace(/_/g, ' ').trim()
  return mots.charAt(0).toUpperCase() + mots.slice(1)
}

function useFicheScenario(id: string | undefined): FicheScenario | undefined {
  const [fiche, setFiche] = useState<FicheScenario | undefined>(undefined)
  useEffect(() => {
    setFiche(undefined)
    if (!id) return
    let annule = false
    void fetch(`/get_scenario_json?${encodeURIComponent(id)}`, { cache: 'no-store' })
      .then((r) => (r.ok ? r.json() : null))
      .then((json: { villain?: string[]; encounter_sets?: string[]; modular_sets?: string[] } | null) => {
        if (annule || !json) return
        setFiche({
          villain: json.villain?.[0],
          sets: [...(json.encounter_sets ?? []), ...(json.modular_sets ?? [])],
        })
      })
      .catch(() => undefined)
    return () => {
      annule = true
    }
  }, [id])
  return fiche
}

function Pastille({ pic, nom }: { pic?: string; nom: string }) {
  return (
    <span
      className="pf-pastille"
      role="img"
      aria-label={nom}
      style={pic ? { backgroundImage: `url("${scanUrl(pic)}")` } : undefined}
    />
  )
}

export function ParcoursFinScenario(p: ParcoursProps) {
  const [page, setPage] = useState<PageId>('victoire')
  const [onglet, setOnglet] = useState<OngletCarnet>('valeurs')
  const estHote = peutValider(p.siege)
  const gagneOuContinue = p.gagne || p.continueSurDefaite
  const estFinal = Boolean(p.scenario.final)
  const suivant = useMemo(
    () => prochainScenario(p.definition, p.campagne, p.scenario, gagneOuContinue),
    [p.definition, p.campagne, p.scenario, gagneOuContinue]
  )
  const fiche = useFicheScenario(p.verdict.perdue || p.reprise.applicable || estFinal ? undefined : suivant?.id)
  const index = PAGES.indexOf(page)
  const auto = p.visibles.filter((c) => c.type === 'auto')
  const choix = p.visibles.filter((c) => c.type !== 'auto')

  const vilain = p.resume.vilains[0]
  const titreVictoire = p.verdict.perdue
    ? t('Campagne perdue')
    : p.gagne
      ? t('Victoire !')
      : t('Défaite')
  const sousTitre = [
    vilain?.nom ? `${vilain.nom} ${p.gagne ? t('vaincu') : ''}`.trim() : '',
    `${t('Scénario')} ${p.scenario.numero} / ${p.definition.scenarios.length}`,
  ]
    .filter(Boolean)
    .join(' · ')

  function suite() {
    if (page === 'bilan' && !estHote) {
      // Un distant envoie SES champs en quittant le bilan : l'hôte les attend.
      void p.onEnvoyer().then(() => setPage('carnet'))
      return
    }
    const prochaine = PAGES[index + 1]
    if (prochaine) setPage(prochaine)
  }

  function retour() {
    const precedente = PAGES[index - 1]
    if (precedente) setPage(precedente)
  }

  // Le texte et le bouton principal de la dernière page, selon ce qui se passe.
  const actionFinale = (() => {
    if (!estHote) return undefined
    if (p.verdict.perdue) return { libelle: t('Consigner la fin de la campagne'), suite: undefined }
    if (p.reprise.applicable) return { libelle: t('Re-préparer les preuves'), suite: undefined }
    if (estFinal) return { libelle: t('Voir la conclusion'), suite: undefined }
    const lancable = suivant && !suivant.assemblee
    return {
      libelle: lancable ? t('Commencer') : t('Choisir la suite'),
      suite: lancable ? ({ lancer: suivant.id } as SuiteDemandee) : undefined,
    }
  })()

  const bloque = page === 'bilan' && estHote && p.manquants.length > 0

  // Dans `document.body` : l'écran de fin porte une transformation qui piégerait un `position: fixed`.
  return createPortal(
    <div className="parcours-fin" role="dialog" aria-modal="true" aria-label={t('Fin du scénario')} data-page={page}>
      <header className="pf-haut">
        <span className="pf-titre-haut">{t('Campagne')}</span>
        <span className="pf-sous-haut">
          {p.campagne.nom} · {t('Scénario')} {p.scenario.numero} / {p.definition.scenarios.length}
        </span>
        <span className="pf-etapes" aria-label={t('Étape')}>
          <b>{t(NOMS_PAGES[page])}</b>
          {PAGES.map((id, i) => (
            <i key={id} className={i === index ? 'on' : ''} />
          ))}
        </span>
      </header>

      <div className="pf-corps">
        {page === 'victoire' ? (
          <PageVictoire
            titre={titreVictoire}
            sousTitre={sousTitre}
            gagne={p.gagne}
            resume={p.resume}
            perdue={p.verdict.perdue}
          />
        ) : null}
        {page === 'bilan' ? (
          <PageBilan {...p} auto={auto} choix={choix} versCarnet={() => { setOnglet('valeurs'); setPage('carnet') }} />
        ) : null}
        {page === 'carnet' ? (
          <PageCarnet {...p} onglet={onglet} setOnglet={setOnglet} suivant={suivant} />
        ) : null}
        {page === 'suite' ? (
          <PageSuite
            {...p}
            suivant={suivant}
            fiche={fiche}
            estFinal={estFinal}
          />
        ) : null}
      </div>

      <footer className="pf-bas">
        {index > 0 ? (
          <button type="button" className="pf-btn pf-btn-sec" onClick={retour} disabled={p.enregistrement}>
            {t('Retour')}
          </button>
        ) : (
          <span />
        )}
        <span className="pf-info">
          {bloque
            ? `${t('À choisir avant de continuer :')} ${p.manquants.map((c) => t(c.libelle)).join(', ')}`
            : page === 'bilan' && !estHote && p.envoye
              ? t("Envoyé. L'hôte valide les récompenses pour la table.")
              : p.echec}
        </span>
        {page === 'suite' ? (
          actionFinale ? (
            <span className="pf-actions">
              {actionFinale.suite ? (
                <button
                  type="button"
                  className="pf-btn pf-btn-sec"
                  disabled={p.enregistrement}
                  onClick={() => p.onValider()}
                >
                  {t('Options du scénario')}
                </button>
              ) : null}
              <button
                type="button"
                className="pf-btn pf-btn-or"
                disabled={p.enregistrement}
                onClick={() => p.onValider(actionFinale.suite)}
              >
                {p.enregistrement ? t('Enregistrement…') : actionFinale.libelle}
              </button>
            </span>
          ) : (
            <span className="pf-attente">
              <span className="pf-point" aria-hidden="true" />
              {t("En attente de l'hôte pour commencer")}
            </span>
          )
        ) : (
          <button type="button" className="pf-btn" disabled={bloque || p.enregistrement} onClick={suite}>
            {t('Continuer')}
          </button>
        )}
      </footer>
    </div>,
    document.body
  )
}

/* ------------------------------------------------------------------ page 1 */

function PageVictoire({
  titre,
  sousTitre,
  gagne,
  resume,
  perdue,
}: {
  titre: string
  sousTitre: string
  gagne: boolean
  resume: ResumeFinScenario
  perdue: boolean
}) {
  const vilain = resume.vilains[0]
  return (
    <div className={`pf-victoire ${gagne ? 'est-victoire' : 'est-defaite'}`}>
      <div
        className="pf-victoire-fond"
        style={vilain?.pic ? { backgroundImage: `url("${scanUrl(vilain.pic)}")` } : undefined}
      />
      <div className="pf-rayures" aria-hidden="true" />
      <div className="pf-victoire-centre">
        <span className="pf-etiquette">{perdue ? t('La campagne s’arrête ici') : t('Scénario terminé')}</span>
        <h2 className="pf-victoire-titre">{titre}</h2>
        <div className="pf-victoire-sous">{sousTitre}</div>
        <div className="pf-puces">
          {resume.rounds ? (
            <span className="pf-puce">
              <b>{resume.rounds}</b> {t('round(s)')}
            </span>
          ) : null}
          {resume.heros.map((h) => (
            <span className="pf-puce" key={h.nom}>
              <Pastille pic={h.pic} nom={h.nom} />
              {h.nom}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

/* ------------------------------------------------------------------ page 2 */

function ResumeLecture({ champ, valeur }: { champ: ChampVictoire; valeur: string }) {
  if (champ.format === 'int') return <span className="pf-grosse-valeur">{valeur || '0'}</span>
  const ids = deListe(valeur)
  if (champ.options?.length && ids.length) {
    return (
      <span className="pf-miniatures">
        {ids.map((id) => (
          <img key={id} src={scanUrl(id)} alt={id} loading="lazy" />
        ))}
      </span>
    )
  }
  return <span className="pf-texte-valeur">{valeur || t('rien')}</span>
}

function PageBilan(
  p: ParcoursProps & {
    auto: ChampVictoire[]
    choix: ChampVictoire[]
    versCarnet: () => void
  }
) {
  const { auto, choix } = p
  return (
    <div className="pf-bilan">
      {p.verdict.perdue ? (
        <p className="pf-alerte">
          {p.verdict.texte}{' '}
          {p.gagne
            ? t('Le scénario est gagné, mais la campagne s’arrête ici.')
            : t('Ce scénario ne se rejoue pas : la campagne s’arrête ici.')}
        </p>
      ) : null}
      {p.reprise.applicable ? (
        <div className="pf-alerte">
          <p>{p.reprise.texte}</p>
          <p>
            {p.preuvesRendues > 0
              ? `${p.preuvesRendues} ${p.preuvesRendues > 1 ? t('preuves te seront rendues') : t('preuve te sera rendue')}`
              : t('Aucune preuve ne te sera rendue : le Conseil n’a jamais fini vidé de ses secrets.')}
          </p>
        </div>
      ) : null}
      {p.continueSurDefaite ? (
        <p className="pf-alerte">{t('Scénario perdu : la campagne continue avec les gains de la défaite.')}</p>
      ) : null}
      {p.champsVisibles && p.modeManuel && auto.length ? (
        <p className="pf-alerte">
          {t(
            'Mode manuel : le moteur ne surveille plus la table, les cases « relevé par le jeu » restent à remplir à la main.'
          )}
        </p>
      ) : null}
      {!p.champsVisibles ? null : !p.visibles.length ? (
        <div className="pf-panneau pf-panneau-seul">
          <p className="pf-vide">
            {p.scenario.final
              ? t('Hydra est vaincue. Rien de plus à reporter : tournez la page.')
              : t('Ce scénario ne rapporte rien à reporter dans le carnet.')}
          </p>
        </div>
      ) : (
        <div className={`pf-bilan-colonnes${auto.length && choix.length ? '' : ' une-seule'}`}>
          {auto.length ? (
            <section className="pf-panneau">
              <h3 className="pf-h">{t('Ce que la partie a produit')}</h3>
              {auto.map((champ) => (
                <div className="pf-constat" key={champ.cle + (champ.condition ?? '')}>
                  <div className="pf-constat-tete">
                    <span>{t(champ.libelle)}</span>
                    <span className="pf-auto">{t('relevé par le jeu')}</span>
                  </div>
                  {(champ.parJoueur ? [...Array(p.total).keys()] : [0]).map((i) => (
                    <div className="pf-constat-ligne" key={i}>
                      {champ.parJoueur ? <span className="pf-qui">{p.nomJoueur(i)}</span> : null}
                      {champ.parJoueur && joueurElimine(p.monde, i) ? (
                        <span className="pf-texte-valeur">{t('Héros vaincu')}</span>
                      ) : (
                        <ResumeLecture champ={champ} valeur={p.valeurs[cleCarnet(champ, i)] ?? ''} />
                      )}
                    </div>
                  ))}
                  {champ.aide ? <p className="pf-aide">{t(champ.aide)}</p> : null}
                </div>
              ))}
              <button type="button" className="pf-lien" onClick={p.versCarnet}>
                {t('Une valeur ne te semble pas juste ? Corriger dans le carnet')}
              </button>
            </section>
          ) : null}
          {choix.length ? (
            <section className="pf-panneau">
              <h3 className="pf-h">{t('Tes choix')}</h3>
              {choix.map((champ) => (
                <ChampRecompense
                  key={champ.cle + (champ.condition ?? '')}
                  champ={champ}
                  total={p.total}
                  monde={p.monde}
                  valeurs={p.valeurs}
                  poser={p.poser}
                  nomJoueur={p.nomJoueur}
                  siege={p.siege}
                  suggestions={p.suggestions}
                />
              ))}
            </section>
          ) : null}
        </div>
      )}
    </div>
  )
}

/* ------------------------------------------------------------------ page 3 */

function PageCarnet(
  p: ParcoursProps & {
    onglet: OngletCarnet
    setOnglet: (o: OngletCarnet) => void
    suivant: ScenarioCampagne | undefined
  }
) {
  const onglets: Array<[OngletCarnet, string]> = [
    ['valeurs', 'Valeurs du carnet'],
    ['journal', 'Journal des scénarios'],
    ['heros', 'Les héros'],
    ['histoire', 'Histoire du livret'],
  ]
  const epilogue = p.scenario.pages?.epilogue ?? []
  const futurs = useMemo(() => {
    const apres = p.definition.scenarios.filter((s) => s.numero > p.scenario.numero)
    return apres.flatMap((s) => (s.victoire ?? []).map((c) => ({ champ: c, scenario: s })))
  }, [p.definition, p.scenario])

  return (
    <div className="pf-carnet">
      <div className="pf-onglets" role="tablist">
        {onglets.map(([id, nom]) => (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={p.onglet === id}
            className={p.onglet === id ? 'on' : ''}
            onClick={() => p.setOnglet(id)}
          >
            {t(nom)}
          </button>
        ))}
      </div>
      <div className="pf-panneau pf-carnet-corps">
        {p.onglet === 'valeurs' ? (
          <div>
            <h3 className="pf-h">{t('Valeurs du carnet')}</h3>
            {p.visibles.length && p.champsVisibles ? (
              p.visibles.map((champ) => (
                <ChampRecompense
                  key={champ.cle + (champ.condition ?? '')}
                  champ={champ}
                  total={p.total}
                  monde={p.monde}
                  valeurs={p.valeurs}
                  poser={p.poser}
                  nomJoueur={p.nomJoueur}
                  siege={p.siege}
                  suggestions={p.suggestions}
                />
              ))
            ) : (
              <p className="pf-vide">{t('Ce scénario ne rapporte rien à reporter dans le carnet.')}</p>
            )}
            {futurs.length ? (
              <>
                <h4 className="pf-sous-h">{t('Se remplit aux scénarios suivants')}</h4>
                <ul className="pf-futurs">
                  {futurs.map(({ champ, scenario }) => (
                    <li key={`${scenario.id}-${champ.cle}`}>
                      <span>{t(champ.libelle)}</span>
                      <span className="pf-quand">
                        {t('scénario')} {scenario.numero}
                      </span>
                    </li>
                  ))}
                </ul>
              </>
            ) : null}
          </div>
        ) : null}
        {p.onglet === 'journal' ? (
          <div>
            <h3 className="pf-h">{t('Journal de campagne')}</h3>
            <ol className="pf-journal">
              {[...p.definition.scenarios]
                .sort((a, b) => a.numero - b.numero)
                .map((s) => {
                  const fini = s.id === p.scenario.id ? p.gagne || p.continueSurDefaite : (p.campagne.termines ?? []).includes(s.id)
                  const statut = fini
                    ? 'fini'
                    : s.id === p.suivant?.id
                      ? 'prochain'
                      : 'futur'
                  return (
                    <li key={s.id} className={`est-${statut}${s.id === p.scenario.id ? ' est-courant' : ''}`}>
                      <strong>
                        {t('Scénario')} {s.numero} — {s.nom_fr ?? s.nom}
                        <span className={`pf-tag ${statut}`}>
                          {statut === 'fini' ? t('Victoire') : statut === 'prochain' ? t('Prochain') : t('À venir')}
                        </span>
                      </strong>
                      {s.resume ? <p>{s.resume}</p> : null}
                    </li>
                  )
                })}
            </ol>
          </div>
        ) : null}
        {p.onglet === 'heros' ? (
          <div>
            <h3 className="pf-h">{t('État des héros')}</h3>
            <div className="pf-heros">
              {[...Array(p.total).keys()].map((i) => {
                const lignes = p.visibles.filter((c) => c.parJoueur)
                return (
                  <section key={i} className="pf-hero">
                    {p.resume.heros[i]?.pic ? (
                      <img src={scanUrl(p.resume.heros[i]!.pic!)} alt={p.nomJoueur(i)} loading="lazy" />
                    ) : null}
                    <div>
                      <h4>{p.nomJoueur(i)}</h4>
                      {lignes.length ? (
                        <ul>
                          {lignes.map((c) => {
                            const valeur = p.valeurs[cleCarnet(c, i)] ?? ''
                            const ids = deListe(valeur)
                            return (
                              <li key={c.cle}>
                                <span>{t(c.libelle)}</span>
                                {ids.length ? (
                                  <span className="pf-miniatures">
                                    {ids.map((id) => (
                                      <img key={id} src={scanUrl(id)} alt={id} loading="lazy" />
                                    ))}
                                  </span>
                                ) : (
                                  <span className="pf-texte-valeur">{valeur || '—'}</span>
                                )}
                              </li>
                            )
                          })}
                        </ul>
                      ) : (
                        <p className="pf-vide">{t('Rien de particulier pour ce héros.')}</p>
                      )}
                    </div>
                  </section>
                )
              })}
            </div>
          </div>
        ) : null}
        {p.onglet === 'histoire' ? (
          <div>
            <h3 className="pf-h">{t('Histoire du livret')}</h3>
            <div className="pf-histoire">
              {epilogue.length && p.gagne ? (
                <div className="pf-bd">
                  {epilogue.map((fichier) => (
                    <img
                      key={fichier}
                      src={`/public/stories/${p.definition.code}/${fichier}`}
                      alt=""
                      loading="lazy"
                    />
                  ))}
                </div>
              ) : null}
              <div className="pf-histoire-texte">
                {p.suivant?.enjeu ? (
                  <>
                    <span className="pf-etiquette">
                      {t('Ce qui est en jeu au scénario')} {p.suivant.numero}
                    </span>
                    <p>{p.suivant.enjeu}</p>
                  </>
                ) : p.scenario.enjeu ? (
                  <p>{p.scenario.enjeu}</p>
                ) : null}
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  )
}

/* ------------------------------------------------------------------ page 4 */

function PageSuite({
  suivant,
  fiche,
  estFinal,
  ...p
}: ParcoursProps & {
  suivant: ScenarioCampagne | undefined
  fiche: FicheScenario | undefined
  estFinal: boolean
}) {
  if (p.verdict.perdue || estFinal || p.reprise.applicable || !suivant) {
    const perdue = p.verdict.perdue
    return (
      <div className={`pf-fin ${perdue ? 'est-perdue' : 'est-gagnee'}`}>
        <div>
          <span className="pf-etiquette">{p.campagne.nom}</span>
          <h2 className="pf-fin-titre">
            {perdue
              ? t('Campagne perdue')
              : p.reprise.applicable
                ? p.reprise.titre || t('Ce scénario est à re-préparer')
                : estFinal
                  ? t('Campagne terminée !')
                  : t('La suite de la campagne')}
          </h2>
          <p className="pf-fin-texte">
            {perdue
              ? p.verdict.texte
              : p.reprise.applicable
                ? p.reprise.texte
                : estFinal
                  ? t('Le carnet de la campagne reste consultable depuis le menu.')
                  : t('Choisis le prochain scénario sur l’écran des campagnes.')}
          </p>
        </div>
      </div>
    )
  }
  return (
    <div className="pf-suite">
      <div
        className="pf-suite-fond"
        style={fiche?.villain ? { backgroundImage: `url("${scanUrl(fiche.villain)}")` } : undefined}
      />
      <div className="pf-suite-texte">
        <span className="pf-etiquette">
          {t('Prochain scénario')} · {suivant.numero} / {p.definition.scenarios.length}
        </span>
        <h2 className="pf-suite-titre">{suivant.nom_fr ?? suivant.nom}</h2>
        {suivant.resume ? <p className="pf-suite-resume">{suivant.resume}</p> : null}
        {fiche?.sets.length ? (
          <div className="pf-bloc">
            <span className="pf-etiquette">{t('Sets de rencontre')}</span>
            <div className="pf-puces">
              {fiche.sets.map((s) => (
                <span className="pf-puce" key={s}>
                  {joli(s)}
                </span>
              ))}
            </div>
          </div>
        ) : null}
        {suivant.enjeu ? (
          <div className="pf-bloc">
            <span className="pf-etiquette">{t('Ce qui est en jeu')}</span>
            <p className="pf-suite-enjeu">{suivant.enjeu}</p>
          </div>
        ) : null}
      </div>
      {fiche?.villain ? <img className="pf-suite-carte" src={scanUrl(fiche.villain)} alt="" /> : null}
    </div>
  )
}
