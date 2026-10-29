// Les contrôles de saisie du carnet de campagne : une ligne par champ du livret
// (relevé par le jeu, ou à choisir), partagés par le panneau de récompenses et
// par le parcours de fin de scénario.
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
  deListe,
  enListe,
  joueurElimine,
  optionsProposees,
  type ChampVictoire,
} from './detecteurs'
import { droitSurChamp, peutValider, type DroitCarnet } from './droits-carnet'

export function ChampRecompense({
  champ,
  total,
  monde,
  valeurs,
  poser,
  nomJoueur,
  siege,
  suggestions,
}: {
  champ: ChampVictoire
  total: number
  monde: World
  valeurs: Record<string, string>
  poser: (cle: string, valeur: string) => void
  nomJoueur: (i: number) => string
  siege: number
  suggestions?: Readonly<Record<string, string>>
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
              <Controle champ={champ} cle={cle} valeurs={valeurs} poser={poser} droit={droit} propositions={optionsProposees(champ, joueurId, suggestions)} />
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
  propositions,
}: {
  champ: ChampVictoire
  cle: string
  valeurs: Record<string, string>
  poser: (cle: string, valeur: string) => void
  /** `lecture` rend le contrôle inerte : la case est à quelqu'un d'autre. */
  droit: DroitCarnet
  /** Les cartes proposées par le moteur (champ à `optionsSuggerees`). */
  propositions?: readonly string[]
}) {
  const valeur = valeurs[cle] ?? ''
  const inerte = droit === 'lecture'

  // Un CHOIX dont la liste vient du moteur (MojoMania : un soutien ou une amélioration éligible). Aucune carte éligible :
  // le livret dit « peut », on le dit au joueur plutôt que de laisser un trou.
  if (champ.type === 'choix' && champ.optionsSuggerees) {
    if (!propositions?.length) {
      return <small className="camp-champ-aide">{t('Aucune carte éligible : rien à garder.')}</small>
    }
    return (
      <ListeCartes
        ids={propositions}
        choisie={(id) => valeur === id}
        inerte={inerte}
        basculer={(id) => poser(cle, valeur === id ? '' : id)}
      />
    )
  }

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

  // Un tableau de cases (Cooperation Progress) : le jeu propose, le joueur corrige case par case.
  if (champ.cases?.length) {
    const cochees = new Set(deListe(valeur))
    const toutes = champ.cases.flatMap((l) => l.exigences.map((e) => `${l.titre}: ${e}`))
    return (
      <table className="camp-cases" data-cle={cle}>
        <tbody>
          {champ.cases.map((ligne) => {
            const faites = ligne.exigences.map((e) => cochees.has(`${ligne.titre}: ${e}`))
            return (
              <tr key={ligne.titre} className={faites.every(Boolean) ? 'complete' : ''}>
                <th scope="row">{ligne.titre}</th>
                {ligne.exigences.map((e, i) => (
                  <td key={e}>
                    <button
                      type="button"
                      className={'camp-case' + (faites[i] ? ' cochee' : '')}
                      aria-pressed={faites[i]}
                      disabled={inerte}
                      onClick={() => {
                        const suite = new Set(cochees)
                        const k = `${ligne.titre}: ${e}`
                        if (suite.has(k)) suite.delete(k)
                        else suite.add(k)
                        poser(cle, enListe(toutes.filter((x) => suite.has(x))))
                      }}
                    >
                      {faites[i] ? '✔ ' : ''}
                      {e}
                    </button>
                  </td>
                ))}
              </tr>
            )
          })}
        </tbody>
      </table>
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
