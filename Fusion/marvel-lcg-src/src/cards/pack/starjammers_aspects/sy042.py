from . import *
# * Kalyx (Protection, allie 4 [physical], 1*/1*, PV 3). STARJAMMER.
# Forced Response: After Kalyx enters play, find Thorn Crew and put it into play.
# [star] Response: After Kalyx uses a basic power, put the top card of your deck into play facedown as a THORN ally.
#
# Cartes de reference : 01135 Ultron / `Enemies.PutYouDeckTopCardAsFacedownMinion` (enemies.py:444 : `player.PopPlayerDeckCards(n, process)`
# + `face.card.SetAsCard(<gabarit>)` + `PutIntoPlay`) ; ul040 / tk101 (carte `Linked` : sy043 est fabriquee MISE DE COTE des que Kalyx est
# creee, fiche linked.md) ; wt020 (`TreatAsAlly`).
# ⚠ Le gabarit d'allie face cachee `sy_thorn_ally` (cards.json, pic « player », ATQ 1, CTR 1, PV 1, trait THORN) porte les valeurs de base que
# donne Thorn Crew : « each facedown THORN ally has a base THW 1, ATK 1 and hit points 1 ». ⚠ « find Thorn Crew » : la lame vit dans la zone mise de cote.
def GetAbilities() -> Sequence['Ability']:
    def kalyx_entre(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        joueur = JoueurDe(effect)
        crews = [f for f in Worlds.GetSetAsideAreaCards(effect) if getattr(f.paper, "card_id", None) == "sy043"]
        if joueur is not None and crews:
            crews[0].PutIntoPlay(joueur, effect, under_control=True)
    def une_equipe_de_cote(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> bool:
        return any(getattr(f.paper, "card_id", None) == "sy043" for f in Worlds.GetSetAsideAreaCards(effect))
    def kalyx_pouvoir(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        def process(face: 'CardFace') -> None:
            from game.card.factory import CardFactory
            gabarit = CardFactory.CreateFace(CardFactory.FindCardPapers("sy_thorn_ally")[0], effect.world)
            face.card.SetAsCard(gabarit)
            face.card.face.CastTo(Ally).PutIntoPlay(joueur, effect)
        joueur.PopPlayerDeckCards(1, process, effect)
    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            kalyx_entre,
            conditions=[une_equipe_de_cote],
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            kalyx_pouvoir,
            powers=["ATK", "THW", "DEF"],
        ),
    ]
