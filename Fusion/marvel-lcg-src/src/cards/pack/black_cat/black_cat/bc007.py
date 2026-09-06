from . import *

# Misfortune — EVENEMENT, cout 0, [mental]. SUPERPOWER. x2.
# Hero Interrupt: When a boost card is flipped during an enemy activation,
#   tuck it under your hero instead. That enemy gets -1 ATK and -1 SCH for that
#   activation for each icon ([star] and [boost]) in that card's boost area.
#
# ---------------------------------------------------------------------------
# ⚠⚠ CARTE A BOUCLE INFINIE SI ON LA CODE DE TRAVERS. A LIRE AVANT DE TOUCHER.
#
# `CanBoost.ResolveBoostCards` (can_boost.py:51-62) tourne ainsi :
#
#     while <paquet de boost non vide>:
#         face = <carte du dessus>
#         would = WhenBoostCardWouldTurnedFaceUp(face, ...)
#         would.Send()
#         if would.is_be_instead:
#             continue          # <-- ON REPART SUR LA MEME CARTE
#         ...
#
# Le `continue` ne retire PAS la carte du paquet. Poser `SetBeInstead` sans
# faire QUITTER la carte, c'est une boucle infinie : la partie se fige et
# `test_capacites` ne rendrait qu'un timeout. Piege identique a `sn004` Web
# Shot, paye la veille — ici la sortie est garantie par le glissement, qui n'a
# AUCUN plafond dans ce pack (voir `GlisserSousIdentite`).
# ---------------------------------------------------------------------------
#
# CARTES DE REFERENCE
#  - `sn004` Web Shot (pack spider_man_noir) : meme fenetre, meme « instead »,
#    meme obligation de sortie.
#  - `sd020` Inspirational Art : le pipeline complet des cartes de bonus, et
#    la raison de preferer « would » quand on veut EMPECHER le retournement.
#  - `19018` Subdue : `message.GainATKForThisAttack(-3, effect)`, LA primitive
#    du « -X ATK for that attack ».
#
# TEXTE CONTRE CODE
#  ⚠ « during an ENEMY activation » -> vilain OU sbire. On ne passe donc PAS
#    `boost_for_card=Villain` (ce que fait `sd020`, qui dit « villain »).
#  ⚠ « -1 ATK AND -1 SCH » -> les deux sont ecrits, mais UNE activation est
#    soit une attaque, soit une manigance : le moteur n'expose que l'une des
#    deux a la fois (`would_message` est un `WhenUnitWouldAttack` OU un
#    `WhenUnitWouldScheme`). On applique donc celui qui existe. Ce n'est pas un
#    ecart : les deux moities de la phrase ne peuvent pas tomber ensemble.
#  ⚠ « FOR THAT ACTIVATION » -> `GainATKForThisAttack` /
#    `GainSCHForThisScheme`, qui vivent dans le message d'activation en cours.
#    Un `GainKeyword` permanent serait faux.
#  ⚠ « each icon ([star] AND [boost]) » -> `IconesEtEtoiles`.
#  ⚠ ON COMPTE AVANT DE GLISSER : une fois dans la pile,
#    `CountBoostIconsInternal` (has_boost_icon.py:33) court-circuite tout et
#    rend `printed_boost`. La valeur serait souvent la meme, mais pas toujours
#    (une icone ajoutee par `sd020` disparaitrait), et on ne code pas sur un
#    « souvent ».
#  « tuck it under YOUR HERO » -> la pile de l'identite, portee par la CARTE
#    (card_face.py:1017). Le nom n'est pas employe : trois « * Black Cat » au
#    depot.


def GetAbilities() -> Sequence['Ability']:

    def malchance(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        carte = message.trigger

        # ⚠ Compter AVANT de glisser (voir l'encadre).
        malus = IconesEtEtoiles([carte]) if carte is not None else 0

        message.SetBeInstead(effect)

        # ⚠ LA CARTE DOIT QUITTER LE PAQUET DE BOOST DANS TOUS LES CAS.
        if carte is not None:
            glissees = GlisserSousIdentite(effect, [carte], JoueurDeCetteCarte(effect))
            if not glissees:
                Faces.DiscardAll([carte], effect)

        if malus <= 0:
            return

        activation = getattr(message, "would_message", None)
        if isinstance(activation, Message.WhenUnitWouldAttack):
            activation.GainATKForThisAttack(-malus, effect)
        elif isinstance(activation, Message.WhenUnitWouldScheme):
            activation.GainSCHForThisScheme(-malus, effect)

    return [
        AbilityFactory.WhenBoostCardWouldTurnedFaceUp(
            AbilityType.HeroInterrupt,
            malchance,
        ).SetPlay(),
    ]
