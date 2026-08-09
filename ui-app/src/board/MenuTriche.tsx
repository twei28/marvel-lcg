// MenuTriche.tsx — le menu qui s'ouvre au clic droit, en mode Bac à sable.
//
// Un seul geste pour tout le mode : clic droit. Sur une carte du plateau, il
// ouvre ses interventions ; sur une pile, il ouvre son contenu (voir
// PileTriche). Le clic GAUCHE reste le jeu normal, sans exception — c'est ce
// qui permet de tricher au milieu d'une partie sans jamais se tromper de geste.
//
// Le menu se ferme dès qu'on agit : enchaîner deux interventions sur la même
// carte demande deux clics droits. C'est volontaire — un menu qui reste ouvert
// masque le plateau, or on veut justement VOIR l'effet de ce qu'on vient de
// faire.

import { useEffect, useRef, useState } from 'react'
import { t } from './langue'
import * as triche from './triche'

export type CibleTriche = {
  id: number
  nom: string
  /** Une manigance : on propose la menace plutôt que les points de vie. */
  estManigance?: boolean
  /** Un personnage : points de vie, inclinaison, états. */
  estPersonnage?: boolean
}

export type MenuTricheProps = {
  cible: CibleTriche
  /** Position du clic, en pixels écran. */
  x: number
  y: number
  onFermer: () => void
  /** Raconte l'intervention à l'historique de partie. */
  onIntervention: (libelle: string) => void
}

/** Une entrée du menu. `valeur` ouvre une saisie de nombre avant d'agir. */
type Entree = {
  libelle: string
  agir: (valeur: number) => Promise<boolean>
  valeur?: number
  danger?: boolean
}

export function MenuTriche({ cible, x, y, onFermer, onIntervention }: MenuTricheProps) {
  const [saisie, setSaisie] = useState<Entree | undefined>(undefined)
  const [nombre, setNombre] = useState(1)
  const boite = useRef<HTMLDivElement | null>(null)

  // Fermeture au clic extérieur et à Échap : sans ça, un menu oublié reste
  // par-dessus le plateau et intercepte les clics de jeu.
  useEffect(() => {
    const dehors = (evenement: MouseEvent) => {
      if (boite.current && !boite.current.contains(evenement.target as Node)) onFermer()
    }
    const touche = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') onFermer()
    }
    document.addEventListener('mousedown', dehors)
    document.addEventListener('keydown', touche)
    return () => {
      document.removeEventListener('mousedown', dehors)
      document.removeEventListener('keydown', touche)
    }
  }, [onFermer])

  const entrees: Entree[] = []

  if (cible.estManigance) {
    entrees.push(
      { libelle: t('Poser de la menace'), valeur: 1, agir: (n) => triche.poserMenace(cible.id, n) },
      { libelle: t('Retirer de la menace'), valeur: 1, agir: (n) => triche.poserMenace(cible.id, -n) },
      { libelle: t('Fixer la menace à'), valeur: 0, agir: (n) => triche.fixerMenace(cible.id, n) },
    )
  } else {
    entrees.push(
      { libelle: t('Soigner'), valeur: 3, agir: (n) => triche.soigner(cible.id, n) },
      { libelle: t('Infliger des dégâts'), valeur: 3, agir: (n) => triche.blesser(cible.id, n) },
    )
  }

  if (cible.estPersonnage !== false) {
    entrees.push(
      { libelle: t('Redresser'), agir: () => triche.redresser(cible.id) },
      { libelle: t('Incliner'), agir: () => triche.incliner(cible.id) },
      { libelle: t('Rendre désorienté'), agir: () => triche.rendreConfus(cible.id) },
      { libelle: t('Rendre sonné'), agir: () => triche.assommer(cible.id) },
      { libelle: t('Rendre coriace'), agir: () => triche.rendreCoriace(cible.id) },
    )
  }

  entrees.push(
    { libelle: t('Ajouter des compteurs'), valeur: 1,
      agir: (n) => triche.poserCompteur(cible.id, 'counter', n) },
    { libelle: t('Défausser'), agir: () => triche.defausser(cible.id), danger: true },
    { libelle: t('Retirer de la partie'), agir: () => triche.retirer(cible.id), danger: true },
  )

  const executer = async (entree: Entree, valeur: number) => {
    const reussi = await entree.agir(valeur)
    const chiffre = entree.valeur !== undefined ? ` ${valeur}` : ''
    onIntervention(
      `${entree.libelle}${chiffre} — ${cible.nom}${reussi ? '' : ` (${t('refusé')})`}`
    )
    onFermer()
  }

  // Le menu est placé au curseur, mais ramené dans l'écran s'il déborde : un
  // clic droit près du bord bas ouvrait sinon un menu partiellement invisible.
  const style = {
    left: Math.min(x, window.innerWidth - 240),
    top: Math.min(y, window.innerHeight - 340),
  }

  return (
    <div className="menu-triche" style={style} ref={boite} role="menu">
      <header className="menu-triche-titre">
        <span>{cible.nom}</span>
        <span className="menu-triche-marque">{t('Triche')}</span>
      </header>

      {saisie ? (
        <div className="menu-triche-saisie">
          <label>
            {saisie.libelle}
            <input
              type="number"
              value={nombre}
              autoFocus
              onChange={(e) => setNombre(Number(e.target.value))}
              onKeyDown={(e) => {
                if (e.key === 'Enter') void executer(saisie, nombre)
              }}
            />
          </label>
          <div className="menu-triche-boutons">
            <button type="button" onClick={() => setSaisie(undefined)}>{t('Retour')}</button>
            <button type="button" onClick={() => void executer(saisie, nombre)}>
              {t('Appliquer')}
            </button>
          </div>
        </div>
      ) : (
        <ul className="menu-triche-liste">
          {entrees.map((entree) => (
            <li key={entree.libelle}>
              <button
                type="button"
                className={entree.danger ? 'est-danger' : undefined}
                onClick={() => {
                  if (entree.valeur !== undefined) {
                    setNombre(entree.valeur)
                    setSaisie(entree)
                  } else {
                    void executer(entree, 0)
                  }
                }}
              >
                {entree.libelle}
                {entree.valeur !== undefined ? <span className="menu-triche-suite">…</span> : null}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
