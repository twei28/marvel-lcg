from . import *

# * Buffy (face heros) : HP 10, ATK 1, THW 1, DEF 1, main 5. SLAYER.
# Buffy gets +1 to each basic power for each HELLMOUTH side scheme in the victory display.
# Chosen One — Response: After a minion enters play, draw 1 card. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `mw001a` Madame Web : `ThisGainKeyword(fn, attack=1, thwart=1, defense=1, change_on_event=..)` pour « +X a chaque pouvoir de base ».
#  - `howard_the_duck/hd002` (meme auteur) : decompte de la zone de victoire par `Worlds.VictoryDisplay(effect).FindCards(..)`.
#  - `ThisGainKeywordWhileFaceIsInVictoryDisplay` (enhance_self.py) : l'evenement `OnEvent.Victory(finder)` qui releve le bonus
#    quand la zone de victoire change.
#  - `hd001a` Howard the Duck : `AfterCardEnterPlay(Response, <type>, op).LimitOncePerRound()` pour la Reponse limitee.
#
# TEXTE CONTRE CODE
#  « Buffy gets » -> NOM PROPRE : la capacite vit sur la face HEROS seulement (l'alter-ego s'appelle Buffy Summers).
#  « each basic power » -> ATK, THW ET DEF (`attack=1, thwart=1, defense=1`) ; la recuperation (REC) n'est pas un pouvoir de
#    heros, elle n'est pas touchee.
#  « HELLMOUTH side scheme in the victory display » -> `CardFinder2("HELLMOUTH", SchemeSide2)` dans `VictoryDisplay`. Une
#    manigance annexe SANS le trait, ou HELLMOUTH mais ailleurs que dans la zone de victoire, ne compte pas.
#  « a minion enters play » -> `Minion` (tout sbire, de rencontre ou allie), `Response` NU : pas « Hero Response ».
#  « draw 1 card » -> `DrawUp(1)`. « Limit once per round » -> `LimitOncePerRound`. Chiffres : +1, 1 carte.


def GetAbilities() -> Sequence['Ability']:

    def pour_chaque_hellmouth(effect: 'Effect', ui: List['CardFace']) -> int:
        faces = ManigancesHellmouthEnVictoire(effect)
        ui.extend(faces)
        return len(faces)

    def chosen_one(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            pour_chaque_hellmouth,
            attack=1,
            thwart=1,
            defense=1,
            change_on_event=OnEvent.Victory(ManigancesHellmouth()),
        ),
        (AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            Minion,
            chosen_one,
        )
            .SetName("Chosen One")
            .LimitOncePerRound()),
    ]
