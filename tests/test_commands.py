import shlex

import pytest

from declic import group, argument, command

base_command_data = [
    (0, 'b: my string'),
    (2, 'b'),
]


@pytest.mark.parametrize('a,b', base_command_data)
def test_base_command(a, b):
    result = {}

    # define a simple command
    @command()
    @argument('-x', type=int, default=1)
    @argument('y', type=str)
    def foo(x, y):
        result['x'] = x
        result['y'] = y

    foo(shlex.split('-x "%s" "%s"' % (a, b)))

    assert result == {'x': a,
                      'y': b}


group_command_data = [
    (0, 'b: my string', False),
    (2, 'b', True),
]


@pytest.mark.parametrize('a,b, invokable', group_command_data)
def test_group_command(a, b, invokable):
    result = {}

    # define the root command (a group)
    @group(description='my description', invokable=invokable)
    @argument('--version', action='version', version='<the version>')
    def root():
        result['bar'] = 'bar'

    @root.command()
    @argument('-x', type=int, default=1)
    @argument('y', type=str)
    def foo(x, y):
        result['x'] = x
        result['y'] = y

    root(shlex.split(f'foo -x "{a}" "{b}"'))

    assert result == {'x': a,
                      'y': b}


@pytest.mark.parametrize('a,b, invokable', group_command_data)
def test_group_command_with_chain(a, b, invokable):
    if invokable:
        expected_result = {'x': a,
                           'y': b,
                           'bar': 'bar'}
    else:
        expected_result = {'x': a,
                           'y': b, }

    result = {}

    # define the root command (a group)
    @group(description='my description', invokable=invokable)
    @argument('--version', action='version', version='<the version>')
    def root():
        result['bar'] = 'bar'

    @root.command(chain=True)
    @argument('-x', type=int, default=1)
    @argument('y', type=str)
    def foo(x, y):
        result['x'] = x
        result['y'] = y

    root(shlex.split(f'foo -x "{a}" "{b}"'))

    assert result == expected_result

@pytest.mark.parametrize('a,b, invokable', group_command_data)
def test_group_command_with_chain_and_on_before(a, b, invokable):
    if invokable:
        expected_result = {'x': a,
                           'y': b,
                           'before': 'before',
                           'bar': 'bar'}
    else:
        expected_result = {'x': a,
                           'before': 'before',
                           'y': b, }

    result = {}

    # define on_before function
    def before_root():
        result['before'] = 'before'

    # define the root command (a group)
    @group(description='my description', invokable=invokable, on_before=before_root)
    @argument('--version', action='version', version='<the version>')
    def root():
        result['bar'] = 'bar'

    @root.command(chain=True)
    @argument('-x', type=int, default=1)
    @argument('y', type=str)
    def foo(x, y):
        result['x'] = x
        result['y'] = y

    root(shlex.split(f'foo -x "{a}" "{b}"'))

    assert result == expected_result