from . import *

# * Terrax the Tamer — sbire NEMESIS de Night Thrasher. COSMIC. MUTANT.
# PV 7, MAN 1, ATQ 2, Boost 2. `desc.Nemesis` = « Night Thrasher ».
# Forced Response: After Terrax the Tamer activates, discard the top 8 cards of
#   the encounter deck. If the Cosmic Ax attachment was discarded this way,
#   reveal it.
#
# Cartes de reference :
#  - **`AfterEnemyActivatesAgainstYou`** (activate.py:68) : « After <sbire>
#    ACTIVATES » couvre l'attaque ET la manigance — c'est la difference exacte
#    avec `as023` * Kingpin, qui imprime « After Kingpin SCHEMES » et se monte
#    sur `AfterUnitSchemeEnd`. Ne pas copier le voisin sans relire le mot.
#  - **`15004`** / `ho014` / `as023` pour
#    `Worlds.DiscardEncounterCards(8, effect)`, qui REND les faces defaussees.
#  - `an015` / `ho014` pour `face.Reveal(joueur, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After Terrax the Tamer **activates** » : l'ACTIVATION, donc attaque ou
#    manigance indifferemment. Un filtre sur l'une des deux amputerait la
#    carte de la moitie de ses declenchements.
#  - « If the Cosmic Ax attachment was discarded **this way** » : parmi les 8
#    cartes que CETTE capacite vient de defausser, pas « si elle est dans la
#    defausse ». `DiscardEncounterCards` rend la liste, c'est elle qu'on
#    fouille — jamais la defausse entiere.
#  - « **reveal it** » : la reveler declenche son texte, qui la fait
#    s'attacher a Terrax (nt016). Les deux cartes se cherchent
#    mutuellement — nt016 fait le chemin inverse — et c'est le coeur du set
#    nemesis.
#  - « the top **8** cards » : huit, un chiffre enorme qui peut vider le deck
#    de rencontre. `DiscardEncounterCards` s'arrete d'elle-meme
#    (`continue_after_shuffle=False`) : pas de boucle a borner ici,
#    contrairement au piege Underling.
#  - PV 7 pour un sbire nemesis : c'est la moitie d'un vilain, et il revient
#    par le deck de rencontre. La carte est concue pour durer.


def GetAbilities() -> Sequence['Ability']:

    def terrax_the_tamer(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        defaussees = Worlds.DiscardEncounterCards(8, effect)
        if not defaussees:
            return

        for face in defaussees:
            if face.IsName("Cosmic Ax"):
                face.Reveal(message.GetAgainstPlayer(), effect)
                return

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            terrax_the_tamer,
        ),
    ]
