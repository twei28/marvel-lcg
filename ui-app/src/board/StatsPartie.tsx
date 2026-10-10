import { createContext, useContext, useState } from 'react'
import { createPortal } from 'react-dom'
import { t } from './langue'
import { scanUrl } from './card-model'
import { nomAffiche } from './noms-cartes-fr'
import type { CarteStat, CompteurStat, StatsJoueur, StatsPartie as Stats } from './world'
import './stats-partie.css'

/** Les lignes par heros, dans l'ordre de la capture de l'utilisateur (10/10/2026). */
const LIGNES: ReadonlyArray<[CompteurStat, string]> = [
  ['degats_mechant', 'Dégâts au méchant'],
  ['degats_sbires', 'Dégâts aux sbires'],
  ['menace_principale', 'Menace retirée de la manigance principale'],
  ['menace_annexes', 'Menace retirée des manigances annexes'],
  ['degats_evites', 'Dégâts évités'],
  ['attaques_defendues', 'Attaques défendues'],
  ['cartes_jouees', 'Cartes jouées'],
  ['degats_subis', 'Dégâts subis'],
  ['ressources_depensees', 'Ressources dépensées'],
]

const ASPECTS: Record<string, string> = {
  Aggression: 'Agressivité',
  Justice: 'Justice',
  Leadership: 'Commandement',
  Protection: 'Protection',
  "'Pool": 'Pool',
  Pool: 'Pool',
  Determination: 'Détermination',
}

const valeur = (j: StatsJoueur, cle: CompteurStat) => j.compteurs[cle] ?? 0

export function formaterDuree(secondes: number): string {
  const minutes = Math.max(0, Math.round(secondes / 60))
  if (minutes < 60) return `${minutes} min`
  const h = Math.floor(minutes / 60)
  return `${h} h ${String(minutes % 60).padStart(2, '0')}`
}

function sousTitre(j: StatsJoueur): string {
  const aspects = j.aspects.map((a) => t(ASPECTS[a] ?? a)).join(', ')
  const pv = typeof j.pv === 'number' && typeof j.pv_max === 'number' && j.pv_max > 0
    ? `${j.pv}/${j.pv_max} ${t('PV restants')}`
    : ''
  return [aspects, pv].filter(Boolean).join(' · ')
}

/** L'apercu au survol sort du cartouche (coupe par son clip-path) : un portail. */
const Survol = createContext<(id: string | null) => void>(() => {})

function Vignettes({ cartes, vide }: { cartes: CarteStat[]; vide: string }) {
  const survoler = useContext(Survol)
  if (!cartes.length) return <p className="stats-vide">{vide}</p>
  return (
    <ul className="stats-cartes">
      {cartes.map((c) => {
        const nom = nomAffiche({ card_id: c.card_id, name: c.nom })
        return (
          <li
            key={c.card_id}
            className="stats-carte"
            tabIndex={0}
            onMouseEnter={() => survoler(c.card_id)}
            onMouseLeave={() => survoler(null)}
            onFocus={() => survoler(c.card_id)}
            onBlur={() => survoler(null)}
          >
            <span className="stats-carte-vignette">
              <img src={scanUrl(c.card_id)} alt="" loading="lazy" />
              <span className="stats-carte-nombre">×{c.n}</span>
            </span>
            <span className="stats-carte-nom">{nom}</span>
          </li>
        )
      })}
    </ul>
  )
}

const VIDE_PLUS = 'Aucune carte jouée'
const VIDE_MOINS = 'Aucune carte piochée'

function BlocHeros({ j }: { j: StatsJoueur }) {
  return (
    <section className="stats-heros" aria-label={j.heros}>
      <h3 className="stats-heros-nom">{j.heros}</h3>
      {sousTitre(j) ? <p className="stats-heros-sous">{sousTitre(j)}</p> : null}
      <dl className="stats-lignes">
        {LIGNES.map(([cle, libelle]) => (
          <div key={cle} className="stats-ligne">
            <dt>{t(libelle)}</dt>
            <dd>{valeur(j, cle)}</dd>
          </div>
        ))}
      </dl>
      <h4 className="stats-sous-titre">{t('Les plus jouées')}</h4>
      <Vignettes cartes={j.plus_jouees} vide={t(VIDE_PLUS)} />
      <h4 className="stats-sous-titre">{t('Piochées mais peu jouées')}</h4>
      <Vignettes cartes={j.moins_jouees} vide={t(VIDE_MOINS)} />
    </section>
  )
}

function TableauHeros({ joueurs }: { joueurs: StatsJoueur[] }) {
  return (
    <div className="stats-tableau-defile">
      <table className="stats-tableau">
        <thead>
          <tr>
            <th scope="col" />
            {joueurs.map((j) => (
              <th key={j.siege} scope="col">
                <span className="stats-heros-nom">{j.heros}</span>
                {sousTitre(j) ? <span className="stats-heros-sous">{sousTitre(j)}</span> : null}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {LIGNES.map(([cle, libelle]) => (
            <tr key={cle}>
              <th scope="row">{t(libelle)}</th>
              {joueurs.map((j) => (
                <td key={j.siege}>{valeur(j, cle)}</td>
              ))}
            </tr>
          ))}
          <tr className="stats-tableau-cartes">
            <th scope="row">{t('Les plus jouées')}</th>
            {joueurs.map((j) => (
              <td key={j.siege}><Vignettes cartes={j.plus_jouees} vide={t(VIDE_PLUS)} /></td>
            ))}
          </tr>
          <tr className="stats-tableau-cartes">
            <th scope="row">{t('Piochées mais peu jouées')}</th>
            {joueurs.map((j) => (
              <td key={j.siege}><Vignettes cartes={j.moins_jouees} vide={t(VIDE_MOINS)} /></td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  )
}

/** L'onglet Stats de l'ecran de fin. Rien n'est calcule ici sauf des sommes. */
export function StatsPartie({ stats, gagne }: { stats?: Stats; gagne: boolean }) {
  const [apercu, setApercu] = useState<string | null>(null)
  if (!stats || !stats.joueurs?.length) {
    return <p className="stats-vide">{t('Statistiques indisponibles pour cette partie.')}</p>
  }
  const somme = (cle: CompteurStat) => stats.joueurs.reduce((n, j) => n + valeur(j, cle), 0)
  const degats = somme('degats_mechant') + somme('degats_sbires')
  const menace = somme('menace_principale') + somme('menace_annexes')
  const tuiles: Array<[string, string]> = [
    [t('Résultat'), gagne ? t('Gagnée') : t('Perdue')],
    [t('Tours'), String(stats.rounds)],
    [t('Temps'), formaterDuree(stats.temps)],
    [t('Dégâts infligés'), String(degats)],
    [t('Menace retirée'), String(menace)],
  ]
  return (
    <Survol.Provider value={setApercu}>
    <div className="stats-partie">
      <dl className="stats-tuiles">
        {tuiles.map(([libelle, v]) => (
          <div key={libelle} className="stats-tuile">
            <dt>{libelle}</dt>
            <dd>{v}</dd>
          </div>
        ))}
      </dl>
      {stats.joueurs.length > 1 ? (
        <TableauHeros joueurs={stats.joueurs} />
      ) : (
        <BlocHeros j={stats.joueurs[0]} />
      )}
      <p className="stats-note">
        {t('Comptées au joueur dont la carte a agi. Les dégâts évités sont les dégâts des attaques ennemies visant ton héros ou tes alliés qui n’ont pas porté : DEF, Tough et effets de prévention.')}
      </p>
      {apercu
        ? createPortal(
            <img className="stats-apercu" src={scanUrl(apercu)} alt="" data-testid="stats-apercu" />,
            document.body
          )
        : null}
    </div>
    </Survol.Provider>
  )
}
