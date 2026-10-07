// La page « Revoir une partie » : deposer un fichier .marvelreplay, voir la
// fiche de la partie, puis la relire sur le vrai plateau avec la barre de
// lecture (pause, pas a pas, vitesse, reperes, point de vue, journal).
import { useCallback, useEffect, useMemo, useState, useSyncExternalStore, type ReactNode } from 'react'
import { t } from '../langue'
import { texteSignificatif } from '../HistoriquePartie'
import { COULEURS_JOUEURS } from '../CoucheCurseurs'
import { FichierInvalide, lireRelecture, type Relecture } from './fichier'
import { activerLecteur, Lecteur, VITESSES } from './lecteur'

type TypeLecteur = Lecteur
import { BandeauRelecture } from './BandeauRelecture'
import './relecture.css'

const nomHeros = (relecture: Relecture, siege: number) =>
  relecture.entete.joueurs[siege]?.heros ||
  relecture.trames[0]?.monde.players?.[siege]?.area_hero?.[0]?.name?.replace(/^\W*/, '') ||
  `${t('Joueur')} ${siege + 1}`

const couleur = (siege: number) => COULEURS_JOUEURS[siege % COULEURS_JOUEURS.length]

function libelleResultat(resultat: string | undefined): string {
  if (resultat === 'victoire') return t('Victoire')
  if (resultat === 'defaite') return t('Défaite')
  return t('Partie inachevée')
}

function useControle(lecteur: TypeLecteur) {
  return useSyncExternalStore(
    (rappel) => lecteur.ecouterControle(rappel),
    () => lecteur.lireControle()
  )
}

function Depot({ charger, erreur }: { charger: (fichier: File) => void; erreur?: string }) {
  const [survol, setSurvol] = useState(false)
  return (
    <main className="relecture-page">
      <h1>{t('Revoir une partie')}</h1>
      <div
        className={`relecture-depot${survol ? ' est-survolee' : ''}`}
        onDragOver={(e) => {
          e.preventDefault()
          setSurvol(true)
        }}
        onDragLeave={() => setSurvol(false)}
        onDrop={(e) => {
          e.preventDefault()
          setSurvol(false)
          const fichier = e.dataTransfer.files[0]
          if (fichier) charger(fichier)
        }}
      >
        <p>{t('Dépose ton fichier .marvelreplay ici')}</p>
        {/* Indispensable au telephone, ou l'on ne peut rien glisser. */}
        <label className="relecture-choisir">
          {t('ou choisis-le')}
          <input
            type="file"
            accept=".marvelreplay"
            onChange={(e) => {
              const fichier = e.target.files?.[0]
              if (fichier) charger(fichier)
            }}
          />
        </label>
      </div>
      {/* La derniere partie jouee sur CETTE table, finie ou non : c'est aussi
          le chemin d'une partie abandonnee, qui n'a pas d'ecran de fin. */}
      <a className="relecture-derniere" href="/get_enregistrement" download="partie.marvelreplay">
        {t('Télécharger la dernière partie jouée sur cette table')}
      </a>
      {erreur ? (
        <p className="relecture-erreur" role="alert">
          {erreur}
        </p>
      ) : null}
    </main>
  )
}

function Fiche({ relecture, lancer }: { relecture: Relecture; lancer: () => void }) {
  const { entete } = relecture
  return (
    <div className="relecture-fiche" role="dialog" aria-label={t('Fiche de la partie')}>
      <h2>{entete.scenario || t('Partie')}</h2>
      <p>
        {entete.expert ? t('Expert') : t('Standard')}
        {entete.date ? ` · ${entete.date}` : ''}
      </p>
      <ul>
        {relecture.entete.joueurs.map((joueur, siege) => (
          <li key={siege} style={{ color: couleur(siege) }}>
            {nomHeros(relecture, siege)}
            {joueur.deck && joueur.deck !== nomHeros(relecture, siege) ? ` (${joueur.deck})` : ''}
          </li>
        ))}
      </ul>
      <p>
        {libelleResultat(entete.resultat)}
        {entete.rounds ? ` · ${t('%1 rounds').replace('%1', String(entete.rounds))}` : ''}
      </p>
      {entete.version ? <p className="relecture-version">{t('Version du jeu')} {entete.version}</p> : null}
      <button type="button" className="relecture-bouton-lecture" onClick={lancer} autoFocus>
        ▶ {t('Lecture')}
      </button>
    </div>
  )
}

function Journal({ lecteur, relecture }: { lecteur: TypeLecteur; relecture: Relecture }) {
  const { index } = useControle(lecteur)
  const lignes = useMemo(() => {
    const resultat: { index: number; texte: string; siege?: number; round: number }[] = []
    let precedent = ''
    relecture.trames.forEach(({ monde }, i) => {
      // Le meme nettoyage que le journal du plateau : sans « [(01,01001b) Peter Parker] ».
      const texte = texteSignificatif(monde.prompt) ?? ''
      if (!texte || texte === precedent) return
      precedent = texte
      const siege = (monde.players ?? []).findIndex((j) => {
        const nom = j.area_hero?.[0]?.name?.replace(/^\W*/, '')
        return nom !== undefined && nom !== '' && texte.includes(nom)
      })
      resultat.push({ index: i, texte, siege: siege === -1 ? undefined : siege, round: monde.round_id })
    })
    return resultat
  }, [relecture])
  let courante = -1
  lignes.forEach((ligne, n) => {
    if (ligne.index <= index) courante = n
  })
  useEffect(() => {
    document.querySelector('.relecture-journal .est-courante')?.scrollIntoView({ block: 'nearest' })
  }, [courante])
  return (
    <aside className="relecture-journal" aria-label={t('Journal de la partie')}>
      <ol>
        {lignes.map((ligne, n) => (
          <li key={ligne.index} className={n === courante ? 'est-courante' : undefined}>
            <button
              type="button"
              onClick={() => lecteur.aller(ligne.index)}
              style={ligne.siege === undefined ? undefined : { borderLeftColor: couleur(ligne.siege) }}
            >
              <span className="relecture-journal-round">R{ligne.round}</span> {ligne.texte}
            </button>
          </li>
        ))}
      </ol>
    </aside>
  )
}

function Barre({ lecteur, relecture }: { lecteur: TypeLecteur; relecture: Relecture }) {
  const controle = useControle(lecteur)
  const { index, total } = controle
  const fin = total - 1
  const position = (i: number) => `${fin === 0 ? 0 : (i / fin) * 100}%`
  const monde = relecture.trames[index]?.monde
  return (
    <div className="relecture-barre" role="toolbar" aria-label={t('Contrôles de relecture')}>
      <div className="relecture-progression">
        <input
          type="range"
          min={0}
          max={fin}
          value={index}
          aria-label={t('Position dans la partie')}
          onChange={(e) => lecteur.aller(Number(e.target.value))}
        />
        {lecteur.reperes.map((repere) => (
          <button
            key={`${repere.genre}-${repere.index}`}
            type="button"
            className={`relecture-repere est-${repere.genre}`}
            style={{ left: position(repere.index) }}
            title={repere.libelle}
            aria-label={repere.libelle}
            onClick={() => lecteur.aller(repere.index)}
          />
        ))}
      </div>
      <div className="relecture-commandes">
        <button type="button" onClick={() => lecteur.precedent()} title={t('Action précédente')} aria-label={t('Action précédente')}>
          ⏮
        </button>
        <button
          type="button"
          className="relecture-bouton-lecture"
          onClick={() => lecteur.basculerLecture()}
          aria-label={controle.enLecture ? t('Pause') : t('Lecture')}
        >
          {controle.enLecture ? '⏸' : '▶'}
        </button>
        <button type="button" onClick={() => lecteur.suivant()} title={t('Action suivante')} aria-label={t('Action suivante')}>
          ⏭
        </button>
        <span className="relecture-situation">
          {monde ? (monde.round_id >= 1 ? `${t('Round')} ${monde.round_id}` : t('Mise en place')) : ''} · {index + 1}/{total}
        </span>
        <label>
          {t('Vitesse')}
          <select value={controle.vitesse} onChange={(e) => lecteur.reglerVitesse(Number(e.target.value))}>
            {VITESSES.map((v) => (
              <option key={v} value={v}>
                ×{v}
              </option>
            ))}
          </select>
        </label>
        <label>
          {t('Pause max')}
          <select value={controle.pauseMaxS} onChange={(e) => lecteur.reglerPauseMax(Number(e.target.value))}>
            {[1, 2, 3, 5, 10, 30].map((s) => (
              <option key={s} value={s}>
                {s} s
              </option>
            ))}
          </select>
        </label>
        <label>
          {t('Vue')}
          <select value={controle.pointDeVue} onChange={(e) => lecteur.reglerPointDeVue(Number(e.target.value))}>
            {relecture.entete.joueurs.map((_, siege) => (
              <option key={siege} value={siege}>
                {nomHeros(relecture, siege)}
              </option>
            ))}
          </select>
        </label>
        <button
          type="button"
          onClick={() => lecteur.basculerMuet()}
          aria-pressed={controle.muet}
          aria-label={controle.muet ? t('Activer les sons') : t('Couper les sons')}
          title={controle.muet ? t('Activer les sons') : t('Couper les sons')}
        >
          {controle.muet ? '🔇' : '🔊'}
        </button>
      </div>
    </div>
  )
}

export function PageRelecture({ rendrePartie }: { rendrePartie: (siege: number) => ReactNode }) {
  const [relecture, setRelecture] = useState<Relecture>()
  const [lecteur, setLecteur] = useState<TypeLecteur>()
  const [erreur, setErreur] = useState<string>()
  const [ficheVue, setFicheVue] = useState(false)
  const [journalOuvert, setJournalOuvert] = useState(false)

  const charger = useCallback((fichier: File) => {
    setErreur(undefined)
    fichier
      .arrayBuffer()
      .then(lireRelecture)
      .then((lue) => {
        const nouveau = new Lecteur(lue, `${fichier.name}-${fichier.size}-${fichier.lastModified}`)
        activerLecteur(nouveau)
        setRelecture(lue)
        setLecteur(nouveau)
        setFicheVue(false)
      })
      .catch((cause: unknown) => {
        setErreur(cause instanceof FichierInvalide ? t(cause.message) : t('Ce fichier ne peut pas être relu.'))
      })
  }, [])

  useEffect(() => () => activerLecteur(undefined), [])

  useEffect(() => {
    if (!lecteur || !ficheVue) return
    const auClavier = (e: KeyboardEvent) => {
      const cible = e.target
      if (cible instanceof HTMLElement && (cible.tagName === 'INPUT' || cible.tagName === 'SELECT' || cible.tagName === 'TEXTAREA')) {
        if (!(cible instanceof HTMLInputElement && cible.type === 'range')) return
      }
      if (e.key === ' ') {
        e.preventDefault()
        lecteur.basculerLecture()
      } else if (e.key === 'ArrowRight') {
        e.preventDefault()
        lecteur.suivant()
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault()
        lecteur.precedent()
      }
    }
    document.addEventListener('keydown', auClavier)
    return () => document.removeEventListener('keydown', auClavier)
  }, [lecteur, ficheVue])

  const pointDeVue = useSyncExternalStore(
    (rappel) => lecteur?.ecouterControle(rappel) ?? (() => undefined),
    () => lecteur?.lireControle().pointDeVue ?? 0
  )

  if (!relecture || !lecteur) return <Depot charger={charger} erreur={erreur} />

  return (
    <div className="relecture-cadre">
      {rendrePartie(pointDeVue)}
      {ficheVue ? null : (
        <Fiche
          relecture={relecture}
          lancer={() => {
            setFicheVue(true)
            lecteur.lecture()
          }}
        />
      )}
      <button
        type="button"
        className="relecture-bascule-journal"
        aria-expanded={journalOuvert}
        onClick={() => setJournalOuvert((o) => !o)}
      >
        {t('Journal')}
      </button>
      {journalOuvert ? <Journal lecteur={lecteur} relecture={relecture} /> : null}
      {ficheVue ? <BandeauRelecture lecteur={lecteur} relecture={relecture} /> : null}
      <Barre lecteur={lecteur} relecture={relecture} />
    </div>
  )
}
