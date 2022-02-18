from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate_queryset(request, queryset, count=6):
    page = request.GET.get('page')
    paginator = Paginator(queryset, count)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        queryset = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        queryset = paginator.page(page)

    page_range = build_page_range(paginator, page)

    return queryset, page_range


def build_page_range(paginator, page):
    left = int(page) - 2
    if left < 1:
        left = 1

    right = int(page) + 3
    if right > paginator.num_pages:
        right = paginator.num_pages

    return range(left, right + 1)


def summarize_text(text, max_length=100):
    length_total = 0
    summary_text = ''

    for word in text.split():
        summary_text += (word + ' ')
        length_total += len(word)
        if length_total > max_length:
            break

    return summary_text + '...'
