// CoucheMeteo — la météo de Storm sur le nouveau plateau.
//
// Transposé de l'ancien client (js/marvel/cards.js + ui.js) : les Soutiens
// météo de Storm changent le fond de la table via une iframe plein écran
// (effets HTML autonomes déjà présents dans public/effects/weather/).
//   36002 Clear Skies -> rien, 36003 Hurricane -> pluie,
//   36004 Thunderstorm -> orage, 36005 Blizzard -> neige.
// Ici on ne dépend pas d'un événement de rendu : on regarde ce qui est EN JEU
// à chaque monde reçu, donc la météo survit à un rechargement de page.
// Activable au choix (localStorage marvel-board-meteo, actif par défaut).
import { useMemo } from 'react'
import type { World, WorldCard } from './world'

const METEO_PAR_CARTE: Record<string, string> = {
  '36003': 'rain',
  '36004': 'storm',
  '36005': 'snow',
}

export const CLE_METEO = 'marvel-board-meteo'

export function lireMeteoActive(): boolean {
  try {
    return window.localStorage.getItem(CLE_METEO) !== 'off'
  } catch {
    return true
  }
}

/** La météo dictée par les cartes en jeu (zones des joueurs), ou ''. */
function meteoDuMonde(world: World | undefined): string {
  if (!world) return ''
  let trouvee = ''
  const parcourir = (valeur: unknown) => {
    if (trouvee) return
    if (Array.isArray(valeur)) {
      for (const element of valeur) parcourir(element)
      return
    }
    if (typeof valeur !== 'object' || valeur === null) return
    const carte = valeur as Partial<WorldCard>
    if (typeof carte.card_id === 'string' && METEO_PAR_CARTE[carte.card_id]) {
      trouvee = METEO_PAR_CARTE[carte.card_id]
      return
    }
    for (const enfant of Object.values(carte)) parcourir(enfant)
  }
  for (const joueur of world.players ?? []) parcourir(joueur)
  return trouvee
}

export function CoucheMeteo({ world, active }: { world: World | undefined; active: boolean }) {
  const meteo = useMemo(() => meteoDuMonde(world), [world])
  if (!active || !meteo) return null
  return (
    <iframe
      className="couche-meteo"
      src={`/effects/weather/${meteo}.html`}
      title=""
      aria-hidden="true"
      tabIndex={-1}
    />
  )
}
