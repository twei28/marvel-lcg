from . import *

# Rotten Lightning — TRAITRISE (deck signature de Zombie Thor, carte 2/3). Trait ATTACK.
# When Revealed: Deal 2 damage to each friendly character.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « friendly character » n'est PAS un mot-cle maison/officiel a fiche dediee (absent de
#   `docs/reference/mots-cles/README.md` comme entree a part) : c'est un terme de regle de base du moteur,
#   couvert directement par `Worlds.GetOnFieldFriendlyCharacters` (identites + allies de TOUS les joueurs en
#   partie), pas par une fiche a ouvrir. Le trait ATTACK imprime sur la carte n'est que de la categorisation
#   thematique (filtrage des sets de rencontre côté editeur) : cette carte ne fait AUCUN appel a `DoActivate`,
#   elle infuse les degats directement comme l'indique son texte imprime (« Deal X damage », pas « attacks »).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « When Revealed: Deal 2 damage to each friendly character » : modele exact `core/01154.py` (Concussive
#   Blast, « When Revealed: Deal 1 damage to each friendly character ») : `Worlds.GetOnFieldFriendlyCharacters
#   (effect)` puis `this.DealDamage(units, N, effect)`. Memes cartes de reference que `wc021`/`wc022`
#   (Wiccan, « Deal 1 damage to each friendly character ») et `twc 07027` pour la variante « you control » (non
#   imprimee ici : hg035 vise bien TOUS les joueurs, cf. bloc texte-contre-code plus bas).
#   Seule difference avec 01154 : hg035 n'a pas de ligne [star] Boost sur le scan fourni — rien d'autre a
#   scripter que le When Revealed.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte
#   (`Condition2.ThisIsTrigger` deja integre a la fabrique, aucune garde a ajouter).
# « Deal 2 damage » -> `this.DealDamage(cibles, 2, effect)`, valeur imprimee = 2 (identique dans
#   `data/cards_custom.json` : `"text": "<b>When Revealed</b>: Deal 2 damage to each friendly character."`,
#   aucun champ `desc` numerique a recouper — cette carte n'a pas de `desc` chiffre).
# « to EACH friendly character » -> `Worlds.GetOnFieldFriendlyCharacters(effect)` : identite (Heros OU
#   Alter-Ego, peu importe la forme) + chaque allie, de CHAQUE joueur en partie (pas seulement le joueur qui
#   revele), meme lecture que `01154` et `wc021`. PAS `player.GetControlCharacters()` (reserve a la variante
#   « you control », absente du texte imprime de hg035) ni `Villains.All`/`Metazombies` (aucun des deux ne
#   designe un personnage « friendly », qui ne concerne que le cote joueurs).
# Aucun `unless`/`otherwise`/`instead`/`if you cannot` imprime sur cette carte : rien d'autre a coder.
#
# A CONFIRMER : aucun doute releve. Carte strictement identique en structure a 01154/wc021, simple changement
# de valeur (2 au lieu de 1) et de theme (Zombie Thor plutot que Rhino/Moridun).

def GetAbilities() -> Sequence['Ability']:

    def foudre_pourrie(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(Treachery)
        units = Worlds.GetOnFieldFriendlyCharacters(effect)
        this.DealDamage(units, 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            foudre_pourrie,
        ),
    ]
