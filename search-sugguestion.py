import flet as ft
import json
from search_suggestion import SearchSuggestion


def main(page: ft.Page):

    f = open("movies.js")
    data = json.load(f)
    movie_titles = []
    year_released = []

    for content in data:
        movie_titles.append(content['title'])
        year_released.append(content['year'])

        # we'll need the movie release year later on.
        # so we map corresponding movies to release years into a dictionary.
        # Note number of items in movie_titles and year_released must be equal.
    released_in = dict(zip(movie_titles, year_released))

    def user_input_changed(e):
        # clear list_element to remove previously added suggestions.
        list_element.controls.clear()

        # More about the search_suggestion package at https://pypi.org/project/search-suggestion/.
        ss = SearchSuggestion()
        ss.batch_insert(movie_titles)

        # All movie titles in the json file start with an upper case letter.
        # so we use the title() module to capitalize the first letter of the user input.
        result = ss.search(e.control.value.title())

        if e.data.isspace() or not bool(e.data) or len(result) == 0:
            search_bar.height = 44
            list_element.controls.clear()
        else:
            search_bar.height = 427
            movie_index = 0
            counter = 0

            for suggestions in result:
                if counter == 5:
                    break
                movie_tile = ft.ListTile(
                    leading=ft.Icon(name="movie", size=35, color='red'),
                    title=ft.Text(f"{result[movie_index]}"),
                    subtitle=ft.Text(f"{released_in[result[movie_index]]}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="Add to Playlist"),
                            ft.PopupMenuItem(text="Share"),
                        ],
                    ),
                )

                list_element.controls.append(movie_tile)
                movie_index += 1
                counter += 1

            # clear result to avoid new suggestions from piling on top of old suggestions.
            result.clear()
        page.update()

    list_element = ft.ListView(controls=[], )

    search_bar = ft.Container(
        bgcolor=ft.colors.BLUE_GREY_50,
        width=420,
        height=44,
        border_radius=ft.border_radius.all(0.5 * 44),
        padding=ft.padding.only(left=15, right=15),
        alignment=ft.alignment.center,
        animate=ft.animation.Animation(curve=ft.AnimationCurve.DECELERATE),
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.SEARCH,
                            disabled=True
                        ),
                        ft.TextField(
                            border=ft.InputBorder.NONE,
                            hint_text="Search...",
                            height=44,
                            on_change=user_input_changed,
                        )
                    ]
                ),
                list_element
            ]),
    )

    page.add(search_bar)
    page.horizontal_alignment = "center"
    page.update()

ft.app(target=main)
