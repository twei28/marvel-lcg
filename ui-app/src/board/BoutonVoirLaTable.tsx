// « Voir la table » : efface d'un coup toutes les fenêtres de décision pour
// regarder le plateau derrière, puis les ramène (signalement Yarro,
// 30/09/2026 : « un moyen de masquer les fenêtres, ou un focus sur la table »).
//
// Bascule, pas maintien : au doigt, garder le doigt sur le bouton interdit de
// toucher la table. Les fenêtres restent en fantôme (CSS `body.voir-la-table`)
// et la table reste cliquable à travers.
//
// ⚠ Le composant lit le DOM plutôt que l'état du jeu : une quinzaine de
// panneaux distincts peuvent s'empiler, et celui qui s'ajoutera demain doit
// être couvert sans qu'on pense à le brancher ici.
import { useEffect, useRef, useState } from 'react'
import { t } from './langue'

// ⚠ À garder identique à la liste de `body.voir-la-table` dans board.css.
export const FENETRES_DE_DECISION =
  '.demande-centrale, .assistant-action, .plateau-selecteur, .deroule-phase, .plateau-regardees-voile'

export const CLASSE_VOIR_LA_TABLE = 'voir-la-table'

export function BoutonVoirLaTable() {
  const [presente, setPresente] = useState(false)
  const [efface, setEfface] = useState(false)
  const nombre = useRef(0)

  useEffect(() => {
    let image = 0
    const lire = () => {
      image = 0
      const n = document.querySelectorAll(FENETRES_DE_DECISION).length
      // Une fenêtre de plus = une décision nouvelle : on la montre, sans quoi
      // le joueur raterait une question posée pendant qu'il regardait la table.
      if (n > nombre.current) setEfface(false)
      nombre.current = n
      setPresente(n > 0)
    }
    const observateur = new MutationObserver(() => {
      if (image === 0) image = requestAnimationFrame(lire)
    })
    observateur.observe(document.body, { childList: true, subtree: true })
    lire()
    return () => {
      observateur.disconnect()
      if (image !== 0) cancelAnimationFrame(image)
    }
  }, [])

  const actif = presente && efface
  useEffect(() => {
    document.body.classList.toggle(CLASSE_VOIR_LA_TABLE, actif)
    return () => document.body.classList.remove(CLASSE_VOIR_LA_TABLE)
  }, [actif])

  // Toujours present dans l'en-tete, grise sans fenetre : un bouton qui
  // apparait et disparait decalerait « Annuler » et les autres a chaque question.
  return (
    <button
      type="button"
      className={`bh-bouton bh-voir-table${actif ? ' est-actif' : ''}`}
      aria-pressed={actif}
      disabled={!presente}
      title={t('Efface les fenêtres pour voir la table')}
      onClick={() => setEfface((courant) => !courant)}
    >
      {actif ? t('Réafficher les fenêtres') : t('Voir la table')}
    </button>
  )
}
