// Le bandeau colle en haut du portrait : ou on en est, et qui doit agir.
//
// Trois segments, comme la barre du plateau PC depuis le 11/09/2026 et comme
// le « Turn 1 | PLAYER PHASE | STEVE ROGERS TO ACT » de l'autre site. C'est la
// premiere chose qu'on lit en reprenant son telephone.
//
// Contrairement au brief d'origine, ce composant ne calcule PAS lui-meme qui
// agit : libelleQuiAgit() a besoin de { aNous, connecte, demande }, qui ne
// sont pas dans BoardProps (et ne doivent pas y entrer, ce sont des details
// de connexion, pas de plateau). Le plateau PC calcule deja ce libelle pour sa
// propre barre ; on le lui fait simplement passer.
import type { ReactElement } from 'react'
import { libellePhase, libelleRound } from '../etat-partie'
import type { World } from '../world'

export function BandeauPortrait({
  monde,
  quiAgit,
}: {
  monde: World | undefined
  quiAgit?: string
}): ReactElement {
  return (
    <header className="portrait-bandeau" role="status">
      <strong>{libelleRound(monde)}</strong>
      <span>{libellePhase(monde)}</span>
      {quiAgit ? <em>{quiAgit}</em> : null}
    </header>
  )
}
