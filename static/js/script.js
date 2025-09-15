document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;

    // Function to spawn hearts floating downward
    function spawnHeart() {
        const heart = document.createElement('div');
        heart.className = 'heart-fall';
        heart.style.left = `${Math.random() * 100}%`;
        heart.style.fontSize = `${Math.random() * 20 + 20}px`;  // between ~20px-40px
        heart.textContent = '💖';

        body.appendChild(heart);

        // remove after animation ends
        setTimeout(() => {
            heart.remove();
        }, 7000);  // matches animation duration
    }

    // create initial hearts
    for (let i = 0; i < 8; i++) {
        spawnHeart();
    }

    // spawn more hearts periodically
    setInterval(spawnHeart, 1500);
});
