from . import *

# * ED-209 : SBIRE nemesis (1/5), ELITE. ROBOT. PV 8, MNG 0, ATQ 4, boost 2. `desc.Nemesis` = « RoboCop ».
# When Revealed: ED-209 engages the RoboCop player.
# Forced Response: After ED-209 enters play, find the Stairs attachment and attach it to ED-209.
# (RoboCop's nemesis minion.)
#
# CARTES DE REFERENCE
#  - `dd015` Mister Fantastic : « engages the X player » (`WhenThisRevealed(None, op)` + `Minion.EngagePlayer(joueur, effect)` sur le joueur dont l'identite porte le nom).
#  - `nt013` Terrax the Tamer / `nt016` : « find ... attachment and attach it » (reveler l'attachement, qui s'attache seul) puis `AttachTo2(cible, effect)` pour forcer l'hote.
#
# TEXTE CONTRE CODE
#  « engages THE ROBOCOP PLAYER » -> le joueur dont l'identite est RoboCop / Alex Murphy, pas celui qui a revele. « After ED-209 ENTERS PLAY » -> a chaque entree en jeu (revele,
#    mis en jeu par Corporate Demonstration ou par Shadow of the Past), Reponse forcee. « FIND the Stairs attachment » -> deck rencontre, defausse ET mise de cote ;
#    « attach it to ED-209 » -> a CE sbire meme, pas au sbire aux PV les plus hauts. Rien si Stairs n'est pas trouvee. Nemesis : `desc.Nemesis`.
#  Chiffres : PV 8, MNG 0, ATQ 4, boost 2.


def GetAbilities() -> Sequence['Ability']:

    def engage_robocop(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        joueur = JoueurRoboCop(effect)
        if joueur is not None:
            this.EngagePlayer(joueur, effect)

    def trouver_stairs(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        joueur = JoueurRoboCop(effect) or Worlds.GetFirstPlayer(effect)
        stairs = Trouver(effect, joueur, NOM_STAIRS, Attachment)
        if stairs is None:
            return
        stairs.Reveal(joueur, effect)
        # `Stairs` s'attache seule au sbire aux PV les plus hauts ; le texte imprime veut ED-209.
        if stairs.card.IsOnField() and stairs.bind_face is not this:
            stairs.CastTo(Attachment).AttachTo2(this, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            engage_robocop,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            trouver_stairs,
        ),
    ]
