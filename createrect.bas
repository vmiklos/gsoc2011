Sub CreateRect
	dim aPoint as new com.sun.star.awt.Point
	dim aSize as new com.sun.star.awt.Size
	aPoint.x = 1000
	aPoint.y = 1000
	aSize.Width = 10000
	aSize.Height = 10000
	oRectangleShape = thisComponent.createInstance("com.sun.star.drawing.RectangleShape")
	oRectangleShape.Size = aSize
	oRectangleShape.Position = aPoint
	thisComponent.getDrawPage(0).add(oRectangleShape)
End Sub
