from declic import group, argument, command

# on_before callbacks are executed if:
# - the group itself is called
# - if any of the child of the group is called
def before_bar():
    print('before bar')

def before_sub(tata):
    print('before sub: %s' % tata)

# define the root command (a group)
@group(description='my description', on_before=before_bar)
@argument('--version', action='version', version='<the version>')
@argument('--foo', type=int, default=1)
def bar():
    print('bar')

# define a sub-group
@bar.group(invokable=True, on_before=before_sub)
@argument('--toto', type=int, default=2)
@argument('--tata', type=str, default='aaa')
def sub(toto, tata):
    print('toto: %s' % toto)
    print('tata: %s' % tata)

# define a sub-command of the sub-group
# chain option allows to execute each parent group (if they are invokable) before the command call
# each on_before functions will be executed anyway
@sub.command(chain=True)
def mop(toto, **kwargs):
    print('kwargs: %s' % kwargs)
    print('toto: %s' % toto)

# define a sub-command of the root group
@bar.command()
@argument('-x', type=int, default=1)
@argument('y', type=float)
def foo(x, y):
    print(x, y)


if __name__ == '__main__':
    import sys

    bar(sys.argv[1:])
    # or bar()