from . import *

# * Silver Surfer (face HEROS) — AERIAL. COSMIC. ADVENTURER. PV 14, THW 1, ATK 3, DEF 2, main 5.
# Compunction — Forced Response: After Silver Surfer makes a basic attack, change your form.
#
# Cartes de reference :
#  - `tg001a` * Throg : meme fabrique `AfterUnitUseBasicPower(type, "This", op, powers=[...])`
#    (« After Throg uses a basic power »), ici restreinte a l'ATTAQUE.
#  - `lj008` / helpers de Lockjaw : `identite.ChangeToOtherIdentityForm(effect)` pour « change your form ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Forced Response » : obligatoire, pas de choix ; resout APRES l'attaque.
#  - « makes a BASIC attack » : seul le pouvoir de base ATK compte, pas l'attaque d'un evenement.
#  - « change YOUR form » : l'identite du joueur (ici la face heros qui devient Norrin Radd).
#  - Le texte « Forced Response » est imprime sur la face HEROS : rien a conditionner en alter-ego.


def GetAbilities() -> Sequence['Ability']:

    def compunction(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            ChangerDeForme(joueur, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            "This",
            compunction,
            powers=["ATK"],
        ).SetName("Compunction"),
    ]
