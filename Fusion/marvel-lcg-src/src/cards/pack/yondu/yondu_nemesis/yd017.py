from . import *

# Hard to Kill — traitrise NEMESIS (4/5). Boost 2 + [star].
# When Revealed: If Sav'rkk is in play, he heals 2 damage. Otherwise, summon
#   Sav'rkk and reveal him.
# [star] Boost: The villain heals 2 damage.
#
# Cartes de reference :
#  - `06030` Trickster / `as025` / `nt015` pour `WhenThisRevealed(None, op)` et
#    `message.GetToPlayer()`.
#  - `ConvoquerRencontre` (helper du set) pour le mot-cle MAISON `summon`.
#  - `an013` Hel-Wolf / `ho015` / `as025` pour `WhenCardBecomeBoost("This", op)`.
#  - `42018` pour `HealthUnits`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Otherwise** » : les deux moities s'EXCLUENT. Sav'rkk present, il se
#    soigne ; absent, il ARRIVE. Coder les deux a la suite le ferait entrer en
#    jeu ET se soigner.
#  - « summon Sav'rkk **and reveal him** » : directement en jeu, pas en main.
#    C'est la difference exacte avec les trois cartes du heros, qui ecrivent
#    « and add it to your hand ».
#  - « [star] **Boost**: The **VILLAIN** heals 2 » : le vilain, pas Sav'rkk.
#    Les deux moities de la carte ne soignent PAS la meme cible, et c'est
#    imprime ainsi.
#  - `[star]` sans « In expert mode » : capacite TOUJOURS active (convention
#    moteur, cf. 04125).
#  - ⚠ La carte est une machine a rendre Sav'rkk penible : PV 4, mais il
#    revient et se soigne. Et tant qu'il est en jeu, « Upgrades cannot be
#    removed from Sav'rkk » cloue la Yaka Arrow sur lui.


def GetAbilities() -> Sequence['Ability']:

    def hard_to_kill(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        savrkk = Worlds.FindCardOnField(effect, name="Sav'rkk", card_type=Minion)
        if savrkk is not None:
            this.HealthUnits([savrkk], 2, effect)
            return

        # « Otherwise, summon Sav'rkk and reveal him. »
        trouve = ConvoquerRencontre(effect, "Sav'rkk", Minion)
        if trouve is not None:
            trouve.Reveal(message.GetToPlayer(), effect)

    def hard_to_kill_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)

        vilains = Worlds.GetVillains(effect)
        if vilains:
            this.HealthUnits([vilains[0]], 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hard_to_kill,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            hard_to_kill_boost,
        ),
    ]
