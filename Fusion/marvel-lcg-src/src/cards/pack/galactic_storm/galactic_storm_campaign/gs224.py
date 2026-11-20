from . import *

# * Rick Jones — ALLIE de campagne (Basic / Campaign, n° 224). Cout 0. THW 1 / ATK 2**, 2 PV. CIVILIAN.
# Honorary.
# Forced Interrupt: When the villain attacks you, it attacks Rick Jones instead.
#
# Carte de reference :
#  - **`hood/crossfires_crew/24026`** Crossfire : `AbilityFactory.WhenUnitWouldAttack(ForcedInterrupt,
#    "This", ...)` + `message.ReplaceTarget(unit)` pour rediriger une attaque qui allait toucher un
#    joueur/personnage vers une AUTRE cible — meme methode, ici la cible de remplacement est toujours
#    Rick Jones lui-meme (`effect.this`), pas un choix.
#
# ⚠ Mots-pieges :
#  - « the VILLAIN attacks YOU » : attaquant = Villain, cible = le controleur de Rick Jones
#    (`against_player="You"`), pas n'importe quel attaquant ni n'importe quelle victime ;
#  - « it attacks Rick Jones INSTEAD » : remplacement total de la cible (`ReplaceTarget`), pas un ajout
#    (`AlsoResolveThisAttackTo` aurait fait attaquer les deux) ;
#  - « Honorary » : base automatique (desc.Class contient deja la portee campagne, aucun mot-cle a coder).


def GetAbilities() -> Sequence['Ability']:

    def rick_jones(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        message.ReplaceTarget(this)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            Villain,
            rick_jones,
            against_player="You",
        ),
    ]
