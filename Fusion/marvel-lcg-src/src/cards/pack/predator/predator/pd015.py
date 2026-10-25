from . import *

# Exposed Target — Obligation (set « Predator »), Boost 2, « Give to the Yd'Nar player ».
# You may flip to alter-ego form. Choose:
#  • Exhaust Yd'Nar → remove Exposed Target from the game.
#  • Discard each cloaked status card from your identity and 1 TECH upgrade you control. If no cards were discarded this way,
#    this card gains surge. Discard this obligation.
#
# Cartes de reference :
#  - `sv011` Silver Down (silver_surfer) / `ch018` Family Ties (shang_chi) : MEME squelette — `WhenThisObligationGiveToYou`,
#    `YouMayFlipToYourAlterEgoForm`, puis `joueur.ChooseAbilities` avec `condition=` par branche ;
#  - `ThisCardGainSurge(effect)` (nt015, mf017) pour « this card gains surge » ;
#  - `face.DiscardCloaked(effect, rule="All")` (can_status.py) pour « discard each cloaked status card ».
#
# ⚠ Mots-pieges :
#  - 1re branche : « → remove FROM THE GAME » ; 2e branche : « DISCARD this obligation » : deux sorties DIFFERENTES (hc013 : une
#    obligation reste en jeu tant qu'on ne la deplace pas) ;
#  - « Exhaust Yd'Nar » : l'alter-ego, donc seulement apres le retournement et s'il est pret ; la fleche en fait un COUT ;
#  - « discard each cloaked status card FROM YOUR IDENTITY AND 1 TECH upgrade YOU CONTROL » : les deux defausses, la carte
#    Cloaked de Predator ET UNE amelioration TECH de ce joueur (au choix) ; « if NO cards were discarded this way » : ni Cloaked
#    ni TECH defaussee -> surge (puis la carte est defaussee comme le texte l'ordonne).


def GetAbilities() -> Sequence['Ability']:

    def exposed_target(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        identite = joueur.GetIdentity()

        def incliner_puis_retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if identite is None:
                return
            Faces.ExhaustAll([identite], effect)
            Faces.RemoveAllFromGame([this], effect)

        def se_debarrasser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            defaussees = 0
            heros = identite.GetHeroFace() if identite is not None else None
            if heros is not None and heros.IsCloaked():
                defaussees += int(heros.DiscardCloaked(effect, rule="All") or 0)
            techs = [u for u in Worlds.FindCardsOnField(effect, card_type=Upgrade, trait="TECH")
                     if u.GetControlByOrOwner() is joueur]
            if techs:
                choisie = joueur.AskChooseFace(techs, effect, prompt="Discard a TECH upgrade")
                if choisie is not None:
                    defaussees += len(Faces.DiscardAll([choisie], effect))
            if defaussees == 0:
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Yd'Nar → remove Exposed Target from the game",
                incliner_puis_retirer,
                condition=(identite is not None and joueur.IsAlterEgo() and not identite.IsExhaust()),
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard each cloaked status card and 1 TECH upgrade. If none were discarded, this card gains surge. Discard this obligation",
                se_debarrasser,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            exposed_target,
        ),
    ]
