# TODO / SPEC — La campagne « Web of Deceit »

**Statut :** conçu le 2026-08-12, non planifié, non implémenté
**Origine :** demande utilisateur (dossier Google Drive partagé)
**Prérequis :** `2026-08-12-nommage-contenu-fanmade.md` (le préfixe `wd`)
**Source :** https://drive.google.com/drive/folders/1K0Q-41Aqy6tgPDMp0K6pYRKdv66IWCIN

---

## 1. Ce que contient le dossier (relevé le 12/8/2026)

**Nom : « Web of Deceit ».** Un rulebook et six sous-dossiers :

```
web-of-deceit-rulebook.pdf   8,6 Mo
Campaign - Rewards/
Campaign Setup Cards/
Heroes/
Modulars/
Other/
Scenarios/
```

C'est la structure exacte d'une campagne : récompenses, cartes de mise en place,
héros, sets modulaires, scénarios. ⚠️ **Le contenu de chaque sous-dossier n'a PAS
été inventorié** : la lecture s'est arrêtée à la liste. Premier geste du plan :
descendre dedans et compter.

Recoupement : une extension « Web of Deceit » circule sur le Workshop Steam avec
Alligator Loki, Beta Ray Bill, Doctor Octopus, Scarlet Spider/Kaine, The Lizard,
et des packs héros (Madame Web, Misty Knight, Mockingbird, Silver Sable,
Spider-Woman…). **À vérifier** : ce Drive est-il la même chose, une part, ou autre
chose ? Plusieurs de ces héros sont **déjà dans le jeu** (Madame Web = set 107,
Albert = 100). Le risque de doublon est réel et se mesure avant de coder.

## 2. Ce qui joue en notre faveur

**Le mode campagne n'a plus de dette connue** (12/8/2026, `docs/CAMPAGNES.md`).
Les huit boîtes sont jouées, les carnets se remplissent seuls, et depuis
aujourd'hui une campagne se joue à plusieurs. **Ajouter une neuvième campagne est
un travail de CONTENU, pas de moteur** — au contraire de l'aspect Determination.

Ce qui existe et se réutilise tel quel :

- `data/campagnes/<code>.json` : la définition (scénarios, champs de victoire,
  pages du livret). Modèle : `trors.json`, le mieux garni.
- `cards/pack/<code>/campaign.py` : les crochets `CampaignSetup(level)` posés sur
  le main scheme 1a. Modèle : `trors/campaign.py`.
- Le panneau de récompenses, les détecteurs, l'écriture automatique du carnet, la
  règle de défaite, la reprise : **rien à écrire**, tout se déclare en JSON.
- `tools/verifier_campagnes.py` refuse une clé de carnet que le moteur ne connaît
  pas, une `detection` inexistante, un `deck: "requis"` sans `parJoueur`.

## 3. Le nommage

Préfixe **`wd`**, selon `2026-08-12-nommage-contenu-fanmade.md` : `wd001`…
Un code de campagne `web_of_deceit` pour `data/campagnes/`.

⚠️ **Si des héros du Drive existent déjà dans le jeu**, ne PAS les redoubler : le
mécanisme `full_link` (`{"card_id": "wd051", "full_link": "32014"}`) pointe vers
une carte identique existante, sans module ni image. Il a servi pour Echo.

## 4. Les chantiers

1. **Inventorier le Drive**, sous-dossier par sous-dossier, et **lire le rulebook**
   (8,6 Mo). C'est lui qui donne l'enchaînement des scénarios, les règles de
   campagne et le contenu du carnet. Sans cette lecture, rien ne peut être conçu.
2. **Croiser avec l'existant** : quels héros, vilains et modulaires sont déjà là ?
3. **La définition de campagne** : `data/campagnes/web_of_deceit.json`, sur le
   modèle de `trors.json`.
4. **Le campaign log** : les champs de victoire, `auto` autant que possible. La
   règle acquise le 11/8 vaut ici : **aucun champ `auto` sans source**, et ce qui
   reste à saisir doit être une vraie décision du livret.
5. **Les scénarios** : `data/scenarios/*.json` + les modules de cartes.
6. **Les images** : redimensionner à l'import (voir la dette du 12/8).
7. **Les crochets** : `cards/pack/wd/campaign.py`.
8. **Les tests** : `verifier_campagnes.py`, `test_cards`, `test_generate_cards`,
   puis une vraie partie par scénario — c'est ce qui a trouvé les vrais bugs sur
   les huit boîtes précédentes.

## 5. À trancher

- **Le périmètre.** La campagne seule, ou aussi les packs héros qui l'accompagnent ?
  Ce sont deux chantiers de taille très différente.
- **Les droits.** Le site source dit ne pas détenir les droits sur le contenu
  qu'il compile. Usage strictement personnel, comme le reste du projet.
- **La campagne à plusieurs.** Elle marche depuis aujourd'hui, mais n'a jamais été
  jouée par un humain. Éprouver ça sur une campagne connue avant d'en ajouter une
  neuve serait plus sage.

## 6. Comment on saura que c'est fait

La campagne apparaît dans l'écran des campagnes, ses scénarios s'enchaînent, le
carnet se remplit tout seul entre deux scénarios, et une partie est menée de bout
en bout sur au moins le premier et le dernier scénario.
