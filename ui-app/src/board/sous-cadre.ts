// LE SOUS-CADRE DU CARTOUCHE DU BAS (refonte du 04/10/2026, decisions D4 a
// D8, D18, D31, D32) : la question du moteur, mise en DONNEES.
//
// Pendant la phase du mechant en scene PC, UN seul endroit porte la question :
// la rangee du cartouche (defense, choix d'une carte revelee) ou le sous-cadre
// pose par-dessus (reponses, cibles, paiement). Ce module dit lequel et avec
// quoi ; le composant dessine, et traduit chaque clic en appel :
//  - vignette d'option → `q.choisirOption(option)` ;
//  - cible ou carte de la main → `agir` de la carte (`interaction.cartes`) ;
//  - « Confirmer », « Jouer » → `interaction.valider()` ;
//  - refus (« Ne pas défendre », « Aucune réponse »…) → `interaction.annuler()`.
// Jamais `repondre` en direct : `valider` et `annuler` portent les
// confirmations du hot-seat et des coups sans effet (piege 27).
//
// ⚠ LA VUE NE PORTE AUCUNE CLOSURE : des identifiants et des textes. Les
// gestionnaires restent dans `QuestionDuMoteur`, cote composant.

import type { ScanCardProps } from '../components/ScanCard'
import type { Demande, Option } from './ask'
import { nettoyerNarration, nomLisible } from './BarreAction'
import type { EtapeDeroule, TempsPhase } from './deroule-phase'
import {
  estFenetreDeReaction,
  libelleRefus,
  nomDeCapacite,
  phraseDeReaction,
  sansIdentifiantsEnFrancais,
} from './DemandeCentrale'
import type { CoutSlot, Interaction } from './interaction'
import { t } from './langue'
import { ligneDefense } from './ligne-attaque'
import { nomAffiche } from './noms-cartes-fr'
import type { WorldCard } from './world'

/** Ce que board.tsx sait de la question ; les closures restent ICI, jamais dans la vue. */
export type QuestionDuMoteur = {
  demande: Demande
  interaction: Interaction
  cartesParId: Map<number, WorldCard>
  /** = choisirOptionDepuisMenu (board.tsx) : pulse des cibles, survol remis a zero, puis interaction.choisirOption. */
  choisirOption: (option: Option, ciblesInitiales?: number[]) => void
  survolerOption: (option: Option | undefined) => void
  carteDeLOption?: (option: Option) => ScanCardProps | undefined
  carteAuSurvol?: (option: Option) => ScanCardProps | undefined
  nomPorteur: (bindId: number) => string | undefined
  texteCapacite: (option: Option) => string | undefined
  estEnMain: (bindId: number) => boolean
  ligneSansDefense?: string
  survolSansDefense?: string
  carteScene: (id: number, faceVisible: boolean) => ScanCardProps | undefined
}

export type VignetteOption = {
  optionId: number
  chiffre: number
  nom: string
  /** Le texte de la capacite, sous la vignette (D32). */
  sousTexte?: string
  scan?: ScanCardProps
  carteId?: number
  /** `failure_reason` du moteur : l'option se voit, grisee, et dit pourquoi. */
  indisponible?: string
  /** Defense : la DEF du defenseur et son nom seul, pour le bouton de l'essai. */
  defense?: { valeur: number; source: string }
}

export type CibleVue = {
  carteId: number
  scan?: ScanCardProps
  nom: string
  choisie: boolean
  horsTable: boolean
  fois?: number
  ordre?: number
  pulse?: boolean
}

export type VueSousCadre =
  | { genre: 'defense'; attaquantId?: number; defenseurs: VignetteOption[]; autres: VignetteOption[]; refus: string }
  | { genre: 'pendant-defense'; options: VignetteOption[]; refus: string }
  /** `refus` absent sur une question forcee : rien ne permet de la refuser. */
  | { genre: 'reponses'; titre: string; choix: VignetteOption[]; refus?: string }
  | { genre: 'choix-carte'; intitule: string; choix: VignetteOption[]; refus?: string }
  | { genre: 'cibles'; titre: string; cibles: CibleVue[]; choisies: number; minimum: number; maximum: number; prete: boolean; raison: string }
  | { genre: 'paiement'; titre: string; cartesMain: CibleVue[]; coutSlots: CoutSlot[]; consigne: string; phraseEtat: string; prete: boolean; libelleJouer: string }
  | { genre: 'confirmer'; titre: string; prete: boolean; raison: string }
  | { genre: 'ordre'; titre: string; cibles: CibleVue[]; prete: boolean }

/** L'option du moteur qui fait choisir l'ordre d'activation des sbires (`enemies.py`). */
const ORDRE_DES_SBIRES = 'Minion_Activates_Order'

/**
 * Les noms d'option qui ne sont qu'un TYPE de capacite, pas un nom propre.
 * Meme liste que `DemandeCentrale.tsx` (`TYPES_DE_CAPACITE`, non exportee) :
 * les deux doivent nommer une capacite de la meme facon.
 */
const TYPES_DE_CAPACITE =
  /^(forced |hero |alter-?ego )?(interrupt|response|action|resource|special|play|when revealed|defen[cs]e|attack|thwart|recover|scheme|activate|basic.*)$/i

/** Le moteur nomme-t-il une capacite propre (« Spider-Sense », « "I Object!" ») ? */
function capaciteNommee(nom: string): boolean {
  if (/^["«]/.test(nom) || /\u2014/.test(nom)) return true
  if (nom.includes('_')) return false
  return !TYPES_DE_CAPACITE.test(nom.trim())
}

/**
 * Le texte d'une capacite sans son en-tete : ni son nom (« « Sens d'Araignée »
 * » suivi du tiret long), ni son type (« Interruption : », « Response: ») que
 * le titre dit deja.
 */
function texteSansEntete(texte: string): string {
  return texte
    .replace(/^[«"]?\s*[^«»"\u2014]{2,60}?\s*[»"]?\s+\u2014\s+/, '')
    .replace(
      /^(?:(?:hero|alter-?ego|forced)\s+)?(?:réponse|interruption|response|interrupt|action)(?:\s+(?:forcée|de héros|d[’']alter-ego))?\s*:\s*/i,
      ''
    )
    .trim()
}

/** Le nom (francais si connu) de la carte qui porte l'option. */
function nomSource(option: Option, q: QuestionDuMoteur): string | undefined {
  if (option.bind_id === 0) return undefined
  const porteur = q.cartesParId.get(option.bind_id)
  return q.nomPorteur(option.bind_id) || (porteur ? nomAffiche(porteur) : undefined)
}

/** Le nom a ecrire sur la vignette : la capacite si elle en a un, sinon la carte. */
function nomOption(option: Option, q: QuestionDuMoteur): string {
  if (capaciteNommee(option.name)) return nomDeCapacite(option, q.texteCapacite(option))
  return nomSource(option, q) ?? nomLisible(option)
}

/**
 * LE TITRE D'UNE REPONSE (D31) : le nom d'abord, toujours, puis le texte
 * francais s'il existe, sinon celui du moteur. « Sens d'Araignée · … » pour une
 * capacite nommee ; « Réponse de Hulk · … », « Interruption de Backflip · … »
 * pour une capacite qui n'a qu'un type.
 */
export function titreReponse(option: Option, q: QuestionDuMoteur): string {
  const texte = q.texteCapacite(option)
  const corps = texte ? texteSansEntete(texte) : ''
  let tete: string
  if (capaciteNommee(option.name)) {
    tete = nomDeCapacite(option, texte)
  } else {
    const porteur = nomSource(option, q)
    const type = q.demande.ability_type
    if (porteur && /interrupt/i.test(type)) tete = t('Interruption de %1').replace('%1', porteur)
    else if (porteur && /response/i.test(type)) tete = t('Réponse de %1').replace('%1', porteur)
    else tete = porteur ?? nomLisible(option)
  }
  return corps ? `${tete} · ${corps}` : tete
}

function vignetteOption(option: Option, chiffre: number, q: QuestionDuMoteur, nom?: string): VignetteOption {
  const texte = q.texteCapacite(option)
  return {
    optionId: option.id,
    chiffre,
    nom: nom ?? nomOption(option, q),
    sousTexte: nom === undefined && texte ? texteSansEntete(texte) || undefined : undefined,
    // La carte que l'option nomme, sinon celle qui la porte : reconnaitre la
    // carte est la moitie de la comprehension (meme ordre que DemandeCentrale).
    scan:
      q.carteDeLOption?.(option) ??
      q.carteAuSurvol?.(option) ??
      (option.bind_id !== 0 ? q.carteScene(option.bind_id, true) : undefined),
    carteId: option.bind_id !== 0 ? option.bind_id : undefined,
    indisponible: option.failure_reason || undefined,
  }
}

/** Le nom d'une carte du monde, francais si le plateau le connait. */
function nomCarte(id: number, q: QuestionDuMoteur): string {
  const carte = q.cartesParId.get(id)
  return q.nomPorteur(id) || (carte ? nomAffiche(carte) : '')
}

/** Les cibles de l'option engagee : celles de la table, puis celles hors table. */
function ciblesDe(q: QuestionDuMoteur): CibleVue[] {
  const i = q.interaction
  return [
    ...[...i.cartes.entries()]
      .filter(([, etat]) => etat.role === 'cible')
      .map(([id, etat]) => ({
        carteId: id,
        scan: q.carteScene(id, true),
        nom: nomCarte(id, q),
        choisie: etat.choisie,
        horsTable: false,
        fois: etat.fois,
        ordre: etat.ordre,
        pulse: etat.pulse,
      })),
    ...i.ciblesHorsTable.map((cible) => ({
      carteId: Number(cible.props.id),
      scan: cible.props,
      nom: cible.props.name,
      choisie: cible.choisie,
      horsTable: true,
      fois: cible.fois,
      ordre: cible.ordre,
    })),
  ]
}

/**
 * LA QUESTION, EN DONNEES. L'ordre des tests compte :
 *  1. une option deja ENGAGEE se compose (ordre, cibles, paiement, confirmation),
 *     selon l'etape de l'assistant (`interaction.assistant.etape`) ;
 *  2. une option `Defense` dans la demande fait la rangee de defense, TESTEE
 *     AVANT `estFenetreDeReaction`, qui englobe la defense (piege 35) ;
 *  3. l'ordre des sbires (option forcee, unique) ;
 *  4. un choix pose par une carte revelee se lit a droite de la carte (D18) ;
 *  5. le defenseur connu (fait `boosts`) : les cartes jouables dans la rangee (D8) ;
 *  6. tout le reste : le sous-cadre des reponses (D4, D32).
 */
export function vueSousCadre(
  q: QuestionDuMoteur,
  ctx: { etape?: EtapeDeroule; tempsQuestion?: TempsPhase }
): VueSousCadre {
  const i = q.interaction
  const options = i.options

  if (i.option) {
    const engagee = i.option
    if (engagee.name === ORDRE_DES_SBIRES) {
      return { genre: 'ordre', titre: t('Choisir l’ordre'), cibles: ciblesDe(q), prete: i.prete }
    }
    const titre = titreReponse(engagee, q)
    if (i.assistant.etape === 'target') {
      return {
        genre: 'cibles',
        titre,
        cibles: ciblesDe(q),
        choisies: i.cibles.length,
        minimum: engagee.target_num_range[0],
        maximum: engagee.target_num_range[1],
        prete: i.prete,
        raison: i.raison,
      }
    }
    if (i.assistant.etape === 'payment') {
      return {
        genre: 'paiement',
        titre,
        // Les cartes qui PEUVENT payer (role `ressource`), et celles deja
        // depensees : la main est cachee pendant la phase (D3), c'est ici seul
        // qu'elle se voit.
        cartesMain: [...i.cartes.entries()]
          .filter(([, etat]) => etat.role === 'ressource')
          .map(([id, etat]) => ({
            carteId: id,
            scan: q.carteScene(id, true),
            nom: nomCarte(id, q),
            choisie: etat.choisie,
            horsTable: false,
            fois: etat.fois,
            pulse: etat.pulse,
          })),
        coutSlots: i.assistant.coutSlots,
        consigne: i.assistant.titre,
        phraseEtat: i.assistant.detail ?? '',
        prete: i.prete,
        libelleJouer: t('Jouer %1').replace('%1', nomSource(engagee, q) ?? nomLisible(engagee)),
      }
    }
    return { genre: 'confirmer', titre, prete: i.prete, raison: i.raison }
  }

  const defenses = options.filter((option) => option.name === 'Defense')
  if (defenses.length > 0) {
    const refus = libelleRefus(
      options,
      estFenetreDeReaction(q.demande),
      q.cartesParId,
      q.nomPorteur,
      q.texteCapacite,
      q.estEnMain
    )
    return {
      genre: 'defense',
      // Le plateau suppose l'attaquant en premiere cible legale de la defense
      // (meme hypothese que `ligne-attaque.ts`).
      attaquantId: defenses[0]?.all_legal_targets[0],
      defenseurs: defenses.map((option, rang) => {
        const source = nomSource(option, q)
        const def = ligneDefense(q.cartesParId.get(option.bind_id), q.nomPorteur)
        const nom = source ? `${t('Défendre avec')} ${source}${def ? ` (${def})` : ''}` : nomLisible(option)
        const valeur = q.cartesParId.get(option.bind_id)?.info?.defense
        return {
          ...vignetteOption(option, rang + 1, q, nom),
          defense: source && typeof valeur === 'number' ? { valeur, source } : undefined,
        }
      }),
      autres: options
        .filter((option) => option.name !== 'Defense')
        .map((option, rang) => vignetteOption(option, defenses.length + rang + 1, q)),
      refus: q.ligneSansDefense ? `${refus} (${q.ligneSansDefense})` : refus,
    }
  }

  const seule = options.length === 1 ? options[0] : undefined
  if (seule?.name === ORDRE_DES_SBIRES) {
    // Pas encore engagee : les memes sbires, a cliquer dans l'ordre.
    return {
      genre: 'ordre',
      titre: t('Choisir l’ordre'),
      cibles: [...new Set(seule.all_legal_targets)].map((id) => ({
        carteId: id,
        scan: q.carteScene(id, true),
        nom: nomCarte(id, q),
        choisie: i.cartes.get(id)?.choisie ?? false,
        horsTable: false,
        ordre: i.cartes.get(id)?.ordre,
      })),
      prete: false,
    }
  }

  const choix = options.map((option, rang) => vignetteOption(option, rang + 1, q))

  if (ctx.tempsQuestion === 'revelation' && q.demande.event_name === 'WhenPlayerChooseAbility') {
    const prompt = nettoyerNarration(sansIdentifiantsEnFrancais(q.demande.prompt_text))
      .replace(/^---\s*/, '')
      .replace(/\s*---$/, '')
    return {
      genre: 'choix-carte',
      intitule: prompt || t('Choisis une réponse'),
      // Chaque choix par son TEXTE (« Subir 2 dégâts »), jamais par la carte
      // qui le porte : c'est la carte revelee, deja en grand a gauche, et deux
      // vignettes identiques ne disaient plus lequel faisait quoi (planche du
      // lot 4, Poseur de Bombe d'Hydra). Une carte que le choix NOMME garde
      // sa vignette.
      choix: options.map((option, rang) => ({
        ...vignetteOption(option, rang + 1, q, nomLisible(option)),
        scan: q.carteDeLOption?.(option),
      })),
      refus: q.demande.show_cancel ? t('Passer') : undefined,
    }
  }

  const etape = ctx.etape
  if (
    etape?.titre === 'attaque' &&
    etape.etat === 'annonce' &&
    etape.defenseurId !== undefined &&
    q.demande.show_cancel
  ) {
    return { genre: 'pendant-defense', options: choix, refus: t('Continuer sans rien jouer') }
  }

  let refus: string | undefined
  if (q.demande.show_cancel) {
    // « Ne rien jouer » devient « Aucune réponse » quand plusieurs reponses
    // sont proposees (D32) ; une seule garde son refus nomme (« Ne pas
    // utiliser Sens d'Araignée », « Ne pas jouer Backflip »).
    refus =
      options.length > 1
        ? t('Aucune réponse')
        : libelleRefus(options, estFenetreDeReaction(q.demande), q.cartesParId, q.nomPorteur, q.texteCapacite, q.estEnMain)
  }
  return {
    genre: 'reponses',
    titre: seule ? titreReponse(seule, q) : phraseDeReaction(options, q.cartesParId, q.nomPorteur),
    // Une seule reponse : le titre porte deja son texte, le redire sous la
    // vignette l'ecrivait deux fois (planche du lot 6, etat 11a).
    choix: seule ? choix.map((vignette) => ({ ...vignette, sousTexte: undefined })) : choix,
    refus,
  }
}
