import shlex

import pytest

from declic import group, argument, command

group_invokable_data = [
    (False),
    (True),
]


@pytest.mark.parametrize('invokable', group_invokable_data)
def test_invokable_group(invokable):
    expected_result = {'root': 'root'} if invokable else {}
    result = {}

    # define the root command (a group)
    @group(description='my description', invokable=invokable)
    @argument('--version', action='version', version='<the version>')
    def root():
        result['root'] = 'root'

    # mock print_help to avoid console flooding
    root.print_help = lambda : None

    root([])

    assert result == expected_result


group_on_before_data = [
    (False, False),
    (True, True),
    (False, True),
    (True, False),
]

@pytest.mark.parametrize('invokable,chain', group_on_before_data)
def test_on_before_order(invokable, chain):
    if chain:
        expected_result = ['before first', 'first',
                           'before second', 'second',
                           'before third', ]
    else:
        expected_result = ['before first', 'before second', 'before third']

    if invokable:
        expected_result.append('third')

    result = []

    # define the root command (a group)
    @group(description='my description', invokable=True, on_before=lambda: result.append('before first'))
    @argument('--version', action='version', version='<the version>')
    def first():
        result.append('first')

    # define a second group
    @first.group(invokable=True, on_before=lambda: result.append('before second'))
    def second():
        result.append('second')

    # and a third one
    @second.group(invokable=invokable, chain=chain, on_before=lambda: result.append('before third'))
    def third():
        result.append('third')

    # mock print_help to avoid console flooding
    third.print_help = lambda : None

    first(shlex.split('second third'))

    assert result == expected_result