from . import *

# Widow's Bite — TRAITRISE (deck signature de Zombie Black Widow, carte 1/3). Pas de trait imprime.
# When Revealed (Alter-Ego): Place 1 infection counter. This card gains Surge.
# When Revealed (Hero): Your hero is stunned. Place 1 infection counter.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Charpente « When Revealed (Alter-Ego) / When Revealed (Hero) » (deux Reponses a la Revelation distinctes,
#   selon la FORME du joueur a qui la carte est revelee) : modele officiel `01106` Stampede (pack `core/rhino`) :
#   `AbilityFactory.WhenThisRevealed("Alter-Ego", ...)` et `AbilityFactory.WhenThisRevealed("Hero", ...)`, DEUX
#   entrees separees dans la liste retournee par `GetAbilities`, chacune avec son propre callback -- jamais un
#   seul callback qui testerait la forme a la main (le parametre de forme de `WhenThisRevealed` fait deja ce
#   filtrage nativement). Egalement conforme a `04120` Mind Ray (meme charpente, deux callbacks nommes
#   `..._alter_ego` / `..._hero`).
# - « This card gains Surge » (branche Alter-Ego) : modele `01106` Stampede, meme branche Alter-Ego exactement :
#   `ThisCardGainSurge` (helper partage `cards/pack/__init__.py:111`, deja documente en fiche [[surge]]), passe
#   directement comme callback OU appele depuis le callback local (ici: appele, pour pouvoir aussi poser le
#   compteur d'infection dans la meme branche -- Stampede n'avait qu'UNE chose a faire dans sa branche
#   Alter-Ego, donc passait le helper nu ; Widow's Bite en a deux, donc le callback local appelle les deux).
# - « Place 1 infection counter » (les DEUX branches) : helper DEJA EXISTANT du scenario, `commun.PoserInfection
#   (effect, joueur, n=1)` (`cards/pack/the_hunger_core/commun.py:307`), deja utilise par `hg002`/`hg003` de ce
#   meme pack pour la meme phrase imprimee. Pose le compteur sur l'identite du joueur resolvant la carte
#   (`Faces.PlaceCountersOn([joueur.GetIdentity()], n, 'infection', effect)`), conforme au livret cite dans son
#   docstring (« a second health bar... tracked... next to your identity card »).
# - « Your hero is stunned » (branche Hero) : modele `01106` Stampede (`Faces.GiveStatus(units, "Stunned",
#   effect)`) et `04120` Mind Ray (`Faces.GiveStatus([hero], "Stunned", effect)` -- cible le HEROS directement,
#   pas l'identite generique comme le fait Mind Ray pour « Confused » en branche Alter-Ego). Widow's Bite dit
#   « Your HERO is stunned » (sujet explicite = le heros), donc modele retenu : `04120`, cible `player.GetHero()`.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[surge]] (mots-cles/surge.md) : « This card gains Surge » -> `ThisCardGainSurge`, lu avant d'ecrire la
#   branche Alter-Ego. Rien a coder pour l'EFFET du mot-cle une fois gagne (automatique, `desc.Surge`/
#   `GainSurge`) : seul le GAIN (la phrase imprimee elle-meme) est scripte ici.
# - « infection counter » : PAS une fiche `mots-cles/` dediee, et aucune a creer. Le texte imprime ne met
#   « infection » ni en gras ni en italique (contrairement a `[[Surge]]`) : c'est un COMPTEUR DE CARTE/SCENARIO
#   nomme ordinaire, meme critere que les compteurs `flame` (`human_torch`), `rage`
#   (`totally_awesome_hulk`) ou `web` (`spider_man_rainy`) deja tranches en tete de
#   `docs/reference/mots-cles/README.md` (« ce sont des compteurs de carte, pas un mot-cle »). Le mecanisme
#   (compteur sur l'identite, seconde jauge de vie) est deja documente dans le DOCSTRING de `commun.
#   PoserInfection`, reutilise tel quel par `hg002`/`hg003` sans qu'aucune fiche n'ait ete requise pour ces
#   deux cartes -- aucune raison de changer la regle ici. A SIGNALER (pas a trancher seul) : si une carte
#   future conditionne un effet AU NOMBRE de compteurs infection deja poses (lecture/seuil, pas simple pose),
#   le besoin d'une fiche dediee serait a reconsiderer a ce moment-la.
# - « Stunned » : statut de regle de base (comme « Confused » sur `04120`), pas un mot-cle maison ; rendu par
#   `Faces.GiveStatus`, aucune fiche `mots-cles/` dediee (absent du README, meme traitement que `Toughness`/
#   `Restricted` cites au §5 du guide comme « bases automatiques »).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed (Alter-Ego) » -> `AbilityFactory.WhenThisRevealed("Alter-Ego", ...)`, ne se declenche QUE si
#   le joueur a qui la carte est revelee (`message.GetToPlayer()`) est en forme Alter-Ego au moment de la
#   revelation (filtrage natif de la fabrique, aucune garde `IsAlterEgo()` a ajouter a la main).
# « When Revealed (Hero) » -> meme fabrique, parametre "Hero" : branche symetrique, forme Heros.
# « Place 1 infection counter » (les DEUX branches, meme valeur « 1 ») -> `PoserInfection(effect, joueur, 1)`,
#   sur LE JOUEUR a qui la carte est revelee dans CETTE branche (jamais « chaque joueur » : contrairement a
#   `hg002`/`hg003` qui bouclent sur `Worlds.GetPlayers(effect)`, cette carte ne vise QUE le joueur resolvant,
#   le texte imprime ne dit ni « each player » ni « you » au pluriel).
# « This card gains Surge » (branche Alter-Ego SEULEMENT) -> `ThisCardGainSurge(effect)`, jamais applique a la
#   branche Hero (qui n'imprime pas cette phrase).
# « Your HERO is stunned » (branche Hero SEULEMENT) -> `Faces.GiveStatus([joueur.GetHero()], "Stunned",
#   effect)` : cible le heros du joueur, PAS son identite generique (le texte dit « your hero », pas « you »
#   nu comme le ferait un « you are stunned » -- piege deja repere sur `04120` Mind Ray qui distingue bien
#   « you are confused » (identite, branche Alter-Ego) de « you are stunned » (identite nue, branche Hero,
#   AUTRE carte que celle-ci) de « that character is stunned » (`01106`, le personnage touche par l'attaque).
#   Ici le sujet imprime est explicitement « your HERO » : `GetHero()`, pas `GetIdentity()`.
# « Your hero is stunned. Place 1 infection counter. » (ORDRE des deux phrases, branche Hero) -> le statut est
#   donne AVANT la pose du compteur, dans l'ordre d'ecriture imprime (aucun effet connu de ce scenario ne
#   depend de cet ordre precis entre ces deux actions, mais le respecter cout rien et evite toute question
#   future si un effet venait a reagir a l'un ou l'autre).
# « Place 1 infection counter. This card gains Surge. » (ORDRE, branche Alter-Ego) -> meme logique, le compteur
#   est pose AVANT le gain de Surge.
#
# ---------------------------------------------------------------------------
# BLOC NOMBRES (etape 6)
#
# - « 1 infection counter » (les deux branches) : code = `PoserInfection(effect, joueur, 1)`, parametre `n=1`
#   explicite malgre la valeur par defaut du helper (`n: int = 1`), pour que la valeur imprimee soit VISIBLE a
#   la lecture du script plutot que silencieusement implicite.
# - « gains Surge » (sans chiffre imprime) : `ThisCardGainSurge` pose toujours `GainSurge(1, ...)`, conforme a
#   la fiche [[surge]] (« Surge. » nu = 1 pioche supplementaire ; un chiffre imprime explicite comme « Surge 2 »
#   n'est pas le cas ici).
#
# A CONFIRMER : aucun point laisse en suspens sur cette carte -- les deux branches sont entierement couvertes
# par des cartes de reference au mot pres (01106/04120) et des helpers deja en place dans ce pack.


def GetAbilities() -> Sequence['Ability']:

    def widows_bite_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()

        PoserInfection(effect, joueur, 1)
        ThisCardGainSurge(effect)

    def widows_bite_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()

        Faces.GiveStatus([joueur.GetHero()], "Stunned", effect)
        PoserInfection(effect, joueur, 1)

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            widows_bite_alter_ego,
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            widows_bite_hero,
        ),
    ]
