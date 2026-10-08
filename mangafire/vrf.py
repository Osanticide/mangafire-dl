import base64


# Dados usados pelo algoritmo de proteção do MangaFire.
STAGE_DATA = [
    {
        "table": (
            "yINlmUNho8VYJT+ibTIP+9ESiULpVEtMOoD6U6lRE0R/xwXo/Xp9NrUgC4cw/"
            "Lmo33vUyjUE40kUoEWIr/fxfNNcq2s79ShQ5NhNrFnJ4hXPwOu/SuXzIbuTQKG"
            "Fvfm08E9jvCfqAtoDqvQq3dVWPQFmJjgvkISBeXY3BgANR+yVnjGbcxZ47d6k"
            "LNfZPIayTq3/YGySb1KuVZodWp/WGNAO5pfMcpaK53Hhs0allBszaMaxuouOwd"
            "xbwgxIw6YunSsXjI05Yi0j9j4eHKfSXR8Ifo/Od+8iamRfCXTyvm7NGRGYdcQ"
            "0ywcK/u6RXhrbcCm4t2eCtrDgQVecJGkQ+A=="
        ),
        "key": "0Ec58JOY3uBzJK9m3zqIOpdlF7UFiax9DmA=",
        "iv": 0x5A,
    },
    {
        "table": (
            "IUFltCxD3Oc2cwCgkJffthaOg9cgPUb0LgW6H/VtfcF0kc5F25t+aWj6JH9V"
            "OhOaY0rAFdUxlDnl5BLNvwEJvQtP5qcw7vdb/K+chnbwnspSHT8mz5lqwz41T"
            "ezG0hkO06FTjJZhsyNuFLDpD2ZZxQj/QIRcF90zpmQ7Byu483WsQqUE0C342H"
            "L+JXngRB6fRzxRyVTaKu83h7UYTJ0QMt6ixFh6S3F8gqkKwrGTL3jHNBsD45U"
            "nifK8+RGtishQV2K3rujLKEkiZxpr2dYcudFW4oFsDKhad3CLBvuyTqsCo4B7m"
            "L5IKQ1vXo/MOOvq1I1d8ar9X6Ttu5KF4fZgiA=="
        ),
        "key": "AAdjb1iPY8CiDmq9H34tKTBF8a3oDQ==",
        "iv": 0x35,
    },
    {
        "table": (
            "NQHlu1/wVO5EmkwQymF810qqY2xG1k2obcas4Z9mCsPEIFl9pRIjFxbJ7ybM"
            "HbBckT5Ton85E0FOeHezbh/mjlEYpmpnlXOS8dgrqeq2KfxImTh1YK9y0PeMN"
            "hzA1OQzSY9brYOJq/l2QnE/hwOeZIhPixVSKIUlDb5vLcH6RWKxkIEMuP0bDw"
            "IqQ71AJJaEaMJL7A6YtyIwoRT+L5v4aZzodN/0+3nOGsfblFjgxSfPzVDjNFe"
            "Nl5P26+kEC/8AHgdrpAbt3hHz3HrRN1Y6e+JHgF7ncFWnoF0y3THL1S71WgWG"
            "Ca6KtSzTCCG58n68nTyj2T3Sshk7utqCtMi/ZQ=="
        ),
        "key": "DELOJgPsVaCcblDtTGMdHzM=",
        "iv": 0xBA,
    },
]


STAGES = [
    {
        "table": base64.b64decode(stage["table"]),
        "key": base64.b64decode(stage["key"]),
        "iv": stage["iv"],
    }
    for stage in STAGE_DATA
]


def _encrypt_stage(
    data: bytes,
    table: bytes,
    key: bytes,
    iv: int,
) -> bytes:
    """Aplica uma etapa da transformação VRF do MangaFire."""
    output = bytearray(len(data))
    previous = iv

    for index, byte in enumerate(data):
        previous = table[byte ^ key[index % len(key)] ^ previous]
        output[index] = previous

    return bytes(output)


def generate_vrf(url: str) -> str:
    """
    Gera o token VRF utilizado pela API do MangaFire.

    A URL deve ser a URL completa da requisição da API.
    """

    from urllib.parse import parse_qsl, urlencode, urlsplit

    parsed = urlsplit(url)

    # O JavaScript do HaruNeko ordena os parâmetros antes
    # de calcular o VRF.
    query = urlencode(sorted(parse_qsl(parsed.query)))

    # Remove /api/ do início do caminho.
    path = parsed.path

    if path.startswith("/api/"):
        path = path[5:]

    data = f"/{path}".encode("utf-8")

    if query:
        data += f"?{query}".encode("utf-8")

    for stage in STAGES:
        data = _encrypt_stage(
            data,
            stage["table"],
            stage["key"],
            stage["iv"],
        )

    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")
