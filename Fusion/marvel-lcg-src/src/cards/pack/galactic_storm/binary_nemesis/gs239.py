from . import *

# Goin' Rogue — MANIGANCE ANNEXE nemesis (Binary Nemesis 2/5). Menace de depart 2 par joueur.
# Icone Hazard. 2 icones de boost.
# "Any chance you can give me a top-off?" —Rogue
# While Touched is attached to a friendly character, Rogue gets +1 SCH.
# While Touched is attached to an enemy character, Rogue gets +1 ATK.
#
# Cartes de reference :
#  - **`iron_fist/64009`** / **`gorr/hc014`** : bonus a valeur variable sur une
#    AUTRE carte = `GiveKeywordToInPlayWhenApplyThis(<cible>, scheme=1 /
#    attack=1, get_new_value=fn, change_on_event=...)`.
#  - **`sk067`** Punish the Defector (meme auteur) : manigance annexe nemesis a
#    icone Hazard (croix sur carte penchee, verifiee par decoupe contre sk067) et
#    menace « 2 [par joueur] » : `desc` seulement (`Hazard`, `StartingThreat`
#    "2*"), aucun script.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « FRIENDLY character » = identite ou allie (`Friend`) ; « ENEMY
#    character » = vilain ou sbire (`Enemy`). Un seul des deux bonus a la fois.
#  - « Rogue GETS +1 » : statistique, pas un mot-cle.
#  - La citation en italique n'est pas une regle.


def ValeurSi(type_de_carte: Any):
    def get_new_value(effect: 'Effect', face: 'CardFace') -> int:
        Unused(face)
        return 1 if PorteurEst(effect, type_de_carte) else 0
    return get_new_value


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CibleRogue(),
            scheme=1,
            get_new_value=ValeurSi(Friend),
            change_on_event=RecalculRogue(),
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CibleRogue(),
            attack=1,
            get_new_value=ValeurSi(Enemy),
            change_on_event=RecalculRogue(),
        ),
    ]
