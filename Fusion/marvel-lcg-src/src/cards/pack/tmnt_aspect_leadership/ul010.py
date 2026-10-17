from . import *

# Heroes in a Half Shell — SOUTIEN Leadership (TMNT Customs, Inkwire), cout 3, [mental]. TEAM.
# Play under any player's control. Max 1 [[TEAM]] card per player.
# Each of your [[TURTLE]] allies get +1 hit point. If each of your characters has the [[TURTLE]] trait,
#   each of your [[TURTLE]] allies cost 1 fewer resource to play.
#
# MODIFIEE (reskin de `36018` Uncanny X-Men) : [[X-MEN]] -> [[TURTLE]] aux trois endroits. Script propre
# copie de 36018, seul le trait change.
#  « Max 1 TEAM card per player » : regle generique du moteur (`limit_monitor/team_limit.py`, trait TEAM).
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR TURTLE allies » : ceux du joueur qui CONTROLE le soutien (« Play under any player's control »).
#  ⚠ « If EACH of your characters » : identite comprise ; la condition se relit quand un trait change.
#  ⚠ « cost 1 fewer » : reduction a la mise en jeu, pas une generation de ressource.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisSupportCard(
            under_any_players_control=True
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder2("TURTLE", Ally),
            control_by="You",
            health=1,
            change_on_event=OnEvent.Trait("YouControlCharacter")
        ),
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder2("TURTLE", Ally),
            1,
            "You",
            conditions=[
                lambda effect, message:
                    Faces.IsAll(effect.GetInitiator().GetControlCharacters(), CardFinder2("TURTLE")),
            ]
        )
    ]
