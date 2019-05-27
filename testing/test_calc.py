import calc


def test_add():
    if calc.add(1, 2) == 3:
        print('TRUE')
    else:
        print('FALSE')


def test_sub():
    if calc.sub(5, 2) == 3:
        print('TRUE')
    else:
        print('FALSE')


def test_mult():
    if calc.mult(5, 2) == 10:
        print('TRUE')
    else:
        print('FALSE')


def test_div():
    if calc.div(8, 4) == 2:
        print('TRUE')
    else:
        print('FALSE')


test_add()
test_sub()
test_mult()
test_div()