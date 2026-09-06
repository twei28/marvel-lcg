from . import *

# * Throg's Armor — AMELIORATION, cout 2, [physical]. ARMOR. ASGARD. UNIQUE.
# You get +2 hit points.
# Hero Response: After you engage a minion, give Throg a tough status card.
#   If you cannot, draw 1 card. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `43009` Adamantium Lacing : le gabarit exact des deux portees dans une
#    meme carte — `GiveKeywordToAttached("You", health=2)` pour « YOU get »,
#    et `GiveKeywordToAttached(CardFinder(name=...), ...)` pour un NOM PROPRE.
#  - `56041` * Patriot: Elijah Bradley : « Response: After you engage a
#    minion, ... » -> `AfterPlayerEngageMinion(<type>, "You", op)`, et
#    `Faces.GiveStatus([...], "Tough", effect)`.
#  - `19001a` * Drax : « ... If you cannot, draw 1 card. » Le repli se mesure,
#    il ne se devine pas.
#
# TEXTE CONTRE CODE
#  ⚠ « YOU get +2 hit points » contre « give THROG a tough status card », sur
#    la MEME carte : les deux portees cohabitent et le contraste est imprime.
#    « You » designe l'IDENTITE, donc les deux faces — Puddlegulp a lui aussi
#    +2 PV. « Throg » est un NOM PROPRE et ne designe que la face heros.
#    Piege `an002` Sera / `06007` Asgard (RECETTES-MOTEUR §3), et le seul
#    endroit du pack ou les deux ecritures se cotoient. Un contre-cas en forme
#    alter-ego prouve les +2 PV ; la Reponse, elle, est « HERO ».
#  ⚠ « IF YOU CANNOT, draw 1 card » -> le repli ne doit PAS etre lie a une
#    cible legale. Le declarer en `SetTarget(..., canbe_tough=True)` (montage
#    de `56041`) rendrait l'abilite sans cible legale quand Throg est deja
#    Tenace : elle ne partirait jamais, et la pioche de repli — le seul cas ou
#    elle sert — serait morte. Meme piege que `ah007` (pack
#    totally_awesome_hulk), paye et commente la-bas. On donne donc le statut
#    dans le corps et on lit le RETOUR de `Faces.GiveStatus`, qui compte les
#    unites reellement servies (faces.py:180-186).
#  « After YOU ENGAGE a minion » -> l'engagement fait par le JOUEUR, quelle
#    qu'en soit la cause : tg002 Airborne Amphibian, tg003 Great Courage,
#    l'obligation tg011, ou un sbire qui s'engage de lui-meme. C'est ce qui
#    rend l'armure rentable dans un pack qui attire les sbires.
#  « (Limit once per PHASE.) » -> `.LimitOncePerPhase()`. Engager trois sbires
#    d'un coup avec Great Courage ne donne QU'UN Tenace : le temoin
#    d'epuisement le mesure (etape 7 bis de PROCESSUS-CARTE).


def GetAbilities() -> Sequence['Ability']:

    def armure_de_throg(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        heros = HerosDuJoueur(effect)
        donnes = Faces.GiveStatus([heros], "Tough", effect) if heros is not None else 0
        if donnes == 0:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=2,
        ),
        AbilityFactory.AfterPlayerEngageMinion(
            AbilityType.HeroResponse,
            "You",
            armure_de_throg,
        ).LimitOncePerPhase(),
    ]
