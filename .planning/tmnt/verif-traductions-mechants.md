# Vérification des traductions : lot « mechants »

Branche `verif-trad-mechants`. Fichier corrigé : `ui-app/src/board/textes-fr-fanmade.ts` (seul fichier touché).
Lot : Shredder (ts), Bebop & Rocksteady (tk), Baxter Stockman (tx), ensembles TMNT Standard/Expert (te).

## Chiffres

- 106 cartes dans le lot. 98 relues face à leur français ; 8 n'ont AUCUN français (voir plus bas).
- 33 cartes corrigées (détail ci-dessous), 65 laissées telles quelles.
- Le « fr = null » du fichier d'extraction était un artefact : 16 des 24 cartes ont bien un français dans `textes-fr-fanmade.ts`, écrit entre apostrophes simples (l'extraction ne lisait que les guillemets doubles). Les 8 restantes sont réellement absentes.
- Test : `traduction-public`, `textes-fr-fanmade`, `vocabulaire-statuts`, `shredder-plateau`, `tmnt-baxter-plateau`, `tmnt-bebop-plateau` passent (les fichiers générés ont été régénérés pour le test puis remis à l'état du dépôt, non commités).

## Références officielles utilisées

`textes-fr-complets.ts` : « gagne Garde / Perçant / Déferlement / Renfort / Solide » (initiale majuscule, 13/34/71/203/9 occurrences), « phase du Méchant » (47) mais « le méchant » (213 contre 2) pour le méchant lui-même, « personnage ami » (56), « attribuez(-vous) … carte Rencontre face cachée » (« distribuez » : 0), « n'importe quelle quantité de dégâts » (102), « est censé être vaincu », « (alter ego) » / « (héros) » en minuscules, « Si ce stade est achevé » (36), « Némésis » avec majuscule, « les sets de rencontre X et Standard », « à la place en mode expert », « choisissez une option : ». Carte officielle jumelle de te005 : 01190 (Shadow of the Past).

## Corrections (id, nom, avant, après, raison)

Les corrections de forme répétées sont regroupées par motif.

### Motif A : « phase du Méchant » avec majuscule (nom de phase)
- tk001a, tk002a, tk003a, tk004a (Bebop / Rocksteady), tk006a (Destructive Dunderheads) : « phase du méchant » devient « phase du Méchant ». Raison : usage officiel et cohérence avec ts/tx.

### Motif B : « le méchant » (la carte) en minuscule
- ts010 Foot Ninja, ts101 Karai, ts204 Koya (deux fois), te006 Skulk, te101 Annihilation (deux fois) : « camouflez le Méchant », « soignez 2 dégâts du Méchant », « le Méchant vous attaque » deviennent « … le méchant / du méchant ». Raison : l'officiel écrit « le méchant » ; seul le nom de la phase prend la majuscule. Aligne aussi sur tk (qui l'avait déjà).

### Motif C : mots-clés après « gagne / gagnent » avec majuscule
- tk009 Shutter Shades, tk010 Aviator Cap, tk011 Roberta, tk012 Juniper : « gagne renfort », « gagnent perçant », « gagnent déferlement » deviennent « gagne Renfort », « gagnent Perçant », « gagnent Déferlement ».
- tx003 Baxter Stockman (III) : « gagne garde » devient « gagne Garde ».
- tx006 Swarm Superiority : « gagne [[AERIAL]] et garde » devient « … et Garde ».
Raison : usage officiel (initiale majuscule), cohérence avec ts201/ts205/ts102/te101 déjà en majuscule.

### Corrections individuelles
- tx003 Baxter Stockman (III) : « distribuez 1 carte Rencontre face cachée à chaque joueur » devient « attribuez 1 carte Rencontre face cachée à chaque joueur ». Raison : le verbe officiel de « deal » est « attribuez » ; le reste du pack l'emploie (tk028, ts101, ts201…).
- tx004b Baxter's Laboratory (1B) : « distribuez-vous 1 carte Rencontre face cachée » devient « attribuez-vous 1 carte Rencontre face cachée ». Même raison.
- tx004a Baxter's Laboratory (1A) : « <b>Contenu :</b> » devient « <b>Contenu</b> : » (balise et espace avant le deux-points comme partout ailleurs) ; « Sets Baxter's Lab, Cyber Swarm et Standard. Deux sets de rencontre modulaires » devient « Les sets de rencontre Baxter's Lab, Cyber Swarm et Standard. Deux sets de rencontre modulaires » ; « (Baxter Stockman (II) et Baxter (III) en mode expert.) » devient « … à la place en mode expert.) ». Raison : formule officielle des manigances principales.
- tk005a Demolition Crew (1A) : « Ensembles Bebop & Rocksteady, Concrete Jungle et Standard. Un ensemble Rencontre modulaire » devient « Les sets de rencontre Bebop & Rocksteady, Concrete Jungle et Standard. Un set de rencontre modulaire » ; « en mode expert » devient « à la place en mode expert ». Raison : formule officielle (« set » est le terme officiel pour encounter set ; la fiche mélangeait « Ensembles » et « Sets »).
- ts004a Clan of Shadows (1A) : « Ensembles Shredder, Shadow of the Foot et Standard. Deux ensembles de rencontre modulaires » devient « Les sets de rencontre Shredder, Shadow of the Foot et Standard. Deux sets de rencontre modulaires » ; « en mode expert » devient « à la place en mode expert ». Même raison.
- te201 Intense Combatants : « Ensembles TMNT Standard et Expert uniquement » devient « Sets TMNT Standard et Expert uniquement ». Même raison.
- tx007 Plague of M.O.U.S.E.R.S., tx012 Flight of Flyborgs : « quand ce sbire subit des dégâts » devient « quand ce sbire subit n'importe quelle quantité de dégâts ». Raison : « any amount of damage » était perdu ; tournure officielle.
- tx013 Superfly : « La MNG et l'ATQ de ce sbire sont égales » devient « … sont égaux ». Raison : accord (masculin l'emporte avec un féminin et un masculin).
- tx005 Baxter Blaster, tx016 Wrapped Up : « un personnage allié » devient « un personnage ami ». Raison : « friendly character » = « personnage ami » (« allié » traduit « ally »).
- tx017 Auto Defense Bots : « quand ce sbire va être vaincu » devient « quand ce sbire est censé être vaincu ». Raison : « would be defeated » = « est censé être vaincu » (officiel, 26 occurrences) ; « va être » n'existe pas dans l'officiel.
- ts004b Clan of Shadows (1B) : « après qu'un sbire [[FOOT CLAN]] a été vaincu » devient « … est vaincu ». Raison : « is defeated » au présent, comme tk106 et le reste des Réponses.
- ts005b Shredder's Wrath (2B) : « Si cette manigance est accomplie » devient « … est achevée ». Raison : officiel « achevé » (36 occurrences), et tx004b dit déjà « achevée ».
- ts015 Disarming Assault : « Si cette attaque inflige des dégâts à votre identité » devient « Si cette attaque vous inflige des dégâts ». Raison : l'anglais dit « to you », pas « to your identity ».
- ts017 Shred : « (Alter ego) » / « (Héros) » deviennent « (alter ego) » / « (héros) ». Raison : usage officiel et cohérence avec tk022/tk026.
- tk203 Jägerbombs : « choisissez un : » devient « choisissez une option : ». Raison : « Choose one: » (officiel) ; « un : » sans nom est incorrect.
- te004 Pursued by Shadows, te102 Haunted by the Past, te103 Sinister Plan : « némésis » devient « Némésis » (sbire, manigance annexe). Raison : l'officiel met la majuscule (« sbire Némésis », « set de rencontre Némésis »).
- te005 Shadow of the Past : « némésis » devient « Némésis » (quatre fois) ; « le reste de votre ensemble de rencontre némésis mis de côté » devient « … set de rencontre Némésis … » ; « n'entre pas en jeu ainsi » devient « n'entre pas en jeu à cause de cet effet ». Raison : le texte anglais est identique à l'officielle 01190, dont le français a été repris pour ces termes.

## Cartes sans français (8) : proposition, rien n'a été écrit dans le fichier

Aucune entrée dans `textes-fr-fanmade.ts`, ni dans une autre structure (recherche faite sur tous les fichiers de textes ; la fiche `tmnt_standard_reskin.json` / `tmnt_expert_reskin.json` ne porte que l'anglais). Ce sont des copies « reskin » de cartes officielles Standard/Expert (01186 à 01193) avec une citation en plus. Le français officiel existe donc dans `textes-fr-complets.ts` ; ma proposition (officiel + citation, à valider) :

- te021 Advance (officielle 01186) : « <b>Une fois révélée</b> : le méchant manigance.\n<i>« Le monde sera à moi. »</i> —Krang »
- te023 Assault (01187) : « <b>Une fois révélée (alter ego)</b> : cette carte gagne Renfort.\n<b>Une fois révélée (héros)</b> : le méchant vous attaque.\n<i>« Je me vengerai ! »</i> —Shredder »
- te025 Caught Off Guard (01188) : « <b>Une fois révélée</b> : défaussez une amélioration ou un soutien que vous contrôlez. Si aucune carte n'a été défaussée ainsi, cette carte gagne Renfort. » (l'officiel dit « n'est défaussée par cette effet », avec une faute ; la formulation de te001 est préférable)
- te026 Gang-Up (01189) : « <b>Une fois révélée (alter ego)</b> : cette carte gagne Renfort.\n<b>Une fois révélée (héros)</b> : le méchant et chaque sbire engagé avec vous vous attaquent. »
- te027 Shadow of the Past (01190, copie de te005) : même texte que te005 corrigé ci-dessus.
- te121 Exhaustion (01191) : « Renfort.\n<b>Une fois révélée</b> : inclinez votre carte Identité.\n<i>« Pourquoi si en colère, petite tortue ? »</i> —Bebop »
- te122 Masterplan (01192) : « <b>Une fois révélée</b> : placez 4 menaces sur chaque manigance annexe. S'il n'y a pas de manigance annexe en jeu, défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'une manigance annexe soit défaussée. Révélez cette manigance annexe.\n<i>« Nous devons tous jouer notre rôle. »</i> —Rat King »
- te123 Under Fire (01193) : « Renfort.\n<b>Une fois révélée</b> : révélez la carte du dessus du deck Rencontre.\n<i>« On les tient ! Ils ne peuvent pas s'échapper ! »</i> —Granitor »

Les citations sont de ma traduction, à valider. Question : ces huit cartes doivent-elles être écrites telles quelles dans `textes-fr-fanmade.ts` ? (Si le jeu les affichait via la carte officielle de même nom, vérifier que le reskin n'apparaît pas en anglais.)

## À trancher (laissé tel quel)

1. ts101 Karai : « Une fois révélée » (féminin, Karai) et « Une fois vaincu » (masculin, sbire) sur la même carte. Options : tout au féminin (« révélée / vaincue », Karai est une femme) ou tout au masculin (« révélé / vaincu », comme les autres sbires, ts010). Je n'ai pas tranché.
2. tk006a Destructive Dunderheads : « <i>Double Peine</i> » pour *Double Trouble*. « Double peine » désigne en français une sanction doublée, pas des ennuis doublés. Options : « Double problème », « Double ennui », ou laisser. Nom de capacité maison, donc à valider.
3. te201 : « plus de rebondissements » pour *additional hijinx* (« hijinx » = frasques, chahut, péripéties comiques). Options : « plus de péripéties », « plus de chahut », ou laisser.
4. tk009, tk010, tk011, tk012 : « après que Bebop passe sur sa face K.O. » pour *flips to his K.O. side*. L'officiel dit « retournez … sur sa face ». Options : « est retourné sur sa face K.O. » ou laisser (sens correct).
5. ts002 / ts003 « cherchez Bladed Armor (attachement) dans le deck Rencontre … » contre tx002 « cherchez dans le deck Rencontre … l'attachement Baxter Blaster » : deux tournures pour la même phrase anglaise. Sens identique ; harmonisation possible (je propose la forme de tx002, plus naturelle).
6. Traits (fichier `traits-fr.ts`, hors de mon périmètre d'édition) : RHINO reste « RHINO » alors que RHINOCEROS devient « RHINOCÉROS » ; TEMPER devient « HUMEUR » (le sens est plutôt « tempérament / caractère ») ; BESTIES devient « COPAINS ». À valider par l'utilisateur ; non modifié. Les autres traits du lot (ALERTE, FURIEUX, SAUVAGE, TURBULENT, PORC, PHACOCHÈRE, ESSAIM, LUNETTES DE SOLEIL, YOKAI, ARME, RELIQUE…) sont corrects.

## Coquilles de l'anglais relevées (non corrigées)

- tx004a : « <b>Content:</b> » avec le deux-points dans la balise (les autres cartes : « <b>Content</b>: »).
- tx004a : « Baxter (III) » au lieu de « Baxter Stockman (III) » (probable abréviation imprimée).
- ts006 / ts007 : l'entité HTML « &#8594; » apparaît à la place de la flèche dans le champ anglais de l'extraction (rendu écran à vérifier, le français porte bien « → »).
- tk007b / tk008b : cartes qui se renvoient « Headstrong » / « Headfirst » (noms conformes aux faces).
- tk014, tk015 : textes identiques à tk013 (trois illustrations d'une même carte), normal.
- tk005a : « Hog Wild attachment » alors que les noms des faces sont Hog Wild / Headfirst (cohérent).

## Ce que je n'ai pas pu vérifier

- Je n'ai pas ouvert les scans : l'anglais de l'extraction est pris comme exact ; aucune coquille d'impression n'a été confrontée au scan.
- La conformité des noms de compteurs de `compteurs-fr.ts` a été vérifiée seulement pour swarm (essaim), knucklehead (andouille), ooze (mutagène) ; cable et shield (câble, bouclier) cohérents avec tx015 et tx017.
- Les citations des personnages (traductions « J'ai mal à la tête ! », etc.) sont de bon français et fidèles, mais leur ton n'a pas de référence officielle.
