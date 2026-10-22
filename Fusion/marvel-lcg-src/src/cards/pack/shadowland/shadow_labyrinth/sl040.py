from . import *

# Whisper in the Dark — ATTACHEMENT. TRAP!
# Treat attached villain as an ELITE minion with 6 printed hit points. It gains : "Guard. Villainous. When Defeated : Set this minion aside."
# When Revealed : If Shifting Corridors is in play, put the set-aside chosen villain into play engaged with you, side A faceup, with this card attached ; otherwise, set this
#   card aside and the villain schemes.
#
# Cartes de reference : punisher_mcdc_2026/capo_of_the_past/pu139 (« Treat attached character as an ELITE minion » : sosie « Minion » cree depuis la face du vilain,
# `GainTraits`, `GainKeyword`, `GainVillainous`, `AttachTo2`), punisher_mcdc_2026/punishment/pu092 (`WhenUnitBeDefeated(WhenDefeated, "AttachedCharacter", ...)`),
# skrull_menace/standard_skrull/sk259 (`DoSchemes(joueur, effect)`).
# ⚠ Mots-pieges : « the SET-ASIDE chosen villain » : le vilain Dark Protege tire a la mise en place (la carte reste de cote, c'est un SOSIE sbire qui entre en jeu) ; « engaged
#  with YOU » : le joueur qui revele ; « side A faceup » : toujours la face A, meme en expert ; « 6 PRINTED hit points » : 6 fixes, pas par joueur ; « Guard. Villainous. »
#  donnes au sbire tant que Whisper y est attache ; « When Defeated : set this minion aside » : le sosie quitte la partie (la carte reste de cote) et Whisper est defausse ;
#  « otherwise, set this card aside » : de cote (pas defaussee) ; « the villain schemes » : contre le joueur qui revele.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        carte = VilainChoisi(effect)
        if Corridors(effect) is not None and carte is not None:
            sbire = CreerLeSbireDuVilain(effect, str(carte.paper.card_id)[:5] + "a", 6)
            sbire.PutIntoPlay(joueur, effect)
            sbire.GainTraits(1, [*sbire.sl_traits, "ELITE"], effect)
            sbire.GainKeyword(1, "Guard", effect)
            sbire.GainVillainous(1, effect)
            this.AttachTo2(sbire, effect)
        else:
            Faces.MoveAllTo([this], Worlds.AsideDeck(effect), effect)
            vilain = Worlds.FindVillain(effect)
            if vilain is not None:
                vilain.DoSchemes(joueur, effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        # « Set this minion aside » : le sosie quitte la table ; la vraie carte du vilain est restee de cote.
        Faces.RemoveAllFromGame([message.trigger], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "AttachedCharacter", vaincu),
    ]
