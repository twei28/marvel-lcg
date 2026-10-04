import { useRef } from 'react'
import type { Demande } from './ask'
import { classeTonaliteAction } from './action-style'
import { nomLisible } from './BarreAction'
import type { Interaction } from './interaction'
import { avecIcones, coutEnIcones } from './icones-ressources'
import { t } from './langue'
import { consigne, phraseEtat } from './phrase-etat'
import { usePlacement } from './placement/usePlacement'
import { useGlisserPanneau } from './placement/useGlisserPanneau'
import type { WorldCard } from './world'
import { nomAffiche } from './noms-cartes-fr'
import './boutons-bd.css'

type AssistantActionProps = {
  demande?: Demande
  interaction: Interaction
  aNous: boolean
  connecte: boolean
  cartesParId: Map<number, WorldCard>
  affichage?: 'simple' | 'detailed'
  /**
   * Design essai : un seul rendu, quel que soit le mode d'affichage. La carte
   * en petit, la consigne en gros (« Payer 1 pour jouer »), les pastilles du
   * coût et une phrase courte (« Il manque 1 ressource »), puis le bouton qui
   * nomme l'action (« Jouer Quinjet »), grise tant que ce n'est pas pret.
   * Voir phrase-etat.ts.
   */
  designEssai?: boolean
  /** Le nom (français si connu) de la carte qui porte l'option, comme dans la barre d'action. */
  nomPorteur?: (bindId: number) => string | undefined
  /** Taille de main du joueur interroge, pour la consigne de fin de tour. */
  tailleMain?: number
  /**
   * La cible se choisit DANS la scene du deroule (CiblesScene, qui porte deja
   * Annuler / Confirmer) : l'assistant se tait, sauf pour payer un cout, que
   * la scene ne sait pas faire. Capture du 04/10/2026 (Hulk contre Klaw).
   */
  choixDansLaScene?: boolean
}

function nomCarte(id: number, cartesParId: Map<number, WorldCard>): string {
  const carte = cartesParId.get(id)
  return carte ? nomAffiche(carte) : `${t('Carte')} ${id}`
}

function nomsCibles(cibles: number[], cartesParId: Map<number, WorldCard>): string {
  const comptes = new Map<number, number>()
  for (const cible of cibles) comptes.set(cible, (comptes.get(cible) ?? 0) + 1)
  return [...comptes.entries()]
    .map(([id, nombre]) => `${nomCarte(id, cartesParId)}${nombre > 1 ? ` x${nombre}` : ''}`)
    .join(', ')
}

function resume(interaction: Interaction, cartesParId: Map<number, WorldCard>): string {
  const option = interaction.option
  if (!option) return ''
  const morceaux = [nomLisible(option)]
  if (interaction.cibles.length > 0) {
    morceaux.push(nomsCibles(interaction.cibles, cartesParId))
  }
  if (interaction.coutAffiche) morceaux.push(`${t('coût')} ${interaction.coutAffiche}`)
  return morceaux.join(' -> ')
}

function etapeDirecte(interaction: Interaction): string {
  const option = interaction.option
  if (!option) return ''
  const etape =
    interaction.assistant.etape === 'target'
      ? t('choisir la cible')
      : interaction.assistant.etape === 'payment'
        ? t('payer le coût')
        : t('confirmer')
  return `${nomLisible(option)} -> ${etape}`
}

function indicationSimple(interaction: Interaction): string {
  const assistant = interaction.assistant
  const etape = assistant.etape
  if (etape === 'target') {
    // Le mode simple n'affiche pas `detail` : sans le compteur ici, une action
    // repartie sur plusieurs attributions (43006) passe pour une cible unique.
    if (assistant.cibleMaximum > 1) {
      return `${t('Choisis les cibles')} ${assistant.cibleNombre}/${assistant.cibleMaximum}`
    }
    return t('Choisis la cible')
  }
  if (etape === 'payment') return interaction.coutAffiche ? `${t('Paie')} ${interaction.coutAffiche}` : t('Paie le coût')
  // Etape de confirmation. Elle ne disait rien, ce qui convient a la plupart
  // des cartes mais pas a celles dont le coût est X : elles n'exigent RIEN, on
  // saute donc directement ici, et confirmer sans avoir depense laisse X a 0.
  // La carte semble alors cassee. Signale en jeu sur Tendril Explosion.
  if (interaction.surpaiementRecompense) {
    return t('Dépense autant de ressources que tu veux, puis confirme')
  }
  return ''
}

function classeType(type: string | undefined): string {
  const t = (type ?? '').toLowerCase()
  return ['r', 'b', 'y', 'g'].includes(t) ? `est-${t}` : ''
}

export function AssistantAction({
  demande,
  interaction,
  aNous,
  connecte,
  cartesParId,
  affichage = 'detailed',
  designEssai = false,
  nomPorteur,
  tailleMain,
  choixDansLaScene = false,
}: AssistantActionProps) {
  const utile = Boolean(
    connecte &&
      aNous &&
      demande &&
      interaction.option &&
      !(choixDansLaScene && interaction.assistant.etape !== 'payment')
  )

  // Les hooks se déclarent AVANT le premier retour : `actif` porte la condition,
  // pas un `return` anticipé. Les cartes à ménager sont celle qui agit et les
  // cibles déjà désignées — c'est sur elles que porte la consigne affichée.
  const panneau = useRef<HTMLElement | null>(null)
  const signature = `${interaction.option?.id ?? ''}|${interaction.assistant.etape}`
  const { style } = usePlacement(panneau, {
    candidats: ['centre'],
    signature,
    actif: utile,
  })
  // Deplacement volontaire, a la poignee (le bandeau `.assistant-eyebrow`),
  // par-dessus le placement automatique -- meme mecanisme que
  // `DemandeCentrale`/`.dc-texte` (demande de l'utilisateur, 28/09/2026,
  // signalement Yarro : ce panneau-ci, PAS SEULEMENT DemandeCentrale, peut
  // recouvrir le selecteur de cibles hors table (`.plateau-selecteur`), qui ne
  // s'esquive jamais lui-meme). Remis a zero a chaque nouvelle decision
  // (`signature`).
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(signature)
  const styleDeplace: typeof style =
    decalage.dx !== 0 || decalage.dy !== 0
      ? {
          ...style,
          left: style.left !== undefined ? `calc(${style.left} + ${decalage.dx}px)` : style.left,
          top: style.top !== undefined ? `calc(${style.top} + ${decalage.dy}px)` : style.top,
        }
      : style

  if (!utile || !interaction.option) return null

  const assistant = interaction.assistant
  const action = resume(interaction, cartesParId)
  const titre = etapeDirecte(interaction)
  const montrerResume = interaction.cibles.length > 0 || interaction.coutAffiche !== ''
  const nomAction = nomLisible(interaction.option)
  // Le nom de la carte qui porte l'option (« Jouer Quinjet »), comme la barre
  // d'action le fait deja. Pas pour une capacite d'identite : « Attaquer
  // Steve Rogers » se lirait comme une attaque CONTRE Steve.
  const porteur = cartesParId.get(interaction.option.bind_id)
  const porteurEstIdentite = porteur?.card_type === 'Hero' || porteur?.card_type === 'AlterEgo'
  const nomDuPorteur =
    designEssai && interaction.option.bind_id !== 0 && !porteurEstIdentite
      ? (nomPorteur?.(interaction.option.bind_id) ?? (porteur ? nomAffiche(porteur) : undefined))
      : undefined
  const nomActionEssai = nomDuPorteur ? `${nomAction} ${nomDuPorteur}` : nomAction
  // Le mulligan est le premier ecran de la partie : « Resolve Mulligans » sur
  // le bouton repeterait le titre sans dire ce que le clic fait. Le bouton dit
  // donc le geste : garder la main, ou defausser N cartes.
  const estMulligan = interaction.option.name.toLowerCase().includes('mulligan')
  // La fin de tour pose LA MEME question que le mulligan (moteur :
  // `MayDiscardHandCardsAndDrawUpToMax`), avec un minimum quand la main
  // depasse sa taille.
  const estFinDeTour = /^end[ _]phase$/i.test(interaction.option.name)
  const minimumDefausse = interaction.option.target_num_range[0] ?? 0
  const cartes = (n: number) => `${n} ${n > 1 ? t('cartes') : t('carte')}`
  const libelleMulligan =
    assistant.cibleNombre === 0
      ? minimumDefausse > 0
        ? `${t('Défausser')} ${cartes(minimumDefausse)}`
        : t('Garder ma main')
      : `${t('Défausser')} ${cartes(assistant.cibleNombre)}`
  const libelleValider = estMulligan ? libelleMulligan : nomActionEssai || t('Confirmer')

  // LE MULLIGAN A SON PROPRE PANNEAU, dans tous les modes d'affichage.
  // Capture du 03/10/2026 : « Résoudre les mulligans », « Choisis les cibles
  // 0/6 », « Annuler » et « Confirmer » ne disaient pas que c'est FACULTATIF.
  // Choix de l'utilisateur, questions une a une : titre « Mulligan », consigne
  // « Sélectionne les cartes que tu veux changer (facultatif) », un seul bouton
  // (« Garder ma main » / « Défausser N cartes ») et PAS d'« Annuler » : il ne
  // faisait que fermer le panneau, qui revenait, et se lisait comme un refus.
  //
  // FIN DE TOUR, meme panneau (demande de l'utilisateur, 04/10/2026 : « ce
  // n'est pas clair qu'on peut défausser des cartes en fin de tour »). La
  // taille de main est celle du heros, jamais un 5 fixe ; un moteur qui ne
  // l'envoie pas encore donne une consigne sans chiffre.
  if (estMulligan || estFinDeTour) {
    const n = assistant.cibleNombre
    const taille = tailleMain && tailleMain > 0 ? tailleMain : undefined
    const repioche = taille ? ` ${t('Tu repioches jusqu’à')} ${taille}.` : ''
    const consigneMulligan =
      n < minimumDefausse
        ? `${t('Défausse au moins')} ${cartes(minimumDefausse - n)}${
            taille ? ` : ${t('ta main est limitée à')} ${taille}.` : '.'
          }`
        : n > 0
          ? `${n} ${n > 1 ? t('cartes sélectionnées') : t('carte sélectionnée')}`
          : estFinDeTour
            ? `${t('Sélectionne les cartes que tu veux défausser (facultatif).')}${repioche}`
            : t('Sélectionne les cartes que tu veux changer (facultatif)')
    return (
      <aside
        ref={panneau}
        className={`assistant-action mode-simple est-mulligan etape-${assistant.etape}`}
        style={styleDeplace}
        aria-live="polite"
      >
        <span
          className="assistant-simple-action poignee-glisser"
          onPointerDown={gestesGlisser.onPointerDown}
          onPointerMove={gestesGlisser.onPointerMove}
          onPointerUp={gestesGlisser.onPointerUp}
          onPointerCancel={gestesGlisser.onPointerCancel}
        >
          {estFinDeTour ? t('Fin de tour') : t('Mulligan')}
        </span>
        <span className="assistant-simple-indication">{consigneMulligan}</span>
        {assistant.indice ? <span className="assistant-indice">{assistant.indice}</span> : null}
        <div className="assistant-boutons">
          <button
            type="button"
            className="assistant-confirmer"
            disabled={!interaction.prete}
            onClick={interaction.valider}
          >
            {libelleMulligan}
          </button>
        </div>
      </aside>
    )
  }

  if (designEssai) {
    const phrase = phraseEtat(assistant, interaction.prete)
    return (
      <aside
        ref={panneau}
        className={`assistant-action design-essai etape-${assistant.etape} ${classeTonaliteAction(nomAction)}`}
        style={styleDeplace}
        aria-live="polite"
      >
        <div
          className="poignee-glisser"
          onPointerDown={gestesGlisser.onPointerDown}
          onPointerMove={gestesGlisser.onPointerMove}
          onPointerUp={gestesGlisser.onPointerUp}
          onPointerCancel={gestesGlisser.onPointerCancel}
        >
          <span className="assistant-eyebrow">{nomDuPorteur ?? nomAction}</span>
          <strong>{consigne(assistant, nomAction)}</strong>
        </div>
        <div className="assistant-ligne-cout">
          {assistant.etape === 'payment' && assistant.coutSlots.length > 0 ? (
            <span className="assistant-cout" aria-label={t('Coût à payer')}>
              {assistant.coutSlots.map((slot) => (
                <span
                  className={`assistant-slot${slot.rempli ? ' est-rempli' : ''} ${classeType(slot.type)}`}
                  key={slot.index}
                >
                  {/* Le picto de la ressource (poing, cerveau, eclair, etoile),
                      pas sa lettre anglaise : « B » ne disait rien a un joueur
                      francais (retour du 11/09/2026). */}
                  {slot.rempli && slot.type ? avecIcones(coutEnIcones(slot.type)) : ''}
                </span>
              ))}
            </span>
          ) : null}
          {phrase ? <span className="assistant-detail">{phrase}</span> : null}
        </div>
        {assistant.coutRegles.length > 0 ? (
          <span className="assistant-regles">{assistant.coutRegles.join(' - ')}</span>
        ) : null}
        {assistant.indice ? <span className="assistant-indice">{assistant.indice}</span> : null}
        <div className="assistant-boutons">
          <button type="button" className="assistant-annuler" onClick={interaction.annuler}>
            {t('Annuler')}
          </button>
          <button
            type="button"
            className="assistant-confirmer"
            disabled={!interaction.prete}
            onClick={interaction.valider}
          >
            {libelleValider}
          </button>
        </div>
      </aside>
    )
  }

  if (affichage === 'simple') {
    const indication = indicationSimple(interaction)
    return (
      <aside
        ref={panneau}
        className={`assistant-action mode-simple etape-${assistant.etape} ${classeTonaliteAction(nomAction)}`}
        style={styleDeplace}
        aria-live="polite"
      >
        <span
          className="assistant-simple-action poignee-glisser"
          onPointerDown={gestesGlisser.onPointerDown}
          onPointerMove={gestesGlisser.onPointerMove}
          onPointerUp={gestesGlisser.onPointerUp}
          onPointerCancel={gestesGlisser.onPointerCancel}
        >
          {nomAction}
        </span>
        {indication ? <span className="assistant-simple-indication">{indication}</span> : null}
        {assistant.indice ? <span className="assistant-indice">{assistant.indice}</span> : null}
        {montrerResume && action ? <span className="assistant-simple-resume">{action}</span> : null}
        <div className="assistant-boutons">
          <button type="button" className="assistant-annuler" onClick={interaction.annuler}>
            {t('Annuler')}
          </button>
          {interaction.prete ? (
            <button type="button" className="assistant-confirmer" onClick={interaction.valider}>
              {t('Confirmer')}
            </button>
          ) : null}
        </div>
      </aside>
    )
  }

  return (
    <aside
      ref={panneau}
      className={`assistant-action etape-${assistant.etape}`}
      style={styleDeplace}
      aria-live="polite"
    >
      <div
        className="poignee-glisser"
        onPointerDown={gestesGlisser.onPointerDown}
        onPointerMove={gestesGlisser.onPointerMove}
        onPointerUp={gestesGlisser.onPointerUp}
        onPointerCancel={gestesGlisser.onPointerCancel}
      >
        <span className="assistant-eyebrow">{nomLisible(interaction.option)}</span>
        <strong>{titre || assistant.titre}</strong>
      </div>
      {assistant.detail ? <span className="assistant-detail">{assistant.detail}</span> : null}
      {assistant.indice ? <span className="assistant-indice">{assistant.indice}</span> : null}

      {assistant.etape === 'payment' && assistant.coutSlots.length > 0 ? (
        <div className="assistant-cout" aria-label={t('Coût à payer')}>
          {assistant.coutSlots.map((slot) => (
            <span
              className={`assistant-slot${slot.rempli ? ' est-rempli' : ''} ${classeType(slot.type)}`}
              key={slot.index}
            >
              {slot.label ?? ''}
            </span>
          ))}
          {assistant.coutRegles.length > 0 ? (
            <span className="assistant-regles">{assistant.coutRegles.join(' - ')}</span>
          ) : null}
        </div>
      ) : null}

      {montrerResume && action ? (
        <span className="assistant-resume">{action}</span>
      ) : null}

      {/* Confirmer / annuler ICI, au centre de l'ecran : plus besoin d'aller
          chercher le bouton en bas a droite a chaque action. */}
      <div className="assistant-boutons">
        <button type="button" className="assistant-annuler" onClick={interaction.annuler}>
          {t('Annuler')}
        </button>
        <button
          type="button"
          className="assistant-confirmer"
          disabled={!interaction.prete}
          onClick={interaction.valider}
        >
          {t('Confirmer')}
        </button>
      </div>
    </aside>
  )
}
