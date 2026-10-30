def add_item_buggy(item, order=[]):
    order.append(item); return order
def add_item(item, order=None):
    if order is None: order = []
    order.append(item); return order
print(add_item_buggy("Tea"), add_item_buggy("Vada"))
print(add_item("Tea"), add_item("Vada"))
print(add_item_buggy.__defaults__)
def bill(total, gst_rate=0.05):
    gst = total*gst_rate
    return total, gst, total+gst
print(bill(200), bill(200, gst_rate=0.18))
x="global"
def f():
    x="local"; return x
def g():
    global x; x="changed"
def outer():
    n=0
    def inner():
        nonlocal n; n+=1; return n
    return inner
print(f(), x); g(); print(x)
c=outer(); print(c(),c())
def make_order():
    order=[]
    def add(item): order.append(item); return order
    return add
o1,o2=make_order(),make_order()
print(o1("Tea"),o1("Dosa"),o2("Vada"))
o=add_item("Tea"); o2=add_item("Idli"); c3=add_item("Coffee"); print(o,o2,c3)
