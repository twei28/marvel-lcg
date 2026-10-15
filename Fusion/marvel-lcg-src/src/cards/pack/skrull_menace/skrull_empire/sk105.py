from . import *

# Overthrow — TRAITRISE x3 (Skrull Empire). 1 icone boost etoile.
# When Revealed: Remove the current villain from the game and reveal the top
#   card of the villain deck. Then, set Overthrow aside, out of play.
# ★ Boost: Deal this card to yourself as a facedown encounter card.
#
# Cartes de reference :
#  - **`55051`** (God of Lies) : remplacer le mechant courant par un autre ;
#    ici par le DESSUS du paquet mechant (ordre impose, livret p. 8), via
#    `RemplacerMechant` (helper du set).
#  - **`hood 24012`** / deadpool `44037` : une traitrise qui se met hors du jeu
#    elle-meme (`Faces.SetAside([this])`, sans defausse : fix_treachery).
#  - **`32167`** : « Deal this card to yourself as a facedown encounter card » =
#    `player.DealEncounterCard(this, effect)`.
#
# ⚠ Mots-pieges : « REMOVE ... from the game » (pas defausse) ; attachements et
# statuts du mechant partent avec lui, seules les cartes boost restent (livret
# p. 8, NettoyerMechant) ; « Then, set Overthrow aside » : APRES le changement ;
# l'environnement II/III les remelangera. Au plus 3 Overthrow par stade pour 4
# mechants : le paquet mechant ne peut pas etre vide (RemplacerMechant ne fait
# rien dans ce cas).


def GetAbilities() -> Sequence['Ability']:

    def renverser(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)
        RemplacerMechant(effect)
        Faces.SetAside([this], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        message.GetToPlayer().DealEncounterCard(this, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, renverser),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
