// Les restes anglais de la narration du moteur, relevés dans de vraies parties (Spider-Man, Dazzler, Blade, Captain Marvel) :
// demande de l'utilisateur du 16/11/2026, « tout ce qui est en anglais et qui n'est pas en français, pour tous les héros ».
import { describe, expect, it } from 'vitest'
import { narrationEnFrancais } from './narration-fr'

describe('narrationEnFrancais — les restes anglais du journal', () => {
  it('traduit les etapes de mise en place (avec ou sans tirets)', () => {
    expect(narrationEnFrancais('--- Set Up ---')).toBe('--- Mise en place ---')
    expect(narrationEnFrancais('--- Draw Cards ---')).toBe('--- Pioche des cartes ---')
    expect(narrationEnFrancais('Resolve Mulligans')).toBe('Résolution des mulligans')
    expect(narrationEnFrancais('--- Resolve Character Setup Abilities ---')).toBe('--- Capacités de mise en place des personnages ---')
    expect(narrationEnFrancais('Scenario Setup')).toBe('Mise en place du scénario')
    expect(narrationEnFrancais('--- Encounter Cards Phase ---')).toBe('--- Phase des cartes rencontre ---')
    expect(narrationEnFrancais('--- Select Hero and Villain ---')).toBe('--- Choix du héros et du méchant ---')
  })

  it('traduit les piles a porteur multi-mots, la position et le genre de « creee »', () => {
    expect(narrationEnFrancais('"Belle Rêveuse" déplacée(s) vers Concert en Direct\'s PlaceCardArea<3>')).toBe(
      '"Belle Rêveuse" déplacée(s) vers la zone à côté de Concert en Direct'
    )
    expect(narrationEnFrancais("Patins déplacée(s) vers Dazzler's PlayerDeck<9> top (règle)")).toBe('Patins déplacée(s) vers deck de Dazzler, au-dessus (règle)')
    expect(narrationEnFrancais('Angoisse déplacée(s) vers EncounterDeck<3> top (L’Effraction !)')).toBe('Angoisse déplacée(s) vers deck de rencontre, au-dessus (L’Effraction !)')
    expect(narrationEnFrancais('AsideDeck<4> créé')).toBe('pile mise de côté créée')
  })

  it('traduit les noms de phase', () => {
    expect(narrationEnFrancais('--- Phase : Player ---')).toBe('--- Phase : Joueurs ---')
    expect(narrationEnFrancais('--- Fin de phase : Villain ---')).toBe('--- Fin de phase : Méchant ---')
  })

  it('traduit les noms de piles, pour tous les heros', () => {
    expect(narrationEnFrancais("Dazzler's PlayerDeck<39> créé")).toBe('deck de Dazzler créé')
    expect(narrationEnFrancais("Captain Marvel's PlayerDeck<39> va être mélangé avec Captain Marvel's DiscardPile<0>")).toBe(
      'deck de Captain Marvel va être mélangé avec défausse de Captain Marvel'
    )
    expect(narrationEnFrancais('EncounterDeck<26> créé')).toBe('deck de rencontre créé')
    expect(narrationEnFrancais('Rhino défaussée vers EncounterDiscardPile<3> (Charge)')).toBe('Rhino défaussée vers défausse de rencontre (Charge)')
    expect(narrationEnFrancais("Spider-Man's PlayerDeck<12> épuisé")).toBe('deck de Spider-Man épuisé')
  })

  it('traduit les statuts et les mots-cles bruts', () => {
    expect(narrationEnFrancais('Rhino gagne Stunned (Épée)')).toBe('Rhino gagne Sonné (Épée)')
    expect(narrationEnFrancais('Rhino gagne Confused (X)')).toBe('Rhino gagne Désorienté (X)')
    expect(narrationEnFrancais('Rhino gagne Tough (X)')).toBe('Rhino gagne Tenace (X)')
    expect(narrationEnFrancais('Rhino gagne (piercing) de Épée')).toBe('Rhino gagne (Perçant) de Épée')
    expect(narrationEnFrancais('Rhino gagne (overkill) de Épée')).toBe('Rhino gagne (Déferlement) de Épée')
  })

  it('traduit les noms d’evenements du moteur', () => {
    expect(narrationEnFrancais('"WhenEffectWouldResolve" est remplacé par Cape')).toBe('« Un effet va se résoudre » est remplacé par Cape')
    expect(narrationEnFrancais('Dazzler sur l’événement "WhenPlayerLikeInTurn"')).toBe('Dazzler sur l’événement « Considéré comme son tour »')
    expect(narrationEnFrancais('"WhenSchemeWouldPlaceThreat" est remplacé par X')).toBe('« De la menace va être posée » est remplacé par X')
  })

  it('traduit le type d’effet cite entre parentheses', () => {
    expect(narrationEnFrancais('L’Effraction ! s’apprête à recevoir 1⚠ (Main Scheme Phase Place Threat)')).toBe(
      'L’Effraction ! s’apprête à recevoir 1⚠ (étape de la manigance principale)'
    )
    expect(narrationEnFrancais('Rhino va comploter (+1) (Game Rule)')).toBe('Rhino va comploter (+1) (règle du jeu)')
    expect(narrationEnFrancais('Dazzler entre en jeu (rule)')).toBe('Dazzler entre en jeu (règle du jeu)')
    expect(narrationEnFrancais('X s’apprête à recevoir 2⚠ ((^!2) Bomb Scare (When Revealed) [2] WhenCardRevealed)')).toBe(
      'X s’apprête à recevoir 2⚠ (Bomb Scare, une fois révélée)'
    )
  })

  it('laisse intact ce qui est deja en francais ou qui n’est pas un reste', () => {
    for (const ligne of ['Dazzler pioche 6 carte(s) (L’Effraction !)', 'Rhino va attaquer Dazzler (+0)', '--- Tour de Dazzler (1) ---', 'Rhino va attaquer Dazzler (+2), avec (Perçant)']) {
      expect(narrationEnFrancais(ligne)).toBe(ligne)
    }
  })
})
