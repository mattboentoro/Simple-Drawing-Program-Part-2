import sys
import math
import inspect
import copy
import time
class Error(Exception):
    pass
class MissingParenthesisError(Error):
    pass
class EmptyArray(Error):
    pass
class Picture:
    def __init__(self):
        self.Xpoint=[]
        self.Ypoint=[]
        self.Transformation=[]
        self.Fill=False
    def RotatePoints(self,X,Y,OriX,OriY,Degree):
        Result1=OriX+math.cos(math.radians(Degree))*(X-OriX)-math.sin(math.radians(Degree))*(Y-OriY)
        Result2=OriY+math.sin(math.radians(Degree))*(X-OriX)+math.cos(math.radians(Degree))*(Y-OriY)
        return Result1,Result2
    def Rotate(self,Degree):
        for i in range(len(self.Xpoint)):
            X,Y=self.RotatePoints(self.Xpoint[i],self.Ypoint[i],0,0,Degree)
            self.Xpoint[i]=X
            self.Ypoint[i]=Y
    def Translate(self,X,Y):
        for i in range(len(self.Xpoint)):
            self.Xpoint[i]+=X
            self.Ypoint[i]+=Y
    def Scale(self,Amount):
        for i in range(len(self.Xpoint)):
            self.Xpoint[i]*=Amount
            self.Ypoint[i]*=Amount
    def RotateString(self,Degree):
        self.Transformation.append("rotate")
        self.Transformation.append(str(Degree))
    def TranslateString(self,X,Y):
        self.Transformation.append("translate")
        self.Transformation.append(str(X))
        self.Transformation.append(str(Y))
    def ScaleString(self,Amount):
        self.Transformation.append("scale")
        self.Transformation.append(str(Amount))
    def ApplyTransformation(self):
        while len(self.Transformation)>0:
            if self.Transformation[0]=="rotate":
                self.Rotate(float(eval(self.Transformation[1])))
                for i in range(2):
                    self.Transformation.pop(0)
            elif self.Transformation[0]=="scale":
                self.Scale(float(eval(self.Transformation[1])))
                for i in range(2):
                    self.Transformation.pop(0)
            elif self.Transformation[0]=="translate":
                self.Translate(float(eval(self.Transformation[1])),float(eval(self.Transformation[2])))
                for i in range(3):
                    self.Transformation.pop(0)
    def PlotPoint(self):
        print(str(self.Xpoint[0])+" "+str(self.Ypoint[0])+" "+"moveto")
        for i in range(1,len(self.Xpoint)):
            print(str(self.Xpoint[i])+" "+str(self.Ypoint[i])+" "+"lineto")
        if len(self.Xpoint)>2:
            print(str(self.Xpoint[0])+" "+str(self.Ypoint[0])+" "+"lineto")
        if self.Fill==True:
            print("fill")
        else:
            print("stroke")
class Rect(Picture):
    def __init__(self,x,y,width,height,fill):
        Picture.__init__(self)
        self.X=x
        self.Y=y
        self.Width=width
        self.Height=height
        self.Fill=fill
    def Draw(self):
        Xpo=float(eval(self.X))
        Ypo=float(eval(self.Y))
        Wid=float(eval(self.Width))
        Hei=float(eval(self.Height))
        self.Xpoint.append(Xpo)
        self.Ypoint.append(Ypo)
        self.Xpoint.append(self.Xpoint[len(self.Xpoint)-1]+Wid)
        self.Ypoint.append(self.Ypoint[len(self.Ypoint)-1])
        self.Xpoint.append(self.Xpoint[len(self.Xpoint)-1])
        self.Ypoint.append(self.Ypoint[len(self.Ypoint)-1]+Hei)
        self.Xpoint.append(self.Xpoint[len(self.Xpoint)-1]-Wid)
        self.Ypoint.append(self.Ypoint[len(self.Ypoint)-1])
        self.ApplyTransformation()
        self.PlotPoint()
class Line(Picture):
    def __init__(self,x1,y1,x2,y2):
        Picture.__init__(self)
        self.X1=x1
        self.Y1=y1
        self.X2=x2
        self.Y2=y2
        self.Fill=False
    def Draw(self):
        X1po=float(eval(self.X1))
        Y1po=float(eval(self.Y1))
        X2po=float(eval(self.X2))
        Y2po=float(eval(self.Y2))
        self.Xpoint.append(X1po)
        self.Xpoint.append(X2po)
        self.Ypoint.append(Y1po)
        self.Ypoint.append(Y2po)
        self.ApplyTransformation()
        self.PlotPoint()
class Ngon(Picture):
    def __init__(self,x,y,r,n,fill):
        Picture.__init__(self)
        self.X=x
        self.Y=y
        self.R=r
        self.N=n
        self.Fill=fill
    def Draw(self):
        Xpo=float(eval(self.X))
        Ypo=float(eval(self.Y))
        Rad=float(eval(self.R))
        Num=float(eval(self.N))
        self.Xpoint.append(Xpo+Rad)
        self.Ypoint.append(Ypo)
        Degree=360/int(Num)
        for i in range(1,int(Num)):
            Xnew,Ynew=self.RotatePoints(self.Xpoint[i-1],self.Ypoint[i-1],Xpo,Ypo,Degree)
            self.Xpoint.append(Xnew)
            self.Ypoint.append(Ynew)
        self.ApplyTransformation()
        self.PlotPoint()
class Sector(Picture):
    def __init__(self,X,Y,R,B,E,Fill):
        Picture.__init__(self)
        self.Xcenter=X
        self.Ycenter=Y
        self.Radius=R
        self.Bangle=B
        self.Eangle=E
        self.Fill=Fill
    def Draw(self):
        Xpt=float(eval(self.Xcenter))
        Ypt=float(eval(self.Ycenter))
        Rad=float(eval(self.Radius))
        Ban=float(eval(self.Bangle))
        Ean=float(eval(self.Eangle))
        while len(self.Transformation)>0:
            if self.Transformation[0]=="rotate":
                Ban+=float(eval(self.Transformation[1]))
                Ean+=float(eval(self.Transformation[1]))
                while Ban>=360:
                    Ban-=360
                while Ean>=360:
                    Ean-=360
                Xpt,Ypt=self.RotatePoints(Xpt,Ypt,0,0,float(eval(self.Transformation[1])))
                for i in range(2):
                    self.Transformation.pop(0)
            elif self.Transformation[0]=="scale":
                Xpt*=float(eval(self.Transformation[1]))
                Ypt*=float(eval(self.Transformation[1]))
                Rad*=float(eval(self.Transformation[1]))
                for i in range(2):
                    self.Transformation.pop(0)
            elif self.Transformation[0]=="translate":
                Xpt+=float(eval(self.Transformation[1]))
                Ypt+=float(eval(self.Transformation[2]))
                for i in range(3):
                    self.Transformation.pop(0)
        X1,Y1=self.RotatePoints(Xpt+Rad,Ypt,Xpt,Ypt,Ban)
        print(str(Xpt)+" "+str(Ypt)+" "+"moveto")
        print(str(X1)+" "+str(Y1)+" "+"lineto")
        print(str(Xpt)+" "+str(Ypt)+" "+str(Rad)+" "+str(Ban)+" "+str(Ean)+" arc")
        print(str(Xpt)+" "+str(Ypt)+" "+"lineto")
        if self.Fill==True:
            print("fill")
        else:
            print("stroke")
class Assignment:
    def __init__(self,var,val):
        self.Variable=var
        self.Value=val
    def Draw(self):
        Text=str(self.Variable)+" = "+str(self.Value)
        exec(Text,globals())
class Linewidth:
    def __init__(self,W):
        self.Width=W
    def Draw(self):
        print(str(eval(self.Width))+" setlinewidth")
class Color:
    def __init__(self,R,G,B):
        self.ColorR=R
        self.ColorG=G
        self.ColorB=B
    def Draw(self):
        print(str(eval(self.ColorR))+" "+str(eval(self.ColorG))+" "+str(eval(self.ColorB))+" setrgbcolor")
def Info():
    print("Type 1 for more information about the syntax, or type any other key to end")
    option=input("Type here...")
    if option=="1":
        print("\nPICTURE ELEMENT\n\n")
        print("(line X0 Y0 X1 Y1)")
        print("Draw a line with the first endpoint at (X0, Y0) and the second endpoint at (X1, Y1).\n")
        print("(rect X Y W H)")
        print("Draw the outline of a rectangle whose lower left corner is at (X,Y), and which has a width of W and height of H. Draw the rectangle counter-clockwise starting from the lower left corner.\n")
        print("(filledrect X Y W H)")
        print("Same as (rect ...), but fill the rectangle rather than simply drawing its boundary.\n")
        print("(tri X Y R)")
        print("Draw the outline of an equilateral triangle whose center is at (X, Y) with one of the vertices at (X + R, Y). Draw the triangle counter-clockwise starting from (X + R, Y). This order applies to all the following picture elements.\n")
        print("(filledtri X Y R)")
        print("Same as (tri ...), but fill the triangle rather than simply drawing its boundary.\n")
        print("(square X Y R)")
        print("Draw the outline of a square whose center is at (X, Y) with one of the vertices at (X + R, Y).\n")
        print("(filledsquare X Y R)")
        print("Same as (square ...), but fill the square rather than simply drawing its boundary.\n")
        print("(penta X Y R)")
        print("Draw the outline of a regular pentagon whose center is at (X, Y) with one of the vertices at (X + R, Y).\n")
        print("(filledpenta X Y R)")
        print("Same as (penta ...), but fill the pentagon rather than simply drawing its boundary.\n")
        print("(hexa X Y R)")
        print("Draw the outline of a regular hexagon whose center is at (X, Y) with one of the vertices at (X + R, Y).\n")
        print("(filledhexa X Y R)")
        print("Same as (hexa ...), but fill the hexagon rather than simply drawing its boundary.\n")
        print("(ngon X Y R N)")
        print("Draw the outline of a regular N-gon for integer N > 2, whose center is at (X, Y) with one of the vertices at (X + R, Y).\n")
        print("(filledngon X Y R N)")
        print("Same as (ngon ...), but fill the ngon rather than simply drawing its boundary.\n")
        print("(sector X Y R B E)")
        print("Draw the outline of a circular sector where (X, Y) is the center, R is the radius, B and E are the beginning and ending angles, respectively, measured in degrees counterclockwise from the positive x-axis. Draw this sector in the following order:")
        print("1. the line from the center to the beginning angle on the arc,")
        print("2. the arc from the beginning angle to the ending angle counterclockwise, and")
        print("3. the line from the ending angle on the arc back to the center.\n")
        print("(filledsector X Y R B E)")
        print("Same as (sector ...), but fill the circular sector rather than simply drawing its boundary.\n")
        print("(group P1 P2 ... PN)")
        print("Draw pictures P1 through PN, in that order. Any transformations applied to this picture element will be applied to all of the members of the group.")
        print("\n\nTRANSFORMATION\n\n")
        print("(translate P X Y)")
        print("Translate the picture P by X units along the x-axis and Y units along the y-axis.\n")
        print("(rotate P X)")
        print("Rotate the picture P by X degrees about the origin.\n")
        print("(scale P S)")
        print("Scale the picture P by a factor of S, where S > 0. If (X ,Y) was a vertice on the picture, then its new coordinate after scaling is (X * S, Y * S).")
        print("\n\nDRAWING PARAMETER\n\n")
        print("(color R G B)")
        print("Set the current color to (R,G,B). The arguments must be numbers between 0 and 1, inclusive. Initially, R = G = B = 0 (i.e. black).\n")
        print("(linewidth W)")
        print("Set the current line width to W, which must be a non-negative number. This meaning of this width value is as that of PostScript, meaning you can pass this value directly to PostScript commands. The initial value of the line width is 1.")
        print("\n\nCONTROL STRUCTURE\n\n")
        print("(for I L U E1 ... EN)")
        print("Execute commands E1 to EN multiple times, first with the symbol I set to the integer L, then to L+1, ..., up to and including U. Does nothing if U < L or N == 0 (e.g., there are no commands). At the end of the command, the symbol I has the value max(L, U).")
        print("\n\nASSIGNMENT\n\n")
        print("(:= X E)")
        print("Where X is a symbol and E a numerical expression. This command will evaluate the numerical expression E, and then store that value to the symbol X. Any subsequent references to X before the next assignment to X will evaluate to that value.")
        print("\n\nNUMERICAL EXPRESSION\n\n")
        print("(+ A B)")
        print("The sum of A and B\n")
        print("(- A B)")
        print("The difference of A and B\n")
        print("(* A B)")
        print("The product of A and B\n")
        print("(sin A)")
        print("The sine of A degrees\n")
        print("(cos A)")
        print("The cosine of A degreess\n")
def IsValid(command):
    Count=0
    ContainsBracket=False
    if command==[]:
        raise EmptyArray
    for items in command:
        if items=="(":
            Count+=1
            ContainsBracket=True
        elif items==")":
            Count-=1
    if Count!=0:
        raise MissingParenthesisError
    if ContainsBracket==False:
        raise SyntaxError
def Tokenize(command):
    command=command.replace("("," ( ")
    command=command.replace(")"," ) ")
    CommandArray=command.split()
    Parse(CommandArray)
def Parse(CommandArray):
    try:
        Continue=True
        IsValid(CommandArray)
        while Continue:
            Counter=0
            IndexOfStart=-1
            IndexOfEnd=-1
            Index=0
            while Index<len(CommandArray):
                if CommandArray[Index]=="(":
                    IndexOfStart=Index
                elif CommandArray[Index]==")":
                    IndexOfEnd=Index
                    break
                Index+=1
                if Index==len(CommandArray):
                    Continue=False
            if Continue==False:
                break
            if CommandArray[IndexOfStart+1]=="linewidth":
                CommandArray[IndexOfStart]=Linewidth(CommandArray[IndexOfStart+2])
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="color":
                CommandArray[IndexOfStart]=Color(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4])
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="rect":
                CommandArray[IndexOfStart]=Rect(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],CommandArray[IndexOfStart+5],False)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="filledrect":
                CommandArray[IndexOfStart]=Rect(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],CommandArray[IndexOfStart+5],True)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="line":
                CommandArray[IndexOfStart]=Line(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],CommandArray[IndexOfStart+5])
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="tri":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],"3",False)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="filledtri":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],"3",True)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="square":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],"4",False)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="filledsquare":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],"4",True)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="penta":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],"5",False)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="filledpenta":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],"5",True)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="hexa":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],"6",False)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="filledhexa":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],"6",True)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="ngon":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],CommandArray[IndexOfStart+5],False)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="filledngon":
                CommandArray[IndexOfStart]=Ngon(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],CommandArray[IndexOfStart+5],True)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="sector":
                CommandArray[IndexOfStart]=Sector(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],CommandArray[IndexOfStart+5],CommandArray[IndexOfStart+6],False)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="filledsector":
                CommandArray[IndexOfStart]=Sector(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4],CommandArray[IndexOfStart+5],CommandArray[IndexOfStart+6],True)
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="group":
                SecondaryArray=[]
                for i in range (IndexOfStart+2,IndexOfEnd):
                    if isinstance(CommandArray[i],list):
                        for j in range(len(CommandArray[i])):
                            SecondaryArray.append(copy.deepcopy(CommandArray[i][j]))
                    else:
                        SecondaryArray.append(copy.deepcopy(CommandArray[i]))
                CommandArray[IndexOfStart]=SecondaryArray
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="rotate":
                if isinstance(CommandArray[IndexOfStart+2],list):
                    for i in range(len(CommandArray[IndexOfStart+2])):
                        CommandArray[IndexOfStart+2][i].RotateString(CommandArray[IndexOfStart+3])
                else:
                    CommandArray[IndexOfStart+2].RotateString(CommandArray[IndexOfStart+3])
                CommandArray[IndexOfStart]=CommandArray[IndexOfStart+2]
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="translate":
                if isinstance(CommandArray[IndexOfStart+2],list):
                    for i in range(len(CommandArray[IndexOfStart+2])):
                        CommandArray[IndexOfStart+2][i].TranslateString(CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4])
                else:
                    CommandArray[IndexOfStart+2].TranslateString(CommandArray[IndexOfStart+3],CommandArray[IndexOfStart+4])
                CommandArray[IndexOfStart]=CommandArray[IndexOfStart+2]
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="scale":
                if isinstance(CommandArray[IndexOfStart+2],list):
                    for i in range(len(CommandArray[IndexOfStart+2])):
                        CommandArray[IndexOfStart+2][i].ScaleString(CommandArray[IndexOfStart+3])
                else:
                    CommandArray[IndexOfStart+2].ScaleString(CommandArray[IndexOfStart+3])
                CommandArray[IndexOfStart]=CommandArray[IndexOfStart+2]
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]==":=":
                CommandArray[IndexOfStart]=Assignment(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+3])
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="+":
                CommandArray[IndexOfStart]="( "+CommandArray[IndexOfStart+2]+" + "+CommandArray[IndexOfStart+3]+" )"
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="-":
                CommandArray[IndexOfStart]="( "+CommandArray[IndexOfStart+2]+" - "+CommandArray[IndexOfStart+3]+" )"
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="*":
                CommandArray[IndexOfStart]="( "+CommandArray[IndexOfStart+2]+" * "+CommandArray[IndexOfStart+3]+" )"
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="/":
                CommandArray[IndexOfStart]="( "+CommandArray[IndexOfStart+2]+" / "+CommandArray[IndexOfStart+3]+" )"
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="sin":
                CommandArray[IndexOfStart]="( "+"math.sin(math.radians("+CommandArray[IndexOfStart+2]+"))"+" )"
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="cos":
                CommandArray[IndexOfStart]="( "+"math.cos(math.radians("+CommandArray[IndexOfStart+2]+"))"+" )"
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            elif CommandArray[IndexOfStart+1]=="for":
                if (int(CommandArray[IndexOfStart+4])>=int(CommandArray[IndexOfStart+3]))and CommandArray[IndexOfStart+5]!=")":
                    SecondaryArray=[]
                    for i in range(int(eval(CommandArray[IndexOfStart+3])),int(eval(CommandArray[IndexOfStart+4]))+1):
                        SecondaryArray.append(Assignment(CommandArray[IndexOfStart+2],str(i)))
                        for j in range(IndexOfStart+5,IndexOfEnd):
                            if isinstance(CommandArray[j],list):
                                for k in range(len(CommandArray[j])):
                                    SecondaryArray.append(copy.deepcopy(CommandArray[j][k]))
                            else:
                                SecondaryArray.append(copy.deepcopy(CommandArray[j]))
                    SecondaryArray.append(Assignment(CommandArray[IndexOfStart+2],CommandArray[IndexOfStart+4]))
                    CommandArray[IndexOfStart]=SecondaryArray
                else:
                    MaxIndex=max(int(eval(CommandArray[IndexOfStart+3])),int(eval(CommandArray[IndexOfStart+4])))
                    CommandArray[IndexOfStart]=Assignment(CommandArray[IndexOfStart+2],str(MaxIndex))
                for i in range(IndexOfStart+1,IndexOfEnd+1):
                    CommandArray.pop(IndexOfStart+1)
            else:
                raise SyntaxError
        print("%!PS-Adobe-3.0 EPSF-3.0")
        print("%%BoundingBox: 0 0 1239 1752")        
        for i in range(len(CommandArray)):
            if isinstance(CommandArray[i],list):
                for j in range(len(CommandArray[i])):
                    CommandArray[i][j].Draw()
            else:
                CommandArray[i].Draw()
        CommandArray=[]
    except NameError:
        print("Error Code 01 - Name Error:")
        print("Put assignment statement before calling the variable, or use for loop with the variable.")
    except AttributeError:
        print("Error Code 02 - Attribute Error:")
        print("Use for-loop in the outermost layer.")
    except SyntaxError:
        print("Error Code 03 - Syntax Error:")
        print("Add the appropiate number of parameter(s), use the correct keyword (eg. rect, line, rotate, for), or use the appropiate variable.")
        Info()
    except ZeroDivisionError:
        print("Error Code 04 - Zero Division Error:")
        print("Do not divide anything with 0.")
    except TypeError:
        print("Error Code 05 - Type Error:")
        print("Use the valid type of parameter.")
        Info()
    except MissingParenthesisError:
        print("Error Code 06 - Missing Parenthesis Error:")
        print("Add the closing bracket to the input.")
    except EmptyArray:
        print("Error Code 07 - Empty Stack Error:")
        print("No input has been detected.")
textcommand=""
text=sys.stdin.read().splitlines()
for i in range(len(text)):
    textcommand+=text[i]+" "

Tokenize(textcommand)
