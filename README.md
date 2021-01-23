# graph-language
Compiled language to generate charts and graphs in HTML + CSS format.

## Setup instructions
1. Install **tox**.
2. Test and build by running `tox` in the project folder.
3. Single-file executable should be in a generated *dist* folder.

## How to run Glang on a file
Simplest version is `./glang -i <input file>`. This generates output CSS and HTML files in
the same directory as the executable.

You can get more information by running `./glang --help`.

## Language
### Variables
Variables are not typed, so an example of a variable definition would be simply `test_variable = 5;`.
Their type can be changed at any moment.
### Built-in data types
#### Boolean expressions
`true` and `false`, in boolean expressions every number except 0 translates to `true`.
You can use variables inside of boolean expressions (which resolve to a number) and functions (which, too, resolve to a number).

Boolean expressions use symbols `|` (OR) and `&` (AND) and `()` for grouping.

ex.: `0 & true`, `(5 > 2) | (a < 3)`
#### Numerical expressions
There's no distinction between integers and non-integers, every numerical value falls under the same type.
Expressions can contain numbers, `+`, `-`, `/`, `*`, variables and function calls.

ex.: `5`, `-12 * 123`, `a(2) * -24`
#### String
Strings are Python-like - you can use either `'` or `"` to mark the beginning and end of a string.
Of course both markers need to be identical in a single string definition.

ex.: `"test string"`, `'another test'`
#### Color
Colors are defined using a "hash" and 6 hexadecimal signs, just as for example in CSS.

ex.: `#ff1234`, `#a3f2d9`
#### Data Point
Data point contains information about the *x* and *y* value of a point that we later use to represent on a chart.
Additionally it can hold a color value for the specified point.

You can access all properties using a property access: `a.x`, `a.y`, `a.color`.
To access the color, you can also use the "hash" selector: `#a = #f0f0f0;`.

ex.: `<1, 15, #0f0f0f>` (x, y, color), `<-1, -15>` (x, y)
#### Named Value
Contains a label and a value to later be represented on a pie/bar chart.
Additionally it can hold a color value for the specified point.

You can access all properties using a property access: `a.value`, `a.label`, `a.color`.
To access the color, you can also use the "hash" selector: `#a = #f0f0f0;`.

ex.: `<'value', 1, #0f0f0f>` (label, value, color), `<'another value', 2>` (label, value)
#### List
List is handled the pythonic way - can store any value of any type.
Adding a value to the list is done using the `+=` operator.
Accessing a list value is done with the `[<integer>]` operator.

ex.:
```
a = ['test']; 
a += 5; 
a += <12,-12>; 
a += #ff0000;
```
#### JSON
Defining a JSON variable with member access later on:
```
a = {"test": 15};
b = a.'test'
c = a."test"
```
JSON variable definition with array access later on:
```
a = {"test": [125, {"test": "abc"}]};
b = a."test"[2]."test" // b equals "abc"
```
#### Built-in functions
Used to generate the HTML+CSS content, as of now theres only a few of them:
##### *pie(list_of_named_values, title)*
Creates a pie chart using a list of Named Values, with a specified title at the top.
##### *bar(list_of_names_values, title)*
Creates a bar chart using a list of Named Values, with a specified title at the top.
##### ~~*render(list_of_data_points, title)*~~ - ***WIP***
~~Creates a chart of an *y(x)* function, where *(x,y)* pairs are extracted from a list of Data Points.
Adds a title at the top of the chart.~~
### Functions
Functions can be defined only at the top level of user's code.
Functions can be called even if they are defined later in the code.
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
### For loop
Nothing special here, here's an example:
```
b = 0;
for(a=0; a<=4; a+=1) { 
    b += 1; 
} // b should be equal to 5
```
### If conditional
Again, very typical, ex.:
```
a = true;
if (!a | true) {
    a = false;
} // a should be false
```