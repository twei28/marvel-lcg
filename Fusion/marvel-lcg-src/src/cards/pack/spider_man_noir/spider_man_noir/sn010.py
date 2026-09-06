from . import *

# Organic Webbing — AMELIORATION, cout 1, [energy]. SUPERPOWER.
# Hero Action: Exhaust Organic Webbing and discard a card tucked under
#   Spider-Man Noir -> ready Spider-Man Noir. He gains the [[AERIAL]] trait
#   until the end of the round.
#
# ⚠ HOMONYMES : « Organic Webbing » existe deja DEUX fois au depot, `30011`
# (pack spiderham) et `52009` (pack silk), toutes deux des ameliorations.
# Celle-ci est la troisieme. Le texte francais s'ecrit sur le `card_id`.
#
# CARTES DE REFERENCE
#  - `12016` Moxie / `tt001a` : `GainUntilRoundEnd`, l'idiome du bonus de
#    round. Il accepte `trait=` (face_action.py:430).
#  - `31009` / `an001a` : `Faces.ReadyAll`.
#
# TEXTE CONTRE CODE
#  ⚠ DEUX COUTS devant la fleche : incliner ET defausser une carte glissee.
#  « ready SPIDER-MAN NOIR » -> la face HEROS. Le filtre est le TYPE, jamais
#    le nom : deux ALLIES du depot s'appellent « Spider-Man Noir ».
#  « HE gains the AERIAL trait » -> le heros, pas l'identite : en forme civile
#    la capacite n'est de toute facon pas disponible (« Hero Action »).
#  « UNTIL THE END OF THE ROUND » -> `GainUntilRoundEnd`, pas un bonus
#    permanent et pas « for this use » : le trait survit a plusieurs usages
#    dans le meme round. Piege `tt001a`, ou la difference etait imprimee.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_une_carte_glissee(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUneCarteGlissee(effect)

    def toile_organique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        heros = HerosDuJoueur(effect)
        if heros is None:
            return
        Faces.ReadyAll([heros], effect)
        heros.GainUntilRoundEnd(effect, trait=["AERIAL"])

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            toile_organique,
            conditions=[PileNonVide],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_une_carte_glissee)),
    ]
