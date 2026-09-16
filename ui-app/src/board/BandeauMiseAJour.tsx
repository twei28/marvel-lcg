// « Une mise à jour du jeu est arrivée. »
//
// ⚠ IL S'INSTALLE, LUI, contrairement au bandeau d'annonce qui passe deux
// secondes toutes les trente. Les deux ne disent pas la même chose : l'annonce
// prévient d'une coupure imminente qu'on ne peut pas rattraper, celle-ci
// constate un état qui dure. Une information permanente doit rester lisible
// tant qu'on n'a pas agi, et elle porte le bouton qui la fait disparaître.
//
// Il ne se ferme pas : tant qu'on n'a pas rechargé, on tourne sur du vieux
// code, et le joueur a le droit de le savoir.
import { t } from './langue'

export function BandeauMiseAJour({ visible, recharger }: {
  visible: boolean
  recharger?: () => void
}) {
  if (!visible) return null
  return (
    <div className="bandeau-maj" role="status">
      <span>{t('Une mise à jour du jeu est arrivée.')}</span>
      <button
        type="button"
        onClick={() => (recharger ? recharger() : window.location.reload())}
      >
        {t('Recharger')}
      </button>
    </div>
  )
}
