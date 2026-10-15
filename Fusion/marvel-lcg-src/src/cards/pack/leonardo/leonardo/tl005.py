from . import *

# Stoicism — evenement signature, x2. SKILL. Cout 2, [mental].
# Hero Action: Ready Leonardo. If you paid for this card with a [energy]
#   resource, ready a [[KATANA]] upgrade you control.
#
# Cartes de reference :
#  - `ls005` Lady Sif (« ready your hero ») : `joueur.GetHero()` APRES un
#    controle `IsHero()` — `Player.GetHero()` LEVE un assert hors forme de
#    heros, et le moteur avale l'exception ;
#  - `16031` Reload : `.SetPlay().SetLabel()` pour une Hero Action sans libelle ;
#  - `tl004` (meme pack) pour le second redressement conditionne au paiement.
#
# Mots-pieges :
#  - « Ready LEONARDO » : le heros (forme de heros), pas l'identite quelle
#    qu'elle soit ;
#  - « paid with a [energy] resource » : HasColor("Y") ;
#  - AUCUN libelle imprime (ni attack ni thwart ni defense).


def GetAbilities() -> Sequence['Ability']:

    def stoicism(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        if joueur.IsHero():
            Faces.ReadyAll([joueur.GetHero()], effect)

        if effect.GetPaidResources().HasColor("Y"):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready a KATANA upgrade you control",
                    lambda cibles: Faces.ReadyAll(
                        [f for f in cibles if f is not None], effect),
                ).SetTarget(Upgrade, trait="KATANA",
                            from_where=["YouControlCards"], canbe_ready=True),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            stoicism,
        ).SetPlay().SetLabel(),
    ]
