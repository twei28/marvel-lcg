from . import *

# * Spider-Bot — allie signature, x1. ROBOT. Cout 4, PV 3, CTR 1*, ATQ 3**,
# ressource [energy]. Toughness 1.
# Toughness.
# Action: Discard Spider-Bot -> flip your Spider Armor upgrade to its
#   [[OPERATIONAL]] side.
#
# Cartes de reference :
#  - `08018` Spycraft et `ls003` pour `CostFunc.Discard("This")` : la carte
#    se defausse elle-meme comme COUT.
#  - **`32030b`** * Kitty Pride (« Action: Flip your mass form upgrade ») et
#    `40122a` * Juggernaut's Helmet pour le retournement declenche par une
#    Action.
#  - `face.FlipTo(effect, trait=...)` (card_face.py:1068) pour « to its
#    [[OPERATIONAL]] side » : un retournement VERS une face nommee, pas un
#    `Flip()` aveugle.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Toughness.** » : base automatique lue dans `desc.Toughness`, AUCUN
#    script (fiche mots-cles/toughness.md). Un module qui la recoderait
#    donnerait DEUX cartes robuste au lieu d'une.
#  - « flip your Spider Armor upgrade **to its [[OPERATIONAL]] side** » : PAS
#    « flip it ». Une armure deja OPERATIONAL ne doit rien faire — d'ou le
#    test de trait avant le retournement. Sans lui, defausser Spider-Bot
#    detruirait une armure intacte.
#  - « **your** Spider Armor » : celle du joueur qui defausse, pas une autre
#    (helper `ArmureDuJoueur`, qui ne balaie que ses propres personnages).
#  - « **Action** » nu : pas « Hero Action », pas « Alter-Ego Action ». C'est
#    ce qui rend cette carte precieuse : elle repare l'armure SANS passer en
#    forme civile, contrairement a as002b qui exige 3 ressources en alter-ego.
#  - ⚠ ECART ASSUME : le retournement declenche le Forced Response de as002a
#    (« After you flip to this side, place 3 metal counters here »), donc
#    Spider-Bot rend une armure PLEINE. C'est bien ce qu'impose la chaine des
#    deux textes imprimes, pas une generosite ajoutee ici.


def GetAbilities() -> Sequence['Ability']:

    def spider_bot(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        armure = ArmureDuJoueur(effect.GetInitiator())
        if armure is None or armure.HasTrait("OPERATIONAL"):
            return
        armure.FlipTo(effect, trait="OPERATIONAL")

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            spider_bot,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
