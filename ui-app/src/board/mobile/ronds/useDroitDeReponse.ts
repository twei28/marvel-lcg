// PERIL en multijoueur (decision Q68, 24/10/2026) : pendant la carte a Peril d'un joueur, SEUL ce joueur peut reagir. Le panneau
// de phase (DeroulePhase) pose son numero dans `data-peril-joueur` sur <html> ; ici on le lit et on suit ses changements.
import { useEffect, useState } from 'react'

function lire(): number | undefined {
  const valeur = document.documentElement.dataset.perilJoueur
  if (valeur === undefined) return undefined
  const joueur = Number(valeur)
  return Number.isFinite(joueur) ? joueur : undefined
}

export function usePerilJoueur(): number | undefined {
  const [joueur, setJoueur] = useState<number | undefined>(lire)
  useEffect(() => {
    const surveillant = new MutationObserver(() => setJoueur(lire()))
    surveillant.observe(document.documentElement, { attributes: true, attributeFilter: ['data-peril-joueur'] })
    setJoueur(lire())
    return () => surveillant.disconnect()
  }, [])
  return joueur
}
