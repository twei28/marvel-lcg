from . import *

# Herald of Galactus — COMPLOT ANNEXE NEMESIS (2/5). Menace de depart 1,
# icone d'acceleration (PAS un boost -- confirme par l'utilisateur le
# 05/11/2026).
#
# Texte imprime :
#  « Threat cannot be removed from this scheme while Terrax is in play. »
#  « Forced Response: After Terrax attacks, add threat here equal to the
#    amount of damage dealt by that attack. Then, if there is 5 or more
#    threat here, remove a random PLANET from the game. »
#
# CARTES DE REFERENCE
#  - `sk033` (skrull_menace) : `AbilityFactory.ThreatCannotBeRemovedFromWhile
#    ("This", while_face_is_in_play=CardFinder(name="Terrax"))` -- modele
#    EXACT pour « threat cannot be removed ... while X is in play ».
#  - `message.total_dealt_damage` (`Message.AfterUnitAttackEnd`,
#    sender_damage.py) : « equal to the amount of damage dealt by that
#    attack ».
#  - `this.PlaceThreatOnSchemes([this], n, effect)` (modele `sm014`) pour
#    « add threat here ».
#  - `Rand.RandomChoice` (operate/rand.py) + `Faces.RemoveAllFromGame` pour
#    « remove a random PLANET from the game » : toutes les cartes EN JEU
#    portant le trait PLANET, tous joueurs confondus (le texte ne dit pas
#    « a planet of yours »).
#
# TEXTE CONTRE CODE
#  « After TERRAX attacks » : Terrax precisement, pas le mechant courant
#    (si Terrax n'est pas le mechant actif, ses propres attaques comptent
#    quand meme -- `AfterUnitAttackEnd` filtre sur Terrax via `name`).
#  « if there is 5 OR MORE threat here » : seuil, pas un palier exact.
#  « a random PLANET » : UNE seule, au hasard parmi toutes celles en jeu a
#    cet instant (y compris Herald of Galactus lui-meme si jamais il
#    portait ce trait -- il ne le porte pas, aucun risque de s'auto-retirer).


def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(SchemeSide2)
        this.PlaceThreatOnSchemes([this], message.total_dealt_damage, effect)

        if this.threat >= 5:
            planetes = [f for f in Worlds.GetOnFieldCards(effect) if f.HasTrait("PLANET")]
            if planetes:
                cible = Rand.RandomChoice(planetes, effect)
                Faces.RemoveAllFromGame([cible], effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            while_face_is_in_play=CardFinder(name="Terrax"),
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            CardFinder(name="Terrax"),
            apres_attaque,
        ),
    ]
