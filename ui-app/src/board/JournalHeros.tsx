// Le journal du héros affiché, posé à la table.
//
// L'historique global (bouton « H ») raconte la partie entière, tous joueurs
// confondus. À plusieurs, on n'y retrouve plus SA propre partie. Cette colonne
// ne garde que ce qui touche le héros qu'on regarde.
//
// Ce qui entre :
//   - ses cartes à lui (identité, alliés, améliorations, soutiens) ;
//   - les ennemis engagés contre lui et les cartes rencontre qu'on lui donne —
//     le moteur les range déjà dans les zones DU JOUEUR, donc ils portent son
//     numéro ;
//   - ce que lui ou ses alliés font ailleurs : la menace retirée d'une
//     manigance, les dégâts infligés au vilain. Ces cartes-là n'appartiennent à
//     personne, on les rattache par l'AUTEUR du fait, que causalite.ts a extrait
//     de la narration.
//
// Volontairement pas de narration brute : la colonne est étroite, elle ne porte
// que les faits marquants.

import { useEffect, useRef } from 'react'
import type { EntreeHistorique } from './HistoriquePartie'
import { t } from './langue'
import type { World } from './world'

/** Noms des cartes que ce joueur contrôle. Sert à reconnaître ses actions. */
function nomsDuJoueur(monde: World | undefined, joueur: number): Set<string> {
  const noms = new Set<string>()
  const zone = monde?.players?.[joueur]
  if (!zone) return noms
  for (const liste of [zone.area_hero, zone.allies, zone.supports]) {
    for (const carte of liste ?? []) {
      const nom = carte.name?.replace(/^\W*/, '').trim()
      if (nom) noms.add(nom.toLowerCase())
    }
  }
  return noms
}

export function entreesDuHeros(
  entrees: EntreeHistorique[],
  monde: World | undefined,
  joueur: number
): EntreeHistorique[] {
  const siens = nomsDuJoueur(monde, joueur)
  return entrees.filter((entree) => {
    // Pas de jalons de phase (« Round 2 · Start Round », « Player 1 Turn ») :
    // le moteur en émet plusieurs par round, souvent en double, et ils
    // remplissaient la colonne à eux seuls. Le round est déjà sur chaque ligne.
    if (entree.type === 'phase') return false
    if (entree.joueur === joueur) return true
    if (entree.acteur && siens.has(entree.acteur.replace(/^\W*/, '').trim().toLowerCase())) return true
    return false
  })
}

export function JournalHeros({
  entrees,
  monde,
  joueur,
  nomHeros,
}: {
  entrees: EntreeHistorique[]
  monde: World | undefined
  joueur: number
  nomHeros?: string
}) {
  const liste = entreesDuHeros(entrees, monde, joueur)
  const bas = useRef<HTMLDivElement>(null)

  // Les entrées arrivent les plus récentes EN TÊTE (voir ajouterNouvellesEntrees).
  // La colonne les lit dans l'ordre du jeu, donc on les remet à l'endroit et on
  // colle au bas, là où se passe l'action.
  const ordreDuJeu = [...liste].reverse()

  useEffect(() => {
    bas.current?.scrollIntoView({ block: 'nearest' })
  }, [liste.length])

  return (
    <section className="journal-heros" aria-label={t('Journal du héros')}>
      <header className="journal-heros-entete">
        <span className="plateau-eyebrow">{t('Journal')}</span>
        {nomHeros ? <strong>{nomHeros}</strong> : null}
        {/* « retenues / total du tampon ». Sert à savoir, quand la colonne
            paraît trop courte, si c'est le filtre qui écarte (total élevé) ou
            le tampon partagé qui est vide (total bas). */}
        <span className="jh-compte" title={t('Entrées retenues sur le total du journal')}>
          {liste.length}/{entrees.length}
        </span>
      </header>

      {ordreDuJeu.length === 0 ? (
        <p className="journal-heros-vide">{t('Rien encore.')}</p>
      ) : (
        <ol className="journal-heros-liste">
          {ordreDuJeu.map((entree) => (
            <li className={`journal-heros-entree type-${entree.type}`} key={entree.cle}>
              <span className="jh-round">R{entree.round}</span>
              <span className="jh-texte">
                <b>{entree.titre}</b>
                {entree.detail ? <small>{entree.detail}</small> : null}
              </span>
            </li>
          ))}
          <div ref={bas} aria-hidden="true" />
        </ol>
      )}
    </section>
  )
}
