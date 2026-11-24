from . import *

# Zombie Iron Man — METAZOMBIE (Horde deck). AVENGER. TECH. SCH 2. ATK 1. PV 11[per_hero].
# Forced Response: After Zombie Iron Man enters play, discard cards from his signature deck until an
# attachment is discarded and attach it to him. Then shuffle the discarded cards into his signature deck.
# Upgrades. Zombie Iron Man gets +1 ATK for each attachment on him.
#
# Cartes de reference :
#  - « discard ... until an attachment is discarded and attach it ... then shuffle the discarded cards into
#    his signature deck » : `commun.DefausserJusquaUneAmeliorationDuDeckSignature` (nouveau helper partage,
#    reutilisable par hg023 Hunger Protocol plus tard), adapte de `04115` Zola's Mutate
#    (`Worlds.DiscardEncounterCardsUntil` + `AttachTo2`) a un deck PRIVE (le deck signature, pas le deck de
#    rencontre) -- la defausse « jusqu'au fond » suit deja la regle generale du deck signature (page 4,
#    `commun.DefausserAuFondDuDeckSignature`).
#  - « Upgrades. ... gets +1 ATK for each attachment on him » : `AbilityFactory.ThisGainKeyword(lambda effect,
#    ui: len(effect.this.GetAttachedAttachments()), attack=1, change_on_event=OnEvent.AttachedMove(Attachment))`,
#    modele EXACT `04114` Ultimate Bio-Servant (« gets +1 ATK for each attachment on it »).
#
# ⚠ Mots-pieges :
#  - « his signature deck », PAS le deck de rencontre : `commun.DeckSignatureDe`, jamais
#    `Worlds.DiscardEncounterCardsUntil` (qui vise le deck de rencontre du scenario, pas un deck prive).
#  - deck signature SANS amelioration disponible (hors cas reel : le deck d'Iron Man, hg019-hg023, porte 4
#    UPGRADE sur 5 cartes -- seule hg023 n'en est pas une) : le helper partage ne boucle jamais plus que la
#    taille INITIALE du deck, et ne tente aucune attache si rien n'est trouve (arbitrage utilisateur du
#    27/10/2026).
#  - « Upgrades » et le nom du Forced Response sont des titres d'ambiance, pas des mots-cles officiels
#    (absents de `docs/reference/mots-cles/README.md`, aucune autre carte du moteur ne les reprend) : rien a
#    ouvrir avant de coder, le texte qui suit EST la regle complete.
#  - « for each attachment ON HIM » : TOUTES les ameliorations attachees (`GetAttachedAttachments`), pas une
#    liste filtree sur « venues de son deck signature » -- en pratique aucune amelioration etrangere ne peut
#    s'y attacher (traits UPGRADE + « Attach to Zombie Iron Man » imprime sur hg019-hg022), mais le code ne
#    filtre pas la source, comme le texte imprime ne le fait pas non plus.


def GetAbilities() -> Sequence['Ability']:

    def iron_man_entre_en_jeu(effect: 'Effect', message: 'Message.AfterCardPutIntoPlay') -> None:
        Unused(message)
        this = effect.this.CastTo(Villain)
        DefausserJusquaUneAmeliorationDuDeckSignature(effect, this)

    # ⚠ PAS `AbilityFactory.AfterCardEnterPlay` : cette fabrique n'ecoute QUE `Message.AfterCardEnterPlay`,
    # envoye par `ApplyAfterEnterPlay` (flux de la REVELATION/du retournement, `card.py:573` /
    # `face_on_event.py:390`). Un Metazombie entre en jeu par `MettreUnMetazombieEnJeu` ->
    # `carte.PutIntoPlay(joueur, effect)` (commun.py), qui envoie `WhenCardPutIntoPlay` PUIS
    # `AfterCardPutIntoPlay` (face_on_event.py:170-208) -- JAMAIS `AfterCardEnterPlay`. Aucune fabrique
    # `AbilityFactory` n'enveloppe `AfterCardPutIntoPlay` pour un usage general (seul `asset.py` l'utilise,
    # cable sur `AttachTo2`) : on construit donc l'Ability directement, modele
    # `AttachToFaceWhenPutIntoPlayInternal` (asset.py:153), condition `effect.this == message.trigger`
    # VERIFIEE EN JEU (ci-dessous), pas seulement lue dans le code.
    #
    # ⚠⚠ PIEGE DE DEBOGAGE (mesure le 27/10/2026) : `Message2.Send()` (game/message/message.py:73) englobe
    # TOUT `BroadcastMessage` dans un `try/except Exception` qui journalise via `Log.OnCrash` SANS jamais
    # remonter au script appelant -- un `assert False` pose dans l'operation d'une capacite NE FAIT PAS
    # planter `test_capacites.py` : le cas echoue juste normalement, SANS trace d'erreur, exactement comme
    # une capacite qui ne se declenche jamais. Les deux symptomes sont IDENTIQUES en surface. Pour trancher
    # entre « la capacite ne part pas » et « la capacite part mais son code plante » : relancer avec la
    # variable d'environnement `MCLCG_TRACE_CRASH=/tmp/un_fichier.log` (lue par `Log.OnCrash`,
    # `engine/log/log.py:229`), qui ecrit CHAQUE exception avalee par le moteur dans ce fichier avec sa
    # trace complete. C'est ainsi qu'a ete confirme que `AfterCardPutIntoPlay` + `effect.this ==
    # message.trigger` partent bel et bien (`this=[(84,hg008) Zombie Iron Man]` dans le fichier de trace),
    # APRES qu'un premier essai avec `AbilityFactory.AfterCardEnterPlay` ait semble silencieusement inerte.
    return [
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterCardPutIntoPlay,
            [lambda effect, message: effect.this == message.trigger],
            iron_man_entre_en_jeu,
            is_local=True,
        ),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: len(effect.this.GetAttachedAttachments()),
            attack=1,
            change_on_event=OnEvent.AttachedMove(Attachment),
        ),
    ]
