// La barre d'action : ce que le moteur demande, et ce qu'on lui repond.
//
// Elle vit hors de la scene, a taille reelle. Deux raisons : le texte d'une
// barre mise a l'echelle deviendrait illisible, et un panneau flottant
// recouvrirait la main, qui est justement ce qu'on regarde en jouant.

import type { Demande, Option } from './ask'
import type { Interaction } from './interaction'
import { t } from './langue'
import { avecIcones, coutEnIcones, marquerRessources } from './icones-ressources'
import { nomActionParlant } from './texte-capacite'
import { sansIndexDeCapacite, traduireEffets, traduireMoteur, traduireTitreRepetition } from './vocabulaire-moteur'

/**
 * Les noms d'options arrivent avec des soulignes, et parfois prefixes de "p_"
 * quand le moteur voulait une image. On rend le texte lisible sans pretendre
 * afficher l'icone.
 *
 * Puis on passe par `traduireMoteur` : ces noms naissent en ANGLAIS dans le
 * moteur Python, et s'affichaient tels quels au milieu d'une interface
 * francaise (« RESOLVE MULLIGANS », signale en jeu). Un nom de capacite imprime
 * sur la carte n'est pas dans la table et reste donc en anglais, comme le scan.
 */
export function nomLisible(option: Option): string {
  const brut = option.name.startsWith('p_') ? option.name.slice(2) : option.name
  const lisible = sansIndexDeCapacite(brut.replaceAll('_', ' ').trim())
  return lisible ? traduireMoteur(lisible) : t('Action')
}

/**
 * Le nom d'une option, avec le RESUME de son paragraphe quand la carte offre plusieurs actions du meme type
 * (« Action de héros : Dépensez [energy] → piochez 1 carte »). Sans texte, ou avec une seule action, c'est `nomLisible`.
 * Demande du 22/10/2026 : plus jamais « Action » et « Action 1 » sans savoir laquelle fait quoi.
 */
export function nomLisibleParlant(option: Option, texteCarte: string | undefined): string {
  const resume = nomActionParlant(option.name, texteCarte)
  const nom = nomLisible(option)
  return resume ? `${nom} : ${resume}` : nom
}

/**
 * Le moteur cite les cartes avec leur identifiant technique :
 * « [(50,01113) Klaw] » ou « [[(01,01001a) Spider-Man]] ». On ne garde que le
 * nom, sans le prefixe (object_id, card_id) ni les crochets.
 */
export function sansIdentifiants(texte: string): string {
  return texte.replace(/\[+\([^)]*\)\s*([^[\]]+?)\]+/g, '$1')
}

/**
 * Le moteur ne dessine pas ses symboles : il les remplace par des jetons texte
 * a destination du client (src/game/render/symbol.py, lignes 71-75). Sans
 * traduction ils s'affichent bruts : « would count boost icons ([[boost]]
 * [[boost]][[boost]]) ».
 *
 * Seul le boost recoit un vrai glyphe — l'etoile, comme sur les cartes
 * Rencontre. Les quatre ressources sont simplement debarrassees de leurs
 * crochets : leur inventer un pictogramme serait plus deroutant que le mot,
 * d'autant que la table les designe deja par leurs lettres (R/B/Y/G).
 */
export function remplacerSymboles(texte: string): string {
  return (
    // Les ressources deviennent des marqueurs d'icones (icones-ressources.tsx),
    // rendus par `avecIcones` la ou le texte s'affiche.
    marquerRessources(texte)
      .replace(/\[\[boost\]\]/g, '★')
      // Le moteur espace ses jetons de boost irregulierement (« ★ ★★ ») : on
      // regroupe les etoiles consecutives pour qu'elles se lisent d'un bloc.
      .replace(/★\s+(?=★)/g, '★')
  )
}

/**
 * Nettoie le jargon moteur des narrations :
 *  - « ? » = carte face cachee (le moteur masque le nom) -> « a facedown card » ;
 *  - « () » vide = liste de cartes toutes cachees -> supprimee ;
 *  - « BoostCardsDeck<1> », « EncounterDeck<7> »... -> noms lisibles sans <N> ;
 *  - les IDENTIFIANTS que `by_effect` deverse.
 *
 * ⚠ Le dernier point vient d'une capture de l'utilisateur (11/09/2026), dans
 * le panneau de decision : « Klaw va comploter (+0) ((^!142) Advance (When
 * Revealed) [01186] WhenCardRevealed) ». Trois formes, toutes internes au
 * moteur et sans le moindre sens pour un joueur :
 *   - `(^!142)`          la reference d'une capacite ;
 *   - `[01186]`          le code de la carte (cinq chiffres, parfois suivis
 *                        d'une lettre de face) ;
 *   - `WhenCardRevealed` le nom d'evenement, qui repete « (When Revealed) ».
 * Ce dernier n'est retire que sur les prefixes du moteur (When/After/Before) :
 * un nom de carte en CamelCase, lui, doit survivre.
 */
export function nettoyerNarration(texte: string): string {
  const propre = remplacerSymboles(texte)
    .replace(/([A-Za-z])<\d+>/g, '$1')
    .replace(/\(\^![^)]*\)/g, '')
    .replace(/\[\d{5}[a-z]?\]/g, '')
    .replace(/\b(?:When|After|Before)[A-Z][A-Za-z]*\b/g, '')
    .replace(/BoostCardsDeck/g, t('pile de boost'))
    .replace(/EncounterDeck/g, t('deck de rencontre'))
    .replace(/PlayerDeck/g, t('deck du joueur'))
    .replace(/(^|\s)\?(?=\s|$|[,.])/g, `$1${t('une carte face cachée')}`)
    .replace(/\s*\(\s*\)/g, '')
    .replace(/\s+/g, ' ')
    // Les retraits ci-dessus laissent des blancs colles aux parentheses
    // (« ( Advance ) ») : on les resserre avant de rendre le texte.
    .replace(/\(\s+/g, '(')
    .replace(/\s+\)/g, ')')
    .trim()
  // En DERNIER, une fois les identifiants partis : la capacite responsable et
  // sa fenetre de declenchement passent en francais. Segment entier seulement,
  // pour ne pas abimer les noms de cartes (voir traduireEffets).
  return traduireEffets(propre)
}

export type BarreActionProps = {
  demande?: Demande
  interaction: Interaction
  /** Le moteur attend-il une reponse de nous ? */
  aNous: boolean
  connecte: boolean
  /** Nom de la carte porteuse d'une option, pour situer l'action. */
  nomPorteur: (bindId: number) => string | undefined
  /**
   * La question en cours a son propre panneau et n'appartient qu'a lui : la
   * face A de la manigance principale (voir `manigance-face-a.ts`).
   *
   * ⚠ DEFAUT TROUVE EN RELECTURE, 15/09/2026. Sans cette porte, la barre
   * offrait « Reveal Main Scheme » EN MEME TEMPS que le panneau, avec ce
   * libelle brut qui n'est meme pas dans `dico-en.ts`. Et pendant les 400 ms
   * du retournement, le panneau passe en `pointer-events: none` : ce bouton-la
   * restait cliquable, contournait la garde « un seul envoi » du panneau et
   * pouvait repondre a la question SUIVANTE a la place du joueur.
   */
  questionPriseParLePanneau?: boolean
}

export function BarreAction({
  demande,
  interaction,
  aNous,
  connecte,
  nomPorteur,
  questionPriseParLePanneau = false,
}: BarreActionProps) {
  if (!connecte) {
    return (
      <footer className="plateau-action plateau-action-attente" role="status">
        <strong>{t('Connexion à la partie perdue.')}</strong>
        <span>
          {t('La partie ne peut pas avancer tant que ce plateau n’accuse pas réception. Reconnexion en cours.')}
        </span>
      </footer>
    )
  }

  // La barre n'a rien a proposer quand la question se joue ailleurs : le
  // panneau de la manigance porte la carte en grand et son seul bouton.
  if (!demande || !aNous || questionPriseParLePanneau) {
    return (
      <footer className="plateau-action plateau-action-attente" role="status">
        <strong>{t('En attente du jeu.')}</strong>
        <span>{t('Rien à décider pour le moment.')}</span>
      </footer>
    )
  }

  const { option } = interaction
  const focus = interaction.carteFocus ?? interaction.cibleFocus
  const nomFocus = focus !== undefined ? nomPorteur(focus) : undefined
  const optionAvecCibles = option ? option.target_num_range[1] > 0 : false
  const optionAvecCout = option ? interaction.coutAffiche !== '' : false

  const etape = option
    ? interaction.assistant.etape === 'target'
      ? t('Étape 1 - choisis la cible')
      : interaction.assistant.etape === 'payment'
        ? // Ne PAS dire « de ta main » : c'est faux pour une carte jouée depuis
          // la réserve de Brawn, que la main n'a justement pas le droit de
          // financer. Le libellé désigne donc les cartes surlignées, sans
          // préjuger de leur zone.
          t('Étape 2 - paie en cliquant les cartes surlignées ou un générateur de ressources')
        : t('Dernière étape - confirme')
    : focus !== undefined && interaction.options.length === 0
      ? `${nomFocus ?? t('Cette carte')} - ${t('aucune action')}`
      : focus !== undefined
        ? `${nomFocus ?? t('Cette carte')} - ${t('choisis une action')}`
        : t('Clique une carte pour agir, ou choisis ci-dessous')
  // ⚠ Une option ENGAGEE doit toujours offrir une issue. Sans ce bouton, un
  // joueur qui choisit une carte puis découvre qu'il ne peut pas la payer reste
  // coincé : le moteur repose la même question à l'infini, et la partie a l'air
  // de boucler. Signalé en partie réelle le 7/8/2026 avec Calculated Defense en
  // réserve — le cloisonnement main/réserve retire des payeurs, et l'impasse
  // devenait bien plus facile à atteindre.
  const boutonSecondaire =
    option !== undefined ? (
      <button type="button" onClick={interaction.annuler}>
        {t('Abandonner')}
      </button>
    ) : focus !== undefined ? (
      <button type="button" onClick={interaction.defocaliser}>
        {t('Retour')}
      </button>
    ) : demande.show_cancel ? (
      <button type="button" onClick={interaction.annuler}>
        {t('Passer')}
      </button>
    ) : null

  return (
    <footer className={`plateau-action plateau-action-secondaire${option ? ' a-action-en-cours' : ''}`}>
      {/* La légende des couleurs n'a de sens que pendant une action, quand il y
          a des cibles à distinguer d'une source. Au repos, elle était un
          élément permanent de plus en bas de l'écran. */}
      {option ? (
        <div className="pa-legende" aria-label={t('Légende des surbrillances')}>
          <span className="pa-leg pa-leg-play">{t('Jouable')}</span>
          <span className="pa-leg pa-leg-target">{t('Cible')}</span>
          <span className="pa-leg pa-leg-chosen">{t('Choisie')}</span>
        </div>
      ) : null}

      <div className="plateau-action-texte">
        <span className="plateau-eyebrow">{t('À toi de jouer')}</span>
        <strong>{demande.prompt_text ? avecIcones(traduireTitreRepetition(nettoyerNarration(demande.prompt_text))) : t('Choisis une action')}</strong>
        <span className="pa-etape">{etape}</span>
      </div>

      {option ? (
        <div className="plateau-action-encours">
          <span className="plateau-action-nom">{avecIcones(marquerRessources(nomLisible(option)))}</span>
          {optionAvecCibles ? (
            <span className="pa-compteur">
              <em>{t('Cibles')}</em>
              <b>
                {interaction.cibles.length}/{option.target_num_range[1]}
              </b>
              {option.target_num_range[0] > 0 ? (
                <i>min {option.target_num_range[0]}</i>
              ) : null}
              {interaction.ciblesRestantes > 0 ? (
                <i className="pa-reste">
                  {t('reste {n} à placer').replace('{n}', String(interaction.ciblesRestantes))}
                </i>
              ) : null}
            </span>
          ) : null}
          {interaction.coutAffiche ? (
            <span className="pa-compteur pa-cost">
              <em>{t('Coût payé')}</em>
              <b>{avecIcones(coutEnIcones(interaction.coutAffiche))}</b>
            </span>
          ) : null}
          {interaction.raison ? (
            <span className="plateau-action-raison">{avecIcones(marquerRessources(sansIdentifiants(interaction.raison)))}</span>
          ) : null}
        </div>
      ) : (
        <div className="plateau-action-options">
          {interaction.options.map((candidate) => {
            const porteur = nomPorteur(candidate.bind_id)
            return (
              <button
                type="button"
                key={candidate.id}
                disabled={candidate.failure_reason !== ''}
                title={candidate.failure_reason || undefined}
                onClick={() => interaction.choisirOption(candidate)}
              >
                {avecIcones(marquerRessources(nomLisible(candidate)))}
                {porteur ? <em>{porteur}</em> : null}
              </button>
            )
          })}
        </div>
      )}

      {boutonSecondaire ? <div className="plateau-action-boutons">{boutonSecondaire}</div> : null}
    </footer>
  )
}
