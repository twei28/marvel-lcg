// La page « Revoir une partie » : deposer un fichier .marvelreplay, voir la
// fiche de la partie, puis la relire sur le vrai plateau avec la barre de
// lecture (pause, pas a pas, vitesse, reperes, point de vue, journal).
import { useCallback, useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react'
import { t } from '../langue'
import { texteSignificatif } from '../HistoriquePartie'
import { COULEURS_JOUEURS } from '../CoucheCurseurs'
import { FichierInvalide, lireRelecture, type Relecture } from './fichier'
import { activerLecteur, Lecteur, VITESSES } from './lecteur'

type TypeLecteur = Lecteur
import { BandeauRelecture } from './BandeauRelecture'
import { CadreJoueur } from '../CadreJoueur'
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

type MaPartie = { n: number; nom: string }

/** « partie-20261008-143005-Rhino.marvelreplay » -> « 08/10/2026 14:30 · Rhino ». */
export function libelleDePartie(nom: string): string {
  const m = /^partie-(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})\d{2}-(.*)\.marvelreplay$/.exec(nom)
  return m ? `${m[3]}/${m[2]}/${m[1]} ${m[4]}:${m[5]} · ${m[6]}` : nom
}

/**
 * MES DERNIERES PARTIES (08/10/2026) : les parties terminees de l'hote de cette
 * table, rangees par le moteur (engine/enregistrement.py). La table ne les rend
 * qu'a son hote ; ailleurs (moteur local, invite) la liste est vide et ne
 * s'affiche pas.
 */
function MesParties({ ouvrir }: { ouvrir: (donnees: ArrayBuffer, nom: string) => void }) {
  const [parties, setParties] = useState<MaPartie[]>([])
  useEffect(() => {
    let vivant = true
    fetch('/get_mes_parties', { cache: 'no-store' })
      .then((r) => (r.ok ? r.json() : []))
      .then((liste: unknown) => {
        if (vivant && Array.isArray(liste)) setParties(liste as MaPartie[])
      })
      .catch(() => undefined)
    return () => {
      vivant = false
    }
  }, [])
  if (parties.length === 0) return null
  return (
    <section className="relecture-mes-parties">
      <h2>{t('Mes dernières parties')}</h2>
      <ul>
        {parties.map((partie) => (
          <li key={partie.nom}>
            <span>{libelleDePartie(partie.nom)}</span>
            <button
              type="button"
              className="relecture-bouton-lecture"
              onClick={() => {
                void fetch(`/get_ma_partie?n=${partie.n}`, { cache: 'no-store' })
                  .then((r) => (r.ok ? r.arrayBuffer() : Promise.reject(new Error('absente'))))
                  .then((donnees) => ouvrir(donnees, partie.nom))
                  .catch(() => undefined)
              }}
            >
              ▶ {t('Revoir')}
            </button>
            <a href={`/get_ma_partie?n=${partie.n}`} download={partie.nom}>
              {t('Télécharger')}
            </a>
          </li>
        ))}
      </ul>
    </section>
  )
}

function Depot({
  charger,
  ouvrir,
  erreur,
}: {
  charger: (fichier: File) => void
  ouvrir: (donnees: ArrayBuffer, nom: string) => void
  erreur?: string
}) {
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
      <MesParties ouvrir={ouvrir} />
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

function Barre({ lecteur, relecture, visible }: { lecteur: TypeLecteur; relecture: Relecture; visible: boolean }) {
  const controle = useControle(lecteur)
  const { index, total } = controle
  const fin = total - 1
  const position = (i: number) => `${fin === 0 ? 0 : (i / fin) * 100}%`
  const monde = relecture.trames[index]?.monde
  return (
    <div
      className={`relecture-barre${visible ? '' : ' est-cachee'}`}
      role="toolbar"
      aria-label={t('Contrôles de relecture')}
      aria-hidden={visible ? undefined : true}
    >
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
          <select
            value={controle.vueAuto ? 'auto' : controle.pointDeVue}
            onChange={(e) => lecteur.reglerPointDeVue(e.target.value === 'auto' ? 'auto' : Number(e.target.value))}
          >
            <option value="auto">{t('Auto (qui a la main)')}</option>
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

type ActionClavier = 'basculerLecture' | 'suivant' | 'precedent' | 'roundSuivant' | 'roundPrecedent' | 'vitessePlus' | 'vitesseMoins'

/** La commande de lecture d'une touche, ou undefined si la touche n'en est pas une. */
export function actionDuClavier(e: Pick<KeyboardEvent, 'key' | 'shiftKey' | 'ctrlKey' | 'altKey' | 'metaKey'>): ActionClavier | undefined {
  if (e.ctrlKey || e.altKey || e.metaKey) return undefined
  if (e.key === ' ') return 'basculerLecture'
  if (e.key === 'ArrowRight') return e.shiftKey ? 'roundSuivant' : 'suivant'
  if (e.key === 'ArrowLeft') return e.shiftKey ? 'roundPrecedent' : 'precedent'
  if (e.key === '+' || e.key === '=') return 'vitessePlus'
  if (e.key === '-' || e.key === '_') return 'vitesseMoins'
  return undefined
}

export const BARRE_DELAI_MS = 2000
export const BARRE_ZONE_BAS_PX = 140

/**
 * LA BARRE SE CACHE TOUTE SEULE (08/10/2026, elle cachait la main) : 2 s sans
 * bouger la souris, elle s'en va ; elle revient quand la souris approche du bas
 * de l'ecran, ou a chaque touche. Elle reste tant que la souris est dessus ou
 * qu'une de ses listes est ouverte.
 */
function useBarreQuiSeCache(active: boolean) {
  const [visible, setVisible] = useState(true)
  const visibleRef = useRef(true)
  visibleRef.current = visible
  const minuteur = useRef<number | undefined>(undefined)
  const armer = useCallback(() => {
    window.clearTimeout(minuteur.current)
    minuteur.current = window.setTimeout(() => {
      const survolee = document.querySelector('.relecture-barre:hover, .relecture-barre :focus-visible, .relecture-barre select:focus')
      if (survolee) armer()
      else setVisible(false)
    }, BARRE_DELAI_MS)
  }, [])
  const montrer = useCallback(() => {
    setVisible(true)
    armer()
  }, [armer])
  useEffect(() => {
    if (!active) return
    armer()
    // Visible, tout mouvement la garde ; cachee, seule l'approche du bas la rappelle.
    const bouger = (e: MouseEvent) => {
      if (e.clientY >= window.innerHeight - BARRE_ZONE_BAS_PX) montrer()
      else if (visibleRef.current) armer()
    }
    window.addEventListener('mousemove', bouger, true)
    return () => {
      window.removeEventListener('mousemove', bouger, true)
      window.clearTimeout(minuteur.current)
    }
  }, [active, armer, montrer])
  return { visible, montrer }
}

export function PageRelecture() {
  const [relecture, setRelecture] = useState<Relecture>()
  const [lecteur, setLecteur] = useState<TypeLecteur>()
  const [erreur, setErreur] = useState<string>()
  const [ficheVue, setFicheVue] = useState(false)
  const [journalOuvert, setJournalOuvert] = useState(false)

  const ouvrir = useCallback((donnees: ArrayBuffer, identite: string) => {
    setErreur(undefined)
    lireRelecture(donnees)
      .then((lue) => {
        const nouveau = new Lecteur(lue, identite)
        activerLecteur(nouveau)
        setRelecture(lue)
        setLecteur(nouveau)
        setFicheVue(false)
      })
      .catch((cause: unknown) => {
        setErreur(cause instanceof FichierInvalide ? t(cause.message) : t('Ce fichier ne peut pas être relu.'))
      })
  }, [])
  const charger = useCallback(
    (fichier: File) => {
      void fichier.arrayBuffer().then((donnees) => ouvrir(donnees, `${fichier.name}-${fichier.size}-${fichier.lastModified}`))
    },
    [ouvrir]
  )

  useEffect(() => () => activerLecteur(undefined), [])

  const { visible: barreVisible, montrer: montrerBarre } = useBarreQuiSeCache(ficheVue)

  // LE CLAVIER, COMME UNE VIDEO (08/10/2026) : Espace lecture/pause, fleches
  // action precedente/suivante, Maj+fleches round precedent/suivant, + et -
  // la vitesse. Lu sur la FENETRE en capture : avant la vitre du plateau
  // (vitre-spectateur.ts), qui arrete ses raccourcis a lui.
  useEffect(() => {
    if (!lecteur || !ficheVue) return
    const auClavier = (e: KeyboardEvent) => {
      const cible = e.target
      if (cible instanceof HTMLElement && (cible.tagName === 'INPUT' || cible.tagName === 'SELECT' || cible.tagName === 'TEXTAREA')) {
        if (!(cible instanceof HTMLInputElement && cible.type === 'range')) return
      }
      const action = actionDuClavier(e)
      if (!action) return
      e.preventDefault()
      e.stopPropagation()
      montrerBarre()
      lecteur[action]()
    }
    window.addEventListener('keydown', auClavier, true)
    return () => window.removeEventListener('keydown', auClavier, true)
  }, [lecteur, ficheVue, montrerBarre])

  const pointDeVue = useSyncExternalStore(
    (rappel) => lecteur?.ecouterControle(rappel) ?? (() => undefined),
    () => lecteur?.lireControle().pointDeVue ?? 0
  )

  if (!relecture || !lecteur) return <Depot charger={charger} ouvrir={ouvrir} erreur={erreur} />

  return (
    <div className="relecture-cadre">
      {/* Le plateau, dans le cadre du joueur : sa taille d'ecran, ses reglages (CadreJoueur.tsx). */}
      <CadreJoueur src={`${window.location.pathname}?relecture&cadre`} siege={pointDeVue} />
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
      <Barre lecteur={lecteur} relecture={relecture} visible={barreVisible || !ficheVue} />
    </div>
  )
}
