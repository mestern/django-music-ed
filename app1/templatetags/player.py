from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def music_player(audio_src):
    html = f"""
    
    <div class="music-player">
      <audio class="mp-audio" src="{audio_src}"></audio>
      <div class="mp-controls">
        <button class="mp-play">▶️</button>
        <input type="range" class="mp-timeline" value="0" min="0" max="100">
      </div>
      <div class="mp-time">
        <span class="mp-current">0:00</span>
        <span class="mp-total">0:00</span>
      </div>
    </div>
    """
    return mark_safe(html)
