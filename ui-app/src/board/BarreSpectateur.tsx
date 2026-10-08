// LA BARRE DU SPECTATEUR : qui l'on regarde, par quels yeux, et comment sortir.
//
// ⚠ POURQUOI ELLE EXISTE. Demande de l'utilisateur, 15/09/2026 : « c'est
// possible d'ajouter un truc qui me permet de voir en live les parties que les
// gens jouent actuellement ? ». Il a choisi de voir « le plateau, en vrai,
// comme si j'y étais », toutes les mains, et de pouvoir CHANGER DE SIÈGE.
//
// Elle dit aussi, en permanence, qu'on ne joue pas. Sans elle, un écran de jeu
// sans boutons ressemble à un écran de jeu CASSÉ : on chercherait pourquoi rien
// ne répond.
//
// ⚠ ELLE NE GARANTIT RIEN, et il ne faut pas s'y tromper. Ce qui interdit
// d'agir est dans le moteur (cookie `spectateur`, `allowed_seats` vide,
// `/post` en 403). Cette barre est ce qu'on VOIT de cette règle.

import { t } from './langue'
import { BoutonReglagesDuJoueur } from './CadreJoueur'

export type BarreSpectateurProps = {
  /** Le siège par les yeux duquel on regarde. */
  siege: number
  /** Combien de sièges la partie compte, d'après le monde rendu. */
  sieges: number
  /** La partie est finie, ou le moteur ne répond plus. */
  terminee?: boolean
  /** Pourquoi elle s'est arrêtée, quand on le sait. */
  raison?: string
}

/**
 * Changer de siège RECHARGE la page, et c'est volontaire.
 *
 * Le siège est porté par l'adresse (`?p=`), que le moteur lit à chaque
 * requête ; tout le plateau en dépend, de la main au surlignage des cibles.
 * Le muter à chaud demanderait de démonter et remonter la partie entière pour
 * gagner une demi-seconde à celui qui regarde.
 */
function allerAuSiege(siege: number) {
  const url = new URL(window.location.href)
  url.searchParams.set('p', String(siege))
  window.location.assign(url.toString())
}

export function BarreSpectateur({ siege, sieges, terminee, raison }: BarreSpectateurProps) {
  const places = Array.from({ length: Math.max(1, sieges) }, (_, rang) => rang)
  return (
    <div className="barre-spectateur" role="status">
      <span className="bs-oeil" aria-hidden="true">
        👁
      </span>
      <span className="bs-mention">{t('Tu regardes cette partie')}</span>

      <BoutonReglagesDuJoueur className="bs-siege" />

      {places.length > 1 ? (
        <span className="bs-sieges">
          {places.map((place) => (
            <button
              key={place}
              type="button"
              className={`bs-siege${place === siege ? ' est-courant' : ''}`}
              aria-pressed={place === siege}
              onClick={() => allerAuSiege(place)}
            >
              {t('Joueur')} {place + 1}
            </button>
          ))}
        </span>
      ) : null}

      {/* ⚠ LE BANDEAU DE FIN, choisi par l'utilisateur parmi trois formes :
          « un bandeau le dit, et je reviens à la liste ». Sans lui, un écran
          qui cesse de bouger ne dit pas s'il est fini ou cassé. */}
      {terminee ? (
        <span className="bs-fin">
          {raison || t('Cette partie est terminée')}
          <a className="bs-retour" href="/suivi">
            {t('Retour à la liste')}
          </a>
        </span>
      ) : null}
    </div>
  )
}
