// Mise en phrase des etapes du deroule.
//
// Separe du decoupage (deroule-phase.ts) a dessein : le decoupage est une
// question de regles du jeu, la mise en phrase une question de langue. Les
// deux se testent separement, et le decoupage reste verifiable sans toucher
// au dictionnaire.

import type { EtapeDeroule, LigneBilan } from './deroule-phase'
import { langueActuelle, t } from './langue'
import { libelleStatut } from './effets-statuts'
import type { EffetRevelation } from './world'

/** Cles de titre que ce module sait rediger. Tout autre titre passe tel quel. */
const REDIGES = new Set([
  'attaque',
  'manigance',
  'menace',
  'statut',
  'distribution',
  'revelation',
  'entree',
  'bilan',
])

/**
 * Accord du pluriel francais : « 1 degat », « 2 degats ». L'anglais rend le
 * meme mot des deux cotes du dictionnaire, ce qui est correct la-bas.
 */
function pluriel(nombre: number, singulier: string, pluriels: string): string {
  return Math.abs(nombre) < 2 ? t(singulier) : t(pluriels)
}

/**
 * Le nom d'une carte de statut dans la langue du plateau.
 *
 * Le moteur les nomme « Stunned », « Confused », « Tough » ; `libelleStatut`
 * (effets-statuts.ts, deja employe par le badge sur la carte) les traduit
 * depuis la meme table, en minuscules. Une seule table pour les deux, sans
 * quoi le badge et le cartouche pourraient se contredire.
 */
export function libelleDeStatut(statut: string | undefined): string {
  const cle = (statut ?? '').toLowerCase()
  if (cle === 'stunned' || cle === 'confused' || cle === 'tough') {
    return libelleStatut(cle, 1, langueActuelle())
  }
  return statut ?? ''
}

export function titreEtape(etape: EtapeDeroule): string {
  if (!REDIGES.has(etape.titre)) return etape.titre

  // Le bilan n'a ni auteur ni cible : c'est le point final de la phase, pas un
  // coup de plus. Son detail se lit sur ses lignes, juste en dessous.
  if (etape.titre === 'bilan') return t('Fin de la phase du méchant')

  // Les noms viennent du FAIT (voir deroule-phase.ts), pas d'une recherche
  // dans l'index du monde courant : une carte morte pendant la phase n'y est
  // plus, et l'etape affichait alors « Ultron attaque #88 ».
  const auteur = etape.auteurNom ?? ''
  const cible = etape.cibleNom ?? ''

  if (etape.titre === 'statut') {
    // « Klaw gagne Sonné ». Le porteur, puis la carte de statut, nommee comme
    // sur la table. Sans porteur connu, une formule impersonnelle plutot
    // qu'un « undefined gagne », comme partout ailleurs ici.
    const nom = libelleDeStatut(etape.statut)
    if (!cible) return `${t('Une carte de statut est posée')} : ${nom}`
    return `${cible} ${t('gagne')} ${nom}`
  }

  if (etape.titre === 'menace') {
    // Repli sur l'ancienne formule generique quand la source ne donne ni nom
    // ni montant : une phrase vague vaut mieux qu'une phrase fausse, et
    // « gagne undefined menaces » serait pire que tout.
    if (!cible || etape.montant === undefined) return t('Menace sur la manigance principale')
    return `${cible} ${t('gagne')} ${etape.montant} ${pluriel(etape.montant, 'menace', 'menaces')}`
  }

  if (etape.titre === 'distribution') {
    // La carte est FACE CACHEE : on ne nomme que le heros qui la recoit. Sans
    // heros connu, repli sur une formule impersonnelle, comme partout ailleurs
    // ici : mieux vaut une phrase vague qu'un « undefined recoit ».
    //
    // L'etape porte le nombre de cartes du joueur (`montant`, une etape par
    // joueur) : en Heroique chacun en recoit deux, et « recoit sa carte
    // rencontre » aurait alors menti sur ce qui vient d'arriver. Un montant
    // absent (moteur ou sauvegarde anterieurs au regroupement) vaut une carte.
    const cartes = etape.montant ?? 1
    if (cartes > 1) {
      return auteur
        ? `${auteur} ${t('reçoit')} ${cartes} ${t('cartes rencontre')}`
        : `${cartes} ${t('cartes rencontre distribuées')}`
    }
    return auteur
      ? `${auteur} ${t('reçoit sa carte rencontre')}`
      : t('Carte rencontre distribuée')
  }

  if (etape.titre === 'entree') {
    // « Drone entre en jeu ». La cause (Ultron, un boost) s'affiche dessous,
    // par `texteCauseActivation`, comme pour une activation declenchee.
    if (!cible) return t('Un sbire entre en jeu')
    return `${cible} ${t('entre en jeu')}`
  }

  if (etape.titre === 'revelation') {
    // Sans heros connu (joueur introuvable, ou l'appelant ne l'a pas fourni),
    // repli sur l'ancienne formule generique : une carte revelee anonyme vaut
    // mieux qu'un « undefined révèle ».
    return auteur ? `${auteur} ${t('révèle')} ${cible}` : `${cible} ${t('révélée')}`
  }

  // L'INTENTION, au futur proche : « Klaw VA attaquer Colossus ». C'est le
  // temps ou le joueur peut encore defendre ou repondre, et le seul endroit du
  // cartouche ou l'on parle d'un coup qui n'a pas eu lieu. Une activation
  // annulee garde ce meme titre : elle a bien ete annoncee, c'est la suite qui
  // manque, et `texteActivationAnnulee` la dit juste en dessous.
  if (etape.etat === 'annonce' || etape.etat === 'annule') {
    return etape.titre === 'attaque'
      ? `${auteur} ${t('va attaquer')} ${cible}`
      : `${auteur} ${t('va manigancer sur')} ${cible}`
  }

  return etape.titre === 'attaque'
    ? `${auteur} ${t('attaque')} ${cible}`
    : `${auteur} ${t('manigance sur')} ${cible}`
}

/**
 * Le chiffre du coup, sous le titre : « → 4 dégâts », « → 2 menaces ».
 *
 * Vide pour l'etape de menace, dont le chiffre est deja dans le titre, et
 * pour toute etape dont la source ne donne pas de montant.
 */
export function resultatEtape(etape: EtapeDeroule): string {
  // Sur une ANNONCE, la valeur imprimee, et dite pour ce qu'elle est : ni la
  // defense ni les cartes de boost ne sont encore connues, donc ce nombre-la
  // n'est pas un resultat. Une annulation ne le montre pas : il n'y a plus
  // rien a attendre, et `texteActivationAnnulee` prend sa place.
  if (etape.etat === 'annonce') {
    if (etape.valeurAnnoncee === undefined) return ''
    if (etape.titre === 'attaque') {
      return `→ ${etape.valeurAnnoncee} ${pluriel(etape.valeurAnnoncee, 'dégât annoncé', 'dégâts annoncés')}`
    }
    if (etape.titre === 'manigance') {
      return `→ ${etape.valeurAnnoncee} ${pluriel(etape.valeurAnnoncee, 'menace annoncée', 'menaces annoncées')}`
    }
    return ''
  }
  if (etape.montant === undefined) return ''
  if (etape.titre === 'attaque') {
    return `→ ${etape.montant} ${pluriel(etape.montant, 'dégât', 'dégâts')}`
  }
  if (etape.titre === 'manigance') {
    return `→ ${etape.montant} ${pluriel(etape.montant, 'menace', 'menaces')}`
  }
  return ''
}

/**
 * Le compteur de la cible apres le coup, a droite du titre : « 5/8 » pour une
 * manigance sur son seuil, « 7 » pour des points de vie, qui n'en ont pas.
 *
 * Rien du tout sans compteur : un « undefined » ou un « 0/0 » vaut moins que
 * l'absence, et un compteur faux serait pire que pas de compteur. Aucun
 * passage par le dictionnaire ici, il n'y a que des chiffres.
 */
/**
 * D'ou vient le chiffre du coup : l'imprime, les boosts un par un, le total,
 * puis ce que la defense a bloque et ce qui a ete subi. Livraison B de la
 * spec du 7 septembre 2026. Sans imprime connu, ou sans boost ni defense (le
 * detail n'apprendrait rien), c'est le resultat simple.
 */
export function detailEtape(etape: EtapeDeroule): string {
  if (etape.etat !== 'resolu' || etape.montant === undefined || etape.base === undefined) {
    return resultatEtape(etape)
  }
  if (etape.titre !== 'attaque' && etape.titre !== 'manigance') return resultatEtape(etape)
  const defense = etape.defense ?? 0
  if (etape.boosts.length === 0 && defense <= 0) return resultatEtape(etape)
  const brut = etape.base + etape.boosts.reduce((somme, boost) => somme + boost.apport, 0)
  const unite = (n: number) =>
    etape.titre === 'attaque' ? pluriel(n, 'dégât', 'dégâts') : pluriel(n, 'menace', 'menaces')
  const termes = [`${etape.base} ${t('imprimé')}`]
  for (const boost of etape.boosts) termes.push(`+ ${boost.apport} (${boost.nom})`)
  let texte = `${termes.join(' ')} = ${brut} ${unite(brut)}`
  if (defense > 0) {
    texte += ` · ${defense} ${t('bloqué par la défense')} · ${etape.montant} ${pluriel(etape.montant, 'subi', 'subis')}`
  }
  return texte
}

/**
 * Ce que le coup a change : « 5 → 7 / 12 » sur une manigance, « Shuri 12 → 8
 * PV » sur un personnage. L'AVANT se deduit du restant et du montant : le
 * fait ne le porte pas, et la table ne peut pas le donner (elle est deja
 * apres). `pvMax` vient du monde (DeroulePhase, `pvMaxParNom`) : le fait
 * d'attaque ne connait pas le maximum de sa cible.
 */
export function evolutionEtape(etape: EtapeDeroule, pvMax?: number): string {
  if (typeof etape.restant !== 'number' || !Number.isFinite(etape.restant)) return ''
  if (etape.montant === undefined) return compteur(etape.restant, etape.plafond)
  const menace = etape.titre === 'menace' || etape.titre === 'manigance'
  if (menace) {
    const avant = Math.max(0, etape.restant - etape.montant)
    const seuil = typeof etape.plafond === 'number' && etape.plafond > 0 ? ` / ${etape.plafond}` : ''
    return `${avant} → ${etape.restant}${seuil}`
  }
  if (etape.titre !== 'attaque') return compteur(etape.restant, etape.plafond)
  // Le maximum plafonne l'avant reconstitue : un coup de 6 sur 4 PV laisse
  // la cible a 0, elle n'avait pas 6 PV.
  const connu = typeof pvMax === 'number' && pvMax > 0
  const avant = connu ? Math.min(etape.restant + etape.montant, pvMax) : etape.restant + etape.montant
  const seuil = connu ? ` / ${pvMax}` : ''
  const nom = etape.cibleNom ? `${etape.cibleNom} ` : ''
  return `${nom}${avant} → ${etape.restant}${seuil} ${t('PV')}`
}

function compteur(restant: number | undefined, plafond: number | undefined): string {
  if (typeof restant !== 'number' || !Number.isFinite(restant)) return ''
  // Le seuil ne s'affiche que s'il en est un : un plafond absent ou nul ne dit
  // rien et donnerait un « 0/0 ».
  if (typeof plafond === 'number' && plafond > 0) return `${restant}/${plafond}`
  return `${restant}`
}

export function compteurEtape(etape: EtapeDeroule): string {
  return compteur(etape.restant, etape.plafond)
}

/**
 * Une ligne du bilan : « Colossus a pris 6 dégâts », « L’Effraction ! a gagné
 * 3 menaces ». Le total est deja fait (voir `lignesBilan`), on le met en
 * phrase et rien de plus.
 */
export function texteLigneBilan(ligne: LigneBilan): string {
  if (ligne.genre === 'statuts') {
    const nom = libelleDeStatut(ligne.statut)
    // « Klaw gagne Sonné », et « x2 » quand la meme carte est posee deux fois
    // (Solide en demande deux pour mordre).
    return `${ligne.cibleNom} ${t('gagne')} ${nom}${ligne.total > 1 ? ` x${ligne.total}` : ''}`
  }
  if (ligne.genre === 'degats') {
    return `${ligne.cibleNom} ${t('a pris')} ${ligne.total} ${pluriel(ligne.total, 'dégât', 'dégâts')}`
  }
  return `${ligne.cibleNom} ${t('a gagné')} ${ligne.total} ${pluriel(ligne.total, 'menace', 'menaces')}`
}

/**
 * Le compteur de la cible a droite de sa ligne de bilan, meme regle qu'ailleurs
 * dans le cartouche : rien du tout quand la source n'en donne pas.
 *
 * Les points de vie s'affichent « 8/14 » quand l'appelant du bilan a pu donner
 * les PV maximum (board.tsx, qui lit le monde), et « 8 » tout seul sinon : le
 * moteur ne les publie pas a cote de ses faits, et un maximum invente serait
 * pire que pas de maximum.
 */
export function compteurLigneBilan(ligne: LigneBilan): string {
  return compteur(ligne.restant, ligne.plafond)
}

/**
 * L'annonce de la chute d'un heros : « Colossus est vaincu ».
 *
 * Rien du tout sans la marque posee par `etapesDeroule` (voir
 * `EtapeDeroule.defaite`), et rien du tout sans nom : une defaite anonyme
 * n'apprendrait rien, et une defaite annoncee a tort ferait douter le joueur de
 * tout le reste du cartouche.
 *
 * Accord au masculin, comme partout ailleurs sur le plateau (« Les heros sont
 * vaincus », « Heros vaincu : il ne participe pas... ») : le monde ne publie
 * pas le genre d'un heros, et l'inventer se tromperait une fois sur deux.
 */
export function texteDefaite(etape: EtapeDeroule): string {
  if (!etape.defaite) return ''
  const nom = etape.cibleNom ?? ''
  if (!nom) return ''
  // Cle a trous plutot qu'une concatenation : l'anglais ne place pas le verbe
  // au meme endroit (« Colossus is defeated »).
  return t('%1 est vaincu').replace('%1', nom)
}

/**
 * Ce que dit une activation ANNULEE : le coup annonce n'a pas eu lieu.
 *
 * Vide sur toute autre etape. Sans cette phrase, l'etape resterait sur son
 * « Klaw va attaquer Colossus » et le joueur attendrait un coup qui ne vient
 * pas.
 */
export function texteActivationAnnulee(etape: EtapeDeroule): string {
  if (etape.etat !== 'annule') return ''
  return etape.titre === 'attaque'
    ? t('L\'attaque n\'a pas lieu.')
    : t('La manigance n\'a pas lieu.')
}

/**
 * D'OU vient cette activation, quand ce n'est pas la regle du jeu.
 *
 * « Klaw attaque Colossus » pendant les activations n'a besoin d'aucune
 * explication : c'est le point 2 de la phase. Mais le meme vilain qu'une carte
 * revelee fait frapper une SECONDE fois parait sortir de nulle part, et c'est
 * exactement ce qui avait ete signale en jeu. Le moteur ne remplit `cause` que
 * dans ce second cas (`CauseDeLActivation` rend '' pendant les activations).
 */
export function texteCauseActivation(etape: EtapeDeroule): string {
  if (!etape.cause) return ''
  return `${t('déclenché par')} ${etape.cause}`
}

/**
 * La mention de la fenetre de reponse, sous une etape d'INTENTION.
 *
 * Elle ne s'affiche QUE quand le moteur pose effectivement une question au
 * joueur local (voir DeroulePhase, `questionAuJoueur`) : l'ecrire quand rien
 * n'est jouable inviterait a chercher une reponse qui n'existe pas, et le
 * joueur cesserait de la lire.
 */
export function texteFenetreReponse(): string {
  return t('tu peux défendre ou répondre')
}

/**
 * CE QU'ON ATTEND, a la place meme ou l'on lisait « La suite arrive… ».
 *
 * Trois phrases pour trois attentes, et c'etait tout le defaut : la meme
 * phrase servait a dire « le moteur calcule » et « la table attend un
 * coequipier parti chercher un cafe » (constat F5 de l'audit du 06/09/2026).
 *
 * Le nom manque encore quand le moteur ne dit pas QUI il attend : un moteur
 * ancien ne publie pas quel client est en retard sur son accuse de reception
 * (voir l'en-tete de `attente-table.ts`). On le dit alors sans en inventer un.
 */
export function texteAttente(attente: { autreJoueur?: boolean; nom?: string }): string {
  if (!attente.autreJoueur) return t('La suite arrive…')
  // Cle a trous plutot qu'une concatenation : l'anglais ne place pas le nom au
  // meme endroit selon la tournure, comme pour « %1 est vaincu ».
  if (attente.nom) return t('En attente de %1').replace('%1', attente.nom)
  return t('En attente d\'un autre joueur')
}

/**
 * LE FILET VA JOUER : « La phase reprend dans 12 s ».
 *
 * Le moteur relache la phase tout seul au bout d'un temps borne, pour qu'un
 * onglet fantome ne gele pas la table (voir `DELAI_FILET_ANTI_BLOCAGE_CLIC_MS`,
 * moteur.ts). Le dire avant evite que la phase qui repart seule ressemble a un
 * bug.
 */
export function texteFiletProche(secondes: number): string {
  return t('La phase reprend dans %1 s').replace('%1', String(secondes))
}

/**
 * « TEMPS PAR DECISION » REGLE : le moteur n'attend pas.
 *
 * Le mode Detaille repose sur une hypothese : le moteur ne produit rien tant
 * qu'on ne lui a pas repondu, donc le cartouche donne le rythme. Elle tombe des
 * que la preparation de mission regle un « Temps par decision » non nul
 * (`max_timeout`, publie dans la trame) : `DoWaitSync` et `DoGetInput`
 * expirent, et le moteur poursuit sans notre accuse ni notre reponse. On le
 * dit, sobrement, plutot que de laisser le joueur croire a un defaut.
 */
export function texteTempsParDecision(): string {
  return t('Temps par décision réglé : le moteur n’attend pas')
}

/** La phrase qui dit que le deroule s'arrete la. */
export function texteArretDefaite(): string {
  return t('La phase s\'arrête ici.')
}

/** Ce que dit le bilan quand la phase n'a rien coute du tout. */
export function texteBilanVide(): string {
  return t('Aucun dégât, aucune menace.')
}

const REGLES: Record<string, string> = {
  'regle:menace': 'Point 1 : chaque joueur ajoute 1 menace à la manigance principale.',
  'regle:activations': 'Point 2 : chaque ennemi s\'active contre le héros engagé avec lui.',
  'regle:distribution': 'Point 3 : chaque joueur reçoit une carte rencontre, face cachée.',
  'regle:revelation': 'Point 4 : chaque joueur révèle sa carte rencontre et en applique l\'effet.',
  'regle:entree': 'Un sbire qui entre en jeu pendant la phase du méchant s\'active à l\'étape des sbires, s\'il est arrivé avant elle.',
  'regle:statut': 'Une carte de statut posée reste jusqu\'à ce qu\'elle soit consommée : sonné annule la prochaine attaque, désorienté la prochaine manigance, robuste absorbe les dégâts d\'une attaque.',
}

/**
 * Ce que la carte revelee a FAIT, un effet par ligne : « → Patrouille d'Hydra
 * gagne 2 menaces (5) », « → Scott Lang subit 1 degat (10 PV) », « → Hydra
 * Mercenary entre en jeu (sbire) ». Les chiffres viennent du moteur, qui a
 * mesure la table avant et apres (voir `EffetRevelation`).
 */
export function texteEffet(effet: EffetRevelation): string {
  const restant = (valeur: number | null | undefined, suffixe = '') =>
    typeof valeur === 'number' && Number.isFinite(valeur) ? ` (${valeur}${suffixe})` : ''
  if (effet.genre === 'menace') {
    return `→ ${effet.cible} ${t('gagne')} ${effet.montant} ${pluriel(effet.montant, 'menace', 'menaces')}${restant(effet.restant)}`
  }
  if (effet.genre === 'degats') {
    return `→ ${effet.cible} ${t('subit')} ${effet.montant} ${pluriel(effet.montant, 'dégât', 'dégâts')}${restant(effet.restant, ` ${t('PV')}`)}`
  }
  return `→ ${effet.carte} ${t('entre en jeu')} (${t(effet.type)})`
}

export function regleEtape(etape: EtapeDeroule): string {
  const regle = REGLES[etape.regle]
  return regle ? t(regle) : ''
}


/** Un morceau de phrase : du texte, en gras ou non. */
export type MorceauDePhrase = {
  texte: string
  gras: boolean
  /**
   * La carte que ce nom désigne, quand on la connaît.
   *
   * ⚠ C'EST ELLE QUI REND LE NOM SURVOLABLE. Demande de l'utilisateur,
   * 15/09/2026 : « arrête de montrer les cartes ; par contre, quand on hover
   * sur le nom, on voit la carte en question ». Un nom sans carte connue reste
   * du texte ordinaire : on ne promet que ce qu'on peut tenir.
   */
  carteId?: number
}

/**
 * La phrase de l'etape, decoupee pour mettre les NOMS DE CARTES en gras.
 *
 * Choix de l'utilisateur parmi trois formes (14/09/2026) : « moitie-moitie,
 * les noms en gras ». On repere qui fait quoi a qui d'un coup d'oeil, sans que
 * la phrase crie comme un titre.
 *
 * ⚠ RETOURNE DES DONNEES, PAS DU JSX. Ce fichier est la mise en PHRASE, pas la
 * mise en page : il reste en `.ts`, testable sans rendu, et c'est le composant
 * qui decide a quoi ressemble un morceau en gras.
 *
 * ⚠ ON DECOUPE SUR LES NOMS QUE L'ETAPE PORTE, jamais sur le texte redige.
 * `titreEtape` compose « <auteur> attaque <cible> » a partir de `auteurNom` et
 * `cibleNom` : ce sont exactement ces chaines-la qui figurent dans la phrase,
 * quelle que soit la langue. Chercher « un nom propre » dans une phrase
 * traduite casserait a la premiere traduction.
 *
 * ⚠ ET LES NOMS PEUVENT SE CONTENIR. « Spider-Man » et « Spider-Man 2099 », ou
 * un auteur qui est aussi la cible : on traite donc du PLUS LONG au plus court,
 * et on ne repasse jamais sur un morceau deja mis en gras.
 */
export function decouperPhrase(
  phrase: string,
  noms: Array<string | undefined>,
  /**
   * L'identifiant de carte de CHAQUE nom, dans le même ordre que `noms`.
   * Facultatif : sans lui, le découpage se comporte exactement comme avant.
   */
  idsDesNoms: Array<number | undefined> = []
): MorceauDePhrase[] {
  const idParNom = new Map<string, number>()
  noms.forEach((nom, rang) => {
    const id = idsDesNoms[rang]
    if (nom && id !== undefined && !idParNom.has(nom)) idParNom.set(nom, id)
  })
  const cherches = [...new Set(noms.filter((n): n is string => Boolean(n && n.trim())))].sort(
    (a, b) => b.length - a.length
  )
  let morceaux: MorceauDePhrase[] = [{ texte: phrase, gras: false }]
  for (const nom of cherches) {
    const suivants: MorceauDePhrase[] = []
    for (const morceau of morceaux) {
      if (morceau.gras) {
        suivants.push(morceau)
        continue
      }
      const parts = morceau.texte.split(nom)
      parts.forEach((part, i) => {
        if (i > 0) suivants.push({ texte: nom, gras: true, carteId: idParNom.get(nom) })
        if (part) suivants.push({ texte: part, gras: false })
      })
    }
    morceaux = suivants
  }
  return morceaux
}
