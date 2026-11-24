from . import *

# Touched — ATTACHEMENT nemesis (Binary Nemesis 3/5). CONDITION. Aucune icone de boost.
# If Rogue is in play, attach to a character other than Rogue. Otherwise, this
#   card gains surge.
# While Touched is attached to a:
#  • Minion, Rogue gains retaliate 2.
#  • Villain, reduce the damage Rogue takes from each attack by 2.
#  • Ally, Rogue gets +2 ATK.
#  • Identity, Rogue gains villainous.
#
# Cartes de reference :
#  - **`tt/55062`** Love Triangle : « Attach to ... Otherwise, this card gains
#    surge » = `AttachToFaceWhenPutIntoPlay(<cible>, if_cannot_gain_surge=True)`.
#  - **`mts/21083`** Restrained : attachement de rencontre pose sur un
#    personnage AMICAL (meme fabrique, cible `Friend`).
#  - **`gmw/16098`** Wide Stance / **`qsv/14027`** : « reduce the damage X takes
#    from each attack by N » = `ReduceCharacterTakeDamageBy(X, N,
#    from_each_attack=True)`.
#  - **`iron_fist/64009`** : mot-cle a valeur variable sur une AUTRE carte =
#    `GiveKeywordToInPlayWhenApplyThis(<cible>, retaliate=1, get_new_value=fn,
#    change_on_event=...)` ; idem pour `attack` et `villainous` (fiche
#    `mots-cles/villainous.md`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « IF Rogue is in play ... OTHERWISE surge » : sans Rogue en jeu, aucune
#    cible n'est legale et la carte gagne Renfort (la condition est portee par
#    le filtre de cible, sinon la branche « otherwise » serait morte).
#  - « a CHARACTER other than Rogue » : identite, allie, vilain, sbire.
#  - Les quatre paliers dependent du TYPE du porteur, un seul a la fois :
#    sbire -> riposte 2 ; vilain -> -2 degats par attaque ; allie -> +2 ATQ ;
#    identite (heros ou alter ego) -> Vilenie.
#  - « reduce the damage ROGUE takes from EACH ATTACK » : attaques seulement
#    (pas un degat de carte non-attaque).
#  - « Rogue » = le sbire nemesis (Minion « Rogue »), pas un heros officiel
#    Rogue que jouerait un joueur (voir binary_nemesis/__init__.py).


def ValeurSi(type_de_carte: Any, valeur: int):
    def get_new_value(effect: 'Effect', face: 'CardFace') -> int:
        Unused(face)
        return valeur if PorteurEst(effect, type_de_carte) else 0
    return get_new_value


def GetAbilities() -> Sequence['Ability']:

    def autre_que_rogue(effect: 'Effect', face: 'CardFace') -> bool:
        return bool(RoguesEnJeu(effect)) and Unit2.IsType(face) and not EstRogue(face)

    def porte_par_un_vilain(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(message)
        return PorteurEst(effect, Villain)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Unit2, check_effect_fn=autre_que_rogue),
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CibleRogue(),
            retaliate=1,
            get_new_value=ValeurSi(Minion, 2),
            change_on_event=RecalculRogue(),
        ),
        AbilityFactory.ReduceCharacterTakeDamageBy(
            CibleRogue(),
            2,
            from_each_attack=True,
            conditions=[porte_par_un_vilain],
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CibleRogue(),
            attack=1,
            get_new_value=ValeurSi(Ally, 2),
            change_on_event=RecalculRogue(),
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CibleRogue(),
            villainous=1,
            get_new_value=ValeurSi(Identity, 1),
            change_on_event=RecalculRogue(),
        ),
    ]
