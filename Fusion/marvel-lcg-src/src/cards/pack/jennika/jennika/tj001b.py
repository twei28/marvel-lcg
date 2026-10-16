from . import *

# * Jenny (face alter-ego) — TEENAGER. MUTANT. TURTLE. REC 3 / PV 12 / main 5.
# Setup: Put the Sosaiken Path into play under your control.
# Action: Discard 1 card from your hand -> search your deck and discard pile for
#   up to 2 TEKKO-KAGI upgrades and put them into play, exhausted. (Shuffle.)
#
# Cartes de reference :
#  - Setup « put <carte mise de cote> into play » : `wonder_man/58001b` +
#    `58002` Ionic Physiology (Permanent, mise de cote) :
#    `AbilityFactory.BeginGameWithSetAside([id], op)` fabrique la carte dans
#    `additional_discard_pile`, `op` la met en jeu ; `deck/starter` la porte dans
#    `set_aside` ;
#  - fouille « up to 2 <trait> upgrades ... exhausted » : `michelangelo/tm001b`
#    (Nunchuck) : `Search.PlayerCard(..., trait=..., card_type=Upgrade, may=True)`
#    deux fois + `PutIntoPlay(player, effect, exhaust=True)`.
#
# ⚠ Mots-pieges :
#  - « Put the Sosaiken Path into play UNDER YOUR CONTROL » : `under_control=True` ;
#  - la Voie est MISE DE COTE (elle n'est pas dans les 15 cartes du deck, comme
#    Ionic Physiology de Wonder Man) : la main de depart n'est donc pas amputee ;
#  - « Action » sur la face alter-ego : `AbilityType.Action` (modele si001b), PAS
#    `AlterEgoAction` ;
#  - le « -> » est un COUT : defausser 1 carte de la main AVANT de chercher ;
#  - « up to 2 » : deux recherches successives, `may=True` ; « deck AND discard
#    pile » : include_discard_pile=True ; « (Shuffle.) » = comportement par
#    defaut de Search ;
#  - « TEKKO-KAGI upgrades » : trait ET type Upgrade (tj009, tj010).


# DECISION UTILISATEUR (16/10/2026, Q4) (la Voie mise de cote plutot que dans le deck) : .planning/tmnt/jennika-questions.md
def GetAbilities() -> Sequence['Ability']:

    def mettre_la_voie_en_jeu(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        for zone in (joueur.set_aside_deck, joueur.additional_discard_pile):
            for face in list(zone.Get()):
                if face.paper.card_id == 'tj011':
                    face.CastTo(Path).PutIntoPlay(joueur, effect, under_control=True)
                    return

    def chercher_les_tekko_kagi(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        for _ in range(2):
            face = Search.PlayerCard(
                effect,
                joueur,
                include_player_deck=True,
                include_discard_pile=True,
                trait="TEKKO-KAGI",
                card_type=Upgrade,
                may=True,
            )
            if not face:
                break
            face.PutIntoPlay(joueur, effect, exhaust=True)

    return [
        AbilityFactory.BeginGameWithSetAside(['tj011'], mettre_la_voie_en_jeu),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            chercher_les_tekko_kagi,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
