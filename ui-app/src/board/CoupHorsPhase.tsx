// LE CARTOUCHE D'UN SEUL COUP, hors de la phase du mechant (decision du
// 03/10/2026). Pendant le tour d'un joueur, une attaque ou une manigance du
// mechant (une carte qui le fait frapper) ouvre le cartouche pour ce coup-la,
// puis « Continuer » le referme. Le moteur ne l'attend pas : il est purement
// informatif, et ne retient aucune trame.
//
// Les etapes viennent de `etapesHorsPhase` (deroule-phase.ts) ; les memes
// phrases que le cartouche de la phase (deroule-textes.ts).

import { useEffect, useRef, useState, type ReactNode } from 'react'
import { createPortal } from 'react-dom'
import { calculCoupTable } from './calcul-coup-table'
import { clavierBloque } from './clavier-cartouche'
import { estSpectateur } from './moteur'
import { phraseHistorique } from './PhaseDynamique'
import { CoucheTraitPhase } from './CoucheTraitPhase'
import { coupsDeLEtape } from './coups-sur-table'
import { TableSansModale } from './TableSansModale'
import { contenuDuTrait } from './trait-phase'
import type { EtapeDeroule } from './deroule-phase'
import { detailEtape, lignesEtoileBoost, texteActivationAnnulee, texteBoostsDuCoup, texteCauseActivation, titreEtape } from './deroule-textes'
import { t } from './langue'

export function CoupHorsPhase({
  etapes,
  ignorerLesPremiers = false,
}: {
  etapes: EtapeDeroule[]
  /**
   * Au chargement de la page, les coups DEJA dans le journal ont ete vus avant
   * le rechargement : on ne les remontre pas (board.tsx le passe a vrai).
   */
  ignorerLesPremiers?: boolean
}) {
  const vus = useRef<Set<string> | undefined>(undefined)
  if (vus.current === undefined) {
    vus.current = new Set(ignorerLesPremiers ? etapes.map((e) => e.cle) : [])
  }
  const [, redessiner] = useState(0)
  // Une annonce attend sa resolution : le coup n'a pas encore eu lieu, et la
  // question de defense passe par le panneau central comme d'habitude.
  const coup = etapes.find((e) => e.etat !== 'annonce' && !vus.current?.has(e.cle))
  if (!coup) return null
  const fermer = () => {
    vus.current?.add(coup.cle)
    redessiner((n) => n + 1)
  }
  const resultat = detailEtape(coup)
  const annulee = texteActivationAnnulee(coup)
  const cause = texteCauseActivation(coup)
  const boosts = texteBoostsDuCoup(coup)
  return (
    <section className="deroule-phase est-hors-phase" role="dialog" aria-label={t('Hors de la phase du méchant')}>
      <p className="deroule-surtitre">{t('Hors de la phase du méchant')}</p>
      <div className="deroule-entete">
        <p className="deroule-titre">{titreEtape(coup)}</p>
      </div>
      {resultat ? <p className="deroule-resultat">{resultat}</p> : null}
      {lignesEtoileBoost(coup).map((ligne) => (
        <p key={ligne} className="deroule-etoile">{ligne}</p>
      ))}
      {annulee ? <p className="deroule-annulee">{annulee}</p> : null}
      {cause ? <p className="deroule-cause">{cause}</p> : null}
      {boosts ? <p className="deroule-cause">{boosts}</p> : null}
      <div className="deroule-boutons">
        <button type="button" className="bh-bouton deroule-suivant" onClick={fermer}>
          {t('Continuer')}
        </button>
      </div>
    </section>
  )
}

/** Rend dans le cadre du plateau (le repere des bandeaux « sur la table »), comme le fait le cartouche de la phase. */
export function DansLeCadre({ children }: { children: ReactNode }) {
  const [cadre, setCadre] = useState<HTMLElement | null>(() => document.querySelector<HTMLElement>('.plateau-cadre'))
  useEffect(() => {
    if (!cadre) setCadre(document.querySelector<HTMLElement>('.plateau-cadre'))
  }, [cadre])
  return cadre ? createPortal(children, cadre) : null
}

/**
 * LE MEME COUP, « SUR LA TABLE » (T16, 19/10/2026). Un sbire Rapide qui frappe pendant le tour du joueur
 * passe par le meme bandeau lateral que la phase du mechant : la phrase (« X attaque Y »), le nombre,
 * le calcul (ATQ − DEF = degats), et le meme « Continuer » (ou la carte doree, ou Espace). Plus de fenetre
 * au centre. Les regles du moteur ne changent pas : seul l'affichage.
 */
export function CoupHorsPhaseSurTable({ etapes, ignorerLesPremiers = false }: { etapes: EtapeDeroule[]; ignorerLesPremiers?: boolean }) {
  const vus = useRef<Set<string> | undefined>(undefined)
  if (vus.current === undefined) {
    vus.current = new Set(ignorerLesPremiers ? etapes.map((e) => e.cle) : [])
  }
  const [, redessiner] = useState(0)
  const coup = etapes.find((e) => e.etat !== 'annonce' && !vus.current?.has(e.cle))
  const cle = coup?.cle
  const fermer = () => {
    if (!cle) return
    vus.current?.add(cle)
    redessiner((n) => n + 1)
  }
  const fermerRef = useRef(fermer)
  fermerRef.current = fermer
  useEffect(() => {
    if (!cle) return
    const touche = (e: KeyboardEvent) => {
      if (e.key !== ' ' && e.key !== 'Enter') return
      const cible = e.target
      if (cible instanceof HTMLElement && (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)) return
      if (clavierBloque(document)) return
      e.preventDefault()
      e.stopPropagation()
      fermerRef.current()
    }
    // En CAPTURE et sans laisser passer : Espace au repos finit le tour (ecouteur du cartouche de la phase),
    // et ce meme Espace ne doit pas, en plus de fermer ce coup, finir le tour du joueur.
    window.addEventListener('keydown', touche, true)
    return () => window.removeEventListener('keydown', touche, true)
  }, [cle])
  if (!coup) return null
  const phrase = phraseHistorique(coup)
  const contenu = contenuDuTrait(coup)
  const nombreEnClair = contenu.montant !== undefined ? `${contenu.montant}${contenu.unite ? ' ' + t(contenu.unite) : ''}` : contenu.unite ? t(contenu.unite) : ''
  const annulee = texteActivationAnnulee(coup)
  const cause = texteCauseActivation(coup)
  // Les cartes de boost se disent AUSSI hors phase (rapport BL-Stark n°103) : sans elles, le coup paraissait n'en avoir retourne aucune.
  const boosts = texteBoostsDuCoup(coup)
  return (
    <DansLeCadre>
      {/* 19/10/2026 : la meme fleche attaquant > cible que la phase du mechant (pas de relecture des boosts).
          Elle part et disparait avec le bandeau : meme `coup`, rendue tant qu'il est la. */}
      <CoucheTraitPhase etape={coup} actif sansEtiquette={coupsDeLEtape(coup).some((c) => c.montant > 0)} />
      <TableSansModale
        acteurId={coup.carteId ?? coup.cibleId}
        cibleId={coup.carteId === undefined ? undefined : coup.cibleId}
        cle={coup.cle}
        phrase={phrase}
        nombre={nombreEnClair && !phrase.includes(nombreEnClair) ? nombreEnClair : undefined}
        calcul={calculCoupTable(coup)}
        peutAgir={!estSpectateur()}
        avancer={fermer}
        libelleAction={`${titreEtape(coup)} — ${t('Suivant')}`}
        suite={[annulee, cause, boosts].filter(Boolean).join(' · ') || undefined}
      />
    </DansLeCadre>
  )
}

/**
 * ESPACE PENDANT LA QUESTION « QUI DEFEND ? » hors phase : il prend l'unique choix possible (comme pendant la phase),
 * et ne finit JAMAIS le tour (l'ecouteur du cartouche de la phase le ferait, sinon).
 */
export function EspaceDeLaQuestion() {
  useEffect(() => {
    const touche = (e: KeyboardEvent) => {
      if (e.key !== ' ' && e.key !== 'Enter') return
      const cible = e.target
      if (cible instanceof HTMLElement && (cible.tagName === 'INPUT' || cible.tagName === 'TEXTAREA' || cible.isContentEditable)) return
      if (clavierBloque(document)) return
      e.preventDefault()
      e.stopPropagation()
      document.querySelector<HTMLElement>('[data-choix-unique]')?.click()
    }
    window.addEventListener('keydown', touche, true)
    return () => window.removeEventListener('keydown', touche, true)
  }, [])
  return null
}
