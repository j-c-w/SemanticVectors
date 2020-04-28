import argparse
import projection
import mathfun

if __name__ == "__main__":
    parser = argparse.ArgumentParser('A simple interface to test the math projection functions')
    parser.add_argument('--test', type=int, nargs=1, action='append', help='Function number to test (by number --- see mathfun.getfunction)', default=[])
    parser.add_argument('--basis', type=int, nargs=1, action='append', help='Add a basis function (by number --- see mathfun.getfunction)', default=[])
    moduleargs = parser.parse_args()
    # Create some basis functions with a single argument
    # and two constants.
    args = [0]
    consts = [2, 3]

    function_numbers = [100000, # v0 // 3 - v0 * 2
            10000, # 2 * 3 - v0
            100, # v0 / 2
            10000001, # v0 * 2 - (v0 ** v0 - 3
            10000272, # (v0 * v0 * 3) - (v0 + 2)
            1, # 2 (const)
            3, # v0 (id function)
            1015 # v0 + v0
            ] + moduleargs.basis

    basis_functions = []
    for num in function_numbers:
        basis_functions.append(mathfun.getfunction(args, consts, num))


    if moduleargs.test:
        for funno in moduleargs.test:
            function = mathfun.getfunction(args, consts, num)
            results = projection.projectonto(function, basis_functions)

            print("Vector for function " + str(function) + " is: ")
            for i in range(len(results)):
                print(str(basis_functions[i]), end='')
                print(': ' + str(results[i][0]))
    else:
        # Compute the distance of all the basis functions to each other.
        for function in basis_functions:
            results = projection.projectonto(function, basis_functions)

            print("Vector for function " + str(function) + " is: ")
            for i in range(len(results)):
                print(str(basis_functions[i]), end='')
                print(': ' + str(results[i][0]))
