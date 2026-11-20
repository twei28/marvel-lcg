from . import *

# Downtown Attack — traitrise NEMESIS, x3 (3/5, 4/5 et 5/5). Boost 1.
# When Revealed: Remove an ally or PERSONA card in play from the game. If no card was removed from the game this way, take
#   3 indirect damage or discard 3 cards from your hand. Then, remove this card from the game.
#
# Cartes de reference :
#  - `nt015` Cosmic Connection : `WhenThisRevealed(None, op)`, `message.GetToPlayer()`, `joueur.GetControlCardsByType(CardFinder(...),
#    ally=True, upgrade=True, support=True, ...)`, `this.DealIndirectDamage(identite, N, effect)` (degats INDIRECTS repartis par le joueur).
#  - `27099` / `27189b` : `joueur.DiscardHandCards(range, effect)` (le joueur CHOISIT les cartes defaussees).
#  - `sv011`/`sv012` : `Faces.RemoveAllFromGame([carte], effect)`.
#  - choix a deux branches : `joueur.ChooseAbilities(effect, ForChoiceAbility(...), ForChoiceAbility(...))`.
#
# ⚠ Mots-pieges :
#  - DECISION UTILISATEUR (24/10/2026) : le joueur qui revele choisit parmi SES alliés et SES cartes PERSONA (pas celles d'un autre joueur).
#  - « an ally OR PERSONA card » : un allie quelconque ou n'importe quelle carte portant le trait PERSONA (amelioration, soutien...) ;
#    l'identite n'est pas ciblee. « IN PLAY » : une carte glissee ou en main n'est pas en jeu.
#  - « If NO card was removed this way » : le repli (indirect OU defausse) n'a lieu QUE si rien n'a ete retire.
#  - « 3 INDIRECT damage » : repartis, non prevenus par une defense. « discard 3 cards from your HAND » : le joueur choisit lesquelles ;
#    sans 3 cartes, il defausse toute sa main.
#  - « Then, remove THIS card from the game » : la traitrise ne va JAMAIS a la defausse rencontre (3 exemplaires, aucun ne revient).


def GetAbilities() -> Sequence['Ability']:

    def downtown_attack(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            Faces.RemoveAllFromGame([this], effect)
            return

        candidates = list(joueur.GetControlCardsByType(
            CardFinder(card_type=Ally),
            ally=True, upgrade=False, support=False, identity=False, attachment=False,
        ))
        for face in joueur.GetControlCardsByType(
            CardFinder(trait="PERSONA"),
            ally=True, upgrade=True, support=True, identity=False, attachment=False,
        ):
            if face not in candidates:
                candidates.append(face)

        retiree = [False]
        if candidates:
            def retirer(cibles: Sequence['CardFace']) -> None:
                if cibles:
                    Faces.RemoveAllFromGame(list(cibles), effect)
                    retiree[0] = True

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove an ally or PERSONA card in play from the game", retirer,
                ).SetTarget(candidates, range=(1, 1), not_move=True),
            )

        if not retiree[0]:
            def indirects(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                # ⚠ `AttackProperty` N'A PAS de `indirect_damage` (TypeError avale par le moteur, vu sur nt015) :
                # l'API est `DealIndirectDamage`, qui laisse le joueur repartir les degats entre son identite et ses allies.
                identite = joueur.GetIdentity()
                if identite is not None:
                    this.DealIndirectDamage(identite, 3, effect)

            def defausser(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                joueur.DiscardHandCards(("Zero", 3), effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Take 3 indirect damage", indirects),
                AbilityFactory.ForChoiceAbility("Discard 3 cards from your hand", defausser),
            )

        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            downtown_attack,
        ),
    ]
