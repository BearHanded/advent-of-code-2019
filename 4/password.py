INPUT_RANGE = (271983, 785961)


# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
def validate_password(num):
    has_adjacent = False
    increasing = True

    pastChar = ""
    str_num = str(num)
    curr_match = ""
    curr_match_count = 0
    for char in str_num:
        if char == pastChar and curr_match != char:
            curr_match = char
            curr_match_count = 2
        elif char == pastChar and curr_match == char:
            # Already matched on this character, clear tracking
            curr_match_count += 1
        elif char != pastChar and curr_match and curr_match_count == 2:
            has_adjacent = True
            break;

        pastChar = char

    # check if valid after last char in str
    if curr_match != "" and curr_match_count == 2:
        has_adjacent = True

    if not has_adjacent:
        return 0

    pastVal = 0
    for char in str_num:
        val = int(char)
        if pastVal > val:
            increasing = False
            break
        pastVal = int(char)

    if increasing and has_adjacent:
        return 1
    return 0


# RUN
print "--------- TESTS -----------"
print "111111: ", validate_password(111111)
print "223450: ", validate_password(223450)
print "123789: ", validate_password(123789)
print "112233: ", validate_password(112233)
print "123444: ", validate_password(123444)
print "111122: ", validate_password(111122)
print "---------------------------"


total = 0
for number in range(INPUT_RANGE[0], INPUT_RANGE[1]):
    total += validate_password(number)

print "TOTAL: ", total
