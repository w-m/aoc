def state_str(result, expected_result):
    if expected_result:
        return '✅' if result == expected_result else '❌'
    else:
        return "❔"

def run_expect(input_filename, input_reader_fn, compute_a_fn, expected_result_a=None, compute_b_fn=None, expected_result_b=None):
    
    print(input_filename)
    puzzle_input = input_reader_fn(input_filename)

    a, a_state = compute_a_fn(puzzle_input)
    
    print(f"a) {a} / {expected_result_a} {state_str(a, expected_result_a)}")

    if compute_b_fn:
        
        b, b_state = compute_b_fn(puzzle_input, a_state)

        print(f"b) {b} / {expected_result_b} {state_str(b, expected_result_b)}")
        print()
        return a, a_state, b, b_state

    return a, a_state, None, None

