from django.shortcuts import render, get_object_or_404
from .models import Chapter


def archive(request):
    chapters = Chapter.objects.filter(is_published=True)

    return render(request, 'archive.html', {
        'chapters': chapters
    })


def chapter_detail(request, slug):
    chapter = get_object_or_404(
        Chapter,
        slug=slug,
        is_published=True
    )

    return render(request, 'chapter.html', {
        'chapter': chapter
    })