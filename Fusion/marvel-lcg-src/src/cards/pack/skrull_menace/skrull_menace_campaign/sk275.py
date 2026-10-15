from . import *

# * Skrull Military Training — COMPLOT ANNEXE DE JOUEUR (Basic / Campaign, n° 275). Cout 0, menace 3.
# Victory 0.
# Threat cannot be removed from this scheme unless it is being thwarted by a SKRULL ally.
# While this card is in the victory display, its owner's hero gets +1 THW, +1 ATK, and +1 DEF.
#
# Cartes de reference :
#  - **`next_evol/cable/40006`** Technovirus Purge et **`hd010`** (`BonusDepuisLaZoneDeVictoire`) : « While X
#    is in the victory display, ... gets +1 » = `GiveKeywordToInPlayWhenApplyThis(<cible>,
#    works_in_the_victory_display=True, ...)` (RECETTES §3bis : seule voie pour un bonus continu depuis la
#    vitrine ; la cible reste EN JEU, la vitrine est relue comme condition).
#  - **`40006`** / **`bc004`** : « threat cannot be removed ... unless » = `ThreatCannotBeRemovedFromWhile("This",
#    conditions=[...])` : `message.by_face` est le personnage qui retire, `message.would_thw_message` n'existe
#    que pour une MENEE (contre).
#
# ⚠ Mots-pieges :
#  - « unless it is being THWARTED by a SKRULL ALLY » : seul un CONTRE (menee) d'un ALLIE portant SKRULL retire
#    de la menace ; ni le heros, ni un evenement, ni un soutien (Cadre K), ni un allie non SKRULL ;
#  - « ITS OWNER'S hero » : le heros du PROPRIETAIRE de la carte (pas un autre joueur, pas l'alter ego) ;
#    la valeur est calculee par `get_new_value` sur le heros en jeu ;
#  - « WHILE in the victory display » : le bonus ne vaut qu'une fois le complot vaincu (Victory 0 le place en
#    vitrine) ; +1 THW, +1 ATK ET +1 DEF.


def GetAbilities() -> Sequence['Ability']:

    def pas_un_contre_d_un_allie_skrull(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        if message.would_thw_message is None:
            return True
        retire_par = message.by_face
        return not (Ally.IsType(retire_par) and retire_par.HasTrait("SKRULL"))

    def heros_du_proprietaire(effect: 'Effect', face: 'CardFace') -> int:
        return 1 if face.GetControlBy() == effect.this.GetOwner() else 0

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            conditions=[pas_un_contre_d_un_allie_skrull],
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            works_in_the_victory_display=True,
            thwart=1,
            attack=1,
            defense=1,
            get_new_value=heros_du_proprietaire,
        ),
    ]
