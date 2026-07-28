import { createRoot } from 'react-dom/client'
import { version } from 'react'
import '../styles/tokens.css'

function Vitrine() {
  return (
    <main>
      <h1>Vitrine du design system</h1>
      <p>
        Cette page n'est pas un ecran de jeu : elle montre les tokens partages
        par les ecrans anciens et nouveaux. Aucune partie n'est en cours.
      </p>
      <p>Rendue par React {version}.</p>
    </main>
  )
}

const cible = document.getElementById('vitrine')
if (!cible) throw new Error('Element #vitrine introuvable dans vitrine.html')
createRoot(cible).render(<Vitrine />)
