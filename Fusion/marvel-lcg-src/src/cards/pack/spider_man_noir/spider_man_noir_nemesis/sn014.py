from . import *

# Lightning Strikes Twice — TRAITRISE nemesis (N 3/5). x2.
#   Aucune icone de boost chiffree, une icone [star].
# When Revealed: Tuck the top card of the encounter deck under your identity
#   (to a maximum of 3 cards). For each icon ([star] and [boost]) in the boost
#   area of cards tucked under your identity, take 1 damage (to a maximum of 4
#   damage).
# [star] Boost: After this activation, this enemy activates again.
#
# MOT-CLE : BOOST etoile — fiche `docs/reference/mots-cles/boost.md`. L'etoile
# n'est PAS une icone chiffree : `desc.Boost = "0"`, et l'etoile n'existe que
# parce qu'une capacite `WhenCardBecomeBoost` est ecrite. Le moteur ne lit pas
# le texte (`has_boost_icon.py` cherche une `AbilityType.Boost`).
#
# CARTES DE REFERENCE
#  - `15004` / `ho014` : `FacesCounter.CountTotalBoostIcons`.
#  - `ls017` / `55014` / `ho017` : `WhenCardBecomeBoost`.
#  - `21133` / la famille « this enemy activates again » pour le ★ Boost.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « For each icon ([star] AND [boost]) » -> LES DEUX SORTES comptent, et
#    CE N'EST PAS CE QUE REND `CountTotalBoostIcons` : cette fonction-la ne
#    somme que `CountBoostIconsInternal`, c'est-a-dire les icones CHIFFREES
#    (faces_counter.py:142). L'etoile vit dans une propriete separee,
#    `boost_star` (has_boost_icon.py:52), et la seule fonction qui additionne
#    les deux est `CountTotalBoostStarAndBoost` (faces_counter.py:160).
#    Ecrit d'abord avec `CountTotalBoostIcons`, corrige le 05/09/2026 apres
#    lecture du moteur : une pile de trois cartes a etoile seule aurait rendu
#    0 degat au lieu de 3, et aucun outil statique ne l'aurait vu.
#    ⚠ Le helper `IconesDeBoost` du set garde `CountTotalBoostIcons`, lui :
#    `sn001b` et `sn003` disent « the number of BOOST icons », sans etoile.
#    Deux comptes differents dans le meme set, c'est imprime.
#  ⚠ « in the boost area OF CARDS TUCKED UNDER YOUR IDENTITY » -> la PILE, pas
#    la zone de boost du vilain. La carte fait payer au heros exactement ce
#    qui fait sa force.
#  « (to a maximum of 4 damage) » -> plafond SUR LES DEGATS, distinct du
#    plafond de 3 sur la pile. Deux nombres differents dans la meme phrase :
#    trois cartes a deux icones feraient 6, on plafonne a 4.
#  ⚠ ORDRE : on glisse D'ABORD, on compte ENSUITE. La carte qu'on vient de
#    glisser compte donc dans les degats. C'est l'ordre imprime.
#  ⚠ « ★ Boost: AFTER THIS ACTIVATION, this enemy activates again » -> pas
#    « maintenant » : la seconde activation doit attendre la fin de la
#    premiere. `RunAt.AfterEnemyActivationEnd(effect, <message d'activation>,
#    fn)` est la primitive prevue (run_at.py:175), et `face.DoActivate(joueur,
#    effect)` celle qui relance (modele `15027` Chaos Manipulation).
#    ⚠ IL N'EXISTE AUCUN HELPER `ThisEnemyActivatesAgain` : c'etait une API
#    inventee, ecartee avant d'etre ecrite. Verifiee au grep sur tout `src/`.
#  ⚠ Le message de boost porte l'activation en cours sur
#    `message.would_atk_message`, A LIRE AVEC `getattr(..., None)` : elle
#    n'existe pas quand le boost sert une MANIGANCE (fiche boost.md). Sans
#    activation identifiable, on ne relance rien.


def GetAbilities() -> Sequence['Ability']:

    def la_foudre_frappe_deux_fois(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        # « Tuck the top card of the encounter deck under your identity
        #   (to a maximum of 3 cards). »
        if identite.GetPlacedCardArea().GetSize() < 3:
            face = Worlds.DiscardEncounterTopCard(effect)
            if face is not None:
                identite.TuckCardUnderHere(face, effect)

        # « For each icon in the boost area of cards tucked under your
        #   identity, take 1 damage (to a maximum of 4 damage). »
        pile = list(identite.GetPlacedCardArea().Get())
        # ⚠ `CountTotalBoostStarAndBoost` et NON `CountTotalBoostIcons` :
        # « [star] and [boost] ». Voir l'encadre en tete.
        degats = min(4, FacesCounter.CountTotalBoostStarAndBoost(pile) if pile else 0)
        if degats > 0:
            identite.TakeDamage(this, degats, effect)

    def rejouer_lactivation(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        """« ★ Boost: After this activation, this enemy activates again. »"""
        activation = getattr(message, "would_atk_message", None)
        if activation is None:
            return
        ennemi = activation.attacker
        joueur = getattr(activation.property, "against_player", None)
        if ennemi is None or not Player.IsType(joueur):
            return

        def relancer() -> None:
            if ennemi.IsInPlay():
                ennemi.DoActivate(joueur, effect)

        RunAt.AfterEnemyActivationEnd(effect, activation, relancer)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            la_foudre_frappe_deux_fois,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            rejouer_lactivation,
        ),
    ]
