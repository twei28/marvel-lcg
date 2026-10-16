from . import *

# Cross Block — EVENEMENT, cout 2, [energy]. DEFENSE. x2.
# Hero Interrupt (defense): When you defend against an attack, you get +3 DEF
#   for that attack. Then, ready Casey Jones and give him a tough status card.
#
# CARTES DE REFERENCE
#  - `14014` Never Back Down : MEME montage (`WhenUnitDefendAgainstAttack(
#    HeroInterrupt, "You", op, is_basic_defense=True).SetPlay().SetLabel(
#    'defense')` + `message.GainDEFForThisAttack(N, effect)`).
#  - `Faces.ReadyAll` / `Faces.GiveStatus(..., "Tough", ...)` : recette §2.
#
# TEXTE CONTRE CODE
#  ⚠ « +3 DEF FOR THAT ATTACK » : `GainDEFForThisAttack(3)` (pour cette attaque
#    seulement, pas jusqu'a la fin du round).
#  ⚠ « THEN, ready Casey Jones AND give him a tough status card » : deux effets
#    dans cet ordre, sur l'IDENTITE (le heros qui defend est incline : le
#    redresser puis le doter de Tough). Le Tough posé PROTEGE de cette meme
#    attaque (les degats l'epuisent) : c'est le texte, pas un bug.
#  ⚠ « Casey Jones » = l'identite du joueur (jamais une recherche par nom : un
#    allie homonyme existe, tr002).
#  ⚠ « When YOU defend » : Casey lui-meme (defense de base), pas un allie.


def GetAbilities() -> Sequence['Ability']:

    def cross_block(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.GainDEFForThisAttack(3, effect)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return
        Faces.ReadyAll([identite], effect)
        Faces.GiveStatus([identite], "Tough", effect)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "You",
            cross_block,
            is_basic_defense=True,
        ).SetPlay().SetLabel('defense'),
    ]
