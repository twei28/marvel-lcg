from . import *

# * Sav'rkk — sbire NEMESIS de Yondu. ELITE. SCOUNDREL.
# PV 4, MAN 1, ATQ 2, Boost 2. `desc.Nemesis` = « Yondu Udonta ».
# Upgrades cannot be removed from Sav'rkk.
# When Revealed: Summon the Sword-Gun-Arm attachment and attach it to Sav'rkk.
#
# Cartes de reference :
#  - **`ag013`** Hallucination (pack agent_13) et `nt016` Cosmic Ax (pack
#    night_thrasher) : le motif « chercher une carte du set nemesis et
#    l'attacher », `Search` puis `AttachTo2` (can_attach.py:49).
#  - `ConvoquerRencontre` (helper du set) pour le mot-cle MAISON `summon`,
#    arbitre par l'utilisateur le 03/09/2026 : deck de rencontre ET defausse.
#  - `06031` Under Surveillance / `50144` pour une interdiction continue.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Upgrades** cannot be removed from Sav'rkk » : c'est une INTERDICTION
#    CONTINUE, et elle vise le pack de plein fouet — la Yaka Arrow plantee sur
#    Sav'rkk ne peut plus repartir, donc `yd006`, `yd009`, `yd011` et `yd012`
#    perdent leur cible. Il faut tuer Sav'rkk pour recuperer la fleche.
#    ⚠ ET `yd012` Yaka Arrow porte justement une `Forced Interrupt` « when
#    attached enemy WOULD BE defeated » : elle s'echappe donc AVANT la mort,
#    ce que cette interdiction n'empeche pas. Les deux textes se repondent, et
#    c'est le sel de la carte.
#  - « summon ... **and attach it** » : directement EN JEU, pas en main. C'est
#    la difference exacte avec les trois cartes du heros, qui ecrivent
#    « and add it to your hand ». Lire le verbe qui suit `summon`.
#  - « **When Revealed** » : a la revelation, donc aussi quand `yd017` ou
#    `yd018` le convoquent et le revelent.
#  - « ELITE » : trait imprime, aucune consequence a scripter, mais il
#    interdit les cartes qui ne visent que les sbires non-Elite.
#  - PV 4 seulement : Sav'rkk est fragile, et c'est voulu — il revient par le
#    deck de rencontre, convoque par deux traitrises.


def GetAbilities() -> Sequence['Ability']:

    def pas_de_retrait(effect: 'Effect', message: 'Message.WhenCardWouldDetachFrom|Message2') -> None:
        message.SetBeInstead(effect)

    def savrkk(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        bras = ConvoquerRencontre(effect, "Sword-Gun-Arm")
        if bras is None:
            return
        bras.CastTo(CanAttach).AttachTo2(this, effect)

    return [
        # ⚠ « Upgrades cannot be removed from Sav'rkk » : la seule fenetre du
        # moteur est `WhenCardWouldAttachTo`, envoyee par `AttachTo2` AVANT le
        # detachement de l'hote precedent (can_attach.py:58-69). L'annuler
        # empeche donc bien la carte de PARTIR de Sav'rkk.
        AbilityFactory.WhenCardWouldAttachTo(
            AbilityType.NonKeyword,
            Upgrade,
            None,
            pas_de_retrait,
            conditions=[
                lambda effect, message:
                    message.upgrade is not None
                    and Hote(message.upgrade) is effect.this
                    and message.to_face is not effect.this,
            ],
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            savrkk,
        ),
    ]
