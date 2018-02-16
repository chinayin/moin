# Copyright: 2010 MoinMoin:DiogenesAugusto
# Copyright: 2010 MoinMoin:ThomasWaldmann
# License: GNU GPL v2 (or any later version), see LICENSE.txt for details.

"""
    MoinMoin - Navibar Tests
"""


from flask import current_app as app

from MoinMoin._tests import wikiconfig
from MoinMoin.themes import ThemeSupport
from MoinMoin import themes

import pytest


class TestNaviBar(object):
    @pytest.fixture
    def cfg(self):
        class Config(wikiconfig.Config):
            interwiki_map = dict(Self='http://localhost:8080/', MoinMoin='http://moinmo.in/', )

        return Config

    @pytest.fixture
    def theme(self):
        return ThemeSupport(app.cfg)

    def test_split_navilink(self, theme):
        tests = [
            # (navilink, (href, text, interwiki)),
            ('ItemName', ('/ItemName', 'ItemName', '')),
            ('[[ItemName|LinkText]]', ('/ItemName', 'LinkText', '')),
            ('MoinMoin/ItemName', ('http://moinmo.in/ItemName', 'ItemName', 'MoinMoin')),
            ('[[MoinMoin/ItemName|LinkText]]', ('http://moinmo.in/ItemName', 'LinkText', 'MoinMoin')),
            ('[[wiki:MoinMoin/ItemName|LinkText]]', ('http://moinmo.in/ItemName', 'LinkText', 'MoinMoin')),
            ('http://example.org/', ('http://example.org/', 'http://example.org/', '')),
            ('[[http://example.org/|LinkText]]', ('http://example.org/', 'LinkText', '')),
        ]
        for navilink, expected in tests:
            result = theme.split_navilink(navilink)
            assert result == expected

    def test_location_breadcrumbs(self, theme):
        test_result = ThemeSupport.location_breadcrumbs(theme, u'some/place/test_item')
        test_segment_name_1, test_item_name_1, test_item_exists_1 = test_result[0]
        test_segment_name_2, test_item_name_2, test_item_exists_2 = test_result[1]
        test_segment_name_3, test_item_name_3, test_item_exists_3 = test_result[2]

        assert test_segment_name_1.namespace == u''
        assert test_item_name_1.namespace == u''
        assert test_segment_name_1.value == 'some'
        assert test_item_name_1.value == 'some'
        assert test_segment_name_2.value == 'place'
        assert test_item_name_2.value == 'some/place'
        assert test_segment_name_3.value == 'test_item'
        assert test_item_name_3.value == 'some/place/test_item'

        test_result = ThemeSupport.location_breadcrumbs(theme, u'users/some/place/test_item')
        test_segment_name_1, test_item_name_1, test_item_exists_1 = test_result[0]
        test_segment_name_2, test_item_name_2, test_item_exists_2 = test_result[1]
        test_segment_name_3, test_item_name_3, test_item_exists_3 = test_result[2]

        assert test_segment_name_1.namespace == u'users'
        assert test_item_name_1.namespace == u'users'
        assert test_segment_name_1.value == u'some'
        assert test_item_name_1.value == u'some'
        assert test_segment_name_2.value == u'place'
        assert test_item_name_2.value == u'some/place'
        assert test_segment_name_3.value == u'test_item'
        assert test_item_name_3.value == u'some/place/test_item'

    def test_parent_item(self, theme):
        test_result = ThemeSupport.parent_item(theme, 'moin/moin-2.0/Item')
        expected = 'moin/moin-2.0'
        assert test_result == expected, 'Expected "%(expected)s" but got "%(test_result)s"' % locals()


def test_shorten_item_name():
    test_result1 = themes.shorten_item_name(u'MoinMoin/some/value', 0)
    assert test_result1 == u'valu...lue'
    test_result2 = themes.shorten_item_name(u'MoinMoin/some/value', 5)
    assert test_result2 == 'value'
    test_result3 = themes.shorten_item_name(u'MoinMoin/some/value')
    assert test_result3 == u'MoinMoin/some/value'


def test_contenttype_to_class():
    test_result = themes.contenttype_to_class(u'MoinMoin/some/value')
    expected = u'moin-mime-MoinMoin'
    assert test_result == expected
