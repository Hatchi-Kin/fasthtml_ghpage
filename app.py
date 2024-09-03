from fasthtml import FastHTML
from fasthtml.common import Div, H1, H2, P, Title, Main, Link, Style, A, Button, Details, Summary, Script, Img, picocss
from starlette.responses import FileResponse
import uvicorn

from repos import top_repos


picolink = (Link(rel="stylesheet", href=picocss), Style(":root { --pico-font-size: 100%; }"))
sortablejs = Script(src="https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.14.0/Sortable.min.js")

app = FastHTML(hdrs=(picolink, sortablejs), static_dir='static')


def create_repo_card(repo):
    img_element = Img(src=f"/static/{repo['preview']}", alt=f"{repo['name']} image", style="margin-top: 12px;") if 'preview' in repo else None

    return Details(
        Summary(H2(repo['name'], style="color: black;")),
        Div(
            Div(
                P(repo['description'], style="color: black;"),
                cls="div1",
                style="grid-area: 1 / 1 / 2 / 4;"
            ),
            Div(
                A(Button("Go to Repo", cls="button"), href=repo['url']),
                cls="div2",
                style="grid-area: 1 / 4 / 2 / 5; display: flex; justify-content: flex-end; align-items: center; align-self: center; margin-top: -10px;"
            ),
            cls="parent",
            style="display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: 1fr; grid-column-gap: 0px; grid-row-gap: 0px;"
        ),
        img_element,
        style=f"background-color: {repo['color']}; margin: 12px; padding: 12px; border-radius: 8px; max-width: 700px;"
    )


@app.get("/")
def home():
    all_cards = [create_repo_card(repo) for repo in top_repos]
    return Title("Hatchi-Kin's repositories"), Main(
        H1("Hatchi-Kin's selection of fresh repos !", style="margin-bottom: 20px; margin-top: 20px;"),
        Div(
            Img(src="/static/github_preview.webp", alt="Hatchi-Kin logo", style="width: 100%; height: auto;"),
            style="max-width: 700px; margin: 0 auto;"
        ),
        Div(*all_cards, id="card-container", style="margin-top: 20px;"),
        Div(
            "Load More",
            hx_get="/show-more",
            hx_trigger="click",
            hx_swap="outerHTML",
            id="load-more",
            cls="button",
            style="margin-top: 20px; cursor: pointer;"
        ),
        Script("""
            document.addEventListener('DOMContentLoaded', function() {
                // Hide cards beyond the first 5
                const cards = document.querySelectorAll('#card-container > details');
                for (let i = 5; i < cards.length; i++) {
                    cards[i].style.display = 'none';
                }

                // Initialize Sortable
                var el = document.getElementById('card-container');
                Sortable.create(el, {
                    animation: 150,
                    ghostClass: 'sortable-ghost'
                });

                // Function to show more cards
                function showMoreCards() {
                    const hiddenCards = document.querySelectorAll('#card-container > details[style*="display: none"]');
                    hiddenCards.forEach(card => card.style.display = '');
                    document.getElementById('load-more').remove();
                }

                // Attach click event to load more button
                document.getElementById('load-more').addEventListener('click', showMoreCards);
            });
        """),
        style="max-width: 800px; margin: 0 auto;"
    )


@app.get("/static/{fname}")
def static(fname: str):
    return FileResponse(f'static/{fname}')


@app.get("/favicon.ico")
def favicon():
    return FileResponse('static/favicon.ico')


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8004, reload=True)