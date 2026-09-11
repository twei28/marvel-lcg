// Un onglet par heros, en coop.
//
// Choix de l'utilisateur le 11/09/2026 : sur un telephone, on ne tient pas
// quatre tables a la fois. On regarde la sienne, et on bascule du pouce pour
// voir celle d'un autre — mains comprises, le jeu est cooperatif et
// l'information ouverte aide a se coordonner.
//
// En solo, le composant se tait : un onglet unique serait une ligne de bruit
// en haut d'un ecran ou chaque pixel compte.
import type { ReactElement } from 'react'

export function OngletsJoueurs({
  joueurs,
  actif,
  choisir,
}: {
  joueurs: Array<{ id: number; nom: string }>
  actif: number
  choisir: (id: number) => void
}): ReactElement | null {
  if (joueurs.length < 2) return null
  return (
    <div className="portrait-onglets" role="tablist">
      {joueurs.map(({ id, nom }) => (
        <button
          type="button"
          role="tab"
          key={id}
          aria-selected={id === actif}
          className={`portrait-onglet${id === actif ? ' est-actif' : ''}`}
          onClick={() => choisir(id)}
        >
          {nom}
        </button>
      ))}
    </div>
  )
}
