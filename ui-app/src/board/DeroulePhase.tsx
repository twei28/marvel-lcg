// Le cartouche du deroule detaille : une etape a la fois.
//
// FIXE en bas au centre, il ne bouge jamais d'une etape a l'autre : l'oeil sait
// ou lire et la main ou cliquer des le deuxieme tour. Un cartouche colle a la
// carte concernee aurait deplace le bouton a chaque clic.
//
// « Precedent » RELIT, il ne rejoue rien : le monde du moteur ne recule pas.
// C'est « Annuler la derniere action » qui fait cela, et il reste disponible.

import { useEffect, useState } from 'react'
import type { EtapeDeroule, TempsPhase } from './deroule-phase'
import { regleEtape, titreEtape } from './deroule-textes'
import { t } from './langue'
import { useDerouleScene } from './useDerouleScene'

/** Le temps de voir passer une etape technique, sans la lire. */
const DELAI_AUTO_MS = 500

/** Les quatre temps de la carte de reference, dans l'ordre. */
const TEMPS: { cle: TempsPhase; libelle: string }[] = [
  { cle: 'menace', libelle: 'Menace' },
  { cle: 'activations', libelle: 'Activations' },
  { cle: 'distribution', libelle: 'Distribution' },
  { cle: 'revelation', libelle: 'Révélation' },
]

export function DeroulePhase({
  etapes,
  onTerminer,
  onToutDerouler,
}: {
  etapes: EtapeDeroule[]
  /** Appele une fois la derniere etape validee. */
  onTerminer: () => void
  /** « Tout derouler » : les etapes restantes defilent sans attendre. */
  onToutDerouler?: () => void
}) {
  const [index, setIndex] = useState(0)
  // Vrai juste apres un « Precedent » : suspend l'enchainement automatique
  // jusqu'au prochain « Suivant ». Sans cela, revenir en arriere sur une
  // etape technique la ferait repartir en avant aussitot, et le bouton
  // « Precedent » serait inutilisable dessus.
  const [suspendu, setSuspendu] = useState(false)
  // Vrai une fois la derniere etape validee : le cartouche doit alors
  // disparaitre de lui-meme. On ne peut pas compter sur l'appelant pour cela
  // (board.tsx passe un `onTerminer` qui ne fait rien), donc le composant se
  // masque lui-meme plutot que de rester affiche indefiniment sur la
  // derniere etape, y compris pendant le tour du joueur suivant.
  const [termine, setTermine] = useState(false)

  // Signature STABLE du contenu, pas l'identite du tableau : board.tsx
  // recalcule `etapes` par useMemo, mais ses dependances (le monde re-parse en
  // JSON a chaque trame) changent d'identite en permanence meme quand rien
  // n'a bouge. Suivre `etapes` directement aurait reinitialise le cartouche
  // (donc rouvert une phase deja terminee) a chaque carte jouee au tour
  // suivant, pile par-dessus le bouton de fin de tour.
  const signature = etapes.map((e) => e.cle).join('|')

  // Une nouvelle phase repart de sa premiere etape. `termine` doit se
  // reinitialiser ICI, pas seulement `index` : sinon le cartouche ne
  // reapparaitrait plus jamais a la phase du mechant suivante, ce qui est le
  // piege symetrique et pire que le defaut d'origine.
  useEffect(() => {
    setIndex(0)
    setTermine(false)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `signature`
    // resume `etapes` a son CONTENU (les cles, dans l'ordre) ; c'est elle qui
    // doit piloter la reinitialisation, pas l'identite du tableau qui la
    // porte.
  }, [signature])

  const etape = etapes[index]

  const avancer = () => {
    // Hors phase du mechant, etapes est vide et il n'y a rien a avancer : une
    // touche pressee ne doit alors rien declencher.
    if (!etape) return
    setSuspendu(false)
    if (index + 1 >= etapes.length) {
      setTermine(true)
      onTerminer()
      return
    }
    setIndex(index + 1)
  }

  const reculer = () => {
    setSuspendu(true)
    setIndex(index - 1)
  }

  // Enchainement automatique des etapes techniques (`auto`) : la narration
  // du moteur ne se lit pas, elle defile seule apres un court delai. Le
  // minuteur est nettoye au demontage et a chaque changement d'etape (deps
  // ci-dessous), sinon deux minuteurs se superposeraient et la phase
  // sauterait une etape.
  useEffect(() => {
    if (!etape?.auto || suspendu) return
    const minuteur = setTimeout(avancer, DELAI_AUTO_MS)
    return () => clearTimeout(minuteur)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `avancer` est
    // recree a chaque rendu ; c'est `etape` et `suspendu` qui doivent piloter
    // le (re)declenchement du minuteur, pas l'identite de la fonction.
  }, [etape, suspendu])

  useEffect(() => {
    const auClavier = (evenement: KeyboardEvent) => {
      // On ecrit peut-etre ailleurs : le tchat est a portee de main pendant la
      // phase, et un espace tape dedans ne doit pas la faire avancer.
      const cible = evenement.target
      if (
        cible instanceof HTMLElement &&
        (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)
      ) {
        return
      }
      // On ne confisque pas Entree/Espace a un bouton du PLATEAU : seul un
      // element interactif EXTERIEUR au cartouche doit garder son activation
      // au clavier normale. Un bouton du cartouche lui-meme (Suivant,
      // Precedent) reste pris en charge ici, comme avant.
      if (
        cible instanceof HTMLElement &&
        cible.closest('button, a, select, [role="button"]') &&
        !cible.closest('.deroule-phase')
      ) {
        return
      }
      if (evenement.key === 'Enter' || evenement.key === ' ') {
        evenement.preventDefault()
        avancer()
        return
      }
      if (evenement.key === 'Escape' && onToutDerouler) {
        evenement.preventDefault()
        onToutDerouler()
      }
    }
    document.addEventListener('keydown', auClavier)
    return () => document.removeEventListener('keydown', auClavier)
  })

  // Mise en scene de l'etape courante. Appele ici, avec les autres hooks :
  // ce composant a un `return null` plus bas, et un hook place apres lui fait
  // tomber tout le plateau (React compte alors un hook de plus au rendu
  // suivant).
  useDerouleScene(etape, !termine)

  // Le `return null` vient APRES tous les hooks, jamais avant : React exige
  // le meme nombre de hooks, dans le meme ordre, a chaque rendu. Ce composant
  // est monte des que le mode "detaille" est actif, donc hors phase du
  // mechant avec `etapes` vide, puis se remplit sans etre demonte quand la
  // phase commence. Un `return null` place plus haut sauterait le second
  // useEffect a un rendu et le rajouterait au suivant, ce que React refuse.
  // `termine` fait disparaitre le cartouche des la derniere etape validee ;
  // il est remis a false des que `etapes` change (voir le useEffect
  // ci-dessus), donc le deroule reapparait bien a la phase suivante.
  if (!etape || termine) return null

  return (
    <section className="deroule-phase" role="dialog" aria-label={t('Phase du méchant')}>
      <ol className="deroule-temps">
        {TEMPS.map((temps) => (
          <li key={temps.cle} className={temps.cle === etape.temps ? 'est-courant' : ''}>
            {t(temps.libelle)}
          </li>
        ))}
      </ol>

      <p className="deroule-titre">{titreEtape(etape)}</p>
      {etape.consequences.length > 0 ? (
        <ul className="deroule-consequences">
          {etape.consequences.map((consequence) => (
            <li key={consequence.cle}>{consequence.texte}</li>
          ))}
        </ul>
      ) : null}
      <p className="deroule-regle">{regleEtape(etape)}</p>
      {etape.brut ? <p className="deroule-brut">{etape.brut}</p> : null}

      <div className="deroule-boutons">
        {index > 0 ? (
          <button type="button" className="bh-bouton" onClick={reculer}>
            {t('Précédent')}
          </button>
        ) : null}
        <button type="button" className="bh-bouton deroule-suivant" onClick={avancer}>
          {t('Suivant')}
        </button>
      </div>
    </section>
  )
}
