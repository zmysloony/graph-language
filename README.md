# graph-language
Compiled language to generate charts and graphs in HTML + CSS format.

## Setup instructions
1. Run `pip install -r requirements.txt`

## Language
### Variables
Variables are not typed, so an example of a variable definition would be simply `test_variable = 5;`.
Their type can be changed at any moment.
### Built-in data types
#### Boolean
`true` and `false`, in logical expressions every number except 0 translates to `true`.

Boolean (logical) expressions use symbols `|` (OR) and `&` (AND).
### Functions
Functions can be defined anywhere, although they can be defined **only once**.
Functions can be called only if they were defined earlier in the code.
It is impossible to access variables outside function's own scope.

Example function definition:
```
def test(a, b, c) {
    return a/b+c;
}
```
Example function call with assignment:
```
a = test(z, x, c);
```
