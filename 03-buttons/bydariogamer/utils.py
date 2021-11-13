from functools import lru_cache
from pathlib import Path

import pygame

from wclib.constants import SIZE, ROOT_DIR

__all__ = [
    "SIZE",
    "SUBMISSION_DIR",
    "ASSETS",
    "SCREEN",
    "load_image",
    "text",
    "blit_centered",
    "ninepatch",
]

SUBMISSION_DIR = Path(__file__).parent
ASSETS = SUBMISSION_DIR.parent / "assets"
SCREEN = pygame.Rect(0, 0, *SIZE)


@lru_cache()
def load_image(name: str, scale=1, alpha=True, base: Path = ASSETS):
    """Load an image from the global assets folder given its name.

    If [base] is given, load a n image from this folder instead.
    For instance you can pass SUBMISSION_DIR to load an image from your own directory.

    If [scale] is not one, scales the images in both directions by the given factor.

    The function automatically calls convert_alpha() but if transparency is not needed,
    one can set [alpha] to False to .convert() the image instead.

    The results are cached, so this function returns the same surface every time it
    is called with the same arguments. If you want to modify the returned surface,
    .copy() it first.
    """

    image = pygame.image.load(base / f"{name}.png")
    if scale != 1:
        new_size = int(image.get_width() * scale), int(image.get_height() * scale)
        image = pygame.transform.scale(image, new_size)

    if alpha:
        return image.convert_alpha()
    else:
        return image.convert()


@lru_cache()
def font(size=20, name=None):
    """
    Load a font from its name in the wclib/assets folder.

    If a Path object is given as the name, this path will be used instead.
    This way, you can use custom fonts that are inside your own folder.
    Results are cached.
    """

    name = name or "regular"
    if isinstance(name, Path):
        path = name
    else:
        path = ROOT_DIR / "wclib" / "assets" / (name + ".ttf")
    return pygame.font.Font(path, size)


@lru_cache(5000)
def text(txt, color, size=20, font_name=None):
    """Render a text on a surface. Results are cached."""
    return font(size, font_name).render(str(txt), True, color)


def blit_centered(screen, surface, rect):
    screen.blit(surface, surface.get_rect(center=rect.center))


@lru_cache(100)
def ninepatch(surface: pygame.Surface, rect: tuple):
    rect = pygame.Rect(rect)
    result = pygame.Surface(rect.size, pygame.SRCALPHA)
    subsurf_w = surface.get_width() // 3
    subsurf_h = surface.get_height() // 3
    a1 = surface.subsurface(0, 0, subsurf_w, subsurf_h)
    a2 = surface.subsurface(subsurf_w, 0, subsurf_w, subsurf_h)
    a3 = surface.subsurface(2 * subsurf_w, 0, subsurf_w, subsurf_h)
    b1 = surface.subsurface(0, subsurf_h, subsurf_w, subsurf_h)
    b2 = surface.subsurface(subsurf_w, subsurf_h, subsurf_w, subsurf_h)
    b3 = surface.subsurface(2 * subsurf_w, subsurf_h, subsurf_w, subsurf_h)
    c1 = surface.subsurface(0, 2 * subsurf_h, subsurf_w, subsurf_h)
    c2 = surface.subsurface(subsurf_w, 2 * subsurf_h, subsurf_w, subsurf_h)
    c3 = surface.subsurface(2 * subsurf_w, 2 * subsurf_h, subsurf_w, subsurf_h)

    result.blit(a1, (0, 0))
    result.blit(pygame.transform.scale(a2, (rect.w - 2 * subsurf_w, subsurf_h)), (subsurf_w, 0))
    result.blit(a3, (rect.w - subsurf_w, 0))
    result.blit(pygame.transform.scale(b1, (subsurf_w, rect.h - 2 * subsurf_h)), (0, subsurf_h))
    result.blit(
        pygame.transform.scale(b2, (rect.w - 2 * subsurf_w, rect.h - 2 * subsurf_h)),
        (subsurf_w, subsurf_h),
    )
    result.blit(
        pygame.transform.scale(b3, (subsurf_w, rect.h - 2 * subsurf_h)),
        (rect.w - subsurf_w, subsurf_h),
    )
    result.blit(c1, (0, rect.h - subsurf_h))
    result.blit(
        pygame.transform.scale(c2, (rect.w - 2 * subsurf_w, subsurf_h)),
        (subsurf_w, rect.h - subsurf_h),
    )
    result.blit(c3, (rect.w - subsurf_w, rect.h - subsurf_h))

    return result
