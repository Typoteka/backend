from rest_framework.exceptions import NotFound


def get_or_404(class_, pk):
    try:
        obj = class_.objects.get(pk=pk)
    except class_.DoesNotExist:
        raise NotFound(
            detail=f'{class_.__name__} with id {pk} does not exist',
            code=404
        )

    return obj
