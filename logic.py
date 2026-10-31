IGNORE = {"Human face", "Human head", "Clothing", "Human body"}
PERSON = {"Man", "Woman", "Boy", "Girl", "Person"}


def describe(x1, y1, x2, y2, W, H):
    cx = (x1 + x2) / 2
    if cx < W / 3:
        side = "left"
    elif cx < 2 * W / 3:
        side = "center"
    else:
        side = "right"

    h_ratio = (y2 - y1) / H
    if h_ratio > 0.6:
        near = "very close"
    elif h_ratio > 0.35:
        near = "close"
    else:
        near = "far"

    return side, near
