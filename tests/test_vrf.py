from mangafire.vrf import generate_vrf


def test_bleach_volumes_vrf():
    url = "https://mangafire.to/api/titles/027/volumes"

    expected = "8sK3xtqdFdvVraPqCYjUe8g4lg"

    assert generate_vrf(url) == expected
