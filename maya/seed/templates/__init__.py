"""Bar type templates for the seed generator."""

from maya.seed.templates.dive_bar import DiveBarTemplate
from maya.seed.templates.cocktail_lounge import CocktailLoungeTemplate
from maya.seed.templates.sports_bar import SportsBarTemplate
from maya.seed.templates.wine_bar import WineBarTemplate

TEMPLATES = {
    "dive-bar": DiveBarTemplate,
    "cocktail-lounge": CocktailLoungeTemplate,
    "sports-bar": SportsBarTemplate,
    "wine-bar": WineBarTemplate,
}
