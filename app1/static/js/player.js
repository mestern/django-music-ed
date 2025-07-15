document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".music-player").forEach(player => {
    const audio = player.querySelector(".mp-audio");
    const playBtn = player.querySelector(".mp-play");
    const timeline = player.querySelector(".mp-timeline");
    const current = player.querySelector(".mp-current");
    const total = player.querySelector(".mp-total");

    function fmt(sec) {
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${m}:${s < 10 ? '0' : ''}${s}`;
    }

    audio.addEventListener("loadedmetadata", () => {
      timeline.max = Math.floor(audio.duration);
      total.textContent = fmt(audio.duration);
    });

    audio.addEventListener("timeupdate", () => {
      timeline.value = Math.floor(audio.currentTime);
      current.textContent = fmt(audio.currentTime);
    });

    timeline.addEventListener("input", () => {
      audio.currentTime = timeline.value;
    });

    playBtn.addEventListener("click", () => {
      if (audio.paused) {
        audio.play();
        playBtn.textContent = "⏸️";
      } else {
        audio.pause();
        playBtn.textContent = "▶️";
      }
    });
  });
});
