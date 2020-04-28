import shittysynth
from mathfun import Function, Add, Div, Mul, Sub, Variable, Const
import mathfun

# This assumes that the basis functions are injective onto N.
# Or, that, that the very least, |codom(basis)| >= |codom(f)|.
def projectonto(function, basisfunctions):
    print("Computing diff to " + str(function))
    inputexmaples = [[1], [2], [10], [100], [23], [32], [5]]
    basis_projections = []
    for basis in basisfunctions:
        # We want to generate a function such that
        # h(basis(x)) = function(x), so compute
        # the IO examples.
        print("Starting synthesis for " + str(basis))
        ioexamples = []
        for input in inputexmaples:
            ioexamples.append(([basis.exec(input)], function.exec(input)))

        h, h_no = shittysynth.synthesize(ioexamples)
        print("Finished synthesis!")
        print("Difference function was " + str(h) + " no " + str(h_no))

        basis_projections.append((h, h_no))

    return basis_projections


if __name__ == "__main__":
    basis_functions = [
        Function([0], Variable(0)), # ID function
        Function([0], Add(Variable(0), Const(10))), # Plus 10 function
        Function([0], Mul(Variable(0), Const(2))), # Times 2 function
        mathfun.getfunction([0], [2], 51485) # Some arbitrary function.
    ]

    addfunc = Function([0], Add(Variable(0), Const(2)))
    projections = projectonto(addfunc, basis_functions)
    print(projections)
