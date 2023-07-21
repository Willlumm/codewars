# https://www.codewars.com/kata/53e57dada0cb0400ba000688/train/python

def factorial(n):
    for m in range(2, n):
        n *= m
    return n

def count_perms(char_counts):
    perms = factorial(sum(char_counts.values()))
    for count in char_counts.values():
        if count == 0:
            continue
        perms /= factorial(count)
    return int(perms)

def list_position(word):
    """Return the anagram list position of the word"""
    char_counts = {char: word.count(char) for char in sorted(list(word))}
    total_perms = 1
    for char0 in word:
        for char, count in char_counts.items():
            if char == char0:
                break
            if count == 0:
                continue
            char_counts[char] -= 1
            total_perms += count_perms(char_counts)
            char_counts[char] += 1
        char_counts[char0] -= 1
    return total_perms
        

print(f"{list_position('A')} == 1")
print(f"{list_position('ABAB')} == 2")
print(f"{list_position('AAAB')} == 1")
print(f"{list_position('BAAA')} == 4")
print(f"{list_position('QUESTION')} == 24572")
print(f"{list_position('BOOKKEEPER')} == 10743")
