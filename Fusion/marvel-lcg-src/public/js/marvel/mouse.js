function updatePlayerMousePosition(playerId, xPercent, yPercent) {
    const x = (xPercent / 100) * MouseSync.rect.width + MouseSync.rect.left;
    const y = (yPercent / 100) * MouseSync.rect.height + MouseSync.rect.top;
    const playerMarker = document.getElementById(`player-mouse-${playerId}`);
    if (playerMarker) {
        playerMarker.style.left = `${x}px`;
        playerMarker.style.top = `${y}px`;
        playerMarker.style.position = 'absolute';
    }
    console.log("Render", playerId, xPercent, yPercent);
}
export class MouseSync {
    static init() {
    }
    static handle(parsedMessage) {
        for (const positions of parsedMessage.mouse_position) {
            updatePlayerMousePosition(positions.player_id, positions.x, positions.y);
        }
    }
}
MouseSync.scene = document.getElementById('scene');
MouseSync.rect = MouseSync.scene.getBoundingClientRect();
MouseSync.is_init = false;
//# sourceMappingURL=mouse.js.map