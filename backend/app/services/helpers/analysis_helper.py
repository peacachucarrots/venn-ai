def describe_option(option, question):
    """
    Return a human-friendly string for an Option, handling half-steps like 3.5.
    """
    if option.label:
        return option.label

    val = float(option.numeric_value)

    low = int(val)
    high = low + 1
    opt_low  = next(o for o in question.options if int(o.numeric_value) == low)
    opt_high = next(o for o in question.options if int(o.numeric_value) == high)

    return (
        f"A mix of “{opt_low.label}” and “{opt_high.label}”"
    )