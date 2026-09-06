import { Lib } from './lib.js';
import { Setting } from "./settings.js";
import { HoverCard } from './hover.js';
export class Scene {
    static init() {
        document.addEventListener('DOMContentLoaded', () => {
            adjustSceneScale();
        });
        window.onresize = () => {
            adjustSceneScale();
        };
        if (Setting.scene_3d) {
            Lib.loader.loadCSS("./css./marvel./scene-3d.css");
            document.body.classList.add('scene-3d');
        }
    }
}
Scene.scale = 0;
export function convertScenePosToWindowPos(sceneX, sceneY) {
    const scene = document.getElementById('scene');
    const rect = scene.getBoundingClientRect();
    const scale = Scene.scale;
    const windowX = (sceneX * scale) + rect.left;
    const windowY = (sceneY * scale) + rect.top;
    return { x: windowX, y: windowY };
}
export function getMousePositionInScene(windowX, windowY) {
    const scene = document.getElementById('scene');
    const rect = scene.getBoundingClientRect();
    const mouseX = windowX - rect.left;
    const mouseY = windowY - rect.top;
    const scale = Scene.scale;
    const sceneX = mouseX / scale;
    const sceneY = mouseY / scale;
    return { x: sceneX, y: sceneY };
}
export function adjustSceneScale() {
    const camera = document.getElementById('camera');
    const rootStyles = getComputedStyle(document.documentElement);
    const sceneWidth = parseFloat(rootStyles.getPropertyValue('--scene-width'));
    const sceneHeight = parseFloat(rootStyles.getPropertyValue('--scene-height'));
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const scaleX = viewportWidth / sceneWidth;
    const scaleY = viewportHeight / sceneHeight;
    Scene.scale = Math.min(scaleX, scaleY);
    camera.style.transform = `scale(${Scene.scale})`;
    if (Setting.scene_3d) {
        document.getElementById('scene').style.transform = `scale(1) rotateX(20deg)`;
    }
    camera.style.display = "unset";
    camera.style.left = `${(viewportWidth - (sceneWidth * Scene.scale)) / 2}px`;
    camera.style.top = `${(viewportHeight - (sceneHeight * Scene.scale)) / 2}px`;
    const x = parseInt(rootStyles.getPropertyValue('--font-size'));
    document.documentElement.style.setProperty('--font-size-out', `${x * Scene.scale}px`);
    HoverCard.updateRect();
}
//# sourceMappingURL=scene.js.map