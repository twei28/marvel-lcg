// EntreesVolets.tsx — les volets du bord droit (Aide, Feuillets, Tchat, Journal ; Ville et Assemblée en campagne), rangés dans le
// menu « … » du téléphone.
//
// Demande de l'utilisateur (16/11/2026, après le message d'un joueur) : « le bouton chat est sur la main... le bouton journal, aide et tout,
// il gâche trop les trucs principaux, c'est-à-dire la main et les piles ». Sur téléphone, leurs languettes sont donc masquées
// (portrait.css) et chaque volet s'ouvre depuis une ligne de ce menu. Le menu n'existe qu'en portrait : hors de lui, ces lignes sont
// cachées (board.css `.bh-volet`), la barre du PC garde ses languettes.
//
// Chaque ligne ne fait que CLIQUER la languette du volet (masquée, toujours dans la page) : le geste, l'état ouvert/fermé et les
// raccourcis restent ceux du volet, rien n'est dupliqué. Une ligne n'existe que si sa languette existe (les Feuillets n'ont pas
// toujours de contenu). Le nombre de messages non lus du tchat est repris sur sa ligne.
import { useEffect, useState, type ReactElement } from 'react'
import { t } from '../langue'

type Entree = { classe: string; libelle: string; nonLus?: string }

/** L'ordre des lignes, et leur libellé (les autres volets de campagne reprennent le texte de leur languette). */
const VOLETS: ReadonlyArray<{ classe: string; libelle: string }> = [
  { classe: 'volet-aide-languette', libelle: 'Aide' },
  { classe: 'volet-feuillets-languette', libelle: 'Feuillets' },
  { classe: 'volet-tchat-languette', libelle: 'Tchat' },
  { classe: 'volet-journal-languette', libelle: 'Journal' },
  { classe: 'volet-ville-languette', libelle: '' },
  { classe: 'volet-assemblee-languette', libelle: '' },
]

export function lireEntrees(racine: ParentNode = document): Entree[] {
  const entrees: Entree[] = []
  for (const volet of VOLETS) {
    const languette = racine.querySelector<HTMLElement>(`.${volet.classe}`)
    if (!languette) continue
    const texte = (languette.querySelector('[class$="-languette-texte"]')?.textContent ?? languette.textContent ?? '').trim()
    const pastille = languette.querySelector('.volet-tchat-pastille')?.textContent?.trim()
    entrees.push({ classe: volet.classe, libelle: volet.libelle ? t(volet.libelle) : texte, nonLus: pastille || undefined })
  }
  return entrees
}

export function EntreesVolets(): ReactElement | null {
  const [entrees, setEntrees] = useState<Entree[]>([])
  useEffect(() => {
    // Seulement sur le plateau PORTRAIT (telephone) : sur PC les languettes restent a leur place et la barre n'a pas de doublon.
    if (!document.body.classList.contains('mode-plateau-portrait')) return
    setEntrees(lireEntrees())
  }, [])
  if (entrees.length === 0) return null
  return (
    <>
      {entrees.map((entree) => (
        <button
          type="button"
          key={entree.classe}
          className="bh-bouton bh-volet"
          data-ferme-menu=""
          onClick={() => document.querySelector<HTMLElement>(`.${entree.classe}`)?.click()}
        >
          {entree.libelle}
          {entree.nonLus ? <span className="bh-volet-non-lus">{entree.nonLus}</span> : null}
        </button>
      ))}
    </>
  )
}
