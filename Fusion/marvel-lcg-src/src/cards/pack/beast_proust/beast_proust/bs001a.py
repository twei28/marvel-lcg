from . import *

# * Beast (Proust) (face heros) : AVENGER. X-MEN. THW 1 / ATQ 1 / DEF 2, main 4, PV 14.
# Ingenious Repurposing — Action: Tuck a TECH upgrade you control under Beast's Lab -> ready your hero and choose THW, ATK or DEF. Until the end of the round, your hero gets +X to the chosen stat,
# where X is the printed cost of this upgrade. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `td012` Donatello's Shell / `gs099q` Maelstrom : `TuckCardUnderHere` d'une carte DEJA EN JEU (amelioration) ; ici le cout est `CostFunc.Custom(Select.From("YouControlCards", finder=..), fn)` car l'hote du
#    glissement est le Lab, pas la carte qui agit (`CostFunc.TuckCardHere` glisse sous `effect.this`).
#  - `12016` Moxie : `hero.GainUntilRoundEnd(effect, attack=.., thwart=.., defense=..)` pour « until the end of the round ».
#  - `14001a` Quicksilver : `Faces.ReadyAll`, `.LimitOncePerPhase()`.
#
# TEXTE CONTRE CODE
#  « Tuck a TECH upgrade YOU CONTROL » : COUT (avant la fleche) ; l'amelioration quitte le jeu et va sous le Lab, visible. « READY your hero » : la face heros se redresse (meme si elle l'est deja). « CHOOSE THW, ATK or DEF » :
#    un seul des trois. « +X where X is the PRINTED cost of THIS upgrade » : `printed_cost.val` de l'amelioration glissee, pas son cout paye. « Until the end of the ROUND ». « Limit once per PHASE ».
#  Chiffres : PV 14, main 4, ATQ 1, CTR 1, DEF 2.


def GetAbilities() -> Sequence['Ability']:

    def lab_et_amelioration_tech(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and LabDe(joueur) is not None and bool(AmeliorationsTech(joueur))

    def glisser_en_cout(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None or not cibles:
            return False
        effect.bs_x = CoutImprime(cibles[0])
        return Glisser(joueur, list(cibles), effect)

    def reexploitation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        joueur = effect.GetInitiator()
        x = getattr(effect, "bs_x", 0)
        Faces.ReadyAll([this], effect)
        if x <= 0:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"+{x} THW until the end of the round",
                lambda cibles:
                    this.GainUntilRoundEnd(effect, thwart=x),
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                f"+{x} ATK until the end of the round",
                lambda cibles:
                    this.GainUntilRoundEnd(effect, attack=x),
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                f"+{x} DEF until the end of the round",
                lambda cibles:
                    this.GainUntilRoundEnd(effect, defense=x),
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            reexploitation,
            conditions=[lab_et_amelioration_tech],
        ).SetName("Ingenious Repurposing")
        .SetCostFunc(CostFunc.Custom(
            Select.From("YouControlCards", finder=CardFinder(card_type=Upgrade, trait="TECH")),
            glisser_en_cout,
        )).LimitOncePerPhase(),
    ]
