import mathfun

MAX_PROGS = 10000000

# This is a program that exhaustively synthesizes programs until
# one fits all the examples.  It stops at MAX_PROGS programs.
def synthesize(ioexamples,consts=[2],progno_start=0):
    progno = progno_start

    args = range(len(ioexamples[0][0]))

    while progno < MAX_PROGS:
        function = mathfun.getfunction(args, consts, progno)

        matches = True
        for (args, true_result) in ioexamples:
            try:
                computed_result = function.exec(args)
            except:
                matches = False

            if computed_result != true_result:
                # print("Function " + str(function) + " failed ")
                # print("Number of ^ was " + str(progno))
                matches = False
                break

        if matches:
            return (function, progno)

        progno += 1

    return (None, None)


if __name__ == "__main__":
    print("Enter some IO examples: (empty when done)")
    examples = []
    running = True
    while running:
        print("Eneter input values: (Comma separated)")
        vals = [int(x.strip()) for x in input().split(',') if x.strip()]
        print("Enter output for those inputs: (empty to stop adding)")
        output = input().strip()
        if output:
            output = int(output)
            examples.append((vals, output))
        else:
            running = False

    (genfunc, gennum) = synthesize(examples)
    if genfunc == None:
        print("Failed to find a function in the first " + str(MAX_PROGS) + " programs")
    else:
        print("Found a function! Number " + str(gennum))
        print("Function code is " + str(genfunc))

