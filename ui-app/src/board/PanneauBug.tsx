// Le bouton « Signaler un bug » de la barre du plateau, et son formulaire.
//
// C'est ICI que les bugs se produisent, et jusqu'à présent le rapport ne savait
// que se copier ou se télécharger : il fallait ensuite le faire parvenir à la
// main, ce que personne ne faisait. Le formulaire l'envoie au site, où il arrive
// sur /admin avec la capture et le journal.
//
// LE JOURNAL PART TOUT SEUL, sur toute la partie. C'est le cœur de l'affaire :
// une personne qui vient de tomber sur un bug décrit ce qu'elle a vu, pas ce
// que le moteur a fait. Elle n'a rien à cocher ni à choisir.
//
// Le bouton ne s'affiche QUE si un site écoute derrière le moteur, comme le
// tchat : en partie locale il n'y a personne à qui envoyer, et le bouton
// « Log » de la barre couvre déjà ce cas en téléchargeant tout le déroulé.
import { useCallback, useEffect, useRef, useState } from 'react'
import { t } from './langue'
import type { OutilsRapport } from './RapportBug'
import './PanneauBug.css'

/* Réduction de la capture AVANT l'envoi. Une capture brute pèse volontiers 2 à
   4 Mo ; réduite à 1600 px en JPEG, elle tombe sous le demi-mégaoctet sans
   qu'on perde ce qu'il y a à voir — et elle passe sous le plafond de corps du
   moteur, qu'une capture brute faisait sauter sans message utile. */
const LARGEUR_MAX = 1600

async function reduire(fichier: Blob): Promise<string> {
  const image = await createImageBitmap(fichier)
  const facteur = Math.min(1, LARGEUR_MAX / Math.max(image.width, image.height))
  const l = Math.round(image.width * facteur)
  const h = Math.round(image.height * facteur)
  const toile = document.createElement('canvas')
  toile.width = l
  toile.height = h
  toile.getContext('2d')?.drawImage(image, 0, 0, l, h)
  image.close?.()
  return toile.toDataURL('image/jpeg', 0.82)
}

export function PanneauBug({ outils }: { outils: OutilsRapport }) {
  const [actif, setActif] = useState(false)
  const [ouvert, setOuvert] = useState(false)
  const [nom, setNom] = useState('')
  const [description, setDescription] = useState('')
  const [capture, setCapture] = useState('')
  const [envoi, setEnvoi] = useState(false)
  const [mot, setMot] = useState<{ genre: 'ok' | 'non' | 'info'; texte: string } | null>(null)
  const fichierRef = useRef<HTMLInputElement | null>(null)

  useEffect(() => {
    let vivant = true
    fetch('/get_rapport_actif')
      .then((r) => (r.ok ? r.json() : { actif: false }))
      .then((d: { actif?: boolean }) => {
        if (vivant) setActif(!!d.actif)
      })
      .catch(() => {})
    return () => {
      vivant = false
    }
  }, [])

  const poser = useCallback(async (source: Blob | null) => {
    if (!source) {
      setCapture('')
      return
    }
    try {
      setCapture(await reduire(source))
    } catch {
      setCapture('')
      setMot({ genre: 'non', texte: t('Image illisible') })
    }
  }, [])

  // Ctrl+V n'importe où dans le formulaire : c'est le geste qui suit un
  // Impr.écran, et obliger à passer par « Parcourir » ferait enregistrer un
  // fichier pour rien.
  const coller = useCallback(
    (ev: React.ClipboardEvent) => {
      for (const item of Array.from(ev.clipboardData?.items ?? [])) {
        if (item.type?.startsWith('image/')) {
          const f = item.getAsFile()
          if (f) {
            ev.preventDefault()
            void poser(f)
            return
          }
        }
      }
    },
    [poser]
  )

  const envoyer = useCallback(async () => {
    if (!nom.trim() || !description.trim()) {
      setMot({ genre: 'non', texte: t('Il faut un nom et une description.') })
      return
    }
    setEnvoi(true)
    setMot(null)
    const r = await outils.envoyer({ nom: nom.trim(), description: description.trim(), capture })
    setEnvoi(false)
    if (r.ok) {
      setMot({ genre: 'ok', texte: t("Merci, c'est envoyé.") })
      setDescription('')
      setCapture('')
    } else {
      setMot({ genre: 'non', texte: t("L'envoi a échoué :") + ' ' + t(r.erreur ?? '') })
    }
  }, [nom, description, capture, outils])

  if (!actif) return null

  return (
    <>
      <button
        type="button"
        className="bh-bouton pbug-bouton"
        onClick={() => setOuvert(true)}
        title={t('Signaler un bug, avec le journal de la partie')}
      >
        <span aria-hidden="true">🐞</span> {t('Bug')}
      </button>
      {ouvert ? (
        <div
          className="pbug-fond"
          onClick={(e) => {
            if (e.target === e.currentTarget) setOuvert(false)
          }}
        >
          <div className="pbug-panneau" onPaste={coller}>
            <div className="pbug-titre">
              <span>🐞 {t('Signaler un bug')}</span>
              <button
                type="button"
                className="pbug-fermer"
                onClick={() => setOuvert(false)}
                aria-label={t('Fermer')}
              >
                ✕
              </button>
            </div>
            <div className="pbug-corps">
              <label className="pbug-champ">
                <span>{t('Ton nom')}</span>
                <input
                  type="text"
                  maxLength={80}
                  value={nom}
                  onChange={(e) => setNom(e.target.value)}
                  autoFocus
                />
                <small>{t('Pour pouvoir te répondre')}</small>
              </label>
              <label className="pbug-champ">
                <span>{t("Qu'est-ce qui s'est passé ?")}</span>
                <textarea
                  maxLength={4000}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
                <small>
                  {t('Ce que tu faisais, ce que tu attendais, ce qui est arrivé à la place.')}
                </small>
              </label>
              <div className="pbug-champ">
                <span>{t("Capture d'écran")}</span>
                {capture ? (
                  <div className="pbug-apercu">
                    <img src={capture} alt={t("Capture d'écran")} />
                  </div>
                ) : (
                  <div
                    className="pbug-zone"
                    tabIndex={0}
                    role="button"
                    onClick={() => fichierRef.current?.click()}
                  >
                    {t('Colle une image avec Ctrl+V, ou choisis un fichier.')}
                  </div>
                )}
                <input
                  ref={fichierRef}
                  type="file"
                  accept="image/*"
                  hidden
                  onChange={(e) => void poser(e.target.files?.[0] ?? null)}
                />
              </div>
              <p className="pbug-joint">
                {t('Le journal de toute la partie part avec le rapport, tu n’as rien à joindre.')}
              </p>
              {mot ? <div className={`pbug-mot ${mot.genre}`}>{mot.texte}</div> : null}
              <div className="pbug-actions">
                <button
                  type="button"
                  className="pbug-action pbug-envoi"
                  disabled={envoi}
                  onClick={() => void envoyer()}
                >
                  {envoi ? t('Envoi...') : t('Envoyer')}
                </button>
                {capture ? (
                  <button
                    type="button"
                    className="pbug-action"
                    onClick={() => void poser(null)}
                  >
                    {t("Retirer l'image")}
                  </button>
                ) : null}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </>
  )
}
