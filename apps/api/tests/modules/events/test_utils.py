from vzticket.modules.events.utils import slugify_city


def test_slugify_city():
    assert slugify_city("São Paulo") == "sao-paulo"
    assert slugify_city("Rio de Janeiro") == "rio-de-janeiro"
    assert slugify_city("Maranhão") == "maranhao"
    assert slugify_city("  Santo André  ") == "santo-andre"
