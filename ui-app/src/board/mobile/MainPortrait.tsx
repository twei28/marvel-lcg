// La main, en rangee qui defile horizontalement.
//
// Choix de l'utilisateur le 11/09/2026, contre l'eventail : les cartes gardent
// une taille LISIBLE et on fait glisser le doigt. C'est la seule zone du
// portrait ou les cartes se lisent a vue ; tout le reste de la table est en
// petit avec ses chiffres a cote.
//
// ECART ASSUME avec CarteAvecChiffres (regle centrale du chantier : jamais de
// chiffre sur l'illustration) : ici on rend ScanCard EN DIRECT, sans retirer
// stats/jauge/allyHp/schemeThreat. La regle protege les VIGNETTES (petites,
// lues via leurs chiffres a cote) ; la main n'en est pas une, elle se lit a
// vue comme une vraie carte, coût et texte imprimes compris. Une carte de
// main n'est de toute facon pas en jeu : le moteur ne lui connait ni PV ni
// stat courante (ces champs viennent de l'unite POSEE), donc ScanCard n'a
// rien a superposer dessus dans les faits.
import type { ReactElement } from 'react'
import { ScanCard } from '../../components/ScanCard'
import { t } from '../langue'
import type { UniteAffichee } from '../zones'
import { useAppuiLong } from './useAppuiLong'

/**
 * Une carte de la main, avec son geste. `useAppuiLong` tient un minuteur par
 * appel : il ne peut donc pas etre invoque depuis la boucle `.map` du parent
 * (nombre de crochets variable d'un rendu a l'autre) — d'ou ce composant,
 * un par carte, qui l'appelle une seule fois.
 */
function CarteMainPortrait({
  unite,
  onOuvrir,
  onJouer,
}: {
  unite: UniteAffichee
  onOuvrir: (unite: UniteAffichee) => void
  onJouer?: (unite: UniteAffichee) => void
}): ReactElement {
  const appui = useAppuiLong(onJouer ? () => onJouer(unite) : undefined)
  return (
    <span className="main-portrait-carte" {...appui.gestes}>
      <ScanCard
        {...unite.carte}
        highlight={false}
        onSelect={() => {
          // Le maintien vient de jouer la carte : le clic qui suit le
          // relachement du doigt ne doit pas AUSSI l'ouvrir, sinon un seul
          // geste ferait les deux actions a la fois.
          if (appui.vientDeDeclencher()) return
          onOuvrir(unite)
        }}
      />
    </span>
  )
}

export function MainPortrait({
  unites,
  onOuvrir,
  onJouer,
}: {
  unites: UniteAffichee[]
  onOuvrir: (unite: UniteAffichee) => void
  /** Appui long : jouer la carte directement, sans passer par la lecture. */
  onJouer?: (unite: UniteAffichee) => void
}): ReactElement {
  if (unites.length === 0) {
    return <p className="portrait-vide main-portrait-vide">{t('Ta main est vide')}</p>
  }
  return (
    <div className="main-portrait-bloc">
      <div className="main-portrait defile">
        {unites.map((unite) => (
          <CarteMainPortrait key={unite.cle} unite={unite} onOuvrir={onOuvrir} onJouer={onJouer} />
        ))}
      </div>
      <span className="portrait-chiffre main-portrait-compte">
        <b>{unites.length}</b>
        <small>{t('en main')}</small>
      </span>
    </div>
  )
}
