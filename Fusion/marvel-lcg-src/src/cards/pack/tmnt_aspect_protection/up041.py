from . import *

# * Usagi Yojimbo — ALLIE 3 [energy], aspect Protection (TMNT Aspects, Inkwire). RABBIT. RONIN.
# THW 1 (1), ATK 2 (1), PV 3.
# Retaliate 2. Toughness.
# Usagi Yojimbo does not exhaust to defend.
#
# NOUVELLE. MOTS-CLES (fiches lues AVANT le code) : Retaliate (retaliate.md), Toughness (toughness.md) —
# tous deux lus dans `desc` (`Retaliate: "2"`, `Toughness: "1"`), AUCUN code.
#
# CARTES DE REFERENCE
#  - `53011` Draw Their Fire (Falcon) : « Falcon does not exhaust to defend » = ajouter la carte a
#    `CostFunc.Exhaust.not_need_to_exhaust` du cout de l'effet `DEF` (pouvoir de base de defense,
#    `friend.py` `ThisCanDefense`, cout `CostFunc.Exhaust("This")`). Ici, pas de limite de phase : c'est
#    permanent tant qu'Usagi est en jeu (pose a l'entree en jeu, comme `ThisEnterPlayWithCounters`, en
#    `AbilityType.NonKeyword`).
#  - Rules Reference v1.8, « Defending » : « A card ability that allows an ally to be declared as a
#    defender without exhausting can be used on an exhausted ally. » Le moteur fait exactement ca :
#    `not_need_to_exhaust` rend le cout payable meme incline (meme comportement que 53011).
#
# TEXTE CONTRE CODE
#  ⚠ « does not exhaust TO DEFEND » : seulement le cout de la defense ; ses attaques/contres l'inclinent.
#  ⚠ Retaliate 2 (pas 1) ; Toughness = 1 carte Tenace a l'entree.


def GetAbilities() -> Sequence['Ability']:

    def ne_s_incline_pas_pour_defendre(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        for defense in this.effect.Find(func_name="DEF"):
            for cout in defense.cost_func.GetAll():
                if isinstance(cout, CostFunc.Exhaust) and this not in cout.not_need_to_exhaust:
                    cout.not_need_to_exhaust.append(this)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.NonKeyword,
            "This",
            ne_s_incline_pas_pour_defendre,
        ),
    ]
