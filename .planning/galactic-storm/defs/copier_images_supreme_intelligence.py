"""Copie les scans du lot GS-8 (Supreme Intelligence, Starforce, Seeds of Corruption, Nega-Bomb) vers le depot
PRINCIPAL : original dans sauvegardes-serveur/scans-originaux/<card_id>.png, image de jeu dans
Fusion/marvel-lcg-src/assets/pics/<card_id>.png (petit cote ramene a 615 px, LANCZOS ; carte paysage :
rotation 90 degres anti-horaire avant). Une seule image par card_id (copies : la premiere suffit).
Les scans ne sont PAS versionnes. IDEMPOTENT."""
import os
import shutil
from PIL import Image

CANDIDATS = [
    "/home/oem/Desktop/Marvel LCG/docs/packs/galactic-storm/sources",
    "/home/oem/Desktop/Marvel LCG/.claude/worktrees/agent-a1a3ae99d214abd96/docs/packs/galactic-storm/sources",
]
SOURCES = next(c for c in CANDIDATS if os.path.isdir(c))
DEPOT = "/home/oem/Desktop/Marvel LCG"
ORIG = f"{DEPOT}/sauvegardes-serveur/scans-originaux"
PICS = f"{DEPOT}/Fusion/marvel-lcg-src/assets/pics"
SI = "Scenario Packs/Supreme Intelligence (Galactic Storm expansion content)"
SF = "Modular Sets/Starforce (Galactic Storm expansion content)"
SC = "Modular Sets/Seeds of Corruption (Galactic Storm expansion content)"
NB = "Modular Sets/Nega Bomb (Galactic Storm expansion content)"

MAPPING = {
    "gs195": f"z1/{SI}/Setup cards/01 supreme intelligence I.png",
    "gs196": f"z1/{SI}/Setup cards/02 supreme intelligence II.png",
    "gs197": f"z3/{SI}/Setup cards/03 supreme intelligence III.png",
    "gs198a": f"z1/{SI}/Setup cards/04 protectors of the kree empire IA.png",
    "gs198b": f"z3/{SI}/Setup cards/04 protectors of the kree empire IB.png",
    "gs199a": f"z3/{SI}/Setup cards/05 The Endless Mind IIA.png",
    "gs199b": f"z3/{SI}/Setup cards/05 The Endless Mind IIB.png",
    "gs200": f"z1/{SI}/Setup cards/06 holding tank.png",
    "gs201": f"z1/{SI}/Encounter cards/07 Genetic Augmentation.png",
    "gs202": f"z2/{SI}/Encounter cards/10 kree infantry.png",
    "gs203": f"z1/{SI}/Encounter cards/13 ren varr.png",
    "gs204": f"z1/{SI}/Encounter cards/15 Supremor.png",
    "gs205": f"z3/{SI}/Encounter cards/16 Loyalty to Supremor.png",
    "gs206": f"z2/{SI}/Encounter cards/17 selective breeding.png",
    "gs207": f"z1/{SI}/Encounter cards/18 Supremor Seed.png",
    "gs208": f"z2/{SI}/Encounter cards/21 summon reinforcements.png",
    "gs209": f"z1/{SF}/01 Cadmi M.png",
    "gs210": f"z1/{SF}/02 Doctor Minerva.png",
    "gs211": f"z3/{SF}/03 Inndig-O the Accuser.png",
    "gs212": f"z2/{SF}/04 Korath the Pursuer.png",
    "gs213": f"z1/{SF}/05 protector.png",
    "gs214": f"z1/{SF}/06 ronan.png",
    "gs215": f"z2/{SF}/07 shatterax.png",
    "gs216": f"z1/{SF}/08 ultimus.png",
    "gs217": f"z2/{SF}/09 starformation.png",
    "gs218": f"z2/{SC}/01 Manipulated Memories.png",
    "gs219": f"z2/{SC}/03 Psychic Shackles.png",
    "gs220": f"z2/{SC}/04 Mental Torture.png",
    "gs221": f"z1/{SC}/07 Whisper in the Mind.png",
    "gs222a": f"z2/{NB}/01 nega bomb.png",
    "gs222b": f"z1/{NB}/01 Detonation.png",
    "gs223": f"z2/{NB}/03 Green Interference.png",
}
PAYSAGE = {"gs198a", "gs198b", "gs199a", "gs199b", "gs205", "gs206", "gs207", "gs219", "gs222a"}

if __name__ == "__main__":
    for cid, rel in MAPPING.items():
        src = os.path.join(SOURCES, rel)
        shutil.copy(src, f"{ORIG}/{cid}.png")
        im = Image.open(src).convert("RGB")
        if cid in PAYSAGE:
            im = im.rotate(90, expand=True)
        w, h = im.size
        k = 615 / min(w, h)
        im.resize((round(w * k), round(h * k)), Image.LANCZOS).save(f"{PICS}/{cid}.png")
    print(f"{len(MAPPING)} images copiees depuis {SOURCES}")
