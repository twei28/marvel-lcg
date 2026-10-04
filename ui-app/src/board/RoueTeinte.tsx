// RoueTeinte — la roue de couleurs du fond (Reglages, 04/10/2026).
//
// Une vraie roue, mais qui N'AFFICHE QUE des couleurs ternes (choix de
// l'utilisateur) : l'angle donne la teinte (0 en haut, sens horaire, comme le
// `conic-gradient` qui la dessine), la distance au centre la saturation (0 a
// 18 %). Un curseur regle la luminosite, du tres fonce au gris clair. La table
// change EN DIRECT ; « Couleur d'origine » efface le choix.
//
// Les calculs vivent dans `teinte.ts` (`teinteDuPoint`, `pointDeLaTeinte`) :
// ce composant ne fait que le geste et le dessin.
import { useRef, type KeyboardEvent, type PointerEvent } from 'react'
import { t } from './langue'
import { BORNES, TEINTE_DE_DEPART, bornerTeinte, pointDeLaTeinte, teinteDuPoint, type Teinte } from './teinte'
import './RoueTeinte.css'

/** La luminosite a laquelle la roue est DESSINEE : la vraie, mais jamais si
    sombre que les teintes deviennent invisibles (en dessous, tout est noir). */
const luminositeDuDessin = (l: number) => Math.max(20, l)

export function RoueTeinte({
  valeur,
  changer,
  reinitialiser,
}: {
  /** `undefined` : couleur d'origine (aucun choix). */
  valeur: Teinte | undefined
  changer: (teinte: Teinte) => void
  reinitialiser: () => void
}) {
  const teinte = valeur ?? TEINTE_DE_DEPART
  const roue = useRef<HTMLDivElement | null>(null)
  const lDessin = luminositeDuDessin(teinte.l)
  const fond = [
    `radial-gradient(closest-side, hsl(0 0% ${lDessin}%), hsl(0 0% ${lDessin}% / 0))`,
    `conic-gradient(${Array.from({ length: 13 }, (_, i) => `hsl(${i * 30} ${BORNES.s[1]}% ${lDessin}%)`).join(', ')})`,
  ].join(', ')
  const repere = pointDeLaTeinte(teinte)

  const depuisLePointeur = (evenement: PointerEvent<HTMLDivElement>) => {
    const boite = roue.current?.getBoundingClientRect()
    if (!boite) return
    const rayon = boite.width / 2
    changer(teinteDuPoint(evenement.clientX - boite.left - rayon, evenement.clientY - boite.top - rayon, rayon, teinte.l))
  }

  // Au clavier : gauche/droite tournent la teinte, haut/bas changent la
  // saturation. Une roue qui n'existe qu'a la souris n'existe pas au Tab.
  const auClavier = (evenement: KeyboardEvent<HTMLDivElement>) => {
    const pas = evenement.shiftKey ? 15 : 5
    const suivant =
      evenement.key === 'ArrowRight' ? { ...teinte, h: teinte.h + pas }
      : evenement.key === 'ArrowLeft' ? { ...teinte, h: teinte.h - pas }
      : evenement.key === 'ArrowUp' ? { ...teinte, s: teinte.s + 1 }
      : evenement.key === 'ArrowDown' ? { ...teinte, s: teinte.s - 1 }
      : undefined
    if (!suivant) return
    evenement.preventDefault()
    changer(bornerTeinte(suivant))
  }

  return (
    <div className="roue-teinte">
      <div
        ref={roue}
        className="roue-teinte-disque"
        style={{ background: fond }}
        role="slider"
        tabIndex={0}
        aria-label={t('Teinte du fond')}
        aria-valuemin={0}
        aria-valuemax={359}
        aria-valuenow={teinte.h}
        aria-valuetext={`${teinte.h}°, ${t('saturation')} ${teinte.s} %`}
        onPointerDown={(e) => {
          e.currentTarget.setPointerCapture(e.pointerId)
          depuisLePointeur(e)
        }}
        onPointerMove={(e) => {
          if (e.currentTarget.hasPointerCapture(e.pointerId)) depuisLePointeur(e)
        }}
        onKeyDown={auClavier}
      >
        <span
          className="roue-teinte-repere"
          style={{
            left: `${50 + repere.x * 50}%`,
            top: `${50 + repere.y * 50}%`,
            background: `hsl(${teinte.h} ${teinte.s}% ${teinte.l}%)`,
          }}
          aria-hidden="true"
        />
      </div>
      <label className="roue-teinte-clarte">
        <span>{t('Plus sombre')}</span>
        <input
          type="range"
          min={BORNES.l[0]}
          max={BORNES.l[1]}
          value={teinte.l}
          aria-label={t('Luminosité du fond')}
          onChange={(e) => changer(bornerTeinte({ ...teinte, l: Number(e.target.value) }))}
        />
        <span>{t('Plus clair')}</span>
      </label>
      <button type="button" className="roue-teinte-origine" onClick={reinitialiser} disabled={valeur === undefined}>
        {t('Couleur d’origine')}
      </button>
    </div>
  )
}
