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
	xlDiagonalDown:_("from upper left to lower right"),
	# Translators: borders index in Microsoft Excel.
	xlDiagonalUp:_("from lower left to upper right"),
	# Translators: borders index in Microsoft Excel.
	xlEdgeBottom:_("at the bottom edge"),
	# Translators: borders index in Microsoft Excel.
	xlEdgeLeft:_("at the left edge"),
	# Translators: borders index in Microsoft Excel.
	xlEdgeRight:_("at the right edge"),
	# Translators: borders index in Microsoft Excel.
	xlEdgeTop:_("at the top edge"),
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
	xlContinuous:_("continuous line"),
	xlDash:_("dashed line"),
	xlDashDot:_("alternating dashes and dots"),
	xlDashDotDot:_("dash followed by two dots"),
	xlDot:_("dotted line"),
	xlDouble:_("double line"),
	xlLineStyleNone:_("no line"),
	xlSlantDashDot:_("slanted dashes"),
}

def getCellBorderStyleDescription(bordersObj):
	items=[]
	for pos in bordersIndexLabels.keys():
		if bordersObj[pos].lineStyle != xlLineStyleNone:
			items.append(_("{color} {style} {position}").format(
				position=bordersIndexLabels.get(pos),
				style=borderStyleLabels.get(bordersObj[pos].lineStyle),
				color=colors.RGB.fromCOLORREF(int(bordersObj[pos].color)).name
			))
	return ', '.join(items)
