from . import *

# * Predator (face HEROS) — SOLDIER. YAUTJA. PV 13, THW 0, ATK 3, DEF 2, main 5.
# Response: After a minion enters play, attach Infralocked to it.
# Camouflaged Hunter — Response: After you defeat a minion, give Predator a cloaked status card.
#
# Cartes de reference :
#  - `ar007` God of War (pack ares) : `AfterCardEnterPlay(.., Minion, op)` pour « after a minion enters play » et
#    `AttachTo2(sbire, effect)`, seule voie pour DEPLACER une amelioration deja en jeu vers un autre hote ;
#    `yd012` Yaka Arrow (pack yondu) : amelioration unique qui change d'hote (ennemi / identite).
#  - `an001a` / `vp001a` : `AfterUnitDefeatedUnit(type, "You", Minion, op)` pour « after you defeat a minion ».
#  - `ShinobiCloak` (cards/pack/__init__.py) : « give X a cloaked status card » (fiche mots-cles/cloaked.md).
#
# ⚠ Mots-pieges :
#  - « Response » nu sur la face HEROS : optionnel (le moteur propose), muet en alter-ego.
#  - « After A minion enters play » : n'importe quel sbire, de n'importe quel joueur, quel que soit le chemin (revelation,
#    boost, Xenomorph joue par le joueur) ; Infralocked change alors d'hote (la carte n'a qu'UN exemplaire).
#  - « After YOU defeat a minion » : un sbire vaincu par Predator lui-meme (jamais par un allie) ; Minion, pas Enemy.
#  - « give PREDATOR a cloaked status card » : le HEROS ; une seule carte Cloaked par personnage, et Xenomorph's Prey
#    (pd016) l'interdit tant qu'il est en jeu.


def GetAbilities() -> Sequence['Ability']:

    def marquer(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Hero)
        joueur = JoueurDeCetteCarte(effect)
        sbire = getattr(message, "trigger", None)
        Unused(this)
        if joueur is None or sbire is None or not Minion.IsType(sbire) or not sbire.card.IsOnField():
            return
        infra = Infralocked(effect, joueur)
        if infra is None or infra.bind_face is sbire:
            return
        infra.AttachTo2(sbire, effect)

    def chasseur_camoufle(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        Camoufler(effect, JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            Minion,
            marquer,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Minion,
            chasseur_camoufle,
        ).SetName("Camouflaged Hunter"),
        ActionHonorHuntEnVitrine(),
    ]
