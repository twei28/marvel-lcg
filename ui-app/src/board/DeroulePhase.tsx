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
import { TraitCible } from './TraitCible'
import { useDerouleScene } from './useDerouleScene'

/** Le temps de voir passer une etape technique, sans la lire. */
const DELAI_AUTO_MS = 500

/** Le temps de lire un boost a capacite avant le suivant. */
const DELAI_BOOST_MS = 1500

/**
 * Les cinq temps de la carte de reference, dans l'ordre.
 *
 * Le mechant et ses sbires sont deux moments distincts du tour (le vilain
 * s'active AVANT ses sbires) : les fondre dans un seul « Activations »
 * cachait ou l'on en etait. Arbitrage de l'utilisateur, qui a decrit la
 * phase exactement dans ces termes.
 */
const TEMPS: { cle: TempsPhase; libelle: string }[] = [
  { cle: 'menace', libelle: 'Menace' },
  { cle: 'mechant', libelle: 'Méchant' },
  { cle: 'sbires', libelle: 'Sbires' },
  { cle: 'distribution', libelle: 'Distribution' },
  { cle: 'revelation', libelle: 'Révélation' },
]

export function DeroulePhase({
  etapes,
  onSuivant,
  onTerminer,
  onToutDerouler,
}: {
  etapes: EtapeDeroule[]
  /**
   * Appele a CHAQUE etape validee (clic, clavier ou enchainement auto), avant
   * de passer a la suivante. C'est lui qui relache le moteur cote reseau
   * (`avancerMaintenant`) : optionnel pour ne pas casser les appelants qui ne
   * pilotent pas le moteur (tests, previsualisation).
   */
  onSuivant?: () => void
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
  // disparaitre de lui-meme. `onTerminer` relache desormais vraiment le
  // moteur (board.tsx), mais cela ne le fait pas disparaitre de l'ecran pour
  // autant : c'est toujours au composant de se masquer, plutot que de rester
  // affiche indefiniment sur la derniere etape, y compris pendant le tour du
  // joueur suivant.
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
  // piege symetrique et pire que le defaut d'origine. `suspendu` doit s'y
  // remettre a zero aussi : un « Precedent » cliqué sur la phase precedente
  // le met a vrai, et si la phase se termine autrement qu'en revalidant
  // jusqu'au bout (le moteur peut avancer seul), rien d'autre ne le
  // redescend. Sans cette reinitialisation, la premiere etape technique de
  // la phase suivante n'attendrait plus son minuteur.
  useEffect(() => {
    setIndex(0)
    setTermine(false)
    setSuspendu(false)
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
    // Relache le moteur AVANT de savoir si c'est la derniere etape : chaque
    // validation (clic, clavier, enchainement auto) correspond au plus a une
    // trame retenue cote moteur (`avancerMaintenant` ne fait rien sans trame
    // en attente), donc l'appeler ici a chaque fois est sans risque, y
    // compris sur la derniere etape ou `onTerminer` l'appelle une seconde
    // fois juste apres.
    onSuivant?.()
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
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `etape` est
    // reconstruit a chaque trame du moteur (meme piege que plus haut avec
    // `signature`, et que useDerouleScene.ts et TraitCible.tsx) : en
    // dependre remettrait ce minuteur a zero en boucle, plus vite qu'il ne
    // peut arriver a echeance, et l'etape technique ne defilerait jamais
    // seule. `etape?.cle` identifie l'etape, `avancer` est recree a chaque
    // rendu et n'a pas a piloter le (re)declenchement.
  }, [etape?.cle, suspendu])

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

  // Combien de boosts sont deja retournes sur l'etape courante. Ils
  // s'enchainent SEULS : c'est l'etape qui attend la validation, pas chaque
  // carte. Une attaque a trois boosts couterait sinon quatre clics.
  const [boostsMontres, setBoostsMontres] = useState(0)

  useEffect(() => {
    setBoostsMontres(etape?.boosts.length ? 1 : 0)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `etape` est
    // reconstruit a chaque trame du moteur (meme piege que plus haut avec
    // `signature`, et que useDerouleScene.ts et TraitCible.tsx) : en
    // dependre remettrait `boostsMontres` a 1 en boucle et aucun boost ne
    // s'enchainerait jamais. `etape?.cle` identifie l'etape, et
    // `etape?.boosts.length` reagit si son compte de boosts change.
  }, [etape?.cle, etape?.boosts.length])

  useEffect(() => {
    const total = etape?.boosts.length ?? 0
    if (boostsMontres === 0 || boostsMontres >= total) return
    const minuteur = window.setTimeout(
      () => setBoostsMontres((n) => n + 1),
      DELAI_BOOST_MS
    )
    return () => window.clearTimeout(minuteur)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- meme raison :
    // `etape?.cle` et `etape?.boosts.length` suffisent a piloter le
    // minuteur, l'identite de `etape` ne doit pas le redeclencher.
  }, [boostsMontres, etape?.cle, etape?.boosts.length])

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

  // Position du temps COURANT dans la chronologie : elle seule dit qui est
  // deja passe. Calculee une fois pour les cinq temps, pas a chaque `<li>`.
  const positionCourante = TEMPS.findIndex((item) => item.cle === etape.temps)

  return (
    <>
      <TraitCible etape={etape} actif={!termine} />
      <section className="deroule-phase" role="dialog" aria-label={t('Phase du méchant')}>
        <ol className="deroule-temps">
          {TEMPS.map((temps, position) => {
            // Vide : aucune etape de la phase ne porte ce temps. Il n'a
            // coute aucun clic (etapesDeroule ne cree pas de placeholder pour
            // lui) ; le joueur doit seulement voir qu'il a ete saute, et
            // pourquoi.
            const estVide = !etapes.some((e) => e.temps === temps.cle)
            const estCourant = !estVide && temps.cle === etape.temps
            const estPasse = !estVide && !estCourant && position < positionCourante
            const classe = estVide ? 'est-vide' : estCourant ? 'est-courant' : estPasse ? 'est-passe' : ''
            return (
              <li key={temps.cle} className={classe}>
                {t(temps.libelle)}
                {/* Motif deja utilise pour « Fin du tour » (board.tsx) : un
                    symbole colle au texte, pas une traduction a part. */}
                {estPasse ? ' ✓' : null}
                {estVide ? <span className="deroule-temps-vide-detail"> ({t('Aucun')})</span> : null}
              </li>
            )
          })}
        </ol>

        <p className="deroule-titre">{titreEtape(etape)}</p>
        {etape.boosts.length > 0 ? (
          <ul className="deroule-boosts">
            {etape.boosts.slice(0, boostsMontres).map((boost) => (
              <li key={boost.cle}>
                <b>{boost.nom}</b>
                <span>+{boost.apport}</span>
              </li>
            ))}
          </ul>
        ) : null}
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
    </>
  )
}
