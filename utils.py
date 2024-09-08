import html


def escape_html(text: str):
    text = text.replace("*", "")
    return html.escape(text)
