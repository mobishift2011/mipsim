def deco(fn):
    def wrapper():
        print("deco head")
        fn()

    return wrapper

@deco
def fn():
    print('body')

a = deco(fn)
a()


@deco
def fn2():
    print("body2")

fn2()