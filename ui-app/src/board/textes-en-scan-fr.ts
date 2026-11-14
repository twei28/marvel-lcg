// textes-en-scan-fr.ts — le texte ANGLAIS posé sur les cartes dont le SEUL scan est français (Beast de Proust, 02/11/2026 ; sept cartes de Mystique).
// Même mécanisme que la traduction française, à l'envers : le scan français est voilé et l'anglais s'écrit dessus (TraductionPosee,
// langue 'en'). Source : le champ `text` de data/cards.json (traduit du français faute d'original), à ne pas éditer ici sans lui.
import { SCANS_FR_SEULS } from './scans-fr'

export const TEXTES_EN_SCAN_FR: Readonly<Record<string, string | undefined>> = {
  'bs001a': "<i>Ingenious Repurposing</i> — <b>Action</b>: Tuck a [[TECH]] upgrade you control under Beast's Lab → ready your hero and choose THW, ATK or DEF. Until the end of the round, your hero gets +X to the chosen stat, where X is the printed cost of this upgrade. <i>(Limit once per phase.)</i>",
  'bs001b': "<b>Setup</b>: Search for Beast's Lab and put it into play under your control.\n<i>Resourceful</i> — <b>Action</b>: Search your deck or discard pile for a resource card and add it to your hand. <i>(Limit once per phase.)</i>",
  'bs002': "Setup. Permanent.\nUpgrades tucked under this card may be played as if they were in your hand.\nIf there are more than 3 cards tucked under this card, discard cards until only 3 remain.",
  'bs003': "Beast gets +1 DEF and +4 hit points, and his basic attacks gain piercing.\n<i>\"Maybe the world isn't worth saving anymore.\" — Beast</i>",
  'bs004': "Reduce the cost of this card by 1 if you control an upgrade with the [[TECH]] trait.\n<b>Hero Interrupt</b>: When Beast uses a basic power, choose:\n• deal 1 damage to an enemy\n• remove 1 threat from a scheme\n<i>\"It doesn't work anymore, Hank!\" — Simon Williams</i>",
  'bs005': "This card enters play with 4 tracer counters on it. Reduce the cost of this card by 1 if you control an upgrade with the [[TECH]] trait.\n<b>Resource</b>: Remove 1 tracer counter from this card → generate 1 [mental] resource for a [[TECH]] card. <i>(Limit once per card.)</i>",
  'bs006': "Reduce the cost of this card by 1 if you control an upgrade with the [[TECH]] trait.\nReduce the damage Beast takes by 1.\n<i>\"You're a rock, Hank. You always have been.\" — Bobby Drake</i>",
  'bs007': "Reduce the cost of this card by 1 if you control an upgrade with the [[TECH]] trait.\nYour hand size is +1 while you are in hero form.",
  'bs008': "This card enters play with 2 psy counters on it. Reduce the cost of this card by 1 if you control an upgrade with the [[TECH]] trait.\n<b>Hero Action</b>: Remove 1 psy counter from Xavier's Cerebro and exhaust it → deal 3 damage to each enemy in play.",
  'bs009': "<b>Hero Action</b>: Exhaust Beast's Lab, then choose:\n• discard a card tucked under Beast's Lab, then ready your hero.\n• search your deck or discard pile for an upgrade with the [[TECH]] trait, then tuck it under Beast's Lab.",
  'bs010': "<b>Hero Action</b> <i>(attack)</i>: Deal 6 damage to an enemy. You may exhaust Beast's Lab and discard 1 card tucked under it. If you do, this attack gains overkill and deals X additional damage, where X is the printed cost of the discarded card.",
  'bs011': "<b>Hero Action</b> <i>(thwart)</i>: Remove 3 threat from a scheme. You may exhaust Beast's Lab and discard a card tucked under it to change to alter-ego form.\n<i>\"Rather than money or things, give me the truth.\" — Beast</i>",
  'bs012': "<b>Hero Response</b>: After you spend this card, search your deck or discard pile for an upgrade with the [[TECH]] trait and tuck it under Beast's Lab.\n<i>\"Avenger once, ...\" — Beast</i>",
  'bs013': "<b><i>Give this card to the Hank McCoy player.</i></b>\nDiscard all cards tucked under Beast's Lab, then discard Overworked. If no [[TECH]] upgrade is discarded this way, deal yourself 1 facedown encounter card, then shuffle Overworked into the encounter deck.",
  'bs014': "<i>\"Thus conscience does make cowards of us all.\" — W. Shakespeare & Black Beast</i>\n<b>When Revealed</b>: Place 1 threat on this card for each upgrade in play.",
  'bs015': "[star] Black Beast gets +X ATK, where X is the printed resource cost of the card tucked under him.\n<b>When Revealed</b>: Tuck the highest-cost [[TECH]] upgrade you control under Black Beast. If you cannot, tuck the top card of your deck under Black Beast.\n<i>(Beast's nemesis minion.)</i>",
  'bs016': "<b>When Revealed</b>: Discard a [[TECH]] upgrade you control and deal X indirect damage to your identity, where X is the printed cost of that upgrade. If no upgrade is discarded by this effect, this card gains surge.",
  'bs017': "Attach this card to Black Beast. If you cannot, attach it to the villain.\n<b>Hero Action</b>: Discard an upgrade you control → discard this attachment.",
  // Mystique (Merlin) : cartes dont le texte du scan EN beta 4.2 est périmé par la Release FR 1.1.1 (le FR prime) ou absent de l'EN (my019). Texte = champ `text` de cards.json.
  'my005a': "Shapeshift form. Permanent.\n<b>Action</b>: Exhaust Friend → ready a hero other than Mystique or an ally.\n<b>Forced Response</b>: When this card is turned faceup, flip each other shapeshift form upgrade facedown.",
  'my005b': "Shapeshift form. Permanent.\n<b>Action</b>: Exhaust Friend → ready a hero other than Mystique or an ally.\n<b>Forced Response</b>: When this card is turned faceup, flip each other shapeshift form upgrade facedown.",
  'my007': "Victory 0.\nCharacters other than Mystique cannot remove threat from Infiltration.\n<b>When Defeated</b>: Choose to deal 5 damage to an enemy or remove 3 threat from a scheme.\nWhile Infiltration is in the victory display, Mystique ignores the guard and patrol keywords.",
  'my012': "<b>Hero Interrupt</b> <i>(defense)</i>: When you would take any amount of damage, prevent 3 of that damage. If the Friend shapeshift form upgrade is faceup, ready Mystique.\n<i>\"Surprise!\"</i>",
  'my013': "<b>Hero Action</b> <i>(thwart)</i>: Remove 3 threat from a scheme. If the Civilian shapeshift form upgrade is faceup, ignore any crisis icon ([crisis]) for this thwart and remove 1 threat from each scheme.\n<i>\"Hello Raven, please tell me you didn't kill the poor soldier.\" — Destiny</i>",
  'my018': "Incite 1.\n<b>When Revealed</b>: Remove 1 [per_hero] threat from Destiny's Warning. If you cannot, Mister Sinister activates against you. If you cannot, this card gains surge.\n<i>\"Oh that woman is just the worst. Perhaps, if I can arrange her to be absent, I can...\"</i>",
  'my019': "Team-Up (Nightcrawler and Mystique). Max 1 per deck.\n<b>Hero Action</b>: Stun and confuse an enemy.\n<i>\"Friends or foes?\"</i>",
}

/** Garde : chaque carte à scan français seul a son texte anglais (testé par scans-fr.test.ts). */
export const CODES_SANS_TEXTE_EN = [...SCANS_FR_SEULS].filter((c) => !TEXTES_EN_SCAN_FR[c])
