from . import *

# Dard'van Priest (185) — SBIRE. MYSTIC. SKRULL. MNG 2, ATQ ★, 3 PV, 2 icones Y.
# When Revealed: Dard'van Priest schemes.
# ★ Forced Interrupt: When Dard'van Priest would attack, instead choose a card in play with a
#   "When Revealed" ability and resolve that ability.
#
# Cartes de reference :
#  - « X schemes » en When Revealed : **`skrull_menace/paibok/sk158`** (`DoSchemes(joueur, effect)`) ;
#  - « would attack, ... instead » : **`jessica_jones/jj019`** Purple Man (`WhenUnitWouldAttack(ForcedInterrupt,
#    "This", op)` + `message.SetBeInstead(effect)`) ;
#  - « resolve that card's When Revealed » : **`sk046`** Mole / **`27083`** (`Faces.ResolveAbility(...)`), via le
#    helper `ChoisirEtResoudreRevelation` du set.
#
# ⚠ Mots-pieges : « INSTEAD » (l'attaque n'a PAS lieu : ni degats ni cartes de boost, la capacite la remplace) ;
# « choose a card IN PLAY » (le Priest peut se choisir lui-meme : son propre « When Revealed » le fait
# comploter) ; « resolve THAT ability » (l'effet seul, pas le reste de la revelation) ; le joueur qui choisit est
# celui engage avec le Priest (le texte ne le precise pas : defs/pantheon_questions.md) ; ATQ ★ : `desc.ATK = 0*`.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        this.DoSchemes(message.GetToPlayer(), effect)

    def au_lieu_d_attaquer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        joueur = this.GetEngagedPlayer() or Worlds.GetFirstPlayer(effect)
        ChoisirEtResoudreRevelation(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", au_lieu_d_attaquer),
    ]
