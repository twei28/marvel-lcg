// « Quand on survole une carte qu'on ne peut pas jouer, j'aimerais avoir la
// raison » (utilisateur, 10/09/2026). Et, sur les motifs non traduits :
// « ça ne doit pas arriver ».
//
// Ces cas gardent la table de phrases. La GATE, elle, vit cote moteur
// (`tools/verifier_raisons_refus.py`) : elle joue de vraies parties et echoue
// des qu'un code atteint le plateau sans entree ici. Les deux sont
// complementaires : ici on verifie ce qu'on ECRIT, la-bas ce qu'on RECOIT.
import { afterEach, describe, expect, it } from 'vitest'
import { codesConnus, phraseDuRefus } from './raisons-refus'

afterEach(() => window.localStorage.clear())

// ⚠ ON PILOTE LA VRAIE BASCULE, PAS UN ESPION. `t()` appelle `langueActuelle`
// DANS son propre module : un `vi.spyOn(langue, 'langueActuelle')` remplace
// l'export mais pas l'appel interne, et le test restait en francais sans rien
// dire (constate le 10/09/2026). La langue se choisit par `localStorage`,
// exactement comme en partie.
const enFrancais = () => window.localStorage.setItem('marvel-langue', 'fr')
const enAnglais = () => window.localStorage.setItem('marvel-langue', 'en')

describe('la raison pour laquelle une carte est injouable', () => {
  it('met en français les motifs vraiment rencontrés en partie', () => {
    enFrancais()
    // Les SEPT motifs releves sur quatre decks joues en entier le 10/09/2026.
    // Aucun ne doit rester muet : c'est la consigne.
    for (const code of [
      'update legal targets',
      'no cost target',
      'player_is_alter_ego',
      'check_can_pay',
      'player_is_hero',
      'check_cannot_generate_self',
      'check_hero_form_only',
    ]) {
      expect(phraseDuRefus(code), code).toBeTypeOf('string')
    }
  })

  it('distingue les deux formes, sinon la phrase serait à contresens', () => {
    enFrancais()
    // Le code nomme la CONDITION qui a refuse : `player_is_hero` a refuse,
    // donc le joueur n'est pas heros, donc la carte veut la forme de heros.
    // Livre a l'envers le 10/09/2026, vu par l'utilisateur sur Lancer de
    // Bouclier (04002, action de heros) annonce « alter ego ».
    expect(phraseDuRefus('player_is_hero')).toBe('Jouable seulement sous forme de héros')
    expect(phraseDuRefus('player_is_alter_ego')).toBe("Jouable seulement sous forme d'alter ego")
  })

  it('dit le maximum par joueur, pas « aucune cible » (Réponse Immédiate, 11/10/2026)', () => {
    enFrancais()
    // Une 2e copie d'une carte « Max 1 per player » se refusait avec « Aucune
    // cible possible en ce moment » : le joueur cherchait une cible qui
    // n'existait pas. play.py nomme maintenant la condition.
    expect(phraseDuRefus('check_max_per_player')).toBe('Tu as déjà le maximum d’exemplaires de cette carte en jeu')
    enAnglais()
    expect(phraseDuRefus('check_max_per_player')).toBe('You already have the maximum number of copies of this card in play')
  })

  it('rend les chiffres du coût, pas une phrase vague', () => {
    enFrancais()
    // Le seul motif du moteur qui porte des nombres. Sans eux, « pas assez de
    // ressources » n'apprend rien : c'est l'ecart qui interesse le joueur.
    expect(phraseDuRefus('cout_insuffisant|3|RB')).toBe('Coût de 3, tu as physique, mental')
  })

  it('tolère un coût sans détail des ressources disponibles', () => {
    enFrancais()
    expect(phraseDuRefus('cout_insuffisant|2|')).toBe('Coût de 2')
  })

  it('ne rend rien pour un code inconnu, plutôt qu une phrase creuse', () => {
    enFrancais()
    // ⚠ `undefined` et pas « Injouable pour l'instant » : le silence doit
    // rester DETECTABLE par la gate. Une phrase de repli maquillerait le trou
    // en reponse et il ne serait jamais comble.
    expect(phraseDuRefus('un_motif_que_personne_na_prevu')).toBeUndefined()
    expect(phraseDuRefus('')).toBeUndefined()
    expect(phraseDuRefus('   ')).toBeUndefined()
  })

  it('bascule en anglais avec le reste du client', () => {
    enAnglais()
    expect(phraseDuRefus('player_is_hero')).toBe('Playable only in hero form')
    expect(phraseDuRefus('check_can_pay')).toBe('Not enough resources')
    expect(phraseDuRefus('cout_insuffisant|3|RB')).toBe('Cost of 3, you have physical, mental')
  })

  it('publie la liste de ses codes, pour que la gate puisse la lire', () => {
    // La gate cote moteur compare ce qu'elle voit passer a cette liste. Sans
    // elle, il faudrait la recopier a la main des deux cotes, et les deux
    // copies divergeraient.
    const codes = codesConnus()
    expect(codes).toContain('check_can_pay')
    expect(codes).toContain('cout_insuffisant')
    expect(new Set(codes).size).toBe(codes.length)
  })
})
