from . import *

# Exposed — QUATRIEME CARTE D'ETAT du moteur, ajoutee pour le pack `sentinel`
# (T-Wrecks, 12/09/2026). Fiche : docs/reference/mots-cles/exposed.md.
#
# « The next time this character is attacked, discard all Exposed status cards
#   from it. That attack deals 1 additional damage for each Exposed status card
#   discarded this way. »
#
# CARTES DE REFERENCE
#  - `tough.py`, `stunned.py`, `confused.py` (meme dossier) : le gabarit d'une
#    carte d'etat — `AbilityType.Status`, cible `"AttachedCharacter"`, et
#    `effect.this.CastTo(StatusCard)` puis `GetBindFace()` pour remonter au
#    personnage qui la porte.
#  - `bl007` Bandolier of Stakes : augmenter les degats d'une attaque EN COURS
#    plutot que la statistique ATQ (`GainATKForThisAttack` n'admet que les
#    attaques de base). Ici la fenetre est `WhenUnitWouldAttackUnit`, dont la
#    methode s'appelle `IncreaseDamage` (sender_damage.py:413).
#
# TEXTE CONTRE CODE
#  ⚠ « is ATTACKED » : `WhenUnitWouldAttackUnit` avec `who_be_attacked`, pas un
#    declencheur de degats. Une carte qui blesse sans attaquer ne consomme pas
#    l'etat (fiche exposed.md, premier piege).
#  ⚠ « discard ALL Exposed status cards from it » : les cartes partent TOUTES,
#    d'un coup. Le bonus vaut le nombre reellement defausse, pas 1.
#  ⚠ CHAQUE carte Exposed porte cette capacite. Sans garde-fou, deux cartes
#    sur la meme cible se declencheraient l'une apres l'autre et ajouteraient
#    leurs bonus DEUX fois (2 + 1). On ne laisse agir que la premiere : les
#    suivantes trouvent la pile deja vide (`LoseState` a tout emporte) et
#    n'ajoutent rien.


def GetAbilities() -> Sequence['Ability']:

    def decouvrir(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(StatusCard)
        unit = this.GetBindFace()

        # Combien d'Exposed portees par CE personnage, avant de les retirer :
        # c'est le bonus de degats, et c'est aussi le garde-fou (une seconde
        # carte, declenchee apres la premiere, en trouvera zero).
        combien = unit.components.status.exposed
        if combien <= 0:
            return

        unit.LoseState("Exposed", effect, rule="All")
        message.IncreaseDamage(combien, effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.Status,
            CardFinder(),
            "AttachedCharacter",
            decouvrir,
        )
    ]
