def convert_case(s: str, case_type: str = "upper") -> str:
    """
    case_type options:
        upper = all upper case (Default)
        lower = all lower case
        title = all title case
    """

    if case_type == "upper":
        return s.upper()
    elif case_type == "lower":
        return s.lower()
    else:
        return s.title()
    
print(convert_case("hello World!"))