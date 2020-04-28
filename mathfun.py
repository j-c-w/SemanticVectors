import random

class Context(object):
    def __init__(self, input_names, input_values):
        dict = {}
        for i in range(len(input_names)):
            dict[input_names[i]] = input_values[i]

        self.context = dict

    def lookup(self, name):
        if name in self.context:
            return self.context[name]
        else:
            raise Exception("No defined identifier " + str(name))


class Mathop(object):
    pass

class Add(Mathop):
    def __init__(self, inp1, inp2):
        self.inp1 = inp1
        self.inp2 = inp2

    def exec(self, context):
        return self.inp1.exec(context) + self.inp2.exec(context)

    def __str__(self):
        return '(' + str(self.inp1) + ' + ' + str(self.inp2) + ')'

class Const(Mathop):
    def __init__(self, value):
        self.value = value

    def exec(self, context):
        return self.value

    def __str__(self):
        return 'c' + str(self.value)

class Sub(Mathop):
    def __init__(self, inp1, inp2):
        self.inp1 = inp1
        self.inp2 = inp2

    def exec(self, context):
        return self.inp1.exec(context) - self.inp2.exec(context)

    def __str__(self):
        return '(' + str(self.inp1) + ' - ' + str(self.inp2) + ')'

class Div(Mathop):
    def __init__(self, inp1, inp2):
        self.inp1 = inp1
        self.inp2 = inp2

    def exec(self, context):
        return self.inp1.exec(context) // self.inp2.exec(context)

    def __str__(self):
        return '(' + str(self.inp1) + ' // ' + str(self.inp2) + ')'

class Mul(Mathop):
    def __init__(self, inp1, inp2):
        self.inp1 = inp1
        self.inp2 = inp2

    def exec(self, context):
        return self.inp1.exec(context) * self.inp2.exec(context)

    def __str__(self):
        return '(' + str(self.inp1) + ' * ' + str(self.inp2) + ')'

class Variable(Mathop):
    def __init__(self, name):
        self.name = name

    def exec(self, context):
        return context.lookup(self.name)

    def __str__(self):
        return 'v' + str(self.name)

class Function(object):
    def __init__(self, inputs, operation):
        self.inputs = inputs
        self.operation = operation

    def exec(self, input):
        assert(len(input) == len(self.inputs))

        return self.operation.exec(Context(self.inputs, input))

    def __str__(self):
        return '(' + ', '.join(['v' + str(inp) for inp in self.inputs]) + ') -> ' + str(self.operation)

def fromname(name, args):
    if name == 'Mul':
        return Mul(args[0], args[1])
    if name == 'Div':
        return Div(args[0], args[1])
    if name == 'Add':
        return Add(args[0], args[1])
    if name == 'Sub':
        return Sub(args[0], args[1])
    if name == 'Variable':
        return Variable(args[0])
    if name == 'Const':
        return Const(args[0])

class SkeletonTree(object):
    def __init__(self):
        self.operations = []
        self.freelist = []

    # Return the number of available leaves.  If the tree is
    # empty, we say it has a single available leaf.
    def available_leaf_count(self):
        if len(self.operations) == 0:
            return 1
        return len(self.freelist)

    def add_leaf_deterministic(self, opname, value):
        if len(self.freelist) == 0:
            assert len(self.operations) == 0
            newindex = 0
        else:
            (replacenode_index, replacenode_argno) = self.freelist[0]
            del self.freelist[0]

            newindex = len(self.operations)
            self.operations[replacenode_index][replacenode_argno] = newindex

        self.operations.append([opname, value])

    def add_node_deterministic(self, opname, noargs, is_reversed=False):
        if len(self.freelist) == 0:
            assert len(self.operations) == 0
            newindex = 0
        else:
            (replacenode_index, replacenode_argno) = self.freelist[0]
            del self.freelist[0]

            newindex = len(self.operations)
            self.operations[replacenode_index][replacenode_argno] = newindex

        self.operations.append([opname] + ([None] * noargs))

        if is_reversed:
            argsrange = range(noargs - 1, -1, -1)
        else:
            argsrange = range(noargs)

        for i in argsrange:
            self.freelist.append((newindex, i + 1))

    def add(self, opname, numargs):
        # Get the index to replace
        if len(self.freelist) == 0:
            assert len(self.operations) == 0 # adding a node to a tree without space
            # We don't have to manage the freelist because this
            # node becomes the head node in the tree.
            newindex = 0
        else:
            index = random.randint(0, len(self.freelist) - 1)
            (replacenode_index, replacenode_argno) = self.freelist[index]
            del self.freelist[index]

            # Replace it with an index to the new tree element.
            newindex = len(self.operations)
            self.operations[replacenode_index][replacenode_argno] = newindex

        # Append the new tree element.
        self.operations.append([opname] + ([None] * numargs))

        # Add any new leaves to the free list.
        for i in range(numargs):
            self.freelist.append((newindex, i + 1))

    def fillleaves(self, leaves):
        for (index, argno) in self.freelist:
            newitem = len(self.operations)
            self.operations[index][argno] = newitem
            self.operations.append([random.choice(leaves)])
        self.freelist = []

    def build(self, vars, consts):
        def recursivebuild(index):
            elements = self.operations[index]
            if elements[0] == 'Variable':
                if len(elements) > 1:
                    return Variable(elements[1])
                else:
                    return Variable(random.choice(vars))
            if elements[0] == 'Const':
                if len(elements) > 1:
                    return Const(elements[1])
                else:
                    return Const(random.choice(consts))

            args = []
            # Build all the arguments for this constructor item.
            for elem in elements[1:]:
                subelem = recursivebuild(elem)
                args.append(subelem)

            return fromname(elements[0], args)

        return recursivebuild(0)

def getfunction(args, consts, functionnumber):
    expression = getexpr(args, consts, functionnumber)

    return Function(args, expression)

def getexpr(varnames, consts, functionnumber):
    noconsts = len(consts)
    noargs = len(varnames)
    operations = ['Mul', 'Div', 'Add', 'Sub']
    leaves = ['Variable', 'Const']

    leaf_options = noconsts + noargs

    builder = SkeletonTree()

    # Keep building the tree until it gets big enough that we won't
    # be able to do all permutations of variables if we build
    # any more.  Each operation adds a single element to each
    # leaf.
    while functionnumber // 8 > leaf_options ** (builder.available_leaf_count() + 1):
        decision = functionnumber % 8 # Two for each of add div mul sub -- one each way around.
        functionnumber = functionnumber // 8

        operation_index = decision // 2 - 1
        is_reversed = decision % 2

        builder.add_node_deterministic(operations[operation_index], 2,
                                       is_reversed=is_reversed)

    # Now, go through and fill up the leaves with variables:
    while builder.available_leaf_count() > 0:
        modnumber = noargs + noconsts
        decision = functionnumber % modnumber
        functionnumber = functionnumber // modnumber
        
        if decision < noargs:
            builder.add_leaf_deterministic('Variable', varnames[decision])
        else:
            builder.add_leaf_deterministic('Const', consts[decision - noargs])

        # If this hits 0 but we are going around the loop
        # again, there wasn't enough number left to cover
        # all the leaf options.
        assert functionnumber > 0 or builder.available_leaf_count() == 0

    # All vars and consts should already be set.
    return builder.build(None, None)


def generate(num_variables, num_nodes):
    constants = range(0, 2)
    varnames = range(0, num_variables)
    operations = ['Mul', 'Div', 'Add', 'Sub']
    leaves = ['Variable', 'Const']

    builder = SkeletonTree()

    while num_nodes > 0:
        builder.add(random.choice(operations), 2)
        num_nodes -= 1

    builder.fillleaves(leaves)

    return builder.build(varnames, constants)


if __name__ == "__main__":
    print(generate(2, 10))
    print(getexpr([0, 1], [2], 1512))
    print(getexpr([0, 1], [2], 15121010101))
    print(getexpr([0, 1], [2], 15173832))
    print(getexpr([0, 1], [2], 1))
    print(getexpr([0, 1], [2], 0))
