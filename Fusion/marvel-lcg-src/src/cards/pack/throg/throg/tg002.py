from . import *

# Airborne Amphibian — EVENEMENT, cout 2, [physical]. AERIAL. SUPERPOWER. x3.
# Hero Action: Ready Throg and Frogjolnir. You may choose a minion engaged
#   with another player and engage it to draw 1 card.
#
# ⚠ TROIS EXEMPLAIRES, identiques au pixel pres (cout, icone de ressource et
# bloc de texte compares entre les scans 1, 2 et 3 : ecart max 0). Un seul
# card_id, contrairement a `bt007a/b` Multi-Tasking dont les deux scans
# differaient par l'icone.
#
# CARTES DE REFERENCE
#  - `31009` / `an001a` : `Faces.ReadyAll`, le redressement de plusieurs
#    cartes en une passe.
#  - `br005` Star Jump : `minion.EngagePlayer(joueur, effect)`, la primitive
#    d'engagement — la meme que celle qui sert a poser un sbire convoque.
#  - `al012` Gator Aid : `joueur.MayChooseFace(candidats, effect)` pour un
#    « you MAY choose » qui peut ne rien choisir.
#
# TEXTE CONTRE CODE
#  « Ready THROG and FROGJOLNIR » -> deux cartes NOMMEES, pas « votre
#    identite ». « Throg » ne designe que la face HEROS (l'alter-ego s'appelle
#    Puddlegulp) : jouee en forme civile la carte ne redresserait rien, ce qui
#    est coherent avec « HERO Action ». Et si le marteau n'est pas en jeu, on
#    ne redresse que le heros — le texte ne conditionne rien.
#  « You MAY choose » -> optionnel de bout en bout : `MayChooseFace` rend None
#    si le joueur refuse, et la pioche ne tombe pas.
#  ⚠ « a minion engaged with ANOTHER PLAYER » -> pas « in play », pas
#    « engaged with you ». En SOLO il n'y a aucun autre joueur : la seconde
#    phrase ne fait donc JAMAIS rien, et c'est normal. Le contre-cas solo est
#    ecrit pour le prouver, plutot que de laisser croire a une panne.
#  « and engage it TO draw 1 card » -> la pioche est la CONSEQUENCE de
#    l'engagement, pas une seconde option : pas de sbire vole, pas de carte.


def GetAbilities() -> Sequence['Ability']:

    def amphibien_volant(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # « Ready Throg and Frogjolnir. »
        a_redresser: List['CardFace'] = []
        heros = HerosDuJoueur(effect)
        if heros is not None:
            a_redresser.append(heros)
        marteau = MarteauEnJeu(effect)
        if marteau is not None:
            a_redresser.append(marteau)
        if a_redresser:
            Faces.ReadyAll(a_redresser, effect)

        # « You may choose a minion engaged with another player and engage it
        #   to draw 1 card. »
        candidats: List['CardFace'] = []
        for autre in Worlds.GetPlayers(effect):
            if autre is joueur:
                continue
            for sbire in autre.GetEngagedMinions():
                if sbire is not None and sbire.card.IsOnField():
                    candidats.append(sbire)
        if not candidats:
            return

        vole = joueur.MayChooseFace(candidats, effect)
        if vole is None:
            return
        vole.CastTo(Minion).EngagePlayer(joueur, effect)
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            amphibien_volant,
        ).SetPlay(),
    ]
