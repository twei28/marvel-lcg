from . import *

# * Silver Samurai's Katana — ATTACHEMENT nemesis (N 4/5). TECH. WEAPON.
#   ATQ+1, 2 icones de boost. UNIQUE.
# Attach to Silver Samurai. If you cannot, find Silver Samurai and put him
#   into play engaged with you with this card attached.
# Silver Samurai cannot take damage from attacks.
# Hero Action: Spend 3 resources of any type -> discard this card.
#
# CARTES DE REFERENCE
#  - `01100` Enhanced Ivory Horn / `04072` Laser Rifle / `sd020` : le triplet
#    « attacher + capacite passive + Hero Action de defausse a cout ».
#  - `AbilityFactory.AttachToFaceWhenPutIntoPlay` pour la premiere phrase, et
#    `AfterCardEnterPlay` pour le repli. ⚠ `WhenCardPutIntoPlay` N'EXISTE PAS
#    comme fabrique (le message existe, pas la fabrique) : l'ecrire leve un
#    AttributeError attrape par `test_cards`.
#  - `21082` Abjuration (pack mts) : LA SEULE AUTRE CARTE DU DEPOT qui emploie
#    `PreventAllDamageTo`, et elle passe un `CardFinder(name=...)` NU.
#
# TEXTE CONTRE CODE
#  ⚠ « IF YOU CANNOT, find Silver Samurai and PUT HIM INTO PLAY ... WITH THIS
#    CARD ATTACHED » -> le repli n'est pas un choix : il tombe quand le
#    samourai n'est pas sur la table. La katana CONVOQUE alors son porteur.
#    C'est le miroir exact de `sf012`, qui convoque la katana : les deux
#    cartes se rappellent l'une l'autre, et il faut que les deux gardes
#    (« if it is not in play » la-bas, « if you cannot » ici) soient ecrites,
#    sinon deux exemplaires arrivent.
#  ⚠⚠ ET C'EST CE COUPLE QUI A PAYE LE PIEGE DE L'ETOILE. Un nom unique
#    s'ecrit SANS le « * » : `paper.py:45-46` le retire du nom effectif, et un
#    `CardFinder(name="* Silver Samurai")` ne trouve JAMAIS RIEN, EN SILENCE.
#    Comme les deux cartes se cherchent l'une l'autre, l'etoile les tuait
#    TOUTES LES DEUX. Trouve par les cas le 06/09/2026 ; piege deja consigne
#    dans `howard_the_duck`, `ms_america` et `patriot`.
#  ⚠ « Silver Samurai cannot take damage FROM ATTACKS » -> des ATTAQUES
#    seulement. Une brulure (`sf009`), qui inflige ses degats par une Reponse
#    forcee et non par une attaque, PASSE. C'est la reponse du pack a ce
#    sbire, et c'est ce que `message.IsFromAttack()` (sender_damage.py:840)
#    distingue.
#  ⚠ LE `CardFinder` DE LA PREVENTION EST NU, SANS `card_type`. Avec
#    `card_type=Minion` la prevention ne tombait PAS et le samourai encaissait
#    comme si la katana n'existait pas — sans un mot dans le journal. Modele
#    `21082`, qui ne passe que le nom.
#  ⚠ « SILVER SAMURAI cannot take damage » et non « attached enemy » : la
#    protection nomme le personnage. En pratique la katana n'est jamais
#    ailleurs, mais on ecrit le nom, qui n'a AUCUN homonyme au depot.
#  ⚠ « Spend 3 resources of ANY TYPE » -> `Cost("3")` : les chiffres ne
#    demandent qu'un NOMBRE, les lettres imposeraient une couleur
#    (element/cost.py:35-41).


def GetAbilities() -> Sequence['Ability']:

    def convoquer_le_samourai(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        # « Attach to Silver Samurai » a-t-il reussi ? Sinon, on le convoque.
        if Hote(this) is not None:
            return
        joueur = JoueurDeCetteCarte(effect)
        if not EstJoueur(joueur):
            return
        # ⚠ `TrouverCarteDuSet` et non `Find.Find` : le samourai est dans
        # `set_aside_nemesis_sets`, que `Find` ne balaie pas.
        samourai = TrouverCarteDuSet(effect, joueur, NOM_SAMOURAI, Minion)
        if samourai is None:
            return
        samourai.PutIntoPlay(joueur, effect)
        this.AttachTo2(samourai, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_SAMOURAI),
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            convoquer_le_samourai,
        ),
        AbilityFactory.PreventAllDamageTo(
            CardFinder(name=NOM_SAMOURAI),
            conditions=[lambda effect, message: message.IsFromAttack()],
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("3")),
    ]
