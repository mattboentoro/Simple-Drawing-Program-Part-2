# "Simple" Drawing Program Part 2

Create a simple drawing program.

A picture is worth a thousand words. In this assignment, transform those words back into a picture. You'll
translate a drawing description into a PostScript file that will produce the specified picture. Your program should
read input from stdin and output the PostScript file to stdout.

## Numerical Expressions
A numerical expression can be a primitive expression or compound expression. Primitive expressions are as
follows:
```
N
```
where N is a floating-point number, e.g., 0, -1, 3.14
```
X
```
where X is a symbol. A symbol is a valid Python identifier. (You may call str.isidentifier() to
determine if a string is a valid identifier.) The last assignment to the symbol determines its value. If X does
not have a value, then the expression is invalid.

Compound numerical expressions are compositions of other numerical expressions (primitive or compound):
```
(+ A B)
```
The sum of A and B
```
(- A B)
```
The difference of A and B
```
(* A B)
```
The product of A and B
```
(/ A B)
```
The quotient of A and B
```
(sin A)
```
The sine of A degrees
```
(cos A)
```
The cosine of A degrees

Handle all numbers in floating point.

### Assignment

```
(:= X E)
```
Where X is a symbol and E a numerical expression. This command will evaluate the numerical expression
E, and then store that value to the symbol X. Any subsequent references to X before the next assignment
to X will evaluate to that value. For example, the following code: 
```
(:= X 1) (linewidth X) (:= X 2)
(line 0 0 X X) 
```
should produce
```
1
setlinewidth
0 0 moveto
2 2 lineto
```

## Input Language

A drawing consists of zero or more picture elements, with each element modified by zero or more
transformations. The drawing may also have zero or more parameter settings before any picture element. All
numbers should be handled in floating-point. The coordinate (0,0) is the origin and is the lower left corner of the
drawing. X-coordinate values increase to the right and y-coordinate values increase to the top.

### Picture Elements

Create picture elements using the commands below.
```
(line X0 Y0 X1 Y1)
```
Draw a line with one endpoint at (X0, Y0) and the second endpoint at (X1, Y1).
```
(rect X Y W H)
```
Draw an outline of a rectangle whose lower left corner is at (X,Y), and which has a width of W and height
of H. The rectangle should be drawn counter-clockwise starting from the lower left corner.
```
(filledrect X Y W H)
```
Same as rect, but fill the rectangle rather than simply drawing its boundary.
```
(filledrect X Y W H)
```
Same as rect, but fill the rectangle rather than simply drawing its boundary.
```
(tri X Y R)
```
Draw the outline of an equilateral triangle whose center is at (X, Y) with one of the vertices at (X + R, Y).  
Draw the triangle counter-clockwise starting from (X + R, Y). This order applies to all the following
picture elements.
```
(filledtri X Y R)
```
Same as tri, but fill the triangle rather than simply drawing its boundary.
```
(square X Y R)
```
Draw the outline of a square whose center is at (X, Y) with one of the vertices at (X + R, Y).
```
(filledsquare X Y R)
```
Same as square, but fill the square rather than simply drawing its boundary.
```
(penta X Y R)
```
Draw the outline of a regular pentagon whose center is at (X, Y) with one of the vertices at (X + R, Y).
```
(filledpenta X Y R)
```
Same as penta, but fill the pentagon rather than simply drawing its boundary.
```
(hexa X Y R)
```
Draw the outline of a regular hexagon whose center is at (X, Y) with one of the vertices at (X + R, Y).
```
(filledhexa X Y R)
```
Same as hexa, but fill the hexagon rather than simply drawing its boundary.
```
(ngon X Y R N)
```
Draw the outline of a regular N-gon for integer N > 2, whose center is at (X, Y) with one of the vertices at
(X + R, Y).
```
(filledngon X Y R N)
```
Same as ngon, but fill the ngon rather than simply drawing its boundary.

### Transformation Elements

Create transformations using the commands below.
```
(translate X Y)
```
Translate the following picture element by X units along the x-axis, and Y units along the y-axis.
```
(rotate X)
```
Rotate the following picture element by X degrees about the origin.
```
(scale S)
```
Scale the following picture element by a factor of S, where S > 0. If (X ,Y) was a vertice on the picture,
then its new coordinate after scaling is (X * S, Y * S).

### Drawing Parameters

Create drawing parameters using the commands below.
```
(color R G B)
```
Set the current color to (R,G,B). The arguments must be numbers between 0 and 1, inclusive. Initially, R =
G = B = 0 (i.e. black).
```
(linewidth W)
```
Set the current line width to W, which must be a non-negative number. This meaning of this width value is
as that of PostScript, meaning you can pass this value directly to PostScript commands. The initial value
of the line width is 1.

## Input Examples

Zero or more whitespaces are allowed between a parenthesis and the start or end of a command, and between
commands. At least one character of whitespace is required to separate arguments within a command.

For example, the following would draw a thick blue square, rotated 45 degrees.

```
(linewidth 5)
(color 0 0 1)
(rotate 45)(rect 100 100 100 100)
```

## PostScript
The output of your program will be a PostScript document. You can view a PostScript file with any PostScript
viewer. A popular one is gv available on Linux. A PostScript file has the following form:
```
%!PS-Adobe-3.1
commands
showpage
```
The commands of the PostScript language are in postfix notation. The actual PostScript language is free form,
meaning operands and operators can be separated by arbitrary whitespace. Your output, however, must mimic
the reference program to make your program easier to debug and grade. Each command will start on a newline
with operands separated by a single space.

The origin of a PostScript starts at (0,0) in the lower left corner, with x-coordinates increasing to the right and ycoordinates
increasing to the top. To draw something, one builds a path, and then strokes it. The PostScript
interpreter maintains a graphics state, which for our purposes consists of

- A current point, (x,y) coordinate, which is initially undefined  
- A current path  
- A current color, a 3-tuple (r,g,b), where each color intensity r,g,b is between 0 and 1 inclusive. (0,0,0) is
black and (1,1,1) is white  
- A current line thickness, which indicates the thickness of lines drawn when stroking  

You can use the following subset of the PostScript language to construct your PostScript file. In this subset, all
operands are decimal numbers (e.g. 0.1, 2.3, 45).

```
X Y moveto
```
Set the current point to (X, Y).
```
X Y lineto
```
Add a line segment to the current path starting at the current point and going to (X, Y), which becomes the
new current point.
```
fill
```
Fill the interior of the current line path with the current color. Clear the current path and set the current
point to undefined.
```
stroke
```
Draw lines with the current line width and color over all the segments in the current path. Clear the current
path and undefine the current point.
```
W setlinewidth
```
Set the current line width to W. The initial value of the line width is 1.
```
R G B setrgbcolor
```
Set the current color to (R, G, B).
