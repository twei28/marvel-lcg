// POURQUOI CETTE CARTE EST-ELLE INJOUABLE ?
//
// Demande de l'utilisateur, 10 septembre 2026 : « quand on survole une carte
// qu'on ne peut pas jouer, j'aimerais avoir la raison ». Et, sur la question
// des motifs qu'on ne saurait pas traduire : « ça ne doit pas arriver ».
//
// CE QUI SE PASSAIT AVANT. Le moteur calculait bien la raison, puis la jetait :
// `EventManager.FilterAvailableEffects` ecarte l'effet refuse ET le motif que
// `CheckCondition` vient d'ecrire. La carte injouable n'etait donc meme pas
// mentionnee dans la question envoyee au plateau. Le code qui lisait
// `failure_reason` (interaction.ts, DemandeCentrale, BarreAction) etait un
// vestige : il ne recevait jamais rien.
//
// CE QUI SE PASSE MAINTENANT. Le moteur joint les refus dans un CANAL SEPARE
// (`refus_json`), sans toucher a `options_json` : ni l'autoplay, ni le harnais
// des cas, ni le plateau existant ne changent de comportement. Le moteur
// n'envoie pas de phrase, il envoie un CODE STABLE ; c'est ici qu'on ecrit la
// phrase, en francais, et `t()` la rend en anglais. Sinon le jeu anglais
// recevrait du francais en dur.
//
// LES CODES. Presque tous sont deja des identifiants du moteur : une valeur de
// `EffectFailure` (« out of play ») ou le nom de la fonction de condition qui a
// refuse (« check_hero_form_only »). Un seul porte des chiffres, celui du cout,
// normalise en `cout_insuffisant|<demande>|<disponible>` par
// `Controller.NormaliserLeMotif`.
//
// ⚠ MESURE, PAS SUPPOSITION (10/09/2026). Il existe 276 noms de conditions
// distincts dans le moteur et 248 de plus dans les modules de cartes, et cela
// n'a servi a rien de les compter : sur QUATRE decks joues en entier, il n'est
// remonte que SEPT motifs. C'est cette table-la. Les autres conditions filtrent
// des evenements, elles ne bloquent pas une carte en main.
//
// ⚠ UN CODE SANS PHRASE EST UN DEFAUT, PAS UN CAS TOLERE. C'est la consigne, et
// elle est tenue par une gate : `tools/verifier_raisons_refus.py` joue de
// vraies parties et ECHOUE des qu'un code atteint le plateau sans entree ici.
// Ajouter une carte qui refuse pour un motif neuf fera donc rougir la batterie,
// pas passer un silence inapercu.

import { t } from './langue'

/** Nom lisible d'une couleur de ressource, pour dire ce qui manque. */
function ressourcesLisibles(brut: string): string {
  const NOMS: Record<string, string> = {
    R: 'physique',
    B: 'mental',
    Y: 'énergie',
    G: 'joker',
    L: 'éclair',
  }
  const lettres = brut.split('').filter((c) => c in NOMS)
  if (lettres.length === 0) return brut
  return lettres.map((c) => t(NOMS[c] as string)).join(', ')
}

/**
 * Les phrases, par code. Le francais est la source ; `t()` donne l'anglais.
 *
 * Le ton : on dit ce qui BLOQUE, pas ce qu'il faudrait faire. « Jouable
 * seulement sous forme de héros » et non « passe en forme de héros » : le
 * joueur sait mieux que nous s'il veut changer de forme.
 */
const PHRASES: Record<string, () => string> = {
  // --- La forme de l'identite -------------------------------------------
  // ⚠ Un code est le nom de la CONDITION QUI A REFUSE (ability.py:113-123),
  // pas l'etat du joueur. `player_is_hero` est posee sur toute capacite de
  // heros : si elle refuse, c'est que le joueur n'est PAS heros, donc la
  // carte demande la forme de heros. Les deux phrases ont ete livrees
  // croisees le 10/09/2026 (Lancer de Bouclier annoncait « alter ego »),
  // corrigees le 11/09.
  player_is_hero: () => t('Jouable seulement sous forme de héros'),
  check_hero_form_only: () => t('Jouable seulement sous forme de héros'),
  player_is_alter_ego: () => t("Jouable seulement sous forme d'alter ego"),

  // --- Le paiement --------------------------------------------------------
  check_can_pay: () => t('Pas assez de ressources'),
  'no cost target': () => t('Rien à dépenser pour payer le coût'),
  check_cannot_generate_self: () => t('Une carte ne peut pas payer son propre coût'),

  // --- Les cibles ---------------------------------------------------------
  'update legal targets': () => t('Aucune cible possible en ce moment'),

  // --- L'etat de la carte -------------------------------------------------
  'out of play': () => t("Cette carte n'est plus en jeu"),
  'is removed': () => t('Cette carte a été retirée de la partie'),
  'treat as blank': () => t('Le texte de cette carte est considéré comme vierge'),
  'already processed in this message': () => t('Déjà résolu pour cette carte'),
  'max targets is 0': () => t('Aucune cible possible en ce moment'),
  'no filter targets': () => t('Aucune cible possible en ce moment'),
  'targets num': () => t('Pas le bon nombre de cibles'),
  'engaged different player': () => t("Cet ennemi est engagé avec un autre joueur"),
  'already resolves defense ability': () =>
    t('Une carte de défense a déjà été jouée contre cette attaque'),
  'type count not enough': () => t("Il n'y a pas assez de cartes de ce type"),
  'check target': () => t('Aucune cible possible en ce moment'),
  'check pay': () => t('Pas assez de ressources'),
  'has cost but no ask player': () => t("Le coût ne peut être payé par personne"),
  'bind face is defeating': () => t('La carte porteuse est en train d’être vaincue'),
}

/** Les codes a parametres, traites a part : ils portent des chiffres. */
function phraseParametree(code: string): string | undefined {
  if (code.startsWith('cout_insuffisant|')) {
    const [, demande, disponible] = code.split('|')
    const manque = t('Coût de') + ` ${demande ?? '?'}`
    if (!disponible) return manque
    return `${manque}, ` + t('tu as') + ` ${ressourcesLisibles(disponible)}`
  }
  return undefined
}

/**
 * La phrase a montrer au joueur, ou `undefined` si le code est inconnu.
 *
 * ⚠ Ne pas confondre avec `glisser/cibles.raisonDuRefus`, qui cherche QUEL
 * refus s'applique a un lacher donne et rend son CODE. Les deux se completent :
 * l'un designe le refus, l'autre l'ecrit en francais.
 *
 * ⚠ `undefined` ne doit JAMAIS arriver en partie : c'est ce que la gate
 * verifie. On rend `undefined` plutot qu'une phrase creuse pour que le silence
 * soit detectable par un test, au lieu d'etre maquille en reponse.
 */
export function phraseDuRefus(code: string): string | undefined {
  const brut = code.trim()
  if (!brut) return undefined
  const parametree = phraseParametree(brut)
  if (parametree !== undefined) return parametree
  const phrase = PHRASES[brut]
  return phrase ? phrase() : undefined
}

/** Les codes connus, pour la gate et pour les tests. */
export function codesConnus(): string[] {
  return [...Object.keys(PHRASES), 'cout_insuffisant']
}
