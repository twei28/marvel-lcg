from . import *

# * Cosmic Ax — ATTACHEMENT nemesis (5/5). WEAPON. +2 ATQ. Boost 2 + [star].
# Attach to Terrax the Tamer. If you cannot, discard the top 8 cards of the
#   encounter deck. If Terrax the Tamer was discarded this way, reveal him and
#   attach Cosmic Ax to him.
# [star] Boost: If Terrax the Tamer is in play, reveal this card.
#
# Cartes de reference :
#  - **`ag013`** Hallucination (pack agent_13) : MEME structure — un
#    attachement qui cherche son porteur, `Worlds.DiscardEncounterCardsUntil`
#    ou `DiscardEncounterCards` puis `minion.Reveal(...)` et
#    `this.AttachTo2(minion, effect)` (can_attach.py:49).
#  - `40122a` * Juggernaut's Helmet pour
#    `AttachToFaceWhenPutIntoPlay(CardFinder(name=...))` et le `+2 ATK` lu
#    directement dans `desc.ATK+`.
#  - `an013` Hel-Wolf / `ho015` pour `WhenCardBecomeBoost("This", op)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **If you cannot** » : verifie AVANT de chercher, pas apres un refus.
#    Terrax absent du terrain = on ne peut pas, donc on fouille. Terrax
#    present = on attache, point final, et les 8 cartes ne sont PAS
#    defaussees (piege `wd028`).
#  - « If Terrax the Tamer was discarded **this way** » : parmi les 8 cartes
#    que CETTE capacite vient de defausser, jamais « s'il est dans la
#    defausse ».
#  - « reveal him **and** attach Cosmic Ax to him » : les deux, dans cet
#    ordre. Le reveler le met en jeu, l'attachement suit.
#  - Symetrie avec `nt013` : Terrax cherche la hache, la hache cherche Terrax.
#    Les deux cartes se rappellent mutuellement, et c'est ce qui fait tenir le
#    set nemesis. Ne pas « simplifier » l'une des deux.
#  - « [star] **Boost**: If Terrax the Tamer is in play, reveal this card. » :
#    une capacite de BOOST, donc active uniquement quand la carte sort comme
#    carte de boost. `[star]` sans « In expert mode » = toujours active
#    (convention moteur, cf. 04125).
#  - « **+2 ATK** » : lu dans `desc["ATK+"]` par le moteur, AUCUN script.


def GetAbilities() -> Sequence['Ability']:

    def chercher_terrax(effect: 'Effect') -> 'CardFace|None':
        return Worlds.FindCardOnField(effect, name="Terrax the Tamer", card_type=Minion)

    def cosmic_ax(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)

        joueur = message.GetToPlayer()

        terrax = chercher_terrax(effect)
        if terrax is not None:
            this.AttachTo2(terrax, effect)
            return

        # « If you cannot » : Terrax n'est pas en jeu, on le cherche.
        defaussees = Worlds.DiscardEncounterCards(8, effect)
        for face in defaussees or []:
            if face.IsName("Terrax the Tamer"):
                face.Reveal(joueur, effect)
                trouve = chercher_terrax(effect)
                if trouve is not None:
                    this.AttachTo2(trouve, effect)
                return

    def cosmic_ax_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        if chercher_terrax(effect) is None:
            return
        effect.this.Reveal(message.against_player, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            cosmic_ax,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            cosmic_ax_boost,
        ),
    ]
