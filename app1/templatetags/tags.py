from django import template
from ..models import Post
from django.db.models import Sum, Count
from django.utils.safestring import mark_safe
from markdown import markdown

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

# @register.inclusion_tag('partials/trend.html')
# def player(audio_src):
#     context ={
#         'audio_src': audio_src
#     }
#     return context


@register.inclusion_tag('partials/trend.html')
def trends(count=2):
    posts = Post.published.filter(auther='1')
    context = {
        'posts': posts
    }
    return context


@register.simple_tag()
def comment_count(post_id):
    Post.published.aggregate(Count('comments'))

@register.filter('markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


