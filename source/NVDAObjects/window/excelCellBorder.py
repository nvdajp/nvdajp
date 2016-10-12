#NVDAObjects/window/excelCellBorder.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 Takuya Nishimoto
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import colors
# XlBordersIndex Enumeration
# see https://msdn.microsoft.com/en-us/library/office/ff835915.aspx
xlDiagonalDown = 5
xlDiagonalUp = 6
xlEdgeBottom = 9
xlEdgeLeft = 7
xlEdgeRight = 10
xlEdgeTop = 8
xlInsideHorizontal = 12
xlInsideVertical = 11
bordersIndexLabels={
	# Translators: borders index in Microsoft Excel.
	xlDiagonalDown:_("down-right diagonal line"),
	# Translators: borders index in Microsoft Excel.
	xlDiagonalUp:_("up-right diagonal line"),
	# Translators: borders index in Microsoft Excel.
	xlEdgeBottom:_("bottom edge"),
	# Translators: borders index in Microsoft Excel.
	xlEdgeLeft:_("left edge"),
	# Translators: borders index in Microsoft Excel.
	xlEdgeRight:_("right edge"),
	# Translators: borders index in Microsoft Excel.
	xlEdgeTop:_("top edge"),
	# Translators: borders index in Microsoft Excel.
	xlInsideHorizontal:_("horizontal borders except outside"),
	# Translators: borders index in Microsoft Excel.
	xlInsideVertical:_("vertical borders except outside"),
}
# XlLineStyle Enumeration
# see https://msdn.microsoft.com/en-us/library/office/ff821622.aspx
xlContinuous = 1
xlDash = -4115
xlDashDot = 4
xlDashDotDot = 5
xlDot = -4118
xlDouble = -4119
xlLineStyleNone = -4142
xlSlantDashDot = 13
borderStyleLabels={
	# Translators: border styles in Microsoft Excel.
	xlContinuous:_("continuous"),
	xlDash:_("dashed"),
	xlDashDot:_("alternating dashes and dots"),
	xlDashDotDot:_("dash followed by two dots"),
	xlDot:_("dotted"),
	xlDouble:_("double"),
	xlSlantDashDot:_("slanted dashes"),
}

def getCellBorderStyleDescription(bordersObj):
	d={}
	for pos in bordersIndexLabels.keys():
		if bordersObj[pos].lineStyle != xlLineStyleNone:
			d[pos]=_("{color} {style}").format(
				style=borderStyleLabels.get(bordersObj[pos].lineStyle),
				color=colors.RGB.fromCOLORREF(int(bordersObj[pos].color)).name
			)
	s=[]
	if d.get(xlEdgeTop) == d.get(xlEdgeBottom) == d.get(xlEdgeLeft) == d.get(xlEdgeRight) and d.get(xlEdgeTop) is not None:
		s.append(_("{desc} surrounding border").format(desc=d.get(xlEdgeTop)))
		del d[xlEdgeTop]
		del d[xlEdgeBottom]
		del d[xlEdgeLeft]
		del d[xlEdgeRight]
	if d.get(xlEdgeTop) == d.get(xlEdgeBottom) and d.get(xlEdgeTop) is not None:
		s.append(_("{desc} top and bottom edges").format(desc=d.get(xlEdgeTop)))
		del d[xlEdgeTop]
		del d[xlEdgeBottom]
	if d.get(xlEdgeLeft) == d.get(xlEdgeRight) and d.get(xlEdgeLeft) is not None:
		s.append(_("{desc} left and right edges").format(desc=d.get(xlEdgeLeft)))
		del d[xlEdgeLeft]
		del d[xlEdgeRight]
	if d.get(xlDiagonalUp) == d.get(xlDiagonalDown) and d.get(xlDiagonalUp) is not None:
		s.append(_("{desc} up-right and down-right diagonal lines").format(desc=d.get(xlDiagonalUp)))
		del d[xlDiagonalUp]
		del d[xlDiagonalDown]
	for pos,desc in d.items():
		s.append(_("{desc} {position}").format(
			desc=desc,
			position=bordersIndexLabels.get(pos)
		))
	return ', '.join(s)
