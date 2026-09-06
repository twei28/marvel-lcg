from . import *

# Hand Ninja — SBIRE nemesis (N 3/5). HAND. NINJA.
#   MNG 1 / ATQ 1* — 2 PV, aucune icone chiffree, une icone ETOILE.
# [star] Hand Ninja's attacks gain piercing.
# Forced Response: After Hand Ninja enters play, it activates against you.
# [star] Boost: Put this minion into play engaged with you.
#
# MOTS-CLES (fiches lues avant d'ecrire)
#  - `piercing` (mots-cles/piercing.md) : les degats ignorent les statuts
#    Tenace. Rendu par `UnitAttackGainKeyword("This", piercing=True)`, modeles
#    `43009` Adamantium Lacing / `27078` / `tg013`.
#  - `special` (mots-cles/special.md) : les deux `[star]` n'ont AUCUNE mention
#    « in expert mode », ils sont donc TOUJOURS actifs. Le premier n'a pas de
#    type imprime et devient une capacite continue de mot-cle ; le second
#    porte le type `Boost`.
#  - `boost` (mots-cles/boost.md) : l'etoile n'est PAS une icone chiffree.
#    `desc.Boost = "0"`, et l'etoile n'existe que parce qu'une capacite
#    `WhenCardBecomeBoost` est ecrite — le moteur ne lit pas le texte
#    (`has_boost_icon.py` cherche une `AbilityType.Boost`).
#
# CARTES DE REFERENCE
#  - `ls017` / `55014` / `ho017` / `sn014` : `WhenCardBecomeBoost`.
#  - `01101` Hydra Mercenary : le squelette d'un petit sbire de rencontre.
#
# TEXTE CONTRE CODE
#  ⚠ L'ETOILE SUR « ATQ 1 » MARQUE LE SPECIAL, pas des degats consecutifs :
#    ceux-ci n'existent que pour les ALLIES (ally.py:41-46). Le depot ecrit
#    quand meme l'asterisque dans les donnees pour un sbire (`57056`, `58026`,
#    `59043`), on fait pareil.
#  ⚠ « After Hand Ninja enters play, IT ACTIVATES AGAINST YOU » -> une Reponse
#    forcee, donc APRES l'entree en jeu. Combinee au Boost etoile, elle rend
#    la carte brutale : le ninja arrive ET frappe dans le meme souffle.
#  ⚠ « Put this minion into play ENGAGED WITH YOU » -> `PutIntoPlay` engage
#    automatiquement un sbire (minion.py:61), il n'y a donc rien de plus a
#    ecrire — mais ce n'est pas evident, d'ou cette ligne.
#  ⚠ Le trait `HAND` est LU par `sf011` Hand Ambush, qui remet les sbires HAND
#    vaincus sur le dessus du deck : ce ninja-la revient donc en boucle tant
#    que le complot est en jeu. C'est le piege du set.


def GetAbilities() -> Sequence['Ability']:

    def sactiver_aussitot(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if Player.IsType(joueur):
            this.DoActivate(joueur, effect)

    def entrer_en_jeu(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if Player.IsType(joueur):
            this.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            sactiver_aussitot,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            entrer_en_jeu,
        ),
    ]
