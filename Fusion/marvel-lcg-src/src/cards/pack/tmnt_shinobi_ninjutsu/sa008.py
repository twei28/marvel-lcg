from . import *

# Smoke Bombs — AMELIORATION 1 [physical], Ninjutsu (TMNT Shinobi, Inkwire). ITEM.
# Uses (2 smoke counters). Max 1 per player.
# Hero Action: Exhaust this card and remove 1 smoke counter from it -> cloak a friendly character.
# « Now you see me... » —Ronin
#
# NOUVELLE. HOMONYME de `27139` Smoke Bombs (set Goblin Gear, ATTACHEMENT du vilain a « bomb counters », aucun
# rapport de regles) : confirme sur le scan (amelioration joueur ITEM, « smoke counters »).
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md), Cloak / Cloaked (cloak.md, cloaked.md), compteur « smoke »
# (shadow-counter.md, cree avec cette carte).
#
# Cartes de reference :
#  - `tj006` Fearless Resolve : amelioration a `Uses` (`desc.Uses = "N,<compteur>"`, NATIF : compteurs poses a l'entree en
#    jeu, carte defaussee au dernier retire) + `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 1, '<compteur>')` ;
#  - `up023` Lookout : amelioration sans « Attach to » = `CanPlayThisUpgradeCard()` (posee devant le joueur, « Max 1 per
#    player » par `desc.MaxPerUnit`) ;
#  - `ud004` / `td005` : « cloak a friendly character » = choix parmi les personnages amis (`Worlds.GetOnFieldFriendlyCharacters`).
#
# TEXTE CONTRE CODE
#  ⚠ « Uses (2 smoke counters) » : 2 compteurs a l'entree en jeu ; la carte part avec le dernier : DEUX utilisations.
#  ⚠ « Max 1 per player » : `MaxPerUnit = 1` (une seule par joueur en jeu).
#  ⚠ « Exhaust this card AND remove 1 smoke counter FROM IT » : deux couts. « cloak A FRIENDLY character » : un
#    personnage AMI au choix : identites et allies de TOUS les joueurs, pas un ennemi.
#  ⚠ « Hero Action » : forme heros.


def GetAbilities() -> Sequence['Ability']:

    def smoke_bombs(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        ShinobiCloak(effect, effect.targets)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            smoke_bombs,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'smoke'))
        .SetTarget(Friend),
    ]
