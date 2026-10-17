from . import *

# Flow of Battle — AMELIORATION 1 [mental], aspect Aggression (TMNT Aspects, Inkwire). SKILL.
# Prerequisite (MARTIAL ARTIST).
# Max 1 per player.
# Hero Response: After you attack and exactly defeat an enemy, discard this card → draw 3 cards.
#
# MOT-CLE (fiche CREEE avant le code) : docs/reference/mots-cles/prerequisite.md. ⚠ Lecture NON tranchee
#   (question Q-UA1, .planning/tmnt/aspects-aggression-questions.md) ; lecture codee en attendant : la carte ne
#   se JOUE que si votre identite a le trait MARTIAL ARTIST.
# CARTES DE REFERENCE
#  - `61035` Shakedown : « After you attack and exactly defeat a minion » = `AfterUnitDefeatedUnit(Response,
#    "You", Minion, ..., is_from_attack=True, has_excess_damage=False)`.
#  - `13017` Lie in Wait : « discard X → » en cout = `CostFunc.Discard("This")`.
#  - « Max 1 per player » : `desc.MaxPerUnit = 1` (amelioration posee sur sa propre identite, play.py).
# TEXTE CONTRE CODE
#  ⚠ « exactly defeat » = sans degat excedentaire (`has_excess_damage=False`).
#  ⚠ « an ENEMY » : vilain ou sbire (Enemy, pas Minion comme 61035).
#  ⚠ « Hero Response » : sous-type dedie (forme heros).


def IdentiteArtisteMartial(effect: 'Effect', message: 'Message2|None' = None) -> bool:
    Unused(message)
    joueur = effect.GetInitiator() or effect.this.GetControlByOrOwner()
    return joueur is not None and joueur.GetIdentity().HasTrait("MARTIAL ARTIST")


def GetAbilities() -> Sequence['Ability']:

    def flow(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        effect.GetInitiator().DrawUp(3, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(conditions=[IdentiteArtisteMartial]),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Enemy,
            flow,
            is_from_attack=True,
            has_excess_damage=False,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
