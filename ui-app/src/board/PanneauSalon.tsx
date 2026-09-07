// Le tchat des comptes, sur la table.
//
// Il n'existait que sur l'ecran de PREPARATION : partie lancee, plus moyen de
// se parler sans tout quitter. Meme canal, meme fil, meme historique — c'est
// bien le tchat du salon qui continue ici, pas un second tchat.
//
// Le bouton ne s'affiche QUE si le tchat repond : partie locale sans site
// derriere, ou siege tenu par un invite plutot que par le titulaire du compte,
// et il n'y a rien a montrer. Un bouton qui n'ouvre rien vaut moins que pas de
// bouton du tout.
import { useEffect, useRef, useState } from 'react'
import { t } from './langue'
import { direSalon, lireSalon, type MessageSalon } from './salon'

// Rythme de relecture. Le moteur ne renvoie que la SUITE du fil, mais chaque
// appel le fait rebondir vers le site : on ne le paie au prix fort que lorsque
// le fil est SOUS LES YEUX. Ferme, il suffit de savoir qu'il s'est dit quelque
// chose, et vingt secondes de retard sur une pastille ne genent personne.
const PERIODE_OUVERT_MS = 4000
const PERIODE_FERME_MS = 20000
/** Au-dela, le fil affiche ne garde que les derniers : c'est un tchat, pas un log. */
const MAX_MESSAGES = 80

export function PanneauSalon() {
  const [actif, setActif] = useState(false)
  const [ouvert, setOuvert] = useState(false)
  const [messages, setMessages] = useState<MessageSalon[]>([])
  const [moi, setMoi] = useState<string | undefined>(undefined)
  const [brouillon, setBrouillon] = useState('')
  /** Messages arrives pendant que le panneau etait ferme. */
  const [nonLus, setNonLus] = useState(0)
  /** Le tchat a repondu qu'il n'existe pas ici : on cesse de le deranger. */
  const [muet, setMuet] = useState(false)
  /**
   * Vrai des que le tchat a repondu present au moins une fois. Sert a
   * distinguer une coupure (reseau tombe en cours de partie) d'une table qui
   * n'a jamais eu de tchat (partie locale, siege d'invite) : la premiere
   * merite un mot a l'utilisateur, la seconde reste muette comme avant.
   */
  const futActif = useRef(false)
  const curseur = useRef(0)
  /** Identifiants deja recus, pour dedoublonner (voir la boucle plus bas). */
  const idsConnus = useRef<Set<number>>(new Set())
  const ref = useRef<HTMLDivElement>(null)
  const filRef = useRef<HTMLDivElement>(null)
  const ouvertRef = useRef(ouvert)
  ouvertRef.current = ouvert

  // Un seul minuteur, qui tourne meme panneau ferme : sans lui, la pastille de
  // messages non lus n'aurait rien a compter.
  //
  // ⚠ IL S'ARRETE DES LA PREMIERE REPONSE NEGATIVE. Une table sans site derriere
  // (partie locale) ou un siege d'invite ne verront jamais de tchat : continuer
  // a demander, c'etait un appel toutes les quatre secondes jusqu'a la fin de la
  // partie, pour rien, et chacun faisait rebondir le moteur vers le site.
  useEffect(() => {
    if (muet) return
    let vivant = true
    let minuteur = 0
    const battre = async () => {
      const vue = await lireSalon(curseur.current)
      if (!vivant) return
      setActif(vue.actif)
      if (!vue.actif) {
        // Coupe A LA SOURCE plutot que d'attendre que `muet` fasse le tour de
        // React : entre les deux, le minuteur aurait encore tire.
        window.clearInterval(minuteur)
        setMuet(true)
        return
      }
      futActif.current = true
      if (vue.pseudo) setMoi(vue.pseudo)
      curseur.current = vue.dernier
      if (vue.messages.length === 0) return
      // Dedoublonne par identifiant : un curseur decale ou un effet relance
      // (l'ouverture du panneau change `ouvert`, donc les deps de cet effet)
      // peut renvoyer un message deja recu. Sans ca, React se plaint de cles
      // dupliquees et le fil peut afficher deux fois le meme message.
      const inedits = vue.messages.filter((m) => !idsConnus.current.has(m.id))
      if (inedits.length === 0) return
      for (const m of inedits) idsConnus.current.add(m.id)
      setMessages((courants) => [...courants, ...inedits].slice(-MAX_MESSAGES))
      if (!ouvertRef.current) {
        // Les notres ne comptent pas : on sait ce qu'on vient d'ecrire.
        const desAutres = inedits.filter((m) => m.pseudo !== vue.pseudo).length
        if (desAutres) setNonLus((n) => n + desAutres)
      }
    }
    void battre()
    minuteur = window.setInterval(
      () => void battre(),
      ouvert ? PERIODE_OUVERT_MS : PERIODE_FERME_MS
    )
    return () => {
      vivant = false
      window.clearInterval(minuteur)
    }
  }, [muet, ouvert])

  // Fermeture au clic exterieur et a Echap, comme le panneau Historique.
  useEffect(() => {
    if (!ouvert) return
    const fermer = (evenement: PointerEvent) => {
      const cible = evenement.target
      if (cible instanceof Node && ref.current?.contains(cible)) return
      setOuvert(false)
    }
    const fermerClavier = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') setOuvert(false)
    }
    document.addEventListener('pointerdown', fermer)
    document.addEventListener('keydown', fermerClavier)
    return () => {
      document.removeEventListener('pointerdown', fermer)
      document.removeEventListener('keydown', fermerClavier)
    }
  }, [ouvert])

  // Le fil se lit par le bas : c'est le dernier message qui compte.
  useEffect(() => {
    if (!ouvert || !filRef.current) return
    filRef.current.scrollTop = filRef.current.scrollHeight
  }, [ouvert, messages])

  // Une table qui n'a jamais eu de tchat (partie locale, siege d'invite) ne
  // montre toujours rien : c'est la regle qui porte tout ce composant. Mais
  // une coupure APRES coup (reseau tombe en cours de partie) le disait
  // seulement en silence, indiscernable pour le joueur d'« il n'y a jamais eu
  // de tchat ici ». Un mot sobre, et un moyen de reessayer : remettre `muet`
  // a faux relance l'effet ci-dessus (il est dans ses dependances), qui
  // reprend le fil la ou `curseur` l'a laisse.
  if (!actif) {
    if (!futActif.current) return null
    return (
      <div className="salon-partie salon-deconnecte">
        <span className="bh-bouton bh-salon-etat" role="status">
          <span aria-hidden="true">💬</span> {t('Tchat déconnecté')}
        </span>
        <button type="button" className="bh-bouton" onClick={() => setMuet(false)}>
          {t('Réessayer')}
        </button>
      </div>
    )
  }

  const envoyer = async () => {
    const texte = brouillon.trim()
    if (!texte) return
    // Vide tout de suite : reecrire par-dessus un champ qui se vide en retard
    // est le plus sur moyen de perdre ce qu'on tape.
    setBrouillon('')
    const parti = await direSalon(texte)
    // Reparti pour rien : on rend le texte plutot que de le perdre en silence.
    if (!parti) setBrouillon(texte)
  }

  return (
    <div className="salon-partie" ref={ref}>
      <button
        type="button"
        className={`bh-bouton bh-salon${ouvert ? ' est-ouvert' : ''}`}
        aria-expanded={ouvert}
        onClick={() => {
          setOuvert((actuel) => !actuel)
          setNonLus(0)
        }}
        title={t('Parler aux autres joueurs')}
      >
        <span aria-hidden="true">💬</span> {t('Tchat')}
        {nonLus > 0 ? <em className="salon-pastille">{nonLus}</em> : null}
      </button>

      {ouvert ? (
        <section className="salon-panneau" role="dialog" aria-label={t('Tchat')}>
          <div className="salon-fil" ref={filRef}>
            {messages.length === 0 ? (
              <p className="salon-vide">{t('Rien encore. Dis quelque chose.')}</p>
            ) : (
              messages.map((message) => (
                <p
                  key={message.id}
                  className={`salon-message${message.pseudo === moi ? ' est-moi' : ''}`}
                >
                  <b>{message.pseudo}</b>
                  <span>{message.texte}</span>
                </p>
              ))
            )}
          </div>
          <form
            className="salon-saisie"
            onSubmit={(evenement) => {
              evenement.preventDefault()
              void envoyer()
            }}
          >
            <input
              type="text"
              value={brouillon}
              maxLength={500}
              placeholder={t('Ton message')}
              aria-label={t('Ton message')}
              onChange={(evenement) => setBrouillon(evenement.target.value)}
            />
            <button type="submit" className="bh-bouton" disabled={!brouillon.trim()}>
              {t('Envoyer')}
            </button>
          </form>
        </section>
      ) : null}
    </div>
  )
}
