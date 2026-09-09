from . import *

# Power Surge — TRAITRISE nemesis, x2. Icone boost etoile.
# When Revealed: Discard the top 5 cards of your deck. Take indirect damage
#   equal to the number of [energy] resources discarded this way. If 2 or less
#   damage was dealt this way, this card gains surge.
# [star] Boost: This card gets +1 boost icon ([boost]) for each [energy]
#   resource in your hand.
#
# CARTES DE REFERENCE
#  - `sm014` et `sm015` (meme set) : le decompte d'icones energie sur des
#    cartes defaussees, `FacesCounter.GetPrintedResources([...]).GetColor(
#    "Y", convert_green_res=False)`.
#  - `an013`, `16140`, `ho015`, `ho017` : « [star] Boost: ... » =
#    `WhenCardBecomeBoost("This", op)`, et les icones s'ajoutent par
#    `face.GainBoostIcons(n, effect)`.
#  - `an010` : `this.GainSurge(1, effect)` pour « gains surge ».
#  - `al022`, `16026` : `identite.TakeIndirectDamage(this, N, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « IF 2 OR LESS DAMAGE WAS DEALT THIS WAY » : la condition porte sur les
#    DEGATS INFLIGES, donc sur le nombre d'icones energie trouvees — et elle
#    est vraie a ZERO. Une defausse sans la moindre energie donne 0 degat,
#    donc « 2 or less », donc SURGE. C'est l'inverse de l'intuition (« il ne
#    s'est rien passe, donc rien ne suit ») et c'est le coeur de la carte :
#    elle est dangereuse quand elle ne fait rien.
#  ⚠ « discard the TOP 5 cards of YOUR deck » : le deck du joueur a qui la
#    carte est revelee (`message.GetToPlayer()`), pas chaque joueur —
#    contrairement a `sm014` Containment Breach, qui dit « each player ». Deux
#    cartes du meme set, deux portees : les lire mot a mot.
#  ⚠ Un deck de moins de 5 cartes ne bloque rien : on compte ce qui est sorti.
#  ⚠ « [star] Boost » : l'etoile signifie qu'il n'y a AUCUNE icone boost
#    chiffree sur la carte, seulement cette capacite. `desc` ne porte donc PAS
#    de cle `Boost` (convention verifiee sur `01121`, `01123`, `01129`... :
#    toutes ont `Boost: None`), et c'est l'existence d'une `AbilityType.Boost`
#    qui allume l'etoile (`has_boost_icon.py:52`).
#  ⚠ « for each [energy] resource IN YOUR HAND » : les icones imprimees des
#    cartes en MAIN au moment ou la carte de boost est retournee, pas les
#    cartes elles-memes. Une carte a deux icones energie en vaut DEUX.
#    ⚠⚠ Et « YOUR hand » designe LE JOUEUR QUI DEFEND, pas le proprietaire de
#    la nemesis : le moteur l'ecrit noir sur blanc (sender_card.py:688), et
#    `message.GetToPlayer()` rend deja ce joueur-la. A deux joueurs, la carte
#    grossit donc selon la main de celui qui encaisse.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def surtension(effect: 'Effect', message: 'Message.WhenThisRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        defaussees = joueur.DiscardDeckTopCards(5, effect)
        energie = IconesEnergie(defaussees)

        if energie > 0:
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(this, energie, effect)

        # ⚠ « 2 or less » est VRAI a zero : voir le bloc texte-contre-code.
        if energie <= 2:
            this.GainSurge(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)

        # ⚠ « YOUR hand » sur une capacite Boost = LE JOUEUR QUI DEFEND, et le
        # moteur le dit lui-meme (sender_card.py:688 : « Any constant or boost
        # abilities that refer to "you" refer to the defending player »). Une
        # carte de rencontre n'a pas de controleur joueur : `JoueurDeCetteCarte`
        # rendrait None ou le mauvais joueur.
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        en_main = [c for c in joueur.hand_cards.Get() if c is not None]
        energie = IconesEnergie(en_main)
        if energie > 0:
            this.GainBoostIcons(energie, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            surtension,
        ),

        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
