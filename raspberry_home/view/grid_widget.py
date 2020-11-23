from typing import Callable, Optional

from raspberry_home.view.stack import HorizontalStack, StackDistribution, VerticalStack
from raspberry_home.view.view import View
from raspberry_home.view.widget import Widget


class GridWidget(Widget):

    class Index:
        def __init__(self, column: int, row: int, index: int):
            self.column = column
            self.row = row
            self.index = index

    def __init__(self, columns: int, rows: int, builder: Callable[[Index], Optional[View]]):
        self.columns = columns
        self.rows = rows
        self.builder = builder

    def build(self) -> View:
        rows = []
        _index = 0
        for row in range(0, self.rows):
            cells = []
            for column in range(0, self.columns):
                index = GridWidget.Index(row, column, _index)
                cell = self.builder(index)
                _index += 1
                cells.append(cell)
            rows.append(HorizontalStack(
                distribution=StackDistribution.Equal,
                children=cells
            ))
        return VerticalStack(
            distribution=StackDistribution.Equal,
            children=rows
        )
